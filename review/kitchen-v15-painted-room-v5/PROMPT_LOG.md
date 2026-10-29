# Kitchen v15 painted-room v5 — image-edit record

Tool mode: OpenAI built-in image generator (`image_gen`), not CLI/API fallback.

## Wall-cupboard extraction trial

Inputs: the v4 wall-cupboard part as edit target, the unchanged liked kitchen
as style authority, and Frank's oven-spacing crop as fault evidence.

Final prompt:

> Use case: background-extraction. Asset type: isolated game-room furniture
> master PNG. Produce one front-on two-door wall cupboard as a clean isolated
> cutout in the brighter duck-egg painted joinery, with dark hand-drawn outlines,
> copper hinges and knobs. Use exact 136:101 proportions, equal-width doors,
> centred geometry and genuine transparency. Include no wall, cream background,
> oven, worktop, shadow, neighbour, label or watermark; do not redesign or add
> objects.

The trial was rejected because it changed the hand-painted line treatment into
a glossy rendered style. It was not copied into this review package and is not
used by the build.

The selected final wall-cupboard master is the already-approved hand-painted
transparent source at
`sources/clean-alpha-masters/wall-cupboard-master.png`. The build crops its
actual alpha bounds once, fits that master uniformly to 136 × 101, and writes
byte-identical `parts/wall_cupboard_1.png` and
`parts/wall_cupboard_2.png`. This preserves the project's painted treatment
while fixing the geometry deterministically.
