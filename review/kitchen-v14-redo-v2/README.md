# Kitchen v14 redo v2 — corrected review candidate

This versioned draft replaces only the invalid v1 cooker-door source. The v1
draft remains untouched and reversible. Its generated door was 1680 × 936,
included oven racks/interior pixels that belonged to the fixed body, and was
cover-cropped to force the 150 × 82 px moving-door footprint. V2 uses a newly
painted door-only source, alpha-trims it, scales it uniformly, and pads it into
the exact footprint without cropping or distortion.

Source SHA-256:

- v1 rejected cooker door: `ff82493dd287ac7e62dee342361354656f01e5fc6c17ca11a65b082e352a18fe`
- v2 replacement cooker door: `7bde6254ad2c87de80ae5f624cf20d6a81127005414a1568b326c25516cca2cb`

This is the painted redo authorised by the GO note in section 19 of
`docs/SPEC.md`. It uses the exact rectangles from
`docs/layout/kitchen_v14_schematic.json`, reuses only the approved v8 room
shell, and does **not** reuse artwork from rejected commit `c9c3f6c6`.

Review these files:

- `outputs/kitchen-v14-redo-v1-v2-door-comparison.png` — unchanged v1 and
  corrected v2 cooker doors side by side, both alone and on the cooker.
- `outputs/kitchen-v14-redo-v8-comparison.png` — new room beside the approved
  v8 room proof at exact 1:1, plus the approved v8 pieces and the 1/8 room.
- `outputs/kitchen-v14-redo-two-viewing-scales.png` — full room at room view
  (2048 × 576) and lighthouse view (256 × 72).
- `outputs/kitchen-v14-redo-contact-sheet.png` — every exact schematic part.
- `outputs/kitchen-v14-redo-door-light-contents-demos.png` — fixed-body and
  removable-door contracts for the fridge, cooker and larder.
- `outputs/kitchen-v14-redo-assembled-room-1x.png` — the exact 1:1 room.

The source art under `sources/imagegen/` was painted with OpenAI's built-in
image generator. The build script only crops, uniformly scales, pads, places,
masks alpha, assembles and annotates review sheets. It never draws item or room
art. The Prime Keeper is copied from the approved 2× Prime source and uniformly
registered without repainting. The empty room shell is the approved v8 shell.

Status: **review candidate awaiting Frank**. Nothing is installed in the
runtime and no production asset is promoted.

Rebuild and verify:

```sh
/Users/frank/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 review/kitchen-v14-redo-v2/build_kitchen_v14_redo.py
/Users/frank/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 review/kitchen-v14-redo-v2/verify_kitchen_v14_redo.py
```
