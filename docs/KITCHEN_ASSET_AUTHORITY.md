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
with Off, Subtle and Emphatic levels. The kettle's detached Broken lid is now
historical rejected evidence: V4 excludes that drawing. Kettle On is
byte-identical to Off, while Broken uses the cracked former-On body. Steam is
separately anchored above the spout and is not drawn in the V4 review. Repair
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

Frank subsequently approved and locked the six fitted units after directing the
OFF tap-registration repair. Their one immutable 1368 x 284 native base is
hash-pinned in
`docs/review/kitchen-fitted-units-lock-approval-2026-10-24.json`. OFF, ON and
BROKEN all retain that exact base at one registration; only declared state,
warning-light, oven-light and environmental overlays may be composited above
it. The unit bodies must not be redrawn, moved, scaled, resampled or recoloured.

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

The active redraft review is published at
`/keeper-review/kitchen-room-layout-v7/`. It uses the locked fitted base in all
three global states, so the full cabinet run cannot move and no source-sheet row
boundary can appear. V7 replaces V6's opaque 100 × 60 ON sink row crop with a
water-only transparent effect: its fall begins at the curved tap outlet and its
splash is clipped before the unchanged opaque basin front. Sink flow, fitted damage, three independent dishwasher
warning lights, the oven cavity light and floor water are registered transparent
overlays. Floor water sits on the walking plane and never participates in the
fitted-run box.

The toaster, kettle, bin, bowl, table and rear-facing chair are target-sized
source drawings extracted 1:1, with no downscaling, resampling or colour
transform. No movable output contains a baked contact shadow; room surfaces
remain owned by the room. Each output has an eight-pixel transparent safety
gutter. Countertop support is local y=84, thirteen native
pixels forward from V4, so the objects occupy the visible worktop plane rather
than its rear edge. Toaster On is one connected silhouette with toast seated in
its slots. Kettle On is byte-identical to Off and has no drawn steam. The broken
bowl physically loses its front-left wall and includes detached pieces. The
rear chair retains every V6 wood pixel but removes five enclosed white
source-paper islands, so the seated Keeper is visible between its slats.

Prime and the kitchen are registered into one world density before camera zoom.
The existing 256 x 320 Prime source cell uses 8 pixels per logical pixel while
the kitchen uses 228/21, so Prime displays at 228/168 = 1.357142857 times its
source cell: 347.43 x 434.29 kitchen-world pixels. This makes the approved
213-pixel worktop read as about 850 mm against a 1,750 mm Keeper, around waist
height. The table is modelled at 750 mm and the rear-facing chair at a 460 mm
seat height. This display registration does not rewrite or downscale either
source; camera zoom applies uniformly to the composed world.

This page is review-only: no approved source or runtime pixel is overwritten or
promoted. Its exact outputs, source hashes, support rows, global-state map,
world-scale equation, pace mapping and discard boundary are recorded in
`data/kitchen_room_layout_review_v7.json` and its extraction register. The
table and rear-facing chair share exact pace 16 beyond the fridge; depth order
is table, rear-seated Keeper, chair. V7 exposes the immutable V6 predecessor and
the corrected draft side-by-side. V5 is rejected shadowed evidence; V4's
fitted-unit approval remains binding.

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
