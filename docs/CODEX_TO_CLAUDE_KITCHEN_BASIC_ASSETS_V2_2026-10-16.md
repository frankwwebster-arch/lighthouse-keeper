# Kitchen basic assets V2: Codex → Claude hand-back

_16 October 2026. Reversible tier-1 review draft only. Nothing in this batch is approved, promoted, registered with the game, or wired into runtime behaviour._

## Result

V2 supersedes V1 **for review only** and leaves V1 unchanged. It keeps Frank's accepted widths and cake-from-oven staging, while redrawing the shell and furniture at native density 4 in the smoother, detailed style of the two supplied concept sheets and the approved Keeper.

Frank's follow-up decisions are incorporated:

- the fridge is a clearly freestanding under-counter appliance, not an integrated cabinet; its enamel case, gasket seam, handle, feet, vent and side gaps remain visible beneath a removable wood top;
- the cleaning-cupboard door and opening run from floor to lintel; the Keeper can walk completely inside, be wholly hidden with broom or hoover, then walk forwards out facing the opposite direction and already sweeping;
- the chair seat is fixed from the recorded `keeper_eat_seated` contact, not inferred from the standing counters;
- the table surface is 17 lp, below the 19-lp standing worktops.

Review page: `/keeper-review/kitchen-basic-assets-v2/`

## Measured geometry

All art is density 4. One bay is 21 lp / 168 ku. The 9-bay room is 193 × 56 lp and the 12-bay reservation is 256 × 56 lp. The cupboard remains part of the far-wall cap and is always last.

The bounds below are the largest measured alpha bounds across the item's supplied states after constraining every state to its declared envelope. Interaction positions are absolute in the composed 9-bay room; offsets remain relative to each object's bay origin in the catalogue.

| Item | States | Largest measured bound | Bays | 9-bay interaction | Relative interaction |
| --- | --- | ---: | ---: | ---: | ---: |
| Pedal bin | `standard`, `full`, `overflowing` | 13 × 14 lp | 1 | 116 ku | 0 ku |
| Freestanding under-counter fridge | `standard`, `on`, `broken` | 15.75 × 19 lp | 1 | 284 ku | 0 ku |
| Kettle counter unit | `standard`, `on`, `broken` | 19 × 30 lp | 1 | 452 ku | 0 ku |
| Toaster counter unit | `standard`, `on`, `broken` | 19 × 30 lp | 1 | 620 ku | 0 ku |
| Basic oven | `standard`, `on`, `broken` | 19 × 26 lp | 1 | 788 ku | 0 ku |
| Mixer counter unit | `standard`, `on`, `broken` | 19 × 30 lp | 1 | 956 ku | 0 ku |
| Sink unit | `standard`, `on`, `broken`; dishes 1–3 overlays | 19 × 27 lp | 1 | 1,124 ku | 0 ku |
| Table for one + chair | `standard` | 38 × 26 lp | 2 | 1,292 ku (chair-side choice) | −84 ku |
| Pet bowl | `standard`, `full`, `broken` | 12 × 3 lp | 0; foreground child of table | 1,376 ku | 0 ku |
| Full-height cleaning cupboard | `standard`, `on`, `open` | 34 × 52 lp | 0; far-wall cap | 1,460 ku | −84 ku |

At 12 bays the cupboard interaction moves with the far wall to 1,964 ku. The pet bowl remains a foreground child of the table and consumes no bay.

## Table and chair evidence

`art/raw/keeper-first-batch/keeper_eat_seated_f8.json` records a 34 × 41 lp clip at density 4, floor anchor `[17, 40]`, `seatPoint` y 29.39 and `handUsePoint` y 17.27. Therefore:

- seat contact above floor = `40 − 29.39` = **10.61 lp**;
- every frame's boot alpha ends on logical floor y 40;
- V2 chair seat = **11 lp**;
- chair back top = **26 lp**;
- table surface = **17 lp**;
- table top thickness = **2 lp** and underside/knee clearance = **15 lp**.

The review overlay shows the approved seated Keeper, chair, table, seat datum, table datum and floor together. His feet meet the floor while seated.

## Required review answers

1. **Do the oven clips read with a 19-lp oven door?** Yes at draft stage. Both existing `keeper_cake_from_oven_back` and `keeper_meal_from_oven_back` are shown against the same 19-lp V2 door and 10-lp rack datum. Frank's accepted cake staging is unchanged.
2. **Does the far-wall cupboard hide the Keeper with the broom?** Yes. The middle proof frame places a broom-carrying Keeper behind the complete closed density-4 leaf; the leaf is in the foreground, reaches the floor and fully hides Keeper, boots and tool. The open frames show the forward entry and the opposite-facing forward exit already sweeping. The same closed leaf also covers the basic-hoover silhouette.
3. **Room door direction.** Retain the outward-into-stairwell proposal with a 4-lp / 32-ku clear area. This batch changes no approved transition and does not promote that proposal.

## Modular shell and layout

- stair-side cap: 46 × 56 lp, outward-open and outward-closed drafts;
- repeat section: 21 × 56 lp, three density-4 variants;
- far-wall cap: 38 × 56 lp, complete closed leaf and open state;
- verified assembled widths: every whole width from 6 through 12 bays;
- composed start: 9 bays in the final order from bin through table, with the cupboard last;
- upgrade outline: 12 bays with the reserved tier-3 footprints only; no higher-tier object was drawn.

## Sources, provenance and reversibility

Generated sources live in `art/source/kitchen-basic-assets-2026-10-16-v2/generated/`; the two supplied direction sheets are copied into `reference/`. The first integrated-fridge attempt is preserved only in `rejected/obj_fridge_integrated_rejected_source.png`; it is absent from all raw art and the review page.

Image generation used the built-in image tool in two prompt families:

- `stylized-concept`: isolated density-4 kitchen objects and shell pieces, transparent background, warm wood/cream/brass/teal palette, smooth antialiased contours, soft material shading, side-on Lighthouse Keeper proportions, no text and no neighbouring furniture;
- `precise-object-edit`: the replacement fridge, explicitly freestanding with exposed enamel casing, recognisable appliance seams/handle/feet/vent/side gaps and no cabinet front.

Exact SHA-256 values for every accepted source, V1/V2 output and review file are in `art/drafts/kitchen-basic-assets-2026-10-16-v2/batch-register.json`. Rejection is reversible by deleting the three V2 art directories, the V2 review directory/set and the V2 builder/verifier; V1 and production remain unchanged.

## Verification and documentation audit

The deterministic V2 verifier checks density and strip geometry, transparent inter-frame gutters, 6–12-bay shell sizes, table datums, freestanding-fridge presence, full-height cupboard bounds/occlusion wiring, both oven clips, review preloading, archive hashes and source/register hashes.

Documentation audit: `README.md`, the live asset manifests, Keeper registers and game wiring remain accurate because this is a review-only draft and changes none of them. The original Claude brief and V1 hand-back remain historical records; this note is the only current V2 continuation point.
