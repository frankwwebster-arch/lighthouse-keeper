# Complete V10 artist-smock animation family — V11 draft

Status: **accepted family design; seven authored animations registered as
reversible review drafts, production unchanged**.

Frank accepted the V10 smock design and asked for it to be applied to every
animation in which the Keeper wears that outfit. The manifest contains fifteen
artist-smock entries. Seven are authored clips and eight are deterministic
neutral/bridge derivatives. V11 redraws all seven authored clips and builds all
eight derivatives without changing production:

- `keeper_artist_smock_walk` — 8 frames;
- `keeper_artist_smock_turn_back` — 6 frames;
- `keeper_artist_smock_turn_front` — 6 frames;
- `keeper_artist_smock_sit_front` — 6 frames;
- `keeper_paint_side` — 8 frames;
- `keeper_paint_back` — 8 frames;
- `keeper_pottery_front` — 8 frames.

The built-in image generator ran once per selected source sheet in referenced-
image identity-preserve mode. Each request used the accepted V10 full-character
source as costume authority, the nearest V10 family sheet as continuity
authority, and the matching canonical/action source as pose authority. The
exact selected prompts are preserved individually under `prompts/`; the exact
input and output SHA-256 values are recorded per clip in
`evidence/validation.json`.

The first one-row painting attempts were rejected because long brushes crossed
the implied frame boundaries. They remain unchanged under
`generated/rejected-overlap/`. The selected painting sources use isolated 4×2
grids. Validation requires a fully transparent seven-pixel band around every
grid boundary before extraction; no crop hides neighbouring-frame overlap.

`normalize_family.py` extracts the isolated source poses, calculates one shared
uniform scale per source sheet from its first pose and matching action
reference, and applies that same scale to every pose. It does not resize heads,
beards, costumes or limbs independently. Alpha is hardened after scaling.
Every draft frame has binary alpha and zero opaque edge pixels. Painting uses
expanded 40×48 logical canvases so raised brushes add transparent space rather
than shrinking the Keeper; all other clip sizes remain proportional to their
existing contract canvases.

Frank identified a pre-existing front seam mismatch and selected the first
frame of `keeper_artist_smock_sit_front` as the authority. V11 therefore reuses
that complete normalized raster as the final frame of
`keeper_artist_smock_turn_front` and as the standing-front neutral. The two
animation frames have zero differing RGBA pixels. Likewise, both turn starts
reuse the complete walk-neutral raster, avoiding side-view seam jumps. No head,
face or costume transplant is involved; each seam reuses a complete frame.

Review evidence:

- `evidence/artist-smock-family-overview.png` — all seven normalized sheets;
- `evidence/front-transition-seam-proof.png` — exact requested front seam;
- `evidence/*-comparison.gif` — existing animation on the left and V11 draft on
  the right, at the same logical pixel scale;
- `evidence/*-preview.gif` — V11 draft alone;
- `evidence/validation.json` — hashes, prompts, inputs, scales, canvas geometry,
  frame hashes, alpha/gutter results and scope gate.

The five neutral stills and three walk start/stop/cycle strips are present under
`drafts/` and derive only from the seven reviewed authored clips. They are
technical neutral/bridge assets and do not appear as separate rows in the
173-animation reviewer. `register_for_review.py` registers the seven exact
artist animation rows with the label `V11 consistent artist set`, while
preserving every canonical source, raw strip, runtime sprite and manifest
entry. Nothing is promoted to production.

Reproduce the deterministic stage with:

```sh
/Users/frank/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 \
  art/drafts/keeper-artist-smock-family-redraw-2026-10-11-v11/normalize_family.py
```
