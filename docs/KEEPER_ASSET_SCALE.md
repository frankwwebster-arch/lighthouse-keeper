# Keeper scale and interaction contract

The keeper is the measuring stick for every room, prop and interaction. The
authoritative machine-readable data is `data/keeper_asset_contract.json`; this
page explains it in ordinary language.

## Fixed scale

- One logical pixel is four source-image pixels (`density: 4`).
- The normal keeper canvas is 32 × 40 logical pixels with his feet anchored at
  `(16,40)`.
- His measured visible reference is 24.75 × 38.25 logical pixels. The uneven
  fractions come from measuring the density-4 source, not from rescaling him.
- The vertical dive uses 48 × 56 with anchor `(24,56)`. Full parachute
  deployment uses 48 × 84 with anchor `(24,84)`. The keeper remains exactly the
  same size; only the transparent space around him grows.
- Bed entry and snoring use 48 × 40 with anchor `(24,40)` so the horizontal
  body fits without rescaling.
- Directional swimming uses a centred 48 × 48 canvas and movement anchor
  `(24,24)`. Party headwear uses 32 × 48 with feet anchor `(16,48)`.
- Never scale the keeper to make him meet an object. Position and size the
  object from the interaction points below.

The coordinate origin is the top-left. X increases rightward and Y increases
downward. A side-facing point at X mirrors with `mirroredX = canvasWidth - X`.

## Object placement heights

| Object or surface | Height above his foot line | Authoritative keeper point |
|---|---:|---:|
| Light switch / small wall button | 23 px | side `(27,17)`; rear `(26,17)` |
| Door handle | 20 px | side `(25,20)`; rear `(24,20)` |
| Rear worktop / basin / cooker | 19 px | `(16,21)` |
| Chair, sofa or toilet seat | 11 px | `(16,29)` |
| Animal food bowl target | 6 px | side `(27,34)` |
| Soil contact for spade | 2 px | side `(27,38)` |
| Seed-scatter target | 6 px | side `(27,34)` |
| Low vegetable harvest | 4 px | side `(26,36)` |
| Fruit harvest | 26 px | side `(25,14)` |
| Welding contact | 18 px | side `(27,22)` |
| Sawing contact | 17 px | extended side canvas `(35,23)` |
| Bed mattress surface | 9 px | extended bed canvas `(24,31)` |
| Fish-feed opening / tank top | 41 px | raised canvas `(26,7)` |
| Aquarium brush target | 23 px | extended side canvas `(34,17)` |
| Aquarium net target | 19 px | extended side canvas `(34,21)` |
| Hammering workbench | 17 px | extended side canvas `(32,23)` |
| Writing surface | 19 px | extended side canvas `(34,21)` |
| Turntable platter | 13 px | extended side canvas `(34,27)` |
| Potter's-wheel hand position | 17 px | `(20,23)` on 40 × 40 canvas |
| Meal table surface | 12 px | tray canvas `(39,28)` |
| Watering target | 9 px | extended side canvas `(35,31)` |
| Barometer / instrument control | 23 px | side `(27,17)`; rear `(26,17)` |
| Lift button | 23 px | front `(27,17)` |

These are interaction datums, not mandatory object sizes. For example, a light
switch can have any suitable plate size, but its button centre must be 23 px
above the floor when the keeper stands on the same floor line.

## Placement recipe

1. Choose the named interaction profile from
   `data/keeper_asset_contract.json`.
2. Give the object a stable world-space interaction point, such as the centre
   of a switch or the lip of a bowl.
3. Place the keeper so the selected profile's point lands on the object point.
4. Keep his scale and feet anchor unchanged.
5. Mirror only clips marked `mirrorSafe`; use the corresponding mirrored point.

Example: the right-facing switch hand is `(+11,-23)` from his feet. If a
switch centre is at world position `(200,100)`, place his feet at `(189,123)`.

For television seating, place the seat contact at the clip's `(16,29)`. Put
the screen centre 24 logical pixels to the right and 15 pixels above that seat
for the right-looking pose, or mirror the strip and use 24 pixels left. The
chair/sofa should support the keeper's seat point but must not extend across the
screen sightline.

For beds, align the mattress surface with `(24,31)` on the 48 × 40 bed-action
canvas and the pillow centre with `(38,22)` for a right-facing layout. Mirror
both the clip and points for a left-facing bed. The bed frame, mattress,
blanket and pillow remain separate layers; play `keeper_get_into_bed` backward
for getting out.

## Rig landmarks

The shared pivot landmarks are neck `(16,11)`, shoulders `(10,15)` and
`(22,15)`, and hips `(13,25)` and `(19,25)`. New outfits must preserve these
landmarks. The striped swimming costume, parachute harness, light powder-blue pyjamas and yellow sou'wester oilskins
therefore change clothing only, never body proportions. Knight, spaceman,
pirate, Tarzan, Halloween and mechanic sets use the same three-view movement
contract: side/right (mirror for left), direct rear and direct front, all on a
32 × 48 canvas with an unchanged body scale.

Directional underwater movement reads `movementVector` from the manifest:
right `(1,0)`, mirrored left `(-1,0)`, up `(0,-1)`, and down `(0,1)`. Water,
bubbles and splashes remain separate effects. The extended party canvas adds
transparent room above his head for the cardboard cone; the same 32 × 48
contract holds the broad sou'wester brim. His body is not scaled down to make
either hat fit. Sou'wester movement vectors are right `(1,0)`, rear/up
`(0,-1)` and front/down `(0,1)`; mirror the side strip for left.

Wide held instruments and reclined poses use the 48 × 40
`extendedHeldInstrument` canvas without changing body scale. Raised drumsticks
use the 32 × 48 `extendedRaisedArmsAction` canvas. Front and rear drumming align
the stool at `(16,37)` and the drum surface at `(16,27)`. Movie seating aligns
at `(24,29)` on its wider canvas; the screen centre is 32 pixels to the viewed
side and 15 pixels above that seat point.

Snow clearing uses the 48 × 40 `extendedSnowToolAction` canvas. Place the
right-facing shovel/snow contact at `(43,37)` and mirror to `(5,37)` for left.
The reusable crouched rear-work loop uses the normal canvas and reaches ground
objects at `(16,38)`. Snow banks, shoveled piles and spray remain separate
layers; the thick winter coat is recorded as `winter-coat` outfit metadata.

Cake retrieval and carrying use the 48 × 40 `extendedTrayAction` canvas. Align
the oven rack to `(24,30)` for the direct-rear retrieval. The connected turn
holds the tray at `(34,20)` for right and mirrored `(14,20)` for left. The
mitts, tray and cake stay on the actor; oven casing, door and rack stay on the
object so different ovens can reuse the same animation.

Any new prop-based animation must add its hand, seat or ground point to the
JSON contract and its sprite sidecar. Verification rejects changes that break
the established switch heights, canvas scale or feet anchors.

Bath, shower and hot-tub clips use the same scale but carry explicit privacy
metadata. Entry and exit frames use `towel-privacy`; washing uses
`mosaic-privacy`, and the hot-tub loop uses `privacy-foam`. The opaque coverage
is part of every relevant actor frame, so pausing or skipping frames cannot
reveal an uncovered intermediate pose. The bath, shower and tub remain separate
objects aligned to the usual feet or seat point.

Welding uses the normal 32 × 40 canvas. The hand saw needs the 40 × 40
`extendedSideTool` canvas so its full stroke remains visible without shrinking
the keeper; its feet anchor is `(20,40)`. Align a separate metal workpiece to
the welding contact or a separate timber/sawhorse assembly to the sawing
contact. Do not bake either work surface into the character strip.
