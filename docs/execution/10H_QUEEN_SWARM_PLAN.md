# 10-Hour Queen Swarm Plan — Agent Portfolio ADLC Execution

> Started: 2026-08-09T02:05Z · Machine: Yogabook (Starlight/83KJ) · Disk OPEN  
> SSOT repo: `starlight-agent-army-architecture` · Branch: `agent/hermes/agent-portfolio-adlc-20260809`

## Objective (done-when)

1. Portfolio + ADLC + Agent Card schema landed and validated  
2. Three host cards minted: Gen-Ω, FrankX Concierge, Starlight Operator  
3. Gen-Ω specialist stubs (5) + KB pack skeletons  
4. Claude adversarial review receipt integrated  
5. Codex + Grok lanes produce score≥1 artifacts (code/schema/eval harness)  
6. Queen receipt + draft PR path + next 10h continuation card  

**Not in scope this 10h:** production deploy, public Arcanea L3 ship, billing, native apps, C940 forge, private vault exposure.

## Topology (10h)

| Window | Focus |
|--------|--------|
| 0:00–0:30 | Admit lanes, write SSOT, start Claude review |
| 0:30–2:30 | Cards + KB + validate script; Claude findings merge |
| 2:30–5:00 | Codex: schema validator + eval harness; Grok: voice/face critique + experiment designs |
| 5:00–7:00 | Adapter stubs (Hermes profile notes + web load contract); AutoResearch exp-001 |
| 7:00–9:00 | Repair, independent verify, draft PR prep |
| 9:00–10:00 | Closure only: receipts, scores, next driver, swarm bus |

## Lanes (artifact-defined)

| ID | Writer | Repo | Artifact | Score target | **Write paths only** |
|----|--------|------|----------|--------------|----------------------|
| L-SSOT | Hermes Queen | army-architecture | Portfolio, ADLC, cards, schema | 2 | `docs/`, `cards/`, `kb-packs/`, `schemas/`, `README.md` |
| L-REVIEW | Claude Code | army-architecture | `receipts/claude-strategy-review-*.md` | 1 | `receipts/claude-*` only |
| L-CODEX | Codex GPT-5.x | army-architecture | validators + evals + CI | 2 | `scripts/`, `evals/`, `.github/workflows/` |
| L-GROK | Grok 4.5 | army-architecture | Voice/cultural review + experiment specs | 1 | `receipts/grok-*`, `experiments/` |
| L-CONSUME | Hermes (later) | GenCreator-Studio (clean path) | Web load contract / shell | 1–2 | other repo only when clean worktree |

**Hard boundary:** one path owner per window. No two lanes edit the same file.

## Provider routing

| Role | Provider |
|------|----------|
| Judgment / adversarial | Claude Code (Sonnet/Opus available) |
| Implement loops | Codex (`codex exec`, workspace-write) |
| Cultural/voice/adversarial creative | Grok CLI |
| Orchestration / synthesis / git | Hermes Queen |
| C940 | Enqueue only if backend/GitOps needed; Book executes local |

## Checkpoints

- **15m:** branch exists, schema file, portfolio MD  
- **45m:** ≥1 host card complete  
- **90m:** validate script or equivalent; Claude receipt  
- **180m:** 3 hosts + 5 specialists draft; no lockfile noise  
- **Closure:** PR-ready commit set + `receipts/10h-*.md`

## Autoresearch experiments (this window)

| Exp | Hypothesis |
|-----|------------|
| exp-001 | Host-only system prompt vs host+specialist chip labels improves task routing accuracy on 10 golden studio tasks |
| exp-002 | Shorter boundary lists (≤7) reduce false refusals without raising safety fails |

## Stop rules

- Disk drops to TIGHT: freeze new worktrees/media  
- Any private vault path in a public card → hard fail  
- GenCreator-Studio dirty branch: **doc-only** consume until clean worktree  
- No production push without Frank gate  

## Continuation

After 10h: open `docs/execution/NEXT_10H.md` with residual backlog and exact first command for the next Queen run.
