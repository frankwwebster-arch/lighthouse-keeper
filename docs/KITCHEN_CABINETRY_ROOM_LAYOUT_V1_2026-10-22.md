# Kitchen Cabinetry Room Layout V1

**Date:** 22 October 2026
**Status:** deployed review workbench; visual approval and production promotion
remain closed

## Purpose

This workbench places the newly approved high-resolution fitted kitchen family
inside the fixed `772 × 224` logical room. It answers the next concrete review
question: do the approved units sit together cleanly when they are independently
movable, or does the fitted run still need occupancy-derived join healing?

Review route:
`/keeper-review/kitchen-cabinetry-room-layout-v1/index.html`.

## Exact inputs

- Approved cabinetry/body foundation:
  `art/source/kitchen-cabinetry-foundation-2026-10-22-v1/cabinetry-module-construction-sheet-approved.png`,
  SHA-256
  `898c212690c2db8a52a6c8ea7bd962afcf12c1df8e577dcc98c4508359cccee3`.
- Approved fitted-state visual authority:
  `art/drafts/kitchen-cabinetry-state-derivatives-2026-10-22-v1/candidate-v4-red-fault-lights-fridge-leak.png`,
  SHA-256
  `d53b7565558acf6dc5544dde8b415fe50ac9eec1683eb374d996114ad5a902e8`.

Neither input is modified. Fourteen review-only transparent crops are generated
under `art/drafts/kitchen-cabinetry-room-layout-2026-10-22-v1/assets/`.
Each crop retains the source drawing inside a declared outer silhouette while
removing the source sheet's dark presentation backdrop. The sink tap and loose
water silhouettes use source-colour-connected masks; no object is redrawn.

## Fixed geometry and movement

Every module body is registered to the existing game geometry:

- bay width: `84` logical pixels;
- body: `84 × 74` logical pixels;
- body top: room `y=134`;
- baseline: room `y=208`;
- legal origins: `x=84, 168, 252, 336, 420, 504`.

Dragging previews freely but commits by swapping two exact bays. The ordered
layout, selected states and zoom persist in browser storage. Broken sink,
dishwasher, oven and fridge states retain the existing movement rule: a Broken
unit cannot move or be displaced until it is repaired.

The state controls expose Sink Off/On/Broken, Dishwasher On/Broken, Oven
On/Off/Broken and Fridge Standard/Broken. Dishwasher Off remains a declared
approved semantic—three dark housings—but no separate dark-lamp high-resolution
render exists yet. The workbench says this explicitly rather than inventing or
silently repainting an unapproved state.

## Raw versus healing comparison

The two room views are synchronized:

1. **Raw approved modules** draws only the exact review crops.
2. **Join-only diagnostic** draws the same crop bytes and positions, then adds a
   deliberately narrow internal countertop/plinth seam cover.

The second view is diagnostic, not proposed final art. It exists to reveal
whether healing is needed and how narrowly it can be scoped without repeating
the earlier broad overlay that damaged the hob. If healing is retained, the
production implementation must still follow the existing contract: derive the
continuous worktop, rear edge, exposed ends and plinth from occupancy at master
resolution rather than painting correction strips over finished appliances.

## Zoom and loading

The renderer offers `1×`, `2×` and `4×`. For every view it sizes the canvas
backing surface from logical dimensions × zoom × device-pixel ratio and draws
the high-resolution crops directly. It never creates or enlarges a `1×`
intermediate room raster. All fourteen image files are loaded and decoded before
movement or state controls unlock.

## Review boundary

This workbench does not approve its transparent extraction masks, join overlay,
state registration, animations or room integration as production art. It does
not change runtime selectors, placement, collision, gameplay or canonical
sprites. Rejection is reversible by discarding this one versioned draft and
review route.
