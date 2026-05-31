from __future__ import annotations

from .models import CandidateNode


def _clamp(value: float, lower: float = 0.0, upper: float = 1.0) -> float:
    return max(lower, min(upper, value))


def normalize_node(node: CandidateNode) -> CandidateNode:
    node.retrieval_weight = round(_clamp(node.retrieval_weight), 2)
    node.injection_weight = round(_clamp(node.injection_weight), 2)
    if node.node_type == "CONSTRAINT":
        node.rationale = "Protected constraint: always included at full fidelity."
    elif node.injection_weight >= 0.75:
        node.rationale = "High injection weight: deserves rich context in the final prompt."
    elif node.injection_weight >= 0.45:
        node.rationale = "Medium injection weight: will compress only if budget pressure appears."
    else:
        node.rationale = "Low injection weight: first candidate for aggressive compression."
    return node
