Paste this into Claude Code, run from your projects folder.

---
Clone https://github.com/frankwwebster-arch/lighthouse-keeper into ./lighthouse-keeper (if not already there), run `npm install`, `npm test`, `npm run build`, and `npm run dev`. Read README.md, HANDOFF_TO_CLAUDE.md, docs/CODEX_BRIEF.md, docs/PRODUCTION_ASSET_KIT.md, docs/STATUS.md and docs/DECISIONS.md first.

Context: a Sims-style lighthouse keeper game for my sons Ralph (7) and Eddie (11). Next.js 14, TypeScript, Neon, Vercel. Live at https://lighthouse-keeper-mu.vercel.app. Finished verified work must be pushed to `main`; preserve the existing Vercel deployment workflow.

Working style: keep replies short and plain. For anything technical, go one step at a time. Tell me which model to pick if not default. Anything I need to paste elsewhere goes in a single copyable block.

Do next, in order:
1. Produce and integrate only the first-batch Pixel PNGs in `docs/PRODUCTION_ASSET_KIT.md`; the modular floors, three-state renderer and strip pipeline already exist.
2. Confirm production saves with Ralph and Eddie after the Neon credential rotation; never commit `DATABASE_URL`.
3. Add the real damage/repair gameplay source for the already-renderable broken state.
4. Add the day/night palette and roughly 30-second recap.
5. Keep later floors, lift, pets, visitors, ship and weather art deferred until explicitly authorised.
Keep the game kid-friendly but not babyish (he plays Roblox and Minecraft). No live AI in the game. Do not slice the concept plates into sprites.
---
