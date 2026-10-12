# Keeper Animation Workbench

## Purpose and boundary

The Keeper Animation Workbench is a new review surface at
`/animation-workbench`. It is deliberately separate from the established
`/keeper-review/` platform and does not share its saved decisions, handoff
queue, review locks or mutable browser state.

The workbench is the assembly and transition layer for the new animation set:

- **Final** contains approved, immutable animation strips and recipes;
- **Draft** contains non-destructive working recipes made from Final assets;
- visible same-costume routes can be played as one sequence, rather than
  judging an action strip in isolation;
- costume-to-costume joins can be marked `door-hidden`, because the closed
  doors provide the transition.

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
runtime walk, stop and neutral strips are read-only context assets used only to
compose transition previews.

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

## Transition contract

Every item declares one of two policies:

- `required`: the join remains visible and must have a reviewable route;
- `door-hidden`: a costume change is fully hidden and the visible seam check is
  intentionally exempt.

The initial right-facing route is:

`walk ×2 → stop → V2 turn → canonical front idle`

The left-facing route mirrors only the mirror-safe production walk and stop;
it then uses the authored left-to-front V2 turn and the same canonical front
idle. The interface plays the real strips consecutively and exposes every
route segment. Metadata diagnostics reject pose or outfit disagreement at a
join. This makes the player's important sequence—walk, settle, turn, act and
recover—an ordinary review object rather than a later integration check.

Future action entries should include the complete visible route relevant to
that action. For example, a snooker item can use:

`walk → stop → turn if required → acquire cue → repeated stroke section → release cue → idle → turn → depart`

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
  gutter, approval and route-contract verifier.

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
both routes contain walk, stop, turn and front-idle segments with compatible
pose metadata.

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
4. Same-costume visible routes require transition preview.
5. Door-hidden costume changes are the only automatic transition exemption.
6. Production promotion remains a separate explicit decision.

## Known limitations

- Drafts are currently local to one browser unless exported as JSON.
- The route definition is repository-authored; the UI does not yet add or
  remove route segments.
- Join diagnostics currently enforce asset, pose and outfit metadata. Visual
  judgement happens in the live transition player; automated per-join pixel,
  anchor and silhouette scoring is an intended extension.
- The workbench assembles playback recipes but does not write PNG strips or
  runtime sidecars.
