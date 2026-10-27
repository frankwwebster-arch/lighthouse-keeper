# Kitchen v14 redo — review candidate

This is the painted redo authorised by the GO note in section 19 of
`docs/SPEC.md`. It uses the exact rectangles from
`docs/layout/kitchen_v14_schematic.json`, reuses only the approved v8 room
shell, and does **not** reuse artwork from rejected commit `c9c3f6c6`.

Review these files:

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
/Users/frank/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 review/kitchen-v14-redo-v1/build_kitchen_v14_redo.py
/Users/frank/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 review/kitchen-v14-redo-v1/verify_kitchen_v14_redo.py
```
