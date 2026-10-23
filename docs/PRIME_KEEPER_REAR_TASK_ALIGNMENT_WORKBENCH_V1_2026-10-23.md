# Prime Keeper rear-task manual alignment workbench V1

Date: 23 October 2026

Status: active manual fallback. V9 is rejected review evidence.

Route: `/prime-keeper-rear-task-alignment`

## Why this exists

V9 still shows the approved trousers' dark waistband below the moving blue
jumper hem in rear-task frames 11–31. Frank rejected it on 23 October 2026.
No further automatic waist composite should be presented for approval without
first reproducing his chosen join from this workbench.

The workbench exposes two exact source layers in a deliberately ordered
crop-first workflow:

- the immutable V6 moving action torso for the selected frame, cropped only at
  a user-controlled bottom row; and
- the hash-pinned approved rear trousers and boots authority, cropped only at
  a user-controlled top row.

The authority's waist-level hands are outside the verified lower-body ownership
bounds and are deliberately excluded. Rows 214–230 use x82–172; rows 231–319
use x70–186, matching the deterministic compositor's authority ownership.
Authority rows 214–218 contain the unwanted top trouser seam and are excluded
from the visible lower layer. The compositor repeats one exact clean interior
trouser-colour pixel from the same approved authority across the narrow waist
bridge, retaining a hidden four-pixel safety underlap before resuming the
unscaled approved pixels from row 219. This prevents a transparent hip tear if
the torso moves laterally without restoring the rejected top waistband seam.
Nothing is written back to source art.

## Controls and persistence

For every frame from 11 through 31 Frank first sees the moving torso alone.
The approved legs remain hidden and all alignment controls remain disabled
until he has cropped away the unwanted lower seam and explicitly confirmed the
jumper crop. Only then does the workbench reveal the legs for alignment.

Frank can:

- drag the yellow jumper-bottom crop line or change it one source pixel at a
  time before any leg pixels are visible;
- confirm each jumper crop independently, with a `C` marker in the frame rail;
- after confirmation, drag either retained torso or approved legs directly;
- nudge the selected layer by one authoring pixel with buttons or arrow keys;
- use Shift + arrow for an eight-pixel move;
- choose the torso bottom and legs top crop rows;
- inspect the waist at 4×;
- play or step across all 21 composites;
- mark frames aligned independently;
- copy a vertical join across the sequence without overwriting the verified
  per-frame horizontal registration;
- download any current 256×320 composite; and
- copy or download all settings as hash-addressed JSON.

Settings remain local to the browser under
`prime-keeper-rear-task-alignment:v1`. The exported JSON is the handback
authority for a later deterministic V10 build and uses schema
`lighthouse-keeper/prime-rear-task-manual-alignment@3`, including independent
`cropConfirmed` and `aligned` states plus the clean-trouser and minimum-underlap
contract. The storage key intentionally remains V1
so earlier unsaved placement work remains recoverable. The workbench itself
promotes nothing to the animation bank.

## Verification

```bash
node scripts/verify_keeper_prime_rear_task_alignment_workbench_v1.mjs
npm run typecheck
npm run build
```

The verifier pins the 21 source frames, lower-body authority hash, ownership
bounds, V9 horizontal starting registrations, crop-first gating, editing
controls, local-only persistence and export path. The page was also
browser-tested for source-image decoding, crop-only display, one-pixel crop
adjustment, explicit crop confirmation, seam-free trouser underlap, leg reveal
and state invalidation after a later crop change.
