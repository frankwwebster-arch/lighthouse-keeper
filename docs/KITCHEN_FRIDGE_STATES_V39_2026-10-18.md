# Kitchen V39 from-scratch fridge correction

Date: 18 October 2026
Status: historically approved, then superseded by clean-slate Rebuild V1; unpromoted/unwired
Review: `/keeper-review/kitchen-fridge-states-v39/`

V39 historically replaced rejected V32 as the active fridge review candidate.
It does not repair or reuse V32 fridge pixels. Frank approved it before later
rejecting the broader asset-by-asset kitchen method; it remains immutable
historical evidence rather than the current construction authority. Standard
and broken were redrawn together from scratch using the approved room only as
a style, projection, palette and measurement reference.

The standard state fills the exact 21-lp bay: x=84–168 and y=140–218 in the
772 × 224 room. The broken state uses the same construction. Its top hinge has
failed; one compact lower-right hinge arm visibly connects the fallen door to
the carcass; the door's lower-left corner reaches the measured y=218 floor;
and the pale-cyan pool is flattened onto that floor and extends into the
foreground. The cavity contains generic milk, jar and produce shapes. Each
state contains one bottom grille only.

The compositor now clears every old-fridge face and grille pixel before adding
one new state. A dedicated cleared-bay proof exposes that intermediate stage.
This prevents the duplicate appliance/grille defect in V32.

The object and pool remain static. A separate effect-only 40-frame strip adds
a slow falling drip and restrained floor ripple at 4 fps for ten seconds. The
page shows that strip alone before showing it over the broken state. The named
sound placeholders remain `kitchen_fridge_low_electrical_buzz_loop` and
`kitchen_fridge_water_drip_slow`; there is no visible electrical effect.

## Rejection boundary

Frank withdrew V32's earlier visual approval after inspecting the deployed
page and rejected V32–V38 on 18 October 2026. V32's pool appeared above the
floor because the replacement was not registered to the room's actual y=218
floor surface, and old-fridge pixels survived underneath, producing duplicate
grilles. V33–V38 are also rejected for state/effect visibility, incorrect
placement, duplicate underlying assets, colour drift or chair occlusion. Their
files remain immutable provenance; they are not active candidates.

Work is again one asset at a time. The kettle remains blocked until Frank has
visually reviewed V39.

## Verification

- Rebuild: `scripts/build_kitchen_fridge_states_v39.py`
- Focused gate: `npm run verify:kitchen-fridge-states-v39`
- Archive gate: `npm run archive:keeper-review` then
  `npm run verify:review-archive`
- Full gates: `npm test`, `npm run typecheck`, `npm run build`

The deterministic gate checks source hashes, transparent cell gutters, exact
bay/floor registration, complete removal of the earlier white fridge, the
connected hinge/floor pool evidence, 40 isolated effect frames, room geometry,
preload/decode locking and the Final/runtime boundary.

Documentation audit completed against the selected source hashes, native
sprites, cleared-bay proof, room composites, review archive, rejection record,
route configuration and no-promotion boundary. The 123-set/2,558-reference
archive verifies at 49.93 MiB public payload; all 179 repository tests,
TypeScript and the production Next.js build pass.
