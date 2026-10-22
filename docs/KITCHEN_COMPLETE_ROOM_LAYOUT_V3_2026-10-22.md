# Kitchen Complete Room Layout V3 — load-safe delivery

Date: 22 October 2026
Status: unapproved review correction; V2 and all art authorities remain immutable

## Why V3 exists

The V2 review shell and every image deployed correctly, but a cold visit had to
follow and decode nineteen separate archived PNG redirects before drawing the
room or enabling controls. This could leave the page apparently stuck at
`LOADING 19 EXACT ASSETS` for long enough to be unusable.

V3 corrects delivery only. It does not redraw, rescale, recolour, reposition or
promote any kitchen asset.

## Delivery change

- All fourteen fitted-unit/state crops and all five loose-object crops from V2
  are packed losslessly into one transparent `520 × 6810` PNG atlas.
- Every original PNG remains pinned by its V2 SHA-256 and an exact atlas source
  rectangle.
- The room downloads and decodes one unique image before enabling movement.
- A 30-second bounded failure state replaces an indefinite loading state.
- The atlas SHA-256 is
  `447b4ad64307e914c0a376ab19eccd0900c097562df3a219289ae7d25ebb7e3d`.

## Unchanged

- approved cabinetry and fitted-state pixels;
- toaster, kettle, bin, table and chair pixels;
- `84 × 74` fitted-body registration and six bay origins;
- table, chair-seat, worktop and floor datums;
- raw/join-only comparison;
- `1×`, `2×` and `4×` direct-source zoom;
- independent loose-object movement, cabinet swapping and Broken-unit lock;
- Kettle V47, runtime, production assets and selectors.

## Review

Route: `/keeper-review/kitchen-complete-room-layout-v3`

The complete-room art remains an unapproved review candidate. V2 is retained
unchanged as provenance; V3 supersedes only its review-page delivery.

## Verification

Run:

```sh
npm run verify:kitchen-complete-room-layout-v2
npm run verify:kitchen-complete-room-layout-v3
npm test
```

The V3 verifier checks the atlas hash and archive entry, all nineteen
non-overlapping source rectangles, exact source dimensions, immutable V2
predecessor hash, one-image loader, bounded failure state and route redirect.
