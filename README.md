# Lighthouse Keeper

A Sims-style lighthouse game for Ralph and Eddie: tell the keeper what to do by typing or tapping objects, then keep him happy through the day. The playable cutaway currently has a kitchen, living room, bedroom with en suite, and lamp room.

## Run it
```
npm install
npm run dev      # Next.js 14; open http://localhost:3000 (or this computer’s address on the same wifi, for the iPad)
npm test         # 149 tests
npm run upgrades # copy data/upgrades.csv (the upgrade list) into the game
npm run build    # production build
npm run sprites  # snap Codex's PNGs in art/raw/ into public/sprites/ (docs/CODEX_ASSETS.md)
npm run keeper-contract # rebuild neutral stills, bridges and the endpoint audit
```
On an iPad: open the address in Safari, Share, Add to Home Screen for full screen.

The keeper animation reviewer works without Wi-Fi on this Mac. Double-click
`Open Keeper Review Offline.command`, leave its Terminal window open, and use
the browser page it opens. It serves only over `127.0.0.1`, loads all 173
animation strips from this repository, retains saved review progress in that
browser and downloads `keeper-scale-choices.json` normally. Browser storage is
not synchronised between the offline and online copies: use Export on one and
Import review JSON on the other. Import validates exact `keeper_*` names, so
comments and decisions are never joined by display position. No `npm` command,
internet connection or Vercel access is required.

## Current implementation

- Floors 1–3 are modular fixed-width components in `src/ui/floors.tsx`: kitchen, living room, and bedroom with en suite. The first production Pixel batch now supplies the red/white shell bands and those three 105 × 35 room plates; interactive furniture remains separate. The toilet and wash basin are both in the en suite.
- Future standard floors are intentionally non-linear: kitchen anchors the base, lamp room stays topmost, bedroom stays directly below it, and each other floor receives a one-time random saved middle position. Concept-art taper is decorative and never fixes room width or unlock order.
- Missions run side by side, so floors arrive in any order; a finished floor appears the next morning in a random middle place that the save keeps (kitchen at the bottom, bedroom under the lamp room).
- Every object renderer accepts `standard`, `on`, and `broken`; active gameplay drives `on`. Broken objects share integer-step casing wobble, smoke and sparks. Add `?broken=tv,cooker` (or `?broken=all`) to the URL for the internal art-state preview.
- Objects can be upgraded with credits from their tap menu. The tier list is `data/upgrades.csv`; the living-room armchair now progresses from basic armchair to rocking chair to Lazyboy-style recliner, always on the same 11 px seat datum. Higher tiers do more good, faster; the bed's tier sets the morning's energy. Grown-ups set upgrade prices (overall %, then per tier) and can gift upgrades. Tier sprites are `obj_<id>_t<n>_<state>`; until they exist a `T<n>` tag stands in. `?tiers=3` previews top tiers.
- The recipe studio (`/studio`, linked from Grown-ups) is the design tool for how each activity plays. It covers walks, doors and hidden costume changes, clips, timing, sounds (drop audio files onto placeholders, then trim and set volume) and solid-object checks against each frame's real pixels. Format and workflow: `docs/RECIPES.md`.
- Grown-ups can change any animation's speed while playing (Grown-ups → Animation speeds): search the animated sprites, watch one in a preview, and step its fps from 1 to 20 in halves. One setting for the whole game, saved with the PIN (database `settings`, else the browser), is applied live. The sprite sheets' metadata remains authoritative: a tweak only lasts while its sheet keeps the speed it was made against, and "Copy for the metadata" gives `{ "animationFps": { … } }` to write back into the sheets.
- Keeper-owned assets can now break during play, block their normal actions, and be repaired. Grown-ups control average fault frequency and maximum concurrent faults; defaults are off / one. Breakdown events expose placeholder SFX categories for later audio. The shop is excluded because it is not the keeper's asset.
- The reviewed production keeper batch remains 191 aligned exports: 173 animation sheets (1,475 frames) plus 18 technical component/reference sheets. The neutral contract adds deterministic derived stills and bridges without changing that review denominator; the current raw contract contains 325 keeper sheets and publishes 339 total pictures including room/effect art. Every full-body sheet has registered `startPose` / `endPose`, walk sounds are authored once as zero-based `sfxCues`, and `npm test` rejects new or regressed endpoint failures. The exact-pixel migration audit is `docs/KEEPER_NEUTRAL_ENDPOINT_AUDIT.md`; 300 legacy endpoints remain an explicit, costume-ordered bridge/frame repair queue rather than being silently treated as exact. The five sample routes already have exact walk, four-facing turn, sit, nap, brush, TV-turn and bed endpoints; tea's specialised held-prop handoffs remain in that queue. Frank's immutable second review leaves 96 happy, 68 awaiting new-draft review, 3 marked for later and 6 unreviewed. See `docs/review/KEEPER_ANIMATION_SECOND_ROUND_DELTA_2026-10-10.md` for the exact delta and current visual-review audit.
- Every sprite-sheet workflow must keep each frame's character, props, effects and projectiles wholly inside its declared cell, with a transparent safety gutter at shared edges. The permanent project rule is `.cursor/rules/sprite-sheet-frame-isolation.mdc`; the exhaustive existing-sheet audit is the next dedicated art task in `docs/prompts/KEEPER_SPRITE_FRAME_ISOLATION_AUDIT.md`.
- Multi-frame keeper animations use 4fps by default. Frank's accepted timing changes are explicit `KEEPER_FPS_OVERRIDES` values from 1fps to 10.5fps, written to each clip's source JSON sidecar and regenerated into the runtime manifest without changing sprite pixels. The shared sprite renderer reads each manifest FPS independently, and the keeper review page can preview, save and export a later 1–20fps proposal for every action.
- Sprite manifest entries may be old string paths or metadata objects with frames, fps and optional loop/mirror/reverse/interaction-point contracts. Horizontal strips animate without CSS scaling or rotation.
- All SVG object targets work by touch, mouse, Enter and Space. At a 1024 × 768 iPad viewport, the first-three-floor targets were verified at a minimum 82 × 94 CSS px.

## Where things are

- `src/game/` — rules (`config.ts` has every number, `commands.ts` the command book and silly reactions, `engine.ts` the rules).
- `src/ui/floors.tsx` — fixed-width room definitions and the reserved diving geometry, which follows the bedroom.
- `src/ui/art.tsx` and `src/ui/Sprite.tsx` — vector fallbacks, the three-state renderer, and production strip playback.
- `public/sprites/` — production room, TV/effect and keeper review PNGs plus their runtime manifest.
- `art/source/keeper-first-batch/` — the generated keeper turnaround, deterministic density-4 authoring script, contact sheet and provenance notes.
- `art/source/first-production-batch/` — untouched generated sources and prompt/provenance notes; `scripts/build_first_asset_batch.py` rebuilds the exact `art/raw/` deliveries, then `npm run sprites` publishes them.
- `docs/PRODUCTION_ASSET_KIT.md` — exact Pixel filenames, dimensions, anchors, pivots, z-order, frame counts, fps, and delivery order.
- `docs/KEEPER_ANIMATIONS.md` — plain-English animation index, direction rules and object-alignment instructions.
- `docs/KEEPER_ANIMATION_HANDOFF.md` — complete keeper review checkpoint, correction history, exact transition-gap inventory, object-binding design and ready-to-paste next-task prompt.
- `docs/prompts/KEEPER_SPRITE_FRAME_ISOLATION_AUDIT.md` — ready-to-paste exhaustive audit/fix prompt for frame overlap and future enforcement.
- `docs/prompts/KEEPER_SIDE_ON_BEARD_OCCLUSION_AUDIT.md` — second-stage ready-to-paste audit/fix prompt for beard, hand and arm layer order across every side-on standing and sitting animation.
- `docs/KEEPER_ASSET_SCALE.md` — human-readable keeper measurements and the rules for sizing/placing objects.
- `data/keeper_asset_contract.json` — authoritative machine-readable scale, pivots and interaction points.
- `data/keeper_pose_registry.json`, `data/keeper_endpoint_audit.json` and `data/keeper_endpoint_exceptions.json` — shared pose vocabulary, current real-pixel endpoint evidence, and the frozen legacy migration boundary.
- `data/keeper_object_dimensions.json` and `docs/KEEPER_OBJECT_DIMENSIONS.md` — keeper-derived furniture, fixture and station dimensions.
- `docs/keeper-scale-audit/review.html` — unified sizing and walk-to-action transition review for all 173 accepted animations, with review-state filters, filter-aware cyclic Previous/Next navigation, a specific read-only Codex response on every awaiting-input card, reload-resumable progress/filter/zoom, focused one-animation mode, frame stepping, current-card play-once/loop, canonical standing and sitting references, precise ±0.5 controls, notes/decision flags and version-9 JSON export/import by exact animation name. Double-click `Open Keeper Review Offline.command` to use this complete workflow without Wi-Fi; transfer progress manually by Export/Import because browser storage does not auto-sync.
- `docs/keeper-scale-audit/` — all-sheet/all-frame metrics, CSV register and nine printable contact sheets; rebuild every output, including the viewer, with the bundled Python runtime and `scripts/audit_keeper_scale.py`.
- `docs/DOORS_STAIRS_AND_COSTUMES.md` — agreed stairway, door and costume-change rules, seamless clip joins, and the decisions still to make.
- `docs/BACKGROUND_ELEMENTS.md` — Codex's brief for every background layer, sunrise and sunset, night lighting, and the every-asset-can-be-upgraded rule for objects.
- `docs/AMBIENCE_AND_BACKDROP.md` — backdrop layers, weather overlays, ambient sound, the lamp's start-up, audio file specs and the decisions still to make.
- `docs/RECIPES.md` — the recipe format, the recipe studio and what each animation sheet needs for it.
- `docs/EXPANSION_DESIGN.md` — living write-up of agreed room ideas, random floor placement, night reveals, weather, transport, island expansions and energy systems.
- `art/manifest.json` and `art/asset_inventory.json` — facts about the concept/prototype image pack; these are not a production rig.

## Stack
Next.js 14 (App Router), React 18, TypeScript, Vitest. Neon Postgres (optional; falls back to browser localStorage). Deploy on Vercel; set `DATABASE_URL` (pooled) for Production.

## Players and the database
A "Who is playing?" screen lets each child have their own game and their own grown-ups' dials (allowance, prices, quiz difficulty). With `DATABASE_URL` set (Neon via Vercel's Storage tab) saves live in Postgres and follow the player to any device; the tables are created automatically on first use. With no `DATABASE_URL` everything stays in the browser. Grown-ups' PIN starts as 1234 (Menu, then Grown-ups), and is checked on the server when the database is on.


## More

`docs/STATUS.md` is the full write-up. `docs/CODEX_BRIEF.md` is the authoritative art brief. `HANDOFF_TO_CLAUDE.md` separates implemented runtime work from missing production artwork.

## Verification

Last verified on 10 October 2026:

```sh
npm test
npm run typecheck
npm run build
```

The verification commands above cover the game and sprite pipeline; `npm test` begins with the keeper contract check. Keeper-scale verification additionally runs `scripts/audit_keeper_scale.py` and `scripts/verify_floor_asset_catalogue.py`; finished asset work is committed directly to the repository's main branch.
