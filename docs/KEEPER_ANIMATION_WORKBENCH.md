# Keeper Animation Workbench

## Purpose and boundary

The Keeper Animation Workbench is a new review surface at
`/animation-workbench`. It is deliberately separate from the established
`/keeper-review/` platform and does not share its saved decisions, handoff
queue, review locks or mutable browser state.

The workbench is the assembly and transition layer for the new animation set:

- **Final** preserves approved, immutable animation strips and recipes, including
  approvals later superseded as route foundations;
- **Draft** contains repository-backed proposals plus non-destructive local edits;
- every animation is judged through a complete moving transition—walk, moving
  stop, optional facing turn, action, and the compatible stop/walk egress—rather
  than as an isolated strip;
- a closed door may hide the costume swap itself, but it does not exempt the
  resulting animation from that ingress contract.

This framework does not promote anything into `art/raw/`, `public/sprites/` or
the runtime manifest. A separate explicit instruction is still required for
production promotion.

## Keeper Prime and the historical Final library

Frank approved the two V2 complete moving-model turn redraws on 12 October
2026 with the exact wording: “I am very happy with your V2.” The workbench
therefore starts with:

- `keeper_turn_front` V2;
- `keeper_turn_left_front` V2.

Live route playback subsequently exposed unacceptable joins into and out of
those V2 strips. Their original approval is retained as immutable history, but
they are tagged as a superseded route foundation and must not seed new work.
The exact V2 right-turn frame 6—byte-identical to
`keeper_neutral_standing-front_f1.png`—is now named **Keeper Prime (KP)** and is
the binding identity for every new direction, pose, outfit and expression.

The first repository Draft set,
`art/drafts/keeper-prime-core-transitions-2026-10-12-v1/`, remains immutable
review history. Frank accepted its walk→stop route and particularly the small
deceleration, but found the acceleration held the stationary endpoint too long;
the front/back turns changed perspective and body volume at route steps 19→20;
and sit/stand exposed a different apparent pixel density around Keeper Prime.

The current proposal is
`art/drafts/keeper-prime-core-transitions-2026-10-12-v2/`. It copies the V1 walk
and stop strips byte-for-byte, begins acceleration on the first distinct reverse
stop frame, and rebuilds the front turn, back turn and sit from one coherent
six-pose source each. Stand is still the exact reverse of sit. No raw/runtime
art or manifest is changed.

## Draft and Final architecture

Both lanes use the same `WorkbenchItem` structure. A timeline entry contains a
stable ID and a reference to a source-frame index; it never contains rewritten
image data. Each item also declares `timelineSegmentId`, the one route segment
controlled by that editable timeline. This is essential when a stop hold and a
walk-start share one source strip: editing the acceleration must not expand the
one-frame hold.

Final entries are loaded only from
`public/keeper-animation-workbench/catalog.json`. The interface intentionally
offers no Final mutation controls. **Copy to Draft** clones the recipe, removes
approval status and assigns new timeline IDs, while retaining provenance back
to the Final record.

The six current core repository proposals are reconciled into Draft on load.
Superseded repository-seeded V1 route records are replaced by V2, while valid
user-created working copies are retained; both V1 and V2 source assets remain
addressable so an older working copy can still render. Local edits are saved
under `keeper-animation-workbench:v2` and can be exported/imported as JSON.
Editing changes timeline references only; the versioned Draft PNGs remain
unchanged.

Draft controls currently support:

- copy a selected frame reference;
- remove a frame reference;
- move a frame left or right;
- loop the complete animation during preview;
- repeat any contiguous section for 2–12 total passes;
- remove a section loop;
- scrub, step, play, pause and restart both the animation and its route.

Section-loop endpoints refer to stable timeline-entry IDs, so copies and
reordering remain explicit. Overlapping section loops are disabled rather than
being interpreted ambiguously. This supports a future snooker recipe in which
the stroke section repeats before the recovery, idle and departure sequence.

## Core transition contract

Every animation has the same ordered contract:

1. `walk` — representative translated cycles in the workbench;
2. `stop` — a translated deceleration with residual root motion;
3. `turn` — optional, only when the action needs front or back facing;
4. `action` — the selected animation begins.
5. `stop` — the action returns to the exact registered side stop;
6. `walk-start` — the stop frames run in exact reverse;
7. `walk` — translated departure continues.

The game engine owns the only variable stitching: it deterministically repeats
the walk cycle from the Keeper's world position and the target asset's world
placement. The workbench does not author a guessed distance or save bespoke
walk counts. The walk begins while the Keeper is still fully hidden behind the
departure door, so his first visible state is already mid-stride; it must never
spawn him visibly and then start the cycle. The ingress preview simulates that
door-side emergence. Once the Keeper reaches the stop point, stop, turn if
needed and action use their fixed authored frames.

Draft V2 exposes six running routes in this exact order:

1. walk → stop;
2. stop → walk;
3. walk → stop → exact Keeper Prime full face;
4. walk → stop → exact directly-away back;
5. walk → stop → sit;
6. exact reversed sit → stop → exact reversed walk-start → walk.

All routes share the same side-stop pixels. Route 1's accepted stop and root
motion are unchanged from V1. Route 2 holds the exact stop once, then uses
reverse stop frames F3→F1 with root motion `[0.35, 0.65, 0.9]`; route 6 does
not add another hold after stand has already supplied the exact-stop frame.
The front route ends on the exact
Keeper Prime bytes; the back route ends on its registered Draft back neutral;
stand is the exact reverse of sit. Per-frame root motion continues through the
stop/start frames, eliminating the earlier walking-on-the-spot preview.

The deterministic V2 seam evidence records width, height, centre, baseline and
opaque-area change for every adjacent pair. At the specifically rejected
F2→F3 joins, front changes by −2 px width/+2 px height, back by 0/0, and sit by
+5/−7 while lowering naturally; all retain the same baseline and opaque-area
ratios of 0.97–0.99. Each moving action records one generated source and one
uniform normalization transform, preventing the previous mixed-family splice.

Future action entries must include this ingress. For example, a front-facing
snooker item can use:

`walk (runtime length) → stop → turn to front → snooker action`

The snooker action recipe can then repeat its stroke section before continuing
through its authored stand-up, idle, turn and departure frames.

## Source layout

- `data/keeper_animation_workbench.json` — authoritative catalogue checked
  into the repository;
- `public/keeper-animation-workbench/catalog.json` — byte-identical deployed
  catalogue;
- `public/keeper-animation-workbench/assets/final/` — content-hashed public
  copies of approved Final strips;
- `public/keeper-animation-workbench/assets/draft/` — content-hashed public
  copies of the six-route Keeper Prime Draft source strips;
- `src/animation-workbench/model.ts` — pure timeline, loop and transition
  compiler;
- `src/animation-workbench/AnimationWorkbench.tsx` — interactive review UI;
- `src/app/animation-workbench/page.tsx` — separate Next.js route;
- `scripts/build_keeper_prime_core_transitions_v2.py` — deterministic V2
  source normalization, endpoint replacement, V1 preservation and comparison
  evidence builder;
- `scripts/build_keeper_animation_workbench.py` — deterministic initial
  catalogue/asset builder;
- `scripts/verify_keeper_animation_workbench.ts` — immutable asset, geometry,
  gutter, approval and ingress-contract verifier.

## Rebuild and verification

The builder uses Pillow and should be run with the bundled workspace Python:

```sh
/Users/frank/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 scripts/build_keeper_prime_core_transitions_v2.py
/Users/frank/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 scripts/build_keeper_animation_workbench.py
npm run verify:keeper-animation-workbench
npm test
npm run typecheck
npm run build
```

The verifier checks byte-identical catalogues; content hashes; strip/sidecar
geometry; binary alpha; transparent cell gutters; historical Final approval
scope; the six Draft routes; residual stop root motion; exact shared side/front/
back endpoints; exact sit/stand reversal; unchanged V1 walk/stop pixels;
single-source moving actions; the shortened acceleration recipe; and numeric
continuity bounds at the three rejected F2→F3 seams.

## Extension points for Claude's review

The framework is intentionally small but complete enough to extend without
changing the asset contract. Useful next improvements include multi-select and
drag reordering, route editing, named loop regions, per-step holds or speed
curves, onion-skin join inspection, a pixel/anchor seam score, server-backed
shared Drafts and a formal Draft-to-Final approval transaction.

The invariants to preserve are:

1. Final never mutates in the browser.
2. Draft operations manipulate references, not source PNG bytes.
3. A new Final version receives a new ID and content-hashed asset path.
4. Every action requires an ingress preview, including actions whose costume
   swap was hidden by a door.
5. The engine determines walk repetition only from world placement; authors do
   not bake distance-specific walk counts into recipes. The cycle starts behind
   the door and visibility begins only after motion has begun.
6. Production promotion remains a separate explicit decision.

## Known limitations

- Edits to repository Drafts are local to one browser unless exported as JSON.
- The ingress definition is repository-authored; the UI does not yet add or
  remove route segments.
- Join diagnostics currently enforce asset, pose and outfit metadata. Visual
  judgement happens in the live transition player; automated per-join pixel,
  anchor and silhouette scoring is an intended extension.
- The workbench assembles playback recipes but does not write PNG strips or
  runtime sidecars.
