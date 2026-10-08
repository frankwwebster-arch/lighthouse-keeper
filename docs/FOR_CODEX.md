# Notes for Codex from Claude (integration hooks)

Working split: Codex owns art, design and layout; Claude owns game logic and wiring. Ask for a code hook here or in HANDOFF_TO_CLAUDE.md.

## Missions and new floors (8 Oct 2026)

Missions (`MISSIONS` in `src/game/config.ts`) unlock, in order: **aquarium**, **weather station**, **hidden lair** (a secret mission; underground), then the **lift**. Logic: `src/game/missions.ts`. Layout: `applyLayout` in `src/game/world.ts`.

- Floor ids and places: `FLOOR_LEVELS` in config.ts (lair −1, ground 0, living 1, bedroom 2, aquarium 3, weather 4). Unlocked floors stack; locked ones take no space; the lamp room is always on top; the ground floor's boards never move (y 640). Change the levels if you want a different order.
- Stripes: `LAYOUT.slot[floor]` is each floor's place from the ground (B1 = −1), used for the red/white parity in `floors.tsx`, so inserted floors keep the pattern.
- Floor modules: `UNLOCKABLE_FLOORS` in `src/ui/floors.tsx` (plain grey walls for now; yours to dress). `floorsOnShow()` lists what is unlocked.
- New clickable objects (sprite names follow the usual `obj_<id>_<state>`): `tank`, `fishfood` (aquarium), `barometer`, `radio` (weather station), `console`, `gadgets` (lair). Their x positions in `OBJECTS` (config.ts) are guesses; move them. Until art exists they draw as dashed labelled boxes.
- Room plates you may want: `room_aquarium`, `room_weather`, `room_lair` (not wired yet; say if you want me to wire room plates for all floors).
- Lift: travel logic only (faster up and down, behind the stairs at `STAIRS_X`). Drawn as a faint dashed shaft stand-in in `Scene.tsx` (`.lift`).
- Arrival: the engine notes an `unlocked` happening (`id` = floor). No arrival animation yet; tell me what hook you want (for example a class on the new floor module for a few seconds).
- Preview: `?floors=all` on the address shows every floor and the lift as if unlocked.
- Underground: day 1 shows nothing below the ground. The view grows downward only once the lair unlocks.
