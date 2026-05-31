from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Optional


class CompressionLevel(str, Enum):
    FULL = "FULL"
    COMPRESSED = "COMPRESSED"
    CONSTRAINT_ONLY = "CONSTRAINT_ONLY"
    OMIT = "OMIT"


COMPRESSION_ORDER = [
    CompressionLevel.FULL,
    CompressionLevel.COMPRESSED,
    CompressionLevel.CONSTRAINT_ONLY,
    CompressionLevel.OMIT,
]


@dataclass
class CandidateNode:
    id: str
    title: str
    node_type: str
    zone: int
    distance: int
    retrieval_weight: float
    injection_weight: float
    recency_rank: int
    review_required: bool
    content: Dict[str, str]
    tags: List[str] = field(default_factory=list)
    block: Optional[str] = None
    compression: CompressionLevel = CompressionLevel.FULL
    included: bool = True
    rationale: str = ""


@dataclass
class Block:
    key: str
    title: str
    body: str
    token_count: int
    node_ids: List[str]


@dataclass
class CompressionEvent:
    iteration: int
    node_id: str
    title: str
    from_level: CompressionLevel
    to_level: CompressionLevel
    tokens_before: int
    tokens_after: int
    total_before: int
    total_after: int
    reason: str


@dataclass
class CompositionResult:
    context_string: str
    blocks: List[Block]
    nodes: List[CandidateNode]
    context_tokens: int
    system_tokens: int
    user_tokens: int
    total_tokens: int
    token_budget: int
    fits_budget: bool
    requires_human_review: bool
    compression_log: List[CompressionEvent]
