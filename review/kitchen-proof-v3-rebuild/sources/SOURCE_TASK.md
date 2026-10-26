# Codex task — Kitchen v3 rebuild (Frank, 26 Oct 2026)

CONFIRMED: your style calibration is the right artistic direction (Frank, 26 Oct). Substantial designed objects, organic black ink, bevelled panels and real material weight, warm restrained modelling, dense purposeful appliance detail, adult-playful ligne claire: keep all of it. Agreed on your caveats: geometry must be re-snapped (this task), and the cast shadows were too aggressive. Decision (Frank, 26 Oct): NO SHADOWS IN THE GAME. No cast shadows on walls, no floor or contact shadows, under items or the keeper (they would look wrong with the keeper walking through them). Shading inside an object (its one shadow tone, bevels, modelling) stays. Proceed to modularise.

Authority: `docs/SPEC.md` (v2.1, the shared working spec; git pull and read it first) plus this brief; where they differ, this brief wins. Create everything in a NEW versioned folder: /review/kitchen-proof-v3-rebuild/. Do not modify, move or overwrite any existing file, approved asset or hash-pinned document, including your style calibration. Report results to Frank and add a short note in section 19 of docs/SPEC.md.

## What Frank approved
Your style calibration is the approved LOOK: palette, ink, bevelled panels, layered edges, material weight, chunky worktop slab, shallow tops, floorboards, window frames, cooker, toaster, kettle, bin and bowl. Keep that look exactly, at the same level of detail. This task rebuilds it (1) as separate parts assembled in code and (2) snapped to the bay grid. Do not simplify or restyle anything.

## Changes from the calibration
1. The kitchen is on the FIRST floor. Remove the arched door on the back wall entirely. No room ever has a door on its back wall. The walk-in area (x 32–328) is plain back wall and floor; a small wall clock at about y 150 is allowed.
2. Circulation door: left wall, at the front, seen ONLY as a proper wooden jamb (frame edge and architrave in the door's timber colour, no black void), x 0–32, y 208–544.
3. Every unit is exactly 84 px (1 bay) or 168 px (2 bays) wide and sits in its bays (layout below).
4. The cooker is a 1-bay slot-in (84 px), redrawn narrower in exactly the calibration's style: own blue hob top with two hotplates, copper dials and handle, red indicator, oven window, blue plinth.
5. Windows: outer frame including the sill ledge exactly 168 × 168 at x 580–748 and x 1084–1252, y 106–274; glass inside the frame, exact #FF00FF.
6. Remove every cast, wall, floor and contact shadow. Shading inside objects stays.
7. Every unit's plinth bottom on y 485.

## Style (unchanged from the calibration)
Ligne claire per V7 (style reference only; never placed in the game): strong organic near-black ink matched to the keeper's outline at 1:1; flat fills with warm restrained modelling; bevelled panels and layered edges; plain line-work details; glows only in light overlays. Light from the upper left. Royal-blue units, cyan worktop, cream enamel, copper handles and knobs.

## Projection (as the calibration)
Front faces are flat true elevations. Object tops show 1/6 of real depth, drawn straight up (0.60 m deep → 17 px). Round things on tops (hotplates, sink bowl, rims) are ellipses about 1/3 as tall as wide. Floor band fixed at 84 px. No vanishing points, side faces or angled walls. Scale 1 m = 168 px; widths quantised to 84 px bays (0.50 m).

## Module geometry (delivered px, 1536 × 576, y from the top)
- Ceiling band y 0–32 (timber beam as in the calibration). Left wall x 0–32. Right wall x 1504–1536.
- Back wall y 32–460, skirting at its base. Floor band y 460–544, floorboards as horizontal lines. Slab y 544–576.
- Keeper walking line (soles) walkY 502.
- Walk-in zone x 32–328 clear. Door standing point x 118.
- Bays: 14 × 84 px, x 328–1504. Bay b spans x 328+84(b−1) to 328+84b. Centres: 370, 454, 538, 622, 706, 790, 874, 958, 1042, 1126, 1210, 1294, 1378, 1462.
- HARD RULE: nothing rises above y 274 inside x 580–748 or x 1084–1252.

## Kitchen layout (bay: item → keeper stop x)
- 1: tall blue utility cupboard (fittedTall, 0.50 × 0.60 × 2.00 m), door opens toward camera (closed + open overlay) → 370
- 2: cream fridge-freezer (fittedTall, 0.50 × 0.60 × 1.80 m) → 454
- 3: drawer unit (fitted) → 538
- 4–5: belfast sink cabinet (2 bays, fitted) + sink insert ON TOP of the worktop, bowl and taps over bay 4 (useBay 1) → 622
- 6: dishwasher (fitted) → 790
- 7: slot-in cooker, 1 bay → 874. Bays 7–8 are reserved for a later range cooker.
- 8: drawer unit (fitted) → 958
- 9: drawer unit; toaster on the worktop → 1042
- 10–11: cupboard fronts; worktop clear (under the right window)
- 12: cupboard unit; kettle on the worktop → 1294
- 13: pet bowl on the floor just in front of the units (behind walkY) → 1378
- 14: blue pedal bin, 0.30 m deep, against the back wall → 1462
- The kitchen has no end closet, so bays 13–14 are usable. Fitted runs: bays 3–6 and 8–12. End caps at x 496, 832, 916 and 1336.

## Vertical positions (match the calibration)
- Unit base y 485. Plinth y 468–485. Unit fronts y 336–468.
- Worktop: front-edge slab y 322–336; top reveal y 305–322. Counter items stand on y 314.
- Fridge-freezer: front y 183–485, top reveal y 166–183. Utility cupboard: front y 149–485, top reveal y 132–149.
- Cooker: own plinth y 468–485, front y 336–468, hob slab y 322–336, hob top y 305–322 (level with the worktop).
- Sink taps stay below y 274.

## Parts (separate files, each its exact declared size, assembled in code — never painted as one picture)
- Shell: room_shell_kitchen.png (back wall, skirting, floor, ceiling beam, side walls, jamb; windows with magenta glass; NO furniture, NO shadows of any kind).
- Run kit: worktop_tile.png (84 × 31), worktop_cap_left.png, worktop_cap_right.png (16 px), worktop_joint.png (2 px); plinth_tile.png (84 × 17), plinth_cap_left.png, plinth_cap_right.png.
- Fronts (84 or 168 wide, y 336–468, no worktop/plinth/outer edges): front_drawers.png, front_cupboard.png, front_cupboard_2bay.png, front_sink_belfast_2bay.png, front_dishwasher.png.
- Insert: insert_sink_2bay.png (bowl rim + taps, laid on a plain worktop tile).
- Slot-in: cooker.png (OFF: dark window).
- Tall: unit_utility_cupboard_closed.png, overlay_utility_cupboard_open.png, unit_fridge_freezer.png.
- Items: toaster.png, kettle.png, pet_bowl.png, pedal_bin.png.
- Light overlays: overlay_oven_window.png (cavity glow + loaf lit), overlay_dishwasher_led.png.
- item.json per item: realSizeM, bayWidth, useBay, fitted | fittedTall | slotIn | freestanding | counter, anchorPx, standPointX, lightOverlays, styleReference. room.json: walkY 502, bays, runs.

## Keeper check (no keeper art changes)
Composite the unchanged Prime Keeper (1:1, 298 px, sole datum frame y 316 on y 502) standing at the sink (x 622), the cooker (x 874) and the fridge (x 454), facing the back. Report the worktop edge height as a % of keeper height, and compare keeper and item ink weight. The full route proof follows in a later task once D15 is decided.

## Outputs and checks
- kitchen_v3_rebuild_room.png (1536 × 576, 1:1), a 2× nearest-neighbour copy, and a side-by-side with your style calibration at the same scale.
- Contact sheet of every part with file name and size.
- Verify and report: window glass is only exact #FF00FF with hard edges; nothing crosses y 274 in window bays; every part is its declared size and sits in its bays; worktops continuous across bays 3–6 and 8–12 with seams only at declared joints; cooker hob level with the worktop; no cut-outs; overlays change pixels only inside their rectangles; no cast, wall, floor or contact shadow pixels anywhere.
- Isolation test: recolour only insert_sink_2bay.png's taps, re-assemble, and prove every other file is byte-identical and the room differs only inside the sink insert's rectangle.

Do not start any other room. Report results and anything physically inconsistent before polishing.
