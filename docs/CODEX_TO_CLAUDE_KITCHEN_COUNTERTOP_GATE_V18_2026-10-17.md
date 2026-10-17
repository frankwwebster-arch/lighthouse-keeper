# Codex to Claude: Kitchen countertop Gate V18

Date: 17 October 2026  
Status: review-only first gate; awaiting Frank  
Review: `/keeper-review/kitchen-countertop-gate-v18/`

## Scope delivered

Only three standard-state candidates exist:

| Item | Cell | Opaque width | Contact | Interaction spot retained |
| --- | ---: | ---: | ---: | ---: |
| Kettle counter | `21 × 31 lp` | `20 lp` | `19 lp` / row `48 px` | `452 ku` |
| Cooker / hob | `21 × 28 lp` | `20 lp` | `19 lp` / row `36 px` | `788 ku` |
| Sink counter | `21 × 29 lp` | `20 lp` | `19 lp` / row `40 px` | `1,124 ku` |

The page includes exact V5 comparisons, candidate/structure/ghost/edge views,
logical scale, a shared-contact triptych, and a three-bay neutral room context
with `4 lp` of clear foreground floor.

## Root cause corrected

The old A/B/C builder drew a replacement slab and then alpha-composited a
rectangular V5 preserve box over it. Those boxes contained V5's inherited
tapered worktop pixels, creating the reported chips and stepped shoulders. It
also used visual front rows `48/32/48` rather than deriving `48/36/40` from the
three declared bottom anchors and the common `19-lp` datum.

V18 does not read old candidate pixels. It uses shape-aware appliance masks and
requires the old Option-B candidates to fail the new exact-RGBA detector.

## Protected surfaces

- Kitchen V5: read-only visual authority.
- Kitchen V17: unchanged immutable rollback.
- Runtime sprites and manifest: unchanged.
- Keeper animations and approved source: unchanged.
- Animation workbench / Final state: unchanged.
- No full family, room shell, states, register, manifest or game wiring was
  rebuilt.

## Next gate

Do not rebuild kettle/toaster/mixer states, the fridge, bin, shelves, porthole
or room shell until Frank explicitly accepts this three-unit construction.
When accepted, apply the recipe to each future state from its exact V5 base and
retain the same negative-control test.
