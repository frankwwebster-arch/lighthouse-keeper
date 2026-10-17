# Kitchen rear-wall flow V22 reference prompt

Built-in OpenAI image generation was given V21's full-room proof and V20's
connected three-bay room as image references, with this prompt:

> Edit the first image, using the second image as the construction reference.
> Keep the exact 772x224 pixel-art lighthouse kitchen composition, palette,
> wall, floor, pedal bin, refrigerator, kettle, toaster, small basic oven,
> mixer bowl, sink, single chair and table. Correct only the fitted cabinetry:
> make the refrigerator and all five counter bays one continuous straight
> galley run fixed flush against the rear wall, exactly edge-to-edge with no
> gaps, offsets, projecting standalone side panels, or staggered depth. Use the
> kettle bay in the first image as the exact depth and rear-wall registration
> authority. Continue one uninterrupted turquoise worktop line and one
> uninterrupted dark plinth line across the whole fitted run; show end panels
> only at the two outer ends. Preserve each bay width and the left-to-right
> order. Crisp deliberate low-resolution pixel art, no antialiasing, no text,
> no labels, no perspective drift.

The generated image is retained only as visual-intent provenance. Production
V22 is rebuilt deterministically on the existing 4-px/lp grid, preserving V21
asset pixels wherever they are not part of the rejected standalone carcasses.
