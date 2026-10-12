# Keeper Prime orthographic views V1

Status: **draft; 90° side and 180° back await Frank's visual approval**.

Prime Master V1 is permanently approved and hash-pinned. This pack derives two
new neutral views from it without altering the approved front, canonical raw
art, runtime sprites, manifests or prior drafts.

Both candidates use a 256 × 320 source cell for the 32 × 40 logical cell at
density 8, anchor `[16,40]`, cap top `y=18` and opaque floor `y=316`. The review
evidence includes a three-view orthographic lineup plus cyan ghost overlays of
the approved front over each proposal. Exact bounds, centres, hashes, sidecars,
transparent gutters and the rejected too-short rear-hair source are recorded in
`batch-register.json`.

The body-shape check is deterministic as well as visual. Twelve registered
landmark rows measure the silhouette. At those rows, the back may differ from
the approved front by at most four source pixels in width (half a logical pixel
at density 8) and by at most 0.5 source pixel in horizontal centre. The centre
check also runs across every occupied row. Both candidates must share the
approved `y=18` cap top and `y=316` floor contact. The side is expected to be
narrower because it describes body depth, but remains locked to the same axis,
cap and floor guides.

Review online at `/keeper-review/keeper-prime-orthographic-v1/`. Approval of
these two views will establish the endpoints used to draw side/front/back
rotations. It will not promote any runtime sprite or animation.

Rebuild and verify:

```sh
/Users/frank/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 scripts/build_keeper_prime_master_v1.py
/Users/frank/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 scripts/build_keeper_prime_orthographic_views_v1.py
node scripts/verify_keeper_prime_orthographic_views_v1.ts
```

Rollback: delete only this versioned pack and its matching public review
directory. The approved Prime Master and production remain unchanged.
