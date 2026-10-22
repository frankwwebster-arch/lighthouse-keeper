# Kitchen Complete Room Layout V5 — corrected fitted interfaces and cabinet-owned objects

Date: 23 October 2026

Status: rejected integration provenance; no runtime or production promotion

Review route: `/keeper-review/kitchen-complete-room-layout-v5`

## Outcome

V5 attempted to replace the rejected V4 healing result with a reversible countertop-interface candidate. Frank rejected the assembled result on 23 October 2026 because the model-generated unit shells still carried incompatible worktop/end geometry: the oven top, right-hand cabinet outline and sink/tap join remained visibly wrong. V5 is preserved as immutable provenance and presents three synchronized views:

1. the exact V4 drawings copied byte-for-byte into the V5 atlas;
2. the corrected high-resolution modules with no connector;
3. the same corrected modules with a small neighbour-derived fitted connector.

The oven/hob remains the required even deep blue. The sink's rear countertop datum is straight in its standard, On and Broken drawings. Every fitted body normalizes to exactly `420 × 370` source pixels and maps to the unchanged `84 × 74` room body. The six fitted origins remain `84, 168, 252, 336, 420, 504` and their exact centres remain `126, 210, 294, 378, 462, 546`.

## Cabinet-owned kettle and toaster

The kitchen grid contract is now `data/kitchen_room_grid_contract_v2.json`.

- The kettle and toaster belong to supporting cabinet identities, not room coordinates.
- Only the cupboard and drawers may own them.
- They must have distinct owners.
- Each object is always centered on its owner's current bay.
- Moving a cabinet visibly carries its owned object during the drag and after the swap.
- Dropping either object on the occupied standard cabinet swaps the two owners.
- The bin, table and chair continue to persist distinct floor-section IDs.
- Raw pointer coordinates are never stored.

The art support planes remain `y=141` for worktops and `y=208` for the floor. The Keeper stop/turn interaction plane remains `y=218`.

## Reversible sources

No approved source, V4 file or earlier generated attempt was overwritten.

Final V5 source sheets:

- `art/drafts/kitchen-countertop-interface-2026-10-22-v5/source/cabinetry-foundation-interface-hob-sink-corrected.png`

  SHA-256 `4b7c25ef2ea006225f465360479b73fac3ea2ab02650ea471a1fdb6f5fd35032`
- `art/drafts/kitchen-countertop-interface-2026-10-22-v5/source/cabinetry-states-interface-hob-sink-corrected.png`

  SHA-256 `6ab62d05bbc0fa7b24357abddbca8e5828ae0bb5a34a90b7dc79f88358721d10`

The first interface attempts and the intermediate hob-only correction remain beside them and are hash-pinned in the V5 manifest. The immutable V4 manifest remains SHA-256 `6340d9cddddabd430872af08dd2b6672b38f08cd2cedad4256016512f164c4f6`.

The image edits were made with the built-in image generator in image-edit mode. The final sink amendment instructed it to change only the sink modules, keep every other module and pixel dimension fixed, retain the corrected deep-blue hob, and give every sink state one full-width straight rear/top datum with square module mating boundaries and no caps, shoulders, steps, projections or outer-end chamfers.

## Delivery architecture

The page preloads and decodes one lossless `36`-drawing atlas before controls are enabled. The atlas contains:

- 14 exact V4 reference drawings;
- 14 corrected candidate drawings;
- 5 loose-object drawings;
- 3 master-resolution fitted-interface connectors (`standard-standard`, `standard-oven`, `oven-standard`).

The archived atlas is served through the same-origin integrity-checking review proxy. The public manifest remains below the 24 KiB archive threshold. The old V22/V32 five-layer healing artwork is not used.

## Verification

Run:

```sh
/Users/frank/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 scripts/build_kitchen_complete_room_layout_v5.py
npm run maintain:keeper-review
node scripts/verify_kitchen_complete_room_layout_v5.mjs
npm test
```

The V5 verifier checks source hashes, immutable V4 pixels, exact body sizes, the straight sink datum in all three sink drawings, exact grid coordinates, cabinet ownership, connector inventory, one-atlas delivery, page syntax, archive integrity and same-origin routing. Headless Chromium additionally verified a clean one-atlas load with no page errors, all three canvases, all-Broken rendering, `1×`/`4×` rendering and a cupboard swap that carried the kettle to the new exact centre.

## Boundary

V5 is rejected review provenance. It does not alter approved Kettle V47, appliance behavior, effects, SFX, production sprites, runtime selectors or game code. Kitchen Fixed Shell Layout V6 supersedes it as the active room-fit review.
