# Kitchen V27 broken-state animation draft

Date: 18 October 2026
Status: rejected visual/timing provenance; unpromoted/unwired
Review: `/keeper-review/kitchen-broken-loops-v27/`

Rejection recorded 18 October 2026: the loops are too short and fast, and the
independently constructed broken art does not match the approved kitchen asset
family closely enough. V27 remains immutable evidence only. Replacement work
starts one object at a time with the coordinated static state-family method in
V28; no V27 art or timing is authoritative for that work.

V27 preserves Kitchen V20–V26 and supplies eight looping, density-4 repair
states at eight frames and 8 fps: overflowing bin, hinge-failed fridge,
overpressure kettle, burning toaster, smoking/flaming oven, smashed mixing
bowl, burst/cracked basin and a tilted table whose failed leg remains partly
attached. The V25 narrow-bin proportion remains binding.

Structural damage is stored separately from seven reusable effect strips:
smell/flies, dark smoke, light smoke, steam, flame, water jet and electrical
sparks. Smoke and sparks reuse the established TV effect drawings from the
floor-asset catalogue. The oven composites two flame instances on its hob as
well as black smoke. Each object strip has named `sfxCues`; because finished
sound files do not yet exist, the review page exposes deterministic Web Audio
placeholder previews and the names are ready for the sound library.

The seated scale proof is also corrected. Prime remains on the V26 seat/floor
registration, but the chair's player-facing posts, rails and seat foreground
are restored after the character layer. The chair is physically behind Prime's
back while correctly occluding his lower back from the player's viewpoint; the
table remains behind both.

Every isolated strip frame has a transparent safety gutter, exact metadata
geometry and a deterministic verifier. Generated source hashes, the rejected
fully snapped table-leg draft, the revised partly attached-leg source, effect
placements and rollback boundary are recorded under
`art/source/kitchen-broken-loops-2026-10-18-v27/` and
`art/drafts/kitchen-broken-loops-2026-10-18-v27/`. No runtime manifest, Final
art or canonical Kitchen/Prime source is changed.

## Verification and documentation audit

- Rebuild: use the bundled Python runtime with
  `scripts/build_kitchen_broken_loops_v27.py`, then run
  `npm run archive:keeper-review`.
- Focused verification: `npm run verify:kitchen-broken-loops-v27` and
  `npm run verify:review-archive`.
- Full verification: `npm test` and `npm run build`.
- The review preloads and decodes all strips before playback or SFX controls
  unlock. Local review before pushing requires regenerated public media because
  archived production URLs point to the remote `main` object store.
- Documentation audit completed on 18 October 2026 against the builder,
  catalogue, archive route, current review status, runtime boundary and manual
  `[deploy]` workflow. README, STATUS and DECISIONS now agree that V27 is
  rejected provenance, V28 is its one-item-at-a-time successor, and V20–V26
  remain immutable.
