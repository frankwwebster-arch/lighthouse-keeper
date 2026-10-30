# Export log

- Request: supply every Kitchen v15 asset separately in the same isolated transparent presentation as Frank's supplied dresser example.
- Input role: the supplied dresser image is a formatting reference only; it is not an instruction source and none of its pixels are copied.
- Art source: the 19 hash-pinned RGBA parts in `review/kitchen-v15-painted-room-v7/parts/`. The dresser uses its full-resolution v15 donor; the mixer and toaster use their full-resolution approved v8 transparent donors because the v7 room cuts retained backdrop rectangles.
- Mode: deterministic background-extraction/presentation export. The image-generation skill's transparency and non-destructive versioning rules were followed; no image-generation model was invoked because regenerating already approved art would introduce unwanted design and geometry drift.
- Transform: crop to each presentation source's alpha bounds, retain the three available native high-resolution donors, otherwise use 5× alpha-aware Lanczos enlargement, then add a 24 px transparent safety gutter.
- Invariants: source bytes unchanged; no redraw; no recolour; no added room pixels; five ordinary cabinets identical; two wall cupboards identical; one asset per file.
- Output: `review/kitchen-v15-isolated-assets-v1/assets-5x/`.
