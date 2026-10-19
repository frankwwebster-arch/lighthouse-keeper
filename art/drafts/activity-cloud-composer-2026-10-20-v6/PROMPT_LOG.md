# Activity Cloud Composer V6 prompt log

Generation date: 20 October 2026

Generator: built-in `image_gen` tool (default Image Generation skill path)

The supplied bathroom image was used only as directional style and subject reference. V5 and the supplied image were not edited. The accepted project-bound source files and SHA-256 values are:

- `source/bathroom-flush-handle-source.png` — `e567612b7dcc27d7b9f260b28ec8fbec7285cbf2d9077ad8dfce85e5c69ae02f`
- `source/bathroom-loo-brush-source.png` — `16361b0098d99312e173137e395c19b8c294dda70bccd0699178060e0683c43b`
- `source/bathroom-bad-smell-source.png` — `eb4b75939e000388ab7ee9338c7d4252b263e9b4f11a71da44f8709b6ba3f540`

## Accepted flush-handle prompt

```text
Use case: stylized-concept
Asset type: isolated game activity-callout token
Primary request: Create one standalone vintage toilet cistern flush handle, recognisable without a toilet: a short aged-brass lever with rounded ivory grip and circular brass escutcheon plate.
Input images: Image 1 is directional reference only for the polished illustrated game language and bathroom hardware; do not copy its layout.
Scene/backdrop: genuinely transparent background.
Style/medium: highly polished hand-painted 2D game illustration, smooth anti-aliased contours, strong dark navy outer line, warm cream highlights, aged copper/brass accents, matching the Lighthouse Keeper game's established callout tokens.
Composition/framing: exactly one object, centered, generous transparent margin on all four sides, compact near-square silhouette.
Constraints: preserve actual alpha transparency; no toilet, no cistern, no wall, no additional objects, no text, no logo, no watermark, no frame, no glow or cast shadow extending into the margin.
```

## Accepted loo-brush prompt

```text
Use case: stylized-concept
Asset type: isolated game activity-callout token
Primary request: Create one standalone traditional loo brush and holder: a cream ceramic cylindrical holder with a dark navy rim and an aged-brass handled brush visibly emerging at a slight angle, immediately readable as a toilet brush.
Input images: Image 1 is directional reference only for the polished illustrated game language and bathroom palette; do not copy its layout.
Scene/backdrop: genuinely transparent background.
Style/medium: highly polished hand-painted 2D game illustration, smooth anti-aliased contours, strong dark navy outer line, warm cream, sea-glass blue and aged copper/brass accents, matching the Lighthouse Keeper game's established callout tokens.
Composition/framing: exactly one combined brush-and-holder object, centered, generous transparent margin on all four sides, compact upright silhouette.
Constraints: preserve actual alpha transparency; no toilet, no bathroom room, no cleaning products, no text, no logo, no watermark, no frame, no glow or cast shadow extending into the margin.
```

## Accepted bad-smell prompt

```text
Use case: stylized-concept
Asset type: isolated comic game activity-callout token
Primary request: Create a discreet family-safe bad-smell symbol consisting of exactly three separate thin curling wavy odour strokes and three tiny round motes.
Input images: Image 1 is directional reference only for the polished Lighthouse Keeper game language.
Scene/backdrop: fully transparent everywhere outside the drawn strokes and motes.
Style/medium: clean flat hand-painted 2D sprite token, dark navy outlines, muted olive and warm ochre interiors, minimal highlights.
Composition/framing: a compact upward-flowing group, centered, very generous transparent margin on all four sides.
Constraints: hard isolated cutout only; every pixel around and between the strokes must be transparent; absolutely no aura, haze, smoke cloud, glow, vignette, background colour, shadow, toilet, person, flies, text, logo, watermark, or frame.
```

The first bad-smell generation and one targeted halo-removal edit were rejected because they retained an unnecessary surrounding haze. Their bytes remain only in the generated-image store and are not referenced by V6.

The builder deterministically fits each accepted source into one 256×256 transparent cell, leaving a measured 20-pixel minimum gutter. It does not paint, redraw or merge the source imagery.
