# Kitchen V17 exact V5 rollback: Codex → Claude hand-back

**Date:** 17 October 2026

**Status:** review-only reversible draft; not approved, promoted or wired

**Review page:** `/keeper-review/kitchen-v5-exact-rollback-v17/`

## Hand-back

V17 is the complete, byte-exact rollback to Kitchen V5 requested by Frank.
There is no reconstructed countertop, double fascia, Option-B layer or other
redraw. V6–V16 remain rejected historical review sets and must not be used as
the current kitchen authority.

The only permitted V5→V17 metadata difference is the versioned review URL
prefix. The raw files, review-image bytes, state/frame records, bounds, bays,
anchors, interaction points, room pieces and room compositions are otherwise
identical.

## Preserved measured bounds, bays and interaction spots

Bounds are maximum alpha bounds at density 4. Interaction X values are
absolute screen positions in Keeper units for the 193-lp starting kitchen.

| Item | Cell (lp) | Measured bound (lp) | Bays | Interaction X (ku) | Preserved state/contact record |
| --- | ---: | ---: | ---: | ---: | --- |
| Pedal bin | 21×16 | 20×14 | 1 | 116 | floor; `standard/full/overflowing` |
| Freestanding fridge | 21×21 | 20×19 | 1 | 284 | worktop 19; `standard/on/broken` |
| Kettle unit | 21×31 | 20×30 | 1 | 452 | worktop 19; `standard/on/broken` |
| Toaster unit | 21×31 | 20×30 | 1 | 620 | worktop 19; `standard/on/broken` |
| Basic cooker | 21×28 | 20×26 | 1 | 788 | 19-lp body/hob; splashback to 26; `standard/on/broken` |
| Mixer unit | 21×31 | 20×30 | 1 | 956 | worktop 19; `standard/on/broken` |
| Sink unit | 21×29 | 20×27 | 1 | 1,124 | worktop 19; three dishes overlays; `standard/on/broken` |
| Table + player-side chair | 42×28 | 40×26 | 2 | 1,292 | table 19; seat 11; standard only |
| Pet bowl | 16×8 | 12×3 | table child | 1,440 | foreground; `standard/full/broken` |
| Cupboard leaf | 38×56 review cell | 34×52 open | fixed far cap | 1,512 | right hinge; 1/8/22/34-lp projected widths; no broken state |

The order remains bin, fridge, kettle, toaster, cooker, mixer, sink and the
two-bay table. The pet bowl remains the table's foreground child. The cupboard
remains fixed in the far cap, takes no bay and is always last.

## Preserved room and interaction conclusions

- Shell: 56 lp high with an exact 5-lp visible floor band.
- Repeat: exact 21 × 56-lp centre section; valid unchanged from 6–12 bays.
- Nine bays: 193 lp including the 4-lp door datum.
- Twelve bays: 256 lp including the 4-lp door datum.
- Ordinary one-bay objects retain a 20-lp measured width inside each 21-lp
  cell, with a transparent half-lp gutter on both sides.
- Cooker: the unchanged rear retrieval clips remain readable with the 19-lp
  oven body/door; the cake retrieval remains clear.
- Cupboard: the fully open 34 × 52-lp right-hinged rectangular leaf extends
  left and hides the Keeper, boots and tool swap. It stays open during the
  cupboard activity, then closes after the Keeper returns the item and emerges
  in the standard walk.
- Table: the chair remains on the camera side and the Keeper sits rear-facing;
  `keeper_sit_back` retains its 10.67-lp seat point against the 11-lp chair
  datum. The table apron hides his lower body so his feet read beneath it.

## Reversible files

- Recipe: `data/kitchen_v5_exact_rollback_v17_recipe.json`
- Raw exact copy: `art/raw/kitchen-v5-exact-rollback-2026-10-17-v17/`
- Review data, copy map and register:
  `art/drafts/kitchen-v5-exact-rollback-2026-10-17-v17/`
- Immutable review page:
  `public/keeper-review/kitchen-v5-exact-rollback-v17/`
- Archive set: `review-archive/sets/kitchen-v5-exact-rollback-v17.json`
- Builder: `scripts/build_kitchen_v5_exact_rollback_v17.py`
- Verifier: `scripts/verify_kitchen_v5_exact_rollback_v17.mjs`

## Verification and delivery

Delivered content commit: `b8d5708`

Kitchen deployment marker: `fc2fbe6`

Production review:
`https://lighthouse-keeper-mu.vercel.app/keeper-review/kitchen-v5-exact-rollback-v17/`

Verified after archive and before release:

- focused exact-copy verifier: passed;
- raw V5/V17 trees: 94 files, identical relative paths and SHA-256 values;
- archived review media: 153 images, identical byte counts, SHA-256 values and
  content-addressed objects to V5;
- asset families: 10;
- room pieces: stair cap, repeat, far closed and far open;
- room compositions: nine bay and twelve bay;
- full repository suite: 18 test files and 179 tests passed;
- runtime, Keeper, Final and production sprite manifests: unchanged;
- production page: HTTP 200;
- production nine-bay room image: resolver HTTP 307 to the immutable archive,
  then HTTP 200 with SHA-256
  `97692918da57cbebd37daf1e129a0544e4edf97bf2e9c2bf796242d24751a6fd`,
  exactly matching the V5 source object.

Nothing in this hand-back approves, promotes or wires the art.
