# Kitchen V16 silhouette-clean Option-B surfaces: Codex → Claude hand-back

**Date:** 17 October 2026  
**Status:** review-only reversible draft; not approved, promoted or wired  
**Review:** `/keeper-review/kitchen-option-b-silhouette-clean-v16/`

## Correction and authority

Frank rejected V15 because its toaster, kettle, mixer and sink counters still
showed the stepped/tapered remnants that began during the V5→V6 perspective
change. The V15 test ignored the inherited rows above its nominal new slab.

V16 starts again from V5 for every appliance, cabinet and animation pixel. It
keeps the selected Option-B `1.5 lp` top and `2 lp` fascia, but clears from the
true first old-countertop row and restores only a measured appliance mask.
V15 is the required failing control for the new exact-pixel test.

## Measured outputs

| Item | Measured visible bounds | Cell / bays | Interaction X | States |
| --- | --- | --- | ---: | --- |
| Kettle unit | x 0.5, y 1, 20 × 30 lp | 21 × 31 lp / 1 | 452 ku | standard/on/broken, 1/4/4 frames |
| Toaster unit | x 0.5, y 1, 20 × 30 lp | 21 × 31 lp / 1 | 620 ku | standard/on/broken, 1/4/4 frames |
| Mixer unit | x 0.5, y 1, 20 × 30 lp | 21 × 31 lp / 1 | 956 ku | standard/on/broken, 1/4/4 frames |
| Sink unit | x 0.5, y 2, 20 × 27 lp | 21 × 29 lp / 1 | 1,124 ku | standard/on/broken, 1/4/4 frames; three unchanged dishes overlays |

Each unit keeps the exact 0.5-lp shared-edge gutter inside its 21-lp bay. The
room proof is `193 × 56 lp`; every floor unit remains on the 52-lp rear-wall
foot line. The sink-owned porthole is still an actual alpha opening onto the
global lighthouse backdrop.

## Permanent test

`scripts/verify_kitchen_option_b_silhouette_clean_v16.mjs` checks the complete
expanded removal zone, not just the nominal countertop. It compares every
unmasked RGBA pixel with the canonical slab or required transparency, rejects
wood in the restored silhouette, preserves masked appliance pixels and all V5
pixels outside the zone, and requires every V15 standard frame to fail above
the new rear edge.

The review page enlarges the V15/V16 pair fourfold, preloads and decodes every
frame before enabling controls, and exposes all standard/on/broken states plus
the unchanged sink overlays.

## Files

- Recipe: `data/kitchen_option_b_silhouette_clean_v16_recipe.json`
- Builder: `scripts/build_kitchen_option_b_silhouette_clean_v16.py`
- Verifier: `scripts/verify_kitchen_option_b_silhouette_clean_v16.mjs`
- Raw draft strips and masks: `art/raw/kitchen-option-b-silhouette-clean-2026-10-17-v16/`
- Catalogue/register: `art/drafts/kitchen-option-b-silhouette-clean-2026-10-17-v16/`
- Review page: `public/keeper-review/kitchen-option-b-silhouette-clean-v16/`

No Keeper animation, production sprite, runtime manifest, register, Final
asset or live-game path was changed. V16 remains a draft awaiting Frank's
visual decision.

## Delivery verification

Deployment and production-response details are recorded here after the
review-only release marker is verified.
