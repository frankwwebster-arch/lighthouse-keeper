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

The canonical online keeper animation reviewer is
`https://lighthouse-keeper-mu.vercel.app/keeper-review/`. The offline launcher
serves an exact repository copy of that same generated page and review-only
draft assets: double-click `Open Keeper Review Offline.command`, leave its
Terminal window open, and use the browser page it opens. Both versions load all
173 animation strips and retain saved review progress in that browser. In the
online reviewer, use **Hand back to Codex** whenever a batch is ready: its
confirmation explains that it will first save any edited cards locally, then
sends the complete exact-name review register to the durable handoff queue and
confirms the receipt on-screen—no JSON download is needed. The collapsed
Advanced backup/import control remains only for exceptional offline recovery.
The offline copy needs no `npm` command, internet connection or Vercel access,
but cannot submit a handoff until the batch is opened online.

## Current implementation

- Floors 1–3 are modular fixed-width components in `src/ui/floors.tsx`: kitchen, living room, and bedroom with en suite. The first production Pixel batch now supplies the red/white shell bands and those three 105 × 35 room plates; interactive furniture remains separate. The toilet and wash basin are both in the en suite.
- Future standard floors are intentionally non-linear: kitchen anchors the base, lamp room stays topmost, bedroom stays directly below it, and each other floor receives a one-time random saved middle position. Concept-art taper is decorative and never fixes room width or unlock order.
- Missions run side by side, so floors arrive in any order; a finished floor appears the next morning in a random middle place that the save keeps (kitchen at the bottom, bedroom under the lamp room).
- Every object renderer accepts `standard`, `on`, and `broken`; active gameplay drives `on`. Broken objects share integer-step casing wobble, smoke and sparks. Add `?broken=tv,cooker` (or `?broken=all`) to the URL for the internal art-state preview.
- Objects can be upgraded with credits from their tap menu. The tier list is `data/upgrades.csv`; the living-room armchair now progresses from basic armchair to rocking chair to Lazyboy-style recliner, always on the same 11 px seat datum. Higher tiers do more good, faster; the bed's tier sets the morning's energy. Grown-ups set upgrade prices (overall %, then per tier) and can gift upgrades. Tier sprites are `obj_<id>_t<n>_<state>`; until they exist a `T<n>` tag stands in. `?tiers=3` previews top tiers.
- The recipe studio (`/studio`, linked from Grown-ups) is the design tool for how each activity plays. It covers walks, doors and hidden costume changes, clips, timing, sounds (drop audio files onto placeholders, then trim and set volume) and solid-object checks against each frame's real pixels. Format and workflow: `docs/RECIPES.md`.
- Grown-ups can change any animation's speed while playing (Grown-ups → Animation speeds): search the animated sprites, watch one in a preview, and step its fps from 1 to 20 in halves. One setting for the whole game, saved with the PIN (database `settings`, else the browser), is applied live. The sprite sheets' metadata remains authoritative: a tweak only lasts while its sheet keeps the speed it was made against, and "Copy for the metadata" gives `{ "animationFps": { … } }` to write back into the sheets.
- Keeper-owned assets can now break during play, block their normal actions, and be repaired. Grown-ups control average fault frequency and maximum concurrent faults; defaults are off / one. Breakdown events expose placeholder SFX categories for later audio. The shop is excluded because it is not the keeper's asset.
- The reviewed production keeper batch remains 191 aligned exports: 173 animation sheets (1,479 frames) plus 18 technical component/reference sheets. The visually rejected second-round production pass was rolled back as a unit to commit `131191c`; that history and Frank's immutable comments remain intact. Separately, Frank explicitly selected nine named source replacements on 10 October, plus the dependent `keeper_parachute_landing` bridge; these ten exact-name clips are now canonical after final-strip inspection, while their previous canonical strips stay visible in the reviewer. The neutral contract adds deterministic derived stills and bridges without changing the 173-sheet review denominator; the current raw contract contains 325 keeper sheets and publishes 339 total pictures including room/effect art. Every full-body sheet has registered `startPose` / `endPose`, walk sounds are authored once as zero-based `sfxCues`, and `npm test` rejects new or regressed endpoint failures. The exact-pixel migration audit is `docs/KEEPER_NEUTRAL_ENDPOINT_AUDIT.md`; 300 legacy endpoints remain an explicit, costume-ordered bridge/frame repair queue rather than being silently treated as exact.
- Every sprite-sheet workflow must keep each frame's character, props, effects and projectiles wholly inside its declared cell, with a transparent safety gutter at shared edges. The first dedicated, draft-only audit is complete: all manifest Keeper frames are classified and all 101 true standing/sitting side-action sheets were checked against the pinned fuller, stepped `keeper_clear_snow` reference. The only confirmed issue is `keeper_darts` frames 3–6, isolated as an unpromoted `Draft v2`; canonical assets remain unchanged. The next audits are exhaustive frame isolation, then released-prop surface contact, via `docs/prompts/KEEPER_SPRITE_FRAME_ISOLATION_AUDIT.md` and `docs/prompts/KEEPER_RELEASE_SURFACE_DATUM_AUDIT.md`. The permanent standard tabletop support datum is 19 logical pixels above the floor—8 pixels above the 11-pixel seat guide—and applies to the base of cake, plate, record and other table-height released props.
- `data/keeper_side_on_beard_occlusion_audit.json`, `art/drafts/keeper-side-on-beard-occlusion-2026-10-10-v2/`, and `scripts/verify_side_on_beard_occlusion.ts` provide the reproducible v2 audit, including hashes, classifications, gutter checks, and the foreground hand-over-beard correction check. The partial v1 audit remains rejected historical evidence only.
- Frank's original 14-pose darts source remains a separate byte-identical `keeper-darts-user-selected-2026-10-10-v1` visual comparison. The reviewer shows canonical, `Draft v2`, and `Frank-selected draft` together; neither draft is promoted. `data/keeper_review_drafts.json` also records the ten selected canonical promotions, each with SHA-256-pinned prior-version evidence. The post-audit review-delta prompt is `docs/prompts/KEEPER_POST_AUDIT_REVIEW_DELTA.md`.
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
- `docs/prompts/KEEPER_SIDE_ON_BEARD_OCCLUSION_AUDIT.md` — first-stage ready-to-paste audit/fix prompt for beard, hand and arm layer order across every side-on standing and sitting animation.
- `docs/prompts/KEEPER_SPRITE_FRAME_ISOLATION_AUDIT.md` — second-stage ready-to-paste exhaustive audit/fix prompt for frame overlap and future enforcement.
- `docs/prompts/KEEPER_POST_AUDIT_REVIEW_DELTA.md` — ready-to-paste exact-name, JSON-ingestion prompt for Frank's next review after all three audits.
- `docs/prompts/KEEPER_RELEASE_SURFACE_DATUM_AUDIT.md` — third-stage ready-to-paste audit prompt for consistent tabletop release height and prop hand-off.
- `docs/prompts/KEEPER_REVIEW_WORKBENCH_BUILD.md` — ready-to-paste separate build prompt for the project-specific next stage of the reviewer: rooms, furniture, annotations, crop proposals, routines, triggers and context preview, with later generic productisation deliberately deferred.
- `docs/KEEPER_ASSET_SCALE.md` — human-readable keeper measurements and the rules for sizing/placing objects.
- `data/keeper_asset_contract.json` — authoritative machine-readable scale, pivots and interaction points.
- `data/keeper_pose_registry.json`, `data/keeper_endpoint_audit.json` and `data/keeper_endpoint_exceptions.json` — shared pose vocabulary, current real-pixel endpoint evidence, and the frozen legacy migration boundary.
- `data/keeper_object_dimensions.json` and `docs/KEEPER_OBJECT_DIMENSIONS.md` — keeper-derived furniture, fixture and station dimensions.
- `public/keeper-review/index.html` — canonical online reviewer deployed at `/keeper-review/`; the offline launcher serves this exact same file and its review-only draft assets. `docs/keeper-scale-audit/review.html` remains the generated audit copy and must be byte-identical. Its gallery is a compact visual scan (name, review state, last local save/redraft, playback and frame stepping); `Open close review` opens any chosen card immediately. `Find animation` searches names and overrides all other filters; otherwise independently filter by review state, pose and active/reserve use list. Close review lets Frank override the inferred pose tag, relegate a likely duplicate to the reversible reserve list, expand/compress retained draft comparisons, and select canonical or every exact-name draft as an exportable preferred-promotion candidate—without mutating production. **Hand back to Codex** always asks for confirmation, saves any unsaved cards to that browser if confirmed, then submits the full batch to the durable server-side queue; JSON backup/import is collapsed as an exceptional recovery option.
- `data/keeper_side_on_beard_occlusion_audit.json`, `art/drafts/keeper-side-on-beard-occlusion-2026-10-10-v2/`, and `art/drafts/keeper-side-on-beard-occlusion-2026-10-10-v1/` — completed draft-only v2 beard/hand audit and preserved rejected v1 history. The active reviewer shows v2 beside canonical and the separate Frank-selected darts draft; the verifier prevents implicit promotion.
- `data/keeper_review_drafts.json` and `art/drafts/` — SHA-256-pinned, exact-name review comparisons: the draft-only darts candidate plus the ten selected canonical promotions and their reversible previous versions. `scripts/verify_keeper_review_drafts.ts` checks their source, canonical/current, comparison strips, sidecars, gutters and reviewer attachment.
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
