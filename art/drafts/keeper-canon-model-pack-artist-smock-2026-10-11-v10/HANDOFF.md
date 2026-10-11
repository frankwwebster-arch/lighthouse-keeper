# Canon model pack and fresh artist-smock exemplar v10

Status: **one fresh artist-smock first-frame exemplar awaiting Frank's visual review**.

This pass returns to the original successful Keeper authoring method. The exact
accepted Keeper pose authorities were extracted as a nine-model reference pack:
the six reviewer ghosts plus the three additional standard contract endpoints.
Each model has an exact full-colour raster and a separately extracted perimeter
outline under `models/` and `outlines/`. The source paths, frame indices and
SHA-256 values are recorded in `evidence/validation.json`.

The artist-smock source is one coherent full-character render made with the
built-in image generator in referenced-image identity-preserve mode. Its three
inputs were the V10 canon model pack, the approved high-resolution Keeper
turnaround and the approved high-resolution walk family. The old smock was not
used as a costume target. `PROMPT.txt` is the exact successful prompt and
`generated/artist-smock-fresh-source.png` is the untouched generated result.

The new costume is an independently designed warm-ivory painter's coat with a
navy V binding and cuffs, two low patch pockets, a mid-thigh hem and a small
repeatable palette of crisp vermillion, ochre, teal and green paint marks. This
is a proposed costume language only; it is not accepted or canonical.

`normalize_and_present.py` isolates the source through its native alpha, takes
the alpha>=32 foreground bounds, and applies one uniform 0.1155624037 scale.
The 556×1298 source foreground becomes 64×150 without independent width/height,
head, beard, costume or limb changes, then sits at `[32,8]` on the 128×160
density-4 canvas with its sole baseline at y=158. Alpha is hardened after the
single resize. The result has binary alpha, zero opaque border pixels, and a
deterministic byte-identical rerun.

Review files:

- `evidence/canon-model-pack.png` — all nine accepted model authorities with
  their extracted outlines;
- `evidence/artist-smock-source-view.png` — the coherent high-resolution source;
- `evidence/artist-smock-native-comparison.png` — existing smock, V10 draft and
  canonical Keeper at nearest-neighbour enlargement and exact native scale;
- `drafts/artist-smock-first-frame-normalized.png` — exact normalized raster.

No animation sequence, second costume, production source, raw strip, manifest,
reviewer registration or deployment was created or changed. Nothing is
committed, pushed, promoted or described as accepted.

Reproduction order:

```sh
/Users/frank/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 \
  art/drafts/keeper-canon-model-pack-artist-smock-2026-10-11-v10/build_canon_model_pack.py

# Run PROMPT.txt once with the three recorded reference inputs in the built-in
# image generator, preserving the returned source as the recorded generated file.

/Users/frank/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 \
  art/drafts/keeper-canon-model-pack-artist-smock-2026-10-11-v10/normalize_and_present.py
```
