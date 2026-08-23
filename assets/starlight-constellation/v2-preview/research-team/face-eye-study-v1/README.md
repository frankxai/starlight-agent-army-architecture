# Starlight Face + Eye Study v1

This is a controlled visual research study, not a production identity release.

The existing twin-cyan-lens face is the continuity control. It is recognizable and clearly mechanical, but it is not assumed to be optimal. The study tests ten broader face architectures, selects the most promising structural base, tests ten eye systems while holding that base constant, and then compares ten illustration and material languages while holding the selected character geometry constant.

## Audience

The primary human audience is the audience already named by the Starlight `.ai` product specification: founders, product leads, developers, researchers, and operators designing governed multi-agent systems. The target response is **warm competence**—approachable enough to invite collaboration, precise enough to carry enterprise trust, and clearly non-human enough to avoid deceptive anthropomorphism.

Machine agents do not experience aesthetic appeal. The machine-facing evaluation is therefore called **agent legibility**: stable visual identity, discriminable geometry, crop resilience, deterministic metadata mapping, and the ability to connect a portrait to an agent card without treating the portrait as authority.

## Research-informed constraints

- A 2024 controlled study of 211 participants found higher reported trustworthiness for round versus narrow robot eyes, but that does not prove round eyes are best for every task or audience: <https://pmc.ncbi.nlm.nih.gov/articles/PMC11244564/>.
- A 2023 eye-tracking study found that abstract anthropomorphic robot eyes could direct attention efficiently and increased perceived competence: <https://www.frontiersin.org/articles/10.3389/frobt.2023.1178433/full>.
- A controlled cobot study found that adding eyes produced at most marginal subjective trust gains and did not improve performance, warning against treating eyes as a universal solution: <https://pmc.ncbi.nlm.nih.gov/articles/PMC10382291/>.
- A study spanning 80 real robot faces found robust uncanny-valley effects on likability and, in some conditions, trust-related behavior: <https://doi.org/10.1016/j.cognition.2015.09.008>.
- Research on human-robot cooperation indicates gaze is most useful when it communicates joint attention and intended action. Static direct staring is not the design goal: <https://www.frontiersin.org/articles/10.3389/fnbot.2012.00003/full>.

These findings bound the experiment; they do not substitute for testing with the actual Starlight audience.

## Controlled variables

Across Phase A:

- Lyra's research-conductor identity and adult human scale
- dark porcelain, obsidian mechanics, restrained ink-blue accents
- near-solid charcoal studio backdrop and soft editorial light
- head-and-upper-torso portrait, eye-level camera, calm neutral posture
- cyan reserved for machine activity; one separate amber environmental witness light
- no human skin, wet human eyeballs, lips, smile simulation, crown, halo, weapon, text, logo, or generated UI

Across Phase B, the selected Phase A face, pose, crop, light, materials, mouth treatment, and collar are locked. Only the optical system changes.

Across Phase C, the Civic Instrument shell with soft-square optics is the identity reference. Head silhouette, panel structure, optics, adult proportions, role, and calm posture remain fixed; medium, mark-making, palette, light, and presentation language change. This phase deliberately tests civic editorial, technical, printmaking, academy, narrative, and tactile approaches rather than ten color-swapped science-fiction renders.

## Evaluation model

### Predicted human appeal — 30 points

Score each 0–5 for warmth, competence, appropriately calibrated trust, brand ownability, low uncanny/surveillance risk, and fit for a calm research conductor.

### Agent legibility — 15 points

Score each 0–5 for identity stability at small crop, geometry distinctiveness from other agents, and clean mapping to deterministic metadata/alt text.

### Production viability — 15 points

Score each 0–5 for consistency across future renders, feasible gaze/state animation, and scalability across fifty agents without becoming repetitive.

Maker-authored scores are hypotheses, not audience evidence and never constitute approval. Real validation requires a randomized five-second role/trait study with the intended audience, followed by pairwise preference and adoption-intent questions.

## Files

- `study-plan.v1.json` — hypotheses, controlled prompt, and output plan.
- `phase-a-face-architecture/` — ten face architecture exports.
- `phase-b-eye-systems/` — ten eye-system exports.
- `style-study.v1.json` — Phase C outcome contract, hypotheses, controlled prompt, and exact style deltas.
- `phase-c-style-languages/` — ten style-language exports and comparison crops.
- `design-loop-evidence.json` — premium-asset provenance, inspection, scoring, and decision trace.
- `evaluation.v1.json` — export facts, heuristic scoring, ranking, and decision once generation finishes.
- `phase-*-contact-sheet.png` and `phase-*-avatar-96-sheet.png` — normalized visual comparison boards and small-crop checks.

No candidate replaces the existing Starlight character identity until independent critique, Frank's decision, a true production crop, and site-context QA pass.
