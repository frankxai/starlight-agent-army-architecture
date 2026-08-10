# Agent Development Life Cycle (ADLC) v1

> Ultra-high-quality lifecycle for minting, shipping, evaluating, and retiring agents across Starlight brands.

## Stages

```
IDEATE → SPEC → CARD → KB → TOOLS → BODY → EVAL → SHIP → OBSERVE → IMPROVE | RETIRE
```

| Stage | Output | Gate |
|-------|--------|------|
| **IDEATE** | Problem, tribe, outcome, non-goals | Business owner accept |
| **SPEC** | Tier L0–L5, brand, host vs specialist, success metrics | Portfolio fit check |
| **CARD** | Valid `agent-card` YAML/JSON | Schema validate |
| **KB** | Versioned pack under `kb-packs/` + provenance | No private leak; citations |
| **TOOLS** | Allowlist + human gates + deny list | Security review for L3+ |
| **BODY** | Surface adapter (Hermes profile / Vercel shell / CoE) | Smoke path |
| **EVAL** | Golden prompts, refusal tests, brand voice, leak tests | **Structural:** suite file exists + validates. **Live (required before customer SHIP):** model harness scores ≥ min_pass_rate. Dry-run alone is not a quality gate. |
| **SHIP** | Draft PR + preview/proof | Independent verifier + live eval for public L1+ |
| **OBSERVE** | Usage, cost, failure modes, CSAT proxies | Weekly digest |
| **IMPROVE** | AutoResearch notes → card/KB/tool patch | Experiment receipt |
| **RETIRE** | Deprecation notice + redirect host | No orphan public faces |

## Quality bars by tier

| Tier | Required before SHIP |
|------|----------------------|
| L0 | Skill MD + one smoke |
| L1 | Card + KB v1 + UI shell + 10 golden prompts + anti-slop UI check |
| L2 | L1 + handoff tests host↔specialist + scope isolation |
| L3 | L2 + face pack lock + voice samples + deep refusal/canon tests |
| L4 | L3-equivalent private + permission matrix + spend gates + memory isolation |
| L5 | L4 + swarm topology + human gates + rollback + cost cap |

## AutoResearch loop (experiments/)

1. Hypothesis (one sentence)
2. Variant A/B on card prompt, KB chunk, or tool policy
3. Fixed eval suite run
4. Metric: quality score, cost/token, latency, safety fails
5. Receipt in `experiments/YYYY-MM-DD-<slug>.md`
6. Promote winner into card only if eval Δ ≥ threshold and no safety regress

## Security & privacy (fail-closed)

- Public cards: `memory.scope ∈ {none, session, user, org}`
- Never `private_vault` on public product bodies
- Secrets never in cards or KB packs
- Human gates mandatory: publish, external_send, spend, DNS, credentials
- Arcanea: CANON_LOCKED only on public lore agents

## Roles in ADLC

| Role | Who |
|------|-----|
| Product owner | Frank / brand lead |
| Card author | Hermes Queen or specialist CLI |
| Builder | Codex / Claude Code lane |
| Adversarial review | Claude Code (judgment) |
| Creative/cultural review | Grok |
| Verifier | Independent CLI, no write |
| Runtime ops | Hermes Queen + C940 for GitOps |

## Definition of Done (agent v1)

- [ ] Card validates against schema
- [ ] KB pack version pinned in card
- [ ] Tools allow/deny listed per surface
- [ ] At least one body adapter documented
- [ ] Eval suite green at tier bar
- [ ] Design/face notes for L1+ public
- [ ] Receipt path in `receipts/`
- [ ] Portfolio table updated

## Anti-patterns

- Soul locked inside one vendor SDK
- Face without boundaries
- Specialist without host
- Swarm without cost/human gates
- “144 agents” exposed as a picker
- Strategy docs without cards or evals
