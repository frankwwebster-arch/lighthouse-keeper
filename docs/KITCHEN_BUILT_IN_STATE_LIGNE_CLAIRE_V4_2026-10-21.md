# Kitchen Built-In State Ligne-Claire V4

Date: 21 October 2026

Original immutable review: `/keeper-review/kitchen-built-in-state-ligne-claire-v4/`

Corrected review delivery: `/keeper-review/kitchen-built-in-state-ligne-claire-v4-delivery-v2/`

Status: complete immutable static review candidate; not approved, registered,
promoted, wired or current.

The original page's archived image URLs returned external redirects that the
review surface did not display. Delivery V2 preserves that page and every V4
byte, while a fresh page and asset prefix serve the same four evidence objects
through hash-verified same-origin responses. See
`docs/KITCHEN_BUILT_IN_STATE_LIGNE_CLAIRE_V4_DELIVERY_V2_2026-10-21.md`.

## Purpose and boundary

Frank approved the exact V3 fitted-cabinet static evidence, then requested that
the same recipe be applied to built-in On and Broken assets without disturbing
healing. V4 is a new dated pack. It does not rewrite V3 or any V41 source,
production asset, controller, selector or effect.

Small countertop objects remain outside scope. A generated calibration board
was rejected because it recomposed the sink; no generated pixel or that board
is present in V4.

## Candidate coverage

V4 contains seventeen deterministic RGB-only candidates:

- oven On;
- oven Broken, cavity-lit, warning-lit and both-lit;
- both complete 40-frame Broken-oven lighting strips;
- dishwasher On and Broken base assets;
- all four left/right exposed/joined variants for each dishwasher state.

The already approved V3 fridge Standard/Broken, sink On/Broken bases, Cabinet
A/B variants and five healing layers are hash-pinned and reused byte-for-byte.
The six separate drip, water and suds effect strips are also hash-pinned and
unchanged.

## Geometry and state lock

The builder changes RGB only. Every new candidate keeps its exact source canvas,
alpha bytes, alpha bounds and transparent padding. The oven strips remain 40
cells of 92 × 85 pixels at 4 fps. Every dishwasher state remains in its 98 × 82
cell, and every edge variant is built directly from its matching source.

Functional aqua/green On indicators and red/amber fault indicators retain
their source coordinates. Doors, failed hinges, racks, controls, hob, dangling
dial, handles, cavities, contents and damage cues retain their exact shapes.

The static room proof records the sink datum explicitly as `(slot x - 4, 104)`
for every arrangement and fails verification if it changes. No room proof or
candidate is permitted to move the sink.

## Healing, movement and repair behavior

V4 pins the approved V41 catalogue, approval and verifier. The following remain
unchanged:

- exact 84-pixel bay origins and pair-aware join selection;
- all dishwasher left/right exposed/joined healing variants;
- body backfill, flat cap, oven-triangle and neighbour seam-cleanup layers;
- occupied-slot swapping and the complete 720-layout healing contract;
- position lock for every Broken movable asset;
- rejection of direct moves, swaps or group moves that displace Broken assets;
- repair to a non-Broken state as the only movement unlock;
- asset-local effect anchors and ownership;
- animation frame order, 4 fps timing and state transitions.

No runtime or gameplay file is modified.

## Static review evidence

Because the interactive reviewer was unreliable, the static sheets are the
approval surface:

- complete On/Broken room-and-healing comparison across four arrangements;
- oven source/candidate state sheet;
- dishwasher source/candidate sheet containing both states and every edge
  variant;
- eight-frame sampling of each 40-frame Broken-oven lighting strip.

Contact sheets use smooth Lanczos enlargement and the page uses normal browser
interpolation. Pixelated review scaling is rejected by verification.

## Verification

```sh
npm run verify:kitchen-built-in-state-ligne-claire-v4
npm run verify:kitchen-fitted-cabinet-ligne-claire-v3
npm run verify:kitchen-dishwasher-workbench-v41
npm run verify:kitchen-split-cabinet-workbench-v38
npm run maintain:keeper-review
npm test
npm run typecheck
npm run build
```

## Approval and rollback

`batch-register.json` keeps registration and promotion false with no selector
changes. Explicit approval is required before V4 can become current.

Rollback is immediate: discard only
`art/drafts/kitchen-built-in-state-ligne-claire-2026-10-21-v4/` and the matching
review set. Approved V3, all source/current/production files, runtime behavior
and selectors remain byte-for-byte in place.
