# Side-on Keeper beard and hand-occlusion audit

## When to run this

Run this **first**, before `KEEPER_SPRITE_FRAME_ISOLATION_AUDIT.md`. It is a
separate identity and layer-order audit; do not combine it with frame-spacing
work.

## Recommended model

Use **GPT-5.6 Luna, High reasoning**. This is a bounded, repetitive visual
consistency audit, so Luna High is sufficient and avoids spending Sol-level
capacity on routine frame-by-frame inspection. Escalate only a genuinely
inseparable raster reconstruction to a stronger model if needed.

## Ready-to-paste prompt

```text
Continue the Lighthouse Keeper work in:

/Users/frank/Documents/ChatGPT/Lighthouse Keeper

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

The defect to look for is an occlusion-order error: in the darts example, the
Keeper's beard overlaps a hand that is physically in front of it. The correct
beard is the fuller, stepped side-on Keeper beard from the accepted shovelling-
snow animation (`keeper_clear_snow`). Treat that beard silhouette, colour,
edge treatment, and identity as authoritative. Preserve the beard itself; do
not shorten, smooth, recolour, or redesign it. The correction is the layer
order at the crossing: a foreground hand/fingers/wrist must render over the
beard, while a genuinely rear hand remains behind it. The beard must never
cover foreground fingers, erase a wrist, or create a pale beard-coloured halo
around the hand.

Start with a complete exact-name inventory and a defect/delta list. For every
side-on standing or sitting sheet, record whether the head/beard/neck and each
arm/hand have the correct physical occlusion in every frame. Never join a
comment, frame, or response by list position, filtered position, or display
order. Frank's saved dimensions, frame count, timing, identity, beard
silhouette, anatomy, interaction contacts, held-prop contacts, and cupboard-
occlusion contract remain authoritative.

Apply fixes in this order:

1. Prefer deterministic recomposition from canonical head/beard, torso, arm,
   and hand components or masks. Change only the affected occlusion pixels;
   do not redraw a whole animation when the correct parts already exist.
2. If a raster sheet has inseparable pixels, isolate the affected pose(s) and
   rerender only those pose(s), using `keeper_clear_snow` for the beard/head
   identity reference and `keeper_walk` for the standard side-on body
   reference. Keep every other pose, prop, contact point, dimension, timing,
   and transparent frame gutter unchanged.
3. Repack deterministically into the existing declared cells. Never solve an
   occlusion mistake by cropping tighter, moving the Keeper, changing saved
   width/height, or hiding the hand behind the beard.

Inspect the FINAL production strip for every corrected animation at 1x and a
zoomed view. Check all frames, including the first/last frame and any hand
crossing, held-object handoff, sit/stand transition, and mirrored output. The
hand must be visibly in front exactly when its pose requires it; the beard
edge must remain clean and anatomically continuous everywhere else. Confirm
that no neighbour-frame pixels, detached props, or transparent halos were
introduced.

Extend the permanent verifier with a side-on occlusion audit register. It
must identify every audited exact animation name, preserve the canonical beard
reference hash, record corrected frame numbers and layer-order decisions, and
fail future changes when a declared foreground hand is covered by beard pixels
or when a corrected side-on sheet loses its transparent frame gutters. Keep
responses read-only and specific to the exact animation name.

After the delta is stable, regenerate only affected raw sheets, production
strips, previews, contact sheets, scale evidence, and review artifacts. Run
the keeper verifier and scale/identity audit once, then tests, typecheck,
production build, and documentation audit. Commit and push directly to remote
main, wait for Vercel success, and verify the canonical live URL returns HTTP
200.

Report only: side-on sheets audited; sheets changed; exact frames with
occlusion corrections; any comments qualified rather than implemented;
verification results; commit and deployment status.
```
