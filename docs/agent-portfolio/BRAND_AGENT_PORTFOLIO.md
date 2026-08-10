# Brand Agent Portfolio — SSOT Decision Record

> Status: ACTIVE EXECUTION (2026-08-09)  
> Owner: Starlight Queen (Yogabook)  
> Repo SSOT: `frankxai/starlight-agent-army-architecture`  
> Consumers: GenCreator-Studio, frankx.ai, arcanea-ai-app, Hermes, ai-coe  
> Companion: `docs/adlc/ADLC.md`, `docs/operations/AGENT_ECONOMICS_AND_CAPABILITY.md`, `observability/`, `schemas/agent-card/`

## Relationship to existing repo systems

This repo already documents **Codex control plane · Hermes profiles · OpenClaw gateway · DeepAgents · SIS provenance** (`README.md`, `docs/swarm-roles.md`, `configs/*`).

**Agent Cards + ADLC do not replace that runtime army.** They are the **identity / productization layer on top**:

| Layer | Owner in this repo |
|-------|-------------------|
| Runtime army (how workers run) | Existing docs + configs (Hermes profiles, gateways, harnesses) |
| Identity (who the agent is, face, KB, tools, memory scope) | **NEW:** `cards/`, `kb-packs/`, `schemas/agent-card/`, ADLC |
| Brand portfolio decisions | **NEW:** this document |
| Product UI bodies | Brand apps (GenCreator-Studio, frankx.ai) via `docs/execution/WEB_LOAD_CONTRACT.md` |

Hermes profiles remain durable workers. Cards are what those workers (and web shells) **load** so souls are not forked per SDK.

## Thesis

One **Agent Card factory**. Many brand skins. Identity is git SSOT. SDKs are bodies, not souls.

```
Agent Card (soul + face + KB + tools + memory scope + permissions)
        │
        ├─ Hermes / Queen ………… L4–L5 life + ops (private)
        ├─ Brand Next apps ……… L1–L3 product chat (Vercel AI SDK UI)
        └─ Optional ADK backends … workflow engines only (never identity home)
```

## SDK law

| Layer | Choice | Non-choice |
|-------|--------|------------|
| Product chat UI | **Vercel AI SDK** in brand Next apps | Not identity SSOT |
| Life / ops runtime | **Hermes** (+ Queen swarm) | Not public tenant default |
| OpenAI Agents SDK | Optional backend handoffs | **Not** bundled into Vercel AI SDK |
| Google ADK | Optional GCP hierarchical workflows | Not brand soul home |
| Claude / Codex CLIs | Builder / maintainer lanes | Not customer faces |

## Persona law

| Layer | Rule |
|-------|------|
| Host | **One** front-door persona per public brand |
| Specialists | 5–12 under host (custom GPT / Gem pattern) |
| Real personas (L3) | Scarce: brand icons only |
| Stewards (L4) | Private / enterprise — face optional |
| Swarm (L5) | Behind host; chip when summoned; human gates on spend/publish |

## Operating/autonomy tier

L0–L5 describes system shape, permissions, memory, and orchestration complexity. It is not an intrinsic intelligence or quality score. Observed capability is measured per deployment with role-specific weights, hard safety gates, and a minimum live sample; see `docs/operations/AGENT_ECONOMICS_AND_CAPABILITY.md`.

| Tier | Name | Public default? |
|------|------|-----------------|
| L0 | Skill / procedure | Yes (OSS, CoE) |
| L1 | Host chat + brand KB + light memory | Yes |
| L2 | Specialist handoff packs | Yes |
| L3 | Full face + deep soul | Scarce public |
| L4 | Steward + tools + long memory | Private / paid |
| L5 | Multi-agent cell + evals | Ops / enterprise pilots |

## Brand portfolio (build what)

### P0 — build first

| Brand | Tribe | Host | Specialists (v1) | Live surface | Memory |
|-------|-------|------|------------------|--------------|--------|
| **GenCreator** | Creators, founders, studio users | **Gen-Ω** L1→L3 | Producer, Visual, Hook, Critic, Ship | `gencreator.ai` + GenCreator-Studio | user/org project |
| **FrankX** | Architects, operators, demand | **FrankX Concierge** L1 | Content, SEO, Interview-private | frankx.ai soft/sign-in | session → light user |
| **Starlight (you)** | Operator excellence | **Hermes / Queen** L4–L5 | SIS roster as internal roles | Hermes desktop/Telegram | private vaults |

### P1 — next

| Brand | Host | Notes |
|-------|------|-------|
| **Arcanea** | Lumina (or locked host) L3 | Lore Keeper hard-canon; few characters |
| **AI-Architect / CoE** | Neutral professional host L1–L2 | ai-coe demo + client templates; enterprise chrome |

### P2 — later / demand-gated

Income/RA thin L1 · Anime Legends companion · public Starlight concierge · Mind/Family/Health **patterns only** (never your raw vaults on public products)

## Explicit non-goals (now)

- 144 public faces
- OpenAI/Google ADK as identity home
- Private vaults on marketing chat
- Native apps before GenCreator PWA
- Public L5 swarms without proof gates
- New top-level home folders / invent-a-verse bases

## Where knowledge lives

| Scope | Location | Who sees |
|-------|----------|----------|
| Public brand KB packs | This repo `kb-packs/<brand>/` + product repo mirrors | Signed-in product users |
| Agent Card souls | `cards/**` | All runtimes load same card |
| Tool contracts | Card `will.tools` + runtime allowlists | Enforced per surface |
| User/org memory | Product DB / tenant store | That tenant only |
| Frank private memory | Hermes + SIS private mounts | Frank / gated stewards |
| Arcanea canon | `arcanea-ai-app/.arcanea/lore/CANON_LOCKED.md` | Arcanea agents only |

## Where tools live

| Surface | Tool class |
|---------|------------|
| Public web | Search, brand KB retrieve, project CRUD, image gen (metered), export |
| GenCreator Studio | Studio pipelines, asset QA hooks, ship checklist |
| Hermes | Full computer-use, git, swarm, vault, multi-CLI — private |
| CoE demo | Sandboxed tools + policy dry-run |

## Frontend embed map

| App | Embed |
|-----|--------|
| GenCreator-Studio / gencreator.ai | Primary product agent shell (Vercel AI SDK) |
| frankx.ai | Thin concierge |
| arcanea-ai-app | Character + lore agents (P1) |
| ai-coe apps/dashboard | Governed roster demo (P1) |
| Hermes | Full stewards + swarm |
| Phone | PWA of Gen-Ω first |

## Success metrics (portfolio)

Construction counts below show portfolio coverage; they do not prove customer value or intelligence. Every runtime also needs a deployment profile and receipt-backed scorecard.

| Metric | Target (90d) |
|--------|----------------|
| Hosts live with card + face pack | ≥3 (Gen-Ω, FrankX Concierge, Hermes Operator card) |
| Public specialists wired | ≥5 under Gen-Ω |
| Cross-runtime card parity | Hermes profile import OR documented adapter stub |
| Tenant memory leak tests | 0 critical |
| Design anti-slop on agent shells | pass verify script on touched UIs |
| Artifact score on Queen lanes | ≥2 (draft PR + gates) for implementation lanes |
| Valid receipt coverage after instrumentation | ≥95% within 14 days |
| Critical tenant/safety failures | 0 |
| Capability and ROI decision | only after role-specific minimum live sample |

## Decision log

| Date | Decision |
|------|----------|
| 2026-08-09 | Single strategy repo: `starlight-agent-army-architecture` (not sprawl across all repos) |
| 2026-08-09 | GenCreator = first full faced product; Hermes = private excellence; FrankX = demand router |
| 2026-08-09 | Vercel AI SDK = UI; cards = SSOT; ADKs optional backends only |
| 2026-08-10 | L0–L5 renamed operating/autonomy tier; capability, cost, and ROI move to deployment receipts + scorecards |

## Related

- `docs/adlc/ADLC.md` — Agent Development Life Cycle
- `docs/execution/10H_QUEEN_SWARM_PLAN.md` — active 10h swarm
- `schemas/agent-card/agent-card.schema.json`
- `docs/operations/AGENT_ECONOMICS_AND_CAPABILITY.md`
- `observability/` — deployment goals, metric catalog, adoption snapshot, synthetic receipt examples
- `cards/hosts/*`
- Estate: `starlight/ECOSYSTEM.md`

## Private business ops cell (2026-08-10)

Internal supervisor stack under Starlight Operator (not a public brand host):

- [BUSINESS_OPS_ORG.md](BUSINESS_OPS_ORG.md)
- [../operations/BUSINESS_AGENT_SUPERVISOR_STACK.md](../operations/BUSINESS_AGENT_SUPERVISOR_STACK.md)
- Cards: `biz-ops-supervisor` + `biz-*` specialists (draft)
