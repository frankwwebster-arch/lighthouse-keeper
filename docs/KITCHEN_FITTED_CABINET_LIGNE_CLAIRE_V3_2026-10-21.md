# Kitchen Fitted-Cabinet Ligne-Claire V3

Date: 21 October 2026

Review: `/keeper-review/kitchen-fitted-cabinet-ligne-claire-v3/`

Status: approved immutable fitted-family visual authority; not promoted or
wired. Approval is recorded externally so the dated pack remains unchanged:
`docs/review/kitchen-fitted-cabinet-ligne-claire-v3-approval-2026-10-21.json`.

## Why V3 exists

Frank rejected Cabinet V2 because it recoloured only Cabinet A/B. The unchanged
fridge worktop and sink cabinet then failed to match the rest of the fitted
family, while V2's nearest-neighbour evidence and CSS pixelated enlargement
introduced a false jagged look. V2 remains untouched and its exact hashes are
pinned by
`docs/review/kitchen-cabinet-ligne-claire-v2-rejection-2026-10-21.json`.

V3 is a clean, separately dated candidate. It handles the fitted cabinetry as
one coordinated material family and uses smooth inspection rendering.

## Included scope

V3 contains eighteen candidates:

- all eight approved V38 Cabinet A/B exposed/joined variants;
- both V37 fridge states, including the complete worktop and carcass;
- all three byte-identical V19 sink-cabinet state bases;
- all five V41 compositor join/healing layers.

The oven, dishwasher and small countertop objects remain current and unchanged.
No effect or animation strip is redrawn.

## Exact-geometry and detail lock

The builder changes RGB only. Every candidate keeps the exact source canvas,
alpha bytes, alpha bounds, transparent padding and semantic membership of:

- construction ink and interior lines;
- worktop pixels;
- cabinet-body pixels;
- hardware and fixture pixels;
- neutral door, basin and residual pixels.

The candidate's semantic masks are reclassified and compared with the source,
not merely recorded from it. Any moved or reinterpreted pixel fails the build.
No resize, crop, blur, contour growth, erosion or detail deletion occurs.

One shared worktop, body, hardware and neutral palette is used across Cabinet
A/B, the fridge and the sink. Broad regions remain spot colours. Narrow,
deterministic transitions around source tonal boundaries retain the calm,
soft-but-clear antialiasing Frank identified in the supplied interior panels.
Every inherited panel edge, worktop lip, hinge, handle, basin line and join cue
remains at its original coordinate.

## Movement, healing and state safety

V3 does not edit implementation. It hash-pins the V19 sink, V37 fridge, V38
split-cabinet and approved V41 movement/healing catalogues and verifiers, plus
the modular authoring standard. This preserves exact bay origins, pivots,
anchors, collision assumptions, occupied-slot swaps, Broken-state movement
locks, repair unlock, effect ownership and the 720-layout pair-aware healing
process.

The inherited fridge drip and both sink-water strips are byte-pinned and remain
separate. The room proof reconstructs all three V38 layouts at their exact
datums with V3 cabinetry and V3 repair layers while leaving the oven current.

## Review presentation

All source/candidate pairs and the complete room proof are generated before any
registration. Contact sheets use Lanczos enlargement; the review page uses
normal browser interpolation. The verifier rejects a return of nearest-neighbour
or CSS pixelated rendering.

The two latest supplied interior panels are copied into the immutable pack as
style evidence for soft clarity and purposeful detail density. A generated
family study is labelled non-authoritative and contributes no candidate pixel.
The approved `sandwich-tomato` V2 remains the primary small-scale calibration.

## Rebuild and verification

```sh
PYTHONDONTWRITEBYTECODE=1 /usr/bin/python3 scripts/build_kitchen_fitted_cabinet_ligne_claire_v3.py
npm run verify:kitchen-fitted-cabinet-ligne-claire-v3
npm run verify:kitchen-sink-smooth-join-v19
npm run verify:kitchen-modular-fridge-workbench-v37
npm run verify:kitchen-split-cabinet-workbench-v38
npm run verify:kitchen-dishwasher-workbench-v41
npm run maintain:keeper-review
npm test
npm run typecheck
npm run build
```

The builder refuses to overwrite an existing V3 public review route. After the
first build, use the verifier only.

## Approval and rollback

`batch-register.json` is the immutable pre-approval snapshot and therefore
continues to record a closed registration gate. Frank approved the exact static
V3 evidence on 21 October 2026; the separate hash-pinned approval record makes
these files the current fitted-family visual authority without rewriting the
pack, promoting Final files or changing runtime selectors.

Rollback is immediate: discard only
`art/drafts/kitchen-fitted-cabinet-ligne-claire-2026-10-21-v3/` and its matching
review set. V1, V2, all approved/source/current files, runtime code and selectors
remain byte-for-byte in place.
