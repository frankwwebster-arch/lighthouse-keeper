# Codex task — Kitchen v3 amendment: freestanding 1950s appliances (Frank, 26 Oct 2026)

Run this AFTER the Kitchen v3 rebuild (docs/prompts/KITCHEN_V3_REBUILD_2026-10-26.md) has been reported, as a new versioned draft (/review/kitchen-proof-v3-freestanding/). Everything in the rebuild brief stays in force except what is listed here. Keep the approved look and the 1950s feel of the assets you are already building. Because every part is its own file, only the files named below change; prove the rest are byte-identical.

## Decision (Frank, 26 Oct)
All appliances are FREESTANDING, with a 1950s character. Only the sink and cupboards remain a short fitted run. No shadows anywhere (unchanged).

## Changes
1. COOKER (bay 7, 1 bay, freestanding): a 1950s gas cooker, 0.50 × 0.60 × 1.50 m. Cream enamel body on short legs or a plinth, oven door with window, copper knobs on a front control strip, hob at worktop height (top y 305–322) with two or three gas burners drawn as ellipses, and rising from the back of the hob a splashback carrying an EYE-LEVEL GRILL compartment with a small hood/canopy, top at y 233. Blue enamel trim to tie it to the units. Body 76 px wide, centred in the bay, 4 px of wall showing either side, feet on y 485. Keeper stop x 874. Bays 7–8 stay reserved for a later range.
2. FRIDGE (bay 2, 1 bay, freestanding): a rounded 1950s fridge, 0.50 × 0.60 × 1.50 m, cream enamel, rounded top corners, single door with a chunky chrome or copper lever handle, small badge, short legs. Body 76 px wide, centred, feet on y 485, front y 233–485. Keeper stop x 454.
3. UTILITY CUPBOARD (bay 1): restyle as a freestanding larder cupboard (finished sides, 76 px body, centred); door still opens toward the camera.
4. DISHWASHER removed (washing-up happens at the sink). Bay 6 becomes front_drawers in the fitted run.
5. Fitted runs unchanged: bays 3–6 and 8–12, end caps at x 496, 832, 916 and 1336, so the cooker stands in its own gap between the runs.

## Files
- New: cooker_1950s.png (OFF: dark oven window, dark grill), fridge_1950s.png, overlay_fridge_open.png (door open, interior lit), overlay_grill_glow.png, overlay_burner_flames.png (small blue gas flames), unit_larder_cupboard_closed.png, overlay_larder_cupboard_open.png.
- Keep: overlay_oven_window.png (redrawn to fit the new oven door).
- Retired from the kitchen (files kept, not deleted): cooker.png, unit_fridge_freezer.png, front_dishwasher.png, overlay_dishwasher_led.png, the fitted utility cupboard files.
- item.json for each new item: placement freestanding, realSizeM, bayWidth 1, standPointX, lightOverlays.

## Checks
Re-assemble the room; prove every file not named above is byte-identical and the room differs only inside bays 1, 2, 6 and 7. Composite the Prime Keeper at the cooker and check the eye-level grill sits at about his eye level. Window rule, magenta and no-shadow checks as before. Report to Frank and note it in section 19 of docs/SPEC.md.
