# Prompt log

**Date:** 21 October 2026

**Tool:** built-in image generation
**Normalisation:** deterministic crop, scale into a 216 px target inside a
256 × 256 transparent cell, nearest fixed per-picture flat palette, centred on
integer coordinates, PNG lossless output.

## Reference roles

- `/Users/frank/Downloads/tintin ref.jpeg`: directional evidence only for
  ligne-claire ink and flat colour. No scene, character, panel, lettering,
  exact prop or arrangement may be copied.
- The current Lighthouse picture named in each entry: semantic and continuity
  reference for subject identity, viewpoint, count, state, container and broad
  composition. It is not copied pixel-for-pixel.

## Accepted sources and exact prompts

### `bbq-grill-unlit-source.png`

Cache: `exec-23685bc4-1383-4b24-8a20-49aa8aa2680e.png`

> Use case: stylized-concept. Create exactly one original isolated activity-story picture: an UNLIT ROUND CHARCOAL BARBECUE. The first reference supplies only flat ligne-claire visual grammar; copy no character, scene, panel, lettering or exact prop. The second reference supplies only the subject category and compact front three-quarter viewpoint; redesign it rather than tracing. Draw a friendly but mechanically believable round enamel kettle grill on three short legs, open bowl and grate visible, containing cold charcoal. Lively near-black contour of mostly even weight, minimal decisive interior ink lines, flat opaque spot colours: dominant muted teal-blue enamel, charcoal black/grey, small ochre handles. No gradients, no highlights, no painterly modelling, no gloss, no shadow, no heat/smoke/spark marks, no text, no scenery, no duplicate object. Genuine transparent background, one owner, centred compact silhouette, generous clear margin, readable at 64 px.

### `bbq-grill-source.png`

Cache: `exec-d7f0a935-b5b6-4ea3-9c82-e1f2e33510b6.png`

> Create a separate LIT version of this exact original round charcoal grill for an activity-story pilot. Preserve the same grill model, front three-quarter viewpoint, silhouette, proportions, grate, legs, handles, line drawing, transparent canvas and generous margin. Change only the charcoal state: make some coals flat coral-red and muted orange with a few black coals remaining. Use pure flat spot colours and near-black lines. Remove any rendered gradient or glossy highlight from the enamel and handles so the whole drawing reads as clean ligne claire. Do not add flame, smoke, heat curls, sparks, glow, text, floor, background, shadow, food or another object. Do not overwrite the referenced source; return a new transparent image.

### `bbq-charcoal-source.png`

Cache: `exec-2cd449c4-d417-4844-be47-381b517edd52.png`

> Create exactly one original isolated ligne-claire refinement of the CURRENT LIGHTHOUSE BBQ CHARCOAL ASSET. Preserve the existing asset’s concept and broad composition: one open ochre paper charcoal bag standing behind several loose charcoal lumps, visible black coals inside the bag, a coral-red flame motif on the bag, front three-quarter view. This is a faithful style translation, not a redesign; do not remove the bag or change the semantic contents. Use the comic reference only for flat near-black ink and spot-colour grammar; copy no panel, character or exact object drawing. Lively mostly even near-black contour, simple fold and crack lines, pure flat ochre, coral, charcoal grey and black. Absolutely no gradients, glossy highlights, painted texture, haze, glow, cast shadow, text, logo, floor, scenery or detached decoration. Genuine transparent RGBA outside the hard outline, one owned illustration, generous clear margin, readable at 64 px.

### `bbq-sausages-source.png`

Cache: `exec-d9e9b757-8d5d-4031-9f76-9714c118d7cf.png`

> Create exactly one original isolated ligne-claire refinement of the CURRENT LIGHTHOUSE RAW SAUSAGES ASSET. Preserve the existing asset’s concept and broad composition: five plump raw sausages joined in one loose curved chain, no plate, tray or garnish. This is a faithful style translation, not a redesign; keep the count, linked state and diagonal flowing silhouette. Use the comic reference only for flat near-black ink and spot-colour grammar; copy no panel or exact drawing. Lively mostly even near-black contour, a few simple curved seam lines, pure flat muted coral-pink with one darker coral spot colour. No gradients, glossy highlights, marbling texture, painterly modelling, shadow, text, floor, scenery or detached decoration. Genuine transparent RGBA, one owner, generous clear margin, readable at 64 px.

### `bbq-hotdogs-source.png`

Cache: `exec-99e4c968-6c20-41cd-bba5-41582dc8d9ab.png`

> Create exactly one original isolated ligne-claire refinement of the CURRENT LIGHTHOUSE HOT DOGS ASSET. Preserve the existing asset’s concept and broad composition: two finished hot dogs overlapping diagonally, each a browned sausage in a golden bun with a mustard zigzag. This is a faithful style translation, not a redesign; keep two, their served state and recognisable arrangement. Use the comic reference only for flat near-black ink and spot-colour grammar; copy no panel or exact drawing. Lively mostly even near-black contour, minimal bun seam and grill lines, pure flat golden yellow, coral-brown, mustard yellow and cream. No gradients, glossy highlights, seed texture, painterly modelling, plate, garnish, shadow, text, floor, scenery or detached decoration. Genuine transparent RGBA, one owned illustration, generous clear margin, readable at 64 px.

### `bbq-tongs-source.png`

Cache: `exec-173fad28-4f96-42a5-a9cb-d0179369c95c.png`

> Create exactly one original isolated ligne-claire refinement of the CURRENT LIGHTHOUSE BBQ TONGS ASSET. Preserve the existing asset’s concept and broad composition: one closed pair of long steel barbecue tongs lying on a rising diagonal, scalloped gripping ends at lower-left, two dark blue handle arms joined by a small ochre hanging loop at upper-right. This is a faithful style translation, not a redesign. Use the comic reference only for flat near-black ink and spot-colour grammar; copy no panel or exact drawing. Lively mostly even near-black contour, minimal decisive metal seam lines, pure flat cream-grey steel, dark teal-blue grips and ochre loop. No gradients, glossy highlights, painterly modelling, shadow, text, floor, scenery or detached marks. Genuine transparent RGBA, one owner, generous clear margin, readable at 64 px.

## Rejected attempts

- `rejected/bbq-charcoal-loose-v1.png` — removed the current charcoal bag and
  changed the asset's meaning; it also introduced haze.
- `rejected/bbq-charcoal-loose-v2.png` — repeated the bagless semantic error
  and retained unwanted background treatment.
