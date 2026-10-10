# Recipes and the recipe studio

Date: 10 October 2026. Written for Codex and later Claude sessions; Frank uses the studio itself.

A **recipe** is one activity written as data: the room, its objects, where he stands, the outfit he starts in, and the steps he goes through. For example: enter by the door, walk to the armchair, sit, nap, stand up, leave. A **macro** is a reusable run of steps, such as entering or leaving a room. A recipe uses a macro by name, so improving the macro improves every recipe that uses it.

The **recipe studio** (`/studio`, linked from Grown-ups) plays a recipe at true pixel size. Frank uses it to fine-tune placement, timing and sounds by eye. Claude and Codex write the drafts; Frank refines them and marks each one *approved*. The game does not play recipes yet. Wiring them into the game comes after Frank's animation review.

Code: `src/studio/recipe.ts` (format, compiler and checks; pure and tested), `src/studio/Studio.tsx` (the screen).

## Where drafts live

- `data/studio/recipes/<id>.json` and `data/studio/macros/<id>.json`, one file each.
- Add every new file to the list in `src/studio/drafts.ts`. A test fails if a file is missing from that list, if a draft names a clip that isn't in `public/sprites/manifest.json`, or if a draft walks into something solid.
- Frank's edits are saved in the database (`studio_docs`) and win over the draft. If a draft changes after Frank has edited that recipe, the studio tells him and offers "Back to the draft". Claude copies approved recipes back into the repo on request.

## The stage

All units are the art's logical pixels and real seconds.

- The room is **110 wide and 56 tall** (the agreed floor height). x = 0 is the room's left wall; the **stairway** runs alongside on the left (x from −38 to 0). Floor y = 0; heights count upwards.
- The door is in the wall at x = 0. Until Codex's door art fixes the numbers, `DOOR` in `recipe.ts` says: a 4 px jamb on the stairway side, and a 12 px leaf that opens into the room towards the camera, 44 px tall. Change those constants when the real door exists; every recipe follows.
- Named places he can walk to: `stairs` (the ladder, x = −27), `doorOut` and `doorIn` (just clear of the doorway on each side), `innerIn` and `innerOut` (for a room with an inner door on the right), `action` (the action point), or any number.
- `KEEPER_HALF` = 11 is his standing half-width, used where a frame's own pixels aren't known.

## A recipe

```json
{
  "id": "armchair_nap", "kind": "recipe", "title": "Nap in the armchair", "notes": "", "status": "draft",
  "activity": "tv_nap",
  "outfit": "standard", "startAt": "stairs", "facing": "right",
  "room": { "name": "Living room", "inner": false },
  "objects": [{ "id": "armchair", "label": "Armchair", "x": 70, "w": 26, "h": 24, "layer": "back", "solid": true, "marks": [{ "label": "seat", "y": 11 }] }],
  "action": { "object": "armchair", "dx": 0, "facing": "right" },
  "walkSpeed": 20,
  "steps": [ … ]
}
```

- `activity` is the game interaction it is for (`INTERACTIONS` in `config.ts`).
- `action` is where his feet go to do it: `dx` pixels from the chosen object's bottom-centre, and the way he faces.
- `marks` are contact heights from `docs/KEEPER_OBJECT_DIMENSIONS.md`, drawn as guide lines.
- `sprite` (optional) shows real object art instead of the placeholder box, once it exists.

### Steps

| `kind` | What it does | Fields |
|---|---|---|
| `walk` | Walks to a place with the outfit's own walk (or `clip`), facing the way he goes. Arriving at `action` turns him to `action.facing`. | `to`, `speed`, `clip`, `facing` |
| `play` | One clip once, holding its last frame. `reverse` plays it backwards, so standing up is sitting down reversed. | `clip`, `reverse`, `facing`, `dx`, `dy` |
| `loop` | One clip repeated for `seconds`. Mark the activity itself `main`. The player can stop the main step at any moment, and `untilStopped` says the game runs it until another order. | `clip`, `seconds`, `main`, `untilStopped` |
| `wait` | Holds a frame (by default the outfit's walk, frame 1) for `seconds`. | `seconds`, `clip` |
| `hide` | Passes through a doorway, unseen. `swapTo` is the outfit he comes out in. This is the only step that crosses a wall. | `through` (`door` / `inner`), `seconds`, `swapTo` |
| `macro` | Runs a macro. `params.swapTo` is the outfit its hidden doorway changes him into. Inside a macro, `"swapTo": "$swapTo"` means "whatever the recipe asks". | `macro`, `params` |

Any step may end with `doorAfter: "open"` or `"close"`, and may carry sound `cues`. `dx` and `dy` nudge him from where he stands. Frank does this by dragging or with the arrow keys.

### Sound cues

```json
{ "id": "c1", "sound": "snore", "at": 0.5, "trimStart": 0, "trimEnd": null, "volume": 1, "loop": true }
```

- `at` is seconds after the step starts.
- `trimStart` / `trimEnd` are seconds into the sound file (`null` = its end).
- `loop` repeats the sound until the step ends.
- A sound is named; the studio's library holds the files (database `studio_sounds`, up to 3 MB each). A name with no file yet is a **placeholder**: it plays a short blip with its own pitch, so timing can be judged now. Frank drops a file on the placeholder and every cue with that name gets it.

## Object types: one recipe for every variant

Every asset in the game can be upgraded (Frank), so a recipe normally names an object **type** rather than one particular object.

- A type lives in `data/studio/categories/<id>.json`: the game's object id (`cooker`), its standing **spots** (`use`, `seat`), whether it is `back` or `front` and `solid`, and its **variants**, usually its upgrade tiers.
- Each variant gives its own size, sprite, contact marks and, for each spot, where his feet go from its bottom-centre and which way he faces.
- In a recipe:
  - an object with `category` and `variant` takes all of that from the variant;
  - `action.spot` puts the action point at that spot, with `action.dx` as a nudge on top.
- Swap the variant and he stands in the right place for the new oven. The studio's **Every variant** row replays the recipe with each variant and shows a tick or the number of problems for each one.
- A walk can go **to an object**: `"@table"` stops him just clear of its nearer edge, and `"@cooker:use"` sends him to a spot. So routes stretch when things are moved, swapped or upgraded.
- List new type files in `CATEGORY_FILES` in `src/studio/drafts.ts`. The tests check every draft recipe against every variant of its types. Frank's edits to a type (variant sizes, spots) are saved in the database and apply to every recipe that uses it.
- Plain objects (no `category`) are only stand-ins.

## Seeing the route, the poses and the evening

- **Route** draws his whole route in a stark magenta: each walk as a line with an arrow, each hidden doorway crossing dashed in blue, and a numbered marker at each stop (the number is the step's number). It is worked out from the objects' positions, so it stretches live as you drag them.
- **Ghosts** shows faint copies of him in the first pose of each stop.
- **Evening** darkens the outside and shades the room. The room's light is on only while its door is open (he opens it on the way in; it closes behind him as he leaves). The stairway is always lit.

## Solid things

Frank's rule: he can never walk into a solid thing, and nothing solid in front of him may ever clip his animation.

- An object has a `layer`:
  - `back`: against the back wall and drawn behind him. He can pass in front of it (a bookshelf, the basin, the TV).
  - `front`: on a side wall or nearer the camera, drawn in front of him and opaque.
- `solid: true` means he can't walk into or through it (an armchair, bed or worktop standing in his path). Front objects are always solid.
- **Walls** are always solid; only a `hide` step crosses one. The **open door leaf** is in front of him and opaque, so he stands clear of it.
- The studio checks every frame he is visible, using the frame's **actual opaque pixels** read from the sheet, not its canvas. It flags:
  - any walk into a wall or solid object;
  - anything in front of him covering any of his pixels.

  Two exceptions: the object he is using (he sits on the armchair), and a door he is opening or closing (his hand is on it).

## What recipes need from each animation sheet

These match Codex's plan for the keeper sheets.

- **`startPose` and `endPose`** on every full-body sidecar, from this shared list: `standing-side-right`, `standing-front`, `standing-back`, `sitting-side-right`, `sitting-front`, `sitting-back`, `lying-side-right`, `crouching-back`, `standing-rear-right`, `sitting-rear-right`, `prone-side-right`, `swimming-side-right`, `swimming-front`, `swimming-back`, `floating-prone-right`, `climbing-back`, `holding-small-object-side-right`, `parachute-open`, `scuba-standing-side-right`, `scuba-swim-right`, `play-guitar-acoustic`, `play-guitar-gretsch`, `play-guitar-flying-v-1967`. Add new names only when an activity needs one, and add them both here and to `data/keeper_pose_registry.json`. Reversed playback swaps start and end.
- A **neutral still frame per outfit and pose**: `keeper_neutral_<pose>` for the standard uniform, `keeper_<outfit>_neutral_<pose>` for the rest.
- **`sfxCues`** on the sidecar, as `[{ "frame": 3, "cue": "door_creak" }]`.
  - `frame` counts from **0**.
  - `cue` uses lower-case letters, digits, `_` and `-`.
  - The studio plays these automatically in every recipe that uses the clip, each time that frame comes round (in a loop too, and in the right place when reversed). They show on the timeline as belonging to the sheet. So mark footsteps once on the walk, and every walk in every recipe has them.
- `reverseFor`, `mirrorSafe`, `facing`, `anchor`, `loop` and `propHandoffFrame` as today. `assetRole` distinguishes `neutral`, `bridge`, ordinary `clip`, and technical `component` / `reference` sheets. The studio already reads `facing` and `mirrorSafe` to decide when to flip a clip. A clip with no facing and no `mirrorSafe` (a rear view) is never flipped.

`npm test` runs `scripts/keeper-contract.ts --check` before Vitest. It checks the shared pose names, zero-based sound frames, the pixel/anchor endpoint audit and the frozen legacy-exception list. Any new endpoint failure, stale audit entry or regression from an exact endpoint fails the normal test command. The ordered human repair queue is `docs/KEEPER_NEUTRAL_ENDPOINT_AUDIT.md`; its machine data is `data/keeper_endpoint_audit.json`.

## Drafting a recipe for a new animation

1. Copy the nearest existing recipe in `data/studio/recipes/`.
2. Set the objects, the action point and the steps. Start and finish with the `enter_room` and `leave_room` macros. Pass `swapTo` if the activity has its own outfit.
3. List the file in `src/studio/drafts.ts` and run `npm test`.
4. Frank opens it in the studio, fine-tunes it and approves it.

## Not built yet

- The game itself playing recipes, with routes between floors and the doors on the way.
- Real door, stairway and furniture art (the studio shows placeholders and switches to the art when it exists).
- A pyjama brushing clip (the bedtime version of brushing teeth).
- Reading object types straight from Codex's sidecars (`docs/BACKGROUND_ELEMENTS.md` §5) instead of `data/studio/categories/`.
- Thought bubbles and the keeper's feelings panel (proposed in `docs/EXPANSION_DESIGN.md`). Recipes would carry the icon he shows when he wants to do the activity.
