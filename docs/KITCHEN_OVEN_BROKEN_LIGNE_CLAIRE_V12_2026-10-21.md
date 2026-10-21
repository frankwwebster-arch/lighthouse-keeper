# Kitchen Oven Broken Ligne-Claire V12

Status: approved visual authority; immutable, not promoted or runtime-wired.

Review route: `/keeper-review/kitchen-oven-broken-ligne-claire-v12/`

## Decision

V8 On remains the approved and immutable oven authority. V12 rebuilds Broken
from those exact pixels instead of treating V9/V10 as a second oven model.
Only three local state cues differ: the third dial is detached on exactly two
short wires, the roast is burnt without changing its silhouette or tray, and a
shallow perspective gap under the unchanged handle shows that the door is
slightly ajar rather than fully horizontal.

This is the lower-risk direction because it does not reopen or replace an
approved On asset. V9 and V10 remain untouched historical review candidates.

## Hard invariants

- Canvas stays `92 × 85`; alpha bounds stay `(4,4)–(88,81)`.
- V8 On is copied byte-for-byte.
- V12 Broken uses V8's exact alpha channel in every static state and every
  animation frame.
- Outside the three declared native masks, V12 both-lit Broken and V8 On have
  zero differing pixels.
- Cabinet silhouette, blue top, cream body, plinth, burners, two intact dials,
  warning lamp, window, tray, anchor and datum remain V8-derived.
- Both inherited flicker strips remain 40 frames at 4 fps with the current
  timing schedules.
- The symbol layer remains separate, byte-identical and independently removed
  by repair.
- Dishwasher assets, adjacency variants, collision, movement locks, repair
  unlocks, interaction and V3 healing/backfill order are unchanged.

## Review evidence

The review page contains a live opacity ghost between V8 On and V12 Broken,
the complete static/animated contact sheet, room healing proofs and the
separate symbol evidence. All review URLs are root-absolute to survive
Vercel's slashless canonical route, and all images decode before controls are
enabled.

The image-generator edit attempt is retained only as rejected provenance; it
globally changed the cabinet and opened the door too far, so none of its pixels
are used by V12.

## Approval and rollback

Frank approved the exact V12 family on 22 October 2026. The separate approval
record registers that decision without rewriting the immutable review pack:
`docs/review/kitchen-oven-broken-ligne-claire-v12-approval-2026-10-22.json`.
`batch-register.json` therefore remains closed with `register:false`,
`promote:false` and no selector changes. Rollback of the decision is immediate:
remove only the approval record; every V12 review byte remains preserved.

## Verification

```sh
npm run verify:kitchen-oven-broken-ligne-claire-v12
npm run verify:kitchen-oven-broken-ligne-claire-v12-approval
npm run maintain:keeper-review
npm test
npm run build
```

## Documentation audit

README, STATUS, DECISIONS, package scripts, this record and the immutable
machine-readable manifest identify V8 On and V12 Broken as approved visual
authorities. V12's manifest remains an accurate pre-approval snapshot. No
production selector, source, Final or runtime claim changed.
