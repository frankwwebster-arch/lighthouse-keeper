# Kitchen Rebuild Modular V10 — structural cabinet separation

Date: 19 October 2026

Status: reversible visual-review draft; unapproved, unpromoted and unwired

Review route: `/keeper-review/kitchen-rebuild-modular-v10/`

## Outcome

V10 replaces V9's complete 84-pixel bay patches with an explicit layer
contract. The room keeps the accepted Rebuild V1 wall, floor, blue cabinet
faces, palette, projection, table and approved bin, but the working run is now:

`standalone fridge | two-cabinet run | standalone cooker/hob | two-cabinet run (sink last) | table`

The two cabinet runs are independent structural images. Fridge, kettle,
one-slice toaster, oven/hob, bowl and basin are alpha-isolated object families;
none contains wall, floor, counter or cabinet pixels. Consequently, changing
any combination of Off, On and Broken states cannot redraw or interrupt the
countertop.

## Fixed geometry and Prime anchors

The six original 84-pixel slots are unchanged:

| Asset | Slot x | Stop/turn anchor |
| --- | ---: | ---: |
| Fridge | 84–167 | `[126, 218]` |
| Kettle | 168–251 | `[210, 218]` |
| Toaster | 252–335 | `[294, 218]` |
| Oven/hob | 336–419 | `[378, 218]` |
| Mixing bowl | 420–503 | `[462, 218]` |
| Basin | 504–587 | `[546, 218]` |

Each anchor is the exact bay-centre x coordinate on the room's y=218 walking
plane. Off, On and Broken variants share one origin and installed-body slot.
Broken doors, water and other overflow may extend outside the body but never
move its anchor. The review page includes a native-size crosshair proof.

## State families

Every object has `off`, `on` and `broken` files:

- fridge: freestanding white enamel body; subtle On indicator; lower-hinged
  broken door, generic contents and floor-level static pool;
- kettle: traditional arched-handle steam kettle; On steam remains a separate
  effect; Broken state has an open neck and displaced lid;
- toaster: deliberately narrow one-slot body; one visible slice in On and one
  blackened slice in Broken;
- oven: standalone cream cooker including its own hob; dark Off cavity, lit On
  cavity/roast/solid warning lamp, and straight-toward-camera Broken door with
  burnt roast and hanging wired dial;
- bowl: exact Off/On object and two separated halves in Broken;
- basin: self-contained basin/tap overlay; On water and Broken spray remain
  separate effects.

The approved V28/V31 bin and the V9 table/chair are byte-preserved.

## Effects and review tool

V10 retains the asset-first V9 workbench: select an asset, apply any number of
compatible effect families, then change model, 0.1×–4× speed, position, size,
crop or removal. Every source loop remains 40 frames at 4 fps for a canonical
ten seconds. The fridge drip remains disabled by default.

The cooker-locked warning and cavity strips were regenerated from the isolated
V10 cooker. The internal-light active cells contain the complete identically
registered lit Broken cooker, so the door and transparent window do not move.
The All On, All Broken and Intermingled canvases now select effects from their
actual state maps instead of V9's hard-coded preview subset.

## Deterministic gates and reversibility

Build:

```sh
/Users/frank/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 scripts/build_kitchen_rebuild_modular_v10.py
```

Verify:

```sh
npm run verify:kitchen-rebuild-modular-v10
```

The verifier checks the two-run geometry, empty fridge/oven structural slots,
all eighteen transparent state cells, two-pixel gutters, absence of cabinet
pixels in countertop props, exact fixed anchors, output hashes, 40 isolated
frames per effect model, review preloading and archive coverage.

No Final sprite, runtime manifest or live-game wiring changes. Rejection is
fully reversible by deleting only the V10 source/raw/draft/review/archive,
builder, verifier and this document; V1–V9 remain immutable.
