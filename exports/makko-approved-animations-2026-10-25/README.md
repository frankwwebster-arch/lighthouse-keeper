# Lighthouse Keeper — approved animation export for Makko

This folder contains the complete approved **production sprite-sheet bank** for the Prime Keeper as reconciled on 22 October 2026. The files are copies; no canonical project artwork has been changed.

## Which files to use

- `sprite-sheets/production-4x/` — 27 runtime-ready transparent PNG strips. Start here for game integration.
- `sprite-sheets/source-8x/` — the same 27 strips at the higher canonical authoring scale. Use these as Makko visual references or for lossless resampling.
- `manifest.json` — cell size, frame count, FPS, looping, pose endpoints, approval provenance and SHA-256 hashes for every sheet.
- `metadata/approved-animation-catalogue.json` — all 14 approved playable animation records, with frame timing and sequencing.
- `metadata/complete-stair-route-v6.json` — the approved door-to-door stair choreography. This is a sequence assembled from the approved walk, turn and stair art, not an additional standalone runtime sheet.
- `CHECKSUMS.sha256` — integrity hashes for the full handoff.

## Geometry

All sprite sheets are horizontal, single-row PNG strips with transparent backgrounds and isolated frames.

- Standard logical cell: **32 × 40**
- Standard production cell at 4× density: **128 × 160 px**
- Standard source cell at 8× density: **256 × 320 px**
- Standard logical anchor: **[16, 40]**, bottom-centre
- Darts is the exception: **56 × 40 logical**, or **224 × 160 px** at production scale

Do not trim individual frames, repack cells, or remove transparent gutters. Use each manifest entry's `w`, `h`, `frames`, `fps`, `loop`, `startPose` and `endPose` values. Filenames ending in `_fN.png` identify the high-resolution strip's frame count.

## Approved animation coverage

1. Walk cycle
2. Stop → walk → stop
3. Front ↔ side turn
4. Side ↔ back turn
5. Stair ascent
6. Stair descent
7. Complete stair route choreography
8. Complete ladder route
9. Sit / stand — side right
10. Sit / stand — side left
11. Sit / stand — front
12. Sit / stand — back
13. Play darts
14. Rear work action

The held-implement upper-body override POC is intentionally absent because its proxy artwork is not production-approved.
