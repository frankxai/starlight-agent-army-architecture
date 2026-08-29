# Playbook — QA / Red Team

- **Card id:** `biz-qa-red-team`
- **Human owner:** `va_plus_founder`
- **Primary artifact:** `qa-report.md`
- **Done when:** Independent verdict with evidence; never self-certify maker work as PASS without check

## Intent triggers

`qa`, `red team`, `review`, `hallucination`, `brand fit`, `compliance`, `claims`

## Skills to load

- `agent-design-review`
- `security-auditor`
- `requesting-code-review`
- `todo-discipline`

## Inputs

- artifact path
- claim set
- brand

## Steps

1. Inventory claims and evidence
2. Check brand voice and CTA purity
3. Flag legal/compliance/privacy risks
4. For code: prefer gstack /review /qa /cso patterns
5. Verdict: PASS | REVISE | BLOCK with ordered fixes

## Human gates

publish, legal_ip, brand_identity

## Coding assist (if relevant)

/review, /qa, /cso, /browse

## Output path convention

`~/.starlight/business-ops/runs/YYYY-MM-DD/biz-qa-red-team/qa-report.md`

## Handoff block (required)

```markdown
## Handoff — QA / Red Team
- Objective:
- Artifact:
- Validation:
- Residual risks:
- Human actions required:
- Next specialist (if any):
```
