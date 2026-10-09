# Floor review decisions — 9 October 2026

Source: `frank-floor-review-2026-10-09.json`, exported from the local review
canvas at `2026-10-09T00:41:05.862Z`. The export is evidence; this file records
how each comment is being applied.

## Accepted design decisions

- The roof parachute platform is an external platform on the left of the tower,
  mirroring the visual logic of the diving platform rather than occupying a
  room.
- The bedroom bed is centred in the room. Its mattress, pillow and seat/contact
  datums come from the keeper scale contract.
- The lamp room must contain the actual optic/lamp. Its glazing is transparent.
  The broken state is dirt plus an unstable flicker and a buzzing/bulb-failure
  sound cue, not generic machine destruction.

## Character corrections included in the scale audit

- Rebuild `keeper_crouch_work_back`: canonical body width, hands in front in
  every working pose, especially frames 3 and 5.
- Rebuild all three party clips: the party hat is headwear only, so the face,
  beard, hair, body and movement must come directly from the approved canonical
  front, side-walk and turn families.
- Rebuild all three scuba directions to restore the approved keeper identity,
  coherent equipment and matching swim-cycle anatomy.
- Expand `keeper_swim_costume_horizontal` and the horizontal scuba clip to an
  80 × 48 canvas so long poses do not force the keeper smaller.
- Measure and correct `keeper_sit_front`, and all three
  sou'wester walks against skull-to-sole and core-body landmarks.
- Improve `fx_broken_smoke`; it remains a shared effect, but the present draft
  is not approved.

Completed in this pass: the crouch, party turn, all scuba directions,
horizontal swimming and sit-front strips
were redrawn; seated sources were normalised against the sit transitions; every
costume family now excludes its hat/helmet envelope from anatomy scale; the
bath-wash and hot-tub figures were rebuilt and measured from their visible head
and shoulder landmarks. `fx_broken_smoke` is now an irregular curling eight-frame
effect rather than stacked circular puffs.

Party-identity correction: `keeper_party_idle`, `keeper_party_walk` and
`keeper_party_turn_back` now inherit the exact canonical keeper frames and add
only the cardboard party hat. This removes the gnome/Santa-like alternate face
that had appeared in the generated party artwork and prevents future costume
work from changing the keeper's identity.

Party-headwear correction: the oversized blue dotted cone was rejected. The
production layer is now a modest pale-pink cardboard cone with a small red
pom-pom and irregular red fringe, based on Frank's supplied physical reference.
`keeper_party_hat_put_on_back` is a rear-view reveal assembled from approved
rear work/raised-arm components; `keeper_party_eat_cake` and
`keeper_party_dance` inherit the approved eating and dancing bodies. The loose
hat belongs to a designated world object and transfers to outfit state only on
the transition's final frame; reversing the clip removes it.

Project-wide identity decision: costumes, hats, handheld props and equipment
must be overlays on approved canonical keeper frames. They never justify a new
keeper drawing. Only a genuinely new body pose may be newly authored, and it
must pass the complete skull-to-sole, head-unit, core-width and landmark audit.

Subsequent review correction: `keeper_spiral_stairs_down` frame 4 had an
erroneous third hand behind the keeper's hip. The extra hand was removed at the
source while retaining the two legitimate arms and the existing descent cycle.

Further scale/anatomy corrections: all three bare-headed Tarzan walks retain
their measured canonical body but now use the standard 32 × 40 actor canvas
rather than misleading 48 px headwear clearance. `keeper_ride_bike_front` was
genuinely undersized and is now canonical on a 48 × 48 interaction canvas,
with unchanged floor-relative bike contacts. `keeper_carry_shopping` was
redrawn so every frame has exactly two hands, one attached to each bag-carrying
arm.

Edge-clipping correction: `keeper_put_record` and
`keeper_water_plants_side` now use 48 × 40 side-action canvases. The larger
transparent bounds retain the full record in frames 5–7 and the entire watering
can/spout without changing keeper scale or floor-relative interaction offsets.

Machete correction: `keeper_machete_side` now carries one consistent broad,
smooth-edged machete in every frame. The serrated saw-like final tool was
removed, and a 64 × 40 long-tool canvas preserves the full right-hand blade
without rescaling the keeper or changing its floor-relative contact.

Frame-isolation correction: `keeper_hot_drink_drink` and
`keeper_hot_drink_put_down` no longer contain neighbouring-frame flecks; the
released mug and intended steam remain. `keeper_snooker` now isolates each
keeper-and-cue pose rather than exposing pieces of adjacent bodies at the cell
edges, without fitting actor scale to the long cue.

Scale correction: `keeper_pressups_side` was redrawn and normalised along its
horizontal body axis while preserving canonical head height and core depth;
outer silhouette width is no longer accepted as a scale proxy. The standing
fishing clip now uses a 64 × 56 transparent canvas so the keeper reaches the
canonical actor height without fitting him to the rod, line or catch.

Paired-animation correction: `keeper_play_drums_front` is now the scale and
timing master for `keeper_play_drums_back`. The rear strip uses the same eight
arm/stick phases viewed through 180 degrees, with its seated body envelope
normalised independently of raised-stick whitespace. Both retain seat `(16,37)`
and strike `(16,27)`.

## Removed from the public art-review set

The modular front/back limb, torso and head layers, `keeper_reference`, and the
procedural `keeper_idle` are rejected as reviewable final character art. They
must not be presented beside production animation sheets. Runtime dependencies
are checked before physical files are removed; a rejected runtime clip is
replaced before deletion rather than leaving a missing sprite.

The current `room_kitchen`, `room_living`, and `room_bedroom` images are also
rejected as final review assets. They remain temporary runtime safety fallbacks
only until replacement room art is installed. `obj_tv_on` is redundant in the
review catalogue; channel-specific television strips remain the intended ON
states. These distinctions prevent a review deletion from silently breaking a
running build.

The generated review now omits every explicitly deleted modular keeper part,
`keeper_reference`, `keeper_idle`, the redundant generic TV ON strip and the
three rejected room plates. The fallback PNGs remain available only to running
code until replacements are installed.

## Additional corrections found during the audit

- The cake and plated-meal placement strips were rebuilt. Both now release at
  the standard 19 px table datum and straighten fully; the meal no longer lands
  on the floor. A subsequent edge pass restored the complete plate and food in
  `keeper_meal_place_side` frames 7–8 while leaving frames 1–6, keeper scale,
  pose and the table datum unchanged.
- The bath-wash and hot-tub strips had enlarged the visible keeper because the
  water hid his lower body. Their head/shoulder units now match the standing
  and seated canonical keeper.
- The lantern-room source now has clear glazing around a visible centred
  Fresnel optic, lamp and machinery base while retaining the inset 95 × 35
  logical footprint and wraparound gallery.
- The object/furniture starting envelope is now machine-readable in
  `data/keeper_object_dimensions.json`.

## Audit rule

Every accepted production keeper sheet is measured independently. Hats,
helmets, raised hands, tools and props never define character scale. Upright
poses use inferred skull-top to sole; articulated poses additionally use head,
shoulder, hip, hand and foot units so sitting, crouching, swimming and press-ups
cannot be enlarged merely because their silhouette is shorter.
