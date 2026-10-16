# Keeper room perspective proposal

Date: 14 October 2026
Status: **superseded for kitchen and standard-room asset authoring on 16
October 2026**. Retain this document and Oven Approach V7 as historical review
evidence only. The current authority is
`docs/KITCHEN_FLAT_CUTAWAY_PROJECTION_SPEC_2026-10-16.md`: a flat cutaway with
constant Keeper/asset scale, no vanishing point or runtime depth scaling, and a
restrained 5-lp floor cue. Do not change runtime placement or existing artwork
from this historical proposal.

Active review: `/keeper-review/keeper-object-approach-oven-v7/`

Historical placement evidence: V3 shared the oven base with the Keeper's foot
datum; V4 raised it only to the 2-lp front lip and was superseded before visual
review. Neither changes approved art or runtime state.

## Decision proposed

Use one restrained perspective system for every room and furnishing instead of
estimating the convergence separately for each asset:

| Datum | Value |
| --- | ---: |
| Notional room depth | 42 lp / 336 ku |
| Existing depth modules | 4 × 10.5 lp |
| Standard furnishing depth | 10.5 lp / 84 ku |
| Front interaction plane | z = 31.5 lp |
| Rear wall / asset rear plane | z = 42 lp |
| Projection distance | 1008 lp |
| Horizon | y = 20 lp in the 56-lp room |
| Rear-wall scale against open front | 96% |
| Asset rear-face scale against its front face | 99% |
| Asset rear-edge rise against its front edge | 0.36 lp |

The projection is `scale(z) = 1008 / (1008 + z)`. It gives exactly 96% at
the 42-lp rear wall and 32/33 at the 31.5-lp interaction plane. Normalising
artwork at that interaction plane makes the rear/front asset ratio exactly
99%. The Keeper and the functional front face of every object therefore stay
at 100% canonical scale.

## Meaning of “all assets have the same depth”

The default authoring box for a furnishing is one 10.5-lp depth module. Its
front face is the interaction plane and its rear face is one module farther
away, normally against the rear wall. This is a visual construction rule, not
a claim that a real sofa and clock are equally deep. A genuine exception may
later declare a different depth, but it must use the same projection formula.

## Grid implications

The placement and locomotion grid does **not** change:

- store x anchors and routes in unprojected keeper units;
- retain the 84-ku / 10.5-lp snap pitch;
- keep the Keeper at canonical scale on the interaction plane;
- keep collision footprints and action anchors orthographic and deterministic;
- bake the subtle convergence into room and asset authoring guides;
- do not continuously rescale raster sprites at runtime.

At density 8, projected positions round to the nearest keeper unit. Bilateral
assets must keep equal left/right rounding, with no more than one ku of error
per side. Because rear faces shrink inward, the projection does not expand an
asset beyond its declared front footprint.

## Rear-wall object and visible floor in the same review

The oven is a rear-wall object, whereas the Keeper walks on the near
interaction line. Oven Approach V7 therefore places the proxy base at the
rear-wall/floor junction, exactly 7 lp above the stage bottom. A 5-lp visible
floor surface runs forward from that junction to the 2-lp front floor lip.
This depth staging—not a runtime scale change—provides the missing perspective
cue and prevents the oven from appearing to share the Keeper's foot line.

V3's 0.5-lp shared datum and V4's unshown 2-lp correction are retained as
rejected/superseded placement provenance. V5 has the same geometry as V6 but
keeps a stale V3 datum label in its large pane. Every approved Keeper URL,
root-motion value, interaction x anchor, timing and endpoint remains unchanged.
V6 tested a 12-lp visible floor and is retained as the rejected deeper control.
