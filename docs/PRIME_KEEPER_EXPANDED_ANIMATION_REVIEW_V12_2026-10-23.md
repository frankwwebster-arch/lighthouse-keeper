# Prime Keeper expanded animation review V12

Date: 23 October 2026

Status: all ten animations approved by Frank on 23 October 2026 as exact,
hash-pinned review authorities. Approval is recorded externally at
`docs/review/keeper-prime-morning-drafts-v12-approval-2026-10-23.json` so this
immutable V12 review pack remains unchanged. No V12 frame was installed in the
runtime animation bank by the approval-recording change.

Routes:

- current review: `/prime-keeper-animation-drafts`
- immutable V12 permalink: `/prime-keeper-animation-drafts-v12`

## Correction

V11 restored complete arm silhouettes, but the transferred arm layers retained
their original inner sleeve and jumper edges. Those lines cut into the fixed
torso at both sides, breaking the blue body and cream stripe.

V12 removes the incompatible layer join. Rear-task positions 11–31 now reuse
complete frames 2–8 from the existing `Cook at counter` sequence byte-for-byte:

- each pose is one intact drawing from cap to boots;
- no arm, sleeve, stripe, torso or hem pixels are composited separately;
- the seven intact poses repeat as three work cycles;
- every replacement remains 256 × 320, shares the same 298-pixel standing
  height and floor registration as the cooking sequence, and has a transparent
  gutter on every cell edge; and
- the optional exact-Prime ghost remains available and off by default.

This is a choreography reuse, not a repaint. It introduces no generated,
scaled or colour-adjusted art.

## Approval result

Frank's verdict was: “excellent. All animations approved.” The decision covers
all ten complete sequences and 162 frame occurrences on the V12 page, including
their exact visible art, ordering, timing, holds, transitions and route
choreography. It does not approve unrelated candidates on other review pages.

The pre-approval status strings inside the immutable V12 manifest describe how
each sequence entered review; the external approval record is the current
decision authority. Individual frame redraft slots remain valid for any future
V13 amendment.

## Reversibility and verification

- V11 remains unchanged at its versioned route and is recorded as rejected for
  the broken jumper edges.
- All seven reused PNGs and the complete V12 strip live in the versioned V12
  draft directory.
- `corrections.json` records the V11 predecessor and exact cooking donor hash
  for each of the 21 replaced positions.
- Every frame has an independent V12 redraft slot and a V11 comparison.
- `scripts/verify_keeper_prime_morning_drafts_v12.mjs` rebuilds the batch,
  proves each replacement is byte-identical to its cooking donor, checks the
  exact 21-frame change scope, strip geometry, transparent gutters, controls,
  ghost default and versioned routing.

Run:

```sh
npm run verify:keeper-prime-drafts
npm run verify:review-archive
npm run build
```
