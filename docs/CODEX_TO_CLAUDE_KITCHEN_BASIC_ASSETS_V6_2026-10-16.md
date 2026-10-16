# Codex to Claude: Kitchen Basic Assets V6

**Date:** 16 October 2026  
**Status:** review-only candidate; not approved, promoted or wired.

Frank rejected Kitchen V5's perspective treatment after live visual review.
Although V5 met its numeric 0–2-lp limits, outlines, bevels and highlights made
the repeated top planes read strongly, and the stacked room-floor bands read
as a theatre platform.

V6 implements the replacement `flat-elevation-v2` authority in
`docs/KITCHEN_FLAT_ELEVATION_PROJECTION_SPEC_V2_2026-10-16.md`.

## Changed from V5

- fridge, ordinary counter units and table: zero visible planar top surface;
- cooker and sink: at most 0.5-lp functional micro-reveal;
- no planar diagonal corners or side returns;
- floor reduced from 5 lp to 2 lp;
- one floor boundary plus one shallow colour band; no front fascia;
- V5 and V6 room/assets shown side by side;
- exact 193 × 56 logical-pixel game-scale view added.

## Retained exactly in contract

- all cells, anchors, room widths, bay positions and interaction spots;
- 19-lp worktop/hob/table and 11-lp seat datums;
- constant Keeper and object scale;
- table/chair/Keeper layer order;
- right-side-wall cupboard dimensions, hinge and lifecycle;
- all Keeper animation bytes and runtime/production files.

The verifier additionally compares V6 standard furniture with V5 and requires
every pixel outside the declared planar edit masks to remain byte-identical.
Review media remains content-addressed and earlier sets are not overwritten.

## Review and promotion boundary

Review URL: `/keeper-review/kitchen-basic-assets-v6/`

Do not wire V6 into room placement or runtime rendering unless Frank explicitly
approves it. Until then V5 and V6 are both historical/review evidence only.
