# Agent observability foundation receipt

- Date: 2026-08-10
- Scope: central contracts, measurement semantics, deployment profiles, calculation, validation, tests, and CI integration
- Repository: `frankxai/starlight-agent-army-architecture`
- Branch: `agent/hermes/agent-portfolio-adlc-20260809`
- Highest environment reached: local working tree
- External state changed: no

## Truth established

- Operating tiers L0-L5 describe autonomy and governance, not intrinsic intelligence.
- Capability is measured from receipt-backed outcomes with deployment-specific weights and safety gates.
- Provider estimates, actual cash, allocated infrastructure, and imputed human cost are separate cost bases.
- ROI uses confidence-adjusted, overlap-deduplicated value; synthetic data cannot authorize scaling.
- Receipt completeness is unknown unless the runtime provides an independent expected-run denominator.
- Synthetic inputs cannot satisfy SMART goals; proposed goals remain inactive until their baselines and budgets are approved.

## Current adoption snapshot

- The central architecture repository has the measurement foundation in this working tree.
- The AI CoE mirror contains the existing card templates.
- The recorded GenCreator implementation branch, product shell files, and pull request were not present at observation time; its adoption state is therefore `planned`, not shipped.
- FrankX is planned; Arcanea and Starlight have identity assets but still need runtime receipt adapters.

The canonical machine-readable snapshot is `observability/adoption-registry.v1.json`.

## Delivered controls

- Deployment, run-receipt, and scorecard JSON Schemas.
- Canonical metric catalog and three initial deployment profiles.
- Privacy-minimized receipt examples containing synthetic metadata only.
- Deterministic scorecard calculator with cost, capability, safety, ROI, goal, and scale-decision logic.
- Observability validator and five formula/decision tests.
- Dry evaluation receipt hardening: hashes and lengths replace generated-content previews.
- CI checks for architecture, cards, eval suites, receipts, observability contracts, formulas, and synthetic proof generation.

## Synthetic formula proof

The committed three-run sample produces the following demonstration only:

- Fresh input tokens: 11,100
- Cached-read tokens: 4,000
- Cache-write tokens: 0
- Output tokens: 2,850
- Economic cost: $6.34
- Actual cash cost: $0.00, because no billing evidence is attached
- Cost per successful run: $3.17
- Overlap-deduplicated adjusted value: $27.80
- Synthetic economic ROI: 3.3849
- Role-weighted capability score: 86.42 / 100
- p95 latency: 12.5 seconds
- Decision: `INSUFFICIENT_DATA`

This sample does not establish product ROI, approve a budget, or demonstrate production capability.

## Verification evidence

- Agent cards: 9/9 valid.
- Evaluation suites: 9/9 structurally valid.
- Dry evaluation cases: 30/30 passed.
- Observability: 3 deployment profiles, 3 synthetic receipts, and 6 adoption surfaces valid.
- Formula tests: 5/5 passed.
- Architecture validation: passed.
- Git whitespace validation: passed for tracked changes at the implementation checkpoint.

## Gates still required before scale

- Instrument each runtime at the service boundary and provide an independent run census.
- Collect at least 50 non-synthetic receipts per deployment and measurement window.
- Attach reconciled provider invoices or billing exports before claiming actual cash cost.
- Measure and approve baselines, value assumptions, attribution rules, budgets, and SMART targets.
- Run human quality review and safety evaluation on real artifacts.
- Verify consumer-repository adapters in preview or production as appropriate.
- Commit, push, pull-request update, deployment, and production release remain intentionally outside this local receipt.
