# Kitchen Oven Broken Ligne-Claire V9

Date: 21 October 2026  
Status: immutable reversible Broken/flicker review gate; not approved, not
registered, not promoted and not runtime-wired

Review route:

`/keeper-review/kitchen-oven-broken-ligne-claire-v9/`

## Purpose

V9 applies the exact approved V8 Oven On drawing language to the existing
Broken state and both inherited complete-oven flicker strips. It does not
change the dishwasher or any previously approved asset.

The Broken drawing keeps the complete V8 hob, two burners, stacked orange hob
control, cream body, blue plinth, frontal cutaway perspective and confident
near-black contour language. Only the inherited Broken semantics differ: the
door remains attached on its bottom hinge and opens straight toward the player,
its glass remains translucent, the roast is blackened, the failed third dial
hangs on exactly two wires, and the red warning lamp remains present.

The generated Broken source is `1305 × 1205` RGBA at SHA-256
`606cb99919eb7267936fd5e3d0bb6585d183569d21273a3a734ed1a5ffadbef9`.
It is mapped once through the measured safe crop `(121,109)–(1204,1058)` to a
`736 × 680` registered master, then once to the exact inherited `92 × 85`
canvas. Every Broken static state and every strip frame has the same alpha,
outer bounds `(4,4)–(88,81)` and transparent shared-edge gutter. The approved
V8 On candidate is copied byte-for-byte at SHA-256
`0ee7572ec03021a7efb747254bc97974de380cdee45a49d47e74b7aba9fd3d80`.

## Lighting and timing

The four fixed registered Broken states are dark, cavity-lit, warning-lit and
both-lit. Lighting is a deterministic colour transform inside compact
shape-following cavity and lamp masks; it never redraws, moves or resizes a
part. Both complete strips reuse those fixed images, so no frame can wobble.

The exact current 40-frame schedules are measured from the V41 source strips
and replayed at the unchanged 4 fps / ten-second contract. Cavity and warning
remain independent complete-oven swaps. Movement locks, repair unlocks,
interaction, handling, state transitions and all effect attachment rules are
inherited and hash-pinned.

## Separate Broken symbology

Frank supplied two comic references for coloured stars, a spiral, small radial
bursts and short agitation marks as readable Broken-state language. V9 includes
one optional `92 × 40` effect layer made from original flat spot-colour marks:

`candidates/oven/fx-oven-broken-symbols.png`

It is a separate owner attached to `anchorAssetId: oven` at oven-local offset
`(0,-37)`. It is not baked into any oven, flicker frame, collision, alpha
footprint or healing layer and must be removed independently when Broken is
healed. The review player can switch it off. This is a review candidate, not a
new runtime behaviour.

Two image-generated symbol attempts are retained as explicit rejection
provenance because they introduced glow/gradients and did not supply the
required agitation marks. The accepted effect is a deterministic flat-colour
master with no glow, gradient or soft modelling.

## Image-generation provenance

The built-in image generator was used in edit/reference mode.

- Broken source input 1: the exact V8 user-confirmed Oven On visual authority.
- Broken source input 2: the earlier three-state Broken oven as structural
  reference only.
- Broken prompt: preserve V8 construction and drawing identity; change only to
  the inherited open-door, burnt-roast, two-wire failed-dial and warning-lamp
  state; omit all baked smoke, sparks, scenery and text.
- Saved project source:
  `art/source/kitchen-oven-broken-ligne-claire-2026-10-21-v9/oven-broken-generated-source.png`.
- Symbol references: Frank's two supplied comic examples. The generator's two
  glowing results are retained under `rejected-symbol-attempts/`; the accepted
  symbol layer was rebuilt deterministically to meet the flat opaque contract.

## Healing, placement and scope

Room proof uses the approved V3 fitted-family candidates and the existing V41
compositor rules. Oven datum remains `(slot x - 4, 127)`; sink datum remains
`(slot x - 4, 104)`. Body backfill, triangular oven underlay, flat countertop
caps and left/right cleanup masks retain their exact order and hashes. All
dishwasher images and adjacency variants are hash-pinned and reused directly
from V41; V9 creates no dishwasher candidate.

The complete current-versus-candidate contact sheet covers all four static
Broken images plus eight labelled samples from both 40-frame strips. The review
page also includes the V8/V9 family sheet, exact-datum room proof, separate
symbol-layer proof and synchronized current/V9 playback. It uses only
root-absolute `/keeper-review/.../assets/...` URLs and decodes every evidence
image and strip before enabling playback or controls.

`batch-register.json` is closed. No source, Final, production, selector or
runtime file is changed. Approval is required before any candidate can become
current. Rollback is immediate by discarding only the V9 draft, source and
review directories plus its builder and this record.

## Verification

```bash
npm run verify:kitchen-oven-broken-ligne-claire-v9
npm run maintain:keeper-review
npm test
npm run build
```

