# Keeper Prime orthographic registration V3

Status: **draft audit; selected side requires landmark redraft**.

V3 preserves V2 and production unchanged. It proves that the approved front,
selected V2 side and V2 exact-silhouette back already share the same 298-source-
pixel total height, cap top y=18 and floor y=316. It also makes the stronger
turn requirement visible: internal anatomy and clothing must share a hard
vertical skeleton.

The register covers cap top, badge centre, ear centre, shoulder apex, beard
base, arm-stripe top/centre/base, midriff-stripe top/centre/base, palm
centre/base, knee band and floor. A horizontal line is drawn from each approved
front datum to the selected side, with the measured delta shown. Only zero is a
pass. The selected V2 side therefore remains the preferred visual design but is
not transition-ready.

Two image-generation edits are retained under `rejected-sources/`. They still
missed hard datums after normalization and must not seed animation work.

Review online at `/keeper-review/keeper-prime-orthographic-v3/`. No animation,
raw/runtime sprite or manifest has been promoted.

Rebuild and verify:

```sh
/Users/frank/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 scripts/build_keeper_prime_orthographic_views_v3.py
node scripts/verify_keeper_prime_orthographic_views_v3.ts
```

Rollback: delete only this V3 pack and matching public review directory.
