# Agent Observability Control Plane

This directory stores sanitized, Git-safe measurement contracts for Agent Card deployments.

| Path | Purpose |
|------|---------|
| `metric-catalog.v1.json` | Canonical metric names, units, directions, and formulas |
| `adoption-registry.v1.json` | Dated cross-repo adoption snapshot with evidence and next gates |
| `deployments/*.json` | SMART goals, proposed/approved budgets, capability weights, and receipt sinks |
| `examples/*.json` | Synthetic receipts for deterministic formula and privacy tests |

Real receipts do not belong here. Consumer runtimes write privacy-minimized records to their governed local/private sink, normally `.starlight/agent-observability/`, and aggregate only sanitized scorecards for publication.

Validate:

```powershell
python scripts/validate_agent_observability.py
```

Calculate a demonstration scorecard:

```powershell
python scripts/calculate_agent_scorecard.py --profile observability/deployments/gencreator-studio-gen-omega.json --receipts observability/examples/gencreator-pilot.sample.json --expected-runs 3
```
