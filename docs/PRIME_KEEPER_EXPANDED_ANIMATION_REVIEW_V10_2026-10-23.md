# Prime Keeper expanded animation review V10

Date: 23 October 2026

Status: rejected reversible evidence. Frank found that the row-125 transfer
boundary cropped the tops of sleeves and raised hands, and that the alignment
ghost was enabled by default. No V10 frame is installed in the runtime bank.

Routes:

- immutable V10 permalink: `/prime-keeper-animation-drafts-v10`
- active successor: `/prime-keeper-animation-drafts-v11`

## Corrected construction

V10 replaces only `rear-work-turn-return-v1` positions 11–31. Earlier seam and
torso/lower-body splices failed because the V6 action torso and the approved
rear Prime were different drawings. Exact alignment could not make their waist
width, side contour and ribbed-band construction coherent.

Each V10 rear-work frame instead begins with the complete hash-pinned approved
rear Prime authority:

`31dbac4efc00089fe6f831dc23f8397b4e3a8faf4d4aaa09a92b2ff407eebc35`

The compositor clears only the approved resting-arm envelope, then copies only
opaque arm pixels from the corresponding immutable V6 choreography frame. The
approved cap, head, ears, beard, neck, torso, cream stripe, complete jumper
band, trousers, boots, standing height and floor registration remain exact.
There is no torso/legs join and no generated, scaled or repainted delivery
pixel.

A model-generated redraw was inspected during diagnosis and rejected before it
entered the project because it changed Prime proportions, line weight and
modelling. It is not referenced by V10.

## Reversibility and review

- All 21 corrected PNGs live in the versioned V10 draft directory with their
  SHA-256 values recorded in `corrections.json`.
- Every frame keeps its V9 predecessor hash and an independent V10 redraft
  slot.
- The review page preloads every unique frame before enabling playback.
- Each sequence supports play, pause, stop, previous/next frame and direct
  frame seeking.
- The rear-task player includes the exact approved rear Prime as a separately
  rendered 10–80% ghost, enabled by default at 38%.
- Changed rear-task frames are shown side-by-side with rejected V9.
- The sandbox can combine and reverse sequences without modifying frame data.
- V1–V9, both manual alignment tools, canonical art and runtime assets remain
  unchanged.

## Deterministic safety contract

`scripts/verify_keeper_prime_morning_drafts_v10.mjs` rebuilds V10 and verifies:

- only rear-task positions 11–31 differ from V9;
- every non-arm pixel follows the approved authority exactly;
- every copied action pixel comes from the matching V6 source coordinate;
- the protected central Prime body is byte-exact in every frame;
- cap top, standing height and floor registration remain exact;
- every cell retains a transparent safety gutter;
- the 21 frames retain varied arm choreography;
- manifests, immutable archive objects, predecessor hashes, redraft slots,
  review controls and ghost controls remain consistent.

Run:

```sh
npm run verify:keeper-prime-drafts
npm run verify:review-archive
npm run build
```
