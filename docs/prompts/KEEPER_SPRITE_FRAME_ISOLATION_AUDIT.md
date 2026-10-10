# Keeper sprite-frame isolation audit

## Recommended model

Use **GPT-5.6 Sol with High reasoning**. This audit combines exhaustive file
inventory, image inspection, deterministic extraction work, verifier design,
and cautious art repair. High reasoning is the best balance; use X-High only if
the first pass finds ambiguous overlapping artwork that needs extensive visual
reconstruction.

## Ready-to-paste prompt

```text
Continue the Lighthouse Keeper work in:

/Users/frank/Documents/ChatGPT/Lighthouse Keeper

Work from the current remote main branch. Read these first:

1. .cursor/rules/sprite-sheet-frame-isolation.mdc
2. docs/KEEPER_ANIMATION_HANDOFF.md
3. docs/review/KEEPER_ANIMATION_SECOND_ROUND_DELTA_2026-10-10.md
4. docs/review/KEEPER_ANIMATION_REVIEW_RESOLUTION_2026-10-10.md

Audit EVERY sprite sheet in the repository, not just the keeper review subset,
and make frame isolation a permanent build invariant. A frame is isolated only
when its character, clothing, held objects, detached props, particles, shadows,
and projectiles are wholly inside its declared cell and a transparent safety
gutter separates opaque pixels from every edge shared with another frame.

Start by inventorying every sheet from the source sidecars, raw assets,
production manifest, and generated outputs. Record exact sheet name, path,
frame count, declared cell dimensions, and whether each shared edge is clean.
Do not associate anything by list position or display order. Produce the full
audit/delta before changing artwork.

Then fix every sheet with overlap, cross-frame contamination, an opaque shared
edge, or ambiguous source-component ownership. Do not regenerate clean sheets.
Prefer deterministic extraction, component assignment, padding, or packing
when the intended pixels already exist. If source poses genuinely overlap,
rerender only the affected artwork as isolated poses. Preserve the keeper's
identity, beard silhouette, anatomy, costume, scale, saved width and height,
timing, interaction contacts, detached-prop ownership, neutral endpoints, and
cupboard-occlusion contract. Saved review dimensions are authoritative; never
replace them with automatic measurements.

Inspect every repaired FINAL production strip frame by frame. In particular,
verify that detached projectiles or tools remain entirely with their intended
frame and that a later frame cannot inherit pixels from its neighbour. Do not
claim success because a source image or intermediate file was generated.

Extend the permanent verifier so all current and future multi-frame sheets fail
if alpha touches a shared cell edge, a crop crosses opaque pixels, metadata and
actual strip geometry disagree, or a source component can be assigned to more
than one frame. Keep exact-name provenance from source through raw output,
manifest, previews, and review artifacts. Generate a concise machine-readable
audit register and human summary.

After the work is stable, regenerate only affected assets and dependent review
artifacts. Run the sprite verifier, keeper scale/identity audit, tests,
typecheck, and production build once. Complete the documentation audit, commit
and push directly to remote main, wait for Vercel success, and verify the
canonical live URL returns HTTP 200.

Report only: sheets inspected; sheets changed; any artwork rerendered rather
than deterministically repaired; verifier/test results; commit and deployment.
```

