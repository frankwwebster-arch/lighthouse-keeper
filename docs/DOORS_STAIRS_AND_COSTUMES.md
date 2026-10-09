# Doors, stairway, costumes and seamless animation

Date: 9 October 2026
Status: agreed design plus open decisions. The fixed-scale visual transition review described in section 7 is now built; the door/stair/costume-routing gameplay and automated pose contracts are not. Written for Frank, Codex and later Claude sessions. Decisions Frank has agreed are marked **Agreed**; everything else is either a recommendation or a decision still to make (the list is at the end).

This builds on Codex's keeper work rather than replacing it:

- `docs/KEEPER_ANIMATIONS.md`: the clip index and the direction rules (mirror, reverse).
- `docs/KEEPER_ASSET_SCALE.md` and `data/keeper_asset_contract.json`: the fixed body scale and contact points.
- `docs/keeper-scale-audit/`: the all-frame scale audit plus the unified fixed-scale walk/action transition viewer (skull, shoulder, hip and sole landmarks; 0.5 px landmark drift, 1 px core-width drift).
- `data/keeper_object_dimensions.json`: door, seat, table and other datums, all taken from the keeper.

## 1. The idea in one paragraph

The stairs are a single tall stairway, separate from the rooms and running from the top of the tower to the bottom. Every room has a door onto it, and rooms on the same floor (bedroom and bathroom) have a door between them. So every trip is **room → door → stairway → door → room**. While he passes through a doorway he is hidden for a moment. That moment is the only time he ever changes costume, so a costume change is never seen and nothing has to animate between two outfits.

## 2. Agreed rules

1. **Agreed.** One continuous stairway runs top to bottom, separate from the rooms.
2. **Agreed.** Every room has a doorway. Doors open, and the doorway hides him as he passes between the stairway and a room, or between two rooms.
3. **Agreed.** He only changes costume while hidden in a doorway. Never on screen.
4. **Agreed.** What he wears is set by the next activity. He keeps his current costume until the next activity begins, then changes at a doorway on the way to it.
5. **Agreed.** Every activity knows its costume. Swimming and then reading puts him back in his standard clothes before he reads.
6. **Agreed.** At bedtime he goes to brush his teeth and changes into pyjamas on the way into the bathroom. In the morning he wakes, goes to the bathroom, and is back in his normal clothes by the time he gets there.
7. **Agreed.** If he is already in the right room but needs a different costume, he steps out of the door and back in (option "a"). Many rooms that need a costume will have their own changing place anyway.
8. **Agreed.** The bed (under the covers) and the loo (door shut) also hide him, so they can be changing points too.

## 3. A blocking problem: the keeper is taller than a floor

This has to be settled before any door, stairway or new room art is made.

| Measure | Logical px | On screen (4×) |
|---|---:|---:|
| Floor band, boards to boards (`FLOOR_STEP`, room plate height) | 35 | 140 |
| Keeper standing height (scale contract) | 38 | 152 |
| Keeper canvas (standard / with hat) | 40 / 48 | 160 / 192 |
| Minimum door opening (`keeper_object_dimensions.json`) | 40 | 160 |

As the numbers stand, he is 3 px taller than the room he stands in, and a door tall enough for him does not fit in a floor. A doorway cannot hide him unless the door is taller than he is, with his tallest hat included.

Options:

- **Taller floors.** For example, 48–52 logical px per band, which fits a 40–44 px door with a ceiling above it. The three delivered room plates and the shell would need redrawing at the new height, and the game constant `FLOOR_STEP` would change. Furniture contact heights are unaffected, because they are measured from the floor.
- **Smaller keeper.** This breaks Codex's locked scale and all 170 delivered sheets (including the 152 accepted animation sheets). Not recommended.
- **Drawing the keeper at a different pixel size from the rooms.** This breaks the "one logical pixel = 4 screen pixels everywhere" rule and makes the pixels mismatched. Not recommended.

**Recommendation:** taller floors, settled by Frank and Codex before the next room or shell art. Whatever height is chosen becomes the one fixed band height for every standard floor and is never changed again.

## 4. The stairway

- **One column, built from one section per floor.** When a floor is inserted at its random middle position, the stairway simply gains a section. The stripe pattern still comes from world height, so nothing else moves.
- **Lamp room.** The stairway ends at the lamp room. A trapdoor and short ladder (`keeper_ladder_climb` exists) also hides him as he climbs through, so it counts as a doorway.
- **Underground stays a surprise.** On day 1 the stairway visibly stops at the ground floor. The section below ground appears only when the lair is revealed (the existing rule: no hint of a basement on day 1).
- **Later transport lives here.** The lift runs in or beside the stairway. The helter-skelter slide wraps around it, with an exit at every floor. Each counts as a hiding point, because he is out of sight inside the lift car or the tube.
- **The cat and visitors use the doors too.** Cat flaps are a nice touch.

Clips already delivered for climbing: `keeper_stairs_up` / `keeper_stairs_down` (straight stairs), `keeper_spiral_stairs_up` / `_down`, `keeper_ladder_climb`, `keeper_slide_side` and `keeper_lift_button_front`.

## 5. Doors

- **Two layers of art.** The door leaf animates open and shut. The door frame and the wall beside it are drawn **in front of** the keeper. For a few frames he is entirely behind the frame, and that is when any costume swap happens. Per the clip rules, no uncovered in-between frame is ever shown.
- **Room doors never break.** A jammed door could trap him or cut him off from the loo. At most a door squeaks or sticks for a beat.
- **The front door** is today a breakable object (greeting visitors). A broken front door may stop the greeting but must never stop him going outside.
- **The bathroom door already exists.** The delivered bedroom plate includes the en-suite partition and doorway. It becomes a real door that hides him.
- **Timing.** Each door adds a short pause, roughly half a second at the game's speed. The pause is a tunable number in `config.ts`.

## 6. Costumes

### Which costume, when

A small table says what each activity needs. The default is the standard uniform.

| Activity | Costume | Condition |
|---|---|---|
| Swim, dive | striped swimming costume | always |
| Scuba | scuba | always |
| Gym: weights, press-ups, bike, trampoline | old-school workout kit | always |
| Paint, pottery | artist's smock | always |
| Mechanic jobs | mechanic overalls | always |
| Brush teeth, wash | light-blue pyjamas | from bedtime (19:00, `GAME.day.bedFrom`) |
| Wash, brush teeth | standard | before bedtime (the morning change) |
| Go to bed for the night | light-blue pyjamas | always |
| Nap | standard | always (on top of the covers) |
| Shower | cream bathrobe → towel → washing | always (the shower sequence) |
| Outside jobs | sou'wester oilskins | when raining (later weather) |
| Outside jobs | winter coat | when snowing (later weather) |
| Party | party hat | during a party event |

Costumes for play or dressing up (knight, spaceman, pirate, Tarzan, Halloween) are set by whichever activity or event uses them.

### At which door

Every costume change happens while the keeper is completely hidden behind a
door. All doors hinge on the player's side and render in front of him, creating
a short full-body occlusion. He approaches in the old outfit, the foreground
door covers him, the runtime swaps costume state while no part of him is
visible, and he emerges in the new outfit. There is no visible dressing or
morphing transition; the party hat follows the same rule, so its put-on clip is
optional flavour rather than required gameplay plumbing.

Use two quick hidden swaps for travel between rooms: as he leaves a room he
changes back to standard clothes, and as he enters the target room he changes
into its costume. He is therefore always in standard clothes on the stairway,
so only the standard uniform needs stair, ladder, lift and slide clips. Where
there is only one door between the two rooms (bedroom ↔ bathroom), use one
hidden swap.

### Changing places

These save him from stepping out and back in:

- **Bedroom wardrobe.** He steps in and comes out in pyjamas, which covers "go straight to bed". This is an object for Codex if agreed.
- **Pool changing cubicle** (already in `EXPANSION_DESIGN.md`).
- **Diving changing room.** The existing two-door changing room by the bedroom.
- **Gym changing room.**
- **Coat hooks by the front door.** Oilskins and the winter coat go on here.

### What each costume needs at minimum

Any costume he can wear in a room needs:

- **A still standing frame.** This is the costume's neutral pose, used for joining clips (section 7) and for standing still.
- **A side walk** (mirrored for left), to get from the door to the activity and back.
- **A turn to face away**, if any of its activities are back to the camera.
- Its activity clips.

Only the standard uniform needs stair, ladder, lift and slide clips under this
door-occluded two-swap rule.

What exists and what is missing today, from `public/sprites/manifest.json`:

| Costume | Delivered | Missing for the minimum set |
|---|---|---|
| standard | 114 clips incl. `walk`, `turn_back`, doors and stairs; the old technical `keeper_idle` is rejected | production standing neutral/idle and phase-aware walk start/stop |
| party hat | idle, walk, turn | none |
| light-blue pyjamas | walk, turn, get into bed, snore | standing frame |
| cream bathrobe | walk, shower door, shower entry | standing frame |
| striped swimming costume | swim up/down/horizontal | standing frame, side walk (to the board or ladder) |
| scuba | swim up/down/horizontal | standing frame, side walk (if he walks in it) |
| old-school workout kit | weights, press-ups, bike, trampoline | standing frame, side walk |
| artist's smock | paint (side/back), pottery | standing frame, side walk |
| winter coat | clear snow | standing frame, side walk |
| sou'wester, knight, spaceman, pirate, Tarzan, Halloween, mechanic | three-view walks (+ mechanic fix) | standing frame |

**Metadata tidy-up.** The manifest's `outfit` field also contains `mosaic-privacy`, `towel-privacy` and `privacy-foam`. Those are privacy coverings, not costumes. A separate `privacy` field would stop the game treating them as outfits.

## 7. Joining clips without a blip

Codex's audit proves every frame is measured at the same body scale. The new
`docs/keeper-scale-audit/review.html` also provides a visual check where one
clip hands over to the next. It does not yet enforce named start/end poses or
automatically prove that every legal gameplay route is seamless.

### The rule

Every clip starts and ends on a **named pose**, and two clips may only follow each other if the end pose of one matches the start pose of the next. Poses within one costume:

| Pose | Example clips that start or end here |
|---|---|
| `stand` (side) | idle, walk, door open, switch press |
| `stand-rear` | turn back (end), rear work, cooking |
| `seated-side` | sit side (end), eat seated, read side |
| `seated-front` | sit front (end), toilet, count money |
| `lying` | get into bed (end), snore |
| `carry-tray` | cake from oven (end), cake turn, carry cake, place cake (start) |
| `hidden` | inside a door, the loo, the shower cubicle, the lift |

The manifest would gain `startPose` and `endPose` on each clip. Reversed playback swaps them. Sitting down is `stand` → `seated-side`, so played backwards it is standing up.

The animation review sheet uses frame 6 of `keeper_turn_back` as its canonical
standing back-to-camera ghost. It is the standard-outfit `stand-rear` endpoint,
not a work-action or costume substitute.
Its facing-front standing ghost is the neutral arms-down frame 1 of
`keeper_wave_camera`, which is also the source used by the exact-canonical-
identity party front idle.

### What gets checked

| Check | Proposed tolerance |
|---|---|
| A clip's first and last frames match its costume's neutral frame for that pose, comparing the body region and ignoring held props | feet anchor exact; body landmarks within 0.5 px (the existing audit tolerance) |
| Loops: the last frame leads cleanly back to the first | same as above |
| Horizontal drift: the feet or hips do not slide sideways during a standing loop | 0 px, unless the clip has a movement vector |
| Declared chains (cake, meal, hot drink, boat, shower) line up frame to frame at each handover | exact at the contact point (tray, mug, gunwale) |
| Every activity has a route of clips from `stand` to its loop and back to `stand` in its costume | must exist (game-side test) |

Props may appear or disappear only at an explicit acquire/release event, behind
an object that conceals the handover, or during full door/cubicle occlusion.
The prop and keeper hand must share the same contact point on both sides of the
handover; an unexplained first-frame pop is not a seamless join.

### The review page

Delivered in `docs/keeper-scale-audit/review.html`:

- A dedicated untouched `keeper_walk` scale-authority panel, followed by all
  152 accepted clips at one unchanged relative world scale on a shared 96 × 96
  stage, with floor, skull, shoulder, hip and seat guide lines and optional
  pose-aware comparison ghosts. A focused view steps through one large card at
  a time with Previous/Next controls, progress and arrow-key navigation while
  retaining card edits. A pinned compact reference can show standing or one
  sitting canon; its endpoint's measured 9.75 × 6.5 face proxy exactly matches
  the standing reference frame. The
  1×–12× display-size slider magnifies the reviewed stage without changing the
  source art or its relative scale. For upright
  standard-cap poses, the gold badge on the blue skull line is a calibrated
  proxy only; changed posture, head angle and headwear need anatomy checks.
- Per-animation 50%–150% width and height sliders reshape the action around its
  declared contact anchor; −0.5%/+0.5% buttons beside each axis provide precise
  adjustments while the reference, ruler, ghost, walk and bridge stay at 100%.
  Horizontal and vertical controls reposition only the reviewed
  action and include a zero-offset reset. Earlier uniform choices migrate to both axes. Saved proposals
  export as JSON for later source-art rebuilding; the viewer never edits sprites.
- Every blue animation-transform slider has −0.5/+0.5 buttons: degrees for
  rotation, logical pixels for position and percentage points for opacity.
  They share the slider limits and normal Save/export workflow.
- Flying and swimming cards align their first-frame figure bottom to the red
  floor line. Global Pause resets every card to frame 1 of its action.
- Every card has Previous/Next frame buttons and an exact frame counter. Using
  them pauses playback and steps through the action without dirtying the review.
- A separate 1–20fps proposed game-speed slider, −0.5fps/+0.5fps buttons and an
  authored-speed reset preview timing live and save/export `animationFps` as a
  production decision. Seam approach walks and bridges retain their own FPS.
  Accepted values go into each source JSON sidecar and the generated runtime
  manifest, not into the sprite PNG.
  A prominent pane badge continuously shows the displayed clip and frame,
  including during playback and for both sides of a frozen seam.
- The adjacent Play animation button starts only that action at frame 1. Its
  selector plays once and holds the final frame, or loops until paused; this
  review-only playback choice does not dirty the card.
- On browser widths of 1500px or more, focused mode uses a three-part horizontal
  workstation: pinned canon, large stage and compact two-column control console.
  Control families have distinct amber, purple, blue, teal and green/red colours.
- Browser-local progress retains display zoom immediately. Every card save marks
  that animation as the latest completed one; reload resumes in focused mode on
  the following filename-ordered animation, or the final card when already last.
- Seated cards automatically use the canonical front/side sitting endpoint.
  Per-card controls can instead select the canonical standing side, facing-front
  or back-to-camera ghost, rotate/reset it or move it alongside, and fade the
  reviewed animation. Rear sitting still has no canonical neutral reference.
- Every card has a free-text notes field, mutually exclusive happy and full
  re-draft decisions, a Save button and saved/unsaved indicator. Saved review
  state survives reloads; export includes notes, approvals and the re-draft
  list, and is blocked while any card remains dirty.
- Reviewed-animation rotation and position are independent of the ghost,
  persist per card and are review aids for horizontal poses rather than sprite edits.
- Action-only, raw matching-outfit walk seams and routes containing the known
  turn/sit/bed bridges.
- A seam-freeze onion skin of the final approach frame and first action frame.
- One filename-ordered gallery showing all 152 clips without search or filters;
  every card names its runtime PNG and source strip. Global controls pause or
  play the whole gallery and apply or remove pose-aware comparison ghosts from all
  clips together. The summary still counts the 33 missing facing/posture
  bridges, 21 states without a walking family, 3 special water/air entries and
  5 bridge clips.

Still to build after the `startPose` / `endPose` metadata exists:

- Neutral-pose red/blue onion skins that can be assessed automatically.
- A random legal clip-to-clip switch test using the declared pose graph, which
  is the closest thing to real play.

### Mood

There are no mood versions of every clip; 80+ clips × 4 moods would be unmanageable. Mood comes from the delivered reaction clips (sad, hungry, bored, cross, yawn) plus the existing bubbles.

## 8. How the game will do it (later work for Claude)

None of this is built. When it is:

- The game state records what he is wearing.
- The costume table lives in `config.ts` (or a CSV like the upgrade list if Frank wants to edit it).
- Each route gains door stops: walk to the door, door opens, he steps behind the frame (the costume swaps here if needed), door shuts, stairway, next door, room.
- The clip table: the game picks a clip by activity and costume, then by animation type, then falls back to the vector drawing. A test fails if an activity has no clip for its costume.
- Lift and slide travel reads the saved floor order, so random floor placement keeps working.
- The `?clip=<name>` and `?costume=<name>` preview URLs work like `?tiers=`.

## 9. Decisions to make

| # | Decision | Options | Recommendation | Who |
|---|---|---|---|---|
| 1 | **Floor height (blocking)** | taller bands / smaller keeper / mixed pixel sizes | taller bands (about 48–52 px), fixed for good | Frank + Codex |
| 2 | Where the stairway goes | inside the 110 px width (rooms narrower, redraw plates) / alongside it (tower wider, rooms untouched) / behind the rooms (unseen) | alongside | Frank + Codex |
| 3 | Which side | left / right | left: the front door and today's stairs are on the left, and the diving extension is on the right | Codex |
| 4 | Stair type on day 1, and whether stairs are an upgrade | ladder / straight stairs / spiral; upgrade tiers for speed | straight stairs on day 1 (clips exist). The ladder → stairs → spiral → slide → lift progression in `EXPANSION_DESIGN.md` could be the stairway's upgrade tiers, since speed is a real benefit | Frank |
| 5 | Who opens doors | he opens each one by hand / they open by themselves as he arrives | by themselves for room doors (fast, magical, and no door clip needed per costume). Opening by hand stays for the front door, shower and wardrobe | Frank |
| 6 | Which door he changes at | entry door only / exit door only / both (standard clothes on the stairway) | both | Frank |
| 7 | Pyjamas on the stairway at night | change back to standard / stay in pyjamas / dressing gown | standard (follows from 6) | Frank |
| 8 | Bedroom wardrobe as a changing place | yes / no | yes | Frank |
| 9 | Bedtime switch for pyjamas | from 19:00 (`bedFrom`) / from 20:00 (`bedtime`) / only the bedtime routine | from 19:00 | Frank |
| 10 | Pyjamas for daytime naps | yes / no | no | Frank |
| 11 | Lamp-room access | door / trapdoor and ladder | trapdoor and ladder | Codex |
| 12 | Door design | one shared door / a themed door per room | one shared door frame, optional themed leaf | Codex |
| 13 | Front door breakdowns | keep breakable but never block going out / unbreakable | keep breakable, never blocks travel | Frank |
| 14 | Neutral frame per costume | new still frame per costume / first frame of its walk | new still frame per costume (a walk frame is mid-stride) | Codex |
| 15 | Who builds the join checks | Codex extends the scale audit / Claude adds game tests / both | both: Codex's visual seam review is delivered; named-pose art checks and Claude's legal-route game tests remain | Frank |
| 16 | `privacy` split from `outfit` in the manifest | yes / no | yes | Codex |
| 17 | Lift and slide placement | inside the stairway column / a second column beside it | the slide wraps the stairway; the lift takes the stairway's back half or a second column, depending on 2 | Codex |
| 18 | Costume table format | in `config.ts` / a CSV Frank can edit | CSV, matching the upgrade list | Frank |
