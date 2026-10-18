# Kitchen V31 comic-readable bin stench

Date: 18 October 2026
Status: approved review authority; unpromoted/unwired
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

Frank approved this exact V31 asset/effect family on 18 October 2026. The
approval pins the two reusable effect strips, the unchanged V28 object and room
proofs, the candidate catalogue, batch register and deployed review page. It
does not promote anything into Final art or runtime wiring.
The durable decision is
[`docs/review/kitchen-bin-effects-v31-approval-2026-10-18.json`](review/kitchen-bin-effects-v31-approval-2026-10-18.json).

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
- Focused verification: `npm run verify:kitchen-bin-effects-v31`,
  `npm run verify:kitchen-bin-effects-v31-approval` and
  `npm run verify:review-archive`.
- Full verification: `npm test` and `npm run build`.
- Documentation audit completed on 18 October 2026. README, STATUS and
  DECISIONS identify V31 as the approved two-overlay semantic-readability
  authority.
  Runtime, Final art and canonical V20–V30 assets remain unchanged.
