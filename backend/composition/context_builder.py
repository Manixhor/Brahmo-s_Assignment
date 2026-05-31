from __future__ import annotations

import json
from pathlib import Path
from typing import Dict, List, Tuple

from .block_assembler import BLOCK_ORDER, assign_blocks
from .budget_fitter import fit_to_budget
from .compressor import apply_initial_compression
from .importance_scorer import normalize_node
from .models import Block, CandidateNode, CompositionResult
from .token_counter import TokenCounter


def load_seed_data(seed_path: Path) -> Dict:
    return json.loads(seed_path.read_text())


def _render_node(node: CandidateNode) -> str:
    if not node.included:
        return ""
    level = node.compression.value.lower()
    content = node.content[level]
    return f"- [{node.id}] {node.title} ({node.node_type}, {node.compression.value}, rw={node.retrieval_weight}, iw={node.injection_weight})\n  {content}"


def _build_blocks(
    grouped: Dict[str, List[CandidateNode]],
    token_counter: TokenCounter,
    role_frame: str,
    boundary_text: str,
) -> Tuple[List[Block], str]:
    bodies: Dict[str, str] = {
        "role": role_frame,
        "open_questions": "No open questions captured in v0.1.",
        "session_boundaries": boundary_text,
    }

    for key in ("global_constraints", "recent_decisions", "active_constraints", "session_context", "stale_flags"):
        lines = [_render_node(node) for node in grouped[key] if node.included]
        bodies[key] = "\n".join(line for line in lines if line).strip()

    blocks: List[Block] = []
    sections: List[str] = []
    for key, title in BLOCK_ORDER:
        body = bodies.get(key, "").strip()
        if key not in {"role", "open_questions", "session_boundaries"} and not body:
            continue
        token_count = token_counter.count_text(body)
        node_ids = [node.id for node in grouped.get(key, []) if node.included]
        blocks.append(Block(key=key, title=title, body=body, token_count=token_count, node_ids=node_ids))
        sections.append(f"=== {title} ===\n{body}")

    return blocks, "\n\n".join(sections)


def compose_context(
    seed_path: Path,
    token_budget: int = 4000,
    system_prompt_reserve: int = 800,
    user_message_reserve: int = 200,
) -> CompositionResult:
    raw = load_seed_data(seed_path)
    token_counter = TokenCounter()
    nodes = [normalize_node(CandidateNode(**item)) for item in raw["candidate_nodes"]]
    apply_initial_compression(nodes)

    role_frame = (
        f"You are assisting {raw['user']['name']}, {raw['user']['role']} in {raw['user']['department']}, "
        f"for patient {raw['patient']['name']}. Prioritize hospital safety constraints, recent decisions, "
        f"and patient-specific treatment details before incidental facts."
    )
    boundary_text = "Capture new decisions, review unresolved warnings, and preserve changed constraints after the session."
    grouped = assign_blocks(nodes)

    def build_current() -> Tuple[List[Block], str]:
        return _build_blocks(grouped, token_counter, role_frame, boundary_text)

    fit_result = fit_to_budget(
        nodes=nodes,
        grouped=grouped,
        token_counter=token_counter,
        build_current=build_current,
        token_budget=token_budget,
        system_prompt_reserve=system_prompt_reserve,
        user_message_reserve=user_message_reserve,
    )

    blocks, context_string = build_current()
    context_tokens = token_counter.count_text(context_string)
    total_tokens = system_prompt_reserve + context_tokens + user_message_reserve

    return CompositionResult(
        context_string=context_string,
        blocks=blocks,
        nodes=nodes,
        context_tokens=context_tokens,
        system_tokens=system_prompt_reserve,
        user_tokens=user_message_reserve,
        total_tokens=total_tokens,
        token_budget=token_budget,
        fits_budget=total_tokens <= token_budget,
        requires_human_review=fit_result["requires_human_review"],
        compression_log=fit_result["compression_log"],
    )
