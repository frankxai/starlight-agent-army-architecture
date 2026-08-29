# Playbook — Business Ops Supervisor

- **Card id:** `biz-ops-supervisor`
- **Human owner:** `founder`
- **Primary artifact:** `mission-board.md`
- **Done when:** Mission board has ≤3 TOP items, each with owner agent, human, artifact path, gate list

## Intent triggers

`route`, `prioritize`, `mission board`, `what should we do`, `supervisor`, `/biz`

## Skills to load

- `business-ops-supervisor-stack`
- `starlight-queen`
- `agentic-execution-orchestration`
- `todo-discipline`
- `starlight-outcome-cockpit`

## Inputs

- objectives
- open PRs
- ledger signals
- prior receipts

## Steps

1. Load org.yaml + active cards
2. List open objectives and blockers (max 3 active TOP)
3. Assign each TOP item to exactly one specialist lane
4. Require artifact path + human gate flags
5. Emit mission-board.md and hand off

## Human gates

spend, publish, external_send, destructive

## Coding assist (if relevant)

N/A — business lane; use gstack only if artifact is code.

## Output path convention

`~/.starlight/business-ops/runs/YYYY-MM-DD/biz-ops-supervisor/mission-board.md`

## Handoff block (required)

```markdown
## Handoff — Business Ops Supervisor
- Objective:
- Artifact:
- Validation:
- Residual risks:
- Human actions required:
- Next specialist (if any):
```
