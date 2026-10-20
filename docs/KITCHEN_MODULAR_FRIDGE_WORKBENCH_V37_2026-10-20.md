# Kitchen Modular Fridge Workbench V37

V37 supersedes rejected V36 as the active reversible fridge review gate. It
changes only the fridge's blue carcass palette and countertop depth; Final and
runtime remain untouched.

## Cabinet match

- The visible fridge countertop is an exact `84 × 14 px` construction from
  approved Cabinet V11 pixels, with its top at cell y=4. It therefore shares
  the cabinet's depth, horizontal bands, colour and rounded outer ends.
- Saturated blue carcass/frame pixels are selected only from Cabinet V11's
  exact body-blue palette. The previous brighter fridge-only blue is removed.
- The dynamic V22/V32 healing resolver is unchanged. It closes an exact join,
  while the standalone fridge itself now matches its neighbour before healing.

## Preserved V36 mechanics

- Exact `84 × 74 px` logical body at room y=134–208.
- Left hinges in both states; Broken has a failed top-left hinge and surviving
  lower-left hinge.
- Literal `68 × 52 px` Standard door reused at scale `1:1` in Broken.
- Maximum four-pixel Broken overflow, static contents/puddle, separate
  removable 40-frame/4-fps ten-second drip/ripple and sound-only low buzz.
- Existing 84-pixel snap grid and Prime midpoint at y=218.

## Review and verification

- Review: `/keeper-review/kitchen-modular-fridge-workbench-v37/`
- Native builder: `scripts/build_kitchen_modular_fridge_assets_v37.py`
- Workbench builder: `scripts/build_kitchen_modular_fridge_workbench_v37.mjs`
- Verifier: `npm run verify:kitchen-modular-fridge-workbench-v37`

The verifier compares the complete fridge worktop against the Cabinet V11
source construction byte-for-byte, then checks all inherited door, hinge,
cell, effect, archive, snap and 24-layout join contracts.
