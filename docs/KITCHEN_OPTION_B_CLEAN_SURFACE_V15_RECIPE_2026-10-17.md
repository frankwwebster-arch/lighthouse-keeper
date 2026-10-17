# Kitchen Option-B clean-surface recipe (V15)

**Date:** 17 October 2026  
**Status:** review-only reversible draft; not approved, promoted or wired  
**Machine record:** `data/kitchen_option_b_clean_surface_v15_recipe.json`

## Authority boundary

- V5 is the sole authority for colour, finish, object detail and animation.
- The selected V6 Option-B calibration remains the geometry authority: a
  `1.5 lp / 6 px` visible top and `2 lp / 8 px` fascia at density 4.
- V6 is the first known broken-surface revision and is retained only as a
  required failing control. Never copy its countertop pixels.
- V13 and V14 are also rejected visual provenance. Do not derive another
  repair from either version.

## Exact construction

1. Reserve an `84 px` one-bay cell. The structural surface owns x `2…81`,
   leaving the exact 2-px transparent gutter at each shared edge.
2. Let `frontY` be the established worktop front datum. The top plane occupies
   `frontY - 6 … frontY - 1`; the fascia occupies
   `frontY … frontY + 7`.
3. Draw the complete `80 × 14 px` surface once. Rear, front and bottom edges
   are straight horizontal runs; the two sides are straight vertical runs.
   Fill every interior pixel. No inherited outline, texture, appliance or
   transparent pixel may interrupt the surface template.
4. Begin each output frame with its corresponding V5 frame. Clear only the
   declared 14-px reconstruction band and composite the canonical surface.
5. Recover the appliance from that same V5 frame with a colour-connected mask:
   non-wood appliance colours seed the mask; only the immediately adjacent
   outline is recovered. Old wood and remote outline pixels are excluded.
6. Composite the recovered appliance over the surface. Never composite the old
   V5 countertop rectangle or V6 preserve rectangle over the new plane.
7. Preserve every RGBA pixel outside the reconstruction band byte-for-byte from
   the corresponding V5 frame. Preserve the three sink dishes overlays
   byte-for-byte and composite them only for review.

Front datums and permitted appliance intervals at density 4:

| Unit | Cell | `frontY` | Surface band | Appliance x interval |
| --- | ---: | ---: | ---: | ---: |
| Kettle | 21 × 31 lp | 48 px | y 42…55 | x 14…68 |
| Toaster | 21 × 31 lp | 36 px | y 30…43 | x 12…72 |
| Mixer | 21 × 31 lp | 52 px | y 46…59 | x 12…72 |
| Sink | 21 × 29 lp | 48 px | y 42…55 | x 14…70 |

## Binding test

For every standard, on and broken frame, compare every RGBA pixel in both
exposed wings of the reconstruction band with the canonical surface template.
The comparison is exact, not alpha-only and not palette-only. Also assert:

- the 80-px rear, front and fascia-bottom edge rows are uninterrupted;
- all 1,120 pixels in the 80 × 14-px template are opaque;
- every pixel outside the reconstruction mask remains exact V5;
- each V6 standard frame fails the same wing comparison;
- the V5 and V6 immutable tree hashes remain unchanged; and
- runtime, Final and Keeper hashes remain unchanged.

This gate prevents the original V5→V6 regression: a later builder cannot pass
by retaining the Option-B dimensions while reintroducing chips, old centre
joins or broken shoulder outlines.

## Room composition

The V15 room proof is `193 × 56 lp` and uses the exact 52-lp rear-wall foot
line. It combines the V15 counters with the V10 detailed white fridge and
plant shelf, V12 matched recipe-book shelf, V10 true-alpha porthole and the
unchanged V8 cooker, compact bin, table, chair and pet bowl. These dependencies
remain review drafts; composition does not approve or wire any asset.
