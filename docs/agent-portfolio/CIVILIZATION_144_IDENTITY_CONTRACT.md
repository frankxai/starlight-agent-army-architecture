# Starlight Civilization 144 identity contract

> Status: implementation contract for a draft public projection  
> Target: exactly 144 stable agent profiles  
> Runtime authority: none  
> Production source: `frankxai/starlight-intelligence-web`  
> Agent Card and prompt source: this repository

## Why this contract exists

The live Starlight Intelligence site currently publishes fifty deep agent dossiers. A separate ready preview presents a twelve-ring, 144-seat civilization matrix derived from the SIS agent blueprint. The matrix is valuable, but its seat number and ring placement are editorial presentation data. It does not yet provide stable agent IDs, profile URLs, skills, voice, boundaries, prompt contracts, evals, or visual assets.

The expansion must not discard the fifty complete profiles, create 194 competing identities, or promote sequential seat numbers into permanent identity. The target is one coherent portfolio of exactly 144 profiles:

- the founding fifty retain their existing `agent_id`, slug, public URL, story, prompt, boundaries, and card depth;
- ninety-four new profiles are added from verified SIS blueprint lineages;
- every profile maps to a source lineage without claiming that a public persona is a live process;
- ring, seat, visual form, and current workflow are mutable projections over a stable identity.

## Identity hierarchy

| Field | Meaning | Stability |
| --- | --- | --- |
| `agent_id` | Canonical public identity key | Immutable after publication |
| `profile_slug` | Public URL slug | Stable; redirects required on change |
| `source_identifier` | Blueprint file lineage | Stable provenance key; may be versioned |
| `legacy_agent_id` | Existing founding-profile key when applicable | Immutable alias |
| `seat` | Presentation order from the imported blueprint | Mutable, never an identity key |
| `ring_id` | Current editorial constellation | Mutable projection |
| `workflow_ids` | Shared workflows in which the agent may participate | Mutable projection |
| `morphology_family` | Current visual embodiment family | Mutable and surface-specific |

The durable registry is `portfolio/civilization-identity-lock.v1.json`. It contains exactly 144 mappings from `source_identifier` to immutable `agent_id` and stable `profile_slug`. Its seal covers the sorted source-identity set, not mutable ring or seat presentation. The compiler resolves identity only through this lock; it never derives an identity from current seat or ring order.

Every lock entry includes `alias_history`, `redirects`, and `migration_history`. A source rename fails closed until the lock is deliberately migrated. A source migration must retain the old source identifier as an alias and include a reviewed receipt. A profile-slug change additionally requires a permanent redirect from the old slug. `agent_id` is immutable and has no migration path.

The compiler rejects duplicate or missing `agent_id`, `profile_slug`, or `source_identifier` values, lock/matrix drift, missing migration receipts, and identities derived only from a numeric seat.

## Founding fifty preservation

The founding fifty are not renamed or regenerated from templates. Their current rich fields remain authoritative until deliberately revised:

- purpose, method, outcomes, voice, and personality;
- capabilities and explicit non-capabilities;
- stop and escalation conditions;
- verified skill references;
- prompt contract and structural eval suite;
- visual DNA and existing public portrait receipt;
- existing inbound, outbound, and dependency relationships.

Each founding profile receives one curated SIS blueprint lineage. A mapping is a provenance relationship, not a claim that the public persona and an executable agent file are the same artifact. Its current status is `curated_draft`; it cannot be promoted without the declared review receipts.

Each v2 founding projection carries content-addressed receipts for its v1 agent card, system prompt contract, structural eval suite, visual asset, visual source map, and immutable capability pack. It also carries a digest of all preservation-critical v1 fields. Validation compares the actual values, not only the founding IDs.

## Ninety-four expansion profiles

New profiles begin as `blueprint_draft`. Their initial source-backed fields are generated from the blueprint display name, domain, responsibility, and source identifier. Every new profile must then pass the same ADLC depth gate as the founding fifty before production:

1. role and outcome contract;
2. method and bounded capabilities;
3. explicit non-capabilities, stops, and escalation;
4. verified skill references;
5. prompt contract;
6. structural evals and adversarial cases;
7. shared-graph participation;
8. visual morphology and asset provenance;
9. public-safety review;
10. profile-page rendering and accessibility QA.

Generated prose is scaffolding, not evidence of capability or deployment.

The imported blueprint responsibility is authoritative only under `lineage.source_responsibility` with `responsibility_is_capability_claim: false`. Generated method copy may quote that responsibility solely inside an explicit provenance-only sentence; it cannot promote the source wording into a capability or execution claim. Every expansion profile has:

- `execution_mode: draft_recommend_only`;
- `tool_binding: none`;
- `required_human_gate: human-gate-expansion-draft`;
- `grants_authority: false`;
- `external_effects: prohibited`.

The safe draft layer does not claim authority to publish, send, approve, diagnose, treat, spend, deploy, or operate. It prepares evidence and review packets. Expansion `depends_on` and `routes_to` remain empty with `relationship_status: unresolved_pending_explicit_review`; editorial seat order cannot create an operational dependency.

Generated copy also passes a deterministic language-quality gate. Artifact names carry reviewed singular and plural forms rather than guessed suffixes; an article helper handles vowel sounds; the bounded qualifier is applied exactly once; and method phrases use a gerund after “by.” Validation scans every prose-bearing field and eval case across all ninety-four expansion profiles for adjacent duplicate words and malformed method phrasing. Public domain labels preserve meaningful casing such as `DeFi` and `IP`, while reviewed wording replaces internal shorthand where needed. Reviewed source-identifier overrides resolve ambiguous keyword collisions, and each public profile, first outcome, and safe capability includes its own seat-specific focus without treating the source responsibility as authority.

## One graph plane

The 144 profiles do not each own a private graph. They are nodes and projections in one typed Starlight graph plane.

Required node types:

- `agent`;
- `ring`;
- `workflow`;
- `human_gate`;
- `proof_artifact`;
- `memory_writeback`.
- `failure_state`.

Required edge types:

- `member_of`;
- `routes_to`;
- `depends_on`;
- `participates_in`;
- `verifies`;
- `hands_off_to`;
- `forks_to`;
- `converges_to`;
- `loops_to`;
- `failure_routes_to`;
- `requires_human_gate`;
- `produces_proof`;
- `writes_back`.

Every edge carries an immutable edge ID, provenance, and status. Ring membership is explicitly `presentation_only`; founding relationship edges are preserved v1 drafts; workflow edges are explicit v2 architecture contracts. Agent pages show a filtered neighborhood of this shared graph. They must never imply a separate runtime or memory system per profile.

## Shared workflow library

The first public workflow projections use explicit multi-agent mechanics rather than decorative lines:

1. **Intent to bounded mission** — router, mission framing, human confirmation.
2. **Research to evidence** — parallel discovery, source audit, synthesis, challenge, convergence.
3. **Build to verified artifact** — design, implementation, independent verification, failing initializer, proof receipt.
4. **Story to responsible release** — narrative, media, accessibility, rights, human publish gate.
5. **Incident to safe recovery** — detection, containment, diagnosis, recovery proposal, human authorization.
6. **Learning to demonstrated mastery** — learner model, curriculum, practice, evaluation, reflection writeback.
7. **Marketplace adoption** — need routing, pack selection, compatibility check, installation plan, human install gate.
8. **Memory and continuity** — source capture, privacy boundary, synthesis, contradiction check, governed writeback.

Every workflow declares step IDs and explicit topology edges. Router patterns must route to at least two branches; diamonds must fork and converge; converge patterns must bring at least two inputs to a reducer; loops must expose a real `loops_to` edge; chains cannot hide a branch. Every maker/reducer output has an independent verifier and the final verifier cannot be a maker.

Every workflow also declares entry criteria, exit proof, writeback behavior, and a failure state. Its structured brakes include positive ceilings for turns, cost, empty rounds, and silence. Every active step has an explicit `failure_routes_to` edge. A brake stops work, preserves the last valid evidence, and escalates; it does not retry automatically and silence is never approval.

## Promotion state machine

The initial status is `founding_rich_draft` for the founding fifty and `blueprint_draft` for the expansion ninety-four. Allowed transitions are explicit:

1. `blueprint_draft` → `enriched_draft` → `review_ready`;
2. `founding_rich_draft` → `review_ready`;
3. `review_ready` → `preview_approved` → `production_approved`.

Every transition requires `receipt_ref`, `reviewed_by`, `reviewed_at`, and human approval. The current expansion projection has no promotion history and all ninety-four profiles remain `blueprint_draft`.

## Visual embodiment is not authority

Morphology communicates role and context; deterministic UI communicates truth.

- `.ai` consequential profiles: full specialist, guardian, instrument, or compact specialist.
- `.org` public-interest stories: biotech, instrument, swarm, or room-scale intelligence.
- Academy and onboarding: chibi guide, compact specialist, creature companion, or soft-shell collaborator.
- Graphs, lists, logs, and notifications: micro-avatar plus deterministic state glyph.
- Marketplace: compact/avatar pair with exact compatibility and permission data.
- Spatial experiences: selected canonical form with a simplified level-of-detail fallback.

Cute scale, height, polish, or cinematic lighting never indicates permissions, confidence, intelligence, or rank.

## Production promotion gate

The 144 projection is promotable only when all of the following are true:

- exactly 144 unique stable identities;
- all fifty legacy URLs resolve without story loss;
- ninety-four new profiles pass the required schema;
- shared graph validates without dangling references or same-actor verification;
- all workflow brakes and human gates are visible;
- no private memory, credentials, or runtime authority enter the public artifact;
- visuals have inspected exports and provenance;
- production pages pass build, accessibility, responsive, and visual QA;
- a Vercel preview is reviewed before production;
- founder approval is recorded for brand-defining visual and production promotion.

## Fail-closed source provenance

The matrix declares `frankxai/Starlight-Intelligence-System`, commit `3f775458f0acc6ac04514c68ef8307ddd01ccf8e`, `docs/AGENT_BLUEPRINT.md`, and the raw blob SHA-256. Normal compiler runs require a local Git checkout whose origin, commit, file blob, and SHA-256 match that receipt. Each of the 144 source identifiers, display names, domains, and responsibilities must occur together on one verified source row. `--matrix-json` does not bypass verification. An unverified override exists only for isolated tests and cannot write generated artifacts or initialize the identity lock.

## Source receipts

- Live fifty-profile portfolio: `portfolio/canonical-portfolio.v1.json`.
- Immutable 144-identity registry: `portfolio/civilization-identity-lock.v1.json`.
- Generated governed profile projection: `portfolio/civilization-portfolio.v2.json`.
- Generated shared graph projection: `portfolio/civilization-graph.v2.json`.
- JSON Schemas: `schemas/agent-portfolio/civilization-identity-lock.schema.json`, `civilization-portfolio-v2.schema.json`, and `civilization-graph-v2.schema.json`.
- 144-seat preview source: `frankxai/starlight-intelligence-web`, branch `codex/constellation-civilization`, file `data/civilization-matrix.public.json`, commit `d5db530c6e1b6082506aab8d356486a51ee307b7`.
- Underlying blueprint receipt declared by that matrix: `frankxai/Starlight-Intelligence-System`, `docs/AGENT_BLUEPRINT.md`, commit `3f775458f0acc6ac04514c68ef8307ddd01ccf8e`.
