# Kitchen V22 rear-wall continuous-run recipe

Date: 17 October 2026  
Status: review candidate; unapproved, unpromoted and unwired  
Review: `/keeper-review/kitchen-rear-wall-flow-v22/`

## Purpose

V21 completed the requested kitchen asset family, but its room proof assembled
mostly complete cabinet drawings. The kettle bay happened to terminate at the
rear-wall body line while the fridge, toaster, oven, mixer and sink retained
deeper lower shells. Those five bays therefore read as separate furniture
standing forward of the kettle.

V22 changes the assembly, not the accepted asset content. The kettle bay is the
depth and wall-registration authority for one connected fitted run.

## Fixed geometry

- room: `193 × 56 lp` / `772 × 224 px`
- density: `4 px/lp`
- fitted run origin: `x=21 lp` / `84 px`
- six bays: `21 lp` / `84 px` each
- total fitted run: `126 lp` / `504 px`
- worktop rear edge: `y=134 px`
- shared body-bottom line: `y=199 px`, taken from the first clear kettle row
- foot line: `y=52 lp` / `208 px`
- clear foreground: `4 lp` / `16 px`

## Construction

1. Draw the room once.
2. Draw one run-wide rear edge, sea-glass worktop, fascia and storm-blue front.
3. Draw one recessed toe-kick from the common body-bottom line to the foot line.
4. Keep full end caps only at `x=84..87` and `x=584..587`.
5. For each V21 bay, retain the central `x=6..77`, `y=0..98` treatment. This
   carries the appliance, work-surface occlusion, handles and front design while
   excluding the standalone side shell and every row forward of the kettle.
6. Redraw the common structural rows last. Draw only 2-px front divisions at
   the five internal 21-lp boundaries; these do not cross the worktop or plinth.
7. Place the V21 pedal bin, chair and table at their unchanged room coordinates.

Basic and Upgrade 1 rooms are identical outside the centre treatment of oven
bay four.

## Source and reversibility

`art/source/kitchen-rear-wall-flow-2026-10-17-v22/continuous-run-reference.png`
is a built-in OpenAI image-generation edit retained as visual-intent
provenance. It is not production art. The shipped V22 proof is deterministic
Pillow assembly by `scripts/build_kitchen_rear_wall_flow_v22.py`.

V20 and V21 source/raw/review trees are not rewritten. Rollback deletes only
the V22 source, raw, draft, review page, archive set, builder, verifier and V22
documentation. Runtime sprites, Workbench Final, Final art and Keeper art are
out of scope.

## Verification

Run:

```sh
npm run verify:kitchen-rear-wall-flow-v22
npm run archive:keeper-review
npm test
npm run typecheck
npm run build
```

The V22 verifier pins all output and source hashes, pins V21's two room hashes,
checks exact room/crop dimensions, proves three structural worktop rows cross
the entire 504-px run, proves the common body/toe-kick lines, confines the oven
tier change to its centre treatment, preserves the four-lp foreground, checks
review preloading and confirms the versioned route.
