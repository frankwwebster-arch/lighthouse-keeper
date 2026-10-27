# Kitchen v8 UK Cottage — complete Day-1 asset review v1

This versioned review set completes the visible Day-1 kitchen object family
from the cooker-corrected v8 style test. It is candidate art only: nothing is
installed in runtime or canon and no room is assembled here.

## Review sheets

- `outputs/kitchen-v8-complete-day1-assets-1x.png` — every visible object at
  exact 1:1 game scale beside the exact Prime Keeper.
- `outputs/kitchen-v8-complete-assets-three-scale.png` — 2× detail, exact 1:1
  room scale and exact 12.5% tower reduction.
- `outputs/kitchen-v8-registered-layers-review.png` — separate fridge and oven
  doors, complete fixed interiors, oven light and cooking/burnt contents.
- `outputs/kitchen-v8-status-lamps-review.png` — dark painted bezels plus
  separate engine-driven green overlays.

## Delivered objects

- cream larder fridge;
- Belfast sink cabinet;
- painted base cupboard (one master reused twice);
- old-school one-unit gas cooker with eye-level hood/grill;
- scrubbed-pine table;
- wooden chair plus deterministic mirrored orientation;
- painted dresser;
- enamel pedal bin;
- enamel electric kettle;
- cream toaster;
- stand mixer; and
- painted wall cupboard.

Every standard freestanding/cabinet unit is `126` px wide. The cooker is one
standard unit. The later range is fixed at exactly two standard units
(`252` px) but Frank explicitly deferred it, so it is not drawn in this set.

## Technical delivery

The exact 1:1 canvases live in `outputs/`. Registered technical layers and
review-only engine-light demonstrations live in `outputs/states/`. Each object
has an `items/<id>/item.json` record containing
its canvas, quantity, state files, bottom-left anchor and, where relevant,
door pivots, contents offsets, light rectangle and status-bezel coordinates.

The approved closed fridge/cooker paintings remain visual authorities. The
technical runtime candidate uses an unchanging fixed body plus a separate door
on the same fixed canvas; closed/open views are compositions, not redrawn item
states. The cooker glass contains genuine partial alpha so the engine-drawn
light and contents sit behind it. The fridge has a right-hinged door; the oven
has a bottom hinge. Green lamp and warm oven-light PNGs are review evidence
only and are deliberately absent from `item.json`: the engine draws those
lights from the recorded points/rectangle. No state changes an object boundary.

## Rebuild and verify

```sh
python3 review/kitchen-proof-v8-assets-v1/build_assets.py --finalise
python3 review/kitchen-proof-v8-assets-v1/verify_assets.py
```

Pillow is required. `PROMPT_LOG.md` records the built-in image-generation
method and prompt contracts. `REPORT.md` records completion and remaining
boundaries.
