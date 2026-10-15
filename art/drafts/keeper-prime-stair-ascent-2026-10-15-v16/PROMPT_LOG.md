# Keeper Prime stair ascent V16 prompt log

Built-in image editing supplied two high-resolution correction studies. They are evidence sources only; deterministic registration and narrow masks decide every candidate pixel.

## RIGHT compact-passing study

Use case: precise-object-edit. Image 1 was V14 RIGHT compact passing; Image 2 was V14 LEFT compact passing. Correct only the raised forward/right leg and boot so its visual lift, knee bend and boot height match the restrained LEFT reference. Preserve the exact Keeper identity, planted leg, body, palette, transparent background and safety gutter. Keep the moving boot compact, retracted and complete.

Built-in output: `sources/generated/right-passing-balanced-lift.png`.

## RIGHT-contact toecap study

Use case: precise-object-edit. Image 1 was V14 RIGHT contact; Image 2 was the same-pose V6 leg authority. Restore only the complete rounded toecap and upper-front contour of the forward/leftmost boot. Preserve pose, sole footprint, contact height, all other anatomy and transparent background.

Built-in output: `sources/generated/right-contact-complete-toecap.png`.

## LEFT-contact artefact

No generated pixels are used. The small detached flesh remnant is removed deterministically by restoring the exact V6 base pixels inside only the measured artefact-difference mask.
