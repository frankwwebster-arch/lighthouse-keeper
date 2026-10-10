# Lighthouse Keeper: status write-up (10 Oct 2026)

## What it is
A Sims-style web game for Ralph (7) and Eddie (11). A keeper lives in a lighthouse; kids type commands (typo-tolerant, curated, no live AI) or click objects (Sims-style menus, auto-zoom camera). Needs and mood, credits, phone, bedtime, multi-day play, a day report, quiz pop-ins, time-aware chat, cheeky humour.

## Where it lives
- Code: github.com/frankwwebster-arch/lighthouse-keeper (branch `main`).
- Live: **https://lighthouse-keeper-mu.vercel.app** (the one address to use and bookmark).
- Vercel project `lighthouse-keeper` (team frankwwebster-4308s-projects). Every push to `main` deploys to production.
- The long addresses like `lighthouse-keeper-di4axnjgx-...vercel.app` are one-off links for a single deploy. Ignore them; they are also login-protected.
- Database: Neon Postgres via `DATABASE_URL` (verified: `/api/players` answers `db:true`). Tables are created on first use: players, saves, player_rules, settings (PIN hash).

## Built
Engine (seeded, deterministic, 122 tests), SVG cutaway scene with zoom camera, typo matcher, quizzes levels 1-3, credit economy with admin dials (allowance from per-need green bars, prices, gifting, quiz level and breakdown pressure per player), who-is-playing screen, per-player saves (DB or localStorage), grown-ups PIN (starts 1234; change it).

The first three playable floors are now modular fixed-width components: kitchen, living room, and bedroom with en suite. Objects have a runtime `standard` / `on` / `broken` contract, state-specific strip support, shared broken effects, keyboard/touch hit areas, and rear-facing cooker/basin keeper fallbacks. Random keeper-owned breakdowns are off by default and controlled by grown-ups' frequency and maximum-concurrent dials; broken assets block normal use until repaired. Floor 3 reserves an invisible two-door changing zone for the later diving-board extension.

Missions (`src/game/missions.ts`, list in `config.ts`) are all open at once and count in parallel, so floors arrive in any order: Fishy Business → aquarium, Storm Chaser → weather station, Strange Rumblings (a mystery until he makes a start) → hidden lair underground, and Puffed Out → lift (opens once the tower has 5 floors). Goals count things he already does (fishing, nature channel, telescope, ships kept safe, digging, visitors, quiz answers, good days). A finished mission pays credits (10 by default) at once; its floor is built overnight and appears the next morning, furnished (one new floor a morning; the lift goes in at once). Each new floor takes a random middle place, saved for good: kitchen always at the bottom, bedroom always directly under the lamp room, lair below ground. The view zooms out to fit; the lift makes stairs quicker. 🎯 Mission button shows progress; grown-ups set an overall mission size (% of normal) and reward, then can override any single goal or reward, and can finish any open mission. Typing about a floor he has not got gets a hint. `?floors=all` previews every floor. New floors and furniture are stand-ins until Codex's art (hooks in docs/FOR_CODEX.md).

Upgrades: almost every object has Basic, Middle and Top tiers, listed in `data/upgrades.csv` (Frank's tracker page and Codex both work from it; `npm run upgrades` copies it into the game, and a test fails if the copy is stale). He buys the next tier from the object's tap menu with credits; a new one replaces a broken one. Each tier makes that object's jobs do more good (+25% / +50%) and take less time (−15% / −30%); the bed's tier sets the morning's energy (80 / 90 / 100%). Grown-ups set one price % for all upgrades, can override any single tier's price, and can give any next tier as a present. Tier art is a stand-in (`T2`/`T3` tag) until Codex's `obj_<id>_t<n>_<state>` sprites arrive; `?tiers=3` previews them.

The living-room nap now belongs to an upgradeable passive armchair: basic
armchair → rocking chair → Lazyboy-style recliner. All tiers retain the same
11 px seat contact, and passive furniture is excluded from breakdowns.

The recipe studio now consumes a checked keeper pose contract. The reviewed
191-sheet keeper source batch is unchanged as the visual-history denominator;
73 exact neutral stills and reusable bridge derivatives bring the working raw
inventory to 325 keeper sheets. Standard sample flows, four-facing standing
turns and the TV seated turn have exact neutral joins, approved outfit walks
have neutral-ended cycle/start/
stop derivatives, and every full-body sidecar has registered pose metadata.
The remaining 300 legacy endpoint repairs are measured from real RGBA pixels
and ordered in `docs/KEEPER_NEUTRAL_ENDPOINT_AUDIT.md`. `npm test` rejects new
or regressed endpoint failures against that frozen migration boundary.

**Still to do on floors:** the dawn reveal animation (Codex; the `unlocked` happening after `dawn` is the hook), furniture migration and the walking-distance bathroom rule from `docs/EXPANSION_DESIGN.md`. The diving extension now follows the bedroom's height but is not playable yet.

## Not built yet (agreed design)

Keeper review cards now also preview, save and export a proposed per-clip
runtime FPS. Accepted `animationFps` values belong in each animation's source
JSON sidecar and generated runtime manifest, not in the PNG sprite pixels.

1. Run the side-on beard/hand-occlusion audit in `docs/prompts/KEEPER_SIDE_ON_BEARD_OCCLUSION_AUDIT.md` first, then run the exhaustive sprite-frame isolation audit in `docs/prompts/KEEPER_SPRITE_FRAME_ISOLATION_AUDIT.md`.
2. Continue the neutral-endpoint repair queue in `docs/KEEPER_NEUTRAL_ENDPOINT_AUDIT.md`: standard outfit first, then one outfit at a time in `docs/KEEPER_COSTUME_ROUTE_AUDIT.md` order. The five studio samples are the early visual gate; the specialised hot-drink prop-state bridges are their remaining seam work. In parallel, Frank's immutable second visual review has 96 of 173 animations Happy, 68 Awaiting new draft review, 3 Review later and 6 Unreviewed. Frank's saved per-animation width and height remain final production art direction.
3. Art for the mission floors (aquarium, weather station, hidden lair), their furniture, the lift and a floor-arrival effect (Codex; hooks in docs/FOR_CODEX.md).
4. Tier art for upgrades (Codex; list in docs/FOR_CODEX.md). Typed commands for upgrading ("upgrade the TV") are not in yet; upgrades are bought from the tap menu.
5. Mini games: fishing, cooking, telescope spotting.
6. Day/night palette, non-skippable ~30s night recap.
7. Replace the temporary on-island shop fallback with an early off-island unlock and boat travel through an indoor water-filled boathouse/dry dock. Boat tiers: rowing boat, tug, speedboat. The external shop never breaks; the keeper's boathouse, jetty and boat may.
8. Workshop floor that reduces breakdown pressure; tune its effect only after Ralph's playtesting shows whether faults are fun or irritating.

## Housekeeping for Frank
- Change the grown-ups PIN from 1234.
- Add Ralph and Eddie on the Who is playing screen (none exist yet).

## Verification and delivery

The prior neutral-contract checkpoint at commit `e74b93b` passed all 149 project tests, TypeScript checking, the production build and its then-current sprite/audit checks. It was deployed on remote `main`, and the canonical Vercel home and `/studio` routes both returned HTTP 200 on 10 October 2026. The current keeper review audit has since advanced to 191 sheets / 1,475 frames; its delivery evidence is recorded in `docs/review/KEEPER_ANIMATION_SECOND_ROUND_DELTA_2026-10-10.md`.
