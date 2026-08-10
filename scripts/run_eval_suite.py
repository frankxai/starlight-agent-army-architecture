#!/usr/bin/env python3
"""Dry-run structural check for eval suites (no live LLM)."""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EVALS = ROOT / "evals"


def main() -> int:
    files = sorted(EVALS.glob("*.json"))
    if not files:
        print("ERROR: no eval suites", file=sys.stderr)
        return 2

    failed = 0
    for path in files:
        rel = path.relative_to(ROOT).as_posix()
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except Exception as e:
            print(f"FAIL {rel}: {e}")
            failed += 1
            continue

        errors = []
        for key in ("suite_id", "agent_id", "cases"):
            if key not in data:
                errors.append(f"missing {key}")
        cases = data.get("cases") or []
        if not isinstance(cases, list) or len(cases) < 1:
            errors.append("cases must be non-empty list")
        for i, case in enumerate(cases):
            if not isinstance(case, dict):
                errors.append(f"case[{i}] not object")
                continue
            for k in ("id", "prompt", "expect"):
                if k not in case:
                    errors.append(f"case[{i}] missing {k}")

        agent_id = data.get("agent_id")
        card_hits = list(ROOT.glob(f"cards/**/{agent_id}.json")) if agent_id else []
        if agent_id and not card_hits:
            errors.append(f"no card file for agent_id={agent_id}")

        if errors:
            failed += 1
            print(f"FAIL {rel}")
            for e in errors:
                print(f"  - {e}")
        else:
            print(f"OK   {rel}  cases={len(cases)} agent={agent_id}")

    print(f"\n{len(files) - failed}/{len(files)} eval suites structurally valid")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
