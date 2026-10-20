# Activity Cloud Composer V7 prompt log

Generation date: 20 October 2026

Generator: built-in `image_gen` tool (default Image Generation skill path)

Reference role: the existing six-symbol source sheet from Prime Rear Action Choreography V1 was supplied as style reference only. It was not edited, copied or promoted.

Accepted project-bound sources:

- `source/generic-action-symbols-sheet-source.png` — `e4afb957aeb8d1015a43fe2664135ef8830270b6ef70ab1941947aca552e390b`
- `source/generic-question-mark-source.png` — `327f29ac9c67fdf237892ac5f4abe52e4508e7107140b7fb1b265cb6b7a71ebb`

Rejected source retained for provenance:

- `rejected/generic-action-symbols-sheet-attempt-1-insufficient-gutter.png` — `69dd1a140f881e497c965ed7d6f3000478ad832304f978ef07b7e42519982530`

## Initial six-symbol source prompt

```text
Use case: stylized-concept
Asset type: transparent 3x2 source sheet for Lighthouse Keeper activity-callout comic symbols
Primary request: Create six compact separate action symbols in this exact reading order: (1) radiant heat shimmer — three rising wavy heat lines, distinct from smoke; (2) pleasant aroma — two graceful warm fragrant curls suggesting something delicious, no flower or food; (3) foul odour — two uneven sickly teal/olive stink curls with small broken accent dashes, readable as a bad smell but not gross; (4) electrical energy — one bold forked lightning arc with two tiny detached charge ticks; (5) welding sparks — one compact fan of sharp hot-metal sparks bursting from a single contact point, no welding tool; (6) exclamation mark — one chunky hand-painted exclamation mark, punctuation only.
Input image: supplied existing six-symbol Lighthouse Keeper source sheet is style reference only; do not copy its subjects or layout pixels.
Scene/backdrop: genuinely transparent background; no black field, panel, tile, floor, scenery, aura, haze, glow or cast shadow.
Style/medium: clean flat hand-painted comic marks matching the supplied Lighthouse Keeper symbols; chunky deep-navy outer contour, warm cream highlight, muted brass-gold, sea-teal, restrained coral and storm-blue palette; crisp compact silhouettes readable at thumbnail size.
Composition/framing: exact regular 3-column by 2-row grid on a 1536x1024 RGBA canvas. Each 512x512 cell owns exactly one complete symbol centred within its central 352x352 area. Keep at least 80 pixels of fully transparent margin on every side of every cell. The lanes and boundary lines at x=512, x=1024 and y=512 must be completely transparent.
Constraints: six cells exactly in requested order; actual alpha transparency; no words, letters, numbers, labels, logos, watermark, border, background, Keeper, person, object, duplicate mark, stray fragment or shared-cell overlap. The exclamation mark is the only permitted punctuation glyph. Each cell has exactly one owned symbol.
```

The initial source had clean alpha and zero shared-boundary pixels, but five cells measured only 41–77 pixels on at least one side. It was rejected rather than tightly cropped or silently accepted.

## Accepted six-symbol scale correction

```text
Edit target: the supplied transparent 1536x1024 six-symbol source sheet.
Primary request: Preserve the six symbols, their exact reading order, design, colours, transparency and 3x2 layout, but uniformly scale each complete symbol down around the centre of its own 512x512 cell so every visible or antialiased pixel lies inside that cell's central 320x320 area. This must leave at least 96 pixels of fully transparent gutter on all four sides of every cell.
Cell order must remain: heat shimmer, pleasant aroma, foul odour, electrical energy, welding sparks, exclamation mark.
Constraints: change only scale and centring. Keep a genuinely transparent background. Do not redraw, add, remove, relabel, duplicate, merge or move a symbol into another cell. No glow, haze, shadow, background, border, words, watermark or new fragments. Boundary lanes at x=512, x=1024 and y=512 must remain fully transparent.
```

The accepted sheet has zero visible pixels on all outer and shared ownership lines. Its six measured minimum source gutters are 99, 97, 93, 111, 115 and 111 pixels.

## Accepted question-mark prompt

```text
Use case: stylized-concept
Asset type: isolated Lighthouse Keeper activity-callout comic symbol
Primary request: Create exactly one chunky hand-painted question mark, punctuation only, immediately readable at thumbnail size. Use a curved storm-blue/sea-teal body, warm cream highlight and restrained brass-gold accent, all enclosed by the established substantial deep-navy contour. Include the question-mark dot as part of this single semantic symbol directly beneath the curve.
Input image: supplied existing Lighthouse Keeper symbol sheet is style reference only; do not copy its subjects.
Scene/backdrop: genuinely transparent background; no black field, panel, tile, scenery, aura, haze, glow or cast shadow.
Style/medium: clean flat hand-painted comic notation matching the supplied Lighthouse Keeper symbols; crisp compact silhouette, friendly but not emoji-like.
Composition/framing: exactly one owned illustration centred on a square RGBA canvas, with generous fully transparent margin on all four sides; keep the complete curve and dot well inside the canvas.
Constraints: actual alpha transparency; no other punctuation, words, letters, numbers, labels, logos, watermark, border, Keeper, person, object, duplicate, stray fragment or background.
```

The builder assigns source pixels geometrically, then fits each owner into a fresh 256×256 RGBA cell with at least 20 pixels of transparent output gutter. It never repaints or merges the sources.
