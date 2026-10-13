# Keeper Prime side-right ↔ back Turn V9 handoff

Status: **new reversible candidate awaiting Frank's visual approval**.

V8's 16-frame strategy is rejected provenance because it was significantly
jerkier. V9 returns directly to V7 and changes only the cadence around the rear
endpoint: every V7 frame is retained byte-for-byte, with one new 172.5° pose
inserted between V7 F7 / 165° and V7 F8 / 180°.

The nine poses run at 9 fps, preserving the original one-second side-to-back
duration. The midpoint is 297 opaque pixels high on floor y=316, precisely
between the 296-pixel F7 and 298-pixel F8 endpoints. Its far-left ear is only
partly revealed; full bilateral rear ears remain exclusive to F9 / 180°.

Review at `/keeper-review/keeper-prime-turn-side-back-v9/`. The page compares
V7 at 8 fps and V9 at 9 fps over the same duration, with large, exact game-scale,
step-frame and isolated F7→F8→F9 views.

No prior draft, approved endpoint, Final item, runtime sprite or manifest was
changed. Rejecting V9 requires deleting only this directory and
`public/keeper-review/keeper-prime-turn-side-back-v9/`.
