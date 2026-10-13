# Keeper Prime Walk V1 prompt and decision log

Built-in image generation was used in identity-preserve mode. Reference order was fixed:

1. approved smooth Side-right master — identity, rendering, proportions, outfit and palette;
2. legacy generated walk sheet — choreography only;
3. approved Rig Motion V3 keyframes — leg amplitude and cadence only.

## Initial generation prompt

> Use case: identity-preserve
> Asset type: high-resolution game character animation source sheet
> Primary request: Create one coherent eight-pose right-facing walk-cycle source sheet of the approved Lighthouse Keeper, arranged as a strict 4 columns × 2 rows grid, read left-to-right across the top row then left-to-right across the bottom row. The eight poses must form a smooth complete walk loop with strong but natural leg movement: contact, down, passing, up, opposite contact, opposite down, opposite passing, opposite up. Use opposite arm swing and clearly planted side-facing boots. The character walks to the right; this is pose artwork only, with no baked horizontal translation.
> Input images: Image 1 is the sole approved identity, rendering, outfit, palette, proportions, beard, face and smooth-edge authority; Image 2 is choreography-only evidence for the existing eight-pose right-facing walk and must not supply identity, pixelation, double-stripe clothing or rendering style; Image 3 is construction-motion-only evidence for the approved larger thigh swing and knee lift and must not supply finished appearance.
> Subject: The exact same adult, rotund Lighthouse Keeper in all eight cells: approved blue cap and badge, solid dark rectangular profile eye with no glint, separate moustache, short readable closed mouth, established forward beard with separate rear hair mass, single broad pale jumper stripe, approved dark trousers and approved side-facing boots.
> Style/medium: match Image 1 exactly: super-smooth high-resolution polished 2D character illustration with clean antialiased outlines, consistent shading and identical colour palette in every pose; never pixel art.
> Composition/framing: genuine transparent background; eight equal generous cells in a 4×2 grid; one complete full-body figure centered in each cell; identical character scale and common floor baseline; large fully transparent gutter around every figure and between every cell; no figure, hair, hand, clothing or boot may touch or cross a cell boundary.
> Constraints: preserve Image 1 identity and total standing scale; preserve head size, beard mass, torso fatness, hand size, boot construction and one-band uniform; use the approved rig's larger leg swing and knee lift; exactly two arms, two hands, two legs and two boots in every pose; smooth cyclic progression with no duplicated pose; first and last poses must join cleanly; no prop; no scenery; no cast shadow; no text; no labels; no guides; no borders; no watermark.
> Avoid: double stripe, generic smile, grin, white eye glint, round childlike eye, mouth merged into moustache, beard/hair confusion, body thinning, perspective or scale change, palette flash, boot shape change, rough or pixelated edges, detached fragments, overlapping cells.

The output had genuine alpha despite the preview showing hidden RGB. A background-only edit was attempted before that was measured; it was retained but rejected as unnecessary.

## Background-only prompt

> Use case: background-extraction
> Asset type: high-resolution game character animation source sheet
> Primary request: Remove the entire dark blue/brown gradient background and every glow or shadow around the figures. Return the same eight Keeper figures on a genuinely transparent alpha background.
> Input images: Image 1 is the edit target.
> Constraints: change only the background and edge cleanup; preserve all eight characters, their poses, positions, scale, colours, linework, shading and 4×2 layout exactly; preserve full antialiased figure edges and fully opaque interiors; keep large fully transparent gutters around and between every figure; no checkerboard baked into the pixels; no scenery; no cast shadows; no halo; no text; no borders; no watermark.

The initial sheet measured a small top-row/bottom-row scale inconsistency. It remains rejected provenance.

## Selected scale-consistency correction prompt

> Use case: identity-preserve
> Asset type: corrected high-resolution game character animation source sheet
> Primary request: Correct only the within-sheet character scale inconsistency in the supplied 4×2 eight-pose Lighthouse Keeper walk cycle. Redraw/register the bottom four figures so all eight figures have exactly the same character scale and body proportions. Every cell must have the same cap-top-to-planted-sole height envelope, while natural walking knee bend may move the cap vertically by only a very small gait bob. Keep all eight existing gait poses and their order.
> Input images: Image 1 is the edit target and sole visual source.
> Composition/framing: preserve the exact 1536×1024 4-column × 2-row layout; each local cell is 384×512; use a common local floor line and generous fully transparent gutter; no figure may touch a cell edge.
> Constraints: change only scale/registration needed to make all eight figures one consistent Keeper; preserve the approved identity, face, beard, hair, one-band uniform, palette, shading, line weight, boot construction, pose sequence and right-facing direction; genuine transparent alpha background; super-smooth antialiased edges; exactly two arms, two hands, two legs and two boots in every pose; no scenery, glow, shadow, text, labels, guides, borders or watermark.
> Avoid: any body thinning, head-size change, beard-size change, palette flash, pose replacement, duplicated pose, pixelated edge or background colour.

Selected source SHA-256: `3df7c4bac24b8e9f066f0dc58a485e330f407fd2b779a120cc50c2a5ffb05e47`.
