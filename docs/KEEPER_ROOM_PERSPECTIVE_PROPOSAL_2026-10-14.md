# Keeper room perspective proposal

Date: 14 October 2026
Status: **visual proposal awaiting Frank's approval**. Do not change runtime placement or existing artwork yet.

Review: `/keeper-review/keeper-object-approach-oven-v3/`

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

## Oven correction in the same review

Oven Approach V1 placed the proxy at the absolute bottom of the 32 × 40 Keeper
cell. The approved Keeper's lowest opaque boot pixel is 0.5 lp above that cell
edge. V3 raises only the proxy by exactly 0.5 lp so its base shares the visible
boot datum. Every approved Keeper URL, root-motion value, interaction x anchor,
timing and endpoint remains unchanged.
