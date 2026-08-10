# Playbook — Bounty

- **Card id:** `biz-bounty`
- **Human owner:** `va`
- **Primary artifact:** `quest-spec.md`
- **Done when:** Quest is runnable by a contributor without ambiguity; payment remains human-gated

## Intent triggers

`bounty`, `quest`, `reward`, `contributor challenge`, `rubric reward`

## Skills to load

- `project-brief`
- `todo-discipline`
- `agentic-execution-orchestration`

## Inputs

- problem
- reward budget
- proof-of-work idea

## Steps

1. Define quest scope and non-goals
2. Write scoring rubric (0–100) and minimum ship bar
3. Define reward terms + dispute path (human pays)
4. Define submission format and deadline
5. Emit quest-spec.md + optional JSON quest record; NEVER auto-pay

## Human gates

spend, external_send, legal_ip

## Coding assist (if relevant)

N/A — business lane; use gstack only if artifact is code.

## Output path convention

`~/.starlight/business-ops/runs/YYYY-MM-DD/biz-bounty/quest-spec.md`

## Handoff block (required)

```markdown
## Handoff — Bounty
- Objective:
- Artifact:
- Validation:
- Residual risks:
- Human actions required:
- Next specialist (if any):
```
