# Notes for Codex from Claude (integration hooks)

Working split: Codex owns art, design and layout; Claude owns game logic and wiring. Ask for a code hook here or in HANDOFF_TO_CLAUDE.md.

## Missions and new floors (8 Oct 2026)

> **Frank's locked design correction:** standard-floor progression must be non-linear. The current aquarium → weather station → hidden lair → lift mission chain is an interim implementation, not the approved final progression. Do not extend or treat that fixed chain as authoritative. Aquarium, weather station, Workshop, Radio Room and other eligible standard floors must be able to unlock in different mission-completion/player-choice orders. The underground lair and lift are special unlocks outside the standard stack.

Current implementation: `MISSIONS` in `src/game/config.ts` unlocks **aquarium**, **weather station**, **hidden lair** (a secret mission; underground), then the **lift**. Logic: `src/game/missions.ts`. Layout: `applyLayout` in `src/game/world.ts`. Claude's next mission-logic pass must replace the fixed chain for standard floors with an eligible-mission choice/set and persist the player's resulting standard-floor sequence.

- Floor ids and current places: `FLOOR_LEVELS` in config.ts (lair −1, ground 0, living 1, bedroom 2, aquarium 3, weather 4). This fixed mapping is also interim for future standard floors. The final layout must keep Day 1 fixed, then stack later standard floors in the player's saved unlock order, with each newly chosen floor immediately below the raised lamp room. Do not solve this by editing one global fixed order.
- Stripes: `LAYOUT.slot[floor]` is each floor's place from the ground (B1 = −1), used for the red/white parity in `floors.tsx`, so inserted floors keep the pattern.
- Floor modules: `UNLOCKABLE_FLOORS` in `src/ui/floors.tsx` (plain grey walls for now; yours to dress). `floorsOnShow()` lists what is unlocked.
- New clickable objects (sprite names follow the usual `obj_<id>_<state>`): `tank`, `fishfood` (aquarium), `barometer`, `radio` (weather station), `console`, `gadgets` (lair). Their x positions in `OBJECTS` (config.ts) are guesses; move them. Until art exists they draw as dashed labelled boxes.
- Room plates you may want: `room_aquarium`, `room_weather`, `room_lair` (not wired yet; say if you want me to wire room plates for all floors).
- Lift: travel logic only (faster up and down, behind the stairs at `STAIRS_X`). Drawn as a faint dashed shaft stand-in in `Scene.tsx` (`.lift`).
- Arrival: the engine notes an `unlocked` happening (`id` = floor). No arrival animation yet; tell me what hook you want (for example a class on the new floor module for a few seconds).
- Preview: `?floors=all` on the address shows every floor and the lift as if unlocked.
- Underground: day 1 shows nothing below the ground. The view grows downward only once the lair unlocks.

Authoritative detail is in `HANDOFF_TO_CLAUDE.md` under **“Locked rule: future floor progression is non-linear”**. Geometry and art must never force mission order: all standard bands remain 110 × 35 logical pixels, the lamp room stays topmost, and stripes come from world Y.
