# Prime rear-action choreography V1 symbol prompt log

**Generation date:** 20 October 2026

**Tool:** built-in Codex image generation

**Use:** six isolated comic-symbol sources for a reversible review candidate only

## Reference roles

- No input image was supplied to the generator.
- `docs/ACTIVITY_CALLOUT_AUTHORING_STANDARD.md` is the binding style,
  transparency, ownership and normalisation authority.
- Activity Cloud Composer V6 is the inherited object vocabulary. None of its
  image bytes were used as an editable generation input.
- Prime Rear Action Sequence V1 is continuity authority only. No Keeper image
  was supplied to or changed by generation.

## Attempt 1 — rejected

```text
Use case: stylized-concept
Asset type: transparent 3x2 source sheet for comic activity-callout punctuation sprites
Primary request: Create six compact separate hand-painted comic symbols in exact reading order: (1) two rising heat curls, (2) a three-pronged sizzle spark, (3) three quick motion ticks, (4) a cluster of three water droplets, (5) a compact cluster of four soap bubbles, (6) a friendly eight-point impact star. These are punctuation marks, not objects or emoji.
Scene/backdrop: genuinely transparent background; no panel, tile, floor, scenery, aura, haze, glow or cast shadow.
Style/medium: clean flat hand-painted game marks matching polished cosy maritime Lighthouse Keeper iconography; substantial smooth dark-navy outer contour; warm cream highlights; aged brass-gold, sea-glass teal, storm blue and restrained coral accents; hard transparent cutout; compact readable silhouettes at thumbnail size.
Composition/framing: exact regular 3-column by 2-row grid in a 1536 by 1024 transparent image. Each cell is 512 by 512. Reserve a completely empty transparent margin of at least 80 pixels on every side of every cell. Keep each complete symbol inside the central 352 by 352 area of its own cell. Fully transparent lanes at x=512, x=1024 and y=512 must contain no mark, glow or antialiasing.
Constraints: six cells exactly in requested order; exactly one semantic symbol owner per cell; no words, letters, numbers, logos, watermark, border, labels, background, character, Keeper, household object, duplicate symbol, stray fragment, aura, haze or glow. Preserve true alpha transparency.
```

Rejected because the returned preview contained an opaque dark backdrop and
diffuse blue/black haze. It was not copied into the repository and was not
cropped or normalised.

## Attempt 2 — rejected transparency edit

```text
Edit the immediately preceding six-symbol 3x2 sheet. Preserve the six symbol designs, their exact reading order, proportions, and generous cell spacing, but remove the entire dark background, all blue/black haze, all glow, all aura, and all cast-shadow pixels. Output a true RGBA image with fully transparent background everywhere outside the six hard-edged symbol cutouts. The exact vertical shared lines x=512 and x=1024 and horizontal shared line y=512 must be fully transparent; keep each complete symbol within its own central 352x352 area. Do not add anything. No panel, vignette, backdrop, fog, halo, text, labels, borders, stray marks, or extra objects. The result must be suitable for deterministic alpha-cell extraction.
```

The output was true RGBA and had zero alpha-greater-than-8 pixels on every
outer/shared ownership line, but four cells measured only 44–71 pixels of
source gutter. The binding 80-pixel source-sheet margin was missed, so the
sheet was rejected before normalisation.

## Attempt 3 — accepted scale/clearance edit

```text
Edit the immediately preceding transparent six-symbol 3x2 sheet. Preserve the exact six designs, true transparency, reading order, colors, and hard cutout edges. Uniformly scale each complete symbol group down to 75 percent of its current size around the center of its own 512x512 cell. Keep each symbol centered in its original cell and entirely inside that cell's central 352x352 area, leaving at least 80 fully transparent pixels on all four sides of every cell. Keep x=512, x=1024, and y=512 fully transparent. Do not add or change any symbol, backdrop, haze, glow, shadow, panel, border, text, or stray mark. Output exact 1536x1024 RGBA with fully transparent background.
```

Accepted source:

- `source/activity-comic-symbols-source-sheet.png`
- SHA-256: `517309ab1ef8ba71849217d6da71fe1cd1c8b2b3a2ef94f86db7ee28fcc43b80`
- Geometry: 1536 × 1024 RGBA, regular 3 × 2 grid
- Measured per-cell alpha-greater-than-8 gutters: 94, 120, 104, 100, 107,
  and 85 pixels
- Outer/shared ownership-line alpha-greater-than-8 pixels: 0
- Rejected attempts before acceptance: 2

## Deterministic normalisation

The builder assigns each 512 × 512 source cell geometrically to its declared
symbol owner, finds its alpha-greater-than-8 bounds, rejects source gutters
below 80 pixels, scales uniformly into a maximum 216 × 216 content area in a
fresh 256 × 256 RGBA cell, centres with integer coordinates, and requires a
measured output gutter of at least 20 pixels. It does not repaint, fill, erase,
reassign disconnected marks, or crop across ownership boundaries.
