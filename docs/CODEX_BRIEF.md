# Codex art brief: Lighthouse Keeper (pixel style)

## Rules for every file

- PNG, transparent background (or flat `#FF00FF` magenta, which the cleanup script removes).
- Flat, front-on 2D cutaway. Not isometric. Dark pixel outline, saturated colours, simple faces.
- One art pixel = one 4 × 4 block in the game. Best: draw at true low resolution (1 art pixel = 1 real pixel). If the tool cannot, deliver larger with crisp square blocks, no blur, no anti-aliasing; the script snaps it down.
- Sizes below are in art pixels. The standing keeper is about 22 × 32, so keep everything in proportion to him.
- Bottom-centre of the image is where the thing touches the floor.
- Same palette family and outline weight across everything.

## Names and states

Every clickable object gets three states: `standard` (still), `on` (in use, animated), `broken` (animated: casing wobble, looping smoke, occasional sparks, plus one small cue unique to the object).

File name: `obj_<id>_<state>_f<frames>.png`, frames laid out left to right in one strip, all the same size. Example: `obj_tv_standard_f1.png`, `obj_tv_on_f4.png`, `obj_tv_broken_f4.png`. Later upgrade tiers: `obj_bed_t2_standard_f1.png` (tier 1 has no `_t1`).

Sizes (width × height):

`door` 13 × 24, `fridge` 12 × 24, `cooker` 18 × 15, `broom` 8 × 23, `petbowl` 10 × 5, `toilet` 13 × 18, `tv` 28 × 23, `bookshelf` 20 × 28, `piano` 25 × 18, `bed` 30 × 14, `phone` 15 × 18, `basin` 15 × 28, `desk` 25 × 20, `telescope` 23 × 23, `lamp` 30 × 35, `garden` 30 × 18, `shop` 33 × 30, `jetty` 55 × 15.

Not everything needs all three art files in the first batch. Door, shop and jetty: standard only. Lamp: standard = off, on = lit. Garden: empty plus 1, 2 and 3 ripe, as `obj_garden_ripe1_f1.png` etc. The runtime contract remains capable of all three states for every clickable object.

Implementation clarification (8 October 2026): “standard only” above describes the first art batch, not permanent ownership or gameplay. The keeper's garden/greenhouse and jetty can break, and the future keeper-owned boat can break; their animated broken art is a later exterior batch. The shop belongs to its proprietor, will eventually be off-island, and is never a breakable keeper asset.

## The keeper: layered puppet

Every part is on the same canvas, 32 wide × 40 high, drawn in its neutral standing position, so stacking all parts at 0,0 rebuilds him. The game stores explicit pivots for assembly; production raster clips use drawn pixel-safe angles rather than blurred arbitrary CSS rotation.

Front view: `keeper_front_head_happy`, `_neutral`, `_grumpy`, `_asleep` (eyes shut), `_open` (mouth open), then `keeper_front_torso`, `_arm_l`, `_arm_r`, `_leg_l`, `_leg_r`.

Back view: the same as `keeper_back_*` (one head, no face variants). The back view is used for cooking, brushing teeth and similar, so draw it with care.

Also one assembled `keeper_reference.png` so the parts can be checked for alignment. Later: small held props as `prop_<name>.png` (pan, toothbrush, book, phone, rod, cup).

## The lighthouse

- `tower_stripe_red.png` and `tower_stripe_white.png`: one horizontal stripe band each, 110 wide × 8 high, same shading. The game stacks them and works out the alternation from each floor's position, so inserted floors line up.
- `tower_base.png` (110 wide, bottom of tower and door surround), `tower_lamproom.png` (inset, fixed width, wraparound rail and outdoor walkway; always sits on top), `tower_roof.png`.
- Rooms, 105 wide × 35 high each: `room_kitchen.png`, `room_living.png`, `room_bedroom.png` (en suite included), `room_lamp.png`. Walls and floor only; furniture is separate.
- `ground_strip.png`: ordinary grass, soil and rock only. No hint of a cave, shaft or basement.

Future ordinary floors are a non-linear player progression. Do not draw them as successively narrower slices or assign a required vertical order. Keep kitchen at the base, lamp room topmost and bedroom immediately beneath it; every other standard floor receives a one-time random saved position in the middle stack. Taper is decorative exterior shading only. Extensions and the underground lair use their separate architectures rather than consuming or constraining this stack. The diving-board extension follows the moving bedroom and may reach the full tower height.

## Later batches — do not start yet

New floors (aquarium, weather station, hidden lair Batcave-style, lift), each furnished with objects and states. Also pet, visitors, ship, weather.

## Delivery report requirement

Report the exact pixel size of each delivered file and every non-obvious pivot (shoulder, hip, neck).
