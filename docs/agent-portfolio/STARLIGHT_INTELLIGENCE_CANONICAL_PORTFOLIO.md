# Starlight Intelligence Canonical Portfolio

> Status: **DRAFT**  
> Contract: exactly **10 bounded swarms × 5 agents = 50 agents**  
> Evidence: structural validation only; **live evaluation has not run**

This v1 contract is the **founding cohort**, not a competing identity universe. The draft
Civilization v2 projection preserves all 50 canonical agent ids and adds 94 source-backed draft
profiles to form exactly 12 rings × 12 agents = 144. Ring and seat are presentation coordinates,
never identity. See `CIVILIZATION_144_IDENTITY_CONTRACT.md` before extending or publishing v2.

This portfolio is the data-driven Starlight Intelligence roster. It compiles into the repo's native
`agent-card.v1` cards, prompt contracts, and structural eval suites. Existing GenCreator, FrankX,
Arcanea, Starlight Operator, and business-ops cards remain separate product/runtime identities and
do not count toward this exact 50-agent roster.

## Single source and compiled projections

| Artifact | Contract |
| --- | --- |
| Source catalog | `portfolio/canonical-portfolio.v1.json` — edit this, not projections |
| Source schema | `schemas/agent-portfolio/canonical-portfolio.schema.json` |
| Native cards | `cards/portfolio/<agent-id>.json` |
| Prompt contracts | `cards/portfolio/prompts/<agent-id>.SYSTEM.md` |
| Structural evals | `evals/portfolio/<agent-id>.v1.json` |
| Compiled manifest | `portfolio/canonical-portfolio.manifest.json` |
| Immutable capability pack | `capability-packs/canonical-portfolio/sha256-<digest>/manifest.json` |
| Compiler | `scripts/generate_canonical_portfolio.py` |
| Structural validator | `scripts/validate_canonical_portfolio.py` |
| Focused tests | `scripts/test_canonical_portfolio.py` |

### Civilization v2 draft projection

| Artifact | Contract |
| --- | --- |
| Identity contract | `docs/agent-portfolio/CIVILIZATION_144_IDENTITY_CONTRACT.md` |
| Source matrix receipt | `portfolio/sources/civilization-matrix.public.2026-08-26.json` |
| Governed portfolio | `portfolio/civilization-portfolio.v2.json` — 50 preserved + 94 expansion drafts |
| Shared typed graph | `portfolio/civilization-graph.v2.json` — one graph plane, not 144 isolated diagrams |
| Compiler and validator | `scripts/compile_civilization_portfolio.py` |
| Focused tests | `scripts/test_civilization_portfolio.py` |

V2 is an additive, public-safe projection. It does not replace the native v1 cards, grant runtime
authority, or imply that every role needs a cinematic humanoid portrait. Deep characters remain
scarce; compact guides, symbols, instruments, and environmental intelligences carry the remainder.

The capability pack is content-addressed and immutable. It is still descriptive evidence, not an
authority token. Authenticated runtime leases, server-owned routing policy, tool adapters, and
human approvals independently decide what any runtime may do.

## Stable roster

| Swarm | Conductor | Four specialists |
| --- | --- | --- |
| `sovereign-command` — Sovereign Command | `astra-sovereign` — Astra | `orion-mission-architect`, `vera-decision-verifier`, `cassian-resource-steward`, `mira-continuity-keeper` |
| `product-forge` — Product Forge | `ignis-product-conductor` — Ignis | `nova-customer-discovery`, `tess-system-designer`, `rivet-build-engineer`, `prism-quality-critic` |
| `intelligence-research` — Intelligence & Research | `lyra-research-conductor` — Lyra | `atlas-signal-scout`, `verity-source-auditor`, `soren-synthesis-analyst`, `delta-forecast-challenger` |
| `creator-worlds` — Creator Worlds | `ember-creator-conductor` — Ember | `aria-story-architect`, `sol-visual-world-director`, `echo-audience-resonance`, `cadence-release-producer` |
| `revenue-venture` — Revenue & Venture | `meridian-venture-conductor` — Meridian | `piper-demand-strategist`, `ledger-unit-economist`, `bridge-partnership-architect`, `clara-deal-critic` |
| `community-academy` — Community & Academy | `sophia-academy-conductor` — Sophia | `kai-curriculum-architect`, `mina-community-steward`, `pulse-cohort-facilitator`, `rune-learning-evaluator` |
| `trust-safety` — Trust & Safety | `aegis-trust-conductor` — Aegis | `sentinel-risk-analyst`, `cipher-privacy-steward`, `equa-policy-auditor`, `beacon-incident-coordinator` |
| `health-flourishing` — Health & Human Flourishing | `solace-flourishing-conductor` — Solace | `terra-nutrition-educator`, `kinetica-movement-coach`, `serene-reflection-guide`, `harbor-care-navigator` |
| `enterprise-transformation` — Enterprise Transformation | `vector-transformation-conductor` — Vector | `maya-operating-model-architect`, `quorum-governance-designer`, `relay-change-enablement`, `metric-value-realization` |
| `web-spatial-protocol-futures` — Web/Spatial/Protocol Futures | `nexus-futures-conductor` — Nexus | `pixel-web-experience-architect`, `orbit-spatial-interface-designer`, `lattice-interoperability-architect`, `horizon-futures-scout` |

Each source agent explicitly defines canonical id, display name, semantic version, draft status,
purpose, outcomes, role lineage, public profile, voice and method, existing skill references,
capabilities and non-capabilities, stop and escalation conditions, graph edges, visual DNA, and two
role-specific eval cases. The compiler adds the shared authority/privacy cases and produces four
structural cases per agent (200 total).

## Public and high-stakes boundaries

- All 50 cards use public-safe `session` memory, empty private KB lists, and `web` / `coe_demo`
  surfaces. No private steward, SIS vault, credential, or private-memory reference is loaded.
- Skill ids are references to existing installed skills. They are not copied, created, or treated as
  runtime grants by this repo.
- Tools are draft/read/analysis/handoff classes only. External send, spend, credentials,
  destructive action, production change, and private/cross-tenant access remain denied and gated.
- Health roles provide general education and navigation only. They deny diagnosis, treatment,
  clinical prescribing, sensitive health storage, and crisis-service substitution; urgent or
  clinical situations escalate to qualified local humans and services.
- Trust roles are defensive and report-only. They deny offensive action, surveillance, and
  autonomous enforcement.
- Future-facing roles label scenarios and proposals. They cannot declare standards, activate
  identity/protocol changes, or present experimental concepts as deployed facts.

## Visual asset contract

Every compiled card points to one downstream portrait asset:

```text
assets/starlight-constellation/v1/agents/<swarm-id>/<agent-id>.webp
```

Its avatar / visual asset id is `<agent-id>-v1`. The source catalog contains the portrait archetype,
signature object, silhouette, accent, swarm palette, materials, lighting, setting, negative cues,
and portrait brief. The compiler does **not** create or edit image assets; asset generation and
provenance remain a separate lane.

## Maintenance workflow

1. Edit only `portfolio/canonical-portfolio.v1.json` for roster content.
2. Keep exactly ten canonical swarm ids, five unique agents per swarm, one conductor, and four
   specialists whose graph depends on that conductor.
3. Reference only entries already listed in the source `skill_registry`; add references, not skills.
4. Keep all agents `draft` while `live_eval_status` is `not_run`.
5. Regenerate and verify:

```powershell
python scripts/generate_canonical_portfolio.py --write
python scripts/generate_canonical_portfolio.py --check
python scripts/validate_canonical_portfolio.py
python scripts/test_canonical_portfolio.py
python scripts/validate_agent_cards.py
python scripts/run_eval_suite.py
```

Generation updates card, prompt, eval, and compiled-manifest projections atomically. A capability
contract change creates a new content-addressed pack; an existing pack is never overwritten.
Unexpected stale projections fail validation and must be reviewed and removed explicitly.

## Promotion gate

Schema validity, projection parity, and structural eval fixtures do not establish model quality,
production readiness, or runtime admission. Promotion from `draft` requires live model-graded
evaluation on the exact card/runtime/model combination, an independent review, authenticated
admission controls, and the relevant human approvals from the ADLC.
