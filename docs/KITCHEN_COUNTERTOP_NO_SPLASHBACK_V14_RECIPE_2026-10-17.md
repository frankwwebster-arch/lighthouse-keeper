# Kitchen countertop V14: no splashback recipe

Frank identified the remaining V13 defect correctly: its smooth full slab still exposed a raised rear reveal on either side of each appliance. Because the appliance interrupted that reveal, it read as a stepped, broken splashback. V14 removes the rear reveal entirely.

## Binding construction

- Retain one front-facing countertop fascia only: x 2–81 px and `frontY` through `frontY + 7`, exactly 20 × 2 lp.
- Clear the complete former rear zone from `frontY - 6` through `frontY - 1` before rebuilding the fascia.
- Restore only genuine appliance pixels in that zone. Never restore any of the four countertop wood colours, and hard-clip the mask to the declared appliance x interval.
- Kettle, toaster and mixer may not interrupt the front fascia. The sink basin may overlap only x 23–61 px; both exposed wings remain byte-equal to the fascia template.
- Apply this construction independently to every standard, on and broken frame. Do not inherit V13's full slab or V10's grown restoration mask.

## Mandatory test

`npm run verify:kitchen-countertop-no-splashback-v14` rejects any countertop-wood pixel above the fascia, any opaque rear-zone pixel outside its appliance interval, any transparent fascia pixel, and any non-canonical fascia RGBA value. V13 is a required failing control, so weakening the test until the old ridge passes is itself a failure. The verifier runs from `npm test`.

V14 remains a reversible review draft. No runtime, Final, Keeper, manifest or live-room asset is changed.
