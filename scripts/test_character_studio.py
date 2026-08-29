#!/usr/bin/env python3
"""Regression tests for the Starlight Character Studio contracts."""

from __future__ import annotations

import copy
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from validate_character_studio import (  # noqa: E402
    load_json,
    validate_asset_program,
    validate_direction_batch,
    validate_document,
    validate_repository,
)


class CharacterStudioTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.contract = load_json(
            ROOT / "templates" / "starlight-character-studio" / "character-visual-contract.template.json"
        )
        cls.job = load_json(ROOT / "templates" / "starlight-character-studio" / "image-job.template.json")
        cls.program = load_json(
            ROOT / "templates" / "starlight-character-studio" / "asset-program.template.json"
        )

    def test_repository_fixtures_are_valid(self) -> None:
        self.assertEqual(validate_repository(), [])

    def test_visual_contract_cannot_grant_runtime_authority(self) -> None:
        candidate = copy.deepcopy(self.contract)
        candidate["authority"]["grants_runtime_authority"] = True
        issues = validate_document(candidate)
        self.assertTrue(any("False was expected" in issue.message for issue in issues))

    def test_approved_contract_requires_human_approval(self) -> None:
        candidate = copy.deepcopy(self.contract)
        candidate["state"] = "approved"
        candidate["provenance"]["human_decision"] = "pending"
        issues = validate_document(candidate)
        self.assertTrue(any("'approve' was expected" in issue.message for issue in issues))

    def test_generated_job_requires_receipt_and_inspection(self) -> None:
        candidate = copy.deepcopy(self.job)
        candidate["output"]["status"] = "generated"
        issues = validate_document(candidate)
        messages = "\n".join(issue.message for issue in issues)
        self.assertIn("is not of type 'string'", messages)
        self.assertIn("is not of type 'object'", messages)
        self.assertIn("True was expected", messages)

    def test_output_path_must_be_repo_relative(self) -> None:
        candidate = copy.deepcopy(self.job)
        candidate["output"]["path"] = "C:/tmp/lyra.png"
        issues = validate_document(candidate)
        self.assertTrue(any("does not match" in issue.message for issue in issues))

    def test_eligible_candidate_requires_ship_threshold(self) -> None:
        candidate = copy.deepcopy(self.job)
        candidate["qa"].update({"inspected": True, "score30": 25, "decision": "eligible-for-human-review"})
        issues = validate_document(candidate)
        self.assertTrue(any("less than the minimum of 26" in issue.message for issue in issues))

    def test_direction_batch_rejects_moving_baseline(self) -> None:
        first = copy.deepcopy(self.job)
        second = copy.deepcopy(self.job)
        second["job_id"] = "2026-08-23-second-direction"
        second["direction"]["territory_id"] = "second-direction"
        second["direction"]["controlled_variables"][0] = "different identity"
        issues = validate_direction_batch([first, second])
        self.assertTrue(any("controlled-variable baseline" in issue.message for issue in issues))

    def test_asset_program_scale_math_is_enforced(self) -> None:
        candidate = copy.deepcopy(self.program)
        candidate["scale_model"]["generated_master_count"] += 1
        issues = validate_document(candidate) + validate_asset_program(candidate, source="<memory>")
        self.assertTrue(any("generated_master_count" in issue.message for issue in issues))

    def test_held_asset_program_cannot_generate(self) -> None:
        candidate = copy.deepcopy(self.program)
        candidate["batches"][0]["status"] = "generating"
        issues = validate_document(candidate) + validate_asset_program(candidate, source="<memory>")
        self.assertTrue(any("held machine admission" in issue.message for issue in issues))


if __name__ == "__main__":
    unittest.main(verbosity=2)
