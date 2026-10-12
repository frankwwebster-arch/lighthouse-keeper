# Lighthouse Keeper

A Sims-style lighthouse game for Ralph and Eddie: tell the keeper what to do by typing or tapping objects, then keep him happy through the day. The playable cutaway currently has a kitchen, living room, bedroom with en suite, and lamp room.

## Run it
```
npm install
npm run dev      # Next.js 14; open http://localhost:3000 (or this computer’s address on the same wifi, for the iPad)
npm test         # full verification suite
npm run upgrades # copy data/upgrades.csv (the upgrade list) into the game
npm run build    # production build
npm run sprites  # snap Codex's PNGs in art/raw/ into public/sprites/ (docs/CODEX_ASSETS.md)
npm run keeper-contract # rebuild neutral stills, bridges and the endpoint audit
```
On an iPad: open the address in Safari, Share, Add to Home Screen for full screen.

The keeper animation reviewer is online only at
`https://lighthouse-keeper-mu.vercel.app/keeper-review/`. Use **Hand back to
Codex** whenever a batch is ready: its
confirmation explains that it will first save any edited cards locally, then
sends the complete exact-name review register to the durable handoff queue. The
queue records an authoritative exact-name delta, so a later Codex task reviews
only animation decisions or notes changed since the previous hand-back (or the
shipped saved-review baseline for the first server hand-back); the receipt
reports that count on-screen—no JSON download is needed. The collapsed
Advanced backup/import control remains only for exceptional browser recovery.
When Codex claims a queued batch to make amendments, the online reviewer polls
that server state and becomes read-only until the amended delivery is marked
complete. Playback and inspection remain available, but no review decisions can
diverge while work is in progress. The repository’s generated audit page is not
a second review workspace: opening it outside the deployed route sends the
viewer to the online reviewer, keeping saved feedback and the work lock in one
place.

The four-hour review hand-back monitor is deliberately outside Codex: the
per-user macOS `launchd` job installed by
`scripts/install_keeper_review_handoff_monitor.sh` reads only the public queue
and shows a native notification only for a new batch with a non-zero semantic
change count. It keeps its own local “already notified” list under Application
Support and never edits review data or sprite assets. The older Codex heartbeat
must remain paused to avoid duplicate alerts.

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
- Every sprite-sheet workflow must keep each frame's character, props, effects and projectiles wholly inside its declared cell, with a transparent safety gutter at shared edges. The side-on beard audit now classifies every manifest frame and inventories 163 standing/sitting side-on sheets. `keeper_clear_snow` is SHA-256-pinned as the canonical fuller stepped beard. An eligible, landmark-aligned beard-mask comparison passes with a symmetric silhouette difference of at most one logical pixel; 994 different-pose frames remain non-comparable until approved beard masks, facial landmarks and depth/component ownership evidence exist. No beard correction is justified or promoted.
- `data/keeper_side_on_beard_occlusion_audit.json` and `scripts/verify_side_on_beard_occlusion.ts` provide the reproducible evidence audit, source hashes, classifications and gutter evidence. Historical v1 and v2 Darts draft files are preserved but are non-promotable evidence only; the v2 colour-predicate edit is not a confirmed fix.
- The immutable 11 October review-platform handoff contains an 81-name amendment delta. Forty-one exact names have new side/rear, timing or object-action candidates available as reversible drafts; `keeper_party_hat_put_on_back`, `keeper_carry_shopping` and `keeper_play_drums_back` also have second variants from the 12 October annotated review, respectively correcting frame-2 hand depth, frames-1/7 bag continuity with a synchronized loop endpoint, and frame-6 hands crossed behind the back. `keeper_put_record` has retained v2 masked-removal and v3 horizontal-held-record comparisons: v3 restores a level record between both hands in frame 5 while retaining the later removals. Thirteen newly rendered face-to-camera candidates were withdrawn on 12 October: twelve remain as rejected provenance, while the complete `keeper_count_money` amendment was explicitly deleted and the previous canonical version retained. Canonical production sprites remain unchanged pending explicit per-candidate promotion. The reviewer carries an exact-name Codex response for all 81 rows, including iterative requests for seated fishing, shower privacy/exit and the helter-skelter-dependent slide.
- Frank's original 14-pose darts source remains a separate byte-identical `keeper-darts-user-selected-2026-10-10-v1` visual comparison. The reviewer shows it beside canonical and explicitly marks the beard audit evidence gate; it is not a beard reference. `data/keeper_review_drafts.json` also records the ten selected canonical promotions, each with SHA-256-pinned prior-version evidence, seven active V11 artist-smock comparisons, and one active `keeper_snooker` complete-route comparison. V11 covers the full 15-asset family, while its eight neutral/bridge derivatives remain technical assets outside the 173-animation gallery. The accepted snooker route retains the canonical standard-uniform Keeper from walk through stop, cue acquisition, two strokes, release, turn and departure; production artist and snooker sprites remain unchanged pending review.
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
- `docs/KEEPER_ARTWORK_AUTHORING_AND_REVIEW_PLAYBOOK.md` — proven Keeper artwork recipe, continuity rules, rejected methods, accepted artist/snooker case studies, evidence checklist and exact-name review workflow.
- `scripts/keeper_review_handoff_monitor.py` and `scripts/install_keeper_review_handoff_monitor.sh` — independent macOS notification monitor and its per-user `launchd` installer; it reads the hand-back queue every four hours without opening Codex.
- `docs/prompts/KEEPER_SIDE_ON_BEARD_OCCLUSION_AUDIT.md` — first-stage ready-to-paste audit/fix prompt for beard, hand and arm layer order across every side-on standing and sitting animation.
- `docs/prompts/KEEPER_SPRITE_FRAME_ISOLATION_AUDIT.md` — second-stage ready-to-paste exhaustive audit/fix prompt for frame overlap and future enforcement.
- `docs/prompts/KEEPER_POST_AUDIT_REVIEW_DELTA.md` — ready-to-paste exact-name, JSON-ingestion prompt for Frank's next review after all three audits.
- `docs/prompts/KEEPER_RELEASE_SURFACE_DATUM_AUDIT.md` — third-stage ready-to-paste audit prompt for consistent tabletop release height and prop hand-off.
- `docs/prompts/KEEPER_REVIEW_WORKBENCH_BUILD.md` — ready-to-paste separate build prompt for the project-specific next stage of the reviewer: rooms, furniture, annotations, crop proposals, routines, triggers and context preview, with later generic productisation deliberately deferred.
- `docs/KEEPER_ASSET_SCALE.md` — human-readable keeper measurements and the rules for sizing/placing objects.
- `data/keeper_asset_contract.json` — authoritative machine-readable scale, pivots and interaction points.
- `data/keeper_pose_registry.json`, `data/keeper_endpoint_audit.json` and `data/keeper_endpoint_exceptions.json` — shared pose vocabulary, current real-pixel endpoint evidence, and the frozen legacy migration boundary.
- `data/keeper_object_dimensions.json` and `docs/KEEPER_OBJECT_DIMENSIONS.md` — keeper-derived furniture, fixture and station dimensions.
- `public/keeper-review/index.html` — canonical online-only reviewer deployed at `/keeper-review/`; `docs/keeper-scale-audit/review.html` is the generated audit artifact and must be byte-identical, but when opened outside `/keeper-review` it sends the viewer to the live platform instead of presenting a second workspace. Its gallery is a compact visual scan (name, review state, last local save/redraft, playback and frame stepping); `Open close review` opens any chosen card immediately. `Find animation` searches names and overrides all other filters; otherwise independently filter by review state, pose and active/reserve use list. Close review lets Frank override the inferred pose tag, relegate a likely duplicate to the reversible reserve list, expand/compress retained draft comparisons, and select canonical or every exact-name draft as an exportable preferred-promotion candidate—without mutating production. **Hand back to Codex** always asks for confirmation, saves any unsaved cards to that browser if confirmed, then submits the full batch to the durable server-side queue. The server records a semantic exact-name delta (ignoring save timestamps), comparing the first server hand-back to the shipped review baseline and later ones to the prior hand-back; the receipt reports only the changed animation count for later Codex work. When Codex claims a batch, the online reviewer becomes read-only until the delivery is completed, while retaining playback and inspection; JSON backup/import is collapsed as an exceptional browser-recovery option.
- `data/keeper_side_on_beard_occlusion_audit.json`, `art/drafts/keeper-side-on-beard-occlusion-2026-10-10-v2/`, and `art/drafts/keeper-side-on-beard-occlusion-2026-10-10-v1/` — completed draft-only v2 beard/hand audit and preserved rejected v1 history. The active reviewer shows v2 beside canonical and the separate Frank-selected darts draft; the verifier prevents implicit promotion.
- `data/keeper_review_drafts.json` and `art/drafts/` — SHA-256-pinned, exact-name review comparisons: the draft-only darts candidate, seven active V11 artist-smock candidates, the accepted complete-route `keeper_snooker` candidate, the 41 exact-name 11 October amendment candidates and the separate party-hat frame-2 v2 variant, plus the ten selected canonical promotions and their reversible previous versions. Hash-addressed reviewer copies prevent same-name historical and current variants from overwriting one another. `scripts/verify_keeper_review_drafts.ts` checks every registered source, canonical/current comparison, sidecar, gutter, publication and reviewer attachment.
- `docs/keeper-scale-audit/` — all-sheet/all-frame metrics, CSV register and nine printable contact sheets; rebuild every output, including the viewer, with the bundled Python runtime and `scripts/audit_keeper_scale.py`.
- `docs/DOORS_STAIRS_AND_COSTUMES.md` — agreed stairway, door and costume-change rules, seamless clip joins, and the decisions still to make.
- `docs/BACKGROUND_ELEMENTS.md` — Codex's brief for every background layer, sunrise and sunset, night lighting, and the every-asset-can-be-upgraded rule for objects.
- `docs/AMBIENCE_AND_BACKDROP.md` — backdrop layers, weather overlays, ambient sound, the lamp's start-up, audio file specs and the decisions still to make.
- `docs/CLAUDE_WORKBENCH_NOTES.md` — Claude's plan of approach for the shared review workbench (the next major build).
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

Last verified on 12 October 2026:

```sh
npm test
npm run typecheck
npm run build
```

The verification commands above cover the game and sprite pipeline; `npm test` begins with the keeper contract check. Keeper-scale verification additionally runs `scripts/audit_keeper_scale.py` and `scripts/verify_floor_asset_catalogue.py`; finished asset work is committed directly to the repository's main branch.
