# Keeper sprite-frame isolation audit

## Recommended model

Use **GPT-5.6 Terra with High reasoning**. This audit combines exhaustive file
inventory, image inspection, deterministic extraction work, verifier design,
and cautious art repair. Terra High is the agreed balance for this full-library
audit; do not use a lower-reasoning model.

## Ready-to-paste prompt

```text
This is the SECOND audit in the project sequence. First confirm that the
side-on beard/hand-occlusion audit in
`docs/prompts/KEEPER_SIDE_ON_BEARD_OCCLUSION_AUDIT.md` has completed, passed
its verifier, and is present on remote main. If it has not, stop and report
that prerequisite.

Continue the Lighthouse Keeper work in:

/Users/frank/Documents/ChatGPT/Lighthouse Keeper

Work from the current remote main branch. Read these first:

1. .cursor/rules/sprite-sheet-frame-isolation.mdc
2. docs/KEEPER_ANIMATION_HANDOFF.md
3. docs/review/KEEPER_ANIMATION_SECOND_ROUND_DELTA_2026-10-10.md
4. docs/review/KEEPER_ANIMATION_REVIEW_RESOLUTION_2026-10-10.md
5. docs/prompts/KEEPER_SIDE_ON_BEARD_OCCLUSION_AUDIT.md

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

Do not alter, replace, or obscure any beard/hand correction or v2 beard-audit
draft created by the completed first audit. Preserve its exact frame-level
identity and occlusion decisions; this second audit addresses only packing,
separation, crop and component ownership.

Then fix every sheet with overlap, cross-frame contamination, an opaque shared
edge, or ambiguous source-component ownership. Do not regenerate clean sheets.
Prefer deterministic extraction, component assignment, padding, or packing
when the intended pixels already exist. If source poses genuinely overlap,
rerender only the affected artwork as isolated poses. Preserve the keeper's
identity, beard silhouette, anatomy, costume, scale, saved width and height,
timing, interaction contacts, detached-prop ownership, neutral endpoints, and
cupboard-occlusion contract. Saved review dimensions are authoritative; never
replace them with automatic measurements.

Draft-first amendment contract (mandatory): copy each affected canonical
source and sidecar into a versioned `art/drafts/<audit-id>/` directory before
editing. Never overwrite `art/raw/`, `public/sprites/`, the runtime manifest,
immutable review exports, or existing previews. Record original and draft
SHA-256 values, keep draft outputs outside the runtime manifest, and expose
canonical and draft variants side-by-side in the existing review tool under
the exact animation name. Stop for Frank's explicit approval. Rejection must
require only discarding the draft; untouched canonical files are the rollback
point.

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

After the work is stable, generate only affected draft assets and dependent
draft review artifacts. Keep canonical and draft variants visible side-by-side
in the existing review tool. Run the verifier against draft outputs where
possible, the keeper scale/identity audit, tests, typecheck, and production
build once. Do not promote or overwrite canonical assets. Commit and push only
the draft-only audit, verifier, evidence and comparison-reviewer changes so
Frank can inspect them online; wait for deployment success and verify the
review URL returns HTTP 200. Stop for Frank's explicit approval; promotion and
final production delivery happen later.

Report only: sheets inspected; sheets changed; any artwork rerendered rather
than deterministically repaired; verifier/test results; commit and deployment.
```
