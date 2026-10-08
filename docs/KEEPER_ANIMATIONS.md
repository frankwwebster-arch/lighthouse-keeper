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

For review, the shared side strip has separate, plainly named
`keeper-switch-press-right-preview.gif` and
`keeper-switch-press-left-preview.gif` files. They demonstrate both directions;
the runtime stores only one side strip and mirrors it.

Cooking, washing and brushing currently use named aliases of the general rear
work loop so gameplay code can remain descriptive without duplicating art.

## Applying a switch animation to an object

All keeper clips use a 32 × 40 logical canvas and feet anchor `(16,40)`.
`handUsePoint` is the fingertip location in that same canvas.

| Pose | `handUsePoint` | Switch position relative to his feet |
|---|---:|---:|
| side, facing right | `(27,17)` | `(+11,-23)` |
| side, mirrored left | `(5,17)` | `(-11,-23)` |
| back, right hand | `(26,16)` | `(+10,-24)` |
| back, mirrored hand | `(6,16)` | `(-10,-24)` |

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
new furniture, door, switch, ladder and stair clips are game-ready assets but
remain unwired until the corresponding object/path mechanics are implemented.
This prevents a seated or climbing character appearing without matching world
geometry.
