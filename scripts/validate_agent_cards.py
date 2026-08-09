#!/usr/bin/env python3
"""Validate Agent Cards against schemas/agent-card/agent-card.schema.json."""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCHEMA_PATH = ROOT / "schemas" / "agent-card" / "agent-card.schema.json"
CARD_GLOBS = ["cards/hosts/*.json", "cards/specialists/*.json", "cards/stewards/*.json"]


def load_json(path: Path):
    with path.open(encoding="utf-8") as f:
        return json.load(f)


def basic_validate(card: dict, schema: dict) -> list[str]:
    """Minimal validator (stdlib-only). Prefer jsonschema if installed."""
    errors: list[str] = []
    required = schema.get("required", [])
    for key in required:
        if key not in card:
            errors.append(f"missing required top-level key: {key}")

    if card.get("schema_version") != "agent-card.v1":
        errors.append("schema_version must be agent-card.v1")

    tier = card.get("tier")
    allowed_tiers = set(schema["properties"]["tier"]["enum"])
    if tier not in allowed_tiers:
        errors.append(f"invalid tier: {tier}")

    brand = card.get("brand")
    allowed_brands = set(schema["properties"]["brand"]["enum"])
    if brand not in allowed_brands:
        errors.append(f"invalid brand: {brand}")

    if tier == "specialist" and not card.get("parent_host_id"):
        errors.append("specialist requires parent_host_id")

    identity = card.get("identity") or {}
    for k in ("display_name", "tagline", "voice", "values", "boundaries"):
        if k not in identity:
            errors.append(f"identity missing {k}")

    mind = card.get("mind") or {}
    mem = mind.get("memory_scope")
    if mem not in {"none", "session", "user", "org", "private_vault"}:
        errors.append(f"invalid memory_scope: {mem}")

    surfaces = (card.get("body") or {}).get("surfaces") or []
    if mem == "private_vault":
        bad = [s for s in surfaces if s in {"web", "phone_pwa", "coe_demo"}]
        if bad:
            errors.append(f"private_vault cannot expose public surfaces: {bad}")

    soul = identity.get("soul_md")
    if soul:
        soul_path = ROOT / soul
        if not soul_path.is_file():
            errors.append(f"soul_md missing file: {soul}")

    for kb in mind.get("public_kb") or []:
        # allow non-path ids later; if looks like path, check
        if "/" in kb or kb.endswith(".md"):
            if not (ROOT / kb).is_file():
                errors.append(f"public_kb missing: {kb}")

    evals = card.get("evals") or {}
    suite_id = evals.get("suite_id")
    if suite_id:
        suite_path = ROOT / suite_id
        if not suite_path.is_file():
            errors.append(f"evals.suite_id missing file: {suite_id}")

    return errors


def main() -> int:
    schema = load_json(SCHEMA_PATH)
    use_jsonschema = False
    try:
        import jsonschema  # type: ignore

        use_jsonschema = True
        validator = jsonschema.Draft202012Validator(schema)
    except Exception:
        validator = None

    cards: list[Path] = []
    for pattern in CARD_GLOBS:
        cards.extend(sorted(ROOT.glob(pattern)))

    if not cards:
        print("ERROR: no cards found", file=sys.stderr)
        return 2

    failed = 0
    for path in cards:
        rel = path.relative_to(ROOT).as_posix()
        try:
            card = load_json(path)
        except Exception as e:
            print(f"FAIL {rel}: JSON parse error: {e}")
            failed += 1
            continue

        errors: list[str] = []
        if use_jsonschema and validator is not None:
            errors.extend(sorted({e.message for e in validator.iter_errors(card)}))
        errors.extend(basic_validate(card, schema))
        # de-dupe
        errors = sorted(set(errors))

        if errors:
            failed += 1
            print(f"FAIL {rel}")
            for err in errors:
                print(f"  - {err}")
        else:
            print(f"OK   {rel}")

    print(f"\n{len(cards) - failed}/{len(cards)} cards valid (jsonschema={'yes' if use_jsonschema else 'basic-only'})")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
