# ADK / OpenAI Agents SDK backend contract

Optional workflow engines may implement tools and multi-step graphs.
They **must not** own identity.

## Required load path
1. Resolve `agent_id` → load card JSON from this repo (or signed mirror).
2. System / developer instructions = `soul_md` + identity fields only.
3. Tools = intersection(card.will.tools_allow, server allowlist) − tools_deny.
4. Memory adapter enforces card.mind.memory_scope.
5. Human gates remain UI/API enforced even if the ADK loop can call tools.

## Forbidden
- Embedding a parallel long-lived persona prompt that diverges from the card
- Exposing private_vault cards on web/phone/coe_demo surfaces
- Skipping eval suite association for `status: active` public cards

## Parity check
Before production: same golden prompts against Vercel body and ADK body must both clear min_pass_rate (live harness — see ADLC EVAL stage; structural dry-run is not sufficient alone).
