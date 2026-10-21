# Kitchen Oven Broken Ajar Ligne-Claire V15

Status: immutable reversible review candidate; not approved, registered,
promoted or wired.

Review route: `/keeper-review/kitchen-oven-broken-ajar-ligne-claire-v15/`

## Decision

V15 keeps approved V12 as the oven-family authority while making the Broken
door visibly physical and ajar. It retains V12's body, countertop, burners,
controls, failed dial, burnt roast, plinth, canvas and datum, and applies only
the established V10 moderate part-open attached-door geometry inside the
declared door/cavity locality.

The preceding V14 proof is retained unchanged as rejected provenance: its
foreshortened glass read as a displaced handle rather than a physical door.

## Hard invariants

- Every candidate cell remains exactly `92 × 85`, with alpha bounds
  `(4,4)–(88,81)` and the exact approved V8/V12 alpha bytes.
- The door remains attached to the same bottom hinge and stays inside the
  existing oven footprint; it is part-open, not horizontal or detached.
- All four Broken lighting states share one fixed geometry.
- Both flicker strips remain exactly 40 frames at 4 fps with their inherited
  lighting schedules.
- The separate comic fault-symbol effect is copied byte-for-byte from approved
  V12 and is still removed independently when the oven heals.
- Oven and sink datums, anchors, pivots, collision, movement locks,
  interactions, repair unlocks and the V3/V41 healing process are unchanged.
- Approved V8/V12, V13 Off, all dishwasher files, source, production, Final and
  runtime files remain untouched.

## Review and rollback

The review page uses root-absolute asset URLs and decodes every image before
enabling opacity or playback controls. It provides an approved-V12/V15 family
comparison, a live opacity ghost, every static lighting state and samples from
both complete strips.

`batch-register.json` remains closed (`register:false`, `promote:false`, no
selector changes). Rejection is immediately reversible by discarding only the
V15 draft, builder, review route and this record.

## Verification

```sh
npm run verify:kitchen-oven-broken-ajar-ligne-claire-v15
npm run maintain:keeper-review
npm test
npm run build
```

## Documentation audit

README, STATUS, DECISIONS, package scripts and this delivery record agree that
V8 On and V12 Broken remain approved authorities, V13 Off remains an
unapproved candidate, V14 is rejected provenance and V15 is the new closed
review candidate. No runtime or production selector changed.
