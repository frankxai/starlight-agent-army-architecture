# Experiment exp-001 — Host-only vs host+specialist chips

## Hypothesis
Visible specialist chips improve correct lane selection on studio tasks vs host-only prompts, without increasing false ship claims.

## Method
- Fixed 10 golden prompts (studio plan, visual, hooks, ship claim, secret probe, price probe, campaign, critique, export, ambiguous)
- Variant A: Gen-Ω host system only
- Variant B: Gen-Ω + specialist catalog in system + chip instruction
- Score: routing accuracy, safety, proof discipline, cost tokens

## Status
Designed 2026-08-09 — execution pending model harness run.

## Promote rule
Ship B only if routing accuracy +≥10pp and safety fails not increased.
