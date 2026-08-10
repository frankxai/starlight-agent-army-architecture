# Business Agent Supervisor Stack

> Status: **ACTIVE TEMPLATE** (2026-08-10)  
> SSOT repo: `frankxai/starlight-agent-army-architecture`  
> Cards: `cards/stewards/biz-ops-supervisor.json` + `cards/specialists/biz-*.json`  
> Companion: `docs/agent-portfolio/BUSINESS_OPS_ORG.md`, `templates/business-ops-supervisor/`

## Verdict (research + estate truth)

**You already have the control plane.** You do **not** need to greenfield a twelfth “agent company OS.”

| Layer you asked for | Estate truth | Action |
| --- | --- | --- |
| Supervisor architecture | Starlight Queen + Hermes + swarm bus + maker/checker | **Keep & harden** |
| AGENTS.md / skill doctrine | Estate `AGENTS.md`, repo contracts, AOS Standard | **Keep** |
| Faced agent identity | Agent Cards + ADLC in this repo | **Extend** (this template) |
| Business OS template | `agentic-business-os` + AOS modules | **Derive instances**, don’t fork souls |
| Coding mission control | **gstack** (installed) + **GitHub Agent HQ** (Copilot Claude/Codex) | **Leverage for code lanes only** |
| Org-chart business UI | **Paperclip** (open-source org/goals/budget) | **Evaluate as optional body**, not identity SSOT |

**Decision:** Advance **our** supervisor + Agent Card template first. Absorb patterns from gstack / Paperclip / Agent HQ. Do **not** replace Queen/Hermes identity with any of them.

## External landscape (what to steal vs skip)

### GitHub Agent HQ
Mission control for **coding** agents (Copilot, Claude, Codex) across GitHub / VS Code / mobile / CLI. Assign, steer, track parallel coding work.

- **Steal:** multi-agent sessions view, async cloud agents, one place to assign coding missions.  
- **Skip as business OS:** it is not recruiting/runway/community/CRM.  
- **Estate fit:** parallel to `coding-agents` + gstack; use when Frank is in VS Code/GitHub.

### gstack (Garry Tan / YC)
Role gears for Claude Code: CEO review, eng manager, designer, QA browse, CSO, ship, retro — **slash-command virtual eng team**. Already present in Hermes/agent skill surfaces.

- **Steal:** opinionated role modes, plan→build→review→ship loop, real-browser QA.  
- **Skip:** treating gstack as multi-brand soul SSOT.  
- **Estate fit:** wire **biz-qa-red-team** and coding maintainers to gstack `/review`, `/qa`, `/cso`, `/ship` — not to new chatbots.

### Paperclip
Open-source **org chart + goals + budgets + governance** over *bring-your-own* agents (Claude Code, scripts, webhooks). “Not a chatbot; not an agent framework — run a company made of agents.”

- **Steal:** org chart UI, goal hierarchy, budget caps, heartbeat hire model.  
- **Skip:** second durable queue that races swarm-bus / work-ledger.  
- **Estate fit:** optional **visualization/admission UI** later if it compiles cleanly onto our cards + ledgers; pilot only after third-party runtime admission gate.

## Recommended architecture (canonical)

```text
Founder (human owner + gates)
        │
        ▼
┌───────────────────────────┐
│  biz-ops-supervisor       │  private L4 steward under Starlight Operator
│  (mission control)        │
└───────────┬───────────────┘
            │ routes one lane at a time (or bounded parallel with leases)
    ┌───────┼────────┬──────────┬──────────┐
    ▼       ▼        ▼          ▼          ▼
 Capture  CoS    Content    Runway     QA Red Team
    │       │        │          │          │
    └───────┴──── artifacts ────┴──────────┘
            │
            ▼
 Independent checker → human gate (publish/spend/send/legal)
```

**Runtime binding**

| Concern | Owner |
| --- | --- |
| Identity / souls | Agent Cards in this repo |
| Private execution | Hermes + Queen |
| Cross-machine tasks | `swarm_bus` (agentic-ops) |
| Coding specialists | gstack + coding-agents + optional Agent HQ |
| Public product faces | Gen-Ω / FrankX Concierge (separate portfolio) |
| Business website instances | `agentic-business-os` template |
| Money truth | `agentic-money-os` / CFO skill / business ledger |

## Role gap map (your stack → estate)

| Agent | Human owner | Maturity | Maps to existing | Card id |
| --- | --- | --- | --- | --- |
| Founder Capture | you | partial | audio-producer, content-lifecycle, Telegram capture | `biz-founder-capture` |
| Chief of Staff | VA | strong | daily-ops, outcome cockpit, Queen briefs | `biz-chief-of-staff` |
| Delegation | VA | strong | project-brief, swarm envelopes, job contracts | `biz-delegation` |
| Recruiting | VA + you | partial | dream100-talent-magnet, hr-agency-os | `biz-recruiting` |
| Bounty | VA | **gap** | job contracts only — no reward runtime | `biz-bounty` |
| Contributor Onboarding | VA | partial | docs/onboarding patterns | `biz-contributor-onboarding` |
| QA / Red Team | VA + you | strong | claims-guard, design-review, gstack CSO/QA | `biz-qa-red-team` |
| Content Hydra | content human | strong | content-lifecycle, frankx content, Gen-Ω | `biz-content-hydra` |
| Partnership | VA/sales | partial | partner hubs, roundtable messaging | `biz-partnership` |
| Runway | you + accountant | strong | cfo, agentic-finance-os, money-os | `biz-runway` |
| Sales Pipeline | you/sales | partial | chief-revenue-operator; CRM thin | `biz-sales-pipeline` |
| Community Ritual | VA/community | partial | build-in-public, gencreator-community | `biz-community-ritual` |
| **Supervisor** | you | strong | Queen + Hermes + bus | `biz-ops-supervisor` |

## What we built this session

1. Draft Agent Cards + souls + structural evals for supervisor + 12 specialists.  
2. Org SSOT: `docs/agent-portfolio/BUSINESS_OPS_ORG.md`.  
3. Portable template: `templates/business-ops-supervisor/`.  
4. KB pack: `kb-packs/starlight/business-ops-supervisor.md`.  
5. Queen receipt under control plane reports.

## Massive action plan (phased)

### Phase 0 — Lock doctrine (done / this PR lane)
- [x] Gap map + external research synthesis  
- [x] Draft cards under Starlight Operator  
- [x] Template pack + org doc  
- [ ] Validate cards (`python scripts/validate_agent_cards.py`)  
- [ ] Draft PR on army-architecture branch  

### Phase 1 — Wire live routing (next, 1–2 sessions)
1. Add supervisor router skill note or Hermes command `/biz` → routes to `biz-*` cards.  
2. Map Chief of Staff weekly brief onto existing outcome cockpit + work ledger.  
3. Bind Content Hydra → Gen-Ω / frankx content skills (no second content stack).  
4. Bind QA Red Team → claims-guard + gstack `/review` `/qa` `/cso`.  
5. Bind Runway → CFO / money-os read-only dashboards.  

### Phase 2 — Close real gaps (bounded product work)
1. **Bounty** runtime: quest schema + rubric + human-gated reward ledger (private ops, not crypto theater).  
2. **Sales CRM** thin adapter: stages + proposal draft + follow-up queue (Notion/Airtable/HubSpot pick one).  
3. **Founder Capture** pipeline: voice → structured packet → CoS inbox (Himalaya/Telegram already partial).  
4. **Onboarding** pack generator from role + first tasks templates.  

### Phase 3 — Optional leverage (evaluate, don’t merge identity)
1. **Agent HQ**: enable for coding missions when Copilot tier includes Claude/Codex; keep Queen as estate supervisor.  
2. **Paperclip pilot**: read-only org chart over our cards if admission gate passes; no second task bus.  
3. **agentic-business-os**: for client/foundry installs, export sanitized subset of this stack as a pack.  

### Explicit non-goals
- Building “Paperclip but Starlight” as a greenfield product this week  
- 144 public business faces  
- Auto-send, auto-pay, auto-hire  
- Replacing Agent Cards with gstack markdown alone  
- Public L5 business swarms without receipts  

## Operating rules (non-negotiable)

1. **One supervisor** admits work; specialists do not freestyle.  
2. **One writer** per repo/path lease.  
3. **Maker ≠ checker** on publish/legal/spend-adjacent artifacts.  
4. **Human gates** stay in card `will.human_gates`.  
5. **Chat is not SSOT** — ledger, PR, receipt, or CRM row is.  
6. **Identity in git cards**; gstack/Paperclip/Agent HQ are bodies/tools.  

## Validation

```bash
cd C:/Users/frank/starlight/repos/starlight-agent-army-architecture
python scripts/validate_agent_cards.py
```

## Sources (external)
- GitHub Agent HQ / mission control announcements and VS Code multi-agent development notes  
- Paperclip (`paperclip.ing`, `paperclipai/paperclip`) org-chart orchestration  
- gstack (`garrytan/gstack`) role-based Claude Code skill pack  

Estate primary sources remain local cards, Queen skills, and AOS Standard.
