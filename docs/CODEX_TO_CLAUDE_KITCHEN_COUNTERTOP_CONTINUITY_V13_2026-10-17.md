# Codex to Claude: Kitchen countertop continuity V13

Frank rejected the V10 countertop result after identifying visible break-up. The old assertion checked alpha on one row and was not a valid surface-continuity test.

Continue from `/keeper-review/kitchen-countertop-continuity-v13/` and `docs/KITCHEN_COUNTERTOP_CONTINUITY_V13_RECIPE_2026-10-17.md`. V13 redraws the complete Option-B slab last in every kettle, toaster and mixer frame. The sink restores its basin only inside x 23–61 px; both wings remain byte-exact canonical slab pixels. The room composite includes the V10 plant shelf and V12 recipe-book shelf.

The V13 verifier covers 1,120 slab pixels per frame across all standard, on and broken states and proves sensitivity with V10 as a failing control. Do not weaken this to opacity, bounding-box or single-row checks. Nothing is approved, promoted or wired.

## Delivery record

- Content commit: `839b66e` (`Add exact Kitchen V13 countertop continuity gate`).
- Production deployment marker: `599902e` (`Deploy: Kitchen V13 exact countertop continuity review [deploy]`).
- Live review: `https://lighthouse-keeper-mu.vercel.app/keeper-review/kitchen-countertop-continuity-v13/` returned HTTP 200.
- The archived complete-room asset resolved through the content-addressed route and measured exactly 772 × 224 px (193 × 56 lp at density 4).
- `npm run verify:kitchen-countertop-continuity-v13`, `node scripts/verify_review_archive.mjs` and the full `npm test` suite passed after rebasing with the concurrent Darts work; Vitest reported 179/179 tests.

Documentation audit completed: `README.md`, `docs/DECISIONS.md`, the reusable recipe, package scripts and this hand-back now identify V10's countertop portion as rejected, V13 as the current review draft, the exact test boundary, deployment state and the continuing no-promotion/no-wiring constraint. No runtime, setup, recovery or live-game documentation changed because V13 adds only immutable review media and its verifier.
