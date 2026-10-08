# Lighthouse Keeper — handoff decisions

Date: 2026-10-08

This note records the decisions made in the visual-design conversation so implementation can continue without relying on chat history.

## Visual direction

- Use the Pixel direction as the primary style.
- The game is flat, front-on 2D cutaway art, not isometric and not full 3D.
- Use a consistent 4 px logical pixel grid, crisp nearest-neighbour scaling, saturated colours, dark pixel outlines, and simple faces.
- The lighthouse is the visual anchor: classic alternating red-and-white exterior stripes.
- The keeper is the main animation challenge. He is assembled from reusable layered parts, with animation variety coming from a library of body-language clips and some rear-facing work poses. Cooking, brushing teeth, and similar actions can often show his back with small arm/body movements rather than requiring bespoke front-facing animation.

## Interior item states

Every clickable interior object uses one shared state contract:

- `standard`: static idle appearance.
- `on`: active/use state, animated.
- `broken`: faulty state, animated.

Broken objects share a visual grammar: gentle casing wobble, looping smoke, and occasional sparks. Add only a small object-specific cue when helpful. The Pixel TV test is in `style_b_pixel/obj_tv_states_sheet.png` with separate AI-generated state crops beside it.

## Lighthouse expansion

- Day 1 begins with four floors, bottom to top: kitchen, living room, bedroom with en suite, and lamp room.
- The lighthouse can expand upward and downward. It does not need to be realistic.
- The lamp room must always remain at the top.
- The main shaft tapers very gradually, if at all. The lamp room is inset and fixed-width, with a wraparound rail and outdoor walkway.
- New floors can slide into place or materialise in a large puff of smoke. Reuse one arrival animation for all new floors.
- New floors must continue the alternating exterior stripe pattern. Calculate stripe phase from world/floor position so inserted floors align automatically.
- Underground expansion should be a surprise. Day 1 must show ordinary grass, soil, and rock only—not an obvious empty basement, shaft, cave, or reserved development space. When the Batcave-style lair unlocks, reveal it by extending the underground surface downward.
- Once the lighthouse exceeds roughly six floors, unlock a lift so inter-floor travel does not become tedious.
- At maximum height, a possible late-game gag is the keeper parachuting from the lamp-room roof.

## Night / day transition

- At the end of the day, the lighthouse closes up completely.
- The camera zooms out to show the whole lighthouse while the keeper sleeps.
- Night lasts approximately 30 seconds and presents a carefully readable daily recap/statistics sequence. It is intentionally not skippable because it is part of the learning experience.
- Energy restoration depends on bed quality: basic 80%, upgraded 90%, master 100%.
- The background should support a reusable day/night treatment rather than requiring a wholly separate world layout.

## New mechanic

The telescope in the lamp room is a dedicated spotting mini-game. It should be treated as a future feature, not decorative furniture: telescope use can zoom the camera, present a scanning/search interaction, and reward spotting ships, visitors, weather events, wildlife, or other distant targets.

## Background asset

The current master concept is:

- `art/background/lighthouse_master_day_pixel.png`

It is designed as a crop-safe master plate: calm expandable sky above, a clean grass/soil/rock boundary below, and no visible underground promise. It contains the four starting floors, the inset fixed-width lamp room, outdoor walkway rail, garden, shop hut, jetty, and sea. The shop hut is now historical concept material only: the canonical shop will be off-island and reached by boat.

## Next implementation priorities

Completed in the first implementation slice:

- Fixed-width modular kitchen, living-room, and bedroom/en-suite runtime bands.
- Shared `standard` / `on` / `broken` object renderer, broken-effect grammar, and horizontal strip playback.
- Rear-facing fallback pose for cooker and basin work.
- Reserved hidden Floor 3 changing-room geometry; the later extension itself is not built.
- Browser verification at desktop and 1024 × 768 iPad sizes.

Next priorities:

1. Produce the exact first-batch PNGs in `docs/PRODUCTION_ASSET_KIT.md`, starting with the aligned 32 × 40 front/back keeper parts and one complete TV state set.
2. Replace the room/furniture fallbacks with 110 × 35 shell bands, 105 × 35 room plates, and separate clickable furniture.
3. Add a day/night palette or overlay system and the proper roughly 30-second recap.
4. Add a real damage/repair gameplay source for the already-renderable broken state.
5. Leave aquarium, weather station, lair, lift, pets, visitors, ship and weather art until the later batch is authorised.
