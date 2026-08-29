#!/usr/bin/env python3
"""Route a natural-language biz intent to a role playbook + run folder."""
from __future__ import annotations

import json
import re
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RUNTIME = Path.home() / ".starlight" / "business-ops"
ROUTER_PATHS = [
    RUNTIME / "router.json",
    ROOT / "templates" / "business-ops-supervisor" / "router.json",
]


def load_router() -> dict:
    for p in ROUTER_PATHS:
        if p.is_file():
            return json.loads(p.read_text(encoding="utf-8"))
    raise SystemExit("router.json not found — run biz_ops_init_run.py first")


def score(intent: str, route: dict) -> int:
    text = intent.lower()
    s = 0
    for phrase in route.get("intents") or []:
        p = phrase.lower()
        if p in text:
            s += 3 if len(p) > 4 else 2
        # token overlap
        for tok in re.findall(r"[a-z0-9]+", p):
            if len(tok) > 3 and tok in text:
                s += 1
    return s


def main(argv: list[str]) -> int:
    if len(argv) < 2:
        print("Usage: biz_ops_route.py \"<intent>\"")
        return 2
    intent = " ".join(argv[1:]).strip()
    router = load_router()
    routes = router.get("routes") or []
    ranked = sorted(((score(intent, r), r) for r in routes), key=lambda x: x[0], reverse=True)
    best_score, best = ranked[0]
    if best_score <= 0:
        best = next(r for r in routes if r["id"] == router.get("default_on_ambiguous", "biz-ops-supervisor"))
        best_score = 0

    today = date.today().isoformat()
    out_dir = RUNTIME / "runs" / today / best["id"]
    out_dir.mkdir(parents=True, exist_ok=True)
    packet = {
        "intent": intent,
        "route_id": best["id"],
        "title": best["title"],
        "score": best_score,
        "playbook": best.get("playbook"),
        "artifact": best.get("artifact"),
        "run_dir": str(out_dir),
        "card": f"cards/specialists/{best['id']}.json" if best["id"] != "biz-ops-supervisor" else "cards/stewards/biz-ops-supervisor.json",
        "instructions_for_agent": [
            f"Load skill business-ops-supervisor-stack",
            f"Load Agent Card {best['id']}",
            f"Follow playbook {best.get('playbook')}",
            f"Write artifact {best.get('artifact')} into {out_dir}",
            "Respect human gates; no auto publish/pay/send/hire",
            "If content/public/legal: hand to biz-qa-red-team before ship",
        ],
        "alternates": [
            {"id": r["id"], "title": r["title"], "score": sc}
            for sc, r in ranked[1:4]
            if sc > 0
        ],
    }
    out_path = out_dir / "route-packet.json"
    out_path.write_text(json.dumps(packet, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(packet, indent=2))
    print(f"\n# Next: open playbook and produce {best.get('artifact')} in {out_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
