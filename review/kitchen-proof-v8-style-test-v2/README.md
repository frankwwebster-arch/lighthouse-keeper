# Kitchen v8 UK Cottage — Step 1 cooker correction v2

This immutable review successor corrects only the rejected narrow cooker from
`review/kitchen-proof-v8-style-test/`. The Belfast sink and painted dresser are
carried forward byte-for-byte.

Primary review image:

`outputs/kitchen-v8-cooker-correction-v2.png`

The replacement is an old-school British gas cooker with:

- an exact `126 × 252` px game canvas;
- one standard-unit (`126` px) width;
- four burners and exactly four copper controls;
- one dark engine-driven status bezel;
- an eye-level hood/grill with its own tray and handle; and
- a closed lower oven with a copper handle and dark glass.

The future range is **not drawn here**. Frank fixed it at exactly two standard
units (`252` px), to be designed in a later task.

Supporting review images show the corrected three-piece family at `2×`, exact
`1:1`, and exact `12.5%` tower scale beside the unchanged Prime Keeper. The
old `101 × 180` cooker remains visible only in the correction comparison and
was not overwritten.

## Boundary

- Review candidates only; no runtime or canon promotion.
- No room, shell, layout or future range was built.
- Exact closed cooker art from this folder is the visible authority used by
  the complete Day-1 asset review in `review/kitchen-proof-v8-assets-v1/`.
- Every 1:1 candidate has a two-pixel transparent edge gutter and contains no
  exact or near-magenta pixels.

## Rebuild and verify

```sh
python3 review/kitchen-proof-v8-style-test-v2/build_style_test.py \
  --sink review/kitchen-proof-v8-style-test-v2/sources/sink-pass-02-final.png \
  --dresser review/kitchen-proof-v8-style-test-v2/sources/dresser-pass-02-final.png \
  --cooker review/kitchen-proof-v8-style-test-v2/sources/cooker-old-school-grill-pass-01-final.png
python3 review/kitchen-proof-v8-style-test-v2/verify_style_test.py
```

Pillow is required. `PROMPT_LOG.md` records the built-in image-generation
mode, references and prompt contract.
