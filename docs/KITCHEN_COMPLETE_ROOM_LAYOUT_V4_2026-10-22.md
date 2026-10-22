# Kitchen Complete Room Layout V4 — exact grid and healing comparison

Date: 22 October 2026
Status: unapproved room-layout review; V3 art remains immutable

## Purpose

V4 answers two room-integration questions without redrawing or promoting any
asset:

1. compare raw joins, V3's narrow diagnostic and the established V22/V32
   pair-aware healing stack side by side;
2. prove that every movable kitchen object commits to the kitchen's declared
   grid and exposes an exact centre-line Keeper interaction anchor.

Review route: `/keeper-review/kitchen-complete-room-layout-v4`

## Kitchen grid contract

The machine-readable authority is
`data/kitchen_room_grid_contract_v1.json`. The kitchen keeps its own grid; its
coordinates must not be copied into another room without that room declaring
the same geometry explicitly.

- Room: `772 × 224 px` at `4 px` per logical pixel.
- Fitted bays: six `84 px / 21 lp` bays at x origins
  `84, 168, 252, 336, 420, 504`.
- Fitted/working centres: `126, 210, 294, 378, 462, 546`.
- Fitted body: `84 × 74 px` at `y=134`.
- Counter-object support: `y=141`.
- Floor-object support: `y=208`.
- Keeper stop/turn plane: `y=218`.

The support plane is where the artwork touches the counter or floor. The
Keeper anchor is deliberately separate: its x coordinate is the exact centre
of the selected section and its y coordinate is always the established room
walking plane.

Kettle and toaster may use only a slot currently supported by cupboard,
drawers, dishwasher or under-counter fridge. Sink and oven/hob slots are
ineligible. The two objects cannot share a counter slot; dropping on the other
object swaps them. A cabinet swap is rejected if it would move the sink or hob
under either occupied object.

Bin, chair and table use the three declared floor sections. They also commit by
slot identifier, remain centred on the section and cannot share a slot. An
occupied drop swaps the two objects.

Only slot identifiers are saved. Pointer coordinates are preview input and are
never persisted. The verifier derives every default object's rendered opaque
centre and support contact from its source metadata and proves exact agreement
with its slot (maximum declared tolerance `0.5 px`; current error `0 px`).

## Healing views

All three canvases share state, arrangement, object slots and zoom:

1. **Raw modules** — exact V3 crops only.
2. **Narrow join diagnostic** — V3's provisional seam cover.
3. **Established pair-aware healing** — the exact five existing compositor
   templates: body backfill, flat countertop cap, oven triangle underlay and
   left/right neighbour cleanup.

The third view uses the established V38 order: background backfills and oven
underlays, unchanged fitted assets, then either a flat cap or the appropriate
oven-neighbour cleanup. It is a suitability test for the new high-resolution
art, not approval of those healing pixels for this family.

## Why 4× looks sharper than 1×

The renderer does not build or enlarge an intermediate 1× room. Every zoom
draws directly from the single lossless master atlas into a device-pixel-ratio
backing canvas. At 1×, however, several authored master pixels must resolve
into one game-size screen pixel. At 4× the browser can display far more of the
source information. The difference is therefore a real information-density
limit, not the old review-page loading or intermediate-scaling defect.

This is also why immediate clarity at 1× remains a separate art-direction test:
high-resolution detail may be beautiful at 4× yet still need simplification or
stronger silhouette decisions at game scale.

## Delivery and boundaries

- The first `520 × 6810` pixels of the V4 atlas are verified byte-for-byte
  against the complete V3 atlas.
- Five existing healing templates are appended; the page still makes one
  unique image request and unlocks only after it decodes.
- Fitted geometry, appliance states, Broken locks, source art, runtime,
  production selectors and Kettle V47 are unchanged.
- No artwork or placement contract is promoted by this page.

## Verification

```sh
npm run maintain:keeper-review
npm run verify:kitchen-complete-room-layout-v3
npm run verify:kitchen-complete-room-layout-v4
npm test
```

The V4 verifier checks the immutable V3 atlas prefix, all five healing-source
hashes and bounds, the exact room/bay/support/interaction datums, unique slot
occupancy, derived object centring, absence of saved free coordinates, inline
script syntax, archive integrity and route configuration.
