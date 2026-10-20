# Kitchen Modular Fridge Workbench V36

V36 supersedes rejected V35 as the active reversible fridge review gate. It
does not alter or promote Final/runtime assets.

## Coordinated state construction

- Standard and Broken use the same freshly drawn storm-blue/turquoise carcass
  and restrained deep-navy edge language as approved Cabinet V11. At native
  scale the intended exterior contour is one pixel; the heavy near-black halo
  from the rejected drafts is not part of this family.
- Both states use left-side hinges. Broken has a failed top-left hinge and a
  visibly surviving lower-left hinge.
- Broken uses the literal `68 × 52 px` door crop from Standard. It is rotated
  rigidly by 12.4 degrees at scale `1:1`; it is neither redrawn nor resized.
  The opposite lower corner reaches the floor while total horizontal overflow
  remains within four pixels of the logical bay.
- The appliance body remains exactly `84 × 74 px` at room y=134–208. Each
  state occupies an isolated `144 × 90 px` transparent cell with deterministic
  transparent gutters.
- Contents and puddle are static in Broken. The water drip/ripple remains a
  separate, removable, variable-speed 40-frame/4-fps ten-second loop. The low
  electrical buzz remains a named sound-only placeholder.

## Placement and joins

V36 retains approved V33 snapping and join resolution. Fridge, sink and oven
snap to three distinct free 84-pixel origins, and every Prime interaction
anchor remains the committed asset midpoint at y=218. Oven adjacencies keep
V32 triangular healing; all other fridge adjacencies receive the exact V22
blue body backfill and countertop cap. The repair layers follow the appliance
and remain separate from its sprite.

## Review and verification

- Review route: `/keeper-review/kitchen-modular-fridge-workbench-v36/`
- Native-state builder: `scripts/build_kitchen_modular_fridge_assets_v36.py`
- Workbench builder: `scripts/build_kitchen_modular_fridge_workbench_v36.mjs`
- Verifier: `npm run verify:kitchen-modular-fridge-workbench-v36`

The verifier checks the shared left hinge, exact `68 × 52 px` source door,
fixed `1:1` scale, body/cell geometry, four-pixel overflow ceiling, isolated
effect frames, all 24 legal arrangements, V33 byte identity, archive hashes
and universal non-oven V22 joining.
