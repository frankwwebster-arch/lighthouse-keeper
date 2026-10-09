# Notes for Codex from Claude (integration hooks)

Working split: Codex owns art, design and layout; Claude owns game logic and wiring. Ask for a code hook here or in HANDOFF_TO_CLAUDE.md.

## Doors, stairway and costumes (9 Oct 2026)

Frank has answered every open question; the full record is `docs/DOORS_STAIRS_AND_COSTUMES.md` (sections 2 and 9). What it asks of you:

- **Floors are 56 px floorboards to ceiling.** Set the floor/ceiling thickness, then that band height is fixed for every standard floor. Redraw the three room plates and the shell at the new height.
- **Stairway alongside the rooms; you pick the side.** Ladders first, then a spiral staircase (if it can look right), then the lift. How the lift arrives is yours, as part of the lighthouse growing left, right, up and down. The slide goes on the outside of the tower.
- **Doors** open as he enters, stay open during the activity and shut as he leaves; the frame must fully hide him (with hats, 48 px tall). Room doors never break.
- **Bedroom floor:** en suite only through the bedroom, a walk-in closet off the bedroom, and the toilet in its own cubicle (door shut only for a poo). Other loos follow the same format.
- **New clips:** a pyjama door-open for the en-suite door (morning), and a standing neutral frame for every outfit. Naps happen in an armchair, so the armchair is a new object.
- Yours to settle without Frank: lamp-room access (trapdoor and ladder suggested), the shared door design, splitting `privacy` from `outfit` in the manifest.

## Missions and new floors (updated 8 Oct 2026: any order)

The fixed mission chain is gone. Logic follows the locked layout in `docs/EXPANSION_DESIGN.md`:

- **Missions run side by side.** Every mission in `MISSIONS` (`src/game/config.ts`) is open at once and counts in parallel, so floors arrive in whatever order he finishes them. A mission may wait for a taller tower (`needsFloors`; the lift needs 5 floors above ground). Secret missions show as "???" until he makes a start. Logic: `src/game/missions.ts`.
- **Floors are built overnight.** Finishing a floor mission pays at once and queues the floor (`State.arriving`). Each morning `nextDay` builds the first queued floor (one a morning) and notes an `unlocked` happening (`id` = floor) right after `dawn`. That is the hook for your dawn reveal. The lift goes in at once (`unlocked`, `id: 'lift'`).
- **Tower order is saved.** `State.middle` is the middle stack, bottom to top. The kitchen is always at the bottom, the bedroom always last (directly under the lamp room). A new middle floor takes a seeded random place in `middle` once and keeps it. Underground floors (`UNDERGROUND`, now just the lair) hang below the kitchen. `towerOf(s)` gives `{ stack, below }`; `applyLayout(stack, below, lift)` in `src/game/world.ts` positions everything.
- Stripes: `LAYOUT.slot[floor]` is each floor's place from the ground (B1 = −1), and stripes are worked out from world Y, so moved floors keep the pattern.
- The diving extension (`DIVING_EXTENSION` in `floors.tsx`) now reads the bedroom's live height, so it rises with the bedroom.
- Floor modules: `UNLOCKABLE_FLOORS` in `src/ui/floors.tsx` (plain grey walls for now; yours to dress). Room plates `room_aquarium`, `room_weather`, `room_lair` are already looked up through the manifest, so they appear as soon as they exist.
- New clickable objects (`obj_<id>_<state>`): `tank`, `fishfood` (aquarium), `barometer`, `radio` (weather station), `console`, `gadgets` (lair). Their x positions in `OBJECTS` are guesses; move them. Until art exists they draw as dashed labelled boxes.
- Lift: travel logic only (faster up and down, behind the stairs at `STAIRS_X`), drawn as a faint dashed shaft stand-in (`.lift` in `Scene.tsx`).
- Preview: `?floors=all` shows every floor and the lift.
- Underground: day 1 shows nothing below the ground. The view grows downward only once the lair arrives.

Authoritative detail is in `HANDOFF_TO_CLAUDE.md` under **“Locked rule: future floor progression is non-linear”**. Geometry and art must never force mission order: all standard bands remain 110 × 35 logical pixels, the lamp room stays topmost, and stripes come from world Y.

The consolidated design backlog—including floor reveal, moving bedroom/diving board, weather, pool, boiler, transport, solar and proposed rooms—is `docs/EXPANSION_DESIGN.md`.

## Upgrade tiers: art request (8 Oct 2026)

Almost every object gets three tiers: Basic (what he starts with), Middle and Top. **The list is `data/upgrades.csv`**: one row per object per tier, with its name, price, what it does, the sprite name and three art-status columns. Frank edits names, prices and perks in his tracker page; Claude syncs that page and the CSV both ways. Please draw from the CSV and, as each sprite lands, set its `normal` / `working` / `broken` cell to `done` (`n/a` where a state is not needed, as for the door's working state). Do not change the `object`, `tier` or `sprite` columns without telling Claude: the game reads them.

- Columns: `room, object, tier, name, price, perk, sprite, normal, working, broken, notes`.
- States in the CSV map to the runtime names: normal = `standard`, working = `on`, broken = `broken`.
- File names: `<sprite>_<state>_f<frames>.png`, e.g. `obj_cooker_t2_on_f4.png`. Tier 1 has no tier suffix. Same footprint and bottom-centre anchor as tier 1 unless you tell me otherwise.
- Runtime lookup: `obj_<id>_t<n>_<state>`, `obj_<id>_t<n>`, then each lower tier, then tier 1. Until a tier sprite exists the game shows the lower tier's art with a small `T2`/`T3` text tag.
- Preview: `?tiers=3` shows every object at its top tier; `?tiers=tv:3,bed:2` picks them. Works with `?broken=`.
- Each object's `<g>` carries `data-tier` and a `tier-<n>` class. No upgrade-arrival effect yet; say if you want one (for example reusing `fx_floor_arrival_smoke`).
- `boat` rows are planned but not in the game yet.
