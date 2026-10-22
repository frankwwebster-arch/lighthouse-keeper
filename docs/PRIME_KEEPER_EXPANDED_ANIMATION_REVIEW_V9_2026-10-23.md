# Prime Keeper expanded animation review V9

Date: 23 October 2026

Status: review candidate. V8 is preserved as rejected evidence.

Current route: `/prime-keeper-animation-drafts`

Versioned route: `/prime-keeper-animation-drafts-v9`

## Correction

V9 responds to the doubled seam still visible in V8 rear-task frames 11–31.
V8 aligned the torso and legs correctly, but placed the approved trousers'
dark top edge directly below the moving jumper hem. That fixed edge read as a
second bottom seam.

V9 retains V8's exact per-frame horizontal registration and changes only the
six rows immediately below the moving hem:

- rows 0–213 remain byte-identical to the moving V6 action source, including
  the complete torso and its one natural ribbed hem;
- rows 214–219 use exact trouser-fill pixels from row 220 of the approved rear
  authority, repeated vertically so the authority waistband edge is occluded
  behind the moving hem;
- rows 220–319 retain the approved rear-authority trousers and boots at V8's
  measured per-frame horizontal registration;
- the outer bounds on rows 213 and 214 remain identical in every frame; and
- no generated, inpainted, rescaled or manually painted pixel enters V9.

All other V8 frames, timing and controls are preserved. Every occurrence has
an independent V9 redraft slot.

## Reversibility and verification

- Correction root:
  `art/drafts/keeper-prime-morning-drafts-corrections-2026-10-23-v9/`
- V8/V9 hash map: `corrections.json`
- Browser manifest: `data/keeper_prime_animation_drafts_v9.json`
- Builder: `scripts/build_keeper_prime_morning_drafts_v9.mjs`
- Verifier: `scripts/verify_keeper_prime_morning_drafts_v9.mjs`

The verifier requires exactly 21 changed frame occurrences, byte-identical
action pixels through row 213, matching row-213/214 outlines, exact approved
row-220 fill in rows 214–219, exact approved-authority pixels below, transparent
cell-edge gutters, archived hashes, full playback controls and independent
redraft slots.

## Approval boundary

V9 remains review-only. It does not approve the rear-task choreography or
promote it into the runtime bank. V1–V8, canonical art and runtime sprites
remain unchanged.
