#!/usr/bin/env python3
"""Structural and adversarial tests for the 144-profile compiler."""

from __future__ import annotations

import copy
import importlib.util
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "scripts" / "compile_civilization_portfolio.py"
SPEC = importlib.util.spec_from_file_location("compile_civilization_portfolio", MODULE_PATH)
assert SPEC and SPEC.loader
compiler = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(compiler)

_FIXTURE: tuple[dict[str, Any], dict[str, Any], dict[str, Any], dict[str, Any], dict[str, Any]] | None = None


def fixture() -> tuple[dict[str, Any], dict[str, Any], dict[str, Any], dict[str, Any], dict[str, Any]]:
    global _FIXTURE
    if _FIXTURE is None:
        matrix = compiler.load_json(compiler.SOURCE_SNAPSHOT_PATH)
        legacy = compiler.load_json(compiler.LEGACY_PATH)
        lock = compiler.load_json(compiler.IDENTITY_LOCK_PATH)
        receipt = {"status": "verified_test_fixture", "grants_authority": False}
        portfolio, graph = compiler.build(matrix, legacy, lock, receipt)
        _FIXTURE = matrix, legacy, lock, portfolio, graph
    return tuple(copy.deepcopy(item) for item in _FIXTURE)  # type: ignore[return-value]


def expect_rejected(
    matrix: dict[str, Any], legacy: dict[str, Any], lock: dict[str, Any],
    portfolio: dict[str, Any], graph: dict[str, Any], message: str,
) -> None:
    try:
        compiler.validate(matrix, portfolio, graph, legacy, lock)
    except ValueError as exc:
        assert message in str(exc), str(exc)
    else:
        raise AssertionError(f"invalid projection was not rejected: {message}")


def all_agents(portfolio: dict[str, Any]) -> list[dict[str, Any]]:
    return [agent for ring in portfolio["rings"] for agent in ring["agents"]]


def test_counts_identity_lock_and_binding() -> None:
    _, _, lock, portfolio, graph = fixture()
    agents = all_agents(portfolio)
    assert portfolio["counts"] == {
        "rings": 12, "agents": 144, "founding_profiles": 50,
        "expansion_profiles": 94, "shared_workflows": 8,
    }
    assert len(lock["identities"]) == 144
    assert len({item["source_identifier"] for item in lock["identities"]}) == 144
    assert len({item["agent_id"] for item in lock["identities"]}) == 144
    assert len({item["profile_slug"] for item in lock["identities"]}) == 144
    assert {(item["source_identifier"], item["agent_id"], item["profile_slug"]) for item in lock["identities"]} == {
        (agent["lineage"]["source_identifier"], agent["agent_id"], agent["profile_slug"]) for agent in agents
    }
    assert graph["identity_lock_digest"] == portfolio["identity_contract"]["identity_lock_digest"]


def test_json_schemas_accept_generated_contracts() -> None:
    import jsonschema

    pairs = (
        (ROOT / "schemas" / "agent-portfolio" / "civilization-identity-lock.schema.json", compiler.IDENTITY_LOCK_PATH),
        (ROOT / "schemas" / "agent-portfolio" / "civilization-portfolio-v2.schema.json", compiler.PORTFOLIO_PATH),
        (ROOT / "schemas" / "agent-portfolio" / "civilization-graph-v2.schema.json", compiler.GRAPH_PATH),
    )
    for schema_path, document_path in pairs:
        schema = json.loads(schema_path.read_text(encoding="utf-8"))
        document = json.loads(document_path.read_text(encoding="utf-8"))
        jsonschema.Draft202012Validator.check_schema(schema)
        jsonschema.validate(document, schema)


def test_founders_preserve_content_and_receipts() -> None:
    _, legacy_catalog, _, portfolio, _ = fixture()
    legacy_by_id = compiler.legacy_agents(legacy_catalog)
    founders = [agent for agent in all_agents(portfolio) if agent["portfolio_cohort"] == "founding-50"]
    assert {agent["agent_id"] for agent in founders} == set(compiler.LEGACY_LINEAGE)
    fields = (
        "display_name", "role_title", "role_kind", "version", "purpose", "outcomes",
        "public_profile", "voice", "method", "skill_refs", "capabilities",
        "non_capabilities", "stop_conditions", "escalation_conditions", "eval_cases",
    )
    for founder in founders:
        legacy = legacy_by_id[founder["agent_id"]]
        assert all(founder[field] == legacy[field] for field in fields)
        assert founder["visual"]["legacy_visual_dna"] == legacy["visual_dna"]
        assert founder["graph"]["depends_on"] == legacy["depends_on"]
        assert founder["graph"]["routes_to"] == legacy["routes_to"]
        receipts = founder["artifact_receipts"]
        assert receipts["agent_card"]["sha256"].startswith("sha256:")
        assert receipts["system_prompt_contract"]["sha256"].startswith("sha256:")
        assert receipts["structural_eval_suite"]["sha256"].startswith("sha256:")
        assert receipts["visual_asset"]["sha256"].startswith("sha256:")
        assert receipts["capability_pack"]["content_digest"].startswith("sha256:")
        assert receipts["capability_pack"]["manifest_sha256"].startswith("sha256:")


def test_expansion_is_distinct_draft_only_and_unrelated_by_seat() -> None:
    _, _, _, portfolio, _ = fixture()
    expansion = [agent for agent in all_agents(portfolio) if agent["portfolio_cohort"] == "expansion-94"]
    assert len(expansion) == 94
    assert len({agent["method"] for agent in expansion}) == 94
    assert len({case["prompt"] for agent in expansion for case in agent["eval_cases"]}) == 94 * 3
    for agent in expansion:
        assert agent["profile_status"] == "blueprint_draft"
        assert agent["promotion_history"] == []
        assert agent["execution"] == {
            "execution_mode": "draft_recommend_only",
            "tool_binding": "none",
            "required_human_gate": "human-gate-expansion-draft",
            "grants_authority": False,
            "external_effects": "prohibited",
        }
        assert agent["graph"]["depends_on"] == []
        assert agent["graph"]["routes_to"] == []
        assert agent["graph"]["relationship_status"] == "unresolved_pending_explicit_review"
        assert agent["lineage"]["responsibility_is_capability_claim"] is False


def test_expansion_language_quality_and_explicit_inflection() -> None:
    matrix, _, _, portfolio, _ = fixture()
    expansion = [agent for agent in all_agents(portfolio) if agent["portfolio_cohort"] == "expansion-94"]
    seats = {
        seat["source_identifier"]: seat
        for ring in matrix["rings"]
        for seat in ring["seats"]
    }
    assert len(expansion) == 94
    assert compiler.with_indefinite_article("ecological observation brief") == "an ecological observation brief"
    assert compiler.with_indefinite_article("user research brief") == "a user research brief"
    assert compiler.with_indefinite_article("IP issue map") == "an IP issue map"
    assert all(role.get("artifact_plural") for role in compiler.ROLE_ARCHETYPES)
    assert len({agent["public_profile"] for agent in expansion}) == 94
    assert len({agent["outcomes"][0] for agent in expansion}) == 94
    assert len({agent["capabilities"][1] for agent in expansion}) == 94
    assert len({agent["capabilities"][2] for agent in expansion}) == 94
    for agent in expansion:
        prose = compiler.expansion_language_strings(agent)
        assert prose
        assert not any(compiler.ADJACENT_DUPLICATE_WORD.search(text) for _, text in prose), agent["agent_id"]
        assert compiler.METHOD_GERUND_PHRASE.search(agent["method"]), agent["agent_id"]
        assert not compiler.MALFORMED_METHOD_PHRASE.search(agent["method"]), agent["agent_id"]
        role = compiler.role_archetype(seats[agent["lineage"]["source_identifier"]])
        assert f"prepares {role['artifact_plural']} for human review" in agent["public_profile"]
    ecology = next(agent for agent in expansion if agent["work_mode"] == "ecology-evidence")
    assert "drafts an ecological observation brief by defining" in ecology["method"]
    decision = next(agent for agent in expansion if agent["work_mode"] == "decision-evidence")
    assert "bounded bounded" not in decision["purpose"].lower()
    music = next(agent for agent in expansion if agent["lineage"]["source_domain"] == "Music IS")
    assert "music intelligence systems" in music["voice"]
    assert compiler.domain_language_label("DeFi", "unused.md") == "DeFi"
    assert compiler.domain_language_label("IP", "unused.md") == "IP"
    expected_overrides = {
        "starlight-adapter-agno.md": "systems-evidence",
        "starlight-crypto-allocation.md": "resource-evidence",
        "starlight-dist-linkedin.md": "creative-evidence",
        "starlight-ops-hardware.md": "continuity-evidence",
        "starlight-space-payload.md": "systems-evidence",
    }
    for source_identifier, role_id in expected_overrides.items():
        assert compiler.role_archetype(seats[source_identifier])["id"] == role_id


def test_language_gate_rejects_defects_in_all_expansion_profiles() -> None:
    matrix, legacy, lock, portfolio, graph = fixture()
    expansion = [agent for agent in all_agents(portfolio) if agent["portfolio_cohort"] == "expansion-94"]
    for agent in expansion:
        agent["purpose"] += " Bounded bounded."
    try:
        compiler.validate(matrix, portfolio, graph, legacy, lock)
    except ValueError as exc:
        assert str(exc).count("adjacent duplicate word") == 94, str(exc)
    else:
        raise AssertionError("adjacent duplicate words were accepted")

    matrix, legacy, lock, portfolio, graph = fixture()
    expansion = [agent for agent in all_agents(portfolio) if agent["portfolio_cohort"] == "expansion-94"]
    for agent in expansion:
        agent["method"] = agent["method"].replace(" by ", " by clarify ", 1)
    try:
        compiler.validate(matrix, portfolio, graph, legacy, lock)
    except ValueError as exc:
        assert str(exc).count("malformed method phrasing") == 94, str(exc)
    else:
        raise AssertionError("malformed method phrasing was accepted")


def test_graph_is_one_declared_provenanced_plane() -> None:
    _, _, _, portfolio, graph = fixture()
    assert graph["source_portfolio_digest"] == f"sha256:{compiler.sha256(portfolio)}"
    assert len({node["id"] for node in graph["nodes"]}) == len(graph["nodes"])
    assert len({edge["id"] for edge in graph["edges"]}) == len(graph["edges"])
    assert all(node["type"] in graph["node_types"] for node in graph["nodes"])
    assert all(edge["type"] in graph["edge_types"] for edge in graph["edges"])
    assert all(edge["provenance"] and edge["status"] for edge in graph["edges"])
    assert {"verifies", "failure_routes_to", "forks_to", "converges_to", "loops_to"}.issubset(
        {edge["type"] for edge in graph["edges"]}
    )


def test_workflow_topologies_and_failure_mechanics() -> None:
    _, _, _, portfolio, _ = fixture()
    patterns = {item["pattern"] for item in portfolio["shared_workflows"]}
    assert patterns == {"router", "diamond", "converge", "loop", "chain"}
    for item in portfolio["shared_workflows"]:
        assert compiler.validate_workflow(item, {agent["agent_id"] for agent in all_agents(portfolio)}) == []
        assert item["brakes"]["limits"] == {
            "max_turns": 12, "max_cost_usd": 5.0,
            "max_empty_rounds": 2, "max_silence_seconds": 180,
        }
        active = {step["step_id"] for step in item["steps"] if "agent_id" in step}
        failure = item["failure_path"]["node_id"]
        failed = {
            edge["from_step"] for edge in item["topology"]["edges"]
            if edge["type"] == "failure_routes_to" and edge["to_step"] == failure
        }
        assert active == failed


def test_local_git_provenance_and_fabrication_rejection() -> None:
    matrix, _, _, _, _ = fixture()
    provenance_repo = Path.home() / "starlight" / "repos" / "Starlight-Intelligence-System"
    assert provenance_repo.exists(), provenance_repo
    receipt = compiler.verify_matrix_provenance(matrix, provenance_repo)
    assert receipt["status"] == "verified_local_git"
    assert receipt["verified_matrix_rows"] == 144
    fabricated = copy.deepcopy(matrix)
    fabricated["source"]["sha256"] = "0" * 64
    try:
        compiler.verify_matrix_provenance(fabricated, provenance_repo)
    except ValueError as exc:
        assert "digest mismatch" in str(exc)
    else:
        raise AssertionError("fabricated provenance digest was accepted")
    fabricated_row = copy.deepcopy(matrix)
    first = fabricated_row["rings"][0]["seats"][0]
    second = fabricated_row["rings"][0]["seats"][1]
    first["responsibility"], second["responsibility"] = second["responsibility"], first["responsibility"]
    try:
        compiler.verify_matrix_provenance(fabricated_row, provenance_repo)
    except ValueError as exc:
        assert "row is not supported" in str(exc)
    else:
        raise AssertionError("fabricated source-row pairing was accepted")
    try:
        compiler.verify_matrix_provenance(matrix, None)
    except ValueError as exc:
        assert "requires --provenance-git-repo" in str(exc)
    else:
        raise AssertionError("missing provenance repository was accepted")
    override = compiler.verify_matrix_provenance(matrix, None, test_override=True)
    assert override["status"] == "test_only_unverified_override"


def test_identity_lock_drift_is_rejected() -> None:
    matrix, legacy, lock, portfolio, graph = fixture()
    lock["identities"][0]["source_identifier"] = "renamed-without-migration.md"
    try:
        compiler.validate_identity_lock(matrix, lock)
    except ValueError as exc:
        assert "identity lock drift" in str(exc)
    else:
        raise AssertionError("identity lock drift was accepted")
    expect_rejected(matrix, legacy, lock, portfolio, graph, "identity lock drift")


def test_presentation_reorder_does_not_change_identity_lock() -> None:
    matrix, _, lock, _, _ = fixture()
    reordered = copy.deepcopy(matrix)
    reordered["rings"] = list(reversed(reordered["rings"]))
    for ring in reordered["rings"]:
        ring["seats"] = list(reversed(ring["seats"]))
    compiler.validate_identity_lock(reordered, lock)


def test_slug_migration_requires_alias_redirect_and_receipt() -> None:
    matrix, _, lock, _, _ = fixture()
    entry = lock["identities"][0]
    old_slug = entry["profile_slug"]
    entry["profile_slug"] = f"{old_slug}-new"
    entry["alias_history"]["profile_slugs"] = [old_slug]
    try:
        compiler.validate_identity_lock(matrix, lock)
    except ValueError as exc:
        assert "profile slug alias lacks migration receipt or redirect" in str(exc)
    else:
        raise AssertionError("unreceipted profile slug migration was accepted")
    entry["redirects"] = [{"from_slug": old_slug, "to_slug": entry["profile_slug"], "status": 308}]
    entry["migration_history"] = [{
        "field": "profile_slug", "from": old_slug, "to": entry["profile_slug"],
        "reason": "test migration", "reviewed_by": "test-reviewer",
        "reviewed_at": "2026-08-28T12:00:00Z", "receipt_ref": "test://slug-migration",
    }]
    compiler.validate_identity_lock(matrix, lock)


def test_duplicate_identity_is_rejected() -> None:
    matrix, legacy, lock, portfolio, graph = fixture()
    portfolio["rings"][0]["agents"][1]["agent_id"] = portfolio["rings"][0]["agents"][0]["agent_id"]
    expect_rejected(matrix, legacy, lock, portfolio, graph, "duplicate or missing agent_id")


def test_promotion_without_receipts_is_rejected() -> None:
    matrix, legacy, lock, portfolio, graph = fixture()
    agent = next(agent for agent in all_agents(portfolio) if agent["portfolio_cohort"] == "expansion-94")
    agent["profile_status"] = "production_approved"
    expect_rejected(matrix, legacy, lock, portfolio, graph, "expansion promotion must remain an unpromoted blueprint draft")


def test_profile_depth_and_safe_execution_are_enforced() -> None:
    matrix, legacy, lock, portfolio, graph = fixture()
    agent = next(agent for agent in all_agents(portfolio) if agent["portfolio_cohort"] == "expansion-94")
    agent["capabilities"] = ["thin"]
    expect_rejected(matrix, legacy, lock, portfolio, graph, "profile depth missing capabilities")
    matrix, legacy, lock, portfolio, graph = fixture()
    agent = next(agent for agent in all_agents(portfolio) if agent["portfolio_cohort"] == "expansion-94")
    agent["execution"]["tool_binding"] = "shell"
    expect_rejected(matrix, legacy, lock, portfolio, graph, "unsafe expansion execution contract")
    matrix, legacy, lock, portfolio, graph = fixture()
    agent = next(agent for agent in all_agents(portfolio) if agent["portfolio_cohort"] == "expansion-94")
    agent["capabilities"][0] = "deploy the live service"
    expect_rejected(matrix, legacy, lock, portfolio, graph, "prohibited execution claim")


def test_editorial_relationship_inference_is_rejected() -> None:
    matrix, legacy, lock, portfolio, graph = fixture()
    expansion = [agent for agent in all_agents(portfolio) if agent["portfolio_cohort"] == "expansion-94"]
    expansion[1]["graph"]["depends_on"] = [expansion[0]["agent_id"]]
    expect_rejected(matrix, legacy, lock, portfolio, graph, "editorial order may not infer expansion relationships")


def test_same_actor_verification_and_broken_topology_are_rejected() -> None:
    matrix, legacy, lock, portfolio, graph = fixture()
    item = next(item for item in portfolio["shared_workflows"] if item["id"] == "build-to-verified-artifact")
    maker = next(step["agent_id"] for step in item["steps"] if step["role"] == "maker_parallel")
    next(step for step in item["steps"] if step["role"] == "verifier")["agent_id"] = maker
    expect_rejected(matrix, legacy, lock, portfolio, graph, "same actor is maker and verifier")
    matrix, legacy, lock, portfolio, graph = fixture()
    item = next(item for item in portfolio["shared_workflows"] if item["id"] == "research-to-evidence")
    item["topology"]["edges"] = [edge for edge in item["topology"]["edges"] if not (edge["type"] == "forks_to" and edge["to_step"] == "research-audit")]
    expect_rejected(matrix, legacy, lock, portfolio, graph, "diamond requires two branches")
    matrix, legacy, lock, portfolio, graph = fixture()
    item = portfolio["shared_workflows"][0]
    item["brakes"]["limits"]["max_empty_rounds"] = 0
    expect_rejected(matrix, legacy, lock, portfolio, graph, "invalid brake limit max_empty_rounds")


def test_graph_uniqueness_declared_types_and_binding_are_enforced() -> None:
    matrix, legacy, lock, portfolio, graph = fixture()
    graph["nodes"].append(copy.deepcopy(graph["nodes"][0]))
    expect_rejected(matrix, legacy, lock, portfolio, graph, "graph node IDs are missing or duplicate")
    matrix, legacy, lock, portfolio, graph = fixture()
    graph["edges"][0]["type"] = "imaginary_edge"
    expect_rejected(matrix, legacy, lock, portfolio, graph, "graph edge type is undeclared")
    matrix, legacy, lock, portfolio, graph = fixture()
    graph["source_portfolio_digest"] = "sha256:" + "0" * 64
    expect_rejected(matrix, legacy, lock, portfolio, graph, "graph/portfolio digest binding mismatch")


def test_missing_founder_receipt_is_rejected() -> None:
    matrix, legacy, lock, portfolio, graph = fixture()
    founder = next(agent for agent in all_agents(portfolio) if agent["portfolio_cohort"] == "founding-50")
    del founder["artifact_receipts"]["system_prompt_contract"]
    expect_rejected(matrix, legacy, lock, portfolio, graph, "founding artifact receipts incomplete")


def main() -> None:
    tests = [
        test_counts_identity_lock_and_binding,
        test_json_schemas_accept_generated_contracts,
        test_founders_preserve_content_and_receipts,
        test_expansion_is_distinct_draft_only_and_unrelated_by_seat,
        test_expansion_language_quality_and_explicit_inflection,
        test_language_gate_rejects_defects_in_all_expansion_profiles,
        test_graph_is_one_declared_provenanced_plane,
        test_workflow_topologies_and_failure_mechanics,
        test_local_git_provenance_and_fabrication_rejection,
        test_identity_lock_drift_is_rejected,
        test_presentation_reorder_does_not_change_identity_lock,
        test_slug_migration_requires_alias_redirect_and_receipt,
        test_duplicate_identity_is_rejected,
        test_promotion_without_receipts_is_rejected,
        test_profile_depth_and_safe_execution_are_enforced,
        test_editorial_relationship_inference_is_rejected,
        test_same_actor_verification_and_broken_topology_are_rejected,
        test_graph_uniqueness_declared_types_and_binding_are_enforced,
        test_missing_founder_receipt_is_rejected,
    ]
    for test in tests:
        test()
        print(f"PASS {test.__name__}")


if __name__ == "__main__":
    main()
