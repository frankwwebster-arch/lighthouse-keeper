# Kitchen Sink Water Workbench V20 — 19 October 2026

## Purpose

V20 corrects the two separate sink-water animations without redrawing or
altering the sink. It also provides a focused placement workbench so Frank can
position and tune these reusable layers directly.

Review route:
`/keeper-review/kitchen-sink-water-workbench-v20/`

## Preserved authority

- `sink-cabinet-v19.png` is byte-identical to V19
  `sink-cabinet-standard.png`.
- `room-v19.png` is byte-identical to V19
  `cabinet-run-plus-sink-native-room.png`.
- The cabinet, worktop, basin and tap receive no new pixels.
- V19, V18, Final art and runtime remain unchanged.

## Revised animation layers

Both candidates are isolated RGBA strips with 40 frames, 4 fps canonical
playback and a ten-second loop. Each 120 × 144 px frame has a fully transparent
gutter on every edge.

### On — thin outlet flow

The existing animated water column is reduced from eight pixels to the exact
four-pixel outlet width. It begins immediately below the four-pixel outlet,
while the existing animated basin splash is retained at native scale.

- File: `fx-sink-on-thin-outlet-flow-f40.png`
- Named SFX placeholder: `kitchen_sink_water_gentle_loop`

### Broken — tall comic upward jets

The existing approved upward-water drawing and palette are retained. Its jet
section is extended vertically to rise approximately 37 native pixels above
the tap crown, while its basin splash remains at native scale.

- File: `fx-sink-broken-tall-comic-jets-f40.png`
- Named SFX placeholder: `kitchen_sink_pipe_burst_loop`

## Placement workbench

The workbench follows the asset-first interaction requested by Frank:

1. choose `Sink · On` or `Sink · Broken`;
2. add or remove that state's animation;
3. drag the cyan bounds to reposition the layer;
4. drag the cyan handle or enter dimensions to resize it;
5. crop any edge non-destructively;
6. set playback speed from 0.1× to 4×;
7. nudge with the arrow keys; and
8. copy or download the resulting placement JSON.

Placements persist locally in the browser. Editing affects only the review
composition; it never rewrites the source strip or sink sprite.

## Reversibility and verification

V20 is an unapproved, unpromoted draft under
`art/raw/kitchen-sink-water-workbench-2026-10-19-v20/` and
`art/drafts/kitchen-sink-water-workbench-2026-10-19-v20/`. Rejection requires
discarding only those versioned directories, the V20 review route and its V20
archive manifest.

`scripts/verify_kitchen_sink_water_workbench_v20.mjs` deterministically checks
the V19 source hashes, registered output hashes, strip dimensions, frame
isolation, transparent gutters, animation diversity, exact four-pixel ON
registration, BROKEN jet height, workbench controls and content-addressed
archive entries.
