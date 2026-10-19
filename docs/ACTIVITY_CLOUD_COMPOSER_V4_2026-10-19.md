# Activity Cloud Composer V4 — deterministic musical notation

**Status:** immutable, reversible review candidate built 19 October 2026; not
approved, promoted, deployed or connected to runtime recipes.

## Change from V3

V4 preserves Composer V3's 86 selectable components, Prime rear-work body,
complete route, default Garden BBQ recipe, timing and main element library. It
adds a separate six-symbol notation vocabulary:

- single quaver and beamed quavers;
- treble and bass clefs;
- sharp with note;
- rising three-note stave phrase.

Selecting any main component in the `music` family enables three notation
accents. They change on six-frame phrases during frames 4–36. A deterministic
FNV-1a seed made from the recipe key and ordered music selection chooses each
symbol, its small positional jitter and its rotation. The same recipe therefore
produces the same result on every replay and export.

The `Musical notation` checkbox controls the complete accent layer without
changing the four-or-five-element main package. Exported recipe JSON records
the switch, seed contract and exact SHA-256 of all six possible accents.

## Ownership and safety

- The generated 1536 × 1024 source is a strict 3 × 2 grid. Outer edges and all
  shared boundaries contain zero alpha above the ownership threshold.
- Every derived accent owns one isolated 256 × 256 cell with at least a
  16-pixel transparent gutter.
- Notation is not baked into instruments, performers, albums, the Keeper,
  household assets or SFX.
- Composer V1–V3, runtime, Final, Workbench and Kitchen remain unchanged.
- Rejection consists of discarding the V4 draft, public shell, set manifest and
  its six content-addressed objects.

## Files and verification

- Review tool: `public/keeper-review/activity-cloud-composer-v4/index.html`
- Draft/source: `art/drafts/activity-cloud-composer-2026-10-19-v4/`
- Builder: `scripts/build_activity_cloud_composer_v4.py`
- Verifier: `scripts/verify_activity_cloud_composer_v4.mjs`

Run:

```sh
npm run verify:activity-cloud-composer-v4
```

The verifier rejects inherited component, Prime body, route, recipe or timing
changes. It also checks fixed source-cell ownership, transparent gutters,
hashes, archive mappings, deterministic notation hooks, preload/decode and the
non-promotion boundary.
