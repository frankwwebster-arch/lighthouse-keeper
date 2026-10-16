# Kitchen basic assets V3: Codex → Claude hand-back

_16 October 2026. Reversible tier-1 review draft only. Nothing in this batch is approved, promoted, registered with the game, or wired into runtime behaviour._

## Result

V3 supersedes V2 **for review only** and leaves V1, V2 and the live game unchanged. It implements Frank's correction in three places:

- the cleaning cupboard is straight ahead in the right end wall of the dollhouse view, not shown as a side corridor;
- every bay-backed item occupies a measured 20 lp of its 21-lp bay, leaving only the required 0.5-lp transparent safety gutter at each side;
- the table is a three-layer composition: chair behind, the existing approved rear-facing Keeper sit clip in the middle, and the table in front, so his boots read beneath the table.

Review page: `/keeper-review/kitchen-basic-assets-v3/`

## Measured geometry and interaction spots

All V3 art is density 4. One bay is 21 lp / 168 ku. The 9-bay room is 193 × 56 lp and the 12-bay reservation is 256 × 56 lp. The bounds below are the largest measured alpha bounds across all states after constraint to the declared envelope.

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

At 12 bays the cupboard interaction moves with the far wall to 1,964 ku. The pet bowl remains a foreground child of the table and consumes no bay.

## Table and chair layering

The existing `keeper_sit_back` record is 34 × 40 lp at density 4, faces back, has floor anchor y=40 and seatPoint y=29.33. Its measured contact is therefore **10.67 lp above the floor**, matching the authoritative 11-lp chair seat.

The review page composes:

1. `obj_table_chair_back_f1`, z=35;
2. the unchanged approved `keeper_sit_back`, z=50;
3. `obj_table_foreground_f1`, z=60.

The table surface is 17 lp, its top is 2 lp thick, the underside is 15 lp and the table spans 40 lp inside its 42-lp allocation. The apron hides the thighs while the boots remain visible between the outer legs. No Keeper animation was created or changed. `keeper_eat_seated` remains the existing side-facing meal clip; V3 recommends the recorded back-facing sit for the seated/rest composition and does not silently invent a rear-facing eating clip.

## Cupboard correction and required answer

The cupboard is now explicitly split into:

- `obj_cupboard_recess_f1`, z=20, a frontal shallow recess in the straight-ahead right end wall;
- unchanged Keeper entry/action clips, z=50;
- `obj_cupboard_leaf_open_f1`, z=80, a full-height opaque outward-opening foreground leaf.

The closed state is also a complete floor-to-lintel occluder. The unencumbered Keeper enters behind the leaf using the rear-facing portion of the existing `keeper_walk_into_lift` depth-walk clip. While fully hidden, the complete Keeper-plus-tool clip is selected. He then emerges already in `keeper_sweep_broom` or `keeper_hoover_basic`, moving into the room. **No turn animation while holding the broom is required.**

Required answer: **yes, the foreground leaf hides the Keeper, boots and tool.** The review page demonstrates the actual layer order rather than flattening the recess, Keeper and leaf into one image.

## Oven confirmation

Both unchanged `keeper_cake_from_oven_back` and `keeper_meal_from_oven_back` remain staged against the 19-lp oven-door datum and 10-lp rack. Both still read at draft stage; Frank's accepted cake retrieval is unchanged.

## Modular room and layouts

- stair-side cap: 46 × 56 lp, outward-open and outward-closed drafts retained from V2;
- repeat section: 21 × 56 lp, three retained V2 variants;
- far-wall cap: 38 × 56 lp, now with independent closed, recess and foreground-leaf assets;
- assembled shells: deterministically checked at every whole width from 6 through 12 bays;
- composed start: 9 bays in the agreed order, with the cupboard always last;
- upgrade outline: 12 bays with only the reserved tier-3 footprints; no tier-2 or tier-3 object was drawn.

## Sources, provenance and reversibility

The built-in image generator was used in `stylized-concept` and `precise-object-edit` modes. The accepted prompt families requested smooth antialiased navy contours, warm cream/walnut/brass/teal materials, orthographic dollhouse presentation, transparent backgrounds and isolated assets. The full-bay run prompt explicitly required a freestanding non-integrated fridge and equal worktop alignment. The cupboard prompt explicitly requested three separate assets: closed front, frontal recess and broad outward leaf. The table prompt explicitly requested chair/background and table/foreground pieces for composition around the approved rear sit.

Accepted source sheets and copied direction references are in `art/source/kitchen-basic-assets-2026-10-16-v3/`. Raw density-4 drafts are in `art/raw/kitchen-basic-assets-2026-10-16-v3/`. Exact SHA-256 values for accepted sources and outputs are recorded in `art/drafts/kitchen-basic-assets-2026-10-16-v3/batch-register.json`.

Rejection is reversible by deleting the three V3 art directories, the V3 review page/archive set, the V3 builder/verifier and this note. V1, V2, production sprites, manifests, registers, animation files and game wiring are unchanged.

## Verification and documentation audit

The deterministic V3 verifier checks density and strip geometry, transparent inter-frame gutters, 6–12-bay shells, 20-lp one-bay occupancy, table and cupboard layer assets, the recorded rear seat contact, fridge identity, both oven clips, review preloading, archive hashes and source/register hashes.

Browser QA before archival decoded all 43 page images, enabled all 10 state controls and both selectors, and confirmed the intended z orders for the table and cupboard. `README.md`, runtime manifests, Keeper registers and live-game documentation need no change because this remains a review-only draft with no runtime effect; this document is the fresh continuation point for V3.
