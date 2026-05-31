from __future__ import annotations

from typing import Dict, List, Tuple

from .models import CandidateNode


BLOCK_ORDER: List[Tuple[str, str]] = [
    ("role", "ROLE"),
    ("global_constraints", "GLOBAL CONSTRAINTS"),
    ("recent_decisions", "RECENT DECISIONS"),
    ("active_constraints", "ACTIVE CONSTRAINTS"),
    ("session_context", "SESSION-SPECIFIC CONTEXT"),
    ("open_questions", "OPEN QUESTIONS"),
    ("stale_flags", "STALE FLAGS"),
    ("session_boundaries", "SESSION BOUNDARIES"),
]


def assign_blocks(nodes: List[CandidateNode]) -> Dict[str, List[CandidateNode]]:
    grouped: Dict[str, List[CandidateNode]] = {key: [] for key, _ in BLOCK_ORDER}

    for node in nodes:
        if node.review_required:
            node.block = "stale_flags"
        elif node.node_type == "CONSTRAINT" and node.zone == 2:
            node.block = "global_constraints"
        elif node.node_type == "DECISION":
            node.block = "recent_decisions"
        elif node.node_type == "CONSTRAINT" and node.zone == 1:
            node.block = "active_constraints"
        else:
            node.block = "session_context"
        grouped[node.block].append(node)

    grouped["recent_decisions"].sort(key=lambda item: (item.recency_rank, -item.injection_weight))
    grouped["global_constraints"].sort(key=lambda item: (-item.injection_weight, item.distance))
    grouped["active_constraints"].sort(key=lambda item: (-item.injection_weight, item.distance))
    grouped["session_context"].sort(key=lambda item: (item.distance, -item.injection_weight, item.id))
    grouped["stale_flags"].sort(key=lambda item: (item.distance, item.id))

    return grouped
