# Prime Keeper expanded animation review V11

Date: 23 October 2026

Status: reversible review-only draft. No V11 frame is installed in the runtime
animation bank.

Routes:

- current review: `/prime-keeper-animation-drafts`
- immutable V11 permalink: `/prime-keeper-animation-drafts-v11`

## Correction

V10 correctly removed the incompatible torso/lower-body splice, but its arm
copy began at row 125. Several sleeves begin above that row, and later work
poses raise hands alongside the head, so the fixed boundary visibly cut their
upper silhouettes. The exact-Prime alignment ghost was also enabled by default,
making the approved resting arms appear over the action arms.

V11 keeps the approved body construction and corrects only rear-task positions
11–31:

- the complete approved rear Prime remains the base;
- the approved resting-arm envelope is cleared from row 115;
- complete V6 action arms may copy through row 242;
- below row 115, action pixels remain confined to the outer arm columns;
- above row 115, raised sleeves and hands may enter only where the approved
  authority is transparent and where a two-pixel dilation of the neutral V6
  rear pose is also transparent; and
- the optional exact-Prime alignment ghost remains available but is off by
  default.

This retains every opaque approved cap, head and beard pixel, the protected
central body, approved jumper band, trousers, boots, height and floor
registration. It introduces no generated, scaled or repainted delivery art.

## Reversibility and verification

- V10 remains unchanged at its versioned route.
- All 21 V11 PNGs and the strip live in the versioned V11 draft directory.
- `corrections.json` records V6, V10, authority, neutral-mask and V11 hashes for
  every corrected frame.
- Every frame has an independent V11 redraft slot and a V10 comparison.
- `scripts/verify_keeper_prime_morning_drafts_v11.mjs` rebuilds the batch and
  checks exact pixel ownership, approved-head protection, restored pixels above
  V10's crop, raised-arm extensions, transparent gutters, dimensions, controls,
  ghost default and versioned routing.

Run:

```sh
npm run verify:keeper-prime-drafts
npm run verify:review-archive
npm run build
```
