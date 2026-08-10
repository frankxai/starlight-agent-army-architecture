# Playbook — Sales Pipeline

- **Card id:** `biz-sales-pipeline`
- **Human owner:** `founder_or_sales`
- **Primary artifact:** `sales-update.md`
- **Done when:** Stages current + drafts ready + explicit founder/sales actions

## Intent triggers

`sales`, `CRM`, `proposal`, `lead`, `pipeline`, `nudge lead`

## Skills to load

- `chief-revenue-operator`
- `product-engine`
- `email-inbox-triage`

## Inputs

- lead notes
- stage
- offer SSOT
- pricing bounds

## Steps

1. Update pipeline stages in tracker (JSON/CSV/MD)
2. Draft proposal from offer SSOT (no freestyle pricing)
3. Draft nudge messages for stalled leads
4. List close risks and next human call/actions
5. Emit sales-update.md; human owns close

## Human gates

external_send, spend, legal_ip, brand_identity

## Coding assist (if relevant)

N/A — business lane; use gstack only if artifact is code.

## Output path convention

`~/.starlight/business-ops/runs/YYYY-MM-DD/biz-sales-pipeline/sales-update.md`

## Handoff block (required)

```markdown
## Handoff — Sales Pipeline
- Objective:
- Artifact:
- Validation:
- Residual risks:
- Human actions required:
- Next specialist (if any):
```
