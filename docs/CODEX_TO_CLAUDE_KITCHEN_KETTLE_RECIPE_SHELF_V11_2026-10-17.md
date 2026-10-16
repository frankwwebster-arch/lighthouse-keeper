# Codex → Claude: Kitchen V11 kettle shelf hand-back

Date: 17 October 2026  
Status: reversible review draft; unapproved and unwired

V11 adds only `obj_kettle_recipe_shelf_v11_f1`: a messy recipe-book shelf with
one jar bookend at each end. It is a separate 21 × 56-lp wall child owned by the
kettle, with no interaction spot. Its x transform is identical to the kettle's
at bays 2, 5 and 8. V10, Keeper art, runtime assets, Final and manifests are
unchanged.

Continue from:

- `data/kitchen_kettle_recipe_shelf_v11_recipe.json`
- `scripts/build_kitchen_kettle_recipe_shelf_v11.py`
- `scripts/verify_kitchen_kettle_recipe_shelf_v11.mjs`
- `/keeper-review/kitchen-kettle-recipe-shelf-v11/`

Do not promote or wire this shelf without Frank's explicit approval.

## Verification record

- Content commit: `8f83497`.
- Production trigger: `0ec0a67` (`[deploy]`).
- Shelf opaque bound: exactly `19 × 6.75 lp` inside its `21 × 56-lp` cell.
- Movement proofs: bays 2, 5 and 8; each jump is exactly `63 lp` for both
  kettle and shelf.
- `npm test`: 18 test files and 179 tests passed, plus every deterministic
  kitchen and Keeper pretest.
- Live review and archived shelf PNG both returned HTTP 200; the live shelf is
  exactly `84 × 224` raster pixels.
- Documentation audit: README, decisions, recipe and hand-back agree that V11
  is decorative, non-interactive, review-only and not wired into the game.
