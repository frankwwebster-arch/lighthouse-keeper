# Kitchen v8 UK Cottage — Step 1 style test

This folder contains only the three-piece style test that Frank promoted to GO
on 27 October 2026. Step 2—the complete 2048 × 576 room—has not started.

Primary review image:

`outputs/kitchen-v8-three-scale-review.png`

It shows all three candidates beside the unchanged Prime Keeper at the three
player-facing scales required by section 8-0:

- close-up at `2×`, prepared directly from the high-resolution selected
  sources rather than enlarging the 1:1 reductions;
- room view at exact `1:1`; and
- tower view at `12.5%`, reduced from the reviewed 1:1 candidates.

It also presents the current sampled sage (`#96B0A5`) and a clearer duck-egg
alternative (`#A8CEC6`) for Frank's colour decision.

The supporting style-authority comparison is:

`outputs/kitchen-v8-three-piece-style-test.png`

It shows, on one shared baseline:

- the new Belfast sink cabinet at its `168 × 211` px review envelope;
- the new painted dresser at `150 × 355` px;
- the new small cream cooker at `101 × 180` px;
- the V7 oven authority normalised to the same 0.90 m game-height datum for a
  line/style comparison; and
- the exact Prime Keeper source cell at native 1:1, with opaque sole y `316`
  on the shared baseline.

The generated pieces are candidates, not production sprites. Their individual
1:1 review canvases are in `outputs/`; the three are also collected without
labels in `outputs/three-new-cottage-pieces-1x.png`.

## Boundary

- No room, floor, shell, window, layout, door, state or animation was built.
- No runtime, canon, active manifest or previously approved asset changed.
- No item is promoted. Frank's approval is required before Step 2.
- The cooker is counter height with no eye-level grill: four copper controls,
  one dark unlit indicator/status bezel and a dark unlit oven window. That
  single indicator is engine-lit steady green while working and flashing red
  when broken; there is no second status lamp.
- The generated low-alpha exterior atmosphere is removed before 1:1 review;
  each candidate has at least two fully transparent pixels on every edge.

## Rebuild and verify

```sh
python3 review/kitchen-proof-v8-style-test/build_style_test.py \
  --sink review/kitchen-proof-v8-style-test/sources/sink-pass-02-final.png \
  --dresser review/kitchen-proof-v8-style-test/sources/dresser-pass-02-final.png \
  --cooker review/kitchen-proof-v8-style-test/sources/cooker-pass-03-final.png
python3 review/kitchen-proof-v8-style-test/verify_style_test.py
```

Pillow is required. `PROMPT_LOG.md` records the built-in image-generation
method, references and final prompt set.
