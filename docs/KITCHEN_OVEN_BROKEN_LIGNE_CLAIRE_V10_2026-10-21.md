# Kitchen Oven Broken Ligne-Claire V10

Status: immutable review candidate; not approved, registered, promoted or wired.

Review route:

`/keeper-review/kitchen-oven-broken-ligne-claire-v10/`

## Outcome

V10 is the narrow successor to V9 requested after review. It changes only the
Broken oven door presentation: the door remains attached to the same lower
hinges but is moderately part-open rather than fully horizontal. V9 remains
byte-for-byte untouched and immediately available for rollback/comparison.

The approved V8 On candidate is still copied byte-for-byte. The Broken oven
retains the full blue countertop contour, burners, orange control, cream body,
two intact dials, one failed dial hanging on exactly two wires, red warning
lamp, cavity, racks, burnt roast and tray. The selected door keeps its cream
frame, orange handle and genuine transparent glass.

## Preserved contracts

- Every oven cell remains exactly `92 × 85` with alpha bounds
  `(4,4)–(88,81)` and transparent shared-edge gutters.
- Both complete flicker strips remain `40` frames at the inherited `4 fps`.
- The V9 master is copied exactly above source row `472`; after registered
  LANCZOS filtering, native rows `0–55` remain byte-identical to V9. Only the
  lower attached-door band and its necessary filter edge differ.
- All Broken states and every strip frame are derived from fixed registered
  masters, so the door and body cannot wobble between lighting states.
- Oven datum remains `(slot x - 4, 127)` and sink datum remains
  `(slot x - 4, 104)`.
- V3 healing/backfill/cap/cleanup order and hashes are unchanged.
- V41 dishwasher images, adjacency variants, movement locks, repair unlocks,
  interaction and healing contracts are unchanged.
- The V9 comic fault effect is copied byte-for-byte: `92 × 40`, oven-anchored
  at local offset `(0,-37)`, never baked into oven/collision/flicker pixels and
  removed independently on repair.
- No source, production, Final, selector or runtime file was overwritten.

## Image-generation provenance

The built-in image generator was used in edit/reference mode.

- Edit target: the exact V9 high-resolution Broken source.
- Prompt: change only the attached door from fully horizontal to a moderate
  one-third-open angle; preserve every other oven part, front perspective,
  palette, line language and transparent canvas; add nothing and avoid blur,
  pixelation, glow, gradients, texture, scenery and text.
- Selected project source:
  `art/source/kitchen-oven-broken-ligne-claire-2026-10-21-v10/oven-broken-part-open-generated-source.png`
  (`1306 × 1205`, SHA-256
  `9cb31501682b731de5e040800ae27c57ea3a6b626d54668585d4e3a256c3262f`).
- One more-closed generated variant is preserved as rejected provenance under
  `rejected-generated-attempts/`; it was not used.
- The generated door glass colour was visually correct but its alpha was
  flattened. The builder restores transparency with one deterministic
  door-glass-only alpha mask while preserving the ink/frame pixels. The same
  alpha is then reused in every static and animated state.

## Key hashes

- Immutable V9 fully-open Broken candidate:
  `6a80b176b6e5964e1c669e483fe1d99199d0e5aa12ad20a0af1ee8b39a81a411`
- V10 part-open Broken candidate:
  `71093271eb36c4ab59cab0f75aaf132a9019091219d6b44f6389fab390da19ea`
- V8 On candidate copied unchanged:
  `0ee7572ec03021a7efb747254bc97974de380cdee45a49d47e74b7aba9fd3d80`
- V9/V10 symbol effect copied unchanged:
  `46d867d1b2ca08aca8329adb38a39c65259743a7eccf60b0a557689d00e421e7`

The complete source/candidate table, every candidate hash, alpha hash,
animation schedule, inherited contract hash, room proof and evidence hash is
recorded in:

`art/drafts/kitchen-oven-broken-ligne-claire-2026-10-21-v10/manifest.json`

## Approval and rollback

`batch-register.json` is closed with `register:false`, `promote:false` and no
selector changes. Explicit Frank approval is required before any V10 candidate
can become current.

Rollback is immediate: discard only the V10 source directory, draft pack,
builder, review route and this delivery record. V9 and every earlier approved,
source, production and runtime asset remain intact.

## Verification

```sh
npm run verify:kitchen-oven-broken-ligne-claire-v10
npm run maintain:keeper-review
npm test
npm run build
```

The review page uses root-absolute asset URLs so Vercel's slashless canonical
route cannot misresolve media. Playback controls remain disabled until every
unique evidence image, both current strips, both V10 strips and the symbol
layer have loaded and decoded.

## Documentation audit

README, STATUS, DECISIONS, package scripts, this delivery record and the
machine-readable manifest agree that V8 On is approved, V9 remains immutable
and unregistered, V10 is the new part-open-door candidate, and no gameplay or
production registration has occurred.
