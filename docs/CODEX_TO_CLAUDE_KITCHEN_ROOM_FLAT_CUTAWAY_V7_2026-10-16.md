# Kitchen Room V7: Codex → Claude hand-back

**Date:** 16 October 2026

**Status:** room and sink-porthole review draft; unapproved, reversible and unwired

**Review page:** `/keeper-review/kitchen-room-flat-cutaway-v7/`

## What changed

The kitchen room shell is redrawn to the same `flat-cutaway-v1` basis now used
by the Option B furniture: straight-on camera, zero horizontal or vertical
convergence, constant scale and parallel architectural bands. Residual diagonal
floor joints are removed. The room remains 56 lp high with an exact 5-lp floor
band and exact `4 + 21n` widths for six through twelve bays.

The V6 furniture family is unchanged. A new `obj_sink_porthole` is a separate
wall-mounted child of the sink rather than a room decoration. Its 21 × 56-lp
cell, 15-lp outer ring and 3-lp side gutters keep it inside the sink's bay. Its
centre is 37.5 lp above the floor and it translates by exactly the same delta
as the sink. The 9-bay starting layout owns it in bay 7; the 12-bay reservation
shows it with the sink reservation.

## Measured room pieces

| Item | Cell | Assembly role | Key datum |
| --- | ---: | --- | --- |
| stair-side cap | 46 × 56 lp | rightmost 4-lp crop contributes to shell | crop `[42,0,46,56)` |
| repeat A/B/C | 21 × 56 lp | one whole bay each | identical left/right edge columns |
| far cap, closed/open | 38 × 56 lp | right-aligned overlay; 0-lp contribution | side wall x 34–38; hinge x 37 |
| sink porthole | 21 × 56 lp | sink-owned wall child, z 25 | 15 × 15-lp bound; centre `(10.5,18.5)` |
| 9-bay shell | 193 × 56 lp | starting room | sink/porthole bay 7 |
| 12-bay shell | 256 × 56 lp | maximum reservation | whole modules only |

The cupboard's exact V6 rectangular leaf remains the foreground occluder. A
closed leaf is not drawn on the back wall; the visible open leaf is still
hinged on the right and extends left. Keeper art and cupboard choreography are
unchanged.

## Files

- precise recipe: `docs/KITCHEN_ROOM_FLAT_CUTAWAY_RECIPE_2026-10-16.md`;
- machine recipe: `data/kitchen_room_flat_cutaway_recipe.json`;
- builder: `scripts/build_kitchen_room_flat_cutaway_v7.py`;
- verifier: `scripts/verify_kitchen_room_flat_cutaway_v7.mjs`;
- source/provenance: `art/source/kitchen-room-flat-cutaway-2026-10-16-v7/`;
- raw draft: `art/raw/kitchen-room-flat-cutaway-2026-10-16-v7/`;
- records: `art/drafts/kitchen-room-flat-cutaway-2026-10-16-v7/`;
- review: `public/keeper-review/kitchen-room-flat-cutaway-v7/`.

Kitchen V6, Keeper sources, runtime sprites, Final and manifests are
hash-protected. Rejecting V7 requires discarding only these new V7 files.

## Verification

- deterministic rebuild digest, identical across two consecutive runs:
  `d7726fdae15fe847bd7eed31edd571aafca1c8312e69cebe5f95352c7ff21200`;
- `npm run verify:kitchen-room-flat-cutaway-v7` passes;
- `npm test` passes: 18 test files and 179 unit tests, plus all repository
  asset and review verifiers;
- `npm run typecheck`, `npm run build` and `git diff --check` pass;
- review media is content-addressed and absent from the public review folder;
- production deployment and browser loading are checked after the delivery
  commit.

The documentation audit covered `README.md`, `docs/DECISIONS.md`, the precise
recipe and this hand-back. Existing setup, architecture, Keeper-animation,
deployment and backlog guidance remains accurate because V7 changes no runtime
or animation contract.
