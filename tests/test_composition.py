from __future__ import annotations

import json
import subprocess
import unittest
from pathlib import Path

from backend.composition.context_builder import compose_context


ROOT = Path(__file__).resolve().parents[1]
SEED = ROOT / "data" / "seed_data.json"


class CompositionTests(unittest.TestCase):
    def test_seed_has_28_candidates(self) -> None:
        payload = json.loads(SEED.read_text())
        self.assertEqual(len(payload["candidate_nodes"]), 28)

    def test_default_budget_fits(self) -> None:
        result = compose_context(SEED, token_budget=4000)
        self.assertTrue(result.fits_budget)
        self.assertFalse(result.requires_human_review)
        self.assertLessEqual(result.total_tokens, 4000)

    def test_constraints_remain_full(self) -> None:
        result = compose_context(SEED, token_budget=2200)
        constraints = [node for node in result.nodes if node.node_type == "CONSTRAINT"]
        self.assertTrue(constraints)
        self.assertTrue(all(node.compression.value == "FULL" for node in constraints))

    def test_low_budget_triggers_review(self) -> None:
        result = compose_context(SEED, token_budget=1200)
        self.assertTrue(result.requires_human_review or result.fits_budget)
        if result.requires_human_review:
            self.assertFalse(result.fits_budget)

    def test_open_questions_block_present(self) -> None:
        result = compose_context(SEED, token_budget=4000)
        titles = [block.title for block in result.blocks]
        self.assertIn("OPEN QUESTIONS", titles)

    def test_large_budget_keeps_all_nodes_full(self) -> None:
        result = compose_context(SEED, token_budget=999999)
        self.assertTrue(all(node.compression.value == "FULL" for node in result.nodes))
        self.assertEqual(len(result.nodes), 28)

    def test_module_entrypoint_runs(self) -> None:
        completed = subprocess.run(
            ["python3", "-m", "backend.demo", "--budget", "4000", "--json"],
            cwd=ROOT,
            check=False,
            capture_output=True,
            text=True,
        )
        self.assertEqual(completed.returncode, 0, completed.stderr)
        payload = json.loads(completed.stdout)
        self.assertIn("fits_budget", payload)


if __name__ == "__main__":
    unittest.main()
