# Prime Keeper approved animation library

Date: 21 October 2026  
Live route: `/prime-keeper-animations`

## Purpose

The Prime Keeper's approved motion had accumulated across many immutable review
pages and approval records. The library gives that work one readable index and
now shows each approved source beside its versioned runtime delivery where a
reusable clip has been extracted.

The page provides:

- 14 playable approved clips grouped into Locomotion, Turns, Circulation,
  Sit & stand and Activities;
- individual play, pause, stop/reset, previous-frame, next-frame and scrubber
  controls for every clip;
- global play, pause, stop/reset and frame-step controls across the library;
- a sequence sandbox where approved clips can be added, reordered, reversed,
  repeated, removed and played as one choreography;
- declared endpoint checks that identify joins which need a bridge pose;
- local persistence and JSON export for the sandbox sequence; and
- direct links back to each immutable original review surface.

The page preloads and decodes all 213 unique source frame URLs plus every
runtime sheet before enabling any transport control or starting playback. It
reuses the content-addressed review archive for source evidence.

## What is in the playable bank

1. Prime Walk V7.
2. Prime Stop–Walk–Stop V2.
3. Prime Turn Front–Side V1.
4. Prime Turn Side–Back V10, pinning the approved nine-frame V9 authority.
5. Prime Stair Ascent V16, pinned by the no-art V17 approval pack.
6. Prime Stair Descent V2.
7. Prime Stair Transitions V6 complete door-to-door route.
8. Prime Ladder Transitions V5's 111 approved Keeper frames, shown through the
   later V6 door-only review link.
9. Side-right Sit–Stand V6.
10. Side-left Sit–Stand V1.
11. Front Sit–Stand V4.
12. Back Sit–Stand V2.
13. Darts Context V8.
14. Rear Action Sequence V1.

The held-implement Upper-body Override POC V3 is linked but deliberately kept
outside the playable approved bank. Its motion feasibility and
`hold_shaft_two_hand` concept are approved, while its proxy body artwork is
explicitly not approved for production.

## Runtime promotion — 22 October 2026

Frank authorised runtime promotion after the earlier boundary was explained.
The versioned promotion installs 27 reusable sprites / 217 registered frames
from 13 of the 14 source clips. The complete stair route is a review composite;
its reusable walk, turn and stair constituents are installed rather than
duplicating the composite as one oversized runtime strip.

The game actively consumes Prime idle, walk start/cycle/stop, stair
ascent/descent and generic rear work. Approved turns now bridge rear work and
seating; TV/nature TV/armchair nap/reading/piano use side sit → hold → stand;
diary uses turn → back sit → hold → stand → turn. Ladder, darts and front/left
seating remain installed but await matching gameplay consumers. The library
labels that distinction and renders approved source and installed delivery
side-by-side. This promotion does not expand any original art approval.

The separate `/prime-keeper-animation-drafts` page now preserves the rejected V9 review:
the five preserved V1 drafts, one isolated broom candidate and four
approved-component choreography previews, plus reversible feedback corrections.
V9 retains the accepted V3 palette, lift and naming amendments, and replaces
only rejected V8 rear-task positions 11–31. Frank rejected V9 on 23 October
because a separate dark waistband line remains visible beneath the moving hem.
These ten
sequences remain outside the approved library and runtime bank until their
complete choreography is accepted. V1–V8
remain at their versioned routes; the current versioned route is
`/prime-keeper-animation-drafts-v9`. See
`docs/PRIME_KEEPER_EXPANDED_ANIMATION_REVIEW_V9_2026-10-23.md`.

The active correction surface is `/prime-keeper-rear-task-alignment`. It keeps
the immutable V6 torso and approved rear legs separate for manual drag, pixel
nudge and crop alignment across frames 11–31, then exports hash-addressed JSON.
It does not alter or promote source art. See
`docs/PRIME_KEEPER_REAR_TASK_ALIGNMENT_WORKBENCH_V1_2026-10-23.md`.

The held-implement POC remains excluded. Its motion feasibility and
`hold_shaft_two_hand` concept are approved, but the proxy body art is not.

The sandbox never edits source frames. It stores only clip identifiers,
direction, order and repeat count in browser local storage under
`prime-keeper-animation-sandbox:v1`.

## Source and verification

- `scripts/build_prime_keeper_animation_library.mjs` extracts exact frame
  routes from the existing approved review data and writes the static catalogue.
- `public/prime-keeper-animations/catalogue.json` is the deployed catalogue.
- `data/keeper_prime_runtime_bank.json` is the runtime register, including
  active bindings, installed assets awaiting consumers and source/delivery
  hashes.
- `art/drafts/keeper-prime-runtime-promotion-2026-10-22-v1/` preserves the
  reversible draft delivery; `art/raw/keeper-prime-runtime-v1/` is the promoted
  versioned source.
- `src/prime-keeper-animations/` contains the page UI and transport/sandbox
  logic.
- `src/app/prime-keeper-animations/page.tsx` owns the route and metadata.

Verify the generated catalogue with:

```sh
npm run verify:prime-keeper-animation-library
npm run verify:keeper-prime-identity
npm run verify:keeper-prime-runtime
npm run verify:keeper-prime-drafts
npm run typecheck
npm run build
```

The catalogue verifier fails if its generated output no longer matches the
underlying approved review sources. The runtime verifier also checks every
hash, manifest field, strip geometry and shared vertical cell edge.

The remaining-work inventory is
`docs/PRIME_KEEPER_ANIMATION_GAPS_2026-10-22.md` and its checked data source is
`data/keeper_prime_animation_gaps.json`.
