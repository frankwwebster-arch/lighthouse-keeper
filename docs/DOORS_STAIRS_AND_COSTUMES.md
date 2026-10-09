# Doors, stairway, costumes and seamless animation

Date: 9 October 2026
Status: agreed design. Frank answered the open decisions on 9 October 2026 (section 9); the remaining layout choices are Codex's. The fixed-scale visual transition review described in section 7 is now built; the door/stair/costume-routing gameplay and automated pose contracts are not. Written for Frank, Codex and later Claude sessions. Decisions Frank has agreed are marked **Agreed**.

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
8. **Agreed.** The bed (under the covers) and the loo cubicle (door shut) also hide him, so they can be changing points too.
9. **Agreed.** A door opens as he goes in, **stays open while the activity runs**, and shuts behind him when he leaves. Each room visit therefore has two hidden moments: in and out.
10. **Agreed.** He changes at both doors. Leaving a room he goes back to standard clothes; entering the next he puts on its costume. He is always in standard clothes on the stairway, and he always opens and shuts stairway doors in standard clothes.
11. **Agreed.** Every standard floor is **56 logical px** from floorboards to ceiling (section 3).
12. **Agreed.** The stairway runs **alongside** the rooms, so every room keeps its full width. Codex chooses the side.
13. **Agreed.** Climbing starts with **ladders**, then a **spiral staircase** (if it can be made to look right), then a **lift**. Codex owns how the lift arrives, as part of a magical lighthouse that can grow left, right, up and down. The helter-skelter slide goes on the **outside** of the tower.
14. **Agreed.** The en suite is reached only through the bedroom. In the morning he opens the bathroom door in pyjamas, the only pyjama door clip needed (Codex is making it). Other loos elsewhere in the house follow the same format.
15. **Agreed.** The bedroom has a **walk-in closet**. He steps in and comes out changed, so going to bed from the bedroom needs no trip out.
16. **Agreed.** Washing and teeth mean pyjamas **from 19:00**.
17. **Agreed.** He never naps in bed. Naps happen in an **armchair**.
18. **Agreed.** The toilet sits in its own **cubicle**. He wees standing up in view and poos with the cubicle door shut (the animations exist).
19. **Agreed.** Room doors never break. The front door can break (greeting visitors suffers) but never stops him going in or out.
20. **Agreed.** Codex adds a still standing (neutral) frame for every outfit.
21. **Agreed.** Codex builds the long animation loops; Claude checks the joins and wires everything into the game.

## 3. Floor height: settled at 56 px

The keeper sets the size of everything, so the floor is made to fit him rather than the other way round. Today's numbers:

| Measure | Logical px | On screen (4×) |
|---|---:|---:|
| Floor band, boards to boards (`FLOOR_STEP`, room plate height) | 35 | 140 |
| Keeper standing height (scale contract) | 38 | 152 |
| Keeper canvas (standard / with hat) | 40 / 48 | 160 / 192 |
| Minimum door opening (`keeper_object_dimensions.json`) | 40 | 160 |

As those numbers stand, he is 3 px taller than the room he stands in, and no door can hide him.

**Agreed: 56 logical px of clear height inside every standard floor**, floorboards to ceiling. It fits every indoor clip:

| Tallest indoor poses | Visible height |
|---|---:|
| Weights with the bar overhead | 54 |
| Party hat | 47.5 |
| Trampoline, spiral stairs, swimming | 46 |
| Standing | 38 |

That leaves room for a door about 44 px tall with a lintel above it. The parachute (79), platform dive (52) and standing fishing (54) all happen outside.

What follows (Codex for art, Claude for code):

- The band height is 56 plus whatever floor and ceiling thickness Codex draws. Once Codex sets it, it is fixed for every standard floor for good.
- The three delivered room plates (105 × 35) and the shell are redrawn at the new height. Furniture contact heights stay as they are, because they are measured from the floor.
- The game's `FLOOR_STEP` (today 140 on screen) changes to match. The whole-tower view zooms out further, and the camera's close-up on an activity is unchanged.

## 4. The stairway

- **Alongside the rooms (agreed); Codex picks the side.** The diving extension is currently on the right.
- **One column, built from one section per floor.** When a floor is inserted at its random middle position, the stairway simply gains a section. The stripe pattern still comes from world height, so nothing else moves.
- **Climbing improves over time (agreed):** ladders, then a spiral staircase, then a lift. Codex designs how the lift arrives (the game currently opens the "Puffed Out" lift mission at 5 floors; Frank has 6 in mind) as part of the lighthouse growing magically in every direction.
- **The slide goes on the outside of the tower (agreed).** He is out of sight inside its tube, so it is a hiding point.
- **Lamp room.** The stairway ends at the lamp room. With ladders on day 1, a trapdoor and ladder fits naturally, and it hides him as he climbs through. Codex decides.
- **Underground stays a surprise.** On day 1 the stairway visibly stops at the ground floor. The section below ground appears only when the lair is revealed (the existing rule: no hint of a basement on day 1).
- **The cat and visitors use the doors too.** Cat flaps are a nice touch.

Clips already delivered for climbing: `keeper_stairs_up` / `keeper_stairs_down` (straight stairs), `keeper_spiral_stairs_up` / `_down`, `keeper_ladder_climb`, `keeper_slide_side` and `keeper_lift_button_front`.

## 5. Doors

- **Two layers of art.** The door leaf animates open and shut. The door frame and the wall beside it are drawn **in front of** the keeper. For a few frames he is entirely behind the frame, and that is when any costume swap happens. Per the clip rules, no uncovered in-between frame is ever shown.
- **Open while he is in there (agreed).** A door opens as he enters, stays open while the activity runs, and shuts behind him when he leaves.
- **Room doors never break (agreed).** A jammed door could trap him or cut him off from the loo. At most a door squeaks or sticks for a beat.
- **The front door (agreed)** can break, which spoils greeting visitors until it is repaired, but it never stops him going in or out.
- **The bathroom door already exists.** The delivered bedroom plate includes the en-suite partition and doorway. It becomes a real door that hides him. The en suite has no stairway door of its own. Its door is the one door he opens in pyjamas (the morning trip).
- **The loo has its own cubicle (agreed).** He wees standing up in view; for a poo the cubicle door shuts. Every other loo in the house works the same way.
- **The walk-in closet** off the bedroom has a doorway like any other room.
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
| Brush teeth, wash | light-blue pyjamas | from 19:00 (agreed; `GAME.day.bedFrom`) |
| Wash, brush teeth | standard | before 19:00 (the morning change) |
| Go to bed for the night | light-blue pyjamas | always |
| Nap | standard | in an armchair, never the bed (agreed) |
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

- **Bedroom walk-in closet (agreed).** He steps in and comes out in pyjamas. A doorway off the bedroom that Codex fits into the bedroom floor alongside the en suite.
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

Frank reports every outfit is now drawn and is reviewing each animation for consistency; the keeper art is **not ready to import** until that review finishes. Codex is adding a standing neutral for every outfit (agreed) and the pyjama bathroom-door clip. The table below is from `public/sprites/manifest.json` on 9 October and will be refreshed at import:

| Costume | Delivered | Missing for the minimum set |
|---|---|---|
| standard | 114 clips incl. `walk`, `turn_back`, doors and stairs; the old technical `keeper_idle` is rejected | production standing neutral/idle and phase-aware walk start/stop |
| party hat | idle, walk, turn | none |
| light-blue pyjamas | walk, side-door open/close, turn, get into bed, snore | standing frame |
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
  173 accepted clips at one unchanged relative world scale, with floor, skull,
  shoulder, hip and seat guide lines and optional pose-aware comparison ghosts.
  Review-state filters isolate Happy, Awaiting new draft review, Review later,
  Unreviewed, Needs my input and cards with a Codex response. A focused view
  steps through one large card at a time; Previous/Next and arrow keys remain
  inside the filter and wrap at its ends. A pinned compact reference can show
  standing side/front/back or sitting side/front/back; the sitting endpoint's
  measured 9.75 × 6.5 face proxy exactly matches the standing reference. The
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
- Seated cards automatically use the canonical front/side/rear sitting endpoint.
  Per-card controls can instead select the canonical standing side, facing-front
  or back-to-camera ghost, rotate/reset it or move it alongside, and fade the
  reviewed animation. The canonical rear-sitting endpoint is `keeper_sit_back`.
- Every card has a free-text notes field, mutually exclusive happy and full
  re-draft decisions, a Save button and saved/unsaved indicator. Saved review
  state survives reloads; export includes notes, approvals and the re-draft
  list, and is blocked while any card remains dirty.
- Reviewed-animation rotation and position are independent of the ghost,
  persist per card and are review aids for horizontal poses rather than sprite edits.
- Action-only, raw matching-outfit walk seams and routes containing the known
  turn/sit/bed bridges.
- A seam-freeze onion skin of the final approach frame and first action frame.
- One filename-ordered gallery showing all 169 clips without search or filters;
  every card names its runtime PNG and source strip. Global controls pause or
  play the whole gallery and apply or remove pose-aware comparison ghosts from all
  clips together. The summary still counts the 33 missing facing/posture
  bridges, 18 states without a walking family, 3 special water/air entries and
  8 bridge clips. The detailed costume-route gap audit is
  `docs/KEEPER_COSTUME_ROUTE_AUDIT.md`.

Still to build after the `startPose` / `endPose` metadata exists:

- Neutral-pose red/blue onion skins that can be assessed automatically.
- A random legal clip-to-clip switch test using the declared pose graph, which
  is the closest thing to real play.

### Mood

There are no mood versions of every clip; 80+ clips × 4 moods would be unmanageable. Mood comes from the delivered reaction clips (sad, hungry, bored, cross, yawn) plus the existing bubbles.

## 8. How the game will do it (later work for Claude)

None of this is built. When it is:

- The game state records what he is wearing.
- The costume table lives in `data/costumes.csv`, copied into the game by a script, like the upgrade list (Frank had no preference; a CSV keeps it readable for him and Codex).
- `FLOOR_STEP` and the room geometry follow the new 56 px floors once Codex fixes the band height.
- Doors: open on entry, stay open, shut on leaving; the en-suite door opens with the pyjama clip in the morning; room doors are removed from breakdowns; a broken front door never blocks travel.
- "Have a nap" moves from the bed to an armchair. "Go to the loo" (wee) is no longer private; "Do a poo" shuts the cubicle door.
- The lift mission's floor requirement follows Codex's lift design (Frank has 6 floors in mind).
- Claude checks clip joins (named start and end poses, legal routes) as well as wiring.
- Each route gains door stops: walk to the door, door opens, he steps behind the frame (the costume swaps here if needed), door shuts, stairway, next door, room.
- The clip table: the game picks a clip by activity and costume, then by animation type, then falls back to the vector drawing. A test fails if an activity has no clip for its costume.
- Lift and slide travel reads the saved floor order, so random floor placement keeps working.
- The `?clip=<name>` and `?costume=<name>` preview URLs work like `?tiers=`.

## 9. Decisions (answered 9 October 2026)

| # | Decision | Answer | Who acts |
|---|---|---|---|
| 1 | Floor height | 56 px clear height inside every standard floor | Codex (band, plates, shell), Claude (`FLOOR_STEP`) |
| 2 | Where the stairway goes | alongside the rooms | Codex |
| 3 | Which side | Codex decides | Codex |
| 4 | Climbing progression | ladders, then spiral staircase (if it looks right), then lift; slide on the outside of the tower | Codex |
| 5 | Lift unlock | Codex designs it, with the lighthouse growing left, right, up and down | Codex |
| 6 | Which door he changes at | both: standard clothes on the stairway | Claude |
| 7 | Door behaviour | opens on entry, stays open during the activity, shuts when he leaves | Codex (art), Claude (logic) |
| 8 | Bedroom ↔ en suite | en suite only through the bedroom; pyjama door-open clip for the morning | Codex |
| 9 | Changing in the bedroom | walk-in closet | Codex |
| 10 | Pyjama time | from 19:00 | Claude |
| 11 | Naps | in an armchair, never the bed | Claude (and Codex for the armchair) |
| 12 | Loo | own cubicle; wee standing in view, poo with the door shut; same format everywhere | Codex, Claude |
| 13 | Breakdowns | room doors never break; front door breaks but never blocks | Claude |
| 14 | Neutral frame per outfit | Codex adds one per outfit | Codex |
| 15 | Join checks | Codex builds the loops; Claude checks the joins and wires them up | Claude |
| 16 | Costume table | CSV (`data/costumes.csv`) | Claude |

Still Codex's to settle, no answer needed from Frank: lamp-room access (trapdoor and ladder suggested), door design (one shared frame suggested), splitting `privacy` from `outfit` in the manifest.
