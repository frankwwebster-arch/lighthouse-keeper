# Kitchen V31 comic-readable bin stench

Date: 18 October 2026
Status: complete effect review draft; awaiting visual confirmation; unpromoted/unwired
Review: `/keeper-review/kitchen-bin-effects-v31/`

V31 replaces V30's object-shaped high plume with wordless comic visual grammar
that should be immediately understandable to a young player familiar with
traditional comics. The approved V28 bin and room pixels remain byte-identical
and the environmental loop remains 40 frames at 4 fps, lasting ten seconds.

The miasma uses three open curling green smell trails with hooked ends over four
broken translucent haze patches. The patches contain large negative cuts, so
they cannot merge into a single smoke object. Three flies now use clearer 2 × 2
px bodies, paired wings and intermittent motion ticks on slow uneven paths.
The centre smell trail remains connected to the rubbish opening in every frame.
The bin object itself does not animate.

Native review outputs live under
`art/raw/kitchen-bin-effects-2026-10-18-v31/`. The reversible catalogue and
rollback register live under
`art/drafts/kitchen-bin-effects-2026-10-18-v31/`. The deterministic visual
recipe is recorded in
`art/source/kitchen-bin-effects-2026-10-18-v31/DESIGN.md` and
`scripts/build_kitchen_bin_effects_v31.py`.

## Verification and documentation audit

- Rebuild with the bundled Python runtime using
  `scripts/build_kitchen_bin_effects_v31.py`, then run
  `npm run archive:keeper-review`.
- Focused verification: `npm run verify:kitchen-bin-effects-v31` and
  `npm run verify:review-archive`.
- Full verification: `npm test` and `npm run build`.
- Documentation audit completed on 18 October 2026. README, STATUS and
  DECISIONS identify V31 as a two-overlay semantic-readability successor.
  Runtime, Final art and canonical V20–V30 assets remain unchanged.
