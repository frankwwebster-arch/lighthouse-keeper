# Kitchen V41 exact-size oven states

Date: 18 October 2026  
Status: awaiting Frank's visual review; unpromoted/unwired  
Review: `/keeper-review/kitchen-oven-states-v41/`

V41 supersedes rejected V40 as the only active oven gate. V40 was too tall,
not broad enough in proportion, and its smoke rose as discrete bubbles. V41
keeps V40 immutable and re-establishes the initially approved V21 oven as the
binding measurement and colour authority.

## Exact measurement and colour contract

The V21 authority is an exact `108 × 120 px` cell with exclusive opaque bounds
`[12,31,96,108]`: precisely `84 × 77 px`. All three V41 states use that same
cell and same footprint. In the native `772 × 224 px` room the footprint is
x=`336–420`, y=`131–208`, with the fitted cabinet plinth continuing below it.

The complete approved hob and sea-glass surround—V21 rows `31:48`—are copied
byte-for-byte into Off, On and Broken. The redrawn lower fascia is normalized
to the remaining `84 × 60 px` and every generated fascia colour is selected
from a 48-colour palette derived from visible V21 oven pixels. The old oven and
hob are fully cleared before any V41 state is inserted.

Off has upright controls, a dark indicator and dark cavity. On has turned
dials, a red indicator, warm interior light and roasting tin. Broken keeps the
door attached and askew; the failed right rotary dial hangs from its empty
socket by two wires.

## Separate effects

The three objects are static. Broken uses three independent reusable
`40`-frame, `4 fps`, ten-second strips:

- a connected, curling, semi-transparent smoke stream made without circular
  puff/bubble primitives;
- two flame clusters anchored to the exact retained hob burners;
- irregular rapid red warning bursts with five occasional cavity flickers.

Named SFX placeholders remain:

- `kitchen_oven_on_fan_loop`
- `kitchen_oven_broken_smoke_hiss_loop`
- `kitchen_oven_hob_flame_loop`
- `kitchen_oven_broken_warning_light_angry_blink_loop`

## Boundary and verification

V41 changes no approved fridge, Final art or runtime wiring. V40 remains
immutable rejected provenance. No later kitchen asset may proceed until V41 is
visually reviewed.

- Rebuild: bundled Python plus `scripts/build_kitchen_oven_states_v41.py`
- Focused gate: `npm run verify:kitchen-oven-states-v41`
- Archive gate: `npm run archive:keeper-review` then
  `npm run verify:review-archive`
- Full gates: `npm test`, `npm run build`, `npm run typecheck`

The focused verifier pins all source/authority hashes; exact state and room
geometry; byte-identical hob rows; approved-palette membership; cleared-bay
construction; state semantics; frame gutters, geometry, density and
uniqueness; a single connected smoke component in every frame; the absence of
ellipse/bubble primitives from the smoke builder; effect anchors; warning
timing; preload/decode locking; and the no-promotion boundary.

Documentation audit completed against the V21 measurement/colour authority,
V39 approved room hash, V40 rejection, V41 source, native outputs, page,
archive manifest and route. The final archive verifies at 127 sets, 2,684
references and 1,767 immutable objects with a 49.96 MiB public payload. All
179 repository tests, the production Next.js build and the sequential
TypeScript check pass.
