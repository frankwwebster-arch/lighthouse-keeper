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
Engine (seeded, deterministic, 63 tests), SVG cutaway scene with zoom camera, typo matcher, quizzes levels 1-3, credit economy with admin dials (allowance from per-need green bars, prices, gifting, quiz level and breakdown pressure per player), who-is-playing screen, per-player saves (DB or localStorage), grown-ups PIN (starts 1234; change it).

The first three playable floors are now modular fixed-width components: kitchen, living room, and bedroom with en suite. Objects have a runtime `standard` / `on` / `broken` contract, state-specific strip support, shared broken effects, keyboard/touch hit areas, and rear-facing cooker/basin keeper fallbacks. Random keeper-owned breakdowns are off by default and controlled by grown-ups' frequency and maximum-concurrent dials; broken assets block normal use until repaired. Floor 3 reserves an invisible two-door changing zone for the later diving-board extension.

## Not built yet (agreed design)
1. Production Pixel PNGs: the 4px grid, exact sizes, names, pivots, floor modules and object-state strips are specified, but `public/sprites/manifest.json` is still empty and vector fallbacks remain in use.
2. Missions unlock floors (aquarium, weather station, hidden lair, lift). Floors arrive furnished; no furniture shop.
3. Tiered upgrades to existing objects bought with credits; prices are admin dials; gifting.
4. Mini games: fishing, cooking, telescope spotting.
5. Day/night palette, non-skippable ~30s night recap.
6. Replace the temporary on-island shop fallback with an early off-island unlock and boat travel. Boat tiers: rowing boat, tug, speedboat. The external shop never breaks; the keeper's jetty and boat may.
7. Workshop floor that reduces breakdown pressure; tune its effect only after Ralph's playtesting shows whether faults are fun or irritating.

## Housekeeping for Frank
- Rotate the Neon password (it was pasted in chat), then update `DATABASE_URL` in Vercel and redeploy.
- Change the grown-ups PIN from 1234.
- Add Ralph and Eddie on the Who is playing screen (none exist yet).

## Verification and delivery

The delivered slice passed 63 tests, TypeScript checking, a production build, and headless Chromium checks at desktop and 1024 × 768 iPad sizes. The 8 October 2026 Vercel deployment from `main` completed successfully; the live site returned HTTP 200 and its loaded bundle was checked for the three floors, breakdown dials, repair action, and shop exclusion.
