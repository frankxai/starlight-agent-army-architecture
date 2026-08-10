# Template: Business Ops Supervisor Stack

Portable starting point for a **supervisor architecture** of private business agents.

## When to use

- Founder wants CoS / capture / content / runway / recruiting agents without chatbot soup  
- Deriving a private ops cell for a brand or client (sanitize before public)  
- Aligning gstack (code roles) + optional Paperclip UI + Hermes execution under one org  

## What you get

| File | Purpose |
| --- | --- |
| `org.yaml` | Machine-readable org + maturity + human owners |
| `AGENTS.template.md` | Copy to private ops repo as `AGENTS.md` when instantiating |
| `ROLE_MATRIX.md` | Human-readable role map |
| `../` cards in army-architecture | Canonical identity SSOT (copy or reference) |

## Instantiate

1. Keep **identity** in `starlight-agent-army-architecture` cards (or fork cards into private instance).  
2. Copy `AGENTS.md` + `org.yaml` into the private ops repo or Business OS instance.  
3. Bind runtimes:
   - Hermes/Queen = supervisor + private specialists  
   - gstack = coding CEO/EM/QA/CSO gears  
   - Agent HQ = optional coding mission control  
   - Paperclip = optional org UI only after admission gate  
4. Activate one lane first: **Chief of Staff weekly brief** or **Content Hydra** — not all twelve.  

## Non-negotiables

- Human gates on publish / spend / external_send / legal  
- Maker ≠ checker  
- No second task bus if swarm-bus / work-ledger already owns durability  
- Public product agents never load `private_vault` cards  
