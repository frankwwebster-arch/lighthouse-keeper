# Kitchen basic assets V5: Codex → Claude hand-back

**Date:** 16 October 2026

**Status:** review-only reversible draft; not approved, promoted or wired

**Projection:** `flat-cutaway-v1`

**Review page:** `/keeper-review/kitchen-basic-assets-v5/`

V5 replaces the rejected perspective treatment for review purposes only. The
live game, Keeper animations, production sprites, manifests and registers are
unchanged. V1–V4 remain immutable.

## What V5 establishes

- The camera is straight-on. Functional fronts are true rectangles, with
  parallel vertical and horizontal edges, no vanishing point and no runtime
  depth scaling.
- The room is 56 lp high with an exact 5-lp visible floor band. The 21×56-lp
  centre modules repeat without stretching from 6 to 12 bays. Nine bays remain
  193 lp wide and twelve bays remain 256 lp wide, including the 4-lp door
  datum.
- Every one-bay object occupies a measured 20 lp of its 21-lp cell, leaving a
  transparent half-lp gutter on each side. Adjacent objects therefore fill the
  run without V-shaped perspective gaps.
- Counter, hob and table contact is 19 lp. The chair seat contact is 11 lp.
  Back-wall top cues are 0–1 lp; the freestanding table cue is 2 lp.
- The under-counter fridge is visibly freestanding, not disguised as an
  integrated cabinet.
- The chair is on the player/camera side of the table. The required draw stack
  is chair behind, Keeper central, table/apron foreground, then pet bowl. The
  table apron hides the Keeper's lower body so his boots read beneath the
  table.
- The cleaning-cupboard frame lies on the right side wall. Closed, the leaf is
  edge-on. During opening its orthographic projected width is 1, 8, 22 then
  34 lp while its real 34×52-lp dimensions, height and right hinge remain
  invariant. Fully open, the opaque rectangular leaf extends left as the
  foreground occluder.

## Measured assets

All bounds are maximum alpha bounds at density 4. Interaction coordinates are
absolute screen X positions in Keeper units for the 193-lp starting kitchen.
For the two-bay table, the chosen seat/place point is 10.5 lp left of the
two-bay centre, which is permitted by the room contract.

| Item | Cell (lp) | Measured bound (lp) | Bays | Interaction X (ku) | Contact / note |
| --- | ---: | ---: | ---: | ---: | --- |
| Pedal bin | 21×16 | 20×14 | 1 | 116 | floor; `standard/full/overflowing` |
| Freestanding fridge | 21×21 | 20×19 | 1 | 284 | worktop 19; `standard/on/broken` |
| Kettle unit | 21×31 | 20×30 | 1 | 452 | worktop 19; `standard/on/broken` |
| Toaster unit | 21×31 | 20×30 | 1 | 620 | worktop 19; `standard/on/broken` |
| Basic cooker | 21×28 | 20×26 | 1 | 788 | 19-lp body/hob; splashback to 26; `standard/on/broken` |
| Mixer unit | 21×31 | 20×30 | 1 | 956 | worktop 19; clear stand mixer; `standard/on/broken` |
| Sink unit | 21×29 | 20×27 | 1 | 1,124 | worktop 19; three dishes overlays; `standard/on/broken` |
| Table + player-side chair | 42×28 | 40×26 | 2 | 1,292 | table 19; seat 11; standard only |
| Pet bowl | 16×8 | 12×3 | table child | 1,440 | foreground; `standard/full/broken` |
| Cupboard leaf | 38×56 review cell | 34×52 open | fixed far cap | 1,512 | right hinge; 1/8/22/34-lp projected widths; no broken state |

The starting order is bin, fridge, kettle, toaster, cooker, mixer, sink, then
the two-bay table. The pet bowl is the table's foreground child. The side-wall
cupboard is fixed in the far cap, takes no bay and is always last.

## Requested confirmations

### 19-lp oven door

Confirmed for this draft. Both unchanged rear retrieval clips still read with
the cooker constrained to the 19-lp body/door datum. The cake retrieval remains
especially clear, so V5 does not widen the oven as a workaround.

### Cupboard occlusion and lifecycle

Confirmed for this draft. The fully open 34×52-lp rectangular foreground leaf
hides the 19-lp rear Keeper core, boots and the broom/basic-hoover prop-swap
route. The lifecycle shown on the page is:

1. closed leaf is edge-on against the right side wall;
2. right hinge stays fixed while the leaf opens left;
3. unencumbered Keeper walks behind the leaf and becomes hidden;
4. he emerges already in the selected cleaning activity while the leaf stays
   open;
5. he returns behind it to put the item away;
6. he emerges in the standard walk; and
7. the leaf closes automatically only after he is clear.

No turn animation while holding the broom is required.

## Table animation record

`keeper_sit_back` is the correct approved geometry proof: its recorded seat
point is 10.67 lp above the floor, within tolerance of the 11-lp chair datum.
`keeper_lean_table_back` is a standing rear-facing reach, not a seated loop.
V5 therefore uses the final rear sit pose for spatial review and records a
future reusable seated rear-facing arm overlay as the only table-animation
gap. It does not modify or invent a Keeper clip.

## Reversible files and verification

- Sources: `art/source/kitchen-basic-assets-2026-10-16-v5/`
- Raw density-4 strips and shell pieces:
  `art/raw/kitchen-basic-assets-2026-10-16-v5/`
- Catalogue, review data and SHA-256 register:
  `art/drafts/kitchen-basic-assets-2026-10-16-v5/`
- Immutable review page: `public/keeper-review/kitchen-basic-assets-v5/`
- Builder: `scripts/build_kitchen_basic_assets_v5.py`
- Verifier: `scripts/verify_kitchen_basic_assets_v5.mjs`

The builder was run twice with a byte-identical aggregate output hash. The
verifier checks density/cell geometry, frame gutters, measured bounds, the
exact 5-lp floor band, 19/11-lp contacts, projection metadata, unchanged scale
between bays, rectangular door rows, fixed hinge/door widths, preload/decode
gating, archive hashes and the absence of runtime outputs.
