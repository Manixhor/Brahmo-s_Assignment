from __future__ import annotations

import argparse
import json
from pathlib import Path

try:
    from .composition import compose_context
except ImportError:  # pragma: no cover
    from composition import compose_context


ROOT = Path(__file__).resolve().parents[1]
SEED_PATH = ROOT / "data" / "seed_data.json"


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run the BRAHMO composition demo.")
    parser.add_argument("--budget", type=int, default=4000, help="Total token budget including reserves.")
    parser.add_argument("--json", action="store_true", help="Print machine-readable summary.")
    parser.add_argument("--show-protected", action="store_true", help="Print protected constraints.")
    parser.add_argument("--focus", nargs="*", default=[], help="Highlight selected node ids.")
    return parser


def main() -> None:
    args = build_parser().parse_args()
    result = compose_context(SEED_PATH, token_budget=args.budget)

    if args.json:
        payload = {
            "budget": result.token_budget,
            "fits_budget": result.fits_budget,
            "requires_human_review": result.requires_human_review,
            "system_tokens": result.system_tokens,
            "context_tokens": result.context_tokens,
            "user_tokens": result.user_tokens,
            "total_tokens": result.total_tokens,
            "blocks": [
                {"title": block.title, "tokens": block.token_count, "node_ids": block.node_ids}
                for block in result.blocks
            ],
            "compression_log": [
                {
                    "iteration": event.iteration,
                    "node_id": event.node_id,
                    "from": event.from_level.value,
                    "to": event.to_level.value,
                    "total_before": event.total_before,
                    "total_after": event.total_after,
                }
                for event in result.compression_log
            ],
        }
        print(json.dumps(payload, indent=2))
        return

    print("BRAHMO Composition Agent Demo")
    print("=" * 32)
    print(f"Budget: {result.token_budget}")
    print(f"System reserve: {result.system_tokens}")
    print(f"Context: {result.context_tokens}")
    print(f"User reserve: {result.user_tokens}")
    print(f"Total: {result.total_tokens}")
    print(f"Fits budget: {'YES' if result.fits_budget else 'NO'}")
    print(f"Human review required: {'YES' if result.requires_human_review else 'NO'}")
    print()
    print("Block summary:")
    for block in result.blocks:
        print(f"- {block.title}: {block.token_count} tokens, {len(block.node_ids)} nodes")
    print()
    print("Compression log:")
    if not result.compression_log:
        print("- No compression needed.")
    else:
        for event in result.compression_log:
            print(
                f"- Pass {event.iteration}: {event.node_id} {event.from_level.value} -> {event.to_level.value} "
                f"({event.total_before} -> {event.total_after})"
            )
    if args.show_protected:
        print()
        print("Protected constraints:")
        for node in result.nodes:
            if node.node_type == "CONSTRAINT":
                print(f"- {node.id}: {node.title} [{node.compression.value}]")

    if args.focus:
        print()
        print("Focus nodes:")
        for focus_id in args.focus:
            matches = [node for node in result.nodes if node.id == focus_id]
            if not matches:
                print(f"- {focus_id}: not found")
                continue
            node = matches[0]
            print(
                f"- {node.id}: rw={node.retrieval_weight}, iw={node.injection_weight}, "
                f"block={node.block}, compression={node.compression.value}"
            )

    print()
    print("Final context preview:")
    print(result.context_string[:1800] + ("..." if len(result.context_string) > 1800 else ""))


if __name__ == "__main__":
    main()
