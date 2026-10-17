# Kitchen V17 exact V5 rollback

**Date:** 17 October 2026  
**Status:** review-only reversible draft; not approved, promoted or wired  
**Review:** `/keeper-review/kitchen-v5-exact-rollback-v17/`

## Decision

Frank rejected Kitchen V16 because its replacement countertop read as a
double-layered worktop. Kitchen V17 therefore makes no new visual proposal. It
restores the complete Kitchen V5 review family byte-for-byte.

Kitchen V6 through V16 remain immutable rejected provenance. Option B is not a
geometry authority for V17 and none of its pixels, redraws, shelves, portholes,
room changes or later countertop repairs are carried forward. A future
perspective experiment must begin as a separate review gate and must not alter
this rollback.

## Exact-copy contract

- Copy the complete V5 raw tree without transforming or re-encoding a file.
- Copy all 153 V5 review images from their content-addressed archive objects.
- Preserve every V5 state, frame, timing record, cell, alpha bound, anchor,
  interaction spot, room piece and room composition.
- Change only the immutable review URL prefix from
  `/keeper-review/kitchen-basic-assets-v5/assets/` to
  `/keeper-review/kitchen-v5-exact-rollback-v17/assets/`.
- Preserve the V5 21-lp bay contract, 56-lp room height, 5-lp floor band,
  nine-bay 193-lp room and twelve-bay 256-lp room.
- Do not change Keeper animations, runtime registers, sprite manifests, Final
  assets or the live game.

The verifier compares the two complete raw trees by relative filename and
SHA-256, normalises only the review URL prefix before comparing metadata, and
requires every archived V17 image to resolve to the same content-addressed
object, byte count and SHA-256 as its V5 source.

## Authoritative inputs

- V5 measured hand-back:
  `docs/CODEX_TO_CLAUDE_KITCHEN_BASIC_ASSETS_V5_2026-10-16.md`
- V5 raw tree: `art/raw/kitchen-basic-assets-2026-10-16-v5/`
- V5 review metadata:
  `art/drafts/kitchen-basic-assets-2026-10-16-v5/review-data.json`
- V5 archive set: `review-archive/sets/kitchen-basic-assets-v5.json`
- V17 recipe: `data/kitchen_v5_exact_rollback_v17_recipe.json`
- V17 builder: `scripts/build_kitchen_v5_exact_rollback_v17.py`
- V17 verifier: `scripts/verify_kitchen_v5_exact_rollback_v17.mjs`

## Review-page gate

The V17 page shows all ten V5 asset families with every recorded state, both
V5 room compositions, and the stair cap, repeat section and far-wall closed and
open pieces. It preloads and decodes the V17 review media before enabling its
controls. The page is a rollback proof only; it grants no approval or runtime
authority.
