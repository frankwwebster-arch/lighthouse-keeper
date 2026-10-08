# Lighthouse Keeper: status write-up (8 Oct 2026)

## What it is
A Sims-style web game for Ralph (7) and Eddie (11). A keeper lives in a lighthouse; kids type commands (typo-tolerant, curated, no live AI) or click objects (Sims-style menus, auto-zoom camera). Needs and mood, credits, phone, bedtime, multi-day play, a day report, quiz pop-ins, time-aware chat, cheeky humour.

## Where it lives
- Code: github.com/frankwwebster-arch/lighthouse-keeper (branch `main`).
- Live: **https://lighthouse-keeper-mu.vercel.app** (the one address to use and bookmark).
- Vercel project `lighthouse-keeper` (team frankwwebster-4308s-projects). Every push to `main` deploys to production.
- The long addresses like `lighthouse-keeper-di4axnjgx-...vercel.app` are one-off links for a single deploy. Ignore them; they are also login-protected.
- Database: Neon Postgres via `DATABASE_URL` (verified: `/api/players` answers `db:true`). Tables are created on first use: players, saves, player_rules, settings (PIN hash).

## Built
Engine (seeded, deterministic, 105 tests), SVG cutaway scene with zoom camera, typo matcher, quizzes levels 1-3, credit economy with admin dials (allowance from per-need green bars, prices, gifting, quiz level and breakdown pressure per player), who-is-playing screen, per-player saves (DB or localStorage), grown-ups PIN (starts 1234; change it).

The first three playable floors are now modular fixed-width components: kitchen, living room, and bedroom with en suite. Objects have a runtime `standard` / `on` / `broken` contract, state-specific strip support, shared broken effects, keyboard/touch hit areas, and rear-facing cooker/basin keeper fallbacks. Random keeper-owned breakdowns are off by default and controlled by grown-ups' frequency and maximum-concurrent dials; broken assets block normal use until repaired. Floor 3 reserves an invisible two-door changing zone for the later diving-board extension.

Missions currently unlock floors one at a time (`src/game/missions.ts`, list in `config.ts`): Fishy Business → aquarium, Storm Chaser → weather station, Strange Rumblings (secret until it starts) → hidden lair underground, Puffed Out → lift. Goals count things he already does (fishing, nature channel, telescope, ships kept safe, digging, visitors, quiz answers, good days). A finished mission pays credits (10 by default) and the floor arrives furnished (tank and fish food; weather instruments and radio; secret computer and gadget bench). The tower restacks itself (lamp room always on top, lair below ground) and the view zooms out to fit; the lift makes stairs quicker. 🎯 Mission button shows progress; grown-ups set an overall mission size (% of normal) and reward, then can override any single goal or reward, and can finish the current mission. Typing about a floor he has not got gets a hint. `?floors=all` previews every floor. New floors and furniture are stand-ins until Codex's art (hooks in docs/FOR_CODEX.md).

Upgrades: almost every object has Basic, Middle and Top tiers, listed in `data/upgrades.csv` (Frank's tracker page and Codex both work from it; `npm run upgrades` copies it into the game, and a test fails if the copy is stale). He buys the next tier from the object's tap menu with credits; a new one replaces a broken one. Each tier makes that object's jobs do more good (+25% / +50%) and take less time (−15% / −30%); the bed's tier sets the morning's energy (80 / 90 / 100%). Grown-ups set one price % for all upgrades, can override any single tier's price, and can give any next tier as a present. Tier art is a stand-in (`T2`/`T3` tag) until Codex's `obj_<id>_t<n>_<state>` sprites arrive; `?tiers=3` previews them.

**Known design mismatch:** that fixed mission chain, fixed future `FLOOR_LEVELS` order and fixed Floor 3 diving geometry are interim. Frank's locked direction is non-linear standard-floor progression with one-time random saved placement: kitchen at the base, lamp room topmost, bedroom directly beneath it, and other standard floors in random middle-stack positions. The bedroom's diving extension follows it upward. The underground lair and lift are special unlocks outside the standard stack. See `docs/EXPANSION_DESIGN.md`, `HANDOFF_TO_CLAUDE.md` and `docs/FOR_CODEX.md`; the next Claude logic pass must refactor this before more standard floors are added.

## Not built yet (agreed design)
1. Continue production Pixel PNGs after the completed first batch. `public/sprites/manifest.json` now maps two 110 × 8 shell bands and the three 105 × 35 implemented room plates. Keeper, object-state, effect, lamp-room, exterior and later-floor art still use vector fallbacks or remain unbuilt.
2. Art for the mission floors (aquarium, weather station, hidden lair), their furniture, the lift and a floor-arrival effect (Codex; hooks in docs/FOR_CODEX.md).
3. Tier art for upgrades (Codex; list in docs/FOR_CODEX.md). Typed commands for upgrading ("upgrade the TV") are not in yet; upgrades are bought from the tap menu.
4. Mini games: fishing, cooking, telescope spotting.
5. Day/night palette, non-skippable ~30s night recap.
6. Replace the temporary on-island shop fallback with an early off-island unlock and boat travel through an indoor water-filled boathouse/dry dock. Boat tiers: rowing boat, tug, speedboat. The external shop never breaks; the keeper's boathouse, jetty and boat may.
7. Workshop floor that reduces breakdown pressure; tune its effect only after Ralph's playtesting shows whether faults are fun or irritating.

## Housekeeping for Frank
- Change the grown-ups PIN from 1234.
- Add Ralph and Eddie on the Who is playing screen (none exist yet).

## Verification and delivery

The first production Pixel batch passed 73 tests, TypeScript checking, a production build, and a 1024 × 768 headless Chromium check with no console errors. The five PNGs were checked at exact source dimensions and hard alpha through `npm run sprites`; runtime rendering remains nearest-neighbour at 4× logical size. Commit `892873e` was deployed through the unchanged `main` → Vercel workflow: the live site returned HTTP 200, its sprite manifest exactly matched the five local entries, and the live kitchen plate was confirmed as a 105 × 35 RGBA PNG.
