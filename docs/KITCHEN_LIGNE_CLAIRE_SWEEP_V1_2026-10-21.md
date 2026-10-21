# Kitchen Ligne-Claire Sweep V1

Date: 21 October 2026

Review: `/keeper-review/kitchen-ligne-claire-sweep-v1/`

Status: rejected visual-review candidate; preserved as an immutable historical
pack; never approved, registered, promoted or wired.

## Outcome

V1 translates the complete active kitchen furniture/object review inventory into
one coordinated ligne-claire candidate language. It uses the approved
`sandwich-tomato` V2 as the primary small-scale calibration. Frank's first six
supplied original comic images are secondary furniture, architecture and contour
references; five later seascape panels extend the same codified language to
future sea, cliff, weather and boat work without changing this furniture pack.
The binding recipe is
`docs/KITCHEN_LIGNE_CLAIRE_ART_RECIPE_2026-10-21.md`.

Frank rejected this pass on 21 October 2026. Exact canvas and alpha preservation
did not preserve every visible internal shape strongly enough: the fridge
worktop lost definition and the oven read too flat. Cabinet-only V2 supersedes
V1 for review without overwriting it; see
`docs/KITCHEN_CABINET_LIGNE_CLAIRE_V2_2026-10-21.md`.

The pack contains 53 candidate PNGs in twelve families:

- Cabinet A and Cabinet B, including all exposed/joined edge variants;
- the five compositor-owned join/healing layers;
- coordinated fridge Standard/Broken states;
- dishwasher Off/On/Broken and all twelve edge/state variants;
- oven Off/On/Broken, three registered Broken lighting variants and both
  full-state 40-frame flicker strips;
- sink Standard/On-base/Broken-base;
- kettle Off/On/Broken high-resolution masters;
- toaster Off/On/Broken;
- mixing bowl Off/On/Broken;
- table with rear-facing chair;
- pedal bin Standard/Broken.

Effect-only water, steam, smoke, heat, smell, flies, suds, sparks and drip files
are not furniture pixels and remain byte-identical. Full-state oven lighting
strips are included because they contain the appliance itself.

## Geometry lock

The conversion changes RGB only. Each candidate retains the source file's exact
canvas and byte-identical alpha channel. This deterministically preserves alpha
bounds, transparent padding, position, footprint and sprite registration. The
source catalogue files which define anchors, pivots, collision geometry, grid
origins, support surfaces, interaction stops, state transitions, movement lock,
effect ownership, frame counts and timing are hash-pinned but not modified.

The complete room proof places current and candidate Standard/Broken sets on the
same exact `772 × 224` room and canonical bay datums. Family contact sheets show
every source beside its candidate on transparency. The review page exposes all
53 comparisons and makes no registration call.

## Generation evidence

One built-in image-generation study combined the current full room, tomato V2
and a contact board of all six supplied references. It is retained only as a
non-authoritative line/palette study. Because it could not guarantee exact
geometry, no generated pixel became a candidate asset.

Production candidates instead use a deterministic, lossless process:

1. preserve the exact RGBA canvas and alpha bytes;
2. retain decisive inherited dark construction marks;
3. add an inside-only one/two-pixel contour using exact tomato ink `#051824`;
4. map visible RGB to the recipe's recorded non-dithered spot palette;
5. write a new candidate path and record source/candidate SHA-256 values.

## Rebuild and verification

```sh
/usr/bin/python3 scripts/build_kitchen_ligne_claire_sweep_v1.py
npm run verify:kitchen-ligne-claire-sweep-v1
npm run maintain:keeper-review
npm test
npm run typecheck
npm run build
```

The verifier rejects missing assets, hash drift, canvas/mode drift, any alpha or
alpha-bound change, a non-spot colour, inherited-effect drift, contract drift,
incomplete contact-sheet coverage, stale pack checksums or an open registration
guard.

## Approval and rollback boundary

`batch-register.json` has `register: false`, `promote: false` and no current
selector changes. Frank must explicitly approve the candidate before any
registration, Final copy, selector update or runtime wiring.

Rollback is immediate: discard only
`art/drafts/kitchen-ligne-claire-sweep-2026-10-21-v1/` and the matching review
set. Every current, approved, source and runtime file remains byte-for-byte in
place.
