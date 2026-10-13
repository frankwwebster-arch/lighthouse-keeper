# Keeper Prime Construction Rig V1

Status: **draft construction contract awaiting Frank's visual approval**.

KP Rig V1 is the common posable measurement foundation for every later Keeper
direction, pose, outfit and animation. It is built from the permanently approved
Prime front and the approved smooth V5 rear. The historical V2 side remains
visible only as the preferred design reference and as evidence of the existing
5/15 landmark failure.

The rig fixes the 32 × 40 logical coordinate system, density-8 working cell,
vertical identity axis, floor anchor, 15 horizontal datums, joint positions,
mirrored segment lengths, body-volume envelopes, pose limits, contacts and
view-specific occlusion order. Front and back share one joint map. Side width is
a projection; it never authorizes a smaller or shorter Keeper.

The online page includes layered front/side/back overlays, an exact measurement
sheet and a live pose lab. The pose controls rotate registered segments while
preserving their lengths. This demonstrates the construction model only: final
beard, hair, clothing and anatomy must be redrawn around it at smooth master
resolution. Finished raster art must never be mechanically stretched.

No side candidate, animation, production sprite or runtime manifest changes in
this pack. Approval authorizes a separate smooth side-right draft targeting
15/15 exact y-datums.

Rebuild and verify:

```sh
/Users/frank/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 scripts/build_keeper_prime_rig_v1.py
node scripts/verify_keeper_prime_rig_v1.ts
```

Rollback: delete only this versioned rig pack and
`public/keeper-review/keeper-prime-rig-v1/`.
