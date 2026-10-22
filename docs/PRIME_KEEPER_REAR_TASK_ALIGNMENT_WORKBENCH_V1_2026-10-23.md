# Prime Keeper rear-task manual alignment workbench V1

Date: 23 October 2026

Status: active manual fallback. V9 is rejected review evidence.

Route: `/prime-keeper-rear-task-alignment`

## Why this exists

V9 still shows the approved trousers' dark waistband below the moving blue
jumper hem in rear-task frames 11–31. Frank rejected it on 23 October 2026.
No further automatic waist composite should be presented for approval without
first reproducing his chosen join from this workbench.

The workbench exposes two exact, independently movable layers:

- the immutable V6 moving action torso for the selected frame, cropped only at
  a user-controlled bottom row; and
- the hash-pinned approved rear trousers and boots authority, cropped only at
  a user-controlled top row.

The authority's waist-level hands are outside the verified lower-body ownership
bounds and are deliberately excluded. Rows 214–230 use x82–172; rows 231–319
use x70–186, matching the deterministic compositor's authority ownership.
No layer is stretched, repainted, generated or written back to source art.

## Controls and persistence

For every frame from 11 through 31 Frank can:

- drag either torso or legs directly;
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
authority for a later deterministic V10 build; the workbench itself promotes
nothing to the animation bank.

## Verification

```bash
node scripts/verify_keeper_prime_rear_task_alignment_workbench_v1.mjs
npm run typecheck
npm run build
```

The verifier pins the 21 source frames, lower-body authority hash, ownership
bounds, V9 horizontal starting registrations, editing controls, local-only
persistence and export path. The page was also browser-tested for source-image
decoding, direct dragging, keyboard nudging and independent frame persistence.
