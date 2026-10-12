# Keeper Animation Workbench

## Purpose and boundary

The Keeper Animation Workbench is a new review surface at
`/animation-workbench`. It is deliberately separate from the established
`/keeper-review/` platform and does not share its saved decisions, handoff
queue, review locks or mutable browser state.

The workbench is the assembly and transition layer for the new animation set:

- **Final** contains approved, immutable animation strips and recipes;
- **Draft** contains non-destructive working recipes made from Final assets;
- every animation is judged through one ingress sequence—walk, stop, optional
  facing turn, then the action—rather than as an isolated strip;
- a closed door may hide the costume swap itself, but it does not exempt the
  resulting animation from that ingress contract.

This framework does not promote anything into `art/raw/`, `public/sprites/` or
the runtime manifest. A separate explicit instruction is still required for
production promotion.

## Initial Final library

Frank approved the two V2 complete moving-model turn redraws on 12 October
2026 with the exact wording: “I am very happy with your V2.” The workbench
therefore starts with:

- `keeper_turn_front` V2;
- `keeper_turn_left_front` V2.

Each Final entry points to a content-hashed public copy of the approved V2
draft strip. The original draft path and SHA-256 remain in the catalogue. The
runtime walk, stop and neutral strips are read-only context assets. Walk and
stop compose the ingress preview; the neutral remains endpoint context.

## Draft and Final architecture

Both lanes use the same `WorkbenchItem` structure. A timeline entry contains a
stable ID and a reference to a source-frame index; it never contains rewritten
image data.

Final entries are loaded only from
`public/keeper-animation-workbench/catalog.json`. The interface intentionally
offers no Final mutation controls. **Copy to Draft** clones the recipe, removes
approval status and assigns new timeline IDs, while retaining provenance back
to the Final record.

Draft entries are saved under the browser-local key
`keeper-animation-workbench:v1`. They can be exported and imported as JSON for
portable handoff. Repository builds ship no mutable Draft records.

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

## Ingress contract

Every animation has the same ordered contract:

1. `walk` — one representative cycle in the workbench;
2. `stop` — the matching stop strip;
3. `turn` — optional, only when the action needs front or back facing;
4. `action` — the selected animation begins.

The game engine owns the only variable stitching: it deterministically repeats
the walk cycle from the Keeper's world position and the target asset's world
placement. The workbench does not author a guessed distance or save bespoke
walk counts. The walk begins while the Keeper is still fully hidden behind the
departure door, so his first visible state is already mid-stride; it must never
spawn him visibly and then start the cycle. The ingress preview simulates that
door-side emergence. Once the Keeper reaches the stop point, stop, turn if
needed and action use their fixed authored frames.

The initial turn-item route is therefore:

`walk (one representative cycle) → stop → action: V2 turn`

The left-facing route mirrors only the mirror-safe production walk and stop,
then begins the authored left-to-front V2 turn. The turn's own final frame is
already the exact canonical front neutral, so no extra join is invented. The
interface plays the real strips consecutively and exposes every route segment.
Metadata diagnostics reject pose or outfit disagreement at a join.

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
- `src/animation-workbench/model.ts` — pure timeline, loop and transition
  compiler;
- `src/animation-workbench/AnimationWorkbench.tsx` — interactive review UI;
- `src/app/animation-workbench/page.tsx` — separate Next.js route;
- `scripts/build_keeper_animation_workbench.py` — deterministic initial
  catalogue/asset builder;
- `scripts/verify_keeper_animation_workbench.ts` — immutable asset, geometry,
gutter, approval and ingress-contract verifier.

## Rebuild and verification

The builder uses Pillow and should be run with the bundled workspace Python:

```sh
/Users/frank/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 scripts/build_keeper_animation_workbench.py
npm run verify:keeper-animation-workbench
npm test
npm run typecheck
npm run build
```

The verifier checks that the data and deployed catalogues are byte-identical;
all asset hashes and strip dimensions match; Final frames are non-empty and
clear of every cell edge; approval scope cannot imply runtime promotion; and
every route is exactly walk, stop, optional turn and action; walk length is
runtime-owned; and all joins have compatible pose metadata.

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

- Drafts are currently local to one browser unless exported as JSON.
- The ingress definition is repository-authored; the UI does not yet add or
  remove route segments.
- Join diagnostics currently enforce asset, pose and outfit metadata. Visual
  judgement happens in the live transition player; automated per-join pixel,
  anchor and silhouette scoring is an intended extension.
- The workbench assembles playback recipes but does not write PNG strips or
  runtime sidecars.
