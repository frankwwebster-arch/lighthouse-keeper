# Lighthouse Keeper: notes for Claude

Project page (the record of every decision, and the user guide): https://claude.ai/artifact/Ehjz6SdSEvsDYLTLWuKZP4. Read it with the Artifact tool, and re-read it before every republish.

- **Stack:** Next.js 14 (App Router), React 18, TypeScript and Vitest, deployed on Vercel. Every push to `main` deploys to https://lighthouse-keeper-mu.vercel.app. Neon Postgres is optional (`DATABASE_URL`).
- **Run:** `npm install`, then `npm test`, `npm run typecheck` and `npm run build`. For a dev server use `DATABASE_URL= npx next dev -p 3123`, because `.env.local` points at the **live family database**.
- **Roles:** Codex owns art, animation and the review pages; Claude owns game logic, the recipe studio and tools. Never edit or promote Keeper art, review drafts, registers, manifests, the Workbench or Final animations. Pull before pushing, because Codex pushes to `main` too.
- **Key docs:** `docs/DECISIONS.md`, `docs/RECIPES.md`, `docs/CODEX_TO_CLAUDE_HANDOFF_2026-10-14.md` (the current shared boundary), `docs/CLAUDE_WORKBENCH_NOTES.md`, `docs/prompts/`.
- **Current task:** furniture placement and walking. Phase 1 (the plan) is done on branch `claude/furniture-locomotion`: `docs/architecture/FURNITURE_PLACEMENT_AND_LOCOMOTION.md`. Phase 2 (pure model and tests) waits for Frank's answers on the project page. Key finding: with today's walk data, no three standing spots on a floor can all be joined in whole steps; the plan asks Codex for re-timed start/stop numbers (42 ku each) and a stop off the other foot.
