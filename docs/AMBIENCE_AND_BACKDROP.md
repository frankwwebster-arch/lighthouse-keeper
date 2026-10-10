# Ambience and the backdrop

Date: 10 October 2026
Status: design and production instructions. **Nothing here is built yet.** Written for Codex (backdrop art), for whoever supplies the audio, and for later Claude sessions (the code). Frank asked for ambient sound (a gentle seascape and changing weather) to be planned as part of the backdrop build, so the picture and the sound are designed from one list.

Related: the backdrop layers in `HANDOFF_TO_CLAUDE.md` §4.12–13, the weather design in `docs/EXPANSION_DESIGN.md` ("Weather and gameplay"), sound cues and the sound library in `docs/RECIPES.md`.

## 1. Principles

1. **Everything you see moving outside has a sound, and every ambient sound has something to see.** The calm sea animation and the calm sea loop are one item, delivered and named together.
2. **Picture and sound read the same weather.** One weather value in the game drives both. A change of weather fades the picture and the sound over the same time, from the same progress value.
3. **Gentle by default.** The boys may play for an hour, so the soundscape is soft, slow and never tiring. Only thunder is allowed to be sudden, and even that is capped in loudness.
4. **Ambience adds atmosphere, never information the player needs.** Anything that matters (a visitor knocking, the ship's horn, a breakdown) is an event sound and is also shown on screen.
5. **Indoors is dry.** The tower is a cutaway, so rain, snow and fog are never drawn inside a room. Indoors the weather is heard muffled and seen only through windows.

## 2. Shared names

Art, audio and code use these keys. Add a new key here before using it anywhere.

**Weather** (matching `EXPANSION_DESIGN.md`):

| Key | Meaning |
|---|---|
| `calm` | still air, flat sea |
| `sunny` | clear, light breeze, gentle sea |
| `windy` | strong wind, choppy sea |
| `light_rain` | drizzle, grey sky |
| `heavy_rain` | downpour, rough sea |
| `storm` | heavy rain, gale, lightning and thunder (today's game "storm") |
| `fog` | low visibility, flat grey, foghorn |
| `snow` | falling snow, muffled, cold |
| `heatwave` | hot still air, shimmer |

**Time of day**, from the game clock: `dawn`, `day`, `dusk` and `night`. These already drive the colour tint: dawn warm overlay, dusk purple, night deep blue, with the lamp beam drawn above the night tint.

**Where the camera is**:

| Key | When |
|---|---|
| `overview` | whole tower in view |
| `room` | zoomed into a room |
| `outside` | zoomed on the garden, jetty or shore |
| `lamp` | zoomed into the lamp room |

**Sea state** follows the weather: `calm` (calm, fog, snow, heatwave), `choppy` (sunny, windy, light rain) or `rough` (heavy rain, storm).

## 3. The backdrop, layer by layer, with its sound

Back to front. The keeper and the tower sit between the island layers and the foreground.

| Layer | Shows | Changes with weather | Changes with time | Sound partner |
|---|---|---|---|---|
| `bg_sky` | sky gradient | `clear`, `grey`, `storm` versions | tint overlay (§2) | none |
| `bg_clouds` | drifting clouds | sets: `clear`, `scattered`, `overcast`, `storm`; drift speed set by wind | tint | wind bed (speed and loudness together) |
| `bg_distant_village` | the far shore, a telescope target | hidden in `fog`; window lights at night | lights on at dusk | optional church bell on the hour |
| `bg_sea` | the sea, animated | strips `bg_sea_calm`, `bg_sea_choppy`, `bg_sea_rough` | tint; moon glints at night | sea bed of the same state |
| `fx_shore_foam` | foam breaking on the rocks | larger and more often when rough | tint | wave-crash one-shot, cued on the foam frame |
| `bg_island_back` / `bg_terrain` | rocks, grass, soil | grass sway by wind; `snow` cover version | tint | wind, gulls |
| `bg_lighthouse_shell` | the tower's outside | wet sheen in rain (optional); snow on ledges | lamp beam at night (exists) | lamp hum in the lamp room |
| weather overlays | rain, snow, fog, lightning, heat shimmer | per weather (§4) | tint | rain, snow hush, foghorn, thunder |
| `bg_foreground` | foreground plants and fence | sway by wind | tint | none |

Rules for the moving art:

- Movement is in whole pixels, with no blur and no smooth rotation (the nearest-neighbour 4× rule).
- Drift and parallax are whole-pixel steps every few frames, not fractional speeds.
- Fog and heat shimmer use a few stepped transparency levels or dithering in the game's palette. Never soft blur.

## 3a. The great lamp

The lamp is the lighthouse's showpiece, so it never just switches on. When the keeper lights it (the existing "Light the lamp" job, which gives the `lamp_lit` happening), it takes a couple of beats to warm up and get turning, and the whole sequence has its own sounds. It is the one big animation every evening.

**Lighting it**, in real seconds (all to tune):

| Beat | What you see | What you hear |
|---|---|---|
| 0 | The keeper's switch or match clip; a small spark at the burner | `sfx_lamp_ignite` (a click and a soft whump) |
| 0–1.5 s | A glow builds in the lens in stepped brightness frames: a dim ember, then warm, then bright. A brief flicker as it catches. | `sfx_lamp_warm` (a rising hiss for the oil lamp, a rising hum for the electric one) |
| 1.5–3 s | The lens starts to turn, slowly at first, then up to speed | `sfx_lamp_windup` (clockwork or motor starting); the turning sound speeds up with it |
| 3 s on | Full beam, sweeping steadily across sky and sea | `amb_lamp_turn` (a gentle, steady tick-whirr loop) under `amb_lamp_hum` |

**Putting it out** (`lamp_out`, or burnt out): the beam fades in steps, the lens slows and stops, and the glow sinks back to an ember (`sfx_lamp_wind_down`, then `sfx_lamp_fizzle`).

**Broken** (the lamp is already a breakable object): the shared wobble, smoke and sparks, plus a stuttering glow that won't settle and a lens that jerks rather than turns.

**Art (Codex):**

| Item | Files | Notes |
|---|---|---|
| Lens glow | `obj_lamp_warm_f<n>` | the warm-up steps, ember to full |
| Lens turning | `obj_lamp_turn_f<n>` | one turning loop, at least 8 hand-drawn positions (16 if it looks jerky); never a smooth raster rotation |
| Beam | `fx_lamp_beam_f<n>` | the sweep across the sky, drawn above the night tint as already planned; at least 8 frames to match the lens loop |
| Start and stop strips | `obj_lamp_start_f<n>`, `obj_lamp_stop_f<n>` | if the hand-over from glow to turning needs its own frames |
| Each upgrade tier | `obj_lamp_t2_…`, `obj_lamp_t3_…` | its own glow, turn and sound for each tier in the upgrade list: oil lamp (warm flame, slow), electric lamp (whiter, quicker start), Mega beam (the grandest start-up and the brightest beam) |

- **Speeding up and slowing down** is done by stepping the loop's frame rate up and down (for example 2, 4, 6, then 8 fps), not by blurring. The beam frames follow the lens frames exactly, so the beam always points where the lens does.
- **The beam shows the lamp's shine.** The game already tracks shine (polishing raises it, every night dulls it), so a dull lamp gives a visibly weaker beam and a polished one a bright, crisp beam. A real reason to polish, shown rather than told. The Mega beam never needs polishing, so its beam is always at full strength.
- **Fog** shows the beam as a solid shaft; on a clear night it is a lighter sweep. By day the lamp is normally off; if it is lit early, the beam is faint.
- **When you hear it:** in the lamp room the lamp sounds are close and full. Elsewhere you hear only a faint tick, or nothing. From the overview you see the beam but hear the sea.

The start-up is a sequence of object animations with sound cues. The recipe studio can preview it as an object sequence once lamp art exists, so its timing can be tuned by eye and ear like a keeper recipe.

## 4. Weather overlays (Codex)

| Overlay | Files | Notes |
|---|---|---|
| Rain | `fx_rain_light_f<n>`, `fx_rain_heavy_f<n>` | Tileable strips. Masked out of the cutaway rooms, so it falls only outside the tower. |
| Rain on windows | `fx_window_rain_f<n>` | Small strip for room windows, so indoor rooms show the weather (only where room plates have windows). |
| Snow | `fx_snow_f<n>` | Tileable, slow. Also `bg_terrain_snow` and snow on the shell's ledges. |
| Fog | `bg_fog_far`, `bg_fog_near` | Far bank behind the tower and in front of the sea; thin near band in front of the island. Hides the village. The lamp beam stays visible through it. |
| Lightning | `fx_lightning_f<n>` | A short full-frame flash and a bolt sprite. Thunder follows after a delay (§6). |
| Heat shimmer | `fx_heat_f<n>` | Subtle, stepped, low over the land. |

Each animated sheet gets the usual sidecar (frames, fps, anchor), plus:
- `weather`: the keys it belongs to;
- `sfxCues` where a frame should make a sound, such as the foam frame that should crash.

The same format as the keeper sheets (`docs/RECIPES.md`) means one sound library serves everything.

## 5. The soundscape

### Beds: continuous loops

| Bed | Plays in | Notes |
|---|---|---|
| `amb_sea_calm`, `amb_sea_choppy`, `amb_sea_rough` | by sea state | the core of the soundscape; stereo, panned towards the sea (§6) |
| `amb_wind_light`, `amb_wind_strong`, `amb_wind_gale` | by weather | louder higher up the tower |
| `amb_rain_light`, `amb_rain_heavy` | rain and storm | outside only |
| `amb_rain_window` | rain, when zoomed into a room | rain on glass and roof |
| `amb_snow_hush` | snow | a very soft, muffled bed |
| `amb_room_tone` | when zoomed into a room | a near-silent indoor hush that the outside fades into |
| `amb_lamp_hum` | the lamp room, while the lamp is lit | |
| `amb_lamp_turn` | the lamp room, while the lens turns | the turning mechanism's steady tick-whirr (§3a) |
| `amb_night` | night | the night version of the shore: sea lower, the odd night bird |

### Scattered one-shots

Random gaps between plays, at least three variants each, each played at a slightly different pitch.

| Sound | When | Roughly how often (real seconds) |
|---|---|---|
| `sfx_gull_<n>` | day; fewer in rain and wind, none at night or in fog | every 15–40 s |
| `sfx_wave_crash_<n>` | always; more when rough; also cued by `fx_shore_foam` | every 8–20 s |
| `sfx_buoy_bell_<n>` | calm, sunny, fog | every 30–60 s |
| `sfx_foghorn` | fog | every 40–70 s |
| `sfx_thunder_far_<n>` | storm, between the game's own thunder | every 25–60 s |
| `sfx_church_bell` | optional, on the hour, day only | hourly |
| `sfx_dawn_gulls` | once, at dawn | |

### Event sounds the game already signals

The engine already records these happenings, so each needs a sound name. They live in the same library and appear there as placeholders until a file is added.

| Game happening | Sound |
|---|---|
| `thunder` | `sfx_thunder_near_<n>`, after the lightning flash |
| `storm` (it begins) | `sfx_wind_gust_rise` |
| `horn` | `sfx_ship_horn` |
| `lamp_lit` / `lamp_out` | the lighting sequence (§3a: `sfx_lamp_ignite`, `sfx_lamp_warm`, `sfx_lamp_windup`) / `sfx_lamp_wind_down`, `sfx_lamp_fizzle` |
| `caller`, `pizza_arrived` | `sfx_door_knock_<n>` |
| `ring` | `sfx_phone_ring` |
| `breakdown` | the four existing categories: `sfx_electronic_fizzle`, `sfx_mechanical_clunk`, `sfx_plumbing_sputter`, `sfx_structure_crack` |
| `repaired`, `upgraded` | `sfx_repair_done`, `sfx_upgrade` |
| `mission_done`, `unlocked` | `sfx_fanfare_small`, `sfx_floor_reveal` |
| `bought`, `credits` | `sfx_till`, `sfx_coins` |
| `quiz` right / wrong | `sfx_quiz_right`, `sfx_quiz_wrong` (gentle) |

## 6. The mix

All of this is data, so it can be tuned without code (§9). Starting values follow; Frank will tune them by ear.

**Each weather sets bed loudness** (0 = off, 1 = full):

| Weather | sea | wind | rain | other |
|---|---|---|---|---|
| calm | calm 0.6 | light 0.15 | — | buoy bell |
| sunny | choppy 0.5 | light 0.3 | — | most gulls |
| windy | choppy 0.7 | strong 0.6 | — | few gulls |
| light_rain | choppy 0.5 | light 0.3 | light 0.5 | few gulls |
| heavy_rain | rough 0.6 | strong 0.4 | heavy 0.7 | no gulls |
| storm | rough 0.8 | gale 0.7 | heavy 0.8 | thunder |
| fog | calm 0.5 | light 0.1 | — | foghorn, buoy bell |
| snow | calm 0.4 | light 0.2 | — | snow hush 0.5 |
| heatwave | calm 0.5 | — | — | gulls, very still |

**Then adjustments:**

- **Time of day.** Night lowers everything by about a third, stops the gulls and adds `amb_night`. Dawn plays the gull chorus once.
- **Where the camera is.**
  - `overview`: everything as set.
  - `room`: the outside muffled (cut down to a dull low rumble, about half as loud), `amb_room_tone` added, plus `amb_rain_window` if raining.
  - `outside`: everything slightly louder, and the sea louder still near the jetty.
  - `lamp`: wind louder, `amb_lamp_hum` while lit.
- **Height.** The higher the floor in view, the more wind and the less sea. This follows the saved random floor order, so it works however the tower has grown.
- **Stereo.** The sea is to the right of the island and the village to the left, so beds pan with the camera's position.
- **Making room for events.** While an activity's own sounds or an event sound play, beds dip a little. During the night recap they dip further and stay soft.
- **Changing weather.** Fades over about 20 seconds, in step with the picture. Lightning is instant, and thunder follows a moment later: sooner and louder when the storm is close.
- **Players' controls.** Separate Ambience and Effects volume sliders and a mute switch in the Menu, remembered on each device.

## 7. Supplying the audio files

- **Beds:**
  - seamless loops of 30–45 seconds, cut at the waveform's zero points, with no fade at either end;
  - an even texture with no stand-out moments inside (distinctive sounds belong in the one-shots, otherwise the loop's repetition becomes obvious);
  - mono, except the sea, which can be stereo.
- **One-shots:** short, trimmed close, at least three variants each.
- **Format:** keep 44.1 kHz WAV masters, and deliver the game files as **AAC (`.m4a`) or MP3**, which every iPad plays. Avoid Ogg.
- **Loudness**, so nothing needs fixing in the mix:

  | Kind | Integrated loudness |
  |---|---|
  | Beds | about −30 LUFS |
  | One-shots | about −24 LUFS |
  | Event sounds | about −18 LUFS |

  Peaks below −1 dBTP in all cases.
- **Names:** exactly the keys above (`amb_sea_calm`, `sfx_gull_2`). Upload each file in the recipe studio's sound library under that name: the studio's library is the game's library, and a placeholder of that name is filled at once.
- **Size:** about 10 MB for all the ambience. Calm sea and light wind load first, the rest when needed.
- **Provenance:** record every file's source, author, licence and link in `data/audio_sources.csv`. Use only material we made or that is clearly licensed for use (CC0 or a paid licence that allows it), never sounds lifted from other games or videos.

## 8. How the game will do it (later, Claude)

- **A weather model.** Today the game knows only "storm". It needs a day's weather plan of states and changes, and a `weatherAt(game, clock)` answer, which also gives the weather station something to forecast. The art and the sound both read that one answer.
- **A sound engine.** Built on the same audio code as the studio. Three channels (ambience, effects, interface) under one master volume, with a low-pass filter on the ambience for the indoor muffle.
- **iPad rules:** sound starts on the first tap (iPad Safari requires that), pauses when the tab is hidden, and keeps decoded audio small (short mono beds, or streaming for the longest).
- **Event sounds** come from the happenings the engine already records; ambience comes from the weather, time, camera and height.

## 9. Tuning it: an ambience page in the studio (next to build)

A second page in the recipe studio:
- pick the weather, the time of day and where the camera is;
- see a backdrop stand-in (later the real layers);
- hear the mix;
- adjust each weather's bed volumes, one-shot rates and the adjustments in §6;
- trigger a weather change to judge the fade.

Saved the same way as recipes: drafts in `data/ambience.json`, Frank's edits in the database.

## 10. Decisions to make

| # | Decision | Options | Recommendation |
|---|---|---|---|
| 1 | Sound on or off when the game opens | on / off / remember the last choice | remember the last choice, starting on at a gentle level |
| 2 | Who supplies the audio | Frank finds or records it / commissioned / a sound library | Frank, using the names and specs above; Codex keeps to the art |
| 3 | First batch of weathers | all nine / a starter set | starter set: `calm`, `sunny`, `light_rain`, `storm`, `fog`. Then `windy`, `heavy_rain`, `snow`, `heatwave` |
| 4 | Music (theme tune, night-recap music) | now / later | later, as its own channel; the ambience must leave room for it |
| 5 | Church bell on the hour | yes / no | yes, soft, as a gentle sense of time passing |
| 6 | Lamp start-up length | about 3 s / longer and grander / shorter | about 3 s to full beam, tuned in the studio; it plays every evening, so it must stay a pleasure, not a wait |
| 7 | Who builds the ambience page | Claude next / after the game plays recipes | Claude, next after the animation review, so the backdrop art can be judged with its sound |
