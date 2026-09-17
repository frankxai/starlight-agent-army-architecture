#!/usr/bin/env python3
"""Deterministic unit tests for scorecard math; no model or network calls."""
from __future__ import annotations

import json
import subprocess
import sys
import unittest
from pathlib import Path

from calculate_agent_scorecard import compare, deduplicated_value, nearest_rank_p95

ROOT = Path(__file__).resolve().parents[1]


class ScorecardMathTests(unittest.TestCase):
    def test_overlap_groups_are_not_double_counted(self) -> None:
        receipt = {
            "outcome": {
                "value_components": [
                    {
                        "amount_usd": 10,
                        "attribution_confidence": 0.5,
                        "overlap_group": "same-benefit",
                    },
                    {
                        "amount_usd": 8,
                        "attribution_confidence": 0.9,
                        "overlap_group": "same-benefit",
                    },
                    {
                        "amount_usd": 3,
                        "attribution_confidence": 1.0,
                        "overlap_group": None,
                    },
                ]
            }
        }
        self.assertEqual(deduplicated_value(receipt, False), 13)
        self.assertEqual(deduplicated_value(receipt, True), 10.2)

    def test_nearest_rank_p95(self) -> None:
        self.assertEqual(nearest_rank_p95([10, 20, 30]), 30)
        self.assertIsNone(nearest_rank_p95([]))

    def test_target_operators(self) -> None:
        self.assertTrue(compare(0.95, ">=", 0.95))
        self.assertTrue(compare(3.0, "<", 4.0))
        self.assertFalse(compare(3.0, ">", 4.0))
        self.assertIsNone(compare(None, ">=", 1.0))

    def test_synthetic_profile_stays_insufficient(self) -> None:
        command = [
            sys.executable,
            str(ROOT / "scripts" / "calculate_agent_scorecard.py"),
            "--profile",
            str(ROOT / "observability" / "deployments" / "gencreator-studio-gen-omega.json"),
            "--receipts",
            str(ROOT / "observability" / "examples" / "gencreator-pilot.sample.json"),
            "--expected-runs",
            "3",
        ]
        completed = subprocess.run(command, check=True, capture_output=True, text=True)
        scorecard = json.loads(completed.stdout)
        self.assertEqual(scorecard["verdict"], "INSUFFICIENT_DATA")
        self.assertEqual(scorecard["sample"]["receipt_completeness_ratio"], 1.0)
        self.assertEqual(scorecard["costs"]["total_economic_cost_usd"], 6.34)
        self.assertTrue(
            all(goal["result"] == "not_evaluable_synthetic" for goal in scorecard["goals"])
        )

    def test_missing_run_census_never_implies_complete_coverage(self) -> None:
        command = [
            sys.executable,
            str(ROOT / "scripts" / "calculate_agent_scorecard.py"),
            "--profile",
            str(ROOT / "observability" / "deployments" / "gencreator-studio-gen-omega.json"),
            "--receipts",
            str(ROOT / "observability" / "examples" / "gencreator-pilot.sample.json"),
        ]
        completed = subprocess.run(command, check=True, capture_output=True, text=True)
        scorecard = json.loads(completed.stdout)
        self.assertIsNone(scorecard["sample"]["receipt_completeness_ratio"])
        self.assertTrue(
            any("independent completed-run count" in item for item in scorecard["limitations"])
        )


if __name__ == "__main__":
    unittest.main()
