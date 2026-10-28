# Room schematic method (Frank, 28 Oct 2026)

Every floor of the lighthouse is planned the same way, on the same shell, with the same standard pieces. A schematic is GEOMETRY ONLY: it fixes where things go and how big they are, never how they look.

Tool: the **Room Planner** artifact (https://claude.ai/artifact/KAvqrmWsYootZJLmEz22kL). Frank lays rooms out there by drag and drop; the planner enforces every rule below and exports the schematic JSON and PNG. It also holds every piece's upgrades, reference images, draft history and Frank's feedback. Codex reads the mirror in `docs/planner/`.

## 1. The shell (identical on every floor)
- Module 2048 × 576 px. 1 m = 168 px. Keeper stops at x = 370 + 84(n−1), n = 1–20.
- Back wall x 160–1888, y 32–460. Floor band y 460 (back wall) to 544 (front edge): 28 px per metre of depth, 3.0 m deep.
- Windows: x 622–790 and 1294–1462, y 106–274. Switchable per room (the lobby has none). No door on any back wall, ever.
- LEFT side-wall door: always present; leads to the stairs (in the lobby: the hallway with the stairs and the front door).
- RIGHT side-wall door: OPTIONAL per room: the cupboard of myriads, a WC, or none.

## 1a. Fixed shell + finishes
- The shell above is ONE drawing for every floor, painted once and never redrawn: ceiling edge, side walls, side doors, window frames, skirting, floor edge.
- Finishes are separate layers painted to the shell's fixed masks, in its perspective: floor (boards, lino, flagstones, carpet, tiles), walls (paint, whitewashed stone, panelling, wallpaper, tiles), ceiling (beams, plain). Each room picks one of each; changing them never touches the shell.

## 2. Clear walking lane — ABSOLUTE (Frank, 28 Oct)
- The side doors' width must never overlap the depth of any furniture. All furniture stands within 0.9 m of the back wall (front faces on y 485). Each side door is 1.0 m wide and spans 1.0–2.0 m out from the back wall (floor y 488–516), straddling the keeper's walking line (y 502).
- So the keeper comes out of the stair door and walks a straight, unimpeded line to the far side of the room. Nothing (furniture, upgrade, prop, open appliance door) ever stands in the doorway or the lane. Side doors open AWAY from the room.

## 3. Datums (exact, never ±)
Unit fronts y 485 · keeper soles y 502 · worktop surface y 326 (worktop reveal y 317–334, front edge 334–348) · hob level with the worktop · stop centres · window rectangles · door positions · ceiling y 32.

## 4. Standard pieces
Floor pieces: width 1, 2 or 3 bays (1.0 / 2.0 / 3.0 m = 168 / 336 / 504 px) × one of five heights, snapped to the approved bays: 9 as standard, left edges on x = 286 + 168k (bays 1–9 = x 286–1798; the windows fill bays 3 and 7). The strips x 160–286 and 1798–1888 are wall only. A room can be given more bays (wider room: a bulge or widening, rare). When the right door is the cupboard of myriads, the wall strip beside its door (x 1798–1888) stays completely empty, wall pieces included.

| Height class | Height | px | Typical |
|---|---|---|---|
| Bench / bed | 0.5 m | 84 | bench, bed, sofa |
| Table | 0.76 m | 128 | table, desk, shoe station |
| Appliance | 0.9 m | 151 | washing machine, basin, tumble dryer |
| Worktop | 1.0 m | 168 | base units, sink (one continuous worktop per run) |
| Tall | 2.0 m | 336 | fridge, cooker, wardrobe, hat stand; may carry a counter at worktop height (dresser) |

Small props: floor prop 0.5 × 0.5 m (84 px); desktop S 44 × 36, M 64 × 60, L 84 × 84 px (stand on the surface beneath them); wall item S 60 × 60, M 100 × 90; shelf ×1 / ×2 (20 px deep); wall cupboard ×1 136 × 101 / ×2 304 × 101 at y 140–241; ceiling-hung ×2 336 × 110 at y 40–150.

## 5. Placement rules (the planner checks all of these)
1. Floor pieces never overlap.
2. Nothing covers a window, at any upgrade tier.
3. Desktop pieces stand on a unit, appliance, table or dresser counter and never hang off its edge.
4. Wall cupboards belong to the base unit or appliance below them.
5. Wall, ceiling and desktop pieces never overlap each other or the floor pieces.
6. Chunky rule: nothing narrower than 1.0 m except small props; nothing taller than twice its width.
7. Upgrades grow up, never out: reserved space rises from the piece to at most twice its width, never into a window.

## 6. Procedure
1. Frank lays out the room in the Room Planner (or asks Claude to draft it there).
2. Claude reads the saved room, checks it against this method and the spec, and files it as `docs/layout/<room>_vN_schematic.json` + `_1x.png`.
3. Frank approves the schematic (recorded in `docs/SPEC.md`).
4. Claude writes the Codex brief: paint the whole furnished room as ONE image using the schematic as the layout guide, then cut it into parts. Datums are exact; piece outlines are ±5%; never contain-and-pad a painting into a box.
