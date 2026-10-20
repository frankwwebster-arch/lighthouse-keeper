# Kitchen Split Cabinet Workbench V38

V38 is a reversible test of separating approved Cabinet V11 into two
independently movable one-bay units. It does not add pair movement and does not
alter the approved source run, V37 appliances, Final or runtime.

## Construction

- Cabinet A and Cabinet B retain the distinct centre artwork of the first and
  second exact V11 bays.
- Each has an `84 × 74 px` logical body inside a `92 × 82 px` transparent cell
  with offset `(-4,-4)`.
- Four deterministic edge variants exist per bay: both sides exposed, only
  left joined, only right joined and both joined.
- Exposed sides use exact V11 rounded outer-end pixels. Joined sides use exact
  V11 internal-edge pixels. No cabinet region is generated or redrawn.

## Placement

Cabinet A, Cabinet B, fridge, sink and oven are five independent one-bay
objects on the six canonical origins `[84,168,252,336,420,504]`. There is
always one empty destination. Loose dragging previews movement; release commits
the selected object to that exact free origin. Pair movement is deliberately
absent.

The resolver evaluates both cabinet sides after every move. Oven pairs retain
the V32 triangular repair; all other adjacent pairs use the V22 body backfill
and countertop cap. The sink's exposed-left correction remains active.

## Review and verification

- Review: `/keeper-review/kitchen-split-cabinet-workbench-v38/`
- Builder: `scripts/build_kitchen_split_cabinet_workbench_v38.mjs`
- Verifier: `npm run verify:kitchen-split-cabinet-workbench-v38`

The verifier checks every pixel in all eight cabinet variants against its
declared V11 source region, all 720 non-overlapping five-object arrangements,
both exposed-side directions, every join class, archive hashes and preload
behaviour. Kettle, toaster and mixing bowl remain explicitly unstarted.
