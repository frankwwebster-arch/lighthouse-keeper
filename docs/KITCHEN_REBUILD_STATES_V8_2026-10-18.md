# Kitchen Rebuild States V8 — coherent broken-oven light

Date: 18 October 2026

V8 corrects only the Broken oven construction and its internal-light flicker.
The object now derives directly from the exact On oven. Its bottom-hinged door
opens only a few degrees straight toward the camera: the exact door is
foreshortened vertically around the same centreline, with no side skew and both
hinge ends aligned. The glass/window treatment remains visibly transparent to
the cavity, the roasting item is burnt and blackened, and the base red warning
indicator is extinguished with the matching Off-state indicator pixels. No
pixel from an earlier Broken oven is reused.

The cavity flicker no longer places a small lighting graphic over the oven.
Each active frame swaps in the complete, identically registered lit Broken oven
at the exact 84×120 object footprint; inactive frames reveal the complete dark
Broken oven. The state-swap cells use an 88×124 cell with two transparent pixels
on every edge, so the complete oven remains isolated. The separately removable
red warning-light layer draws above the state swap, and smoke draws above both.

All other V7 state objects, effects, asset-first controls, multi-layer stacks,
model/speed/position/size/crop controls and JSON persistence remain unchanged.
Every animation remains 40 frames at 4 fps for a canonical ten-second loop.

Route: `/keeper-review/kitchen-rebuild-states-v8/`

Build: `python scripts/build_kitchen_rebuild_states_v8.py`

Verify: `npm run verify:kitchen-rebuild-states-v8`

V8 is a reversible review draft. V7 remains immutable; Final/runtime wiring is
unchanged.
