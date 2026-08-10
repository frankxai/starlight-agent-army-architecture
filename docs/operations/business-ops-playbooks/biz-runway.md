# Playbook — Runway

- **Card id:** `biz-runway`
- **Human owner:** `founder_plus_accountant`
- **Primary artifact:** `runway-decision.md`
- **Done when:** Decision packet with numbers provenance + recommended action + human gate

## Intent triggers

`runway`, `burn`, `ROI`, `budget`, `spend decision`, `cash`

## Skills to load

- `cfo`
- `agentic-finance-os`
- `agent-operations-accounting`
- `starlight-token-tracker`

## Inputs

- ledger snapshot
- revenue notes
- planned spends
- token costs

## Steps

1. Summarize cash/burn/runway signals (label estimates vs books)
2. List ROI of recent agent/infra spend if known
3. Recommend next spend: do / delay / cut with rationale
4. List accountant/founder questions
5. Emit runway-decision.md; never move money

## Human gates

spend, credentials, external_send

## Coding assist (if relevant)

N/A — business lane; use gstack only if artifact is code.

## Output path convention

`~/.starlight/business-ops/runs/YYYY-MM-DD/biz-runway/runway-decision.md`

## Handoff block (required)

```markdown
## Handoff — Runway
- Objective:
- Artifact:
- Validation:
- Residual risks:
- Human actions required:
- Next specialist (if any):
```
