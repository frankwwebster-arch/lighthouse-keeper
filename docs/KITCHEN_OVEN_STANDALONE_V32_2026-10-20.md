# Kitchen Oven Standalone V32

Date: 20 October 2026

Status: reversible visual-review draft; awaiting visual review, unpromoted and
unwired.

Review page: `/keeper-review/kitchen-oven-standalone-v32/`

## Corrected interpretation

V31 is rejected because its broad rectangular foreground cap flattened the
correct V30 triangular transition. V32 restores the V30 construction and
removes only the unwanted cabinet-facing diagonal line:

1. retain the V30 triangular turquoise underlay behind each snapped join;
2. retain the V22 cabinet-blue body backfill behind the assets;
3. retain the oven-facing diagonal edge exactly;
4. cover only the six-pixel-wide cabinet end contour with row-matched V22
   countertop pixels, so the triangle flows into one continuous cabinet slab.

No oven or cabinet sprite is redrawn or amended.

## Exact three-layer rule

- Oven body: `x=336..420`, `y=131..208` in the 772 × 224 room.
- Shared snapped edges: `x=336` and `x=420`.
- Body layer: crop `6 × 63` pixels from the approved V22 blue backfill and draw
  it behind the assets at `(333,145)` or `(417,145)`.
- Triangular surface layer: draw the full V30 `24 × 12` V22-derived triangle
  behind the assets at `(324,134)` or `(408,134)`.
- Cabinet-seam cleanup: draw a `6 × 12` row-matched mask in front at
  `(330,134)` or `(420,134)`. On the first row it covers only the cabinet-side
  pixels; on the remaining rows it covers the six-pixel cabinet end contour.
- Draw order: room background → active body backfills and triangular underlays
  → cabinet neighbours → standalone oven → active cabinet-seam cleanup masks.
- Each edge activates independently only for exact snapped adjacency.
- Removing either neighbour removes all three layers on that edge only.

The cleanup masks are deliberately narrower than V31's caps. Deterministic
verification proves that they never overlap an opaque oven pixel, so the
oven-facing diagonal and approved oven silhouette remain unchanged.

## Preserved invariants

- Every Off, On and Broken state PNG is byte-identical to V30.
- The protected foreground hanging dial remains byte-identical to V30 in all
  light combinations.
- Body `84 × 77`, cell `92 × 85`, four-pixel transparent gutter, room position,
  projection and Prime interaction anchor `(378,218)` are unchanged.
- Both 40-frame, 4-fps, ten-second irregular fault schedules remain separately
  removable and variable-speed.
- Cabinet V11, approved V22 templates, room background, Final, runtime and
  later kitchen assets remain unchanged.
- Smoke remains a separate reusable environmental layer.

## Verification

Run:

```sh
npm run verify:kitchen-oven-standalone-v32
npm run build
```

The verifier reconstructs all six complete-room states from the declared draw
order, checks the exact asymmetric cleanup-mask alpha patterns and approved row
colours, rejects any overlap with opaque oven pixels or pale-wall body gaps,
checks all state and animation bytes against V30, and validates transparent
gutters, archive hashes, geometry and the unchanged Prime anchor.
