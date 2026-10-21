# Bubble stories symbol redraws V1 prompt log

Generation date: 21 October 2026

Generator: built-in `image_gen` tool (default Image Generation skill path)

Reference roles:

- `art/drafts/keeper-prime-rear-action-choreography-2026-10-20-v2/claude-code-model-test-pack/assets/source/activity-comic-symbols-source-sheet.png` was supplied as the accepted Lighthouse Keeper comic-symbol style reference only.
- Each existing rejected V1 mark was supplied only as subject/rejection context for its redraw. No old pixels were edited or copied.

Accepted source files:

- `source/symbol-heat-shimmer-source.png` — `47295475be43bbd16a9ce6b9d3b5ec046d4ecf7643b88bbb1821de6f276bcbe4`
- `source/symbol-pleasant-aroma-source.png` — `79b0156641a3e4303f39a5ee02dfb7787328d7cb23f76de4fd69593a6f0f5cfd`
- `source/symbol-welding-sparks-source.png` — `712a74a84ed34c2472656d9168412c3547fe209113ff5c9d7a1f02074c1a9240`
- `source/symbol-clean-glint-source.png` — `650edb67d1b9d1d70d6f11c576fa330b0423ba62bb752b5682d72324877e0639`

Rejected generated attempts: 0.

## Heat shimmer

```text
Use case: stylized-concept
Asset type: isolated game activity-callout mark
Input images: Image 1 is the accepted Lighthouse Keeper comic-symbol style reference. Image 2 is the rejected prior heat-shimmer concept and is subject reference only; do not preserve its flame silhouette.
Primary request: Draw exactly one heat-shimmer mark made from three separate broad horizontal rippling lines above an implied hot surface. The lines should undulate gently sideways like refracted hot air, clearly reading as heat distortion rather than flames, steam, or vertical heat curls.
Scene/backdrop: genuinely transparent background.
Style/medium: clean flat hand-painted mark matching the accepted Lighthouse Keeper activity-callout symbols; substantial smooth dark-navy outer contours, warm cream centres with restrained aged-brass and a small sea-glass teal accent; hard transparent cutout.
Composition/framing: compact centred mark, horizontally wider than tall, with three stacked irregular wave lines and generous transparent margin on every side; instantly readable at 64 px.
Constraints: exactly one semantic heat-shimmer mark; preserve actual alpha transparency; no hot surface, object, Keeper, room, floor, panel, text, logo, watermark, cast shadow, aura, haze, glow, flame tips, closed loops, detached specks, or extra decoration.
```

## Pleasant aroma

```text
Use case: stylized-concept
Asset type: isolated game activity-callout mark
Input images: Image 1 is the accepted Lighthouse Keeper comic-symbol style reference. Image 2 is the rejected prior pleasant-aroma concept and is subject reference only; do not preserve its question-mark hooks.
Primary request: Draw exactly one pleasant-aroma mark consisting of two separate open S-shaped wisps rising gently. Each wisp must be an unmistakable open flowing S stroke with both ends visibly open, never curling inward into a hook or closed spiral. It should read as a lovely food aroma, not steam or punctuation.
Scene/backdrop: genuinely transparent background.
Style/medium: clean flat hand-painted mark matching the accepted Lighthouse Keeper activity-callout symbols; substantial smooth dark-navy outer contours, warm cream centres, restrained aged-brass edges, only a tiny sea-glass teal accent; hard transparent cutout.
Composition/framing: compact centred pair of asymmetrical open S wisps, one slightly taller than the other, generous transparent margin on every side, readable at 64 px.
Constraints: exactly one semantic aroma mark made of two open strokes; preserve actual alpha transparency; no food, vessel, Keeper, room, floor, panel, text, logo, watermark, dots, question marks, closed hooks, spirals, cast shadow, aura, haze, glow, detached specks, or extra decoration.
```

## Welding sparks

```text
Use case: stylized-concept
Asset type: isolated game activity-callout mark
Input images: Image 1 is the accepted Lighthouse Keeper comic-symbol style reference. Image 2 is the rejected prior welding-sparks concept and is subject reference only; replace its symmetric firework burst.
Primary request: Draw exactly one welding-sparks mark: a compact hot-white star-like contact core at the lower left, with a clearly directional one-sided fan of six to eight long sparks spraying up and to the right from that single contact point. Mix two or three long tapered streaks with a few small hot fragments. It must read as metal welding, not a general impact star or cooking sizzle.
Scene/backdrop: genuinely transparent background.
Style/medium: clean flat hand-painted mark matching the accepted Lighthouse Keeper activity-callout symbols; substantial smooth dark-navy contours, hot-white and warm-cream core, aged-brass and restrained coral-orange sparks, one tiny sea-glass teal accent; hard transparent cutout.
Composition/framing: compact asymmetric diagonal spray from lower-left to upper-right, generous transparent margin on every side, readable at 64 px.
Constraints: exactly one semantic welding-spark mark from one contact point; preserve actual alpha transparency; no welder, tool, metal, Keeper, room, floor, panel, text, logo, watermark, symmetric radial burst, second contact point, cast shadow, aura, haze, glow, smoke, flame, or unrelated decoration.
```

## Clean glint

```text
Use case: stylized-concept
Asset type: isolated game activity-callout mark
Input images: Image 1 is the accepted Lighthouse Keeper comic-symbol style reference and is directional style reference only.
Primary request: Draw exactly one small clean glint: a crisp slender four-point diamond sparkle with a hot-white centre, long vertical point, medium horizontal points, and one subtle curved shine facet. It should instantly say “freshly clean and finished” when placed on cutlery or a washed object, distinct from an impact burst or sizzle spark.
Scene/backdrop: genuinely transparent background.
Style/medium: clean flat hand-painted mark matching the accepted Lighthouse Keeper activity-callout symbols; substantial but elegant smooth dark-navy outer contour, warm cream centre, restrained aged-brass edge and a small sea-glass teal highlight; hard transparent cutout.
Composition/framing: one compact centred asymmetric four-point glint, generous transparent margin on every side, readable at 48–64 px.
Constraints: exactly one semantic clean-glint mark; preserve actual alpha transparency; no object, cutlery, bubbles, Keeper, room, floor, panel, text, logo, watermark, multiple stars, symmetric many-point impact burst, motion lines, cast shadow, aura, haze, glow, detached specks, or extra decoration.
```

The deterministic builder measures visible alpha greater than 8, crops each
source to that measured owner, scales uniformly into a 216 × 216 maximum area,
and centres it using integer coordinates in a fresh 256 × 256 RGBA cell. It
does not repaint, merge, or invent pixels.
