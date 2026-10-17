# Kitchen countertop continuity V13 recipe

V10's countertop assertion was insufficient: it checked only that one row was opaque. Opaque appliance-mask pixels could therefore replace the intended wood colours and outlines while still passing. V13 treats the complete Option-B slab as protected structure.

## Binding construction

- Cell: 21 lp wide at density 4; the slab occupies x 2–81 inclusive, giving the selected 0.5-lp side gutters.
- Slab band: 14 raster pixels, from `frontY - 6` through `frontY + 7` inclusive.
- Kettle, toaster and mixer: the complete 80 × 14-pixel band must equal the canonical Option-B RGBA template exactly in every frame.
- Sink: the basin may occlude only x 23–61 inclusive. Both exposed wings must equal the canonical template exactly; the restoration mask is hard-clipped so antialias growth cannot escape.
- Every pixel across the complete slab band remains opaque, including the intentional sink-basin interval.
- Apply the canonical slab after the inherited V10 frame. Restore only the sink basin inside its declared interval. Never recover an appliance with an unconstrained grown mask.

## Mandatory automated gate

`npm run verify:kitchen-countertop-continuity-v13` checks every pixel of every standard, on and broken frame. It compares exact RGBA values, not merely alpha. It also runs V10 as a required failing control: the standard frames contain 148 kettle, 111 toaster, 167 mixer and 248 exposed-sink structural mismatches outside the final hard-clipped basin interval. If those negative controls ever pass, test sensitivity has been lost and the gate fails.

This verifier is part of `npm test`. Future countertop assets must use the same full-band exact-structure test, adjusted only for a narrowly declared, visually necessary appliance occlusion.

## Boundary

V13 is a reversible review draft. V10 and V12 remain immutable. No runtime sprite, live room, manifest, Keeper animation or Final asset is changed.
