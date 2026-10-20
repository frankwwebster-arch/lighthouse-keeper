# Kitchen Kettle Standalone V42

Date: 20 October 2026

Status: reversible visual/behaviour review draft; unapproved, unpromoted and
unwired.

Review: `/keeper-review/kitchen-kettle-standalone-v42/`

V42 is the first countertop appliance built after Frank approved Dishwasher
Workbench V41. It applies the approved modular geometry, Broken-state movement
lock and asset-owned effect rules without altering any Dishwasher V41,
Cabinet V11, Final or runtime byte.

## Native counter scale

The binding scale is the approved kitchen at its real `772 × 224 px` game
size, not the enlarged source sheet or inspection cards.

- One `84 px` bay represents the documented `60 cm` fitted unit.
- The kettle's round body is approximately the earlier `18 cm` target.
- Handle and whistle spout produce a maximum `32 × 32 px` visible envelope,
  close to the documented seven-logical-pixel (`28 px`) target while retaining
  a readable old-fashioned silhouette.
- The production cell is `48 × 48 px`, offset `(18, -44)` from the selected
  one-bay body origin. Every state has at least four transparent pixels of
  safety gutter.
- The opaque base ends at local y `44`. With the cell at room y `90`, the base
  contacts the exact approved worktop plane at room y `134` without floating,
  sinking or owning a counter pixel.
- The default logical origin is x `168`, so Prime's stop/turn point remains the
  exact bay midpoint `(210, 218)`.

The live review permits only the exact compatible counter origins x `168`,
`336` and `504`. The underlying cabinet, dishwasher, joins and worktop do not
move with the kettle. This is a separate countertop-appliance occupancy layer,
not a replacement fitted-unit body.

## Coordinated states

- **Off:** closed old-fashioned cream enamel kettle with a navy arched handle,
  turquoise lid/base and warm copper fittings.
- **On:** byte-identical to Off. Heat/steam is not painted into the casing.
- **Broken:** the same physical kettle with one failed handle mounting while
  the handle remains attached, a sprung but attached lid, one body dent and a
  small enamel chip. No detached part crosses the cell gutter.

The high-resolution built-in image-generation source sheet is retained under
`art/source/kitchen-kettle-standalone-2026-10-20-v42/generated/`. The builder
deterministically crops and normalises it to native scale; generated pixels are
never served directly.

## Asset-owned steam

On and Broken each have compact, regular and emphatic steam models. Every
model is an isolated `40`-frame strip at `4 fps` for a canonical ten-second
loop. Each placed layer stores:

- `anchorAssetId: kettle`;
- applicable kettle state;
- asset-local x/y, size, crop, speed and model;
- the requirement to remain attached while Broken.

The On placement is a restrained spout wisp. The Broken placement is a larger
pressure leak above the sprung lid. These are separate effect strips and never
change kettle body pixels. Removing a layer is independently allowed.

Named SFX placeholders are `kitchen_kettle_heating_hiss_loop`,
`kitchen_kettle_broken_handle_rattle` and
`kitchen_kettle_broken_pressure_hiss_loop`.

## Broken movement lock

Off and On may move only between the three exact compatible origins. Broken
rejects direct dragging and bay-button movement, retaining its snapped origin,
Prime midpoint and owned effect transforms until repair to Off or On. The
review implements this contract; the gameplay kitchen furniture controller
still does not exist.

## Reversibility and boundary

V42 uses a new source, raw, draft, public review and archive prefix. It does
not overwrite rejected Kettle V33 or any approved source. Rejecting V42
requires discarding only its versioned directories and route. Dishwasher V41
is separately pinned by
`docs/review/kitchen-dishwasher-workbench-v41-approval-2026-10-20.json`.

Toaster and mixing bowl work has not started and remains blocked until Frank
reviews this kettle.

## Verification

```sh
npm run verify:kitchen-dishwasher-workbench-v41-approval
npm run verify:kitchen-kettle-standalone-v42
npm test
npm run typecheck
npm run build
```

The focused V42 gate checks exact inherited V41 room/counter hashes, native
envelopes and y=134 contact, Off/On byte identity, cell gutters, forty-frame
effect isolation, Broken movement rejection, repair unlocking, kettle-local
effect ownership, preload/decode gating and the content-addressed archive.

## Delivery audit

The final documentation audit reconciled README, STATUS, DECISIONS, the V41
approval record, the V42 source/draft/raw/archive paths, route, geometry,
effect ownership, review boundary and the explicit toaster/bowl hold. The
archive contains `185` set manifests, `4,502` logical references and `2,697`
committed-tree objects after V42; only the HTML shell remains in `public/`.

The focused V41 approval and V42 gates, TypeScript check and production Next.js
build pass. The review JavaScript parses and the built route serves the exact
HTML plus a content-addressed redirect carrying the expected kettle hash. The
repository-wide `npm test` reaches and passes the new gates, then retains its
pre-existing failure in `verify_review_archive.mjs`: current remote main is
already `53.27 MiB` in `public/` while that historical guard still requires
less than `50 MiB`. V42 adds only its `21,777`-byte HTML shell to that tree and
does not weaken the unrelated guard. This known baseline discrepancy is not a
Kettle V42 verification failure.
