# Codex → Claude: Kitchen V8 wall-anchored correction draft

Date: 16 October 2026  
Status: review-only, reversible, unapproved

## What Frank approved as direction

Frank approved the lower-room composition in the recorded reference study:
the units read as attached to the rear wall, leave a visible foreground floor,
use smooth unbroken countertop wings, show a plain bright-white fridge and use
a much smaller bin.

He subsequently clarified that “pushed back” means **anchored to the rear
wall**, and asked for a larger porthole whose view can reflect weather and time
of day.

## V8 response

- All back-wall objects now use the exact `y=52 lp` foot line against the
  `y=51 lp` wall/floor junction, leaving `4 lp` of clear foreground floor.
- Kettle, toaster, mixer and sink worktop wings are repainted as uninterrupted
  Option B slabs.
- The fridge is a bright-white freestanding appliance with no wood countertop.
- Every bin state is contained by a `10 × 12-lp` envelope.
- The porthole grows from V7's `15 lp` to `19 lp` outer diameter.
- The porthole frame has an alpha-clear `14-lp` aperture. Day, sunset, night and
  rain are separate underlay files at `z24`; the frame is `z26`; the sink is
  `z40`.
- Sink, frame and underlay move by the same bay delta.

## Measured asset hand-back

| Item | Cell | Largest bound | Bays | Interaction |
|---|---:|---:|---:|---:|
| bin | 21 × 16 lp | 10 × 12 lp | 1 | 116 ku |
| fridge | 21 × 21 lp | 19 × 21 lp | 1 | 284 ku |
| kettle | 21 × 31 lp | 20 × 31 lp | 1 | 452 ku |
| toaster | 21 × 31 lp | 20 × 31 lp | 1 | 620 ku |
| cooker | 21 × 28 lp | 20 × 28 lp | 1 | 788 ku |
| mixer | 21 × 31 lp | 20 × 31 lp | 1 | 956 ku |
| sink | 21 × 29 lp | 20 × 29 lp | 1 | 1124 ku |
| table/chair | 42 × 28 lp | 40 × 26 lp | 2 | 1292 ku |
| pet bowl | 16 × 8 lp | 12 × 3 lp | 0 | 1440 ku |
| cupboard | 38 × 56 lp | 34 × 52 lp | far-cap overlay | 1512 ku |

## Files to continue from

- Exact recipe: `data/kitchen_wall_anchored_v8_recipe.json`
- Human recipe: `docs/KITCHEN_WALL_ANCHORED_V8_RECIPE_2026-10-16.md`
- Builder: `scripts/build_kitchen_wall_anchored_v8.py`
- Verifier: `scripts/verify_kitchen_wall_anchored_v8.mjs`
- Candidate catalogue:
  `art/drafts/kitchen-wall-anchored-2026-10-16-v8/asset-catalogue.json`
- Immutable review page:
  `/keeper-review/kitchen-wall-anchored-v8/`

## Protection boundary

Do not promote, approve, register or wire V8 from this handoff. Kitchen V6,
Kitchen Room V7, Keeper animations, runtime sprites, Final, manifests and
registers are protected and unchanged. If Frank requests another visual
correction, publish a fresh versioned review set rather than rewriting V8.

## Verification recorded by Codex

- Deterministic rebuild digest, identical across two clean builder runs:
  `7063fd8da04b29663be40c9ee503827f4ada4f5076ae5dd886f2d529ac12f647`.
- `node scripts/verify_kitchen_wall_anchored_v8.mjs`: passed.
- `npm test`: passed, including all Kitchen V1–V8 verifiers and 179 Vitest
  tests across 18 files.
- `npm run typecheck`: passed after the production build generated current
  Next.js route types.
- `npm run build`: passed.
- Content-addressed review archive: 88 V8 review images included; no review
  binaries remain under `public/keeper-review`.
- Documentation audit: README, decisions, the machine recipe, human recipe and
  this handoff agree on the 52-lp foot line, 4-lp clear floor, 10 × 12-lp bin,
  counterless white fridge and 19/14-lp layered porthole. No runtime or
  promotion document claims were changed.
