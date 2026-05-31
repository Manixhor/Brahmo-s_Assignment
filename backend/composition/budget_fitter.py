from __future__ import annotations

from typing import Callable, Dict, List, Tuple

from .compressor import demote
from .models import CandidateNode, CompressionEvent
from .token_counter import TokenCounter


def _select_node(nodes: List[CandidateNode]) -> CandidateNode | None:
    candidates = [node for node in nodes if node.node_type != "CONSTRAINT" and node.compression.value != "OMIT"]
    if not candidates:
        return None
    return min(candidates, key=lambda item: (item.injection_weight, -item.distance, item.recency_rank, item.id))


def fit_to_budget(
    nodes: List[CandidateNode],
    grouped: Dict[str, List[CandidateNode]],
    token_counter: TokenCounter,
    build_current: Callable[[], Tuple[list, str]],
    token_budget: int,
    system_prompt_reserve: int,
    user_message_reserve: int,
) -> Dict[str, object]:
    compression_log: List[CompressionEvent] = []
    requires_human_review = False
    iteration = 0

    while True:
        _, context_before = build_current()
        total_before = system_prompt_reserve + token_counter.count_text(context_before) + user_message_reserve
        if total_before <= token_budget:
            break

        node = _select_node(nodes)
        if node is None:
            requires_human_review = True
            break

        iteration += 1
        from_level = node.compression
        node_text_before = node.content[from_level.value.lower()] if from_level.value.lower() in node.content else ""
        next_level = demote(node)
        if next_level is None:
            requires_human_review = True
            break

        _, context_after = build_current()
        total_after = system_prompt_reserve + token_counter.count_text(context_after) + user_message_reserve
        node_text_after = node.content[next_level.value.lower()] if next_level.value.lower() in node.content else ""
        compression_log.append(
            CompressionEvent(
                iteration=iteration,
                node_id=node.id,
                title=node.title,
                from_level=from_level,
                to_level=next_level,
                tokens_before=token_counter.count_text(node_text_before),
                tokens_after=token_counter.count_text(node_text_after),
                total_before=total_before,
                total_after=total_after,
                reason="Lowest injection-weight non-constraint under budget pressure.",
            )
        )

    return {
        "compression_log": compression_log,
        "requires_human_review": requires_human_review,
    }
