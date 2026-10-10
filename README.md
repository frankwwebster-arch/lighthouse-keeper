# Lighthouse Keeper

A Sims-style lighthouse game for Ralph and Eddie: tell the keeper what to do by typing or tapping objects, then keep him happy through the day. The playable cutaway currently has a kitchen, living room, bedroom with en suite, and lamp room.

## Run it
```
npm install
npm run dev      # Next.js 14; open http://localhost:3000 (or this computer’s address on the same wifi, for the iPad)
npm test         # 146 tests
npm run upgrades # copy data/upgrades.csv (the upgrade list) into the game
npm run build    # production build
npm run sprites  # snap Codex's PNGs in art/raw/ into public/sprites/ (docs/CODEX_ASSETS.md)
```
On an iPad: open the address in Safari, Share, Add to Home Screen for full screen.

## Current implementation

- Floors 1–3 are modular fixed-width components in `src/ui/floors.tsx`: kitchen, living room, and bedroom with en suite. The first production Pixel batch now supplies the red/white shell bands and those three 105 × 35 room plates; interactive furniture remains separate. The toilet and wash basin are both in the en suite.
- Future standard floors are intentionally non-linear: kitchen anchors the base, lamp room stays topmost, bedroom stays directly below it, and each other floor receives a one-time random saved middle position. Concept-art taper is decorative and never fixes room width or unlock order.
- Missions run side by side, so floors arrive in any order; a finished floor appears the next morning in a random middle place that the save keeps (kitchen at the bottom, bedroom under the lamp room).
- Every object renderer accepts `standard`, `on`, and `broken`; active gameplay drives `on`. Broken objects share integer-step casing wobble, smoke and sparks. Add `?broken=tv,cooker` (or `?broken=all`) to the URL for the internal art-state preview.
- Objects can be upgraded with credits from their tap menu. The tier list is `data/upgrades.csv`; the living-room armchair now progresses from basic armchair to rocking chair to Lazyboy-style recliner, always on the same 11 px seat datum. Higher tiers do more good, faster; the bed's tier sets the morning's energy. Grown-ups set upgrade prices (overall %, then per tier) and can gift upgrades. Tier sprites are `obj_<id>_t<n>_<state>`; until they exist a `T<n>` tag stands in. `?tiers=3` previews top tiers.
- The recipe studio (`/studio`, linked from Grown-ups) is the design tool for how each activity plays. It covers walks, doors and hidden costume changes, clips, timing, sounds (drop audio files onto placeholders, then trim and set volume) and solid-object checks against each frame's real pixels. Format and workflow: `docs/RECIPES.md`.
- Grown-ups can change any animation's speed while playing (Grown-ups → Animation speeds): search the animated sprites, watch one in a preview, and step its fps from 1 to 20 in halves. One setting for the whole game, saved with the PIN (database `settings`, else the browser), is applied live. The sprite sheets' metadata remains authoritative: a tweak only lasts while its sheet keeps the speed it was made against, and "Copy for the metadata" gives `{ "animationFps": { … } }` to write back into the sheets.
- Keeper-owned assets can now break during play, block their normal actions, and be repaired. Grown-ups control average fault frequency and maximum concurrent faults; defaults are off / one. Breakdown events expose placeholder SFX categories for later audio. The shop is excluded because it is not the keeper's asset.
- The production keeper batch supplies 191 aligned exports. The 173 reviewable animation sheets (1,420 frames) have a permanent original-comparison audit and unified transition viewer in `docs/keeper-scale-audit/`; 18 obsolete modular/reference sheets are technical history only. Frank's immutable 161-review export leaves 88 happy, 70 awaiting new-draft review, 3 marked for later and 12 unreviewed. All 70 awaiting cards have a specific read-only response naming the delivered change. Frank's saved width and height are the production sizing authority—including Halloween, pyjamas, bath, Tarzan and redraft clips—and every reviewed sidecar records the exact `reviewScale`; the untouched `keeper_walk` remains the identity/anatomy reference rather than an automatic override. Direct comparison ratios fail closed only for comparable clips without a saved visual resize. The corrective pass re-rendered the falsely completed bath entry/exit and shopping carry, repaired the wider comment set, and checked final strips for neighbouring-frame contamination. Scuba has a matching jetty walk and one-shot dive whose final frame exactly hands off to horizontal swimming; parachuting has a separate slow drift loop and landing. Cleaning tiers still select a broom, basic upright hoover or eccentric super-hoover whose included tool changes only behind full cupboard-door occlusion. See `docs/review/KEEPER_ANIMATION_AWAITING_INPUT_AUDIT_2026-10-10.md` for the corrective audit.
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
- `docs/KEEPER_ASSET_SCALE.md` — human-readable keeper measurements and the rules for sizing/placing objects.
- `data/keeper_asset_contract.json` — authoritative machine-readable scale, pivots and interaction points.
- `data/keeper_object_dimensions.json` and `docs/KEEPER_OBJECT_DIMENSIONS.md` — keeper-derived furniture, fixture and station dimensions.
- `docs/keeper-scale-audit/review.html` — unified sizing and walk-to-action transition review for all 173 accepted animations, with review-state filters, filter-aware cyclic Previous/Next navigation, a specific read-only Codex response on every awaiting-input card, reload-resumable progress/filter/zoom, focused one-animation mode, frame stepping, current-card play-once/loop, canonical standing and sitting references, precise ±0.5 controls, notes/decision flags and version-9 JSON export.
- `docs/keeper-scale-audit/` — all-sheet/all-frame metrics, CSV register and nine printable contact sheets; rebuild every output, including the viewer, with the bundled Python runtime and `scripts/audit_keeper_scale.py`.
- `docs/DOORS_STAIRS_AND_COSTUMES.md` — agreed stairway, door and costume-change rules, seamless clip joins, and the decisions still to make.
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

The verification commands above cover the game and sprite pipeline. Keeper-scale verification additionally runs `scripts/audit_keeper_scale.py` and `scripts/verify_floor_asset_catalogue.py`; finished asset work is committed directly to the repository's main branch.
