# Kitchen Dishwasher Ligne-Claire V7

Status: immutable review candidate; not approved, registered, promoted or wired.

Review: `/keeper-review/kitchen-dishwasher-ligne-claire-v7/index.html`

V7 supersedes V6 because V6 retained V5's faulty image-reference crop. Sparse
near-transparent generation pixels above the visible appliance enlarged the
crop and lowered the appliance's own blue top trim. The exact cabinet worktop
was then overlaid above it, leaving a rejected second turquoise strip in Off,
On and Broken.

## Correction

- Source bounds are derived at alpha `>= 16`, with a two-source-pixel safety
  pad; retained RGBA and antialiasing are otherwise unchanged.
- The one exact Cabinet V3 worktop remains rows `4–16`. The cream fascia now
  begins directly beneath it, with no second turquoise worktop layer.
- The correction applies to all fifteen Off/On/Broken and join variants.
- Broken retains V6's good reference-led construction: wider-open door, failed
  lower-right hinge, attached lower-left hinge, one-ended hanging handle and no
  unexplained bolt.
- The V41 `98 × 82 px` canvases and alpha channels, cabinet-side shoulders,
  movement, locks, repair, healing and separate suds effect remain exact.
- Production and approved/static assets remain unchanged.

## Verification

```sh
npm run verify:kitchen-dishwasher-ligne-claire-v7
```

The verifier checks all canvases and alpha channels, exact worktop and cabinet
shoulders, the cream fascia band immediately below the worktop in every state,
departure from rejected V6 bytes, archive integrity and the closed gate.

Rollback removes only the V7 source-reference directory, draft, public shell
and archive-set file.
