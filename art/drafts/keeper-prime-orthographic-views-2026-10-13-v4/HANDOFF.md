# Keeper Prime orthographic views V4

Status: **draft; corrected rear-facing boots await visual approval**.

Frank identified that the V2 180° rear elevation incorrectly retained
front-facing feet. V4 preserves V2 as rejected provenance and changes only the
lower-leg/boot region from source y=273 through y=315. The proposed boots use
rear heel counters, vertical back seams and rear sole edges rather than rounded
front toe caps.

Rows 0–272 remain byte-identical to V2. The candidate's complete alpha channel
remains byte-identical to the permanently approved front, so total height,
outer contour, floor contact, centreline and transparent gutter are unchanged.
The selected side remains blocked by the V3 15-point vertical-landmark audit.

Review online at `/keeper-review/keeper-prime-orthographic-v4/`. Approval would
accept only the corrected back endpoint for later KP Rig construction. Nothing
is promoted into raw/runtime art or either animation lane.

Rebuild and verify:

```sh
/Users/frank/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 scripts/build_keeper_prime_orthographic_views_v4.py
node scripts/verify_keeper_prime_orthographic_views_v4.ts
```

Rollback: delete only this V4 pack and matching public review directory.
