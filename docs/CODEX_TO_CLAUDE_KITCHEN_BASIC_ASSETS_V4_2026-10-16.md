# Kitchen basic assets V4: Codex → Claude hand-back

_16 October 2026. Reversible tier-1 review draft only. Nothing in this batch is approved, promoted, registered with the game, or wired into runtime behaviour._

## Result

V4 supersedes V3 **for review only** and leaves V1–V3 and the live game unchanged. It makes Frank's final cupboard correction while retaining the accepted V3 full-bay furniture, freestanding fridge, table layering, room widths and oven proof.

Review page: `/keeper-review/kitchen-basic-assets-v4/`

The cleaning-cupboard leaf is now a strict front-elevation rectangle: parallel sides, horizontal top and bottom, no trapezoidal depth, no foreshortening and no visible side edge. It is hinged on the right, extends left when open and stays in front of the Keeper. Only the handle projects visually from the door face.

## Measured geometry and interaction spots

All V4 art is density 4. One bay is 21 lp / 168 ku. The 9-bay room is 193 × 56 lp and the 12-bay reservation is 256 × 56 lp. Bounds are the largest measured alpha bounds across every state after constraint to the declared envelope.

| Item | States | Largest measured bound | Bays | Relative interaction | 9-bay interaction |
| --- | --- | ---: | ---: | ---: | ---: |
| Full-bay pedal bin | `standard`, `full`, `overflowing` | 20 × 14 lp | 1 | 0 ku | 116 ku |
| Freestanding under-counter fridge | `standard`, `on`, `broken` | 20 × 19 lp | 1 | 0 ku | 284 ku |
| Full-bay kettle counter | `standard`, `on`, `broken` | 20 × 30 lp | 1 | 0 ku | 452 ku |
| Full-bay toaster counter | `standard`, `on`, `broken` | 20 × 30 lp | 1 | 0 ku | 620 ku |
| Full-bay basic oven | `standard`, `on`, `broken` | 20 × 26 lp | 1 | 0 ku | 788 ku |
| Full-bay mixer counter | `standard`, `on`, `broken` | 20 × 30 lp | 1 | 0 ku | 956 ku |
| Full-bay sink unit | `standard`, `on`, `broken`; dishes 1–3 overlays | 20 × 27 lp | 1 | 0 ku | 1,124 ku |
| Layered table for one + chair | `standard` | 40 × 26 lp | 2 | 0 ku (two-bay centre) | 1,376 ku |
| Pet bowl | `standard`, `full`, `broken` | 12 × 3 lp | 0; table foreground child | 0 ku | 1,376 ku |
| Front-on cleaning cupboard | `standard`, `on`, `open` | 36 × 52 lp | 0; far-wall cap | −84 ku | 1,460 ku |

At 12 bays the cupboard interaction moves with the far wall to 1,964 ku. The open door leaf itself is a measured **34 × 52 lp** rectangle inside its 38 × 56 lp layer cell.

## Cupboard geometry and complete activity lifecycle

The review uses three independent depth roles:

1. `obj_cupboard_recess_f1`, z=20, the shallow frontal recess;
2. the unchanged Keeper clip, z=50 behind the leaf during entry and put-away, or z=90 while active/exiting in the room;
3. `obj_cupboard_leaf_open_f1`, z=80, the 34 × 52 lp flat rectangular foreground occluder.

The five review panels document the intended lifecycle:

1. the door opens and the unencumbered Keeper walks behind it using the existing rear-facing portion of `keeper_walk_into_lift`;
2. the door remains open while `keeper_sweep_broom` or `keeper_hoover_basic` runs outside the cupboard;
3. the Keeper returns behind the still-open leaf, hiding both body and tool while the tool is put away;
4. he emerges using the unchanged standard `keeper_walk`, with no turn animation and no tool;
5. the door closes automatically only after the Keeper is clear.

This means no broom/hoover appears beneath the door, no loaded turn animation is required, and the door does not close prematurely during the activity.

## Retained V3 decisions

- Every one-bay item occupies 20 lp of its 21-lp cell; there are no decorative inter-item gaps.
- The fridge remains a visibly freestanding under-counter appliance, not an integrated cabinet.
- The table remains chair z=35, unchanged `keeper_sit_back` z=50, table z=60. The seat contact is 10.67 lp above the floor; table surface is 17 lp, underside 15 lp, and the boots read beneath the table.
- Both unchanged oven retrieval clips still read against the 19-lp door and 10-lp rack datum.
- The stair cap, 21 × 56 lp repeat sections and far-wall cap still assemble cleanly from 6–12 bays. The 9-bay kitchen remains in the agreed order and the cupboard is always last; the 12-bay page remains an outline only.

## Sources, provenance and reversibility

The built-in image generator was used in precise-object-edit mode only for the V4 door leaf. The prompt required a single isolated, full-height walnut leaf in exact orthographic front elevation, a true rectangular silhouette, right-edge hinges, a left-side brass handle, no perspective, no foreshortening, no visible thickness, transparent surroundings and the approved smooth navy-outlined style. The generated colour surface is fitted to a deterministic 34 × 52 lp opaque rectangle so automated verification rejects any tapered row.

Sources and copied V3 direction references are in `art/source/kitchen-basic-assets-2026-10-16-v4/`. Raw density-4 drafts are in `art/raw/kitchen-basic-assets-2026-10-16-v4/`. Exact SHA-256 values for every accepted source and output are recorded in `art/drafts/kitchen-basic-assets-2026-10-16-v4/batch-register.json`.

Rejection is reversible by deleting the three V4 art directories, the V4 review page/archive set, the V4 builder/verifier and this note. V1–V3, production sprites, manifests, registers, animation files and game wiring are unchanged.

## Verification and documentation audit

The deterministic V4 verifier checks density and strip geometry, transparent inter-frame gutters, 6–12-bay shells, 20-lp one-bay occupancy, table/cupboard layer assets, fridge identity, oven clips, review preloading, archive hashes and source/register hashes. It additionally checks every opaque row of the open leaf has the same x extent, proving the leaf is rectangular rather than trapezoidal.

Browser QA before archival decoded all 48 page images, enabled all 10 state controls and both selectors, and confirmed the five-step cupboard loop renders in the specified depth order. `README.md`, runtime manifests, Keeper registers and live-game documentation need no change because V4 remains review-only with no runtime effect; this document is the fresh continuation point.

Post-archive verification passed with 167 content-addressed V4 review references. The complete repository suite passed 18 test files / 179 tests, and the production Next.js build completed successfully.
