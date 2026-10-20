# Kitchen Modular Join Workbench V33

Date: 20 October 2026

Status: approved placement/join review authority; hash-pinned, unpromoted and
unwired.

Review page: `/keeper-review/kitchen-modular-join-workbench-v33/`

## Purpose

V33 puts the approved sink and oven join systems in one placement workbench.
The exact V11 two-bay cabinet run remains fixed in bays 2–3. The exact V25 sink
and V32 oven can be selected and moved independently into any two distinct free
bays, including immediately beside one another in either order.

No appliance or cabinet sprite is redrawn or amended. All repairs are separate
dynamic compositor layers.

Frank approved exact V33 on 20 October 2026 with “excellent. Approved.” The
catalogue, register, review shell and archive manifest are pinned by
`docs/review/kitchen-modular-join-workbench-v33-approval-2026-10-20.json`.
This releases the fridge as the next standalone appliance but does not promote
V33 into Final or runtime.

## Exact placement contract

- Canonical origins: `[84,168,252,336,420,504]`.
- Fixed cabinet origins: `[168,252]`.
- Sink and oven legal origins: `[84,336,420,504]`.
- The other movable appliance is excluded from the selected asset's legal
  destinations, so overlap cannot be committed.
- During drag, the pointer position is a translucent preview only.
- Release discards the raw pointer coordinate and commits the selected asset to
  the nearest legal unoccupied origin.
- Both appliance bodies are 84 pixels wide. Their Prime interaction anchors are
  therefore `committed x + 42`, at canonical y=218.

## Pair-aware join resolver

The renderer sorts the fixed cabinet, sink and oven by body origin, then
classifies every zero-gap adjacency independently:

1. **Any pair containing the oven** — draw the six-pixel V22 cabinet-blue body
   backfill and V30/V32 24 × 12 triangular underlay behind both assets. After
   the assets, draw only the six-pixel V32 cleanup mask over the non-oven end
   contour. The oven-facing diagonal remains intact. This applies to
   cabinet↔oven, sink↔oven and oven↔sink.
2. **Cabinet↔sink** — draw the approved V22 body backfill behind the assets and
   the 16 × 12 row-matched flat cap in front.
3. **Sink left side exposed** — compose the sink on an isolated layer, clear
   its exact local `[0,26,12,82]` replacement window, then draw the rounded V11
   end crop into that cleared window, exactly as approved in V25.
4. **Oven edge exposed** — draw no join and invent no countertop bridge.

The complete draw order is room background; active body fills and triangular
underlays; fixed cabinet and movable appliance layers; then V22 flat caps and
V32 narrow neighbour-side cleanup masks.

## Oven state controls

The workbench retains exact V32 Off, On and Broken sprites. Broken retains both
independently removable 40-frame, 4-fps, ten-second irregular fault layers and
0.1×–4× playback speed. Sink water and oven smoke remain separate reusable
effects and are intentionally outside this placement/healing gate.

## Verification

Run:

```sh
npm run verify:kitchen-modular-join-workbench-v33
npm run build
```

The verifier enumerates all 12 ordered, non-overlapping sink/oven placements;
checks exact grid origins and Prime midpoints; reconstructs both direct-adjacent
room proofs; checks pair-method selection, body-gap coverage, V25 exposed-sink
replacement bytes and oven transparent gutters; proves all source assets remain
byte-identical to V22/V25/V32; and validates the archive manifest and reversible
boundary.
