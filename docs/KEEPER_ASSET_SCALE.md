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
- Wide airborne actions use a 48 × 40 canvas with anchor `(24,40)`. The keeper
  remains exactly the same size; only the transparent space around him grows.
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

## Rig landmarks

The shared pivot landmarks are neck `(16,11)`, shoulders `(10,15)` and
`(22,15)`, and hips `(13,25)` and `(19,25)`. New outfits must preserve these
landmarks. The striped swimming costume, parachute harness and all future
costumes therefore change clothing only, never body proportions.

Any new prop-based animation must add its hand, seat or ground point to the
JSON contract and its sprite sidecar. Verification rejects changes that break
the established switch heights, canvas scale or feet anchors.
