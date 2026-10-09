# Lighthouse Keeper — first-three-floor production asset kit

Status: production specification. Delivery-order item 1 is complete for the two shell stripe bands and the kitchen, living-room, and bedroom/en-suite plates. All older PNGs remain concept/prototype references; do not cut sprites out of the scene plates. The modular keeper-part section below is retained as historical rig documentation only: Frank rejected those part images and `keeper_reference` as reviewable final art. Production animation, scale and object work now follows `data/keeper_asset_contract.json`, `data/keeper_object_dimensions.json` and `docs/keeper-scale-audit/`.

## Coordinate and export contract

- Author at one source pixel per logical pixel on a 300 × 190 logical stage. Runtime SVG coordinates are logical coordinates × 4 (`viewBox="0 0 1200 760"`). Use integers only.
- The gameplay core is fixed at 110 × 35 logical pixels per floor band (runtime 440 × 140). Room plates are exactly 105 × 35. Do not taper or rescale a floor.
- Future standard floors unlock non-linearly. Keep kitchen at the base, lamp room topmost and bedroom directly below it; give every other unlocked standard floor a one-time random saved position in the middle stack. Never encode a permanent height, taper-dependent width or stripe colour into a future room asset. Calculate stripes from world Y.
- Export transparent PNGs (or flat `#FF00FF` for the existing cleanup script) with nearest-neighbour sampling, no blur and no anti-aliasing.
- Object filename: `obj_<id>_<state>_f<frames>.png`. All equal-size frames are arranged left-to-right in one strip. Tier 1 has no tier suffix; later tiers use `_t2`, `_t3`, and so on before the state.
- `standard` is one frame; the first production pass uses four-frame `on` and `broken` loops at the fps below. The manifest stores `file`, `frames` and `fps`; the runtime already supports string entries for old stills and metadata entries for strips.
- Object origin is bottom-centre `(0,0)` at its floor contact. Keeper origin is between the boots. Effect and bubble origins are explicit manifest points, never inferred from transparent bounds.

## Keeper kit

Historical rig parts used a **32 × 40** transparent canvas. They are not final review art or a production-size authority. The approved side walk and anatomy contract provide the identity baseline; Frank's saved per-animation width and height provide the final production size.

| Part | Pivot | z-order | Required views |
|---|---:|---:|---|
| left arm | `(10,15)` shoulder | 10 rear / 80 front | front, back |
| left leg | `(13,25)` hip | 20 | front, back |
| torso | `(16,25)` hips | 30 | front, back |
| right leg | `(19,25)` hip | 40 | front, back |
| head | `(16,11)` neck | 50 | front happy/neutral/grumpy/asleep/open; back |
| beard | head-aligned | 60 | included in the head artwork |
| cap | head-aligned | 70 | included in the head artwork |
| right arm | `(22,15)` shoulder | 80 front / 10 rear | front, back |
| hand/held prop | per clip, wrist-aligned | 90 | pan, toothbrush, book, phone |
| foreground effect | clip manifest | 100 | steam, bubbles, notes, ZZZ |

Initial clips:

Every delivered multi-frame keeper clip uses the global 4fps baseline. The
table records that current authored value; accepted review choices may add a
per-clip override without changing the sprite strip.

| Clip | View | Frames · fps | Loop | Interaction point |
|---|---|---:|---|---|
| `idle` | front | 4 · 4 | yes | floor anchor |
| `walk` | front/side composite | 8 · 4 | yes | floor anchor; no sub-pixel travel |
| `turn_back` | front to back | 6 · 4 | no | reverse frames for `turn_front` |
| `work_back` | back | 8 · 4 | yes | hands `(16,21)`; generic domestic work |
| `reach_use` | front | 5 · 4 | no | hand to object use point |
| `cook_back` | back | 8 · 4 | yes | alias of `work_back`; hands `(16,21)` |
| `read` | front | 4 · 4 | yes | book pivot `(21,22)` |
| `sit_side` | side | 6 · 4 | no | seat `(16,29)`; mirror left; reverse to stand |
| `sit_front` | front | 6 · 4 | no | seat `(16,29)`; reverse to stand |
| `sit_back` | rear | 6 · 4 | no | canonical rear-sitting ghost; seat `(16,29)`; reverse to stand |
| `eat_seated` | side | 8 · 4 | yes | seat `(16,29)`; fork to mouth `(24,17)`; mirror left |
| `piano` | rear three-quarter | 8 · 4 | yes | seat `(16,29)`; hands `(24,20)` |
| `sleep` | front-derived | 4 · 4 | yes | bed contact `(16,31)` |
| `phone` | front | 4 · 4 | yes | handset pivot `(22,14)` |
| `brush_teeth_back` | back | 8 · 4 | yes | alias of `work_back`; hands `(16,21)` |
| `wash_back` | back | 8 · 4 | yes | alias of `work_back`; hands `(16,21)` |
| `urinate_back` | back | 6 · 4 | yes | discreet clothed pose; hands low `(16,27)` |
| `door_open_side` | side | 6 · 4 | no | handle `(25,20)`; mirror left; reverse to close |
| `door_open_side_pyjamas` | side | 6 · 4 | no | clean canonical light-blue pyjama redraw; side-door progression; same handle `(25,20)`; mirror left; reverse to close |
| `door_open_back` | back | 6 · 4 | no | handle `(24,20)`; mirror handle side; reverse to close |
| `ladder_climb` | back | 8 · 4 | yes | invisible rungs; reverse for descent |
| `stairs_up` | side | 8 · 4 | yes | high-knee ascent; mirror left |
| `stairs_down` | side | 8 · 4 | yes | balanced descent; mirror left |
| `switch_press_side` | side | 6 · 4 | no | fingertip `(27,17)`; mirror left; reverse to withdraw |
| `switch_press_back` | back | 6 · 4 | no | fingertip `(26,17)`; same height as side; mirror hand; reverse |
| `walk_into_lift` | rear to front | 8 · 4 | no | rearward depth walk; baked 100%→75% scale and 0→−6 px rise; finishes fully front-facing |
| `parachute_jump` | side | 9 · 4 | no | 48 × 84; pack opens and round canopy deploys |
| `platform_dive` | side | 10 · 4 | no | 48 × 56; ends vertical head-first; splash separate |
| `dig` | side | 8 · 4 | yes | spade contact `(27,38)`; mirror left |
| `feed_animals` | side | 8 · 4 | no | scoop/bowl target `(27,34)`; mirror left; includes rise |
| `sow_seeds` | side | 8 · 4 | yes | scatter target `(27,34)`; pouch included; mirror left |
| `pick_vegetable` | side | 8 · 4 | no | low harvest `(26,36)`; mirror left |
| `pick_fruit` | side | 8 · 4 | no | high harvest `(25,14)`; mirror left |
| `carry_shopping` | side | 8 · 4 | yes | two-bag walk; mirror left |
| `row_boat` | side | 8 · 4 | yes | 40 × 40; seat `(20,29)`; oar hands `(30,20)` |
| `drive_speedboat` | side | 8 · 4 | yes | global 4fps baseline; 2-second helm cycle; seat `(16,29)`; helm hands `(25,20)` |
| `operate_outboard` | rear ¾ | 8 · 4 | yes | tiller hand `(4,21)`; mirror left |
| `watch_tv` | rear ¾ | 8 · 4 | yes | seat `(16,29)`; screen target `(40,14)`; mirror left |
| `weld` | side | 8 · 4 | yes | torch contact `(27,22)`; goggles/gloves included; workpiece separate |
| `saw_wood` | side | 8 · 4 | yes | 40 × 40; blade contact `(35,23)`; timber/bench separate |
| `wave_camera` | front | 8 · 4 | no | warm greeting one-shot |
| `yawn` | front ¾ | 8 · 4 | no | sleepy expression and full-body stretch |
| `pyjamas_walk` | side | 8 · 4 | yes | right; mirror left; light powder-blue pyjamas with cream piping |
| `pyjamas_turn_back` | front to back | 6 · 4 | no | reverse to turn front |
| `get_into_bed` | side | 8 · 4 | no | 48 × 40; surface `(24,31)`; pillow `(38,22)`; reverse to rise |
| `pyjamas_snore` | lying side | 6 · 4 | yes | 48 × 40 breathing/snore loop; bed separate |
| `swim_costume_horizontal` | side | 8 · 4 | yes | 80 × 48 centred; right, mirror left; expanded canvas preserves canonical body scale |
| `swim_costume_up` | rear | 8 · 4 | yes | 48 × 48 centred; vector `(0,-1)` |
| `swim_costume_down` | front | 8 · 4 | yes | 48 × 48 centred; vector `(0,1)` |
| `scuba_swim_horizontal` | side | 8 · 4 | yes | 80 × 48 centred; right, mirror left; expanded canvas preserves canonical body scale |
| `scuba_swim_up` | rear | 8 · 4 | yes | mask, tank, regulator and fins |
| `scuba_swim_down` | front | 8 · 4 | yes | mask, tank, regulator and fins |
| `party_idle` | front | 4 · 4 | yes | 32 × 48; exact canonical front identity plus cardboard cone party hat |
| `party_walk` | side | 8 · 4 | yes | 32 × 48; exact canonical side walk; right, mirror left |
| `party_turn_back` | front to back | 6 · 4 | no | 32 × 48; exact canonical turn; reverse to turn front |
| `souwester_walk_side` | side | 8 · 4 | yes | 32 × 48 yellow oilskins; right, mirror left |
| `souwester_walk_back` | rear | 8 · 4 | yes | direct walk away; vector `(0,-1)` |
| `souwester_walk_front` | front | 8 · 4 | yes | direct walk toward camera; vector `(0,1)` |
| `dance` | front | 8 · 4 | yes | joyful full-body loop with strong arm and leg motion |
| `play_guitar` | front ¾ | 8 · 4 | yes | 48 × 40; guitar included; mirror front-left |
| `nap_seated` | side seated | 8 · 4 | yes | canonical seat `(16,29)`; closed eyes, reclined head and open mouth; furniture separate; mirror left |
| `play_guitar_gretsch` | front ¾ | 8 · 4 | yes | tier 2 black Gretsch; canonical actor scale; mirror front-left |
| `play_guitar_flying_v_1967` | front ¾ | 8 · 4 | yes | tier 3 red 1967 Flying V; 64 × 40; mirror front-left |
| `guitar_pickup_*` | side → rear → front ¾ | 12 · 4 | no | 64 × 56; separate rack; prop handoff on frame 6; acoustic/Gretsch/Flying V tiers |
| `artist_smock_walk` | side | 8 · 4 | yes | canonical walk heights; right, mirror left |
| `artist_smock_turn_back/front` | side to rear/front | 6 · 4 | no | matching-outfit activity bridges; reversible |
| `artist_smock_sit_front` | front stand to sit | 6 · 4 | no | seat `(16,29)`; reverse to stand |
| `play_drums_front` | front seated | 8 · 4 | yes | 32 × 48; paired timing/scale master; seat `(16,37)`; strike centre `(16,27)` |
| `play_drums_back` | rear seated | 8 · 4 | yes | 32 × 48; same eight poses through 180°; identical seat and strike points; kit separate |
| `watch_movie` | rear ¾ reclined | 8 · 4 | yes | 48 × 40; popcorn included; seating and screen separate |
| `clear_snow` | side | 8 · 4 | yes | 48 × 40; winter coat and shovel; contact `(43,37)`; mirror left |
| `crouch_work_back` | rear crouched | 8 · 4 | yes | reusable low work proxy; ground contact `(16,38)` |
| `cake_from_oven_back` | rear | 8 · 4 | no | 48 × 40 one-shot; oven rack `(24,30)`; oven separate |
| `cake_turn_right` | rear to side | 6 · 4 | no | 48 × 40; tray carry `(34,20)`; mirror for left |
| `loo_hide` | hidden | 0 | n/a | keeper is not drawn |

The old part files and `keeper_reference.png` are no longer required review deliveries. Airborne strips may expand to 48 × 56 for the dive or 48 × 84 for parachute deployment without rescaling the keeper. Long side tools may use 40 × 40, bed poses 48 × 40, vertical swimming 48 × 48, horizontal swimming 80 × 48, press-ups 64 × 40, standing fishing 64 × 56, overhead weights 48 × 56, and tall headwear 32 × 48. Props are separate `prop_<name>.png` files with their own tight bounds and explicit wrist pivot. `data/keeper_asset_contract.json` is authoritative for scale and use points.

The dive outfit reuses every pivot. Its approved reference is a traditional full-length red-and-white striped one-piece costume, without cap or helmet and with bare feet. Changing is an invisible clip: inner door closes, keeper disappears, zip/rustle SFX, outfit swaps, exterior door opens, dressed keeper exits. There is never a visible frame between the two doors.

## Floor modules and furniture

Floor-local object use points are logical x positions; y is the floor plane. Runtime positions are stored at ×4 in `src/game/config.ts`.

| Floor | Module | Clickable objects at local x | Static set dressing |
|---|---|---|---|
| 1 | `floor_kitchen_t1` | door 23, fridge 44, cooker 64, broom 81, pet bowl 100 | worktop, wall shelf, hooks |
| 2 | `floor_living_t1` | TV 35, bookshelf 64, piano 94 | upgradeable armchair, rug, framed sea chart |
| 3 | `floor_bedroom_ensuite_t1` | bed 33, phone 56, desk 73, basin 95, toilet 110 | bedside table, en-suite partition/door, mirror |

Every clickable set needs the same manifest fields:

```json
{
  "anchor": [0, 0],
  "keeperUsePoint": [-8, 0],
  "effectOrigin": [0, -18],
  "bubbleOrigin": [0, -28],
  "z": 40,
  "states": {
    "standard": { "frames": 1, "fps": 0 },
    "on": { "frames": 4, "fps": 8, "loop": true },
    "broken": { "frames": 4, "fps": 8, "loop": true }
  }
}
```

Object-specific bounds and overrides:

| Object | Frame size | Exact first-pass files (strip size) | Keeper use point | Unique broken cue |
|---|---:|---:|---:|---|
| door | 13 × 24 | standard f1: 13 × 24 | `(8,0)` | static in this batch; runtime contract remains extensible |
| fridge | 12 × 24 | f1: 12 × 24; on/broken f4: 48 × 24 | `(-8,0)` | door hangs ajar, frost puff |
| cooker | 18 × 15 | f1: 18 × 15; on/broken f4: 72 × 15 | `(-10,0)` | one burner sputters |
| broom | 8 × 23 | f1: 8 × 23; on/broken f4: 32 × 23 | `(-6,0)` | split bristle |
| pet bowl | 10 × 5 | f1: 10 × 5; on/broken f4: 40 × 5 | `(0,0)` | small crack/leak |
| TV | 28 × 23 | f1: 28 × 23; on/broken f4: 112 × 23 | `(14,0)` | cracked screen/static |
| bookshelf | 20 × 28 | f1: 20 × 28; on/broken f4: 80 × 28 | `(-14,0)` | slipping book |
| piano | 25 × 18 | f1: 25 × 18; on/broken f4: 100 × 18 | `(-15,0)` | stuck key |
| bed | 30 × 14 | f1: 30 × 14; on/broken f4: 120 × 14 | `(0,0)` | spring pokes out |
| phone | 15 × 18 | f1: 15 × 18; on/broken f4: 60 × 18 | `(-10,0)` | dead-line spark |
| desk | 25 × 20 | f1: 25 × 20; on/broken f4: 100 × 20 | `(-12,0)` | lamp flicker |
| basin | 15 × 28 | f1: 15 × 28; on/broken f4: 60 × 28 | `(-9,0)` | tap leak |
| toilet | 13 × 18 | f1: 13 × 18; on/broken f4: 52 × 18 | `(-8,0)` | cistern rattle; privacy door covers keeper |

Each `broken` loop is the object’s intact casing plus the shared grammar: a 1 logical-pixel horizontal casing wobble, looping smoke, and occasional sparks. Do not draw unique smoke systems into every object.

### Ownership and later exterior kit

The three-floor batch above is the current production priority. Ownership still governs later damage art:

- `garden` (eventual greenhouse included) and `jetty` are keeper-owned and need `standard`, `on`, and `broken` strips in the later exterior batch.
- The future keeper boat is also repairable. Preserve one bottom-centre waterline anchor across the rowing-boat, tug, and speedboat tiers; each tier needs all three states.
- `shop` is an off-island destination owned by its proprietor. It needs destination/open states when travel is built, but never a keeper-repair `broken` state.
- Breakdown event hooks currently emit `electronic-fizzle`, `mechanical-clunk`, `plumbing-sputter`, or `structure-crack`. These names are placeholders for an eventual start/fizzle-loop/repair-success audio set; no sound files are delivered.

## Shared effects, doors and bubbles

| Asset | Canvas / anchor | Frames · fps | z-order / use |
|---|---|---:|---|
| `fx_broken_smoke` | 12 × 16, `(6,16)` | 8 · 8 | 95; seamless rise |
| `fx_broken_sparks` | 12 × 12, `(6,6)` | 6 · 12 | 96; play 1–2 times per loop |
| `fx_steam` | 16 × 20, `(8,20)` | 8 · 8 | 95; cooker |
| `fx_water_bubbles` | 16 × 16, `(8,16)` | 6 · 8 | 95; basin |
| `fx_music_notes` | 20 × 20, `(10,20)` | 8 · 8 | 95; piano |
| `fx_zzz` | 20 × 20, `(10,20)` | 8 · 4 | 95; bed |
| `door_ensuite_standard_f1` | 13 × 24, bottom-centre | 1 · 0 | static room architecture |
| `door_dive_inner` | 13 × 24, bottom-centre | deferred | later extension; do not draw yet |
| `door_dive_exterior` | 13 × 24, bottom-centre | deferred | later extension; do not draw yet |
| `bubble_speech` | 36 × 20, tail `(8,20)` | 4 · 6 | z 110; subtle tail bob |
| `bubble_thought` | 36 × 20, tail `(8,20)` | 4 · 6 | z 110 |
| `bubble_alert` | 20 × 20, tail `(5,20)` | 4 · 8 | z 110 |

The current Floor 3 reservation uses extension seam x 117, inner-door use point x 113, hidden zone x 118–130 and exterior exit x 135. Preserve those bedroom-local coordinates, but do not preserve the global Floor 3 height: final implementation moves the whole extension with the bedroom immediately beneath the lamp room. These are reserved coordinates, not Day 1 visible art.

## Delivery order

1. Floor bands, partitions and three room palettes. **Delivered 8 October 2026:** `tower_stripe_{red,white}.png` and `room_{kitchen,living,bedroom}.png`.
2. Shared object-state overlays and one fully proven object (TV). **Delivered for review 8 October 2026.**
3. Keeper master parts plus the initial movement/action set: `idle`, `walk`, `turn_back`, `work_back`, its domestic-action aliases, sitting/eating, bathroom, door/switch, ladder, stair and piano clips. **Identity, walk and this action direction approved by Frank on 8 October 2026.**
4. Remaining object state sets and effects.
5. Door/changing-room assets and dive outfit only when the extension becomes playable.

## Lighthouse shell files

| File | Exact size | Anchor / z-order |
|---|---:|---|
| `tower_stripe_red.png` | 110 × 8 | top-left; shell z 10 |
| `tower_stripe_white.png` | 110 × 8 | top-left; shell z 10 |
| `tower_base.png` | 110 × 35 | bottom-centre; shell z 10 |
| `tower_lamproom.png` | 110 × 35 | bottom-centre; shell z 10 |
| `tower_roof.png` | 110 × 20 | bottom-centre; shell z 20 |
| `room_kitchen.png` | 105 × 35 | bottom-centre; room z 20 |
| `room_living.png` | 105 × 35 | bottom-centre; room z 20 |
| `room_bedroom.png` | 105 × 35 | bottom-centre; room z 20; en-suite walls included, furniture separate |
| `room_lamp.png` | 105 × 35 | bottom-centre; room z 20 |
| `ground_strip.png` | 300 × 30 | stage bottom-left; scenery z 0; ordinary grass/soil/rock only |

Only the five files explicitly marked in delivery-order item 1 are delivered by this implementation slice. The remaining table entries still record future exact output sizes and must not be inferred as present.
