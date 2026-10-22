# Kitchen Dishwasher Ligne-Claire V3

Date: 22 October 2026

Status: immutable reversible review candidate; not approved, registered,
promoted, selected as current or wired to production/runtime.

Review route: `/keeper-review/kitchen-dishwasher-ligne-claire-v3/index.html`

## Outcome

V3 supersedes the rejected Dishwasher V1 drawing and the retained V2 audit.
It uses the approved V41 dishwasher as the sole semantic and geometric
authority and the approved Oven V8 as the line-quality authority. The pack
contains Off, On and Broken states plus all four left/right adjacency variants:
15 candidates on the exact V41 `98 × 82 px` canvases.

## Geometry and ghost audit

Every candidate reuses its corresponding V41 alpha channel byte-for-byte.
Canvas, opaque bounds, transparent padding, silhouette, placement, door,
carcass, perspective, footprint, anchors, pivots, attachment points and
collision envelope are therefore fixed. A current/candidate alpha ghost is
included for every state and edge variant.

The only authorised internal geometry change is the Broken handle: its right
attachment hangs farther down, while the door and carcass remain locked. The
pack includes a separate native-size 64 px proof so line quality is judged at
game scale rather than through browser interpolation.

## One control panel

Off, On and Broken share one physical control-panel drawing and coordinates:

- LCD at upper left;
- selector at upper right;
- tiny status lamp immediately to the selector's right.

Only state indication changes: dark/off, cyan display plus green lamp/on, and
fault display plus red lamp/broken. Nothing floats on the door front.

## Continuous worktop run

The V41 turquoise cap still looked visibly separate from the approved fitted
cabinet family when ghosted into the complete kitchen. V3 therefore copies the
approved Cabinet V3 worktop RGB byte-for-byte across source rows `4–15`, using
the matching left/right exposed or joined cap for each adjacency variant. The
V41 alpha is reapplied afterwards. The evidence pack includes a full-run ghost
and a control-panel invariance sheet. The rejected V2 cyan-cap audit remains
immutable and is not overwritten.

## Behaviour invariants

This is image-only review work. V41 movement, swapping, Broken-state movement
lock, repair unlock, animation timing, interaction, handling, effect ownership
and countertop healing are not changed. No game controller, room layout,
collision file, selector, Final asset or production file is written.

## Verification

```sh
npm run verify:kitchen-dishwasher-ligne-claire-v3
npm run maintain:keeper-review
npm test
npm run build
```

The dedicated verifier requires all 15 exact canvases and alpha channels, one
invariant panel geometry, exact approved worktop-cap pixels and a closed
registration gate.

## Approval and rollback

`batch-register.json` remains closed: `register:false`, `promote:false`, no
current-selector changes and no production writes. Explicit approval is
required before registration.

Rollback is immediate: discard only the V3 draft, review shell, archive set,
new content-addressed objects, builder and this record. V1, V2, V41 and every
approved/current or production asset remain byte-for-byte unchanged.
