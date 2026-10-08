# Lighthouse Keeper

A Sims-style game for Ralph: tell the keeper what to do by typing or tapping objects, and keep him happy through the day.

## Run it
```
npm install
npm run dev      # Next.js 14; open http://localhost:3000 (or this computer’s address on the same wifi, for the iPad)
npm test         # 53 tests
npm run build    # production build
```
On an iPad: open the address in Safari, Share, Add to Home Screen for full screen.

## Where things are
- `src/game/` rules (config.ts has every number, commands.ts the command book and silly reactions, engine.ts the rules).
- `src/ui/` the screen. `docs/` questions for Frank, sprite list, V2 ideas, decisions.

## Stack
Next.js 14 (App Router), React 18, TypeScript, Vitest. No database yet: the game saves in the browser (localStorage). Supabase can be added later for cross-device saves. Deploy on Vercel (framework: Next.js, no environment variables needed).
