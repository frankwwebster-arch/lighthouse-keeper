# Keeper Animation Workbench

> **26 October 2026 migration boundary:** This workbench remains exact
> installed-Prime review and animation evidence. It does not authorize new
> Keeper art. New Keeper work is paused until Frank-approved canon references
> populate `/public/art/keeper/canon/`; preserve every installed Prime byte.
> Prime's one broad stripe and current scale are not the target canon defined by
> `CODEX_BRIEF.md`.

Last updated: 14 October 2026.

## Installed Prime workbench state

The separate workbench is deployed at `/animation-workbench`. **Final contains
zero animations and Draft contains zero active animation proposals.** Frank
reset both lanes after live playback showed that the coarse Frame 6 raster
created visible pixel-density, width, height, face and perspective changes at
route joins. Earlier V1/V2 turn and core-transition assets remain hash-pinned,
addressable provenance; they are not Final and must not seed new animation.

Frank permanently approved Prime Master V1, the smooth rear and Side-right
endpoints, KP Rig V1, Motion V3, front ↔ side Turn V1 and exact nine-frame
side-right ↔ back V9. Exact Walk V6 and stop → walk → stop V1 are also approved
core authorities. Walk → stop → turn to camera V1 composes those exact bytes;
Frank judged it excellent and then approved **Fast Timing V1** for its
locomotion and turn phases. The route therefore keeps its artwork, frame order,
root motion and endpoints unchanged. None of these approvals has entered
workbench Final or production.

`/keeper-timing-lab` is the separate phase-timing surface. Its immutable V1
history contains the original 10 fps turn-only proposal. The repository-backed
V2 catalogue now exposes approved **Fast Timing V1**: walk 10 fps,
deceleration 12 fps, zero neutral beat, turn 16 fps and a 625 ms endpoint hold.
It provides A/B playback, large and exact game-scale views, complete or
phase-only loops, frame stepping, presets, device-local personal proposals and
JSON export. Fast Timing V1 applies only to locomotion, stopping bridges and
turns; action entry, loops, exits, comic beats and prop choreography remain
independently timed so activities can be savoured. Timing approval remains
separate from artwork, Final and production approval.

## Prime Keeper authority

The exact right-turn Frame 6 originally established the Keeper's identity,
front stance, head position and endpoint intent. Its coarse 128 × 160 raster is
no longer a rendering target. Frank selected the first smooth generated render
as the proposed Prime Keeper base and replaced the legacy double pale stripe
with one broad pale chest-and-sleeve band because the simpler uniform is more
likely to remain coherent through turns and action poses.

Prime Master V1 is normalized into a 256 × 320 source cell representing the
same 32 × 40 logical cell at density 8, with anchor `[16, 40]`. It retains the
adult rectangular eyes, separate moustache, straight closed mouth, established
beard mass and slightly fuller body. The V11 artist-smock neutral remains a
rendering-quality comparison only. All double-stripe generations are rejected
provenance. The approved PNG and approval wording are hash- and text-pinned by
the verifier so a later rebuild cannot silently replace or demote it.

The orthographic V2 pack shows the approved front in cyan over each full-colour
view. For the back, all 81,920 alpha values are copied from the approved front,
so contour, transparent gaps, cap top, floor, centreline and every row width
match exactly. Later visual review found its rounded toe-cap construction still
faced the player, so V2 is not a valid rear endpoint despite its exact outer
silhouette. Orthographic V1 and V2 are retained unchanged as provenance.

Orthographic V3 adds the stronger front-to-side vertical skeleton: cap top,
badge centre, ear centre, shoulder apex, beard base, arm-stripe top/centre/base,
midriff-stripe top/centre/base, palm centre/base, knee band and floor. The
selected side already matches total height (298 source pixels, y=18→316), arm
stripe and outer anchors. It misses badge, ear, shoulder, beard, midriff stripe,
palm and knee datums, so it is not transition-ready. Two guided generation
attempts remain rejected provenance because they also failed the hard register.

The rigged side-right V1 pack supersedes that historical side only as a review
candidate. It preserves the approved Prime identity, single broad stripe,
adult rectangular profile eye, separate moustache and readable closed mouth;
rear hair remains distinct from the forward beard. Its high-resolution source,
registered proxy, sidecar, front/side/back lineup, 15-point board and ghost
overlay are SHA-256-pinned. No non-uniform warp was used: registration is one
Lanczos scale plus translation. Frank approved Side-right V1 on 13 October
2026; it remains an artwork authority rather than a Final or production
promotion.

Orthographic V5 records Frank's explicit selection of the first rear-boot
render: rounded rear heel counters, central back seams and rear sole edges. It
preserves V2 rows 0–272 byte-for-byte and changes only rows 273–315. Its complete
alpha channel still has zero mismatches against the approved front. The exact
1122 × 1402 source is the smooth artwork master; the 256 × 320 registered image
is a Lanczos-resampled measurement/export proxy. V4's second, rougher and more
squared render is historical provenance, not a visual authority. Every future
approved model must pass smooth-render review separately from geometry.

## Purpose and boundary

The workbench is the assembly and transition layer for the future redrawn set.
It is deliberately separate from `/keeper-review/` and does not share that
platform's decisions, queue, locks or browser state.

- Final is repository-backed and immutable in the browser.
- Draft recipes edit frame references, never source PNG bytes.
- Every animation must be judged through a complete route, not an isolated
  strip.
- A hidden door may conceal a costume change, but does not exempt the visible
  animation from its transition contract.
- Workbench approval does not promote raw or runtime sprites.

## Required transition contract

Every eventual action must provide:

1. `walk` — the engine extends only this stage from world placement;
2. `stop` — visible deceleration with continuing root motion;
3. optional `turn` — to exact front or exact back where the action requires it;
4. `action` — begins from the registered stop or turn endpoint;
5. recovery to the exact stop;
6. `walk-start` — acceleration without walking on the spot;
7. `walk` — translated departure.

The first walk cycle begins while the Keeper is fully hidden behind the
departure door, so the first visible pose is already mid-stride. Costume
transitions may be hidden behind doors. Standard-uniform pose, scale, floor
anchor, head position and rendering density must remain continuous at every
visible join.

## Editor framework

The implemented Draft/Final architecture remains ready for the new set:

- copy, remove and reorder frame references;
- loop an entire preview;
- repeat a selected contiguous frame section 2–12 times;
- scrub, step, play, pause and restart animation and route previews;
- export/import browser Draft JSON;
- display pose/outfit metadata warnings at joins.

Timeline entries use stable IDs and `timelineSegmentId` identifies the one
route segment controlled by an editable timeline. Overlapping section loops
fail closed. Browser storage is now namespaced as
`keeper-animation-workbench:v3`, so rejected V1/V2 working state is not loaded
into the reset library; its older local-storage key remains untouched and can
still be recovered manually.

## Source layout

- `data/keeper_animation_workbench.json` — authoritative catalogue;
- `public/keeper-animation-workbench/catalog.json` — byte-identical deployed
  catalogue;
- `review-archive/objects/`, `review-archive/sets/` and
  `review-archive/index.json` — deduplicated, SHA-256-addressed review media and
  legacy-path redirects; no review image/GIF is shipped inside `public/`;
- `src/animation-workbench/model.ts` — timeline, loop and transition compiler;
- `src/animation-workbench/AnimationWorkbench.tsx` — review UI;
- `src/keeper-timing-lab/` — phase-timing model, tests, A/B player and proposal
  controls;
- `public/keeper-timing-lab/catalog.json` — immutable Timing Lab V1 history;
- `public/keeper-timing-lab/catalog-v2.json` — current deployed route,
  Fast Timing V1 authority, presets and phase definitions;
- `data/keeper_timing_policy.json` — machine-readable project transition
  default and explicit action-timing non-inheritance rule;
- `art/drafts/keeper-timing-lab-2026-10-14-v1/` — feedback, source hash,
  recommended 10 fps turn proposal and approval boundaries;
- `art/drafts/keeper-fast-transition-timing-2026-10-14-v1/` — Frank's
  approved fast-transition values, scope exclusions and unchanged-authority
  hashes;
- `art/drafts/keeper-prime-walk-stop-turn-back-2026-10-14-v1/` — the active
  review-only route combining exact Walk V6, the approved stop bridge, exact
  side/back V9 and Fast Timing V1 without new character drawing;
- `scripts/build_keeper_animation_workbench.py` — deterministic catalogue and
  historical-asset publisher;
- `scripts/verify_keeper_animation_workbench.ts` — lane, provenance, geometry,
  gutter and framework verifier;
- `scripts/build_keeper_prime_master_v1.py` and
  `scripts/verify_keeper_prime_master_v1.ts` — new smooth foundation pack.
- `scripts/build_keeper_prime_orthographic_views_v1.py` and
  `scripts/verify_keeper_prime_orthographic_views_v1.ts` — aligned side/back
  historical candidates and tolerance-based cross-sections;
- `scripts/build_keeper_prime_orthographic_views_v2.py` and
  `scripts/verify_keeper_prime_orthographic_views_v2.ts` — exact-alpha back
  candidate and zero-mismatch front/back contract;
- `scripts/build_keeper_prime_orthographic_views_v3.py` and
  `scripts/verify_keeper_prime_orthographic_views_v3.ts` — active 15-point
  front-to-side vertical skeleton and fail-closed side-redraft gate;
- `scripts/build_keeper_prime_orthographic_views_v4.py` and
  `scripts/verify_keeper_prime_orthographic_views_v4.ts` — active rear-boot
  alternative provenance;
- `scripts/build_keeper_prime_orthographic_views_v5.py` and
  `scripts/verify_keeper_prime_orthographic_views_v5.ts` — approved smooth
  rear-boot authority with exact alpha and unchanged-upper-body verification;
- `scripts/build_keeper_prime_rig_v1.py` and the rig-motion builders/verifiers
  — fixed anatomy, 15 datums and the approved eight-step motion authority;
- `scripts/build_keeper_prime_side_right_rigged_v1.py` and
  `scripts/verify_keeper_prime_side_right_rigged_v1.ts` — approved smooth
  side-right authority, exact 15/15 registration and approval boundary;
- `scripts/build_keeper_prime_turn_front_side_v1.py` and
  `scripts/verify_keeper_prime_turn_front_side_v1.ts` — current eight-pose
  front ↔ side review draft, reversible strips and continuity bounds.

Historical V1/V2 public assets remain content-addressed so provenance and old
exported recipes are recoverable. Presence in the asset table is not approval
and does not place an item in either active lane.

## Rebuild and verification

```sh
/Users/frank/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 scripts/build_keeper_prime_master_v1.py
/Users/frank/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 scripts/build_keeper_prime_orthographic_views_v1.py
/Users/frank/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 scripts/build_keeper_prime_orthographic_views_v2.py
/Users/frank/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 scripts/build_keeper_prime_orthographic_views_v3.py
/Users/frank/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 scripts/build_keeper_prime_orthographic_views_v4.py
/Users/frank/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 scripts/build_keeper_prime_orthographic_views_v5.py
/Users/frank/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 scripts/build_keeper_prime_rig_v1.py
/Users/frank/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 scripts/build_keeper_prime_rig_motion_v2.py
/Users/frank/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 scripts/build_keeper_prime_rig_motion_v3.py
/Users/frank/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 scripts/build_keeper_prime_side_right_rigged_v1.py
/Users/frank/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 scripts/build_keeper_prime_turn_front_side_v1.py
/Users/frank/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 scripts/build_keeper_prime_turn_side_back_v1.py
/Users/frank/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 scripts/build_keeper_prime_walk_stop_turn_back_v1.py
/Users/frank/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 scripts/build_keeper_animation_workbench.py
/Users/frank/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 scripts/build_keeper_timing_lab_v1.py
npm run verify:keeper-prime-master-v1
npm run verify:keeper-prime-orthographic-v1
npm run verify:keeper-prime-orthographic-v2
npm run verify:keeper-prime-orthographic-v3
npm run verify:keeper-prime-orthographic-v4
npm run verify:keeper-prime-orthographic-v5
npm run verify:keeper-prime-rig-v1
npm run verify:keeper-prime-rig-v2
npm run verify:keeper-prime-rig-v3
npm run verify:keeper-prime-rig-v4
npm run verify:keeper-prime-side-right-rigged-v1
npm run verify:keeper-prime-turn-front-side-v1
npm run verify:keeper-prime-turn-side-back-v1
npm run verify:keeper-prime-walk-stop-turn-back-v1
npm run verify:keeper-prime-walk-stop-turn-back-v2
npm run verify:keeper-animation-workbench
npm run verify:keeper-timing-lab-v1
npm test
npm run typecheck
npm run build
```

The checks pin the two selected references, generated source, rejected variants,
normalized candidate, sidecar, masks/guides and comparison evidence; require a
transparent cell-edge gutter; require data/public catalogue identity; require
zero active Final and Draft items; preserve the editor feature contract; and
confirm raw/runtime art and the runtime manifest remain unchanged.

## Next approval gate

Fast Timing V1 is approved and hash-pinned at
`art/drafts/keeper-fast-transition-timing-2026-10-14-v1/`; the compared frame
URLs remain identical. Walk → stop → turn fully away V1 is now the active
one-at-a-time review route. It contains 32 playback frames, travels 374
high-resolution pixels and lasts approximately 3.058 seconds: 16 walk frames
at 10 fps, four deceleration frames at 12 fps, eight turn frames at 16 fps and
the approved 625 ms rear hold. It replays neither the walk contact nor the
stationary side entry frame. Review it before front → side → walk, back → side
→ walk and the two sit/stand routes. Only after those core joins are accepted
should action and costume inventories move to the next chat.

Before those transition batches, use the approved **KP Rig V1**: a posable
2D construction skeleton with fixed bone lengths, view-specific projected
measurements, body-volume envelopes, facial/beard/clothing datums, prop contacts,
occlusion rules and floor anchors. It is an authoring underlay and measurement
contract, not a mechanical deformation of final raster art. Rig V1 remains an
immutable reversible review pack. Motion V3 is the approved construction-motion
authority while V2 remains feedback provenance; the side correction is its
first derived-art validation.

## Known limitations

- The workbench currently assembles recipes; it does not draw or rewrite PNGs.
- Browser Drafts are local unless exported.
- Fast Timing V1 is the repository-backed transition default. Other Timing Lab
  proposals and personal preview defaults are device-local unless exported;
  they do not silently update repository or runtime metadata.
- The Timing Lab's two-column large inspection panes are too narrow to show a
  complete translated walk → stop → turn route comfortably. Add a full-width
  or expanded inspection mode without changing the underlying frames, root
  motion or synchronized A/B and game-scale views.
- The UI does not yet add/remove route segments.
- Visual seam judgement still happens in playback; the future redraw builder
  must add deterministic pixel, anchor, silhouette and unchanged-region checks
  per join.
