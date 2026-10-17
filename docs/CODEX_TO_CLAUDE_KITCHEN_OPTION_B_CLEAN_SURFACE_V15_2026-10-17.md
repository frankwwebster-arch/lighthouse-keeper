# Kitchen V15 clean Option-B surfaces: Codex → Claude hand-back

**Date:** 17 October 2026  
**Status:** review-only reversible draft; not approved, promoted or wired  
**Review:** `/keeper-review/kitchen-option-b-clean-surface-v15/`

## Correction

Frank identified V5→V6 as the countertop-surface regression boundary. V5 is
the last visually sound family, but the selected perspective correction still
has to occur. V15 therefore does not roll the assets back to V5 geometry:

- all V5 pixels outside the countertop reconstruction band are preserved;
- the selected Option-B `1.5 lp` shallow top and `2 lp` fascia remain;
- the full surface is rebuilt as one uninterrupted plane; and
- only the V5 appliance silhouette is restored over it, so old countertop
  outlines cannot break up the new surface.

V6 is a required failing control. V13 and V14 remain rejected and immutable.

## Measured outputs

| Item | Cell | Bays | Interaction X | States | Worktop |
| --- | ---: | ---: | ---: | --- | ---: |
| Kettle unit | 21 × 31 lp | 1 | 452 ku | standard/on/broken, 1/4/4 frames | 19 lp |
| Toaster unit | 21 × 31 lp | 1 | 620 ku | standard/on/broken, 1/4/4 frames | 19 lp |
| Mixer unit | 21 × 31 lp | 1 | 956 ku | standard/on/broken, 1/4/4 frames | 19 lp |
| Sink unit | 21 × 29 lp | 1 | 1,124 ku | standard/on/broken, 1/4/4 frames; three unchanged dishes overlays | 19 lp |

Every unit remains inside its exact 21-lp bay with 0.5-lp transparent side
gutters. The room proof keeps the rear-wall foot line at 52 lp and the 4-lp
foreground floor clear. The sink porthole remains a true alpha hole onto the
global lighthouse backdrop.

## Permanent regression gate

`scripts/verify_kitchen_option_b_clean_surface_v15.mjs` now checks every state
and frame. It requires exact canonical pixels in both exposed surface wings,
uninterrupted 80-px structural rows, full template opacity and exact V5 pixels
outside the reconstruction band. Each V6 standard frame must fail the same
comparison or the test reports loss of sensitivity.

The three sink dishes overlays are copied byte-for-byte from V5. The verifier
also pins V5, V6, runtime manifest and animation-workbench hashes and checks the
content-addressed review archive plus preload/decode gating.

## Files

- Recipe: `data/kitchen_option_b_clean_surface_v15_recipe.json`
- Builder: `scripts/build_kitchen_option_b_clean_surface_v15.py`
- Verifier: `scripts/verify_kitchen_option_b_clean_surface_v15.mjs`
- Raw draft strips: `art/raw/kitchen-option-b-clean-surface-2026-10-17-v15/`
- Catalogue/register: `art/drafts/kitchen-option-b-clean-surface-2026-10-17-v15/`
- Review page: `public/keeper-review/kitchen-option-b-clean-surface-v15/`

No Keeper animation, production sprite, manifest, register, Final asset or live
game path was changed.
