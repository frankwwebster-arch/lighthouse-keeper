# Kitchen fitted-galley V20 construction recipe

**Status:** review-only recipe; no asset is approved, promoted or wired.

**Review:** `/keeper-review/kitchen-fitted-galley-v20/`

This recipe replaces the freestanding-cupboard construction explored in V5–V19
with fitted kitchen architecture. At Frank's direction, the obsolete Kitchen
V1–V4 and V6–V19 pages were removed from public review tooling on 17 October
2026. Their art trees and review evidence are retained offline under `art/` and
`review-archive/retired/`; exact V5 is the only publicly retained cream/brown
reference and V20 is the new replacement direction.

## 1. Fixed scale

- Author at `4 source px = 1 logical pixel (lp)`.
- One standard UK `60 cm` cabinet is exactly `21 lp = 84 source px` wide.
- The conversion is `2.857142857 cm/lp`.
- The rear-wall foot line is `52 lp = 208 px` in a `56 lp = 224 px` room.
- Rows `52–56 lp` are the Keeper's clear foreground walking channel.
- Every standard cabinet, oven and undercounter appliance owns exactly one
  `21-lp` bay. Internal art may not widen or narrow that bay.

Use real dimensions for props whenever they are known:

| Object | Real width | Calculated width | Drawn envelope |
|---|---:|---:|---:|
| Kettle | 18 cm | 6.3 lp | about 7 lp / 28 px |
| Toaster | 28 cm | 9.8 lp | about 10 lp / 40 px |

Measure future props with `object_lp = object_cm × 21 / 60`. Round only the
final envelope to a useful source-pixel cluster. Props may be dimensional, but
they may not distort the cabinet below them.

## 2. Projection

Use `90% orthographic structure / 10% illustrative depth`.

Cabinet bodies are strict front elevations:

- all verticals parallel and vertical;
- all horizontals parallel and horizontal;
- rectangular bodies only;
- no convergence, trapezoids, rhomboids, side faces or isometric projection;
- no internal feet, thick posts or per-module outer frames;
- identical worktop, fascia, cabinet, plinth and baseline heights in every bay.

Depth is limited to these repeatable source-pixel bands:

| Layer | Depth |
|---|---:|
| Worktop top plane | 3–5 px |
| Worktop front fascia | 2–3 px |
| Shadow under worktop | 1–2 px |
| Recessed plinth | 2–3 px |
| Internal bay seam | 1–2 px |

The top plane has equal front and rear widths and never tapers. Use upper-left
highlights, lower-right shadows, restrained front inset shading and small local
contact shadows beneath props.

## 3. Build architecture, not furniture

Never export six complete freestanding cupboards and then place them beside one
another. Assemble a run in this order:

1. Decide the number and order of `21-lp` bays.
2. Draw one run-wide recessed plinth from the far-left to far-right end.
3. Tile the common flat storm-blue carcass once per bay.
4. Insert the required front layer in each bay: cupboard/drawer, fridge,
   oven-and-grill or sink front.
5. Draw each internal seam exactly once, at the shared bay boundary.
6. Draw one run-wide worktop top plane, one continuous highlight, one fascia
   and one under-worktop shadow across all compatible bays.
7. Apply a left end cap only to the complete run's far-left edge and a right end
   cap only to its far-right edge.
8. Add hob, kettle, toaster, bowl/spoon, sink and faucet as overlays.
9. Add local prop contact shadows without interrupting structural worktop rows.

The oven uses the same bay, baseline and plinth as a counter. Its hob is a
shallow integrated strip. The front has a clearly separate grill compartment
above the oven. The undercounter fridge remains recognisably white enamel, but
fits the same bay and shared run datum.

## 4. Required reusable layers

- `counter-carcass-flat`: the exact `21-lp` internal bay, with no end cap;
- `front-cupboard-drawer`;
- `front-oven-grill`;
- `front-fridge-white`;
- `front-sink`;
- `overlay-kettle-7lp`;
- `overlay-toaster-10lp`;
- `overlay-mixing-bowl-spoon`;
- `overlay-hob-strip`;
- `overlay-sink-faucet`;
- `run-left-end-cap` and `run-right-end-cap`;
- run-width generators for worktop, highlight, fascia and plinth.

The visual palette is deep storm-blue fronts, pale sea-glass worktops,
restrained aged-copper hardware, dark navy outlines and small coral-red prop
accents. Preserve the warmth, colour richness and readable pixel clusters of
the lighthouse concept, not the former cream/brown kitchen family.

## 5. Mandatory continuity test

For every run length and every animation state:

1. Assert each bay is exactly `84 px` wide and all baselines match.
2. Assert worktop top plane depth is constant at every x coordinate.
3. Assert the highlight, fascia and plinth span the whole run without a
   transparent or wall-coloured pixel at an internal seam.
4. Allow interruptions only from declared prop masks, never from copied old
   countertop pixels.
5. Assert internal seams are `1–2 px`; reject doubled seams and black gaps.
6. Assert no end-cap pixels occur at an internal boundary.
7. Assert the two outer caps occur exactly once each.
8. Composite the run at y=`208 px` and reject any cabinet pixel in rows
   `208–223` reserved for foreground walking.
9. Check kettle and toaster envelopes against `28 px` and approximately `40 px`.

This test must operate on full RGBA/colour structure, not alpha alone. The
V6–V16 splintering history proves that alpha-only tests can pass visibly broken
worktops.

## 6. V20 gate boundary

The isolated V20 sheet is a visual appearance reference with transparent
presentation gutters. It is **not** permission to use each displayed outer
outline as a middle-module edge. The joined kettle–oven–sink room proof is the
construction authority. Exact reusable layers and the complete state family
come only after Frank accepts this gate.

Rollback is deletion of the V20 source/raw/draft/review directories and its
V20 scripts/docs. Exact V5 and all runtime files remain unchanged.
