# Claude Code implementation prompt

Work in the Lighthouse Keeper repository. Read `AGENTS.md`, `CLAUDE.md`, and the current `docs/SPEC.md` before editing, and preserve unrelated user work.

Wire the approved ordinary room-door system from:

`art/drafts/room-door-compass-rose-wiring-handoff-2026-10-29-v1/`

Read that directory's `README.md` and `door-runtime-contract.json` in full. Use the supplied painted PNGs. Do not redraw the leaf in code, and do not use the reference MP4 as runtime art.

Core requirements:

- room scale 168 px/m;
- runtime leaf 168 × 336 px; lighthouse mip 20 × 40 px;
- canonical Prime Keeper stays exactly 120 × 298 px and is never resized;
- leaf opens automatically toward stage front to exactly 90°, with its full face parallel to the player/camera;
- it reaches open and becomes stationary before the Keeper crosses;
- the stationary open leaf renders in front of and fully occludes the Keeper;
- it cannot open or close while the Keeper intersects its swept volume;
- it auto-closes only after his full bounds clear the sweep plus safety margin;
- left/right room-door variants mirror hinge and handle placement correctly, with no double hinges;
- decorative and stained-glass designs are room-door-only; cupboard and secret-cupboard doors remain opaque monotone.

The studio currently has placeholder geometry in `src/studio/recipe.ts`, a rectangle leaf in `src/studio/StageView.tsx`, and useful coverage/collision tests in `src/studio/recipe.test.ts`. Preserve the useful semantics, use an explicit logical-unit-to-art-pixel conversion, and wire the same behaviour into the actual game room renderer—not only the studio.

The current SPEC records the approved automatic 90° visible leaf animation and the no-Keeper-handle-animation rule. Keep code, tests and documentation consistent with it.

Verify the complete flow at room and lighthouse scales, run the relevant tests and build, and follow the repository's issue, review, commit and delivery rules. Do not broaden scope into kitchen cabinetry or generate replacement art.
