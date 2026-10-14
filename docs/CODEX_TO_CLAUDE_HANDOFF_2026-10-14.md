# Lighthouse Keeper — Codex to Claude handoff

Date: 14 October 2026

Repository: `/Users/frank/Documents/ChatGPT/Lighthouse Keeper`

Branch: `main`

Starting commit: `cca03dc` (`Add Keeper timing lab`)

## Purpose of this note

Frank is deliberately using both Codex and Claude Code on this project. This
note is the shared boundary between them. It records the current Keeper
animation authorities, what remains only a proposal, the next animation gates,
and a separate architecture task Claude can progress without disturbing the
artwork review.

Before changing animation-related code or metadata, read these files in full:

- `docs/KEEPER_ARTWORK_AUTHORING_AND_REVIEW_PLAYBOOK.md`
- `docs/KEEPER_ANIMATION_HANDOFF.md`
- `docs/KEEPER_ANIMATION_WORKBENCH.md`
- this handoff

Pull `main` and confirm commit `cca03dc` or a documented successor before
working. Do not infer approval from the presence of an asset in the repository
or a public review page.

## Can Claude review the public site?

Yes, provided the Claude environment has public web/browser access. The pages
are public and do not require authentication:

- Timing Lab: `https://lighthouse-keeper-mu.vercel.app/keeper-timing-lab?v=cca03dc`
- Source route: `https://lighthouse-keeper-mu.vercel.app/keeper-review/keeper-prime-walk-stop-turn-front-v1/?v=cca03dc`
- Animation Workbench: `https://lighthouse-keeper-mu.vercel.app/animation-workbench?v=cca03dc`

The Timing Lab is the best place for visual timing review. Compare A and B at
both large and game scale, and loop `stop → front` and `turn only`. Frank has
now approved **Fast Timing V1** for transition phases: walk 10 fps,
deceleration 12 fps, no neutral pause, turn 16 fps and a 625 ms endpoint hold.
It does not govern action animation timing.

There is one current UI defect: the **large inspection pane is too narrow to
show the complete walk → stop → turn route comfortably**. Do not interpret
clipping or cramped travel as an animation defect. A future UI amendment should
offer a full-width/expanded inspection stage while preserving the side-by-side
A/B comparison and exact game-scale view.

A web review alone is not a full technical review. The repository is required
to inspect immutable hashes, source registers, root-motion data, rejection
history, test contracts and promotion boundaries. If Claude cannot use a
browser, it can still inspect the committed catalogues and tests, but should not
claim a visual verdict.

## Keeper identity and approval state

The Keeper is derived from **Prime Master V1**: the smooth, adult, slightly
rotund standard-uniform model with one broad pale jumper band. Preserve the
restrained face, solid dark rectangular eyes, separate moustache, readable
closed mouth, established beard mass, stable floor anchor and smooth rendering.

Approved artwork/construction authorities now include:

- Prime Master V1 front identity;
- the smooth Orthographic V5 rear endpoint with correctly rear-facing boots;
- Side-right V1, registered to all 15 rig datums;
- KP Rig V1 and KP Rig Motion V3;
- front ↔ side Turn V1, with its accepted slight cadence change near 45°;
- exact nine-frame side ↔ back Turn V9, pinned by V10;
- exact Walk V6, pinned by its V7 approval record;
- exact stop → walk → stop V1, pinned by its V2 approval record;
- the exact frame composition of walk → stop → turn to camera V1, which Frank
  judged excellent.

The timing of walk → stop → turn to camera is approved as **Fast Timing V1**.
The complete route previews in approximately 2.996 seconds rather than 4.000
seconds. Frame bytes, order, root motion and endpoints are identical. The
approved scope is locomotion, stopping bridges, turns and their short readable
endpoint hold. Action entry, loops, exits, reactions and prop choreography are
explicitly excluded and retain independent, activity-specific timing.

No animation is currently in Workbench **Final**, and no Keeper Prime draft has
been promoted into canonical raw/runtime art or the production manifest.
Artwork approval, timing approval, Workbench Final and production promotion are
four separate gates.

Important rejected provenance must remain rejected:

- do not reactivate the withdrawn face-camera amendments;
- do not recreate the explicitly deleted `keeper_count_money` amendment
  without a new direct instruction from Frank;
- do not use coarse historical Frame 6 pixels as a rendering target;
- do not restore the double-stripe jumper;
- do not use the rougher rear model or the front-facing rear boots;
- do not use the 16-frame side/back V8 experiment: it was visibly jerkier.

## What Codex has done in the current core-animation pass

The recent work rebuilt the Keeper from a single smooth identity authority,
then established orthographic endpoints, a measurement rig and the following
core movement chain:

1. smooth Prime front, side-right and rear authorities;
2. front ↔ side and side ↔ back turns;
3. an eight-frame side walk with opposing arms and accepted leg motion;
4. deterministic acceleration and deceleration bridges;
5. the approved stop → walk → stop route;
6. walk → stop → turn to camera assembled only from exact approved frames;
7. a separate Timing Lab so cadence can be tuned without redrawing or silently
   re-approving artwork.

The approved locomotion data is not cosmetic. In the high-resolution 256 × 320
registration space, stop → walk uses deltas `2, 6, 12, 18`, steady walking uses
`21` per frame, and walk → stop uses `18, 12, 6, 2`. There are zero
walking-on-the-spot frames. Runtime movement must eventually consume the
animation's root-motion schedule instead of moving the character at an
unrelated constant speed.

All new proposals remain versioned and reversible. Deterministic checks cover
authority hashes, frame order, geometry, transparent gutters, public/source
agreement and production non-mutation. The Fast Timing V1 delivery passes all
176 tests, type-checking and the production build; use the latest documented
successor to `cca03dc` before changing these contracts.

## Next Keeper animation steps

Continue one route at a time, with Frank reviewing each deployed proposal:

1. Improve the Timing Lab inspection layout so a complete translated route can
   use a full-width or expanded stage. Do not change animation data as part of
   that UI repair.
2. Build front → side → walk using approved Fast Timing V1.
3. Build walk → stop → back, then back → side → walk using approved Fast Timing
   V1.
4. Build walk → stop → sit and sit → stop → walk using fixed seat/contact
   anchors.
5. Only after these core joins are accepted, move to action animations and
   costume families. Costume changes may be hidden behind doors; visible joins
   still require exact pose, scale, floor and timing continuity. Action timing
   must remain expressive and must not inherit the fast transition preset.

Do not batch-promote work merely because individual components are approved.

## A safe and useful Claude task now

Claude can work in parallel on the **furniture placement and phase-aware
locomotion architecture**. This is valuable now because the present playable
movement system predates the approved animation/root-motion contract:

- `src/game/config.ts` stores one hard-coded `x` per object;
- `src/game/world.ts` routes between points but has no furniture footprint or
  collision model;
- `src/ui/Actors.tsx` advances the Keeper at constant `SPEED = 240`, independent
  of sprite frame and foot phase;
- if gameplay changes phase early, `Actors.tsx` may snap him directly to the
  target;
- `src/ui/floors.tsx` defines room zones but not a general placement grid,
  approach slot or clearance contract.

That is acceptable prototype history, but it must not be wired directly to the
new Keeper Prime animation routes.

### Requested architecture deliverable

Prepare a proposal and pure model/tests before migrating runtime rendering.
The proposal should define:

1. **One coordinate contract.** Distinguish logical art pixels, the current 4×
   1200 × 760 stage coordinates, high-resolution Keeper review coordinates and
   CSS display pixels. Conversion belongs at explicit boundaries; no silent
   fractional positions.
2. **Furniture placement records.** Separate `renderAnchor`, footprint,
   collision/solid intervals, `keeperUsePoint`, allowed approach side/facing,
   effect/bubble origins, z-order, room zone and door/aisle clearance. Tier
   upgrades retain footprint and use points unless a reviewed migration says
   otherwise.
3. **A placement grid and validator.** Furniture and especially its
   `keeperUsePoint` must snap deterministically. Reject overlaps, blocked doors,
   unreachable approach points, out-of-room bounds and unsafe Keeper/prop
   intersections. Do not bake movable furniture into room plates.
4. **A route plan, not just a destination.** The plan should contain door or
   stair transfer points, occluded lead-in/lead-out, direction, exact stop
   anchor, optional turn, action ingress and action egress.
5. **A phase-aware locomotion controller.** Frame selection and world
   translation must come from the same timeline. Reserve the authored
   acceleration/deceleration distances, repeat complete steady walk phases
   where possible, and arrive on the exact stop frame without a teleport,
   planted-foot slide or walking on the spot.
6. **An explicit remainder policy.** Arbitrary room distances will not always
   equal an integer number of authored walk cycles plus the fixed start/stop
   bridges. Compare documented options—placement/use-point quantisation,
   bounded per-frame distance adjustment, additional phase-compatible stop
   bridges, or hidden-door absorption—and recommend one with measured visual
   tolerances. Do not silently stretch a stride or snap the final frame.
7. **Deterministic tests.** At minimum: identical inputs produce identical
   placements/routes; all coordinates obey the declared grid; solids and door
   clearance do not overlap; every target has a reachable approach; frame/root
   motion agree; acceleration starts moving immediately; deceleration reaches
   the exact target; no locomotion frame has zero movement; left/right routes
   mirror correctly; save/load preserves placements; and object tiers do not
   move their interaction anchor unexpectedly.
8. **A debug overlay proposal.** Show grid, footprints, use points, route
   segments, current gait frame/foot phase, planned root delta and residual
   distance. This is diagnostic UI, not production art.

Recommended output location:

- `docs/architecture/FURNITURE_PLACEMENT_AND_LOCOMOTION.md`
- pure types/model/tests in a new isolated module only if the written contract
  is sufficiently settled;
- no edits to Keeper PNGs, draft registers, review pages, Workbench Final,
  production manifests or existing approved hashes.

The architecture proposal must treat the current object locations and the
catalogue's `usePoint`/footprint values as evidence to reconcile, not automatic
truth. `data/keeper_object_dimensions.json`, `docs/KEEPER_OBJECT_DIMENSIONS.md`,
`docs/floor-asset-catalogue/`, `docs/RECIPES.md` and
`docs/DOORS_STAIRS_AND_COSTUMES.md` are relevant inputs.

## Collaboration protocol

To avoid Codex and Claude overwriting one another:

1. pull the latest `main` and quote the starting commit in the work note;
2. use a dedicated branch/worktree for the furniture/locomotion architecture;
3. do not touch active Keeper art/draft/reviewer directories;
4. record assumptions and unresolved choices in the architecture document;
5. run relevant tests, type-checking and build checks;
6. hand back the branch/commit, changed-file list, verification results and
   explicit open decisions;
7. let Frank approve any gameplay contract that would constrain furniture
   placement or animation authoring before runtime migration.

Claude is welcome to challenge the proposed architecture with evidence. It
should not reinterpret a visual or production approval, nor make a promotion,
without Frank's direct instruction.
