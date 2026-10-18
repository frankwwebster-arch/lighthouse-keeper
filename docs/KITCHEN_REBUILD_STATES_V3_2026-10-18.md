# Kitchen Rebuild States V3 — reusable effect workbench

Date: 18 October 2026
Status: reversible review draft; no Final/runtime promotion

V3 supersedes V2 as the active visual-review gate. It preserves V2's coherent
state objects except for three measured corrections: the broken toaster and
basin regain source headroom, the table/chair are normalized to the canonical
room datums, and the broken oven warning/cavity flicker is pinned to the exact
On-state lamp and cavity coordinates.

## Furniture datums

- one-person table width: 80 px / 20 lp;
- tabletop top: room y=150 / 14.5 lp above the foot line;
- rear-chair seat support: room y=177 / 7.75 lp above the foot line;
- common furniture foot line: room y=208.

## Effect library

Objects remain static wherever possible. Environmental motion is stored only
in isolated 40-frame, 4-fps, ten-second strips with transparent gutters. Ten
families are available: kettle On steam, toaster On heat, basin On flow,
fridge broken drip/ripple, kettle broken steam, toaster broken smoke, oven
broken smoke, oven broken warning/cavity flicker, basin broken spray and the
approved bin smell. Every family offers three animated models. The approved
V31 bin-smell pixels remain exact inside the common editable cell.

The review workbench can choose a model, drag, resize, crop from four sides,
nudge by one pixel (four with Shift), persist settings in browser storage, and
copy or download implementation-ready placement JSON. Transform data remains
separate from sprite strips, so placement changes never modify source art.

## Source provenance

- User-supplied richer effect source: `art/source/kitchen-rebuild-states-2026-10-18-v3/generated/user-approved-broken-effects.png`, SHA-256 `75899da25b94494545263afbd49b17663c93442725d6043e9bb9782f1f1c41ee`.
- Table/chair source: built-in image generation in precise-object-edit mode,
  then deterministically normalized to the datums above. Source path:
  `art/source/kitchen-rebuild-states-2026-10-18-v3/generated/canon-height-table-chair-source.png`, SHA-256 `6e60ddfe6ba9c205618dbdb4404f6f4b31d2a612ae5b884482ae07ff7b6086a1`.

Build with `python scripts/build_kitchen_rebuild_states_v3.py`. Verify with
`npm run verify:kitchen-rebuild-states-v3`. The review route is
`/keeper-review/kitchen-rebuild-states-v3/`.
