# Repository Instructions

This repo is part of the FrankX / Starlight / Arcanea agent estate.

## Classification

- Repo: starlight-agent-army-architecture
- Class: agent-substrate
- Default health command: `git status` (structural validation: `powershell -ExecutionPolicy Bypass -File scripts/validate-architecture.ps1`)
- Remote: https://github.com/frankxai/starlight-agent-army-architecture.git

## What This Repo Is

The Starlight implementation playbook for running local/cloud agent armies: Codex as repo control
plane, Hermes profiles as durable workers, OpenClaw as chat/mobile gateway, DeepAgents as
long-running harnesses, Claude Code as maintainer lane, SIS as memory/provenance. Docs live in
`docs/` (swarm-roles, control-plane-workflow, sis-memory-provenance, health-checks,
deployment-recipes), example configs in `configs/`, the validation script in
`scripts/validate-architecture.ps1`. For the neutral architecture layer, see
`agentic-architecture-field-guide`; for the ecosystem index, see `awesome-agent-operating-systems`.

## Agent Rules

- Read this file before making changes.
- Preserve existing user work and unrelated dirty files.
- Keep edits scoped to the requested task.
- Prefer existing repo conventions over new abstractions.
- Run the health command before handoff when feasible.
- Do not publish secrets, private memory, credentials, or internal-only strategy.

## Class-Specific Guidance

- Preserve skill/plugin/MCP schemas and frontmatter.
- Validate skills, manifests, scripts, and generated registries after edits.
- Keep public/private memory boundaries explicit.

## Handoff

Summarize changed files, validation run, risks, and any follow-up needed.

## Design Taste Kernel

For any site, app, landing page, dashboard, visual identity, brand, motion, media, social, or frontend task, apply the shared Design Taste Kernel before handoff:

- C:\Users\frank\starlight\repos\DESIGN_TASTE.md
- C:\Users\frank\starlight\repos\WEB_EXPERIENCE_STANDARD.md
- C:\Users\frank\starlight\repos\MOTION_TASTE_RUBRIC.md
- C:\Users\frank\starlight\repos\MULTI_AGENT_DESIGN_COUNCIL.md
- C:\Users\frank\starlight\repos\VISUAL_QA_GATE.md

When motion, scroll, generated media, GIF/video, or premium polish matters, route through the Motion Design Studio plugin/skills and verify the result visually.

