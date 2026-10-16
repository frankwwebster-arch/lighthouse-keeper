# Kitchen countertop Option B recipe

**Authority:** selected by Frank, 16 October 2026

**Machine-readable record:** `data/kitchen_countertop_option_b_recipe.json`

**Reusable constructor:** `scripts/kitchen_countertop_option_b.py`

Use this recipe for every future kitchen asset whose structural top is a
countertop, hob or matching table surface. It defines construction, not asset
approval or promotion.

## Reserve geometry before drawing

1. Author at density 4: one logical pixel is four source pixels.
2. Reserve the complete logical cell and anchor first.
3. An ordinary unit owns one 21-lp / 84-px bay. Its opaque width is at most
   20 lp / 80 px, centred with a 0.5-lp / 2-px transparent gutter on each side.
4. A two-bay table owns 42 lp / 168 px. Its structural top is 40 lp / 160 px,
   centred with a 1-lp / 4-px gutter on each side.
5. Never let an outline stroke, effect, shadow or moving part enter a shared
   edge column. Check the rendered pixels, not only the intended coordinates.

## Draw the selected top

- visible top: exactly 1.5 lp / 6 px;
- fascia: exactly 2 lp / 8 px;
- shear: 0;
- rear-edge scale: 1;
- rear and front edges: horizontal and equal in width;
- side edges: vertical and parallel;
- structural front: a true rectangle with equal top and bottom width;
- common V5 palette, outline weight and highlight treatment;
- no vanishing point, rear-edge narrowing, taper, wedge or V-shaped join.

The table uses the same construction over its wider 40-lp edge. Appliances may
retain curved self-volume, but that volume never changes the top construction.
The freestanding fridge must remain unmistakably an appliance rather than a
painted cabinet door.

## Animate from one base

Finish the standard base once. Every `on`, `broken`, open or effect frame starts
from those exact bytes. Define one or more moving-part/effect rectangles, draw
only inside them, and verify every RGBA channel outside them is byte-identical
to the standard base. Never resize, shift, recolour, sharpen or re-render the
base per frame.

## Verify and publish

- exact strip and sidecar geometry;
- exact anchors, interaction spots and 19-lp work/hob/table datum;
- 11-lp chair seat where applicable;
- transparent shared edges in every frame;
- exact 80-px ordinary and 160-px table envelopes;
- fixed pixels outside state masks;
- one construction and palette across counterparts;
- whole-bay room snapping and 6–12-bay shell dimensions;
- immutable V5, runtime, Final and Keeper sources;
- a new content-addressed, preload-safe review page.

Keep every pass reversible. A new asset is a draft until Frank explicitly
approves it; approval and runtime promotion remain separate steps.
