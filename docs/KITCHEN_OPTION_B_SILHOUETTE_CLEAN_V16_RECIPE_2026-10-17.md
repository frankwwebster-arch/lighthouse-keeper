# Kitchen Option-B silhouette-clean recipe (V16)

**Date:** 17 October 2026  
**Status:** review-only reversible draft; not approved, promoted or wired  
**Machine record:** `data/kitchen_option_b_silhouette_clean_v16_recipe.json`

## Why V15 failed

V15 reconstructed only the new `80 × 14 px` Option-B band. The inherited V5
countertop starts above that band: at y 38 for kettle and sink, y 22 for
toaster and y 44 for mixer. V15 therefore left two to four rows of the old
tapered top in place. Those retained pixels are the stepped brown/black
shoulders Frank identified; the former wing test did not inspect them.

V15 is rejected and immutable. V16 keeps V5 as the sole visual and animation
authority and keeps Option B as the required perspective geometry, but expands
the reconstruction boundary to the measured first inherited-surface row.

## Exact construction

1. Reserve the exact `84 px` one-bay cell. The structural countertop owns
   x `2…81`, retaining a 2-px transparent shared-edge gutter on each side.
2. Use the established `frontY`. The Option-B top occupies
   `frontY - 6 … frontY - 1`; its fascia occupies
   `frontY … frontY + 7`.
3. Measure the first V5 row that spans both outer wings. Clear the complete
   row range from that `removalTop` through `frontY + 7`, not merely the new
   slab rectangle.
4. Draw the canonical `80 × 14 px` Option-B surface once. Its rear, front and
   bottom edges are straight horizontal runs, its sides are vertical, and its
   interior has no transparent gaps.
5. Recover only the appliance/effect silhouette from the matching V5 frame.
   Teal, neutral enamel and declared sink-gold regions seed a binary mask; the
   mask may grow only two pixels to recover adjacent cool/dark outline pixels.
6. Reject inherited wood colours from the mask. Hard-clip the result to the
   measured appliance x interval. Above the new rear edge, every unmasked
   pixel in the removal zone must be transparent; within the slab, every
   unmasked pixel must equal the canonical surface exactly.
7. Preserve every V5 pixel outside the expanded removal zone byte-for-byte.
   Preserve all three dishes overlays byte-for-byte.

Measured density-4 boundaries:

| Unit | Cell | `frontY` | First old-surface row | New slab | Silhouette x |
| --- | ---: | ---: | ---: | ---: | ---: |
| Kettle | 21 × 31 lp | 48 px | y 38 | y 42…55 | x 18…65 |
| Toaster | 21 × 31 lp | 36 px | y 22 | y 30…43 | x 19…65 |
| Mixer | 21 × 31 lp | 52 px | y 44 | y 46…59 | x 18…66 |
| Sink | 21 × 29 lp | 48 px | y 38 | y 42…55 | x 14…70 |

## Binding regression gate

For every standard, on and broken frame:

- the binary mask must be empty outside the expanded removal zone and the
  measured appliance width;
- masked pixels must be exact V5 pixels and may not be inherited wood;
- every unmasked pixel from `removalTop` through the fascia bottom must equal
  either the canonical slab or transparency above its rear edge;
- all V5 pixels outside that zone must remain exact;
- the 80-px rear, front and bottom structural rows must be uninterrupted;
- the V15 standard frame must fail this same rule, including at least one
  failure above the new rear edge; and
- V5, rejected V15, runtime manifest and Keeper-workbench hashes must remain
  unchanged.

The required negative control is V15, not a synthetic damaged sample. If V15
ever passes, the gate has stopped detecting the exact defect reported by Frank.

## Room and future assets

The room proof remains `193 × 56 lp`, uses the exact 52-lp rear-wall foot line
and retains 4 lp of clear foreground floor. The detailed white fridge, compact
bin, matched plant/recipe shelves and true-alpha porthole are unchanged.

Future one-bay countertop assets must record both `frontY` and the first row of
any inherited/source surface. A replacement must clear the larger of those
zones, restore only a binary object silhouette, and use the same negative-
control principle. A test restricted to the nominal new slab is insufficient.

