# Agent Economics, Capability, and SMART Outcomes

> Status: SSOT contract v1 · 2026-08-10
>
> Applies to: public brand agents, private stewards, swarm cells, and runtime adapters
> Machine-readable contracts: `schemas/agent-deployment/`, `schemas/agent-run-receipt/`, `schemas/agent-scorecard/`

## Executive rule

Do not call an agent intelligent, cheap, valuable, deployed, or profitable from a prompt, model name, scheduler status, structural eval, or receipt count.

Decisions require a named deployment, a frozen measurement window, valid privacy-minimized run receipts, role-specific quality evidence, and a scorecard that separates actual cash from estimates.

## Two different ladders

### Operating/autonomy tier

L0–L5 describes **what the system is allowed and structured to do**:

| Tier | Operating form |
|------|----------------|
| L0 | Skill or deterministic procedure |
| L1 | Host chat with scoped KB and light memory |
| L2 | Specialist with handoffs and domain pack |
| L3 | Full persona with locked identity and deeper tool surface |
| L4 | Private/enterprise steward with long memory and permissions |
| L5 | Multi-agent cell with gates, rollback, and cost cap |

It is not IQ and it is not evidence that L5 performs better than L1.

### Observed capability score

Capability is measured for one **agent card × runtime × model policy × task set × time window**.

Default public-host formula:

```text
Capability Score = 100 × (
  0.30 × task success
  + 0.15 × evidence grounding
  + 0.15 × reliability
  + 0.20 × safety
  + 0.10 × efficiency
  + 0.10 × judgment/routing
)
```

Weights live in the deployment profile and must sum to 1. A role can use different weights: a private operator gives safety and evidence more weight; a router gives judgment more weight.

Safety is non-compensatory. A critical tenant leak, unauthorized spend/send, fabricated deployment proof, or private-memory boundary violation produces **HOLD**, even when the weighted score is high.

Minimum decision samples:

- Public host/specialist: 50 representative live runs.
- Private operator: 30 admitted live runs.
- High-consequence enterprise lane: define a larger task-stratified set in its deployment profile.
- Structural dry-runs never count toward this sample.

## Cost accounting

Every cost component declares one basis:

| Basis | Meaning |
|-------|---------|
| `actual_cash` | Provider invoice, tool invoice, or other cash evidence |
| `estimated_provider` | Price-table equivalent; not an invoice |
| `allocated_infra` | Documented share of fixed infrastructure |
| `imputed_human` | Review/recovery minutes × approved loaded rate |

Do not record the same provider charge as both actual and estimated.

```text
Total economic cost =
  provider cost (actual when known, otherwise estimate)
  + metered tools
  + allocated infrastructure
  + imputed human review
  + failure/recovery cost

Cost per success = total economic cost / successful outcomes
```

Report fresh input, cached read, cache write, and output tokens separately. Total processed tokens are useful capacity telemetry, not a synonym for tokens paid or cash spent.

Build cost belongs in a separate investment ledger. If amortized into unit economics, state the horizon and expected successful outcomes explicitly; do not silently mix one-time build effort into provider run cost.

## Value and ROI

Allowed value components are revenue, time saved, avoided cost, loss avoided, and a deliberately named other category. Each component needs a source and attribution confidence from 0 to 1.

Components sharing an `overlap_group` are alternatives describing the same benefit. The calculator takes the highest value in that group rather than summing it.

```text
Confidence-adjusted value =
  sum(value amount × attribution confidence), overlap-deduplicated

Confidence-adjusted ROI =
  (confidence-adjusted value - total economic cost) / total economic cost
```

Examples:

- ROI `1.0` means net value equals cost: two dollars of adjusted value for each dollar of cost.
- ROI `0.0` is break-even.
- ROI `-0.5` loses fifty cents of adjusted value per dollar of cost.

Revenue and time saved must not both be counted when they describe the same converted outcome. Risk reduction needs a documented probability and exposure basis before it is monetized.

## SMART deployment goals

Agent Cards remain identity assets. SMART goals belong to a **deployment profile** because the same identity can have different economics on web, phone, and Hermes.

Every goal carries:

- one specific outcome;
- one catalog metric;
- a measured baseline, or `baselining` status while the baseline is collected;
- an operator and numeric target;
- an ISO deadline;
- a concrete owner;
- an evidence source;
- safety and attribution guardrails.

No business-performance goal becomes `active` without a measured baseline. Instrumentation can start active with a measured baseline of zero.

Default sequence:

1. **Instrument:** ≥95% valid receipt coverage within 14 days; zero raw prompt/response storage.
2. **Baseline:** collect the role-specific minimum representative sample.
3. **Prove quality:** meet task-success and capability gates with zero critical safety failures.
4. **Prove economics:** meet approved cost-per-success and confidence-adjusted ROI gates.
5. **Scale, improve, hold, or stop:** use the period scorecard, not activity volume.

Proposed budgets in this repo are planning hypotheses. They do not authorize spend until the named owner changes `budget_status` to `approved` after baseline review.

## Storage topology

### This strategy repo owns

- Agent Cards, KB pointers, portfolio, and ADLC.
- Metric catalog and formulas.
- Deployment-profile schema and central planned profiles.
- Run-receipt and period-scorecard schemas.
- Deterministic validator and scorecard calculator.
- Sanitized synthetic examples.
- Cross-repo adoption registry.

### Consumer repos/runtimes own

- The runtime adapter and server-side enforcement.
- A thin deployment-profile mirror or immutable reference to the central profile.
- Receipt emission at the actual model/tool boundary.
- Private/local receipt storage under `.starlight/agent-observability/` or a governed telemetry store.
- Product-specific outcome evidence and live isolation tests.

Consumers load cards; they do not fork souls. Raw conversations, prompts, responses, provider payloads, secrets, tenant identifiers, and private-memory content never enter this public repository.

## Evidence hierarchy

1. Current deployment, endpoint, PR, process, and provider/invoice state.
2. Durable run receipts bound to the deployment and exact window.
3. Provider/Tokscale usage telemetry reconciled to the receipts.
4. Fixed live eval results and verifier evidence.
5. Session history and narrative receipts for context only.

Use the environment ladder exactly:

`local only → committed → pushed → draft PR → preview → merged → production`

## Commands

```powershell
python scripts/validate_agent_observability.py
python scripts/calculate_agent_scorecard.py `
  --profile observability/deployments/gencreator-studio-gen-omega.json `
  --receipts observability/examples/gencreator-pilot.sample.json `
  --expected-runs 3
```

`--expected-runs` must come from an independent runtime/scheduler census. Without that denominator, receipt completeness is unknown; the calculator never assumes the observed receipts are the full run population.

The committed example is synthetic. Its expected decision is `INSUFFICIENT_DATA`, even if quality and ROI look positive, because three fabricated demonstration receipts cannot justify scaling.

## Current adoption truth

The dated machine-readable snapshot is `observability/adoption-registry.v1.json`.

As observed on 2026-08-10:

- The SSOT foundation is in open draft PR `frankxai/starlight-agent-army-architecture#1`; existing architecture and card checks are green.
- The AI CoE card mirror exists on `agent/hermes/agent-card-templates-20260809`.
- The previously recorded Gen-Ω product-shell lane has no current local branch/worktree and no remote PR under the recorded branch name. It is therefore **planned**, not implemented or previewed.
- FrankX and Arcanea have identity assets but no evidenced runtime receipt instrumentation in this measurement system.
- Starlight Operator has a card and adapter document; private runtime receipt emission remains the next gate.

This registry is an observation receipt, not a forever-live deployment database. Re-query decision-critical external state before reporting or promoting.
