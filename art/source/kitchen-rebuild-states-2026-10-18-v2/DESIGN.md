# Kitchen Rebuild V2 design record

V2 is an amendment set, not a kitchen rerender. Rebuild V1 remains the exact
room, cabinet, table/chair and projection authority.

## Composition method

- The V1 cream/terracotta background and table/chair are byte-identical.
- Standard kettle, toaster, oven, bowl and basin cells remain byte-identical
  to V1.
- The standard fridge changes only to a white/ivory enamel door.
- On and Broken pixels are normalized with the exact V1 coordinate transform
  and then confined to their existing 84-pixel bay.
- The broken fridge alone uses an extended x=44–168/y=105–224 cell so its
  attached fallen door and puddle can meet the real floor without covering the
  kettle bay.
- Upper-only amendments clear and replace their complete object/worktop zone;
  they are never alpha-composited over an intact appliance.
- The approved V28/V31 bin object/effects remain byte-identical.

## State family

- Fridge: Standard white door; Broken failed top hinge, lower-hinge attachment,
  exposed generic contents, floor puddle and separate drip/ripple.
- Kettle: Standard/On unchanged object with separate spout steam; Broken lid
  off with a larger separate steam cloud.
- Toaster: On browned toast and separate heat; Broken black toast and separate
  connected smoke.
- Oven: Off unchanged; On warm cavity, roasting dish and solid red indicator;
  Broken attached open door, separate billowing smoke and irregular
  red-indicator/cavity flicker.
- Bowl: Standard; Broken in two halves.
- Basin: Standard/On unchanged object with separate gentle flow; Broken failed
  outlet and separate upward spray.

Every new environmental strip contains 40 isolated 120 × 144 frames at 4 fps,
giving a sedate ten-second loop. The review compositor redraws from the empty
V1 background and selects exactly one state per asset, enabling arbitrary mixed
states without hidden intact objects.
