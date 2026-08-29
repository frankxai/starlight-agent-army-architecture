# Business Ops Cell — Agent Instructions (template)

> Copy into a private ops repo as `AGENTS.md` only when instantiating.  
> Identity SSOT remains `starlight-agent-army-architecture` Agent Cards (`biz-*`).

Private supervisor stack for business agents.

## Topology

1. **Founder** sets goals and irreversible gates.  
2. **biz-ops-supervisor** admits work and routes one primary lane.  
3. **biz-*** specialists produce artifacts only in-lane.  
4. **biz-qa-red-team** (or gstack `/review`/`/qa`/`/cso` for code) checks consequential outputs.  
5. Human approves publish / spend / external send / legal.

## Do

- Load the matching Agent Card before acting.  
- Write durable artifacts (brief, task packet, draft, receipt).  
- Prefer existing skills listed on the card over inventing new agents.  
- Use swarm-bus / work-ledger for cross-session durability.

## Do not

- Spin parallel unsupervised agents.  
- Auto-publish, auto-pay, or auto-send contracts.  
- Put private vault memory on public product agents.  
- Treat Paperclip, gstack, or GitHub Agent HQ as soul SSOT.

## Coding lanes

Use **gstack** role gears and optional **GitHub Agent HQ** for implementation/review/ship. Business supervisor still owns priority and human gates.

## Handoff format

- Objective  
- Artifact paths  
- Validation run  
- Residual risks  
- Exact human actions required  
