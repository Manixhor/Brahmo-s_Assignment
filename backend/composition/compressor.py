from __future__ import annotations

from .models import COMPRESSION_ORDER, CandidateNode, CompressionLevel


def initial_level(node: CandidateNode) -> CompressionLevel:
    return CompressionLevel.FULL


def apply_initial_compression(nodes: list[CandidateNode]) -> None:
    for node in nodes:
        node.compression = initial_level(node)
        node.included = node.compression != CompressionLevel.OMIT


def demote(node: CandidateNode) -> CompressionLevel | None:
    if node.node_type == "CONSTRAINT":
        return None
    current_index = COMPRESSION_ORDER.index(node.compression)
    if current_index >= len(COMPRESSION_ORDER) - 1:
        return None
    node.compression = COMPRESSION_ORDER[current_index + 1]
    node.included = node.compression != CompressionLevel.OMIT
    return node.compression
