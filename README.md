# Lighthouse Keeper

A Sims-style lighthouse game for Ralph and Eddie: tell the keeper what to do by typing or tapping objects, then keep him happy through the day. The playable cutaway currently has a kitchen, living room, bedroom with en suite, and lamp room.

## Run it
```
npm install
npm run dev      # Next.js 14; open http://localhost:3000 (or this computer’s address on the same wifi, for the iPad)
npm test         # 72 tests
npm run build    # production build
npm run sprites  # snap Codex's PNGs in art/raw/ into public/sprites/ (docs/CODEX_ASSETS.md)
```
On an iPad: open the address in Safari, Share, Add to Home Screen for full screen.

## Current implementation

- Floors 1–3 are modular fixed-width components in `src/ui/floors.tsx`: kitchen, living room, and bedroom with en suite. The toilet and wash basin are both in the en suite.
- Every object renderer accepts `standard`, `on`, and `broken`; active gameplay drives `on`. Broken objects share integer-step casing wobble, smoke and sparks. Add `?broken=tv,cooker` (or `?broken=all`) to the URL for the internal art-state preview.
- Keeper-owned assets can now break during play, block their normal actions, and be repaired. Grown-ups control average fault frequency and maximum concurrent faults; defaults are off / one. Breakdown events expose placeholder SFX categories for later audio. The shop is excluded because it is not the keeper's asset.
- Cooker and basin work use a reusable rear-facing keeper fallback. Production keeper PNGs are not delivered yet.
- Sprite manifest entries may be old string paths or `{ "file", "frames", "fps" }` objects. Horizontal strips animate without CSS scaling or rotation.
- All SVG object targets work by touch, mouse, Enter and Space. At a 1024 × 768 iPad viewport, the first-three-floor targets were verified at a minimum 82 × 94 CSS px.

## Where things are

- `src/game/` — rules (`config.ts` has every number, `commands.ts` the command book and silly reactions, `engine.ts` the rules).
- `src/ui/floors.tsx` — fixed-width room definitions and reserved Floor 3 diving-extension geometry.
- `src/ui/art.tsx` and `src/ui/Sprite.tsx` — vector fallbacks, the three-state renderer, and production strip playback.
- `docs/PRODUCTION_ASSET_KIT.md` — exact Pixel filenames, dimensions, anchors, pivots, z-order, frame counts, fps, and delivery order.
- `art/manifest.json` and `art/asset_inventory.json` — facts about the concept/prototype image pack; these are not a production rig.

## Stack
Next.js 14 (App Router), React 18, TypeScript, Vitest. Neon Postgres (optional; falls back to browser localStorage). Deploy on Vercel; set `DATABASE_URL` (pooled) for Production.

## Players and the database
A "Who is playing?" screen lets each child have their own game and their own grown-ups' dials (allowance, prices, quiz difficulty). With `DATABASE_URL` set (Neon via Vercel's Storage tab) saves live in Postgres and follow the player to any device; the tables are created automatically on first use. With no `DATABASE_URL` everything stays in the browser. Grown-ups' PIN starts as 1234 (Menu, then Grown-ups), and is checked on the server when the database is on.


## More

`docs/STATUS.md` is the full write-up. `docs/CODEX_BRIEF.md` is the authoritative art brief. `HANDOFF_TO_CLAUDE.md` separates implemented runtime work from missing production artwork.

## Verification

Last verified on 8 October 2026:

```sh
npm test
npm run typecheck
npm run build
```

All 63 tests passed, the production build completed, and a headless Chromium pass covered desktop plus 1024 × 768 iPad layouts with no console errors. The resulting `main` deployment was also verified live at [lighthouse-keeper-mu.vercel.app](https://lighthouse-keeper-mu.vercel.app).
