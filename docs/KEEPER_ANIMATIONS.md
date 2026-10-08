# Keeper animations — plain-English index

This is the human-readable index for the keeper. Start here rather than trying
to infer meaning from filenames or Git history.

## Which files matter

| Need | Use this location |
|---|---|
| Watch an animation | `docs/floor-asset-catalogue/keeper-*-preview.gif` |
| Put it in the game | `public/sprites/keeper_*.png` via `public/sprites/manifest.json` |
| Rebuild or adjust it | `art/source/keeper-first-batch/author_keeper.py` and the matching `*-generated-source.png` |
| Check exact frames, speed and alignment | matching JSON in `art/raw/keeper-first-batch/` |
| Build an object at the right size/height | `docs/KEEPER_ASSET_SCALE.md` and `data/keeper_asset_contract.json` |

Folders named `replaced-*` are history only. Never use those in the game.

## Direction rules

- A right-facing side animation marked **mirror left** supplies both directions.
- **Reverse** means play the same frames backward; no duplicate artwork is needed.
- A rear animation marked **mirror hand** stays back-to-camera but swaps which
  hand reaches to the object.
- Furniture, doors, switches, ladders and stairs are separate object art. They
  are deliberately not baked into the keeper frames.

## Current reusable clips

| What Frank means | Runtime sprite | Direction/application rule |
|---|---|---|
| Walk | `keeper_walk` | right; mirror left |
| Turn away | `keeper_turn_back` | reverse to face camera |
| General work | `keeper_work_back` | washing, cooking, polishing and similar |
| Sit on side chair | `keeper_sit_side` | right; mirror left; reverse to stand |
| Sit facing camera | `keeper_sit_front` | sofa/toilet; reverse to stand |
| Eat at table | `keeper_eat_seated` | right; mirror left; fork and knife included |
| Play piano/instrument | `keeper_piano` | rear three-quarter; seated |
| Urinate | `keeper_urinate_back` | discreet rear three-quarter pose |
| Open side door | `keeper_door_open_side` | right; mirror left; reverse to close |
| Open door ahead | `keeper_door_open_back` | rear; mirror handle side; reverse to close |
| Climb ladder | `keeper_ladder_climb` | forward/up; reverse/down |
| Walk upstairs | `keeper_stairs_up` | right; mirror left |
| Walk downstairs | `keeper_stairs_down` | right; mirror left |
| Press side switch | `keeper_switch_press_side` | right; mirror left; reverse to withdraw |
| Press switch ahead | `keeper_switch_press_back` | rear/right hand; mirror for left hand; reverse to withdraw |
| Parachute jump | `keeper_parachute_jump` | 9 frames; pack opens and round canopy deploys |
| Dive from platform | `keeper_platform_dive` | 10 frames; right/mirror left; ends vertical head-first |
| Dig garden | `keeper_dig` | right; mirror left; soil remains separate |
| Feed animals | `keeper_feed_animals` | right; mirror left; bowl and animal remain separate |
| Sow seeds | `keeper_sow_seeds` | right; mirror left; pouch included, bed separate |
| Pick vegetables | `keeper_pick_vegetable` | low harvest point; right; mirror left |
| Pick fruit | `keeper_pick_fruit` | high harvest point; right; mirror left |
| Carry shopping | `keeper_carry_shopping` | two-bag walk; right; mirror left |
| Row boat | `keeper_row_boat` | seated; two oars included; hull/water separate |
| Drive speedboat | `keeper_drive_speedboat` | seated at invisible helm; mirror when layout permits |
| Operate outboard | `keeper_operate_outboard` | rear three-quarter; fixed tiller point; mirror left |
| Watch TV | `keeper_watch_tv` | rear three-quarter right; mirror left; screen stays visible |
| Weld | `keeper_weld` | right; mirror left; goggles, gloves and torch included; workpiece separate |
| Saw wood | `keeper_saw_wood` | right; mirror left; hand saw included; timber and bench separate |
| Wave to camera | `keeper_wave_camera` | front-facing one-shot greeting |
| Yawn | `keeper_yawn` | front three-quarter one-shot sleepy reaction |
| Walk in pyjamas | `keeper_pyjamas_walk` | right; mirror left |
| Turn away in pyjamas | `keeper_pyjamas_turn_back` | reverse to face camera |
| Get into bed | `keeper_get_into_bed` | right-side bed; mirror left; reverse to get out |
| Snore in pyjamas | `keeper_pyjamas_snore` | right-side loop; mirror left; bed and bedding separate |
| Swim left/right | `keeper_swim_costume_horizontal` | striped costume; right; mirror left |
| Swim up | `keeper_swim_costume_up` | striped costume; direct rear view |
| Swim down | `keeper_swim_costume_down` | striped costume; direct front view |
| Scuba swim left/right | `keeper_scuba_swim_horizontal` | right; mirror left; bubbles separate |
| Scuba swim up | `keeper_scuba_swim_up` | direct rear view; bubbles separate |
| Scuba swim down | `keeper_scuba_swim_down` | direct front view; bubbles separate |
| Party idle | `keeper_party_idle` | front; normal clothes plus cardboard party hat |
| Party walk | `keeper_party_walk` | right; mirror left |
| Party turn away | `keeper_party_turn_back` | reverse to face camera |

For review, the shared side strip has separate, plainly named
`keeper-switch-press-right-preview.gif` and
`keeper-switch-press-left-preview.gif` files. They demonstrate both directions;
the runtime stores only one side strip and mirrors it.

TV watching follows the same rule. `keeper-watch-tv-right-preview.gif` and
`keeper-watch-tv-left-preview.gif` show the two seating arrangements, but the
runtime stores one rear-three-quarter strip. The keeper's seat is placed 24
logical pixels to one side of the TV screen centre, with the screen centre 15
pixels above the seat. This leaves the screen visible rather than putting his
back directly in front of it.

Cooking, washing and brushing currently use named aliases of the general rear
work loop so gameplay code can remain descriptive without duplicating art.

## Applying a switch animation to an object

Normal keeper clips use a 32 × 40 logical canvas and feet anchor `(16,40)`.
The head-first dive uses 48 × 56; the full parachute deployment uses 48 × 84.
Both add transparent room without changing his scale.
`handUsePoint` is the fingertip location in that same canvas.

| Pose | `handUsePoint` | Switch position relative to his feet |
|---|---:|---:|
| side, facing right | `(27,17)` | `(+11,-23)` |
| side, mirrored left | `(5,17)` | `(-11,-23)` |
| back, right hand | `(26,17)` | `(+10,-23)` |
| back, mirrored hand | `(6,17)` | `(-10,-23)` |

For a new switch, button or control:

1. Give the object a stable world-space switch point.
2. Put the keeper's feet at the object's `keeperUsePoint`.
3. Align the selected clip's fingertip offset above with the switch point.
4. Play frames forward to press and backward to return to idle.
5. Mirror only when the table says it is safe.

The sprite manifest carries `interaction`, `facing`, `handUsePoint`,
`mirrorSafe`, `mirrorsFor` and `reverseFor`, so application code does not need
hard-coded knowledge of the artwork.

## Current integration boundary

Cooker and basin jobs already select their production rear-work aliases. The
new furniture, door, switch, ladder, stair and workshop clips are game-ready assets but
remain unwired until the corresponding object/path mechanics are implemented.
This prevents a seated or climbing character appearing without matching world
geometry.

## Animation backlog

The next animation work should follow gameplay dependency rather than novelty.

### Priority 0 — everyday playable lighthouse life

- Seated reading and TV sit/stand transitions; the watching loop is delivered.
- Bed entry, sleep/snore loop and get-out reverse are delivered; blanket and
  pillow artwork remain part of the bed object.
- Telescope look, telephone use and fishing cast/reel/catch.
- Sweep/tidy, carry/pick up/put down, and remaining repair/polish variants;
  welding and hand-sawing are delivered with their visible tools.
- Garden watering and planting; sowing and low/high harvesting are delivered.
- Pet/stroke/play and a standing hand-feed variant for larger animals.
- Receiving/giving an item, thinking and additional idle variants; the
  front-facing wave and yawn reactions are delivered.

### Priority 1 — complete the new adventure actions

- Parachute steering, hanging-descent loop and landing/roll. The delivered jump
  now includes pack opening, pilot chute, canopy inflation and hanging pose.
- Dive splash, underwater entry, floating, climb out and rescue. Directional
  swimming is delivered in both striped and scuba outfits; the platform dive
  ends just before water contact.
- Boat embark/disembark, speedboat acceleration/braking and outboard starting.
- Spacesuit floating for the later expansion.

### Priority 2 — personality and comedy

- Dance, celebratory jump, spin, shake, shrug and robot walk.
- Laugh, cry, hide, headstand and flex.
- Rare bodily/comedy reactions kept separate from ordinary interaction clips.
