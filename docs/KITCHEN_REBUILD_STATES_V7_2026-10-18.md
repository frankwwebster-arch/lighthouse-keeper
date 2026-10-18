# Kitchen Rebuild States V7 — asset-first animation builder

Date: 18 October 2026

V7 replaces V6's effect-first controls with an appliance-first workflow. Choose
Fridge, Kettle, Toaster, Oven, Mixing bowl, Basin tap or Bin; the complete
native-size kitchen then shows that asset's Broken state with every other asset
Standard. Drag any compatible animation family from the library onto the
kitchen, or click it for a sensible starting position. An asset may own any
number of effect instances, including multiple copies of the same reusable
family.

Each applied animation is independently selectable and removable. Its model,
0.1×–4× playback speed, x/y position, width, height and four-sided crop can be
edited and are persisted in browser local storage and exported as JSON. The
fridge starts without the rejected drip. Oven smoke stays movable; warning-dot
and cavity-light flickers are separate removable layers but remain registered
to the exact oven coordinates. Defaults retain kettle steam, toaster smoke,
oven smoke plus both lights, basin spray, and approved bin smell plus flies.

All effect media are byte-identical to V6. Every source strip remains exactly
40 isolated 120×144 cells at 4 fps—a canonical ten-second loop. Speed changes
playback only. The page preloads and decodes every unique source before enabling
its controls.

Route: `/keeper-review/kitchen-rebuild-states-v7/`

Build: `python scripts/build_kitchen_rebuild_states_v7.py`

Verify: `npm run verify:kitchen-rebuild-states-v7`

V7 is a reversible review draft. V6 remains immutable; Final/runtime wiring is
unchanged.
