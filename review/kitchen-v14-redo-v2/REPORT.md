# Kitchen v14 redo v2 — verification report

- Amendment: v1's cooker-door source is rejected for wrong source dimensions,
  cover-cropping, and oven-interior pixels in the moving layer. V2 changes only
  that asset in a separate draft and leaves v1 byte-for-byte recoverable.
- Corrected cooker door: newly painted door-only source, uniformly contained
  and transparently padded into the exact 150 × 82 px visible footprint on the
  168 × 336 px registered cooker canvas. No cover crop or distortion.

- Scope: tier-1 Kitchen v14 review candidate only.
- Geometry: exact 2048 × 576 room and exact rectangles from the approved v14
  schematic.
- Art method: every new visible item is image-generator painted; deterministic
  code only crops, uniformly scales, pads, places, masks alpha and assembles.
- Rejected candidate: no artwork from `c9c3f6c6` is reused.
- Shell: approved v8 one-point-perspective shell, symmetric about x = 1024.
- Furniture projection: front-on with shallow straight-up top reveals.
- Keeper: approved Prime source, unchanged and registered to soles y = 502.
- Openable items: fridge, cooker and larder use fixed bodies with complete
  interiors and separate removable doors.
- Cooker stack: separate body, semi-transparent door glass, separate cooking
  and burnt contents; engine light/status remain engine-owned.
- Two scales: exact room view 2048 × 576 and exact lighthouse view 256 × 72.
- Lighthouse read: cream fridge/cooker and the duck-egg cabinet/dresser/larder
  blocks remain distinct; knobs, panel bevels, plate decoration and clock hands
  intentionally disappear at 1/8.
- Runtime: untouched; approval and integration deliberately deferred.
