# Starlight character generation template

Use this template only after the stable Agent Card/profile exists. Character imagery explains an
identity; it does not create identity or grant authority.

## 1. Structured intake

```yaml
agent_id: <stable kebab-case id>
display_name: <public name>
surface: <.ai profile | .org story | Academy | graph | marketplace | spatial>
representation_level: <canonical | companion | avatar | state-glyph | spatial>
specialty_verb: <what the agent does>
primary_artifact: <what changes or gets produced>
exclusive_instrument: <one function-shaped object>
working_behaviors:
  - <observable temperament behavior>
  - <observable temperament behavior>
authority_boundary: <what remains human-held>
morphology_family: <M01-M14 or approved descendant>
candidate_seed: <board and candidate number>
eye_semantic: <joint-attention | routing | vigilance | adaptive-sensing | evidence-only | deep-analysis>
render_lane: <cinematic-3d | product-editorial | gouache | line-wash | cel-interactive | stop-motion | paper-relief | glass-editorial>
identity_invariants:
  silhouette: <dominant and supporting shape>
  proportions: <adult compact, chibi, room-scale, etc.>
  locomotion_or_support: <mechanically credible system>
  face_architecture: <none until silhouette gate passes>
  material: <approved family material>
  accent: <semantic, never decorative>
target_crop: <1:1 | 4:5 | 16:9 | 9:16>
resolution_master: <2048px minimum edge for production character art>
prompt_receipt_path: <repo-relative .prompt.txt written before generation>
```

## 2. Prompt skeleton

```text
Use case: stylized-concept.
Asset role: [profile illustration / Academy guide / micro identity / role instrument / spatial agent].

Create an original Starlight Intelligence [MORPHOLOGY FAMILY] for [AGENT DISPLAY NAME], stable id
[AGENT ID]. Its specialty must be understood before color or facial expression: it [SPECIALTY VERB]
and produces [PRIMARY ARTIFACT] using one exclusive [INSTRUMENT]. Show [WORKING BEHAVIOR 1] and
[WORKING BEHAVIOR 2] through posture, handling, spatial arrangement, or task state.

Lock these invariants: [SILHOUETTE], [PROPORTIONS], [LOCOMOTION OR SUPPORT], [MATERIAL], and
[IDENTITY SIGNATURE]. Preserve the selected seed [BOARD/CANDIDATE] while solving its documented
mechanical and visual risks. Make load paths, hinges, balance, storage, hands, and contact points
credible for the stated task. Adult specialist forms must read as competent rather than toy-like.
Academy chibi forms may be warm and short-legged but must remain capable and never infant-coded.

Authority boundary: [AUTHORITY BOUNDARY]. Visualize this as a separate amber human-held gate or
external interaction point; do not depict autonomous approval, command, enforcement, diagnosis,
spend, publication, or deployment.

Composition: [CROP AND CAMERA], one dominant subject, quiet warm-neutral field, generous negative
space, exact subject separation, no cropping of essential silhouette or instrument. Generated media
contains no semantic text; leave intentional blank rails where exact HTML or code overlays will sit.

Negative constraints: no copied franchise or studio character, no direct Pixar imitation, no Astro
Bot, WALL-E, Baymax, Star Wars droid, superhero, anime, military armor, weapon, police coding,
surveillance-camera face, giant generic mono-eye, halo, cape, magical levitation, glowing circuitry,
purple-blue SaaS gradient, decorative node web, fake UI, pseudo-text, signature, watermark, or logo.
Do not make eye size, body size, cuteness, material, or color imply authority or intelligence.
```

## 3. Required generation sequence

1. Silhouette: four flat-black candidates, 96-pixel proof included.
2. Mechanics: front/side/three-quarter views plus one task interaction; no face polish.
3. Face and eye architecture: ten controlled variants on the approved body only.
4. Material and palette: two or three restrained variants using semantic color roles.
5. Expression and behavior: task states, not exaggerated emotion sheets.
6. Surface master: exact crop and context for one named route.
7. Derivatives: crop from the approved master; never regenerate identity independently per size.

Founder approval is required between steps 1, 3, and 6.

## 4. Quality gate

Reject or restart when any answer is no:

- Does the silhouette remain identifiable at 96 pixels without color?
- Can a viewer infer the specialty and artifact before reading the name?
- Is the form mechanically coherent and safe for its stated environment?
- Does it avoid close resemblance to an existing franchise, consumer robot, drone, or medical device?
- Is temperament expressed through work behavior rather than stereotypes?
- Is human authority visible and separate from the character?
- Are all labels and essential state exact HTML/code rather than generated pixels?
- Are original prompt, source output, dimensions, bytes, hash, rights, and transformations recorded?
- Has the original export and every intended crop been inspected?
- Does the 30-point score reach 26/30 on the actual target surface?

Every production asset receives a provenance sidecar and an entry in `design-loop-evidence.json`.

## 5. Atomic prompt and receipt protocol

Prompt provenance is part of the asset, not optional documentation added later.

1. Create the image-job JSON in `queued` state and save the exact final prompt as a sibling `.prompt.txt` before calling an image model.
2. Record the provider, available model or lane identifier, references, rights status, target surface, intended crop, and creation timestamp in the queued job.
3. Generate one controlled candidate per call. Do not combine morphology, eye, material, and rendering experiments in one untraceable batch.
4. Copy—not move—the original result into the project-bound asset directory; preserve the provider output.
5. Record the original source path, repository path, SHA-256, dimensions, bytes, and inspection timestamp immediately after generation.
6. Create compressed derivatives only from the preserved master and record every transformation.
7. If the exact prompt or source receipt is missing, label the output `research_candidate` with `prompt_capture_status: unavailable_at_audit`. It cannot advance to production approval, regardless of visual score.

### Controlled comparison formula

```text
one stable agent contract
× one morphology hypothesis
× one eye/state hypothesis
× one rendering lane
× one named surface and crop
= one auditable candidate
```

Change one primary variable between comparison candidates. A visually exciting result is not informative when the experiment cannot explain what improved.
