# Keeper Fast Timing V1

Frank approved the saved **Fast walk to front turn** profile on 14 October
2026 with the exact instruction “approve fast timing v1”. The approved profile
is:

- walk: 10 fps;
- deceleration: 12 fps;
- neutral beat: 0 ms;
- turn: 16 fps;
- full-face endpoint hold: 625 ms.

The complete 32-frame review route therefore lasts approximately 2.996 seconds
instead of 4.000 seconds. Frame bytes, frame order, root motion and endpoint
contracts are unchanged.

This is a **transition timing authority**, not a universal animation-speed
setting. It applies to brisk walking, walk acceleration/deceleration, facing
turns and the short endpoint hold that makes a transition readable. Action
entry, action loops, action exit, comic reactions and prop choreography keep
their own timing. Those activities should be enjoyable to watch and may be
slower or use deliberate holds.

The earlier Timing Lab V1 catalogue and its 10 fps recommendation remain
immutable history. The V2 catalogue makes Fast Timing V1 the repository-backed
default while retaining personal device presets as non-authoritative
experiments. Nothing is promoted to Workbench Final or production.

`data/keeper_timing_policy.json` is the machine-readable project contract for
later runtime integration. It explicitly records that action timing does not
inherit the transition profile. Runtime integration remains false until the
approved Keeper Prime routes receive their separate Final and production
promotion.
