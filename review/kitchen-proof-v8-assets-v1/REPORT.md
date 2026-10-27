# Kitchen v8 Day-1 asset completion report

Status: **DONE as a versioned review candidate; not runtime-promoted**.

## Completed

- Twelve visible Day-1 object types, including one master reused for the two
  matching base cupboards and a deterministic mirror for the second chair.
- One-unit (`126` px) old-school cooker retained exactly from the praised v2
  correction; eye-level hood/grill, four controls and one status bezel.
- Separate refrigerator and lower-oven doors over complete fixed interiors.
- A review-only oven-light demonstration plus production cooking and burnt
  contents sprites; production metadata records `lightRectPx` for the engine.
- Review-only demonstrations of the engine-drawn status lamp for fridge,
  cooker, kettle, toaster and mixer; production metadata records points only.
- Individual item metadata, exact canvas sizes, state paths and layer
  registration coordinates.
- Review at 2×, 1:1 and 1/8, plus dedicated technical-layer and status sheets.

## Deliberately not done

- No `252` px future range; Frank deferred it.
- No assembled kitchen room, shell, windows, flooring or runtime placement.
- No runtime/canon promotion and no Keeper generation or mutation.
- No broken/dirty art states; those remain engine overlays.

## Verification

`verify_assets.py` checks source/output hashes, declared canvas sizes,
transparent safety gutters, zero exact/near-magenta pixels, byte-identical
inheritance of the three praised v2 masters, deterministic chair mirroring,
registered doors/interiors, partial-alpha oven glass, state-overlay geometry,
individual metadata and the absence of any range asset.
