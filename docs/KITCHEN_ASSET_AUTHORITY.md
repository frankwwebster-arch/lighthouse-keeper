# Kitchen asset authority

The kitchen's approved art and geometry authority is the single consolidated
Warm Ligne-Claire Family package dated 24 October 2026.

## Files to use

- High-resolution visual master:
  `art/source/kitchen-warm-ligne-claire-family-2026-10-24-v4-on-food-corrected.png`
- Legacy 84 × 74 compatibility bodies and light-only animation layers:
  `art/drafts/kitchen-warm-ligne-claire-family-2026-10-24-v4/`
- Machine-readable requirements:
  `data/kitchen_asset_contract_v1.json`
- Room grid:
  `data/kitchen_room_grid_contract_v2.json`
- Rebuilder and verifier:
  `scripts/build_kitchen_warm_family_v4.py` and
  `scripts/verify_kitchen_warm_family_v4.mjs`
- Reversible runtime promotion:
  `data/kitchen_runtime_promotion_v1.json` and
  `scripts/build_kitchen_runtime_v1.mjs`

The master SHA-256 is
`a8a6972dd8398ec3cd52f42825a5a5f056a1e289d10b77796f3294b3ac85ab98`.

## Binding visual direction

Use the master exactly as the kitchen's style source: warm, softly dimensional,
adult ligne claire with observationally accurate furniture and machinery,
controlled near-black outlines, cream enamel, deep/cyan blue cabinetry and
orange hardware. It must remain crisp at native size and at 2x/4x zoom. Do not
revert to flat schematic art, childish proportions, candy gloss, cute smoke,
flies or arbitrary cartoon damage.

## Binding native presentation and locomotion geometry

Kitchen art must be retained and reviewed at the approved master's native
resolution. It must not be reduced to 84 × 74 bodies for visual approval or
future final presentation. Camera zoom may scale the composed world for the
viewport, but there is no reduced intermediate artwork and 100% review zoom
maps one source pixel to one CSS pixel.

The high-resolution master uses six equal 228-pixel source bays at x boundaries
65, 293, 521, 749, 977, 1205 and 1433. Each source bay maps independently to
two exact Prime Keeper paces: one pace is 10.5 logical pixels, or 84 integer
Keeper units, and is represented by 114 source pixels in the native kitchen
review. Every point the Keeper walks between must sit on this pace lattice.
That exact walk distance is the binding spatial restraint; asset resolution is
not constrained by the locomotion grid.

The 772 × 224 coordinate system, six x origins 84…504 and 84 × 74 bodies are
retained as the reversible Runtime Promotion V1 compatibility boundary only.
They are not the continuing visual authority. Taps, the hob, broken doors and
environmental effects continue to use registered overflow layers.

The Belfast sink is centred and rear-set. The basic fridge is a one-bay
undercounter model. The cabinetry forms one fitted family, with a continuous
worktop and plinth and perspective only at exposed outer ends.

## States and animation

Off, On and Broken reuse identical bodies, apertures, handles, controls and
lamp positions. State changes are limited to declared doors, contents, lamps
and removable environmental layers.

- Dishwasher: Off has three dark lenses; On has the same three green; Broken
  has the same three red. In Broken only those red lenses animate, flashing
  intermittently and independently. Its door is merely ajar.
- Oven: Off is dark; On contains properly cooked golden food; Broken contains
  the burnt version, one failed dial on two wires and a moderately ajar attached
  door. In Broken only the internal cavity light flashes. The red indicator is
  static.
- Sink: On flows from the intact tap; Broken flooding remains a separate layer.
- Fridge: Off and On are identical and unlit. Broken has a mostly closed door
  sagging down-left from a surviving lower hinge, restrained contents and a
  separate leak.

Both light animations are 40 frames at 4 fps. Each frame uses a 92 x 82 cell
containing the registered 84 x 74 body position plus a four-pixel transparent
gutter. No body pixel moves between frames.

## Loose objects, movement and audio

Kettle and toaster belong to separate eligible standard cabinets, sit at the
exact counter midpoint and move with their owners. The bowl is worktop-only.
The bin, table and chair snap to declared floor sections; the chair seat is
7.75 logical pixels above the floor.

Broken appliance motion uses independent whole-object and component layers
with Off, Subtle and Emphatic levels. The kettle's detached Broken lid remains
a component layer and steam is separately anchored above the opening. Repair
stops every animation and sound immediately and unlocks movement.

Every asset/state exposes an independently toggleable, drag-and-drop replaceable
SFX slot. Broken appliances may initially use an intermittent metal-rattle
placeholder. No final audio is baked into art or animation.

## Status

Frank approved this visual family and its perspective on 24 October 2026. It is
the only continuing kitchen art authority. Runtime Promotion V1 is wired and
technically verified, but its reduced 84 × 74 visual presentation is rejected
and must be replaced by a native-resolution promotion after the loose assets
complete review. Until then it remains the reversible live compatibility
implementation. It maps the existing `cooker` gameplay object to V4 Oven and
`fridge` to V4 Fridge; the other four fitted modules remain Off until they gain
gameplay consumers. Broken Oven uses only the approved cavity-light strip. The
Dishwasher strip is installed and hash-pinned, but the live Dishwasher remains
Off because no Dishwasher gameplay object exists yet.

Runtime Promotion V1's compatibility coordinate system is 772 × 224 with six
84 × 74 reduced bodies. Those dimensions are preserved only so rollback and
current gameplay behaviour remain deterministic; they are not approved art
dimensions. Cooker/Fridge interaction points, commands, need changes, activity
timing, upgrades, saves, breakdown state and repair behaviour are unchanged.

Promotion is reversible. Exact approved bytes are copied through the versioned
draft, production-source and public-delivery locations recorded in
`data/kitchen_runtime_promotion_v1.json`. The prior
`public/sprites/room_kitchen.png` is neither overwritten nor removed and its
hash is pinned in the promotion record.

## Current loose-asset review

The complete movable room is published at
`/keeper-review/kitchen-room-layout-v2/`. It displays the approved fitted run
and the toaster, kettle, bin, bowl, table and chair at native source resolution.
The fitted run is an unscaled master crop. Loose objects are deterministic 1:1
cutouts whose retained RGB bytes match the master exactly; only the connected
sheet background becomes transparent and a four-pixel safety gutter is added.
All destinations sit on the Prime Keeper pace lattice and Broken appliances
stay movement-locked until repaired.

This page exists so Frank can specify amendments to the loose assets shown on
the source sheet. It is review-only: no approved source or runtime pixel is
overwritten or promoted, and no superseded kitchen draft is restored. Its exact
native crops, output hashes, pace mapping and discard boundary are recorded in
`data/kitchen_room_layout_review_v2.json` and its extraction register.

V1 is rejected and frozen only as historical evidence. It incorrectly used the
reduced 84 × 74 compatibility bodies as review artwork, resized loose crops,
changed their colour with a blend mode and presented them on a schematic
canvas. It must never be used as an art reference.

## Consolidation record

The approval ended an unusually large exploratory run. Immediately before
consolidation the repository contained **158 superseded kitchen room/furniture
draft directories** in `art/drafts` (3,402 files, approximately 321 MiB), plus 79
superseded source directories, 134 superseded review routes, 134 archived
review-set manifests, 268 obsolete kitchen build/verification utilities, 153
superseded kitchen delivery/specification documents and 28 superseded kitchen
approval/rejection records. The formal drafts also had 85 duplicate `art/raw`
derivative directories. Archive pruning removed 4,218 retired kitchen media
references and 1,105 content objects used by no surviving review. These counts
exclude this approved V4 package. The kitchen-named Claude condiment/prep pack
was retained because its 14 assets belong to the live Bubble Stories catalogue,
not to the room/furniture iteration history.

Those prior versions were removed on 24 October 2026 at Frank's instruction.
Their binding requirements were reconciled into this document,
`data/kitchen_asset_contract_v1.json` and
`data/kitchen_room_grid_contract_v2.json` first. The deletion deliberately did
not touch the then-loaded runtime kitchen sprite. Runtime Promotion V1 later
retained that same sprite as the backdrop and rollback target while installing
the approved fitted family as a separate versioned layer.
