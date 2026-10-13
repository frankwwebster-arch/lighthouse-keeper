# Keeper Prime side-right ↔ back Turn V8 handoff

Status: **new reversible candidate awaiting Frank's visual approval**.

V8 tests a denser authored cadence. It retains all eight V7 pose PNGs
byte-for-byte at F1, F3, F5, F7, F9, F11, F13 and F16, then inserts eight new
smooth 1122 × 1402 drawings between them. Playback changes from 8 poses at
8 fps to 16 poses at 16 fps, so the side-to-back turn still lasts exactly one
second.

The deliberate rear occlusion sequence is:

- F13 / 165°: far-left ear hidden;
- F14 / 170°: narrow far-left ear sliver;
- F15 / 175°: partial far-left ear;
- F16 / 180°: complete rear-view ear.

The verifier pins the source and draft hashes, exact V7 frame retention,
transparent gutters, common floor, bounded adjacent height/centroid movement,
component palette registration, disjoint trouser/boot masks, ear progression,
forward/reverse strip order, sidecars and public assets.

Review at `/keeper-review/keeper-prime-turn-side-back-v8/`. The page compares
V7 at 8 fps with V8 at 16 fps over the same duration, and includes large,
128 × 160 game-scale, step-frame and rear-ear evidence views.

No prior draft, approved endpoint, Final item, runtime sprite or manifest was
changed. Rejecting V8 requires deleting only this directory and
`public/keeper-review/keeper-prime-turn-side-back-v8/`.
