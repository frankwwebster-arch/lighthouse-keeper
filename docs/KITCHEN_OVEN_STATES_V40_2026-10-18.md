# Kitchen V40 from-scratch oven states

Date: 18 October 2026
Status: rejected by Frank; immutable unpromoted/unwired provenance
Review: `/keeper-review/kitchen-oven-states-v40/`

Frank approved exact Fridge V39 and released the oven as the next single-asset
gate. V40 historically replaced rejected V35, but is now itself rejected. It
does not repair, composite over or reuse V35 oven pixels.

> Rejection update, 18 October 2026: Frank rejected V40 because the oven was
> too high and insufficiently wide in proportion, while its smoke rose as
> bubbles. The successor must use the initially approved oven's exact measured
> size and colours and must retain the hob. V41 is the active correction. V40
> remains unchanged as provenance; see
> `docs/review/kitchen-oven-states-v40-rejection-2026-10-18.json`.

Off, On and Broken were drawn together from the same new construction in the
approved storm-blue, sea-glass and copper kitchen language. Each state fills
the exact oven bay at room `x=336–420`, `y=123–218`. Before inserting a state,
the compositor replaces the complete previous hob, controls, cavity and door
with clean fitted-galley surfaces. The review exposes this cleared-bay stage.

Off has upright dials, no interior light and a dark indicator. On has turned
dials, a red indicator, warm interior light and a readable roasting tin.
Broken keeps its door physically attached but askew. Its right rotary dial has
failed: the empty fascia socket is visible and the dial hangs below it from two
short wires.

The three oven objects are static. Broken-state billowing smoke, two clear hob
flame clusters and an angry warning-light layer are separate effect-only
`40`-frame strips at `4 fps`, giving ten-second loops. The warning strip fires
the red indicator in irregular rapid bursts and flickers the internal amber
light only five times in forty frames. All share a `120 × 144` transparent
cell, retain safety gutters and are shown alone, with the isolated oven, and at
exact `772 × 224` game scale. Named sound placeholders are:

- `kitchen_oven_on_fan_loop`
- `kitchen_oven_broken_smoke_hiss_loop`
- `kitchen_oven_hob_flame_loop`
- `kitchen_oven_broken_warning_light_angry_blink_loop`

## Boundaries

V40 is rejected provenance only. It changes no Final art, runtime wiring,
approved V39 fridge pixels or rejected V35 provenance. V41 is the active oven
gate; kettle, toaster, bowl, basin and table work remains blocked until V41 has
been visually reviewed.

## Verification

- Rebuild: bundled Python runtime plus
  `scripts/build_kitchen_oven_states_v40.py`
- Focused gate: `npm run verify:kitchen-oven-states-v40`
- Archive gate: `npm run archive:keeper-review` then
  `npm run verify:review-archive`
- Full gates: `npm test`, `npm run build`, `npm run typecheck`

The deterministic gate checks both generated source hashes, approval of V39,
hard-alpha cell gutters, identical exact bay bounds, complete removal of the
old oven/hob, distinct Off/On lighting, the hanging-dial location, four named
SFX cues, exact room geometry, 40 isolated frames in each of the three effect
strips, warning/flicker timing, effect density and uniqueness, preload/decode
locking and the no-promotion boundary.

Documentation audit completed against the V39 approval hashes, both V40 source
hashes, native sprites, cleared-bay proof, room composites, ten archived review
images, route configuration and no-promotion boundary. The 125-set/
2,611-reference archive verifies at 49.95 MiB public payload; all 179 repository
tests, TypeScript and the production Next.js build pass.
