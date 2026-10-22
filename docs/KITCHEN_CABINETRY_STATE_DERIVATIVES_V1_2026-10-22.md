# Kitchen cabinetry state derivatives V1

**Date:** 22 October 2026  
**Status:** exact V4 fitted-state visual authority approved by Frank;
production extraction, animation and runtime remain closed

## Approved visual authority

The exact V4 review sheet approved by Frank is preserved at
`art/drafts/kitchen-cabinetry-state-derivatives-2026-10-22-v1/candidate-v4-red-fault-lights-fridge-leak.png`.
It is the byte-exact `1024 × 1536` RGB
`exec-f6e9efc2-a481-44a1-9d33-e43a6266938a.png`, SHA-256
`d53b7565558acf6dc5544dde8b415fe50ac9eec1683eb374d996114ad5a902e8`.

The sheet reads in pairs:

1. Sink On / Broken;
2. Dishwasher On / Broken;
3. Oven Off / Broken;
4. Fridge standard Off/On / Broken.

The approved body authority remains
`art/source/kitchen-cabinetry-foundation-2026-10-22-v1/cabinetry-module-construction-sheet-approved.png`
and is displayed beside the state authority in the review tool. Frank confirmed
the exact V4 sheet on 22 October 2026. This approval covers the depicted state
art and the state semantics below; it does not approve extracted sprites,
animation, registration or runtime wiring.

## Complete fitted-state definition

- Cupboard and drawers are static.
- Sink Off is the approved dry body; On adds the spout stream; Broken adds the
  floor flood.
- Dishwasher Off uses the three fixed lamp housings dark; On uses the same
  housings steady green; Broken opens across the complete lower hinge, reveals
  restrained crockery, leaks water and flashes all three lamps red using three
  independent deterministic irregular schedules.
- Oven Off has a dark indicator and cavity; On is the approved lit body and
  food; Broken is slightly ajar with the burnt version of that food and separate
  flashing cavity/red-lamp layers.
- Fridge Off and On are identical with no light; Broken uses the selected
  sagging-door geometry, restrained contents and a separate water leak.

Every indicator fill, moving door and water effect must be extracted as a
same-canvas transparent layer. Repair cancels every animation and removes every
effect before the repaired state is displayed.

## What remains before production

The approved V4 sheet is a visual state authority, not a sprite atlas. Production still
requires exact transparent extraction from the approved body family, alignment
and re-composition tests, logical footprint/native-scale proofs, isolated
indicator schedules and isolated water layers. No runtime, collision,
interaction, placement or production selector has changed.

Approval record:
`docs/review/kitchen-cabinetry-state-derivatives-v1-approval-2026-10-22.json`.

Review route:
`/keeper-review/kitchen-cabinetry-state-derivatives-v1/index.html`.
