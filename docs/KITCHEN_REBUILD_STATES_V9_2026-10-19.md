# Kitchen Rebuild States V9 — irregular failing-bulb timing

Date: 19 October 2026

Frank approved the corrected V8 Broken-oven geometry on 19 October 2026. V9
preserves that oven, its straight-toward-camera door, transparent window, burnt
roast, registration and every unrelated asset byte-for-byte. It changes only
the timing of the three internal-light full-state strips.

The lamp now reads as an intermittent electrical fault rather than an orderly
pulse. Each model mixes uneven dark holds, isolated quarter-second flashes,
short two- and three-frame sputters and an irregular terminal flutter. No model
contains a repeating cadence of ten frames or fewer. The choices are named
`Random`, `Sputtering` and `Near Blow`; `Random` is the default.

The source contract remains 40 frames at 4 fps for a canonical ten-second
loop, with 0.1×–4× playback control. Every lit cell is the exact complete V8
lit Broken oven and every dark frame is transparent so the exact V8 dark oven
shows beneath it. All cells retain two transparent gutter pixels on every edge.

All V8 asset-first controls, independent smoke/warning/internal-light layers,
removal, persistence and JSON export remain unchanged.

Route: `/keeper-review/kitchen-rebuild-states-v9/`

Build: `/usr/bin/python3 scripts/build_kitchen_rebuild_states_v9.py`

Verify: `npm run verify:kitchen-rebuild-states-v9`

V9 is a reversible review draft. V8 remains immutable; Final/runtime wiring is
unchanged.
