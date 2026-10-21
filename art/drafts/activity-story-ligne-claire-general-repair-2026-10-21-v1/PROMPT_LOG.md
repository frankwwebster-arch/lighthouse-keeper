# Prompt log

**Date:** 21 October 2026

**Tool:** built-in image generation

**Normalisation:** alpha-greater-than-8 crop, Lanczos scale into a 216 px
target inside a 256 x 256 transparent RGBA cell, nearest fixed per-picture
flat palette, integer-centred placement, lossless PNG.

## Reference roles

- Each exact current V1 picture is the sole authority for identity, viewpoint,
  count, state, construction, topology, arrangement, overlap and silhouette.
- Approved `washing-plate` V2 is the primary shape calibration for lively
  mostly-even near-black contour and controlled minor asymmetry.
- Approved `sandwich-tomato` V2 is the primary colour calibration for flat
  opaque spot colour and selective detail.
- No outside comic panel or copyrighted visual was supplied to the generator.

## Accepted sources and exact prompts

### `repair-toolbox-source.png`

Cache: `exec-939406d7-8741-42bd-90a1-7c3eebc9ccdb.png`

> Use case: illustration-story.
> Asset type: isolated 256x256 Bubble stories picture source for Lighthouse Keeper.
> Input images: Image 1 is the exact current toolbox and is the sole semantic and compositional authority. Image 2, the approved washing plate, is the primary hand-drawn contour and asymmetry calibration. Image 3, the approved tomato, is the primary flat-colour and detail calibration.
> Primary request: Translate Image 1 into the approved original ligne-claire-inspired language. Preserve exactly ONE open dark-blue rectangular metal toolbox in the same low front three-quarter viewpoint: raised lid, box body, brass corner guards, central latch, two lid catches and U-shaped brass carry handle. Preserve the recognisable visible contents and their relative overlaps: spanner at left, red-handled pliers at centre, orange-brown screwdriver at right, and the smaller pale/blue tool shapes. Preserve the relative proportions and broad trapezoid silhouette. This is a faithful style refinement, not a redesign.
> Style/medium: lively near-black contour of mostly even weight with slight natural irregularity, simplified accurate shapes, strict flat opaque spot colours and minimal decisive interior lines.
> Composition/framing: one owned illustration centred on a genuine transparent background with generous clear margin, instantly readable at 64 px.
> Constraints: preserve identity, open state, viewpoint, construction, recognisable contents, relative arrangement and silhouette.
> Avoid: closed toolbox, extra or removed tools, changed hardware, gradients, gloss, reflected shine, rust texture, painterly modelling, cast shadow, hands, scenery, text, panel, watermark.

### `repair-boat-hull-patch-source.png`

Cache: `exec-6c1acbe0-cda2-40a9-aab1-545a3f0a867a.png`

This accepted source corrects the provenance-count conflict in the rejected
first pass below. Its exact edit prompt was:

> Use case: precise-object-edit.
> Asset type: isolated 256x256 Bubble stories picture source for Lighthouse Keeper.
> Input images: Image 1 is the rejected edit target whose successful flat ligne-claire finish should be retained. Image 2 is the exact current hull-patch picture and is the sole semantic and structural authority. Image 3, the approved washing plate, is the contour and controlled-asymmetry calibration.
> Primary request: Preserve exactly FOUR overlapping weathered blue hull planks. Preserve exactly TWO horizontal brown patch battens with exactly TWO visible brass fasteners on each. Preserve exactly TWO short vertical brown straps at the upper-right/right edge with exactly ONE visible brass fastener on each. There must be SIX visible brass fasteners total. Preserve exactly ONE wooden mallet in front-right with its handle extending down-left. Retain Image 1's successful flat colours, viewpoint, overlaps, broad silhouette and controlled hand-drawn asymmetry while making the construction unequivocally match Image 2.
> Constraints: four blue planks; two horizontal battens; two short vertical straps; six fasteners total; one mallet; genuine transparency and generous clear margin.
> Avoid: three or five planks, missing straps, missing or extra fasteners, extra tools, gradients, gloss, painterly modelling, cast shadow, scenery, text, panel, watermark.

### `repair-hammer-nails-source.png`

Cache: `exec-f5767384-ff41-46fe-b6b7-61a28f7e3438.png`

> Use case: illustration-story.
> Asset type: isolated 256x256 Bubble stories picture source for Lighthouse Keeper.
> Input images: Image 1 is the exact current hammer-and-nails picture and is the sole semantic and compositional authority. Image 2, the approved washing plate, is the primary hand-drawn contour and asymmetry calibration. Image 3, the approved tomato, is the flat-colour calibration.
> Primary request: Translate Image 1 into the approved original ligne-claire-inspired language. Preserve exactly ONE diagonal claw hammer running from its broad steel head at upper-right to its handle at lower-left: dark steel striking face and split claw, warm brown timber upper handle and weathered marine-blue lower grip. Preserve exactly THREE separate ochre-brass nails at lower-right in the same fan, with points down-left and heads upper-right. Preserve their relative sizes, spacing, viewpoint and broad silhouette.
> Style/medium: lively near-black mostly-even contour with minor natural irregularities, simplified accurate shapes, strict flat opaque spot colours and minimal decisive interior lines.
> Composition/framing: one owned illustration centred on a genuine transparent background with generous clear margin, instantly readable at 64 px.
> Avoid: extra or missing nails, bent nails, mallet, changed orientation, gradients, metallic gloss, reflected shine, cast shadow, hands, timber, scenery, text, panel, watermark.

### `repair-wrench-cog-source.png`

Cache: `exec-c83e004e-3a68-4d0c-94fa-ce707e4ed543.png`

> Use case: illustration-story.
> Asset type: isolated 256x256 Bubble stories picture source for Lighthouse Keeper.
> Input images: Image 1 is the exact current wrench-and-cog picture and is the sole semantic and compositional authority. Image 2, the approved washing plate, is the primary contour and controlled-asymmetry calibration. Image 3, the approved tomato, is the flat-colour calibration.
> Primary request: Translate Image 1 into the approved original ligne-claire-inspired language. Preserve exactly ONE large ochre-gold toothed cog behind, including its dark steel inset circular ring/hub and central opening. Preserve exactly ONE silver combination spanner crossing in front from open jaw at upper-left to ring end at lower-right, including the brown inset grip panel with exactly TWO brass pins. Preserve the crossing order, relative proportions, viewpoint, arrangement and broad silhouette.
> Style/medium: lively near-black contour of mostly even weight, simplified accurate shapes, strict flat opaque spot colours and minimal decisive interior lines. Allow minor hand-drawn irregularity in teeth, rings and curves without changing construction.
> Composition/framing: one owned illustration centred on a genuine transparent background with generous clear margin, instantly readable at 64 px.
> Avoid: extra gears or wrenches, adjustable wrench, changed crossing order, missing hub or grip pins, gradients, metallic gloss, reflected shine, cast shadow, scenery, text, panel, watermark.

### `repair-rope-knot-source.png`

Cache: `exec-e35cf3fc-68ee-4858-bdd0-183711d5a312.png`

This accepted source is the topology correction of the rejected first pass
below. Its exact edit prompt was:

> Use case: precise-object-edit.
> Asset type: isolated 256x256 Bubble stories picture source for Lighthouse Keeper.
> Input images: Image 1 is the rejected source and supplies the accepted flat ligne-claire finish. Image 2 is the exact current rope-knot picture and is the sole topology and compositional authority. Image 3, the approved washing plate, is the contour and controlled-asymmetry calibration.
> Primary request: Correct ONLY the central knot topology. Remove the invented upper braided loops. Redraw the centre as the same compact simple interwoven knot as Image 2, preserving its exact visible over-under route, crossings, lobes, height and broad horizontal silhouette. This must read as Image 2's knot, not as a more elaborate decorative knot. Keep exactly TWO short horizontal bound rope ends with their existing frayed tassels. Retain Image 1's pale-tan colour family, lively line language, genuine transparency and minor hand-drawn asymmetry.
> Constraints: preserve the current compact topology and two-end construction; change no unrelated attribute.
> Avoid: braided wreath, multiple upper loops, bow, noose, sailor's decorative knot, extra rope ends, gradients, gloss, cast shadow, scenery, text, panel, watermark.

## Rejected attempts and exact prompts

### `rejected/repair-boat-hull-patch-three-count-prompt-v1.png`

Cache: `exec-40bb0f89-7e94-4b0e-8433-982a696198f8.png`

Rejected because its pixels happened to retain the correct four planks and six
fasteners, but the prompt incorrectly asserted three planks and four total
fasteners. An enlarged audit corrected the provenance before acceptance.

> Use case: illustration-story.
> Asset type: isolated 256x256 Bubble stories picture source for Lighthouse Keeper.
> Input images: Image 1 is the exact current hull-patch picture and is the sole semantic and compositional authority. Image 2, the approved washing plate, is the primary hand-drawn contour and asymmetry calibration. Image 3, the approved tomato, is the flat-colour calibration.
> Primary request: Translate Image 1 into the approved original ligne-claire-inspired language. Preserve exactly THREE overlapping weathered blue hull planks, exactly TWO horizontal brown patch battens with exactly TWO visible brass fasteners on each, and exactly ONE wooden mallet in front-right with its handle extending down-left. Preserve the current viewpoint, overlap, relative scale and broad silhouette.
> Style/medium: lively near-black mostly-even contour with controlled minor irregularity, simplified accurate shapes, strict flat opaque spot colours and minimal decisive detail.
> Composition/framing: one owned illustration centred on a genuine transparent background with generous clear margin, instantly readable at 64 px.
> Avoid: extra planks, extra fasteners, extra tools, gradients, gloss, painterly modelling, cast shadow, scenery, text, panel, watermark.

### `rejected/repair-rope-knot-overcomplicated-v1.png`

Cache: `exec-b51ebc2e-1154-45b8-a5db-3339774dc9d8.png`

Rejected because it turned the current compact knot into an elaborate
multi-loop braided form.

> Use case: illustration-story.
> Asset type: isolated 256x256 Bubble stories picture source for Lighthouse Keeper.
> Input images: Image 1 is the exact current rope-knot picture and is the sole semantic, topological and compositional authority. Image 2, the approved washing plate, is the primary contour and controlled-asymmetry calibration. Image 3, the approved tomato, is the flat-colour calibration.
> Primary request: Translate Image 1 into the approved original ligne-claire-inspired language. Preserve exactly ONE thick pale-tan rope forming the same compact central interwoven knot, the same visible over-under path and crossings, and exactly TWO short horizontal bound ends with frayed tassels. Preserve the current relative proportions and broad horizontal silhouette.
> Style/medium: lively near-black contour of mostly even weight, simplified accurate rope strands, strict flat opaque spot colours and minimal decisive interior twist lines.
> Composition/framing: one owned illustration centred on a genuine transparent background with generous clear margin, instantly readable at 64 px.
> Avoid: changed knot topology, added loops, braided wreath, bow, noose, extra rope ends, gradients, glossy fibres, photoreal texture, cast shadow, scenery, text, panel, watermark.
