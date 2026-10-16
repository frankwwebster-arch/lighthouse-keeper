# Kitchen Basic Assets V6 Option B: Codex → Claude hand-back

**Date:** 16 October 2026

**Status:** full-family review draft; unapproved, reversible and not wired

**Review page:** `/keeper-review/kitchen-basic-assets-v6-option-b/`

## Decision applied

Frank selected countertop calibration **B**. Every compatible unit now uses a
1.5-lp visible top, 2-lp fascia, zero shear, equal-width horizontal rear/front
edges and vertical parallel sides. Kitchen V5 remains the sole baseline. The
removed former V6 was not used.

During the full pass, the calibration implementation's two-pixel right outline
was found to paint one source pixel beyond the nominal edge. V6 corrects that
stroke inward: ordinary tops now measure exactly 80 px / 20 lp inside their
84-px / 21-lp cells. This is the selected B appearance with the precise room-
grid containment Frank required.

Frank also found the V5-width bin too broad. V6 centres a 15-lp pedal bin in
the unchanged 21-lp cell, leaving 3 lp clear on each side. Its full and
overflowing states share the same narrower base.

## Measured assets

| Item | Cell | Largest alpha bound | Bays | Interaction spot | States |
| --- | ---: | ---: | ---: | ---: | --- |
| pedal bin | 21 × 16 lp | 15 × 15 lp | 1 | 116 ku | standard, full, overflowing |
| freestanding fridge | 21 × 21 lp | 20 × 21 lp | 1 | 284 ku | standard, on, broken |
| kettle counter | 21 × 31 lp | 20 × 31 lp | 1 | 452 ku | standard, on, broken |
| toaster counter | 21 × 31 lp | 20 × 31 lp | 1 | 620 ku | standard, on, broken |
| cooker / hob | 21 × 28 lp | 20 × 28 lp | 1 | 788 ku | standard, on, broken |
| mixer counter | 21 × 31 lp | 20 × 31 lp | 1 | 956 ku | standard, on, broken |
| sink counter | 21 × 29 lp | 20 × 29 lp | 1 | 1124 ku | standard, on, broken; three dish overlays |
| table + player-side chair | 42 × 28 lp | 40 × 26 lp | 2 | 1292 ku | standard; separate chair/table layers |
| pet bowl | 16 × 8 lp | 12 × 3 lp | foreground child | 1440 ku | standard, full, broken |
| cupboard leaf | 38 × 56 lp | 34 × 52 lp open | fixed far cap | 1512 ku | edge-on, opening, open |

All ordinary furniture remains in its 21-lp ownership cell. The 9-bay room is
193 × 56 lp; the 12-bay outline is 256 × 56 lp; modular shells remain exact
for 6–12 bays. The cupboard is fixed to the far right side wall and remains
last. Worktop, hob and table interaction datum remains 19 lp; chair seat remains
11 lp. Existing Keeper oven, table and cupboard clips are unchanged.

## Animation contract

Every revised `on` and `broken` strip is made from one exact V6 standard base.
Effects and moving parts are clipped to declared rectangles; the verifier
compares every RGBA channel outside those masks with the base. V5's whole-
object broken-state shake is deliberately removed because it moved stationary
cabinet pixels. Timing and four-frame counts remain unchanged.

## Recipe and reversible files

- recipe: `docs/KITCHEN_COUNTERTOP_OPTION_B_RECIPE_2026-10-16.md`;
- machine authority: `data/kitchen_countertop_option_b_recipe.json`;
- constructor: `scripts/kitchen_countertop_option_b.py`;
- builder: `scripts/build_kitchen_basic_assets_v6_option_b.py`;
- verifier: `scripts/verify_kitchen_basic_assets_v6_option_b.mjs`;
- source/provenance: `art/source/kitchen-basic-assets-2026-10-16-v6-option-b/`;
- raw draft: `art/raw/kitchen-basic-assets-2026-10-16-v6-option-b/`;
- records: `art/drafts/kitchen-basic-assets-2026-10-16-v6-option-b/`;
- immutable review page: `public/keeper-review/kitchen-basic-assets-v6-option-b/`.

Runtime sprites, manifests, Final, V5, the calibration set and approved Keeper
sources are hash-protected and unchanged. Rejection is reversible by discarding
only the new Option B V6 directories and records.

## Verification

- deterministic rebuild digest, identical across two consecutive runs:
  `a8786816c568dbc37bda21b20658127afd811f8739773ac29ad30657c7277741`;
- `npm run verify:kitchen-basic-assets-v6-option-b` passes;
- `npm test` passes: 18 test files and 179 unit tests, plus all repository
  asset/review verifiers;
- `npm run typecheck` and `npm run build` pass;
- `git diff --check` passes;
- review media is content-addressed and absent from the public page directory;
- production deployment and page loading are verified after the delivery commit.

No Keeper animation record needed editing: the V6 page references the existing
unchanged sitting, cupboard and oven evidence only. `README.md`, this hand-back,
the durable decisions log and the reusable recipe are the affected documentation
set; other setup, architecture, deployment and backlog guidance remains accurate.
