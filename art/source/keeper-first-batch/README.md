# Keeper first production batch

`keeper-turnaround-source.png` is the untouched image-generation study used to
settle the keeper's identity: navy cap, blue work jumper, cream stripe and
beard, dark trousers and boots. It uses the approved CRT as its rendering
reference and the lighthouse master image as its world/palette reference.

`author_keeper.py` is the deterministic production source. It redraws the
keeper on the locked 32 x 40 logical canvas at density 4, with hard alpha and
integer coordinates. Run it with the bundled workspace Python:

```sh
/Users/frank/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 \
  art/source/keeper-first-batch/author_keeper.py
npm run sprites
python3 scripts/build_floor_asset_catalogue.py
```

The batch supplies aligned front/back master parts and the first required
clips: idle, walk, cook back, wash back and brush-teeth back. The review canvas
embeds the resulting runtime strips automatically after it is rebuilt.

The generated study is reference material, not a runtime sprite. The authored
PNGs in `art/raw/keeper-first-batch/` are the review candidates.
