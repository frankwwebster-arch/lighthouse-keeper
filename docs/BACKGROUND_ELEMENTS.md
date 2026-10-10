# Background elements: art brief

Date: 10 October 2026
Status: first draft of the brief, for Codex. Nothing here is drawn yet. The keeper is the measuring stick for everything (`data/keeper_asset_contract.json`); this brief applies the same discipline to the world around him.

Read with:
- `docs/AMBIENCE_AND_BACKDROP.md`: the weather keys, the sound partner of each layer, the weather overlays and the great lamp's start-up;
- `docs/DOORS_STAIRS_AND_COSTUMES.md`: 56 px floors, the stairway alongside the rooms;
- `docs/RECIPES.md`: object types, variants and standing spots.

## 1. Ground rules

- **One logical pixel is four screen pixels**, nearest-neighbour only. Movement is in whole pixels; no blur, no smooth rotation, no fractional scrolling.
- **The keeper is 38 px tall.** Near things are at his scale. Far things are smaller and simpler: houses on the far shore are a few pixels, and ships on the horizon have a readable silhouette at telescope size. Every element states its scale relative to him in its sidecar notes.
- **The world grows, so nothing is one fixed picture.**
  - The tower gains floors upward (and downward with the lair), so the sky must keep going up without a seam.
  - The island grows left and right with expansions, so terrain must join and repeat.
  - The overview camera zooms out as the tower grows.

  Every layer is built from **tiles or modules** with a stated repeat, not from a single plate. The day-1 stage is 300 × 190 logical px, but the scene will be much bigger than that.
- **Time of day is a tint over the same art** (dawn warm, dusk purple, night deep blue; values in `HANDOFF_TO_CLAUDE.md` §4.13), plus the specific sunrise, sunset and night pieces in §4. There is no separate night version of every layer.
- **Every file gets a sidecar** as for the keeper: frames, fps, anchor, repeat (the tile size and direction), the `weather` keys it belongs to, and `sfxCues` where a frame should make a sound (a wave breaking).
- **Indoors is dry.** Weather layers are never drawn inside the cutaway rooms (`AMBIENCE_AND_BACKDROP.md` §1).

## 2. The layers, back to front

Sizes are proposals. Change them if the art needs it, but record the final numbers in the sidecar and here.

| Element | Files | Size and repeat | Frames | Changes with | Notes |
|---|---|---|---|---|---|
| Sky | `bg_sky_<clear\|grey\|storm>` | a horizon band plus a band that repeats upward | 1 | weather; time (tint and §4) | must extend upward for a tall tower |
| Stars | `bg_stars` | a tile that repeats in both directions | 2–3, slow twinkle | night only | fade in at dusk |
| Sun and moon | `bg_sun`, `bg_moon` | single sprites | 1 (sun), phases optional (moon) | time (§4) | moon phases later suit the observatory floor |
| Clouds | `bg_clouds_<clear\|scattered\|overcast\|storm>` | wide strips that repeat sideways | 1 each | weather; drift speed by wind | drift in whole-pixel steps |
| Far shore and village | `bg_far_shore` | a strip that repeats sideways, small scale | 1, plus a lights-on frame | fog hides it; lights at night | a telescope target |
| Horizon ships | `bg_ship_<kind>` | small sprites | 2–4 (bob) | time (lights at night) | telescope targets; the evening ship the lamp guides home is one of these |
| Sea | `bg_sea_<calm\|choppy\|rough>` | tileable sideways, horizon to shore | 4–8 each | weather (sea state) | sound partner: the sea bed of the same state |
| Glitter path | `fx_sea_glitter` | strip under the sun or moon | 4 | sunny days, moonlit nights | |
| Shore foam | `fx_shore_foam` | sprites at rocks and shore | 6–8 | rough = bigger and more often | `sfxCues` on the breaking frame |
| Rocks and reef | `bg_rocks` | modules | 1 | | the hazard the lamp warns ships off |
| Buoy | `bg_buoy` | small sprite | 4 (bob), plus a light blink at night | weather (bobs harder) | bell sound partner |
| Gulls | `fx_gull_fly`, `fx_gull_rest` | small sprites | 6 (flap), 2–4 (resting) | none at night or in fog; few in rain | call sounds |
| Back hills | `bg_island_back` | modules that join sideways | 1 | grass sway by wind (optional frames) | |
| Terrain | `ground_strip` and modules: grass top, soil, cliff to sea, beach, path | 300 × 30 strip (already in the brief), split into joinable modules | 1; grass sway optional | snow cover version | must join as the island grows |
| Underground | `bg_strata_<soil\|rock\|deep>` | tiles repeating down and sideways | 1 | | hidden until the lair is revealed |
| Lighthouse shell | `tower_stripe_*` (delivered), `tower_base`, `tower_lamproom`, `tower_roof`, `tower_window_<lit\|dark>` | per floor band | 1 | time (windows); weather (wet sheen, snow on ledges) | stripes come from world height |
| Foreground | `bg_foreground_<plants\|fence\|posts>` | modules | 1–4 (sway) | wind | sits in front of the island, never in front of the tower's rooms |

The **jetty, garden, shop and future boathouse are objects**, not background: the keeper uses them and they can be upgraded (§5). They follow the object rules even though they're outside.

## 3. Weather

The weather keys and overlays (rain, snow, fog, lightning, heat shimmer) are specified in `AMBIENCE_AND_BACKDROP.md` §2 and §4. Each layer above lists what changes with the weather. A weather change fades over about 20 seconds, art and sound together.

## 4. Times of day

### Sunset

Frank wants a real sunset, not just a tint.

- It runs through the game's evening: dusk is 17:30 and dark is 19:00, about 50 seconds of real play.
- The sky moves through a stepped sequence of gradients (about 8 keyframes): day blue → gold → orange and pink → purple → night blue. Never a smooth blend: each step is a palette change.
- The sun sinks in whole-pixel steps. Near the horizon it flattens in a few drawn steps, then slips below.
- Clouds catch the light from below: a lit-edge version of each cloud set for sunset.
- The glitter path on the sea turns from white to orange and fades.
- The shell's sunward side warms, then cools.
- Stars fade in at the end.

### Sunrise

A short sequence. It plays during the morning, when the tower opens and the new day starts (the dawn reveal in `EXPANSION_DESIGN.md`):

- stars fade;
- the horizon glows;
- the sun rises in steps, round once it is clear of the horizon;
- the sky passes through the dawn colours to day.

### Night

- **Moon and stars.** The moon's path is the same as the sun's but slower; phases come later.
- **The lighthouse at night, lit room by room.** No light art is needed: the game shades each room.
  - A room the keeper isn't in is dark.
  - **In the evening, a room's light comes on as he opens its door and goes off as the door closes behind him.** The stairway is always lit.
  - At bedtime the tower closes like a doll's house and only the bedroom window stays lit until the keeper's light clicks off (`EXPANSION_DESIGN.md`, "Bedroom, diving board and night ending").
  - For the art, this means two things. Room plates must still read when darkened, so don't rely on mid-greys that disappear under the night shade. And the closed tower needs `tower_window_lit` and `tower_window_dark` for each floor band.
- **The lamp beam** sweeps above the night tint. Its start-up sequence is in `AMBIENCE_AND_BACKDROP.md` §3a.

The recipe studio already previews this room lighting: tick "Evening" and the room stays dark until its door opens.

## 5. Every asset can be upgraded

Frank: assume **every** asset in the game can be upgraded. So:

- Anything the keeper owns or uses is an **object type** with **variants**, usually its upgrade tiers. That covers furniture, fixtures, the lamp, and outdoor things like the jetty, garden, boat, buoy and boathouse.
- **One set of keeper animations serves every variant.** Three ovens, one oven animation. A variant may be bigger or smaller, but it keeps the same keeper-facing contact heights (seat 11, worktop 19 …, as the object dimensions already require). It declares where his feet go to use it, so recipes adapt to its size.
- For each variant's sidecar, please record:
  - `category` (the game's object id, e.g. `cooker`) and `tier`;
  - the footprint the keeper can't walk through;
  - `layer`: `back` (against the back wall; he passes in front) or `front` (side wall or nearer the camera; opaque, drawn over him);
  - `solid`;
  - `keeperUsePoints`: `{ "<spot>": [x, y] }` in the canvas, with the facing for each spot (for example `use` for the oven, `seat` for the armchair).

  These match the object types the studio uses (`data/studio/categories/`). Until the studio reads them straight from the sidecars, Claude copies them across.
- **Draw tier 1 first.** Higher tiers can follow, but their contacts and spots must be fixed before the art, so recipes don't move.
- Pure scenery (sky, sea, far shore, clouds) isn't upgraded, but the island itself grows with expansions (§1).

## 6. Delivery order

1. Sky gradients, the time-of-day tint check, and the sunset and sunrise keyframes.
2. The three sea states and the shore foam.
3. Terrain modules and the back hills.
4. Cloud sets.
5. The far shore, horizon ships and gulls.
6. Night: stars, moon and tower windows.
7. Weather overlays, starter set first: `calm`, `sunny`, `light_rain`, `storm`, `fog`.
8. Underground strata.
9. Shell pieces (base, lamp room, roof) and the lamp sequence.

For each, provide contact sheets and GIF previews as for the keeper. The studio will get an ambience page to judge each layer with its sound (`AMBIENCE_AND_BACKDROP.md` §9).

## 7. Decisions for Frank

| # | Question | Options | Recommendation |
|---|---|---|---|
| 1 | Where the sun rises and sets | rises over the sea (right) and sets behind the far shore (left) / the other way round | rises over the sea during the morning reveal, sets behind the far shore, so the sea glitter shows at sunrise |
| 2 | Moon phases | now / with the observatory floor | with the observatory |
| 3 | Parallax as the camera moves | none / subtle | subtle: far layers move less than near ones when the camera pans or zooms |
| 4 | Grass and foreground sway | animated / still | animated with wind, at most 2–4 frames |
| 5 | Lit windows on the closed tower at night | yes / no | yes: the doll's-house night ending needs them |
