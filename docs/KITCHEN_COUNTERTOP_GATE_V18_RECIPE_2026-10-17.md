# Kitchen countertop Gate V18 recipe

Status: review-only first gate; not approved, promoted or wired.

## Authority

- Visual pixels: exact Kitchen Basic Assets V5 only.
- Geometry values: Option B values only—`1.5 lp` (`6 px`) visible top,
  `2 lp` (`8 px`) fascia, zero shear, equal-width front/rear edges.
- Never copy candidate pixels from the historical A/B/C page or Kitchen
  V6–V16.
- V17 remains an immutable exact-V5 rollback.

## Bay and contact construction

- Density: `4 px/lp`.
- Cell: `21 lp` / `84 px` wide.
- Opaque structure: x `2..81` inclusive (`20 lp`), leaving x `0..1` and
  `82..83` transparent.
- Worktop/hob contact is exactly `19 lp` above the bottom anchor. Therefore:
  - kettle, `31 lp` high: contact row `48 px`;
  - cooker, `28 lp` high: contact row `36 px`;
  - sink, `29 lp` high: contact row `40 px`.
- The rear edge is exactly six rows above the contact row. No rear ridge,
  splashback substitute, stepped shoulder, taper or convergence is allowed.
- Cabinet fronts remain true rectangles with parallel verticals.

## Semantic layering

1. Begin with the exact V5 standard raster.
2. Clear the complete inherited tapered-surface region, beginning at its first
   measured row; do not clear only the nominal new slab.
3. Draw one continuous 20-lp structure from a V5 centre-material sample which
   contains no inherited side outline.
4. Restore only a measured appliance silhouette above that structure.
5. Never restore a rectangular crop after step 3. A rectangular restore can
   silently paste the old tapered worktop back into the candidate.
6. Draw no second lip, rail, rear ledge or decorative strip that reads as
   another worktop layer.

The kettle's exact V5 appliance pixels move down `1 lp` so its contact shadow
rests on the corrected rear edge. The sink uses a row-measured tap/basin mask;
its wooden wings are excluded. The cooker preserves the declared backsplash
and centre burner information but discards the inherited tapered outer hob.

## Binding verification

For every candidate:

- derive the contact row from cell height rather than a shared hard-coded row;
- require every x `2..81` structure pixel to be opaque on every structure row;
- compare exact RGBA between the candidate and semantic structure wherever the
  appliance mask is transparent;
- require both shared cell edges to remain transparent;
- run the same detector against the historical Option-B candidate and require
  it to fail;
- preserve SHA-256 snapshots of V5, V17, runtime manifest, Final/workbench and
  approved Keeper source.

Alpha continuity alone is not a sufficient countertop test.

## Rear-wall review staging

The three gate assets are placed in adjacent `21-lp` bays without scaling.
Their bottom anchors sit on the `52-lp` rear-wall foot line in a `56-lp` room.
The wall/floor junction is `51 lp`; the final `4 lp` is a clear foreground
walking channel. The staging shell uses neutral pale trim and thin separators,
not a heavy wooden picture frame. This context is evidence only, not a full
room-shell approval.
