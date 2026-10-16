# Kitchen V9 dimensional fridge and attached-shelf recipe

Date: 17 October 2026  
Status: review draft; not approved, promoted or wired  
Machine authority: `data/kitchen_fridge_shelf_v9_recipe.json`

## Scope and visual authority

V8 remains the sole room/family baseline. V9 changes only the refrigerator and
adds one separate refrigerator-owned wall child. The V5 fridge is consulted
only for its richer bevel/highlight/shadow treatment; no V5 wooden countertop
is retained. Frank's supplied room image is consulted only for the shelf,
plant, blue pot and cream-jar arrangement.

The `image_gen` study in
`art/source/kitchen-fridge-shelf-2026-10-17-v9/` is reference evidence. The
review sprites are drawn deterministically by
`scripts/build_kitchen_fridge_shelf_v9.py` and contain no generated-study
pixels.

## Grid and projection

- Density: exactly 4 raster pixels per logical pixel (`lp`).
- Projection: `flat-cutaway-v1`, straight on, with zero convergence and no
  depth scaling.
- Bay: exactly 21 lp.
- Room height: exactly 56 lp.
- Fridge bottom-centre anchor: `(10.5, 21) lp` inside its cell.
- Room placement: unchanged V8 foot line at `y=52 lp`, leaving the last 4 lp
  of foreground floor clear.

## Refrigerator construction

The refrigerator remains a `21 × 21-lp`, one-bay appliance with interaction
spot `284 ku`. Its standard opaque bound is `19.5 × 20.5 lp`, starting at
`(0.75, 0.5) lp` inside the cell.

It has no furniture countertop. The top is a white enamel appliance lid built
from an ink silhouette, cool-grey lower bevel, white body and bright highlight.
The body then uses a cool-grey casing return, a bright inset door, a left
highlight, a darker right-side return, door seams, the brass pull and hinges,
a detailed navy grille and two shaded feet.

This hierarchy is mandatory for future white appliances. “White” must not mean
one flat fill: at least four distinct neutral light/shadow values must remain
visible. Brown V6 countertop colours are forbidden in the lid region.

Standard, `on` and `broken` retain the V8 state names. Effects are applied to
one immutable V9 standard base using the existing declared masks.

## Fridge-owned wall shelf

`obj_fridge_wall_shelf_v9` is a separate transparent `21 × 56-lp` wall child.
It is not baked into the fridge or room shell.

- Opaque bound: exactly `19 × 17 lp`.
- Bound origin: `(1, 13.5) lp` from the child-cell top-left.
- Side gutters: exactly `1 lp` each.
- Opaque vertical range: `y=13.5..30.5 lp`.
- Layer: `z26`, behind the `z40` refrigerator.
- Contents: trailing plant, blue pot and two cream pantry jars.
- Shelf board and brackets: straight, horizontal, front-on construction.
- Runtime wiring: none in V9.

The fridge begins at room `y=31 lp`; the wall child ends at `y=30.5 lp`, so
the assets never overlap. The future ownership rule is:

```text
shelfDeltaLp == fridgeDeltaLp
```

Moving the refrigerator to bays 2, 5 or 8 translates both elements by the same
whole-bay offset without changing either asset's bytes or scale.

## Preservation boundary

All other V8 object art and states, the V7 room shell, bin dimensions, Option B
countertops, cooker, sink, table/chair, pet bowl, cupboard and sink-owned
porthole layers remain unchanged. Keeper art, runtime sprites, Final art,
registers, manifests and live-game wiring remain untouched.

## Acceptance checks

- Fridge cell remains 21 × 21 lp and its bound remains inside the cell.
- Fridge lid contains no V6 wood-palette pixel.
- At least four neutral enamel tones remain visible in the body/lid.
- Shelf bound is exactly 19 × 17 lp with one-lp side gutters.
- Shelf bottom remains strictly above the refrigerator top.
- Bay 2→5 and 5→8 moves are each exactly 63 lp for both parent and child.
- The final 4 lp of the 9-bay room remain byte-identical to the V7 shell.
- V8, Keeper, runtime and Final snapshot hashes remain unchanged.

