# Lighthouse Keeper

A Sims-style game for Ralph: tell the keeper what to do by typing or tapping objects, and keep him happy through the day.

## Run it
```
npm install
npm run dev      # then open the address it prints (works on iPad on the same wifi)
npm test         # 53 tests
npm run build    # production files in dist/
```
On an iPad: open the address in Safari, Share, Add to Home Screen for full screen.

## Where things are
- `src/game/` rules (config.ts has every number, commands.ts the command book and silly reactions, engine.ts the rules).
- `src/ui/` the screen. `docs/` questions for Frank, sprite list, V2 ideas, decisions.
