# Keeper full-face canon pack — V1

Status: **approved by Frank on 12 October 2026 for small-batch authoring; no production art promoted**.

This reversible pack locks the selected full-face identity before animation-family work begins. Its standard standing neutral is byte-identical to the primary geometry authority `art/raw/keeper-first-batch/keeper_neutral_standing-front_f1.png` (SHA-256 `6d3b5057f7dad4410230c5c2a1959a2db468aca6f2d28486ec6db9e07827056a`). No image-generation call was used because a fresh interpretation would weaken the user's exact selected geometry. The V11 artist-smock neutral remains an unmodified, unpromoted rendering-quality comparison (SHA-256 `14c70ab69c9cb558d1a7b9b092425718a43269ea8fb2a20ad3d64638d30ea17a`).

The pack contains:

- the V1 standard neutral candidate and sidecar under `drafts/`;
- stored, hash-pinned copies of both selected references under `references/`;
- exact eye masks plus deterministic head, beard, moustache, mouth and nose guides under `masks/`;
- full-body, head-only and coloured landmark comparisons under `evidence/`;
- exact source/logical landmarks, hashes, geometry, alpha and safety-gutter results in `canon-pack-register.json`;
- the read-only 62-asset production/technical inventory in `docs/KEEPER_FULL_FACE_INVENTORY.md` and `data/keeper_full_face_inventory.json`;
- a versioned public comparison page at `/keeper-review/full-face-canon-v1/`.

The prior face-camera amendments are not review choices here. Twelve remain `withdrawn-by-user` rejected provenance, and the deleted `keeper_count_money` amendment was not recreated. No raw/runtime image, manifest entry, historical draft, immutable export or existing preview was overwritten.

Frank approved this pack with “Approve full-face canon pack V1. These are excellent.” The approval authorizes small, reversible animation-normalisation batches. It does not promote pixels or authorize a whole-inventory rewrite.

Rebuild:

```sh
/Users/frank/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3   scripts/build_keeper_full_face_canon.py
node scripts/verify_keeper_full_face_canon.ts
```

Rollback: delete this versioned draft and its versioned public comparison page, then remove the inventory files and reviewer link/test registration. Production remains untouched throughout.
