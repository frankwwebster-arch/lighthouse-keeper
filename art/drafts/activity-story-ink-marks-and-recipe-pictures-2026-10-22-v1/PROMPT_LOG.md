# Prompt log — black-ink marks and recipe pictures V1

Source generation and correction completed on 22 October 2026 with the
built-in image-generation/editing tool. Production components were then
normalised deterministically: alpha-greater-than-8 crop, fit to a 216 px box,
nearest declared flat palette, integer centring in a transparent 256 × 256
RGBA cell, and lossless PNG output.

## Shared mark prompt

> Original European ligne-claire comic ink on genuine transparent alpha. One
> upright centred compact cue with generous margin, readable around 40 px. The
> mark is the ink stroke itself: one consistent bold hand-drawn near-black
> weight, targeting about 11 px in the 256 px cell. No outline-plus-fill unless
> the brief requires a pale interior; no gradient, shading, highlight, glow,
> blur, shadow, context, object, person, panel, text or watermark. A permitted
> single flat accent never replaces the structurally complete black ink.

Exact subject requests, in sheet order:

- `symbol-impact-star`: solid central star and seven short radiating strokes.
- `symbol-motion-ticks`: three short curved parallel whoosh strokes.
- `symbol-water-droplets`: one outlined teardrop with white interior.
- `symbol-soap-bubbles`: three outlined circles of different sizes.
- `symbol-heat-curls`: three vertical wavy strokes.
- `symbol-sizzle-spark`: five-stroke tiny burst.
- `symbol-clean-glint`: slim solid four-point cross-star.
- `symbol-dust-puff`: one five-lobed outlined pale-grey cloud.
- `symbol-earth-clods`: three outlined flat-brown clods.
- `symbol-sawdust`: six black flecks and curls.
- `symbol-seasoning-flecks`: seven black dots and flecks.
- `symbol-spray-mist`: a fan of about twelve fine black dots.
- `symbol-steam-puff`: one outlined white rising curl.
- `symbol-question-mark`: solid heavy hand-brushed question mark and dot.
- `symbol-exclamation-mark`: solid heavy hand-brushed exclamation and dot.
- `symbol-foul-odour`: three wavy rising black lines.
- `symbol-pleasant-aroma`: two smooth black curls and one tiny pink accent.
- `symbol-heat-shimmer`: three horizontal black waves and one red accent.
- `symbol-welding-sparks`: seven straight black sparks and one orange origin.
- `symbol-cold-snowflake`: simple six-arm black snowflake.
- `symbol-electrical-arc`: black zigzag bolt with flat yellow interior.
- `symbol-speed-lines`: three straight parallel horizontal strokes.
- `symbol-swirl`: one loose black swirl stroke.
- `symbol-spiral`: one tight black spiral.
- `symbol-zigzag`: one short four-segment black zigzag.
- `symbol-ink-star`: one small solid black five-point star.
- `symbol-accent-red-star`: black-outlined flat-red grawlix star.
- `symbol-accent-yellow-sun`: yellow disc and eight short black rays.
- `symbol-accent-blue-spiral`: blue spiral bounded by black ink on both sides.

## Shared object prompt

The washing plate, sandwich tomato and repair toolbox were supplied as
co-equal style references: living hand-drawn shape, flat-colour economy and
credible adult construction. Each request used:

> One isolated semantic object on genuine transparent alpha, centred with a
> generous clear margin and readable at 64 px. Original observational ligne
> claire, not cartoon: one even near-black outline on every real outer and
> inner edge; every closed area one flat opaque muted local colour; no heavy
> silhouette, gradient, shading, highlight, gloss, reflection band, hatching,
> stipple, painted texture, cast shadow, scene, text, logo, watermark, face,
> mascot, toy-like inflation or detached comic mark.

Exact subject requests:

- `dishwasher-machine`: built-in dishwasher, door folded down, empty lower rack half out.
- `laundry-washing-machine`: front-loader, closed porthole, dial and soap drawer.
- `laundry-basket-dirty`: wicker basket heaped with crumpled clothes.
- `wear-shirt-muddy`: crumpled adult work shirt with flat brown mud patches.
- `floor-muddy`: four-board low three-quarter floor patch with three boot prints.
- `floor-clean`: same floor, all mud removed and identity preserved.
- `furniture-side-table-dusty`: four-legged side table, flat grey dust top and three fluff balls.
- `furniture-side-table-clean`: same table, all dust and fluff removed and identity preserved.
- `garden-plant-pot`: terracotta pot full of dark soil, nothing growing.
- `fishing-sea-water`: small calm two-blue water band with three ripple lines.

## Corrections and rejected attempts

- The first laundry basket used dense tiny weave crossings and too many fabric
  wrinkles. The accepted edit keeps six broad horizontal bands, simple
  vertical ribs and only construction-defining garment folds.
- The first muddy floor was independently generated and did not match the
  clean partner closely enough. The accepted version edits the clean source,
  preserving its floor while adding exactly three simplified prints.
- The first dusty table used mottled dust, edge speckles and curled fluff
  interiors. The accepted version edits the clean source and uses one flat
  grey top field plus three plain closed fluff balls.

All source filenames, original generator cache names, fixed palettes, hashes,
self-test results and rejection reasons are pinned in `batch-register.json`.
