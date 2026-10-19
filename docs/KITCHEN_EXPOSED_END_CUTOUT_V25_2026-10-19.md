# Kitchen Exposed End Cutout V25 — 19 October 2026

## Correction

V24 selected the right exposed-end artwork but used it as a conventional overlay. The approved V11 end contains transparent pixels around its rounded outline, so the obsolete V19 sink join triangle remained visible through those transparent pixels.

V25 replaces rather than merely covers that portion of the movable sink:

1. draw the complete sink to an isolated transparent layer;
2. if and only if its left side is exposed, clear the exact `12 × 82` destination window occupied by the V11 end crop;
3. draw the exact V11 crop into that cleared window;
4. composite the finished isolated sink layer over the untouched room;
5. if the left side instead has an exact neighbour, skip the clear and V11 end overlay and use the complete sink with the approved V22 join.

Clearing occurs only on the isolated sink layer. It never cuts a hole in the room background or another asset. Because the clear window and overlay destination are identical, the transparent pixels around the rounded V11 contour now reveal the cream wall rather than obsolete sink pixels.

## Preserved contracts

- V23 exact 84-pixel grid snapping and Prime midpoint anchors;
- V22 joined-edge body and countertop repair;
- all five source assets byte-for-byte;
- complete sink geometry whenever a left neighbour is present;
- reversible review-only implementation with no Final/runtime promotion.

The V25 page defaults to exposed bay 5 with construction guides hidden and includes an 8× end focus plus an untreated/corrected comparison control.
