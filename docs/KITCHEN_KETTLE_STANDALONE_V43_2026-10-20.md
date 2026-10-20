# Kitchen Kettle Standalone V43

Date: 20 October 2026

Status: reversible visual/behaviour review draft; unapproved, unpromoted and
unwired.

Review: `/keeper-review/kitchen-kettle-standalone-v43/`

V43 is the visual correction requested after V42 review: V42 looked too
pixelated and its base floated above the visible countertop. V43 keeps the
approved modular geometry, Broken-state movement lock and asset-owned effect
rules while redrawing at a more legible native scale and seating the base on
the actual visible top surface. It does not alter any Dishwasher V41, Cabinet
V11, V42, Final or runtime byte.

## Native counter scale

The binding scale is the approved kitchen at its real `772 × 224 px` game
size, not the enlarged source sheet or inspection cards.

- One `84 px` bay represents the documented `60 cm` fitted unit.
- The kettle's round body is approximately `20–22 cm` against that bay.
- Handle and whistle spout produce a maximum `44 × 44 px` visible envelope.
  The extra envelope belongs to those overhanging parts; it does not turn the
  body into a half-bay-wide domestic kettle.
- The production cell is `64 × 64 px`, offset `(10, -53)` from the selected
  one-bay body origin. Every state has at least four transparent pixels of
  safety gutter.
- Room y `134` is the approved worktop's rear edge, not its visual support
  line. The turquoise top plane continues through y `140`. The opaque kettle
  base therefore ends at local y `59` / room y `140` (bottom-exclusive y
  `141`), overlapping the top plane naturally without sinking into its fascia
  or owning a counter pixel.
- The default logical origin is x `168`, so Prime's stop/turn point remains the
  exact bay midpoint `(210, 218)`.

The live review permits only exact compatible surface origins x `84`, `168`,
`336` and `504`. Origin x84 is the approved fridge worktop; the other slots are
the two ordinary cabinets and dishwasher worktop. Placement persists
`supportAssetId`, `surfaceSlotId` and an asset-local offset rather than only a
room coordinate. The current room origin and Keeper stop/turn point are derived
from that supporting bay. This makes the kettle a dynamic `make-cup-of-tea`
place: Prime stops at `support origin + 42, y218` and faces the worktop.

The underlying cabinetry and joins do not become kettle pixels. A support
asset may move normally while carrying an Off/On kettle, updating the derived
kettle origin and tea stop. A support carrying a Broken kettle cannot move
until the kettle is repaired or removed, because moving it would displace the
locked appliance.

## Coordinated states

- **Off:** closed old-fashioned cream enamel kettle with a navy arched handle,
  turquoise lid/base and warm copper fittings.
- **On:** byte-identical to Off. Heat/steam is not painted into the casing.
- **Broken:** the same physical kettle with one torn handle mounting, a sharply
  sagging handle retained by the surviving mount, conspicuously sprung attached
  lid, deep crushed dent, large contained exposed-metal chip and bent attached
  whistle. No detached part crosses the cell gutter.

Broken also owns an eight-frame body-rattle strip at `4 fps`. Its broad base
row is byte-identical in every frame and remains pinned to y140 while upper
parts shear by at most two pixels. Steam remains a separate kettle-owned layer;
the body strip contains no steam or other environmental pixels.

The high-resolution built-in image-generation source sheet is retained under
`art/source/kitchen-kettle-standalone-2026-10-20-v43/generated/`. It was
redrawn with a restrained outline, simpler enamel highlights and a broad,
stable base for a cleaner 44-pixel reduction. The builder
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

Off and On may move only between the four exact compatible origins. Broken
rejects direct dragging and bay-button movement, retaining its snapped origin,
Prime midpoint and owned effect transforms until repair to Off or On. The
review also rejects movement of the current supporting asset. The gameplay
kitchen furniture controller still does not exist.

## Reversibility and boundary

V43 uses a new source, raw, draft, public review and archive prefix. It does
not overwrite V42, rejected Kettle V33 or any approved source. Rejecting V43
requires discarding only its versioned directories and route. Dishwasher V41
is separately pinned by
`docs/review/kitchen-dishwasher-workbench-v41-approval-2026-10-20.json`.

Toaster and mixing bowl work has not started and remains blocked until Frank
reviews this kettle.

## Verification

```sh
npm run verify:kitchen-dishwasher-workbench-v41-approval
npm run verify:kitchen-kettle-standalone-v43
npm test
npm run typecheck
npm run build
```

The focused V43 gate checks exact inherited V41 room/counter hashes, native
envelopes and y=140 visible-surface seating, Off/On byte identity, cell gutters, forty-frame
effect isolation, Broken movement rejection, repair unlocking, kettle-local
effect ownership, preload/decode gating and the content-addressed archive.

## Delivery audit

The final documentation audit reconciled README, STATUS, DECISIONS, the V41
approval record, the V42 rejection context, V43 source/draft/raw/archive paths, route, geometry,
effect ownership, review boundary and the explicit toaster/bowl hold. The
archive contains `186` set manifests, `4,518` logical references and `2,704`
committed-tree objects after V43; V43 contributes sixteen logical references
backed by seven new objects, including the explicit fridge-top proof, and only
its HTML shell remains in `public/`.

The focused V41 approval, V42 preservation and V43 gates, TypeScript check and production Next.js
build pass. The review JavaScript parses and the built route serves the exact
HTML plus a content-addressed redirect carrying the expected kettle hash. The
repository-wide `npm test` reaches and passes the new gates, then retains its
pre-existing failure in `verify_review_archive.mjs`: current remote main is
already `53.31 MiB` in `public/` while that historical guard still requires
less than `50 MiB`. V43 adds only its HTML shell to that tree and does not
weaken the unrelated guard. This known baseline discrepancy is not a Kettle
V43 verification failure.
