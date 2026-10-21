# Kitchen Cabinet Ligne-Claire V2

Date: 21 October 2026

Review: `/keeper-review/kitchen-cabinet-ligne-claire-v2/`

Status: rejected by Frank on 21 October 2026; never approved, registered,
promoted or wired. Preserved as immutable review history.

Frank rejected V2 because recolouring only Cabinet A/B left the fridge worktop
and sink cabinet outside the fitted-family palette. The V2 contact sheets and
web reviewer also used nearest-neighbour/pixelated enlargement, which made the
result appear more jagged. The rejection is pinned in
`docs/review/kitchen-cabinet-ligne-claire-v2-rejection-2026-10-21.json`.
The clean successor is Kitchen Fitted-Cabinet Ligne-Claire V3 at
`/keeper-review/kitchen-fitted-cabinet-ligne-claire-v3/`.

## Why V2 exists

The full-kitchen Ligne-Claire V1 pass is rejected. Although it kept canvas and
alpha bytes exact, its broad palette collapse did not retain every visible
internal shape strongly enough: the fridge worktop lost definition and the oven
read too flat. V2 does not amend or overwrite V1. It starts a new dated pack and
reduces the review scope to cabinets and their healing layers.

## Included scope

V2 contains thirteen new files:

- all four exposed/joined variants of Cabinet A;
- all four exposed/joined variants of Cabinet B;
- the exact five compositor-owned join/healing layers used by the existing
  modular kitchen.

Fridge, oven, dishwasher, sink, kettle, toaster, bowl, bin and table/chair are
explicitly excluded. Their current bytes and selectors remain unchanged.

## Strong shape lock

Every candidate is an RGB-only translation of its current authority. The
builder performs no resize, crop, rotation, dilation, erosion, new silhouette
construction or alpha edit. In addition to exact canvas, alpha, alpha bounds and
transparent padding, V2 independently hashes the source masks for:

- the worktop;
- the cabinet body;
- handles and hinges;
- dark construction lines;
- neutral residual pixels.

Those semantic masks are the visible shapes. Their membership and pixel
positions are immutable. Colour tiers may change, but no pixel can move from one
shape to another.

## Movement and healing

V2 does not replace or edit the movement/healing implementation. It hash-pins
the V38 split-cabinet and V41 dishwasher catalogues, their deterministic
verifiers and the modular join standard. Those authorities retain:

- six exact 84-pixel bay origins;
- independent Cabinet A/B movement;
- occupied-bay swapping;
- exposed-versus-joined edge selection;
- pair-aware countertop caps, triangle underlays, body backfill and neighbour
  seam cleanup;
- the existing movement locks, repair unlock and asset-local ownership rules.

The review pack includes origin-contiguous, dislocated-contiguous and
separated-exposed current-versus-candidate room proofs on the identical room
datums. The unchanged V38/V41 workbenches remain the interactive behavioural
authorities. Their exhaustive tests cover the existing 720-layout compositor.

## Rebuild and verification

```sh
PYTHONDONTWRITEBYTECODE=1 /usr/bin/python3 scripts/build_kitchen_cabinet_ligne_claire_v2.py
npm run verify:kitchen-cabinet-ligne-claire-v2
npm run maintain:keeper-review
npm test
npm run typecheck
npm run build
```

The V2 verifier rejects any source/candidate hash drift, canvas or alpha change,
semantic-mask drift, non-spot colour, movement/healing contract change, stale
pack checksum or open registration guard.

## Approval and rollback

`batch-register.json` keeps `register` and `promote` false and contains no
selector changes. Nothing becomes current without Frank's explicit approval.

Rollback is immediate: discard only
`art/drafts/kitchen-cabinet-ligne-claire-2026-10-21-v2/` and its matching review
set. V1, every current asset, approved source and runtime file remain intact.
