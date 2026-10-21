# Prompt log

**Date:** 21 October 2026

**Tool:** built-in image generation

**Normalisation:** alpha-greater-than-8 crop, Lanczos scale into a 216 px
target inside a 256 × 256 transparent RGBA cell, nearest fixed per-picture
flat palette, integer-centred placement, lossless PNG.

## Reference roles

- Each exact current V1 picture is the sole authority for identity, viewpoint,
  count, state, construction, arrangement, overlap and broad silhouette.
- Approved `sandwich-tomato` V2 is the primary style calibration for confident
  near-black contour, restrained flat colour, selective interior detail and
  64 px readability.
- Approved BBQ components are supporting style authority only.
- No outside comic panel or copyrighted visual was supplied to the generator.

## Accepted sources and exact prompts

### `washing-plate-source.png`

Cache: `exec-280b4e8e-d312-4e57-80e0-a18813386a63.png`

This accepted source is a flat-colour correction of the first rejected plate
pass below. Its exact edit prompt was:

> Use case: precise-object-edit.
> Asset type: isolated 256×256 Bubble stories picture source for Lighthouse Keeper.
> Input images: Image 1 is the edit target whose successful plate geometry, viewpoint, rim construction and bubble arrangement must be retained. Image 2 is the exact current washing-plate and remains the semantic/compositional authority. Image 3, the approved tomato, is the strict flat-colour style calibration.
> Primary request: Change ONLY Image 1's colour treatment to the genuinely flat opaque spot-colour language of Image 3. Remove every gradient, tonal blend, soft highlight, soft shadow and modelled lighting transition. Fill each bounded region with one uniform solid colour: warm cream ceramic, dark marine blue rim, pale aqua bubbles and near-black ink. Preserve the exact plate geometry, same oval perspective, double rim, bubble count and positions, linework, transparent canvas and broad silhouette.
> Style/medium: lively near-black contour of mostly even weight, strict flat opaque solid fills, minimal decisive interior lines. The output must look screen-printed or cel-coloured, not rendered.
> Constraints: change only the tonal treatment; preserve all shapes and layout; genuine transparency; no colour variation within any filled region.
> Avoid: gradients of any kind, radial shading, blue tonal shifts, cream tonal shifts, glossy highlights, reflected white shine, airbrush, feathering, soft shadows, cast shadow, texture noise, painterly modelling, extra bubbles, text, scenery, panel, watermark.

### `washing-liquid-source.png`

Cache: `exec-8809dc8f-f501-4a90-9e5a-3bdde560c654.png`

> Use case: illustration-story.
> Asset type: isolated 256×256 Bubble stories picture source for Lighthouse Keeper.
> Input images: Image 1 is the exact current washing-liquid picture and is the sole semantic and compositional authority. Image 2, the approved tomato, is the primary Lighthouse Keeper ligne-claire style calibration. Image 3 is additional approved style authority only.
> Primary request: Translate Image 1 into the approved original ligne-claire-inspired language. Preserve exactly ONE upright green washing-up-liquid squeeze bottle with the same compact hourglass body, broad rounded shoulders, narrow pinched waist, flat base, cream neck ring, dark-green ridged screw collar and short green push-pull cap. Preserve the low front viewpoint, slight rightward lean, relative proportions, construction and tall rounded silhouette. Preserve the two overlapping aqua soap bubbles outside the lower-left of the bottle and the few small round bubbles on its front; keep their relative arrangement without adding any. This is a faithful style refinement, not a redesign.
> Style/medium: lively near-black contour of mostly even weight, simplified accurate shapes, strict flat opaque spot colours, minimal decisive interior lines; match the approved tomato's confident contour, restrained colour and selective detail.
> Color palette: dominant emerald green bottle, restrained darker forest-green collar/side plane, warm cream neck ring, pale aqua bubbles, near-black ink.
> Composition/framing: one owned illustration centred on a genuine transparent background with generous clear margin, instantly readable at 64 px.
> Constraints: preserve subject identity, exactly one bottle, cap and collar construction, viewpoint, proportions, bubble arrangement and broad silhouette from Image 1. Use uniform solid fills; no reflected white shine.
> Avoid: gradients, translucent bottle rendering, glossy highlights, reflected white streaks, painterly modelling, airbrush, haze, bloom, cast shadow, thick sticker rim, label, branding, text, hands, sink, plate, scenery, panel, extra bottles, extra bubbles, watermark.

### `washing-sponge-source.png`

Cache: `exec-3880c735-c718-4753-85cf-4cdd7a20a262.png`

This accepted source is the targeted foam-and-count correction of the rejected
first pass below. Its exact edit prompt was:

> Use case: precise-object-edit.
> Asset type: isolated 256×256 Bubble stories picture source for Lighthouse Keeper.
> Input images: Image 1 is the edit target and supplies the accepted ligne-claire sponge construction. Image 2 is the exact current washing-sponge and is the authority for foam amount, bubble count and arrangement. Image 3 is the approved flat style calibration.
> Primary request: Correct ONLY the foam and bubble excess in Image 1. Reduce the foam to the modest single bank attached along the sponge's front-left edge as in Image 2; it must not wrap across the whole front or sit behind the upper edge. Keep exactly FIVE detached bubbles arranged like Image 2: one small at far left, one larger behind the upper-right edge with one tiny neighbour, and one larger at lower-right with one tiny neighbour. Reduce the sponge pores to a few sparse orange dots. Keep Image 1's exact one-sponge geometry, low front three-quarter viewpoint, yellow top, burnt-orange side faces, orientation, line language, transparent canvas and broad silhouette.
> Style/medium: lively near-black contour, simplified accurate shapes, flat opaque spot colours and minimal decisive interior lines.
> Constraints: change only foam extent, detached bubble count/placement and pore density; preserve all other shapes and layout.
> Avoid: foam behind the top edge, foam across the full front, more or fewer than five detached bubbles, dense pores, gradients, gloss, cast shadow, extra sponge, text, scenery, panel, watermark.

### `washing-droplets-source.png`

Cache: `exec-dd0ce19d-a366-4f7b-a260-fe5b3468bac6.png`

> Use case: illustration-story.
> Asset type: isolated 256×256 Bubble stories picture source for Lighthouse Keeper.
> Input images: Image 1 is the exact current washing-droplets picture and is the sole semantic and compositional authority. Image 2, the approved tomato, is the primary Lighthouse Keeper ligne-claire style calibration. Image 3 is additional approved style authority only.
> Primary request: Translate Image 1 into the approved original ligne-claire-inspired language. Preserve exactly FOUR separate falling water droplets: one dominant tall teardrop at centre, one medium curved teardrop at left, one smaller teardrop at right and one tiny round droplet below-left of centre. Preserve their individual pointing directions, relative sizes, spacing, low horizontal arrangement and broad compact triangular silhouette. This is a faithful style refinement of that exact asset, not a redesign.
> Style/medium: lively near-black contour of mostly even weight, simplified accurate shapes, strict flat opaque spot colours, minimal decisive interior lines; match the approved tomato's confident contour, restrained colour and selective detail.
> Color palette: dominant pale aqua, restrained deeper turquoise side facets, near-black ink.
> Composition/framing: one owned four-droplet illustration centred on a genuine transparent background with generous clear margin, instantly readable at 64 px.
> Constraints: preserve exactly four droplets, their shapes, orientation, relative scale, arrangement and broad silhouette from Image 1. Use uniform solid fills with at most one flat darker facet per large droplet.
> Avoid: gradients, transparency inside droplets, glossy highlights, reflected white shine, painterly modelling, airbrush, haze, bloom, cast shadow, thick sticker rim, bubbles, splashes, tap, sink, text, scenery, panel, extra droplets, watermark.

### `washing-cutlery-source.png`

Cache: `exec-c3ee3b28-61de-469d-a5e2-20ab8b97edd2.png`

This accepted source corrects the provenance conflict in the rejected first
pass below. Its exact edit prompt was:

> Use case: precise-object-edit.
> Asset type: isolated 256×256 Bubble stories picture source for Lighthouse Keeper.
> Input images: Image 1 is the edit target whose successful ligne-claire construction should be retained. Image 2 is the exact current washing-cutlery and is the semantic/compositional authority. Image 3 is the approved flat style calibration.
> Primary request: Faithfully retain exactly TWO crossed pieces of cutlery as in Image 2: one THREE-PRONGED fork running from upper-left to lower-right and one oval-bowled spoon running from upper-right to lower-left, with the spoon passing in front at the central crossing. Preserve Image 1's flat ligne-claire treatment, while ensuring the fork has exactly THREE clearly separated rounded prongs, matching Image 2. Preserve the rounded handles, one small ochre-gold inset near each handle end, bubble clusters, orientations, relative proportions, crossing order and broad X-shaped silhouette.
> Style/medium: lively near-black contour of mostly even weight, simplified accurate shapes, flat opaque spot colours and minimal decisive interior lines.
> Constraints: exactly one three-pronged fork and one spoon; preserve the existing composition, transparent canvas and bubble arrangement; do not change anything else.
> Avoid: four-pronged fork, extra utensils, changed crossing order, gradients, metallic gloss, cast shadow, hands, plate, sink, text, scenery, panel, watermark.

## Rejected attempts and exact prompts

### `rejected/washing-plate-tonal-v1.png`

Cache: `exec-99b8f58b-6582-46b2-a6ed-a8e2728c902d.png`

Rejected because the plate preserved its construction but retained blue and
cream tonal modelling rather than the tomato-calibrated flat treatment.

> Use case: illustration-story.
> Asset type: isolated 256×256 Bubble stories picture source for Lighthouse Keeper.
> Input images: Image 1 is the exact current washing-plate picture and is the sole semantic and compositional authority. Image 2, the approved tomato, is the primary Lighthouse Keeper ligne-claire style calibration. Image 3 is additional approved style authority only.
> Primary request: Translate Image 1 into the approved original ligne-claire-inspired language. Preserve exactly ONE broad oval cream ceramic plate in the same low front three-quarter viewpoint, with the same dark blue double rim, shallow central well, relative proportions, orientation and broad compact diagonal silhouette. Preserve the existing small aqua soap bubbles around the plate, including the overlapping bubbles near the upper-left and lower-right rim and the bubbles just outside the right edge; keep their relative placement without adding bubbles. This is a faithful style refinement of that exact asset, not a redesign.
> Style/medium: lively near-black contour of mostly even weight, simplified accurate shapes, flat opaque spot colours, minimal decisive interior lines; match the approved tomato's confident contour, restrained colour and selective detail.
> Color palette: dominant warm cream ceramic, restrained dark marine blue rim, pale aqua bubbles, near-black ink.
> Composition/framing: one owned illustration centred on a genuine transparent background with generous clear margin, instantly readable at 64 px.
> Constraints: preserve subject identity, exactly one plate, viewpoint, rim construction, bubble arrangement, relative scale, orientation and broad silhouette from Image 1. Replace glossy rendering with flat colour; no reflected white shine.
> Avoid: gradients, glossy highlights, reflected white shine marks, painterly modelling, airbrush, haze, bloom, cast shadow, thick sticker rim, emoji treatment, food, cutlery, hands, sink, text, scenery, panel, extra plates, extra bubbles, watermark.

### `rejected/washing-sponge-excess-foam-v1.png`

Cache: `exec-a11f0589-011f-4ea3-9430-e8d6a41ffb38.png`

Rejected because it enlarged the foam bank, added bubbles and increased pore
density instead of preserving the current restrained arrangement.

> Use case: illustration-story.
> Asset type: isolated 256×256 Bubble stories picture source for Lighthouse Keeper.
> Input images: Image 1 is the exact current washing-sponge picture and is the sole semantic and compositional authority. Image 2, the approved tomato, is the primary Lighthouse Keeper ligne-claire style calibration. Image 3 is additional approved style authority only.
> Primary request: Translate Image 1 into the approved original ligne-claire-inspired language. Preserve exactly ONE thick rectangular yellow cellulose kitchen sponge with softly rounded corners in the same low front three-quarter viewpoint, showing the broad perforated yellow top face and the narrower burnt-orange front and right side faces. Preserve its left-high to right-low orientation, proportions and broad compact diagonal silhouette. Preserve the bank of pale aqua-white soap foam along the front-left edge and the few detached bubbles around it in the same relative arrangement. This is a faithful style refinement of that exact asset, not a redesign.
> Style/medium: lively near-black contour of mostly even weight, simplified accurate shapes, strict flat opaque spot colours, minimal decisive interior lines; match the approved tomato's confident contour, restrained colour and selective detail.
> Color palette: dominant warm golden yellow sponge, restrained burnt-orange side plane and pores, pale aqua-white foam, near-black ink.
> Composition/framing: one owned illustration centred on a genuine transparent background with generous clear margin, instantly readable at 64 px.
> Constraints: preserve subject identity, exactly one sponge, viewpoint, thickness, face construction, orientation, foam placement, detached-bubble arrangement and broad silhouette from Image 1. Use uniform solid fills; pores must remain sparse.
> Avoid: gradients, glossy highlights, reflected white shine, painterly modelling, airbrush, texture noise, dense pores, haze, bloom, cast shadow, thick sticker rim, green scouring layer, hands, sink, plate, text, scenery, panel, extra sponges, excessive foam, extra bubbles, watermark.

### `rejected/washing-cutlery-prompt-conflict-v1.png`

Cache: `exec-c1c27cee-0e01-4515-9190-a81f1b9d69b0.png`

Rejected because the image correctly retained three fork prongs but the prompt
incorrectly asserted four; the accepted rerun makes provenance unambiguous.

> Use case: illustration-story.
> Asset type: isolated 256×256 Bubble stories picture source for Lighthouse Keeper.
> Input images: Image 1 is the exact current washing-cutlery picture and is the sole semantic and compositional authority. Image 2, the approved tomato, is the primary Lighthouse Keeper ligne-claire style calibration. Image 3 is additional approved style authority only.
> Primary request: Translate Image 1 into the approved original ligne-claire-inspired language. Preserve exactly TWO crossed pieces of clean cutlery: one four-tined fork running from upper-left to lower-right and one oval-bowled spoon running from upper-right to lower-left, crossing at centre with the spoon in front. Preserve the warm cream metal faces, restrained taupe side facets, narrow dark outlines, rounded handles, one small ochre-gold round inset near the end of each handle, the low front three-quarter viewpoint, relative proportions, crossing order and broad X-shaped silhouette. Preserve the small pale-aqua soap-bubble clusters around the crossing in their same relative arrangement. This is a faithful style refinement of that exact asset, not a redesign.
> Style/medium: lively near-black contour of mostly even weight, simplified accurate shapes, strict flat opaque spot colours, minimal decisive interior lines; match the approved tomato's confident contour, restrained colour and selective detail.
> Color palette: dominant warm cream cutlery, restrained taupe side planes, pale aqua bubbles, ochre-gold handle insets, near-black ink.
> Composition/framing: one owned crossed-cutlery illustration centred on a genuine transparent background with generous clear margin, instantly readable at 64 px.
> Constraints: preserve exactly one fork and one spoon, fork tine count, crossing order, orientations, handle details, bubble arrangement, relative scale and broad silhouette from Image 1. Use uniform solid fills.
> Avoid: gradients, metallic gloss, reflected white shine, painterly modelling, airbrush, haze, bloom, cast shadow, thick sticker rim, knife, extra utensils, changed crossing order, hands, plate, sink, text, scenery, panel, extra bubble clusters, watermark.
