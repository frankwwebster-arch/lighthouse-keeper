# Kitchen Rebuild States V6 — switchable variable-speed effect workbench

Date: 18 October 2026

V6 adds an independent saved enable/disable switch for each effect family. The
fridge drip starts disabled; every family remains user-switchable. Broken-oven
smoke, fascia warning flicker and internal cavity-light flicker are three
separate compatible layers which can run at once. The two light layers are
locked to the oven rather than freely repositionable. The cavity illumination
uses the On-state light treatment, flickers on/off, and preserves a permanently
burnt, blackened roasting item in the amended Broken object.

Every source remains exactly 40 frames at 4 fps: a canonical ten-second loop.
The speed control changes only playback time, from 0.1× to 4×, and reports the
effective duration. Speed is stored with position, size and crop values in
browser local storage and in exported placement JSON. It never resamples,
shortens or overwrites a source strip.

Route: `/keeper-review/kitchen-rebuild-states-v6/`
Build: `python scripts/build_kitchen_rebuild_states_v6.py`
Verify: `npm run verify:kitchen-rebuild-states-v6`

All other V5 state/effect media remain byte-identical. V6 is a reversible
review draft. Final/runtime wiring remains unchanged; V5 remains immutable.
