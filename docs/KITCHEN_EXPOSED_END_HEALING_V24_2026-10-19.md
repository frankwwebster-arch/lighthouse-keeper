# Kitchen Exposed End Healing V24 — 19 October 2026

## Purpose

V23 proved imprecise drag with exact 84-pixel bay snapping, deterministic Prime midpoint anchors and an exact V22 repair whenever the sink touches the fixed two-bay cabinet run. It left one visual case unresolved: the V19 sink's join-shaped left worktop contour remained visible when no cabinet occupied the bay to its left.

V24 preserves the complete V23 placement contract and adds an automatic exposed-edge state.

## Surface-state rule

After every exact grid commit, the compositor classifies each relevant edge from snapped occupancy:

- exact adjacent neighbour: apply the approved V22 body backfill and countertop join cap;
- no exact adjacent neighbour: apply a finished exposed-end overlay;
- during free drag: preview the surface state of the nearest legal destination, but persist nothing until release.

The sink's left exposed-end overlay is not newly rendered artwork. It reuses the exact leftmost `12 × 82` pixels of approved `cabinet-run-v11-exact.png`, registered at `body origin − 4 px` on both axes. This supplies the established rounded teal worktop lip and blue cabinet side. The overlay disappears automatically when the sink snaps immediately to the right of the cabinet run, where V22 takes authority instead.

The sink's existing right side is already a finished exposed end and does not need another overlay.

## Preserved geometry

- bay origins: `84, 168, 252, 336, 420, 504`;
- one-bay width: `84 px`;
- occupied fixed-run bays: `168, 252`;
- legal sink origins: `84, 336, 420, 504`;
- Prime target: exact snapped body midpoint at `y = 218`;
- source sink, cabinet, room and V22 repair assets: byte-identical.

The review defaults to exposed bay 5 (`x = 420`, midpoint `x = 462`) so the new repair is immediately visible. A review-only control can compare the raw and healed edge. Normal behaviour always enables healing.

## Boundary

V24 is reversible, unapproved and unpromoted. It adds review-compositor behaviour only. Approved V22 pixels, the V23 placement proof, Final art and runtime remain unchanged.
