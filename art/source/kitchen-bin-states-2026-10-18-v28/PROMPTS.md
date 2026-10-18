# Kitchen V28 bin state-family source prompts

Date: 18 October 2026
Mode: built-in image generation, followed by deterministic native-size reduction

## Initial coordinated drawing

Draw a compact narrow cylindrical enamel pedal bin from scratch in exactly two
states, standard and broken/overflowing. Both states use the same front-facing
design, scale, shell geometry, turquoise/cyan palette, navy pixel outline,
orange foot pedal, viewpoint and floor contact. The broken state has a lid
forced upward and off-centre by packed, recognisable household rubbish. The
background is genuinely transparent and the two static sprites have a wide
transparent gutter. No animation effects, room, text or watermark.

Generated source:
`generated/bin-two-state-source-v1.png`
SHA-256: `d917330d83d2e9527e02dc7d8dbdaae0a9e27aa024879775839645a89f99d5ba`

## One-change spill revision

Change only the broken state by adding a restrained floor spill at its base:
one crumpled paper piece, one orange peel/vegetable scrap and one small dark
refuse scrap. Preserve the standard state and the broken shell, lid, packed
rubbish, scale, viewpoint, palette, pedal and baseline. Keep the background
transparent and omit flies, miasma, motion marks, smoke, water and other
animation effects.

Selected source:
`generated/bin-two-state-spill-source-v2.png`
SHA-256: `f07c82b186dab52aff66fbde0ccabe23ef0f3428f64656dbe4f9716b6c74d1ec`

The complete structured prompts are preserved in the originating Codex task.
This file records the durable production intent, source choice and hashes.

## Reusable environmental effects

The static object sources above do not contain animation. V28's builder draws
two independent native-pixel overlays from deterministic coordinates:

- `stench_miasma`: four staggered olive/green puffs connected continuously to
  the bin opening by a narrow vapour stem;
- `slow_flies`: three small flies on shallow independent orbits with restrained
  two-frame wing changes.

Both strips use 80 × 80 px isolated cells, 24 distinct frames at 4 fps and a
six-second loop. They can be positioned against another asset by changing only
the layer anchor; they do not modify the underlying object pixels.
