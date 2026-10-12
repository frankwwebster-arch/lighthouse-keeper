# Keeper Prime Master V1

Status: **draft, awaiting Frank's visual approval; zero animations are Final**.

This reversible pack replaces the coarse Frame 6 raster as a rendering source
without discarding its identity role. Frame 6 remains the authority for pose,
face identity, head position and endpoint intent; V11 remains the smooth-finish
reference. The proposed master is Frank's preferred first smooth render, using
one broad pale chest-and-sleeve band instead of the legacy double stripe.

The proposed cell is 256 × 320 source pixels for a 32 × 40 logical cell at
density 8. Its floor anchor remains `[16, 40]`. The source is normalized
deterministically into a transparent safety gutter. Exact facial, beard,
moustache, mouth, head and band guides, hashes, comparison evidence and rejected
generation provenance are recorded in `master-pack-register.json`.

Review online at `/keeper-review/keeper-prime-master-v1/`. No animation work
should begin until this master receives explicit approval. On approval, every
direction, walk, stop, turn, sit and action is to be redrawn from this one
smooth family; old V1/V2 transition strips remain comparison provenance only.

Rebuild and verify:

```sh
/Users/frank/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 scripts/build_keeper_prime_master_v1.py
node scripts/verify_keeper_prime_master_v1.ts
```

Rollback is deletion of this versioned pack and its matching public review
directory only. Raw art, runtime sprites, manifests and previous drafts remain
unchanged.
