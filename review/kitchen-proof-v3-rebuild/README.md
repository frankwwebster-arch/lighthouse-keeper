# Kitchen V3 rebuild

Status: **review-only candidate; awaiting Frank.** This folder does not alter
canon, runtime art or any previous immutable review set.

The package rebuilds the approved style calibration as 23 separate item/run
parts plus one room shell on the exact `1536 × 576`, 14-bay geometry. Authored high-resolution
sources are normalised into deterministic bay-sized sprites, assembled only in
code and checked against the 26 October rebuild brief.

## Review

Open `review.html`. The principal files are:

- `outputs/kitchen_v3_rebuild_room.png` — empty room at native 1:1;
- `outputs/calibration_vs_rebuild.png` — approved calibration and rebuild at
  the same display scale;
- `outputs/keeper_check_sheet.png` — exact Prime Keeper at fridge, sink and
  cooker;
- `outputs/contact_sheet.png` — every isolated part with its dimensions;
- `parts/item.json` and `parts/room.json` — asset and assembly contracts;
- `TECHNICAL_REPORT.md` — results, method and physical notes.

## Rebuild and verify

```sh
/Users/frank/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 review/kitchen-proof-v3-rebuild/build_review.py
/Users/frank/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 review/kitchen-proof-v3-rebuild/verify_review.py
```

Generated source illustrations are retained under `sources/generated/` with
hashes. Production parts are reproducible from those sources; no live image
generation is needed to rebuild the review package.

## Shadow boundary

The image generator's low-alpha exterior glow is not production art. During
normalisation, source alpha below 200 is discarded before fitting and any
low-alpha resampling ring below 16 is removed. Only deterministic edge
antialias remains. The verifier rejects partial-alpha pixels detached from a
hard silhouette. Room architecture is drawn without cast, wall, floor or
contact shadows.
