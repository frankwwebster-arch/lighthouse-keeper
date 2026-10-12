# Keeper Prime orthographic views V2

Status: **draft; exact-silhouette back awaits Frank's visual approval**.

V2 answers Frank's request that the approved front and proposed 180° back match
absolutely in the ghost overlay. The back's complete 256 × 320 alpha channel is
copied from the permanently approved Prime Master front after the generated rear
detail is normalized and row-fitted. All 81,920 alpha values therefore match
pixel for pixel: outer contour, transparent gaps, cap top, floor contact,
centreline and every row width are identical.

The 90° side is carried forward byte-identically from V1. V1 remains immutable
historical provenance and its former back is shown online as the superseded
comparison. V2 preserves the full cream rear hair, one broad pale jumper band,
rear-facing anatomy and smooth Prime rendering family.

Review online at `/keeper-review/keeper-prime-orthographic-v2/`. Approval will
establish neutral authoring endpoints only. No raw/runtime sprite, manifest or
animation lane has changed.

Rebuild and verify:

```sh
/Users/frank/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 scripts/build_keeper_prime_orthographic_views_v2.py
node scripts/verify_keeper_prime_orthographic_views_v2.ts
```

Rollback: delete only this V2 pack and its matching public review directory.
The permanent Prime Master, V1 draft and production remain unchanged.
