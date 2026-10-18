# Kitchen Rebuild States V5 — variable-speed effect workbench

Date: 18 October 2026

V5 preserves every V4 state object, effect model, source pixel and placement
capability exactly. It corrects the review-boundary copy inherited by V4 so
that the displayed version and rollback directory are both accurately V5.

Every source remains exactly 40 frames at 4 fps: a canonical ten-second loop.
The speed control changes only playback time, from 0.1× to 4×, and reports the
effective duration. Speed is stored with position, size and crop values in
browser local storage and in exported placement JSON. It never resamples,
shortens or overwrites a source strip.

Route: `/keeper-review/kitchen-rebuild-states-v5/`
Build: `python scripts/build_kitchen_rebuild_states_v5.py`
Verify: `npm run verify:kitchen-rebuild-states-v5`

V5 is a reversible review draft. Final/runtime wiring remains unchanged; V4
remains immutable provenance.
