# Web runtime load contract (Vercel AI SDK)

## Purpose
Brand Next apps load Agent Cards without forking souls.

## Flow
1. Resolve `agent_id` (default host per brand).
2. Fetch card JSON from this repo publish path or mirrored `public/agents/`.
3. Build system message = `SOUL.md` + identity.voice + boundaries + approach.
4. Attach tools from `will.tools_allow` minus deny; enforce human_gates in UI.
5. Retrieve KB packs listed in `mind.public_kb`.
6. Memory adapter respects `mind.memory_scope` only.
7. Specialists: host sets `active_specialist_id`; UI shows chip; on complete return to host.
8. **Handoff memory rule:** never carry `private_kb` / `private_vault` content across a memory_scope boundary. Only a structured task packet (goal, non-secret constraints, artifact ids) may cross.

## GenCreator default
- Host: `gen-omega`
- Specialists: `gen-producer`, `gen-visual`, `gen-hook`, `gen-critic`, `gen-ship`

## FrankX default
- Host: `frankx-concierge`
- No private_vault

## Hard fails
- Card with `memory_scope: private_vault` on web → reject
- Missing soul file → reject
- Unknown tool not in server allowlist → reject

## Implementation note
GenCreator-Studio is currently on a dirty branch (`agent/hv-studio-workbench`). Implement chat shell on a clean worktree from main when admitting frontend lane.
