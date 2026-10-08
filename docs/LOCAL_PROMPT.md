Paste this into Claude Code, run from your projects folder.

---
Clone https://github.com/frankwwebster-arch/lighthouse-keeper into ./lighthouse-keeper (if not already there), run `npm install`, `npm test`, `npm run build`, and `npm run dev`. Read README.md, docs/STATUS.md, docs/DECISIONS.md, docs/CODEX_HANDOFF.md and docs/V2_UPGRADES.md first.

Context: a Sims-style lighthouse keeper game for my sons Ralph (7) and Eddie (11). Next.js 14, TypeScript, Neon, Vercel. Live at https://lighthouse-keeper-mu.vercel.app. Pushing to `main` deploys, so ask me before pushing.

Working style: keep replies short and plain. For anything technical, go one step at a time. Tell me which model to pick if not default. Anything I need to paste elsewhere goes in a single copyable block.

Do next, in order, checking with me after each:
1. Copy `.env.example` to `.env.local` and ask me for `DATABASE_URL` (never commit it). Confirm saves work locally with Ralph and Eddie.
2. Build the pixel art pipeline (4px grid, striped tower, layered keeper puppet, object states standard/on/broken) using the Codex assets in `public/sprites` once I add them; vector fallbacks stay.
3. Build missions that unlock floors (aquarium, weather station, hidden lair, lift), furnished automatically.
4. Build tiered upgrades for existing objects, with admin price dials and gifting.
5. Add the telescope spotting mini game, then fishing and cooking.
Keep the game kid-friendly but not babyish (he plays Roblox and Minecraft). No live AI in the game.
---
