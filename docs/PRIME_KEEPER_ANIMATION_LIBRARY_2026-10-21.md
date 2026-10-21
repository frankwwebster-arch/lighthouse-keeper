# Prime Keeper approved animation library

Date: 21 October 2026  
Live route: `/prime-keeper-animations`

## Purpose

The Prime Keeper's approved motion had accumulated across many immutable review
pages and approval records. The new library gives that work one readable index
without changing, copying over, promoting or redrawing an approved source.

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

The page preloads and decodes all 213 unique frame URLs before enabling any
transport control or starting playback. It reuses the content-addressed review
archive and adds no image media.

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

## Approval boundary

This is an inspection and composition tool, not a promotion. Prime Keeper Final
and runtime remain unchanged and still contain no promoted Prime animation.
The page's “approved” label means the exact review authority described by the
source decision; it does not expand any decision's original scope.

The sandbox never edits source frames. It stores only clip identifiers,
direction, order and repeat count in browser local storage under
`prime-keeper-animation-sandbox:v1`.

## Source and verification

- `scripts/build_prime_keeper_animation_library.mjs` extracts exact frame
  routes from the existing approved review data and writes the static catalogue.
- `public/prime-keeper-animations/catalogue.json` is the deployed catalogue.
- `src/prime-keeper-animations/` contains the page UI and transport/sandbox
  logic.
- `src/app/prime-keeper-animations/page.tsx` owns the route and metadata.

Verify the generated catalogue with:

```sh
npm run verify:prime-keeper-animation-library
npm run typecheck
npm run build
```

The catalogue verifier fails if its generated output no longer matches the
underlying approved review sources.
