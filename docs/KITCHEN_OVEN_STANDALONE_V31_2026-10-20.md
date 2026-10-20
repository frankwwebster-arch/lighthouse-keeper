# Kitchen Oven Standalone V31

Date: 20 October 2026

Status: reversible visual-review draft; unapproved, unpromoted and unwired.

Review page: `/keeper-review/kitchen-oven-standalone-v31/`

## Requested corrections

V30 remains immutable. V31 corrects only its join compositor:

1. V30 drew the V22 countertop cap behind the oven and cabinets. Their end
   outlines therefore remained visible as a dark line across each turquoise
   V-shaped repair. V31 draws the approved seamless cap after the assets, as
   required by the approved V22 sink methodology.
2. The narrow pale-wall gaps below the worktop receive the approved V22
   cabinet-blue body backfill before the assets are drawn.

No oven or cabinet sprite is redrawn or amended.

## Exact two-layer rule

- Oven body: `x=336..420`, `y=131..208` in the 772 × 224 room.
- Shared snapped edges: `x=336` and `x=420`.
- Body layer: crop `6 × 63` pixels from the approved V22 blue backfill and draw
  it behind the assets at `(333,145)` or `(417,145)`.
- Surface layer: crop `16 × 12` pixels from the approved V22 seamless cap and
  draw it in front of the assets at `(328,134)` or `(412,134)`.
- Draw order: room background → active blue body backfills → cabinet
  neighbours → standalone oven → active seamless countertop caps.
- Each edge activates independently only for exact snapped adjacency.
- Removing or moving one neighbour removes both layers for that edge only.

This restores the complete approved sink-join architecture: a structural
background fill for the body and a row-matched foreground cap for the shared
worktop surface.

## Preserved invariants

- Every Off, On and Broken state PNG is byte-identical to V30.
- The protected foreground hanging dial remains byte-identical to V30 in all
  light combinations.
- Body `84 × 77`, cell `92 × 85`, four-pixel transparent gutter, room position,
  projection and Prime interaction anchor `(378,218)` are unchanged.
- Both 40-frame, 4-fps, ten-second irregular fault schedules remain separately
  removable and variable-speed.
- Cabinet V11, both approved V22 join templates, the room background, Final,
  runtime and later kitchen assets remain unchanged.
- Smoke remains a separate reusable environmental layer.

## Verification

Run:

```sh
npm run verify:kitchen-oven-standalone-v31
npm run build
```

The verifier reconstructs every complete-room state from the declared layer
order, requires the foreground cap to own every pixel across both shared
countertop joins, rejects pale-wall pixels in either body gap, checks all state
and animation bytes against V30, validates transparent gutters, archive hashes,
geometry and the unchanged Prime anchor.
