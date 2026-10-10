# Side-on Keeper beard and hand-occlusion audit

## When to run this

Run this **first**, before `KEEPER_SPRITE_FRAME_ISOLATION_AUDIT.md`. It is a
separate identity and layer-order audit; do not combine it with frame-spacing
work.

## Recommended model

Use **GPT-5.6 Terra, High reasoning**. This run is no longer a narrow occlusion
spot-check: it must classify every frame in the manifest, compare every true
side-on pose with one exact beard reference, distinguish deterministic edits
from pose-specific rerenders, and preserve reversible draft provenance across
the reviewer and verifier. Terra High is the agreed higher-capability model
for that cross-library visual and implementation judgement. Do not use a
lower-reasoning model for this audit.

## Ready-to-paste prompt

```text
Continue the Lighthouse Keeper work in:

/Users/frank/Documents/ChatGPT/Lighthouse Keeper

Work on the current remote `main` and confirm the worktree is clean before
starting. Verify that historical rollback commit
`240c7613fa0d71b8288acc56b939655ee4e4d3a9` is an ancestor; do not reset back
to it. The failed second-round art pass and the rejected v1 beard/hand draft
are historical evidence only; neither is a valid source for new artwork. Keep
the ten later user-selected canonical promotions intact, including current
`keeper_clear_snow`; their previous versions are reviewer evidence, not sources
to restore.
The separate `keeper-darts-user-selected-2026-10-10-v1` review draft is a new
explicit selection by Frank and must be included in the visual audit, but it
is not canonical and must not be overwritten or silently promoted. If it
needs a beard/occlusion correction, copy that selected draft into the new
audit-v2 working directory and record both sets of hashes.

This is the FIRST audit in a two-audit sequence. Complete and commit this
side-on beard/hand-occlusion audit before starting the later exhaustive
sprite-frame isolation audit. Do not mix the two audits.

Read these before changing anything:

1. .cursor/rules/sprite-sheet-frame-isolation.mdc
2. docs/KEEPER_ANIMATION_HANDOFF.md
3. docs/review/KEEPER_ANIMATION_REVIEW_RESOLUTION_2026-10-10.md
4. art/source/keeper-first-batch/README.md

Audit ALL side-on Keeper animations whose actor is standing or sitting. Use
the source sidecars and manifest to find every right-facing, left-facing,
front-right/front-left, and rear-right/rear-left side-action clip, including
standard, winter, pyjama, artist-smock, mechanic, scuba, costume, seated,
mirrored, and derived runtime variants. Do not audit only the review subset.
Inspect the named source clip and its final production strip; inspect the
mirror/derived output as a consumer, but do not duplicate a source correction
for a deterministic mirror.

The primary defect to look for is the wrong side-on beard being used. The
accepted shovelling-snow animation (`keeper_clear_snow`) contains the
authoritative fuller, stepped side-on Keeper beard. Treat its silhouette,
length, stepped lower edge, colour, edge treatment, and identity as the
canonical beard format. Pin the restored canonical files before inspecting any
draft:

- `art/raw/keeper-first-batch/keeper_clear_snow_f8.png` SHA-256
  `fd866ef8f433211946b596c27cd1941dfdcc0bf40e0efb8555cb87c375a39d96`
- `art/source/keeper-first-batch/keeper-clear-snow-round2-grid-generated-source.png`
  SHA-256
  `b5470890cef0448794414393947e50eb55971884d59cb389a8947bdbbf5dc455`

If either hash differs, stop and report the mismatch; do not silently choose a
different reference. This is not an optional reference or a single-clip fix:
compare that beard against EVERY sprite in the manifest. Whenever any frame
reaches a true 90-degree side view to the player—whether the actor is standing
or sitting, and whether the side view occurs briefly during a turn,
transition, interaction, mirror, or derived variant—the frame must use that
same fuller, stepped side-on beard. Audit every frame, not just the first or
representative frame, and record the exact animation name and frame numbers
where the beard is missing, shortened, rounded, front-facing, back-facing, or
otherwise inconsistent. Preserve the beard itself; do not shorten, smooth,
recolour, or redesign it. The correction is to reproduce the canonical beard
silhouette and its correct layer placement in each affected side-on frame.

Also check the related occlusion-order defect: in the darts example, the
Keeper's beard overlaps a hand that is physically in front of it. A foreground
hand/fingers/wrist must render over the beard, while a genuinely rear hand
remains behind it. The beard must never cover foreground fingers, erase a
wrist, or create a pale beard-coloured halo around the hand.

Start with a complete exact-name inventory and a defect/delta list. For every
sprite in the manifest, classify every frame and transition as side-on,
front-facing, rear-facing, or indeterminate. For every side-on standing or
sitting frame, compare the beard directly with the canonical
`keeper_clear_snow` beard and record pass/fail, exact frame number, and the
reason. Then record whether the head/beard/neck and each arm/hand have the
correct physical occlusion. Never join a comment, frame, or response by list
position, filtered position, or display order. Frank's saved dimensions, frame
count, timing, identity, beard silhouette, anatomy, interaction contacts,
held-prop contacts, and cupboard-occlusion contract remain authoritative.

Draft-first amendment contract (mandatory): create a NEW versioned directory,
`art/drafts/keeper-side-on-beard-occlusion-2026-10-10-v2/`. Never reuse,
reactivate, amend, copy artwork from, or overwrite the rejected
`art/drafts/keeper-side-on-beard-occlusion-2026-10-10-v1/` directory. Before
changing any affected animation, copy its current canonical source and sidecar
from current `main` into the v2 working directory. Record the
canonical and draft SHA-256 values in a new v2 draft register. Apply fixes only
to the v2 working copy and write draft strips, previews, contact sheets, scale
evidence, and review evidence outside `art/raw/`, `public/sprites/`, the
runtime manifest, immutable review exports, and existing previews. Do not
create a draft for a clean animation. The existing review tool must show the
canonical and v2 draft variants together for direct comparison, with exact
animation-name labels and no replacement of the canonical preview. Every card
must state `Canonical` and `Draft v2`, show both hashes, and retain Frank's
existing exact-name review, dimensions, status, and complete comment. Stop
with a current-versus-draft comparison and request Frank's explicit promotion
decision; rejecting v2 must require only discarding its v2 draft directory,
leaving canonical files untouched as the automatic rollback point.

Apply fixes in this order:

1. Prefer deterministic recomposition from the canonical
   `keeper_clear_snow` head/beard component plus the existing torso, arm, and
   hand components or masks. Change only the affected beard and occlusion
   pixels; do not redraw a whole animation when the correct parts already
   exist.
2. If a raster sheet has inseparable pixels, isolate the affected pose(s) and
   rerender only those pose(s), using `keeper_clear_snow` for the beard/head
   identity reference and `keeper_walk` for the standard side-on body
   reference. Keep every other pose, prop, contact point, dimension, timing,
   and transparent frame gutter unchanged.
3. Repack deterministically into the existing declared cells. Never solve an
   occlusion mistake by cropping tighter, moving the Keeper, changing saved
   width/height, or hiding the hand behind the beard.

Inspect the FINAL draft production strip for every corrected animation at 1x
and a zoomed view. Check all frames, including the first/last frame, every
90-degree side-on moment, every turn and sit/stand transition, held-object
handoff, hand crossing, and mirrored/derived output. For each side-on frame,
the beard must visibly match the fuller, stepped `keeper_clear_snow` format;
the hand must be in front exactly when its pose requires it; and the beard
edge must remain clean and anatomically continuous everywhere else. Confirm
that no neighbour-frame pixels, detached props, or transparent halos were
introduced.

Extend the permanent verifier with a side-on occlusion audit register. It
must identify every audited exact animation name and frame, preserve the
canonical `keeper_clear_snow` beard reference hash, record side-on beard
classification and corrected frame numbers, and fail future changes when a
90-degree side-on frame does not match the canonical fuller stepped beard, a
declared foreground hand is covered by beard pixels, or a corrected side-on
sheet loses its transparent frame gutters. Keep responses read-only and
specific to the exact animation name.

After the delta is stable, generate only affected v2 draft sheets, draft
strips, previews, contact sheets, scale evidence, and draft review artifacts.
Extend the existing review tool so canonical and Draft v2 variants are visible
side-by-side for each exact animation name. Run the keeper verifier and
scale/identity audit against draft outputs where possible, then tests,
typecheck, and a production build without promoting drafts. Inspect the final
rendered v2 strips, not merely their source files.

Commit and push the draft-only audit, verifier, evidence, and review-tool
changes to remote `main`, allow Vercel to deploy the comparison reviewer, wait
for success, and verify the canonical live review URL returns HTTP 200. This
deployment is authorised only to expose reversible draft comparisons: do not
modify or promote canonical production assets. Stop with the online
canonical-versus-Draft-v2 comparison ready for Frank and request an explicit
promotion/rejection decision. Draft promotion remains a later task after
approval.

Report only: side-on sheets audited; sheets given a v2 draft; exact frames with
beard or occlusion corrections; any comments qualified rather than
implemented; verification results; final commit; comparison-reviewer
deployment status; confirmation that canonical assets remain byte-identical.
```
