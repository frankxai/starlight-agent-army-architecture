# Starlight Character Studio templates

These templates turn character generation into a governed design process rather than a folder of attractive but disconnected images.

## Files

- `character-visual-contract.template.json` defines the agent's recognizable identity, role-shaped morphology, operational personality, mutable elements, prohibited cues, provenance, and human approval state.
- `image-job.template.json` records one controlled design hypothesis in the prompt structure used by the OpenAI `imagegen` workflow.
- `selection-receipt.template.json` compares at least two inspected candidates without allowing an automated reviewer to silently approve a brand identity.
- `direction-brief.template.md` is the human-readable brief used before a generation batch.
- `quality-review.template.md` is the inspection record used after actual exports exist.

## Workflow

1. Copy the visual contract and bind it to one canonical `cards/portfolio/*.json` agent card.
2. Keep shared identity variables fixed and write three genuinely different role-morphology hypotheses.
3. Create one image job per hypothesis. Use an owned reference as an edit target when identity continuity matters.
4. Generate one asset per call, copy the output into the repository, and record provider, lane/model, SHA-256, dimensions, and prompt.
5. Inspect the real exports. Score each candidate against the 30-point premium visual gate.
6. Mark scores of 26–30 as eligible for human review, 22–25 as iterate, and below 22 as restart.
7. Record the comparison in a selection receipt. Only a human decision can set `selected` or approve an identity contract.
8. Derive site crops, icons, motion source, and marketplace media only after the identity master is approved.

The character contract is descriptive. It deliberately grants no tools, permissions, memory, runtime admission, or execution authority.

## Validation

From the repository root:

```powershell
python scripts/validate_character_studio.py
python scripts/test_character_studio.py
```

The first command checks schemas, canonical-card linkage, safe paths, owned references, artifact receipts, and controlled comparison variables. The second command proves the most important failure cases remain closed.
