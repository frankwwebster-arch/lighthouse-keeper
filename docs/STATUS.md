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
Engine (seeded, deterministic, 54 tests), SVG cutaway scene with zoom camera, typo matcher, quizzes levels 1-3, credit economy with admin dials (allowance from per-need green bars, prices, gifting, quiz level per player), who-is-playing screen, per-player saves (DB or localStorage), grown-ups PIN (starts 1234; change it).

## Not built yet (agreed design)
1. Pixel art direction (with Codex): 4px grid, red-and-white striped tower, layered keeper puppet, object states standard/on/broken, animation-ready. Sprite manifest `public/sprites/manifest.json` is empty; vector fallbacks are in use.
2. Missions unlock floors (aquarium, weather station, hidden lair, lift). Floors arrive furnished; no furniture shop.
3. Tiered upgrades to existing objects bought with credits; prices are admin dials; gifting.
4. Mini games: fishing, cooking, telescope spotting.
5. Day/night palette, non-skippable ~30s night recap.

## Housekeeping for Frank
- Rotate the Neon password (it was pasted in chat), then update `DATABASE_URL` in Vercel and redeploy.
- Change the grown-ups PIN from 1234.
- Add Ralph and Eddie on the Who is playing screen (none exist yet).

## Limits in the cloud session
Could not create GitHub repos, read/set Vercel env vars, or reach Neon from the sandbox. No linked computer, so files were not copied locally; clone from GitHub.
