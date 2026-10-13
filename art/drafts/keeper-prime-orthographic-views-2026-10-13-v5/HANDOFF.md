# Keeper Prime orthographic views V5

Status: **rear boot design and integrated 180° rear endpoint approved for KP Rig
V1 authoring; not promoted to raw/runtime art**.

On 13 October 2026 Frank selected the first generated rear-boot treatment and
said: “They don't look like toe caps, they are excellent. Approved.” V5 copies
that exact source—SHA-256
`2371101e33fcd2b9b27cbfdbcecdc1587c41783d5773605117a4678b5ac3ecc6`—from
V4 rejected provenance into this pack. It is not regenerated.

The deterministic builder transfers only source y=273 through y=315 into the
registered rear endpoint. Rows 0–272 remain byte-identical to V2 and the entire
alpha channel remains byte-identical to the approved front. This locks total
height, outer silhouette, centreline, floor contact and transparent gutter.

The copied 1122 × 1402 source is the approved smooth artwork master. The 256 ×
320 orthographic image is its registered measurement/export proxy, created with
Lanczos resampling. Every outer alpha value—including the anti-aliased fringe—
matches the approved Prime front. Geometry passing is not sufficient: a rough
full-resolution edge, jagged internal line or nearest-neighbour master resize is
an approval blocker for this and every later Keeper model.

V4's more squared substitute is now historical provenance. The V3 side remains
blocked because it matches only 5 of 15 registered horizontal datums. V5
authorizes the approved front/back pair as input to KP Rig V1; the first
rig-derived art task is a zero-delta side endpoint.

Review online at `/keeper-review/keeper-prime-orthographic-v5/`.

Rebuild and verify:

```sh
/Users/frank/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 scripts/build_keeper_prime_orthographic_views_v5.py
node scripts/verify_keeper_prime_orthographic_views_v5.ts
```

Rollback: delete only this V5 pack and matching public review directory. V2–V4,
Prime Master, production sprites and manifests remain unchanged.
