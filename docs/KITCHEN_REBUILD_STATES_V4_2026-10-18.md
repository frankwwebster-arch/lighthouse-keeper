# Kitchen Rebuild States V4 — variable-speed effect workbench

Date: 18 October 2026

V4 preserves every V3 state object, effect model and placement capability. It
adds the approved slow-fly loop as an eleventh reusable effect family and adds
an independent saved playback-speed multiplier to every model.

Every source remains exactly 40 frames at 4 fps: a canonical ten-second loop.
The speed control changes only playback time, from 0.1× to 4×, and reports the
effective duration. Speed is stored with position, size and crop values in
browser local storage and in exported placement JSON. It never resamples,
shortens or overwrites a source strip.

Route: `/keeper-review/kitchen-rebuild-states-v4/`
Build: `python scripts/build_kitchen_rebuild_states_v4.py`
Verify: `npm run verify:kitchen-rebuild-states-v4`

V4 is a reversible review draft. Final/runtime wiring remains unchanged.
