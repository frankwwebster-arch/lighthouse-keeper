# Kitchen v15 painted-room v7 — image-edit record

Tool mode: OpenAI built-in image generator (`image_gen`), precise object edits.
No CLI/API fallback was used.

## Rejected v7 whole-carcass depth trial

Inputs: v6 dresser as edit target, the neighbouring base-cabinet depth
authority, and the v6 assembled room as context. Final prompt:

> Change only the front-to-back depth of the dresser's complete lower cabinet
> carcass below the wooden worktop. The lower cabinet, plinth and feet must
> extend all the way forward to the identical floor/base contact plane as the
> neighbouring fitted cabinet. Preserve the upper hutch, crockery, width,
> worktop thickness, duck-egg paint, copper fittings, matte hand-drawn style,
> front elevation and transparent background. Add no side faces, shadows or
> objects.

The trial correctly understood the deeper silhouette but repainted the retained
matte dresser with glossy modelling. It was rejected and is not stored or used.
V7 instead preserves the v6 pixels and extends the complete lower carcass to
the exact shared y485 datum deterministically.

## Selected shell edit

Inputs: v5 empty shell, `reference/shell/room-shell-reference-01.png`, and the
approved compass-rose door leaf. Final prompt:

> Edit only the two side door areas of this 2172 × 724 bright duck-egg kitchen
> shell. Remove both baked-in orange door leaves and handles while preserving
> the jambs, one-point side-wall perspective, wall colour, beams, skirting,
> floorboards, windows and every central-room pixel. Leave symmetrical dark,
> empty doorway apertures ready for a separate approved moving leaf. Do not add
> furniture, props, people, text, shadows or a different room style. Preserve
> the source canvas and framing.

Selected generated source:
`sources/imagegen/kitchen-v15-jambs-only-shell-source.png` (2172 × 724).
The build uses only its two side-door pixel regions, then deterministically
registers the aperture height to the approved y208–544 leaf contract. The
central liked shell remains from the v5 source.

## Rejected sink edit trial

Inputs: the shared base-cupboard master, v5 sink and v5 room. Prompt asked for
the identical cabinet body with only a Belfast basin and compact copper taps.
The result was rejected because it introduced glossy 3D modelling and changed
the approved painted cabinet language. It is not stored or used. V6 instead
splits the retained approved v8 Belfast master across the existing worktop and
sink-cabinet boxes.

## Rejected dresser edit trial

Inputs: v5 dresser, base cupboard, worktop and room. Prompt asked to preserve
the dresser while changing only its front-to-back reveal to the shared 0.60 m
depth. The result was rejected because it repainted details and increased
gloss. It is not stored or used. V6 deterministically fits the retained v5
dresser around the exact 31 px worktop-master band.
