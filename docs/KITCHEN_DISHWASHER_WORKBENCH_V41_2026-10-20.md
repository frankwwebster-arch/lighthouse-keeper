# Kitchen Dishwasher Workbench V41

V41 is the reversible behaviour successor to Dishwasher V40. It changes no
art pixels. It applies the canonical rule that every movable kitchen asset is
position-locked while Broken and that environmental effects are stored as
asset-owned local layers.

Status: approved by Frank on 20 October 2026; exact review/specification bytes
pinned by `docs/review/kitchen-dishwasher-workbench-v41-approval-2026-10-20.json`;
unpromoted and not runtime-wired.

Review: `/keeper-review/kitchen-dishwasher-workbench-v41/`

## Broken-state rule

When the dishwasher is Broken:

- dragging the dishwasher is rejected;
- selecting another bay for it is rejected;
- dropping another unit onto its bay is rejected because that would displace
  the dishwasher;
- rotating the complete run is rejected because it includes a locked asset;
- exact bay origin, Prime midpoint and active healed joins remain unchanged.

Changing the dishwasher to Off or On represents repair and unlocks movement.
Returning it to Broken locks its new exact snapped position. The same contract
applies to the fridge, oven, sink and every later movable kitchen asset when
their runtime state families are wired.

## Effect ownership

Suds remain separate reusable forty-frame, 4-fps, ten-second strips. Each
placed layer now explicitly records `anchorAssetId: dishwasher`, state and its
local transform. Model, speed, offset, size, crop and removal remain editable.
This data model also applies to oven smoke, fridge water and later fault
effects: the effect is not baked into the object, but cannot drift away from
its owner.

## Art and runtime boundary

All 49 V41 image files are required to be byte-identical to V40. V40 remains
immutable. The current game has no kitchen furniture/state controller, so V41
does not claim runtime wiring; the review and
`KITCHEN_MODULAR_ASSET_AND_JOIN_STANDARD_2026-10-20.md` are the tested contract
for that later implementation. Final assets and approved cabinetry are
unchanged.

## Verification

Run:

```sh
npm run verify:kitchen-dishwasher-workbench-v41
```

The verifier checks all 49 V41 assets against V40 hashes, tests direct lock,
swap displacement rejection and repair unlocking, checks asset-local effect
metadata and validates the content-addressed review manifest.
