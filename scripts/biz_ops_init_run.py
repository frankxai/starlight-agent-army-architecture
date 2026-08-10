#!/usr/bin/env python3
"""Initialize private business-ops runtime for full stack use."""
from __future__ import annotations

import json
import shutil
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RUNTIME = Path.home() / ".starlight" / "business-ops"
TODAY = date.today().isoformat()
TRACKERS = ROOT / "templates" / "business-ops-supervisor" / "trackers"
ORG = ROOT / "templates" / "business-ops-supervisor" / "org.yaml"
ROUTER = ROOT / "templates" / "business-ops-supervisor" / "router.json"
ARTIFACTS = ROOT / "templates" / "business-ops-supervisor" / "artifacts"
PLAYBOOKS = ROOT / "docs" / "operations" / "business-ops-playbooks"

ROLE_IDS = [
    "biz-ops-supervisor",
    "biz-founder-capture",
    "biz-chief-of-staff",
    "biz-delegation",
    "biz-recruiting",
    "biz-bounty",
    "biz-contributor-onboarding",
    "biz-qa-red-team",
    "biz-content-hydra",
    "biz-partnership",
    "biz-runway",
    "biz-sales-pipeline",
    "biz-community-ritual",
]


def main() -> int:
    RUNTIME.mkdir(parents=True, exist_ok=True)
    (RUNTIME / "runs" / TODAY).mkdir(parents=True, exist_ok=True)
    (RUNTIME / "trackers").mkdir(parents=True, exist_ok=True)

    if ORG.is_file():
        shutil.copy2(ORG, RUNTIME / "org.snapshot.yaml")
    if ROUTER.is_file():
        shutil.copy2(ROUTER, RUNTIME / "router.json")

    if TRACKERS.is_dir():
        for p in TRACKERS.glob("*.json"):
            dest = RUNTIME / "trackers" / p.name
            if not dest.exists():
                shutil.copy2(p, dest)

    created = []
    for rid in ROLE_IDS:
        d = RUNTIME / "runs" / TODAY / rid
        d.mkdir(parents=True, exist_ok=True)
        # seed from artifact templates if present
        for tpl in ARTIFACTS.glob("*.md"):
            # match by reading first lines for card id is heavy; copy common names from playbook convention
            pass
        readme = d / "README.md"
        if not readme.exists():
            pb = PLAYBOOKS / f"{rid}.md"
            readme.write_text(
                f"# {rid}\n\nDate: {TODAY}\nPlaybook: {pb if pb.exists() else 'n/a'}\n\nRun via: Biz: ... or scripts/biz_ops_route.py\n",
                encoding="utf-8",
            )
            created.append(str(readme))

    (RUNTIME / "README.md").write_text(
        f"""# Business Ops runtime (private)

Initialized: {TODAY}
SSOT cards: {ROOT}
Playbooks: {PLAYBOOKS}
Use guide: {ROOT / 'docs/operations/BUSINESS_OPS_USE.md'}

## Commands
```bash
python {ROOT / 'scripts/biz_ops_route.py'} "weekly priorities"
python {ROOT / 'scripts/biz_ops_route.py'} "content hydra from: my idea"
python {ROOT / 'scripts/biz_ops_status.py'}
```
""",
        encoding="utf-8",
    )

    # seed artifact shells for today
    mapping = {
        "biz-ops-supervisor": "mission-board.md",
        "biz-founder-capture": "capture-packet.md",
        "biz-chief-of-staff": "weekly-brief.md",
        "biz-delegation": "task-packet.md",
        "biz-recruiting": "recruiting-packet.md",
        "biz-bounty": "quest-spec.md",
        "biz-contributor-onboarding": "onboarding-pack.md",
        "biz-qa-red-team": "qa-report.md",
        "biz-content-hydra": "content-hydra-set.md",
        "biz-partnership": "partnership-pack.md",
        "biz-runway": "runway-decision.md",
        "biz-sales-pipeline": "sales-update.md",
        "biz-community-ritual": "ritual-pack.md",
    }
    for rid, art in mapping.items():
        src = ARTIFACTS / art
        dest = RUNTIME / "runs" / TODAY / rid / art
        if src.is_file() and not dest.exists():
            shutil.copy2(src, dest)
            created.append(str(dest))

    print(json.dumps({"ok": True, "runtime": str(RUNTIME), "date": TODAY, "seeded": len(created)}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
