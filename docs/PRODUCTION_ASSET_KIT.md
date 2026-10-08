# Lighthouse Keeper — first-three-floor production asset kit

Status: production specification. Delivery-order item 1 is complete for the two shell stripe bands and the kitchen, living-room, and bedroom/en-suite plates. All older PNGs remain concept/prototype references; do not cut sprites out of the scene plates.

## Coordinate and export contract

- Author at one source pixel per logical pixel on a 300 × 190 logical stage. Runtime SVG coordinates are logical coordinates × 4 (`viewBox="0 0 1200 760"`). Use integers only.
- The gameplay core is fixed at 110 × 35 logical pixels per floor band (runtime 440 × 140). Room plates are exactly 105 × 35. Do not taper or rescale a floor.
- Export transparent PNGs (or flat `#FF00FF` for the existing cleanup script) with nearest-neighbour sampling, no blur and no anti-aliasing.
- Object filename: `obj_<id>_<state>_f<frames>.png`. All equal-size frames are arranged left-to-right in one strip. Tier 1 has no tier suffix; later tiers use `_t2`, `_t3`, and so on before the state.
- `standard` is one frame; the first production pass uses four-frame `on` and `broken` loops at the fps below. The manifest stores `file`, `frames` and `fps`; the runtime already supports string entries for old stills and metadata entries for strips.
- Object origin is bottom-centre `(0,0)` at its floor contact. Keeper origin is between the boots. Effect and bubble origins are explicit manifest points, never inferred from transparent bounds.

## Keeper kit

Every keeper part is a **32 × 40** transparent PNG on the same aligned canvas. The standing silhouette is approximately 22 × 32; floor anchor `(16,40)`. Stacking the neutral parts at `(0,0)` must rebuild `keeper_reference.png` exactly. Shared pivots are measured within that canvas.

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

| Clip | View | Frames · fps | Loop | Interaction point |
|---|---|---:|---|---|
| `idle` | front | 4 · 6 | yes | floor anchor |
| `walk` | front/side composite | 8 · 10 | yes | floor anchor; no sub-pixel travel |
| `reach_use` | front | 5 · 10 | no | hand to object use point |
| `cook_back` | back | 6 · 8 | yes | hands `(16,21)` to cooker |
| `watch_tv` | back | 4 · 5 | yes | seated anchor `(16,37)` |
| `read` | front | 4 · 5 | yes | book pivot `(21,22)` |
| `piano` | back | 8 · 10 | yes | hands `(16,21)` |
| `sleep` | front-derived | 4 · 4 | yes | bed contact `(16,31)` |
| `phone` | front | 4 · 6 | yes | handset pivot `(22,14)` |
| `brush_teeth_back` | back | 6 · 8 | yes | hand `(22,18)` to basin |
| `wash_back` | back | 6 · 8 | yes | hands `(16,21)` to basin |
| `loo_hide` | hidden | 0 | n/a | keeper is not drawn |

Required part files are `keeper_front_head_{happy,neutral,grumpy,asleep,open}.png`, `keeper_front_{torso,arm_l,arm_r,leg_l,leg_r}.png`, the equivalent `keeper_back_*` files with one back head, and `keeper_reference.png`; every file is 32 × 40. Props are separate `prop_<name>.png` files with their own tight bounds and explicit wrist pivot. Pivots are for assembly tooling; production raster limbs use drawn key angles or integer translations in final clips rather than arbitrary CSS rotation.

The later dive outfit reuses every pivot. Supply `keeper_outfit_dive_*` in Victorian red-and-white stripes only when that later batch begins. Changing is an invisible clip: inner door closes, keeper disappears, zip/rustle SFX, outfit swaps, exterior door opens, dressed keeper exits. There is never a visible frame between the two doors.

## Floor modules and furniture

Floor-local object use points are logical x positions; y is the floor plane. Runtime positions are stored at ×4 in `src/game/config.ts`.

| Floor | Module | Clickable objects at local x | Static set dressing |
|---|---|---|---|
| 1 | `floor_kitchen_t1` | door 23, fridge 44, cooker 64, broom 81, pet bowl 100 | worktop, wall shelf, hooks |
| 2 | `floor_living_t1` | TV 35, bookshelf 64, piano 94 | sofa, rug, framed sea chart |
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

The Floor 3 extension seam is at local x 117. Inner door use point is x 113; the hidden changing zone occupies x 118–130; exterior exit is x 135. These are reserved coordinates, not Day 1 visible art.

## Delivery order

1. Floor bands, partitions and three room palettes. **Delivered 8 October 2026:** `tower_stripe_{red,white}.png` and `room_{kitchen,living,bedroom}.png`.
2. Shared object-state overlays and one fully proven object (TV).
3. Keeper master parts plus `idle`, `walk`, `cook_back`, `wash_back` and `brush_teeth_back`.
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
