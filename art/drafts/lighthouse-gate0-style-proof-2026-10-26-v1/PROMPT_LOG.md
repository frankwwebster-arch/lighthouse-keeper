# Prompt and provenance log

Date: 26 October 2026  
Tool: built-in image generation  
Use case: `stylized-concept`

## Input references

All three inputs are approved identity references, not edit targets:

1. `sources/keeper-approved-side.png` — primary identity and side-neutral pose.
2. `sources/keeper-approved-front.png` — face, beard, costume and front identity.
3. `sources/keeper-approved-back.png` — cap, hair, jumper and rear identity.

Their exact SHA-256 values are recorded in `manifest.json`.

## Candidate A Keeper prompt

```text
Use case: stylized-concept
Asset type: transparent Keeper candidate for Lighthouse Keeper style proof A
Primary request: Redraw the exact approved Lighthouse Keeper as a full-body neutral side-right standing candidate in high-resolution pixel illustration.
Input images: Image 1 is the primary approved side-neutral identity and pose reference. Images 2 and 3 confirm the approved face, beard, costume and proportions. Preserve identity exactly.
Subject: navy peaked cap with small gold badge; full white beard and moustache; pink nose; bright blue knitted jumper with exactly two separate white horizontal chest stripes and one white stripe around each sleeve; ribbed blue cuffs and hem; plain navy trousers; chunky navy boots; stocky body about three heads tall. Same neutral side-right pose as Image 1, feet level.
Style/medium: high-resolution pixel illustration, crisp deliberate pixel clusters, hard alpha edges, deep-navy outline, flat colours with one shadow tone and one restrained highlight, no anti-aliasing, no gradients, no dithering, no stray pixel noise.
Composition/framing: one complete character only, centred in a portrait canvas with generous transparent margin on every side; full cap and boots visible.
Scene/backdrop: genuinely transparent background.
Constraints: candidate only; no floor, shadow, prop, text, logo, watermark, sailor collar, scarf, coat, apron, glasses, extra stripes, missing stripe, weapon, changed hat, changed face, changed beard or changed body build.
```

## Candidate B Keeper prompt

```text
Use case: stylized-concept
Asset type: transparent Keeper candidate for Lighthouse Keeper style proof B
Primary request: Redraw the exact approved Lighthouse Keeper as a full-body neutral side-right standing candidate in the current smooth flat-colour illustration style.
Input images: Image 1 is the primary approved side-neutral identity and pose reference. Images 2 and 3 confirm the approved face, beard, costume and proportions. Preserve identity exactly.
Subject: navy peaked cap with small gold badge; full white beard and moustache; pink nose; bright blue knitted jumper with exactly two separate white horizontal chest stripes and one white stripe around each sleeve; ribbed blue cuffs and hem; plain navy trousers; chunky navy boots; stocky body about three heads tall. Same neutral side-right pose as Image 1, feet level.
Style/medium: bright clean smooth 2D flat-colour game illustration; crisp anti-aliased deep-navy outlines; flat fills with exactly one simple shadow tone per material; no gradients, glossy highlights, airbrushed shading, painterly texture or pixel-art blocks.
Composition/framing: one complete character only, centred in a portrait canvas with generous transparent margin on every side; full cap and boots visible.
Scene/backdrop: genuinely transparent background.
Constraints: candidate only; no floor, shadow, prop, text, logo, watermark, sailor collar, scarf, coat, apron, glasses, extra stripes, missing stripe, weapon, changed hat, changed face, changed beard or changed body build.
```

## Rejected full-room generations

The first pass also generated one full room per style. Both are retained as
`room-source-a-rejected.png` and `room-source-b-rejected.png`. They were
rejected because the model introduced perspective floor surfaces and failed to
produce byte-exact magenta panes. Their prompts used the same identity inputs,
empty-room inventory and A/B rendering constraints as the accepted Keeper
prompts.

## Deterministic construction

`build_review.py` places the two accepted transparent Keeper candidates into
the same exact room geometry. Candidate A is reduced to the 768 × 256
authoring grid, palette-snapped, hard-alpha normalised and delivered at exact
2×. Candidate B is palette-snapped while retaining smooth alpha edges and is
composited at native 1536 × 512. Exact-magenta panes are written after smooth
rasterisation so no near-magenta edge pixels exist.

