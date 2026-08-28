# Phase D — morphology silhouettes

**Status:** bounded generation resumed after machine-performance allow
**Production eligible:** no  
**Founder reviewed:** no

Phase D corrects the failed Phase C experiment by varying robot morphology before eyes, color, materials, cinematic rendering, or surface illustration style.

## Completed

- `m02-compact-field-specialist-board-v1.png` — four compact, short-legged adult-machine chassis; inspected at 1536 × 1024.
- `m03-chibi-academy-guide-board-v1.png` — four Academy-role concepts in improved two-tone maquette quality; inspected at 1536 × 1024.
- `m07-biotech-symbiote-board-v1.png` — four non-humanoid clean-biotech concepts; inspected at 1536 × 1024.

The first board is promising as a morphology study because the four candidates differ in torso architecture, tool storage, silhouette, and stance. It is still a draft. The generator introduced more component detail than the requested silhouette-only gate, so the next iteration should flatten internal seams and compare the four bodies at 96 pixels before selecting one.

## Generated set

The generation manifest now records fourteen independently generated form families—ten core directions plus four extended directions—for a total of at least 56 morphology candidates:

1. full specialist;
2. compact field specialist;
3. chibi Academy guide;
4. micro avatar;
5. guardian operator;
6. agile scout;
7. biotech symbiote;
8. swarm gestalt;
9. non-humanoid instrument;
10. creature companion;
11. soft-shell care collaborator;
12. modular transforming fabricator;
13. aerial knowledge navigator;
14. architectural room-scale intelligence.

Every board was generated separately and has its own exact prompt receipt, source path, byte count, dimensions, SHA-256 digest, and maker inspection. The set deliberately does not select a universal body. M04, M05, M07, M09, and M14 are the strongest current family-level proofs; M08 is a documented restart because it reintroduced a central-node cliché. No individual form is production-approved.

The independent quality gate is recorded in `INDEPENDENT_CRITIQUE.md`. The machine-readable
keep/iterate/restart map is `morphology-selection.v1.json`. Future production generations must use
`../STARLIGHT_CHARACTER_GENERATION_TEMPLATE.md`.

## Selection gate

The next step is not 144 polished portraits. It is a comparative founder and independent-critic review of all fourteen boards, followed by 96-pixel legibility and real-surface tests. Select a small morphology grammar for each context, then produce turnarounds and face/state studies only for those finalists.

## Pause receipt

On 2026-08-24, both `pp preflight --workload browser-qa` and `pp preflight --workload review-lite` returned `HOLD`. The latter reported approximately 4.3 GB free RAM against a 6 GB reserve and 17 active Codex task runtimes against a budget of 12. The image loop stopped after the current atomic generation; no browser, server, local model, parallel agent, or additional image job was started.

On 2026-08-28 `pp preflight --workload swarm` returned `ALLOW` with a two-process ceiling. Frank explicitly authorized the broader comparison. Generation resumed single-threaded, beginning with M03 and M07 because they create the largest useful contrast with M02. All outputs remain unapproved drafts.
