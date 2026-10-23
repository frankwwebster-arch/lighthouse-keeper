# Kitchen asset authority

The kitchen's approved art and geometry authority is the single consolidated
Warm Ligne-Claire Family package dated 24 October 2026.

## Files to use

- High-resolution visual master:
  `art/source/kitchen-warm-ligne-claire-family-2026-10-24-v4-on-food-corrected.png`
- Exact fitted bodies and light-only animation layers:
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

## Binding geometry

The room is 772 x 224 logical pixels. There are six adjacent fitted bays at x
origins 84, 168, 252, 336, 420 and 504. Every fitted cabinet or appliance body
is exactly 84 x 74 pixels; the run is exactly 504 pixels wide. Interaction
centres are x 126, 210, 294, 378, 462 and 546 on y 218. Worktop support is y
141 and cabinet floor support is y 208.

The high-resolution master uses six equal 228-pixel source bays at x boundaries
65, 293, 521, 749, 977, 1205 and 1433. Each source bay maps independently to
one 84-pixel game bay. Taps, the hob, broken doors and environmental effects use
registered overflow layers; they never change the 84 x 74 body footprint.

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

Frank approved this visual family, its perspective and the exact equal-bay
normalization on 24 October 2026. It is the only continuing kitchen art
authority. Runtime Promotion V1 is now wired and verified. The live room maps
the existing `cooker` gameplay object to V4 Oven and `fridge` to V4 Fridge;
the other four fitted modules remain Off until they gain gameplay consumers.
Broken Oven uses only the approved cavity-light strip. The Dishwasher strip is
installed and hash-pinned, but the live Dishwasher remains Off because no
Dishwasher gameplay object exists yet.

The full approved 772 × 224 room coordinate system receives one uniform outer
presentation transform into the existing 420-unit floor viewport. Every body
retains its exact 84 × 74 source cell, declared origin, order and relative
registration. Cooker/Fridge interaction points derive from the approved bay
centres; commands, need changes, activity timing, upgrades, saves, breakdown
state and repair behaviour are unchanged.

Promotion is reversible. Exact approved bytes are copied through the versioned
draft, production-source and public-delivery locations recorded in
`data/kitchen_runtime_promotion_v1.json`. The prior
`public/sprites/room_kitchen.png` is neither overwritten nor removed and its
hash is pinned in the promotion record.

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
