# Keeper Animation Workbench

Last updated: 13 October 2026.

## Current state

The separate workbench is deployed at `/animation-workbench`. **Final contains
zero animations and Draft contains zero active animation proposals.** Frank
reset both lanes after live playback showed that the coarse Frame 6 raster
created visible pixel-density, width, height, face and perspective changes at
route joins. Earlier V1/V2 turn and core-transition assets remain hash-pinned,
addressable provenance; they are not Final and must not seed new animation.

Frank permanently approved
`art/drafts/keeper-prime-master-2026-10-12-v1/` on 13 October 2026 with the
wording “Approved. Make sure this is NEVER forgotten.” It is the sole identity,
rendering, proportion, face and single-band uniform authority. The only active
visual proposal is `keeper-prime-orthographic-views-2026-10-13-v2`, reviewed at
`/keeper-review/keeper-prime-orthographic-v2/`. It carries the V1 90° side
forward byte-identically and replaces the approximate V1 back with an exact
approved-front alpha silhouette. No animation redrafting begins until Frank
approves that V2 back endpoint.

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
match exactly. The rear RGB detail remains a true back view with full cream rear
hair—not beard—and one broad pale band. Orthographic V1 is superseded but
retained unchanged as provenance.

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
- `src/animation-workbench/model.ts` — timeline, loop and transition compiler;
- `src/animation-workbench/AnimationWorkbench.tsx` — review UI;
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
  `scripts/verify_keeper_prime_orthographic_views_v2.ts` — active exact-alpha
  back candidate and zero-mismatch front/back contract.

Historical V1/V2 public assets remain content-addressed so provenance and old
exported recipes are recoverable. Presence in the asset table is not approval
and does not place an item in either active lane.

## Rebuild and verification

```sh
/Users/frank/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 scripts/build_keeper_prime_master_v1.py
/Users/frank/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 scripts/build_keeper_prime_orthographic_views_v1.py
/Users/frank/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 scripts/build_keeper_prime_orthographic_views_v2.py
/Users/frank/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 scripts/build_keeper_animation_workbench.py
npm run verify:keeper-prime-master-v1
npm run verify:keeper-prime-orthographic-v1
npm run verify:keeper-prime-orthographic-v2
npm run verify:keeper-animation-workbench
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

Frank must approve the exact-silhouette V2 back endpoint before any animation
is redrafted. The side is unchanged from V1. After approval, restart at the core set in small
reviewable batches: walk and exact stop, stop-to-walk, side-to-front/back turns,
then sit/stand. Every frame in a batch must be authored from the same smooth
high-resolution family. Only after the core joins are accepted should action
and costume inventories follow.

## Known limitations

- The workbench currently assembles recipes; it does not draw or rewrite PNGs.
- Browser Drafts are local unless exported.
- The UI does not yet add/remove route segments.
- Visual seam judgement still happens in playback; the future redraw builder
  must add deterministic pixel, anchor, silhouette and unchanged-region checks
  per join.
