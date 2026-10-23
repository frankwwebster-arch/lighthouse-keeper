# Prime Keeper rear-task manual alignment workbench V1

Date: 23 October 2026

Status: superseded lower-seam experiment, retained as reversible comparison
evidence. The active correction is V2, which targets the upper jumper-band seam.

Route: `/prime-keeper-rear-task-alignment`

Active successor: `/prime-keeper-rear-task-alignment-v2`; see
`PRIME_KEEPER_REAR_TASK_UPPER_SEAM_WORKBENCH_V2_2026-10-23.md`.

## Why this exists

V9 still shows the approved trousers' dark waistband below the moving blue
jumper hem in rear-task frames 11–31. Frank rejected it on 23 October 2026.
No further automatic waist composite should be presented for approval without
first reproducing his chosen join from this workbench.

The workbench exposes two exact source layers in a deliberately ordered
crop-first workflow:

- the immutable V6 moving action torso for the selected frame, clipped at a
  user-controlled five-point jumper-bottom curve; and
- the hash-pinned approved rear trousers and boots authority, cropped only at
  a user-controlled top row.

The authority's waist-level hands are outside the verified lower-body ownership
bounds and are deliberately excluded. Rows 214–230 use x82–172; rows 231–319
use x70–186, matching the deterministic compositor's authority ownership.
Authority rows 214–218 contain the unwanted top trouser seam and are excluded
from the visible lower layer. The compositor continues clean approved rows
219–230 upward column-by-column across the narrow waist bridge, retaining their
real colour variation and shading instead of using a flat fill. The authority's
black outline columns x83 and x171 extend upward until they meet the moving
curved jumper hem. A hidden four-pixel safety underlap then prevents a
transparent hip tear if the torso moves laterally or vertically without
restoring the rejected top waistband seam. Nothing is written back to source
art.

## Controls and persistence

For every frame from 11 through 31 Frank first sees the moving torso alone.
The approved legs remain hidden and all alignment controls remain disabled
until he has cropped away the unwanted lower seam and explicitly confirmed the
jumper crop. Only then does the workbench reveal the legs for alignment.

Frank can:

- drag any of five jumper-bottom control points in the whole-frame view or the
  editable 4× waist inspection, or change the selected point one source pixel
  at a time before any leg pixels are visible;
- preserve the base as a shallow U rather than a flat cut, mirror either side
  for symmetry, and reset it to the measured default `[-4,-1,0,-1,-4]` curve;
- retain a true-black two-pixel outline along the complete extended hem;
- confirm each jumper crop independently, with a `C` marker in the frame rail;
- after confirmation, drag either retained torso or approved legs directly;
- nudge the selected layer by one authoring pixel with buttons or arrow keys;
- use Shift + arrow for an eight-pixel move;
- choose the torso bottom and legs top crop rows;
- compare opaque height, overall width, floor row and centre against the exact
  approved Prime rear authority at alpha threshold 128;
- show or hide that exact approved rear Prime as a canonical-position,
  canonical-scale translucent ghost over both the whole figure and 4× waist
  inspection, with opacity adjustable from 10% to 80%;
- play or step across all 21 composites;
- mark frames aligned independently;
- copy a vertical join across the sequence without overwriting the verified
  per-frame horizontal registration;
- download any current 256×320 composite; and
- copy or download all settings as hash-addressed JSON.

Settings remain local to the browser under
`prime-keeper-rear-task-alignment:v1`. The exported JSON is the handback
authority for a later deterministic V10 build and uses schema
`lighthouse-keeper/prime-rear-task-manual-alignment@4`, including the five hem
offsets, control x positions, black outline contract, independent
`cropConfirmed` and `aligned` states plus the clean-trouser and minimum-underlap
contract. The storage key intentionally remains V1
so earlier unsaved placement work remains recoverable. The workbench itself
promotes nothing to the animation bank.

The V6 archive set is delivered through the existing hash-verifying same-origin
proxy on this route. A versioned query suffix avoids any previously cached
off-origin redirect. This lets the browser read alpha bounds for the live
dimensional audit without altering, rescaling or repainting the images.

The Prime ghost is a separate pointer-transparent canvas layer. It is never
painted into the working composite, alpha-bounds audit, downloaded PNG or JSON
handback, so comparison remains reversible and cannot contaminate production
art.

## Imported frame 11 dimensional audit

Frank's exported `@3` settings from 23 October set frame 11 to `torsoCutY 205`,
`legsX +3`, `legsY -11` and `legsCropY 219`. Replaying those values against the
exact approved Prime rear authority at alpha threshold 128 gives:

- approved authority: x50–203, y18–314, 154 px wide × 297 px high, centre x126.5;
- frame 11 composite: x55–202, y18–303, 148 px wide × 286 px high, centre x128.5;
- lower-body centre x130, 3 px right of the approved lower-body centre x127.

It therefore fails the size check: the `legsY -11` placement raises the floor
from row 314 to 303 and makes the figure 11 px too short. The moving source pose
is also 6 px narrower than the standing Prime silhouette, independently of the
leg placement. These are now reported directly in the workbench rather than
left to visual estimation.

## Verification

```bash
node scripts/verify_keeper_prime_rear_task_alignment_workbench_v1.mjs
npm run typecheck
npm run build
```

The verifier pins the 21 source frames, lower-body authority hash, ownership
bounds, V9 horizontal starting registrations, five-point curve geometry,
shaded trouser extension, upward black side outlines, separate exact-authority
ghost layer, alpha-bounds audit, crop-first gating, editing controls, local-only
persistence and export path. The page is also browser-tested for
source-image decoding, crop-only display, one-pixel point adjustment, explicit
crop confirmation, seam-free trouser underlap, dimensional comparison, leg
reveal and state invalidation after a later crop change.
