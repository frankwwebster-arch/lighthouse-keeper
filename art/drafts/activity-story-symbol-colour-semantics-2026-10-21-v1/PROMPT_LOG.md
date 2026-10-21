# Bubble stories symbol colour semantics V1 prompt log

**Tool:** built-in image generation, 21 October 2026. Each mark was generated
in its own call. Exact cache filenames and concise primary requests are pinned
in `batch-register.json`.

All four calls used this shared production contract:

> Use case: stylized-concept
>
> Asset type: isolated 2D game activity-callout mark for Lighthouse Keeper
>
> Scene/backdrop: genuinely transparent background; every pixel outside the
> mark fully transparent.
>
> Style/medium: highly polished hand-painted cosy maritime game illustration;
> smooth anti-aliased contours; substantial dark-navy outline; tactile but
> clean; consistent with Lighthouse Keeper activity-callout tokens.
>
> Composition/framing: centred compact mark, complete and readable at
> thumbnail size, generous transparent margin on all four sides, designed to
> fit a 256 × 256 cell.
>
> Constraints: one unambiguous owned effect; no object, person, floor, cast
> shadow, halo, text, logo, watermark, frame or background.

Per-mark requests and exclusions:

- `symbol-heat-shimmer`: three broad horizontal distortion ripples. Hot
  coral-red/vermilion outer bands, deep-orange inner bands and warm-cream
  centres. No flames, vertical aroma curls, stars or sun.
- `symbol-pleasant-aroma`: three slender warm-cream and blush-pink fragrance
  curls carrying two small five-petal flowers and one clean sparkle—classic
  comic shorthand for “this smells lovely”. No teal/red paired ribbons,
  question-mark dots, closed hooks, green sludge, flies, skull, smoke cloud,
  flame, food or perfume bottle.
- `symbol-welding-sparks`: a tiny blue-white arc core, short jagged electric
  arc and one-sided cyan/ice-blue/cobalt needle-spark spray, with only two or
  three molten coral-orange droplets near contact. No large star, symmetry,
  gold-dominant impact burst, tool, welder, metal object or smoke.
- `symbol-cold-snowflake`: one friendly six-armed frost crystal with pale
  ice-blue arms, cyan facets, white centre and storm-blue shadow facets. No
  gold, heat ripple, loose snow, cloud, weather scene or thermometer.

The first aroma candidate used a sea-teal wisp and a coral wisp. Frank
correctly found that two coloured ribbons did not communicate “pleasant
smell”. It is retained under `rejected/` with its cache name and SHA-256 in
the register; it was never added to the picture library. The accepted retry
uses the comic fragrance/flower/sparkle vocabulary above.
