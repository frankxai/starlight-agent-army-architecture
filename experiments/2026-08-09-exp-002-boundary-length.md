# Experiment exp-002 — Boundary list length

## Hypothesis
Capping boundaries at ≤7 high-severity rules reduces false refusals vs long lists, holding safety probes constant.

## Method
- Same safety probes (secrets, cross-tenant, fake ship, illegal)
- Variant A: current Gen-Ω boundary list
- Variant B: top 7 only
- Metrics: false refusal rate on benign creative tasks; safety fail rate

## Status
Designed 2026-08-09 — pending harness.

## Promote rule
Shorter list only if safety fail rate unchanged and false refusals drop.
