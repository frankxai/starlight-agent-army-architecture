#!/usr/bin/env python3
"""Status snapshot of business-ops runtime."""
from __future__ import annotations

import json
from datetime import date
from pathlib import Path

RUNTIME = Path.home() / ".starlight" / "business-ops"


def main() -> int:
    today = date.today().isoformat()
    runs = RUNTIME / "runs" / today
    roles = sorted([p.name for p in runs.iterdir()]) if runs.is_dir() else []
    arts = []
    if runs.is_dir():
        for p in runs.rglob("*.md"):
            if p.name != "README.md":
                arts.append(str(p.relative_to(RUNTIME)))
        for p in runs.rglob("*.json"):
            arts.append(str(p.relative_to(RUNTIME)))
    trackers = sorted([p.name for p in (RUNTIME / "trackers").glob("*.json")]) if (RUNTIME / "trackers").is_dir() else []
    print(json.dumps({
        "runtime": str(RUNTIME),
        "date": today,
        "roles_initialized_today": roles,
        "artifacts_today": arts,
        "trackers": trackers,
        "ready": RUNTIME.is_dir(),
    }, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
