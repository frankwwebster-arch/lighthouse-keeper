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
| Build an object at the right size/height | `docs/KEEPER_OBJECT_DIMENSIONS.md`, `data/keeper_object_dimensions.json` and `data/keeper_asset_contract.json` |
| Compare every animation at one scale and test walk seams | `docs/keeper-scale-audit/review.html` |
| Inspect the all-sheet measurement evidence | `docs/keeper-scale-audit/README.md` and its fixed-scale contact sheets |

Folders named `replaced-*` are history only. Never use those in the game.

## Direction rules

- A right-facing side animation marked **mirror left** supplies both directions.
- **Reverse** means play the same frames backward; no duplicate artwork is needed.
- A rear animation marked **mirror hand** stays back-to-camera but swaps which
  hand reaches to the object.
- Furniture, doors, switches, ladders and stairs are separate object art. They
  are deliberately not baked into the keeper frames.
- Costumes, headwear, handheld props and equipment are overlays on canonical
  keeper frames. Never regenerate the actor just to change what he wears or
  carries; a genuinely new pose must pass the full anatomy audit.

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
| Climb into boat | `keeper_boat_enter` | right; fixed gunwale `(39,23)` and bench `(36,35)`; hull/dock separate; mirror left |
| Climb out of boat | `keeper_boat_exit` | front-right; independent weight transfer; same gunwale/bench; mirror left |
| Drive speedboat | `keeper_drive_speedboat` | seated at invisible helm; mirror when layout permits |
| Operate outboard | `keeper_operate_outboard` | rear three-quarter; fixed tiller point; mirror left |
| Watch TV | `keeper_watch_tv` | rear three-quarter right; mirror left; screen stays visible |
| Weld | `keeper_weld` | right; mirror left; goggles, gloves and torch included; workpiece separate |
| Saw wood | `keeper_saw_wood` | right; mirror left; hand saw included; timber and bench separate |
| Wave to camera | `keeper_wave_camera` | front-facing one-shot greeting |
| Yawn | `keeper_yawn` | front three-quarter one-shot sleepy reaction |
| Sad | `keeper_sad` | front; drooping eyes, downturned mouth, slumped shoulders and eye wipe |
| Hungry | `keeper_hungry` | front; worried sad face and repeated tummy rub |
| Bored | `keeper_bored` | front; half-lidded face, loose posture and boot tap |
| Cross | `keeper_cross` | front; knitted eyebrows, frown, folded arms and clean boot stamp |
| Vomit into toilet | `keeper_vomit_loo_back` | direct rear one-shot; separate toilet aligns its bowl target to `(32,35)` |
| Walk in bathrobe | `keeper_bathrobe_walk` | cream terrycloth robe; right; mirror left |
| Open shower door in bathrobe | `keeper_shower_door_open_bathrobe` | rear-right one-shot; separate handle aligns to `(35,18)`; mirror rear-left |
| Enter shower in bathrobe | `keeper_shower_enter_bathrobe` | rear-right to direct rear one-shot; separate cubicle aligns at the feet/threshold anchor |
| Walk in pyjamas | `keeper_pyjamas_walk` | light powder blue with cream piping; right; mirror left |
| Turn away in pyjamas | `keeper_pyjamas_turn_back` | light powder blue; reverse to face camera |
| Get into bed | `keeper_get_into_bed` | light powder blue; right-side bed; mirror left; reverse to get out |
| Snore in pyjamas | `keeper_pyjamas_snore` | light powder blue; right-side loop; mirror left; bed and bedding separate |
| Swim left/right | `keeper_swim_costume_horizontal` | striped costume; right; mirror left; 80 × 48 canonical-scale horizontal canvas |
| Swim up | `keeper_swim_costume_up` | striped costume; direct rear view |
| Swim down | `keeper_swim_costume_down` | striped costume; direct front view |
| Scuba swim left/right | `keeper_scuba_swim_horizontal` | right; mirror left; 80 × 48 canonical-scale horizontal canvas; bubbles separate |
| Scuba swim up | `keeper_scuba_swim_up` | direct rear view; bubbles separate |
| Scuba swim down | `keeper_scuba_swim_down` | direct front view; bubbles separate |
| Party idle | `keeper_party_idle` | exact canonical front face/body; small pale-pink cone, red pom-pom/fringe |
| Party walk | `keeper_party_walk` | exact canonical side-walk identity; right; mirror left |
| Party turn away | `keeper_party_turn_back` | exact canonical turn identity; reverse to face camera |
| Put on party hat | `keeper_party_hat_put_on_back` | rear-view one-shot; play after ordinary turn-away; reverse to remove |
| Eat party cake | `keeper_party_eat_cake` | canonical seated-eat body with party hat and jam-layer cake slice; mirror left |
| Party dance | `keeper_party_dance` | canonical dance body with party hat |
| Walk in sou'wester left/right | `keeper_souwester_walk_side` | yellow oilskins; right; mirror left |
| Walk away in sou'wester | `keeper_souwester_walk_back` | direct rear view; movement vector `(0,-1)` |
| Walk toward camera in sou'wester | `keeper_souwester_walk_front` | direct front view; movement vector `(0,1)` |
| Dance | `keeper_dance` | front-facing eight-frame loop; broad arm and leg motion |
| Play guitar | `keeper_play_guitar` | standing front-right; guitar included; mirror front-left |
| Play drums facing camera | `keeper_play_drums_front` | seated direct front; paired motion/scale master; sticks included; stool and kit separate |
| Play drums back to camera | `keeper_play_drums_back` | the same eight poses viewed through 180°; identical seated scale, seat/strike contacts and timing; sticks included; stool and kit separate |
| Watch a movie | `keeper_watch_movie` | reclined rear-right with popcorn; mirror rear-left; seating and screen separate |
| Clear snow | `keeper_clear_snow` | thick winter coat and shovel; right; mirror left; snow bank/effects separate |
| Crouched ground work | `keeper_crouch_work_back` | direct rear reusable proxy; animated low alternating arm reaches |
| Take cake from oven | `keeper_cake_from_oven_back` | direct rear one-shot; oven/rack separate; mitts, tray and cake included |
| Turn carrying cake | `keeper_cake_turn_right` | rear-to-right one-shot; mirror for rear-to-left |
| Walk carrying cake | `keeper_carry_cake` | right; mirror left; mitts, tray and cake included; connects from cake turn |
| Place cake on table | `keeper_place_cake` | right; mirror left; places at the standard 19 px table datum, releases tray, then straightens fully; table separate |
| Feed fish overhead | `keeper_fish_feed_up` | right; mirror left; aligns to high tank opening |
| Brush aquarium glass | `keeper_aquarium_brush` | right; mirror left; dry algae brush included, tank separate |
| Net aquarium fish | `keeper_aquarium_net` | right; mirror left; net and caught fish included |
| Hammer at workbench | `keeper_hammer_side` / `keeper_hammer_back` | side mirrors left; workbench separate |
| Read sitting | `keeper_read_side` / `keeper_read_front` | side mirrors left; chair and table separate |
| Write | `keeper_write_side` / `keeper_write_back` | side mirrors left; desk separate |
| Check wall instrument | `keeper_check_instrument_side` / `keeper_check_instrument_back` | semantic reuse of switch reach at the same control height |
| Inspect tabletop | `keeper_lean_table_back` | rear lean; table separate |
| Look through telescope | `keeper_telescope` | right; mirror left; telescope mount separate |
| Put on a record | `keeper_put_record` | right; mirror left; 48 × 40 side-action canvas; record included and edge-safe; turntable separate |
| Paint | `keeper_paint_side` / `keeper_paint_back` | splodged artist smock; side mirrors left; canvas/easel separate |
| Use potter's wheel | `keeper_pottery_front` | seated front in artist smock; clay included, wheel separate |
| Type at computer | `keeper_type_computer` | semantic reuse of piano hand motion; desk/computer separate |
| Search boxes | `keeper_search_boxes` | low rear rummage; final arms reach forward into the unseen box; boxes separate |
| Retrieve meal from oven | `keeper_meal_from_oven_back` | rear one-shot; plate/meal included, oven separate |
| Walk carrying plated meal | `keeper_carry_meal` | right; mirror left; mitts, plate and meal included |
| Place meal on table | `keeper_meal_place_side` | right; mirror left; places at the standard 19 px table datum, releases the complete uncropped plate, then straightens fully; table separate |
| Count money | `keeper_count_money` | seated front; notes and coins included |
| Play snooker | `keeper_snooker` | right; mirror left; cue included, table/balls separate |
| Play table tennis | `keeper_table_tennis` | right; mirror left; paddle/ball included, table separate |
| Throw darts | `keeper_darts` | right; mirror left; dart included, board separate |
| Bounce on trampoline | `keeper_trampoline_front` | front; old-school workout kit; trampoline separate |
| Lift weights | `keeper_lift_weights_back` | rear overhead press; old-school workout kit; barbell included; 48 × 56 overhead canvas preserves body scale |
| Do press-ups | `keeper_pressups_side` | right; mirror left; old-school workout kit; 64 × 40 canvas; canonical head/core depth and 47–52 px articulated body-axis envelope |
| Float in anti-gravity | `keeper_anti_gravity` | centred 48 × 48 loop; prone right-facing float in goggles, two-pixel vertical bob and one backward somersault; no parachute; room may add wider drift/circling translation |
| Chop plants | `keeper_machete_side` | right; mirror left; consistent smooth-edged machete included; plants separate; 64 × 40 long-tool canvas; hand/contact `(50,28)` |
| Drink handled pint | `keeper_drink_pint` | seated front-right; mirror front-left; tankard included |
| Use stationary exercise bike | `keeper_ride_bike_front` | direct front; 48 × 48; old-school workout kit; actor only; align separate bike to hand `(24,27)`, seat `(24,35)` and pedal `(24,42)` |
| Press lift button | `keeper_lift_button_front` | front, right-hand reach; mirror to swap hand |
| Spiral stairs up | `keeper_spiral_stairs_up` | right three-quarter to rear curved ascent; staircase/rail separate |
| Spiral stairs down | `keeper_spiral_stairs_down` | rear to front-right curved descent; staircase/rail separate |
| Spiral stairs legacy alias | `keeper_spiral_stairs` | retained ascent for compatibility; use the explicit `up` clip for new work |
| Pour hot drink | `keeper_hot_drink_pour` | 10 frames; right; clean two-hand kettle grip; fixed mug/worktop `(40,28)`; finishes by lowering and releasing kettle; mirror left |
| Stir hot drink | `keeper_hot_drink_stir` | right; mug and spoon at fixed worktop; mirror left |
| Pick up hot drink | `keeper_hot_drink_pickup` | right; mug transfers from worktop to hand; mirror left |
| Drink tea/coffee | `keeper_hot_drink_drink` | right-facing held-mug sipping loop; mirror left |
| Put down hot drink | `keeper_hot_drink_put_down` | right; mug transfers from hand to fixed worktop; mirror left |
| Ride slide | `keeper_slide_side` | right; mirror left; slide separate |
| Use barbecue | `keeper_bbq_back` | rear; tongs included, barbecue separate |
| Soak in hot tub | `keeper_hot_tub` | seated front with opaque water/foam privacy band; tub separate |
| Ten-pin bowling | `keeper_bowling` | right; mirror left; ball included, lane/pins separate |
| Play video game | `keeper_video_game` | rear-right with controller; mirror rear-left; TV/seat separate |
| Water plants | `keeper_water_plants_side` / `keeper_water_plants_back` / `keeper_water_plants_front` | side uses 48 × 40 and mirrors left; can/stream included and edge-safe; plants separate |
| Fish standing | `keeper_fish_standing` | right; mirror left; 64 × 56 canvas keeps the actor at canonical scale while retaining the full rod, line and catch |
| Fish seated | `keeper_fish_seated` | right; mirror left; seat/water separate |
| Collect eggs | `keeper_collect_eggs_back` | canonical low rear work loop; basket, eggs and coop are separate aligned objects |
| Enter / wash / exit bath | `keeper_bath_enter`, `keeper_bath_wash`, `keeper_bath_exit` | entry/exit towel; wash has opaque mosaic/foam privacy coverage; bath separate |
| Enter / wash / exit shower | `keeper_shower_enter`, `keeper_shower_wash`, `keeper_shower_exit` | entry/exit towel; wash has opaque mosaic privacy coverage; shower separate |
| Walk as knight | `keeper_knight_walk_side/back/front` | side mirrors left; three-view canonical movement |
| Walk as spaceman | `keeper_spaceman_walk_side/back/front` | side mirrors left; three-view canonical movement |
| Walk as pirate captain | `keeper_pirate_walk_side/back/front` | side mirrors left; three-view canonical movement |
| Walk as Tarzan | `keeper_tarzan_walk_side/back/front` | family-friendly tunic; bare-headed standard 32 × 40 canvas; side mirrors left; three-view movement |
| Walk in Halloween costume | `keeper_halloween_walk_side/back/front` | friendly face-visible vampire; side mirrors left |
| Walk as mechanic | `keeper_mechanic_walk_side/back/front` | side mirrors left; three-view canonical movement |
| Fix car or boat | `keeper_mechanic_fix` | right; mirror left; spanner included, vehicle/engine separate |

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

Movie watching uses a wider version of that contract. The keeper reclines at
`seatPoint (24,29)`, looks toward `(56,14)`, and holds the popcorn tub with the
character. Mirror the strip and points for a rear-left seat. Keep the cinema
seat or sofa and screen separate, with 32 logical pixels of horizontal screen
clearance so his body never blocks the picture.

The front and rear drum clips share `seatPoint (16,37)` and strike centre
`handUsePoint (16,27)` on their 32 × 48 raised-arm canvas. Drumsticks stay with
the actor; the stool and kit are object assets aligned to those points.

Snow clearing uses a 48 × 40 tool canvas and a right-side shovel contact at
`(43,37)`, three pixels above the floor; mirror both clip and point for left.
The thick winter coat is outfit metadata, while snow banks and spray remain
separate effects. The rear crouched work proxy reaches `(16,38)` so it can be
shared by any low object or ground-level activity without baking in a prop.

Cake retrieval aligns an unseen oven rack to `(24,30)` on a 48 × 40 tray
canvas. The clip ends with the same mitt, tray and cake pose that begins
`keeper_cake_turn_right`; mirror that turn and its carry point from `(34,20)`
to `(14,20)` for left. The oven body, door and rack remain separate objects.

Cooking, washing and brushing currently use named aliases of the general rear
work loop so gameplay code can remain descriptive without duplicating art.
Instrument checking similarly reuses the measured switch reach, while computer
typing reuses the piano hand cycle. These are separately named manifest entries,
so object code never needs to know that the pixels are shared.

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

## Costume transitions and object binding

Objects should declare an interaction profile, not directly force an arbitrary
animation. The controller owns the short transition graph between locomotion,
facing and action states. For the party hat:

1. The loose-hat object exposes a use point and the `put-on-party-hat`
   interaction.
2. The keeper walks to that point, stops, and plays `keeper_turn_back`.
3. The object transfers the loose hat prop to
   `keeper_party_hat_put_on_back`; the rear-view clip raises it behind his head.
4. On the final frame, gameplay sets outfit state `party-hat` and hides the
   loose object. The keeper may then reverse the party turn to face camera or
   enter a party action directly.
5. Removal uses the put-on clip in reverse, restores the loose object on its
   final frame and clears the outfit state.

The same model applies to pyjamas, bathrobe, diving/scuba kit and later
costumes: object interaction chooses a transition recipe; the recipe supplies
walk-stop, facing change, equip/unequip and the final activity. Individual
furniture therefore needs only its stable use/seat/hand points and interaction
tag—the controller fills the standard approach and departure transitions.

Use `docs/keeper-scale-audit/review.html` to test those recipes before they are
wired into gameplay. Its raw-seam mode appends an action directly to the final
four frames of the matching same-outfit walk, deliberately exposing jumps. Its
known-bridge mode inserts the currently documented turn, sit or bed-entry clip.
Seam freeze overlays the final approach pose and first action pose. A standard
uniform action uses `keeper_walk`; costume actions use their own walking family
so the viewer never creates a magical outfit change merely to test a seam.

The current generated inventory gives 119 actions a same-outfit walk and 36 a
known bridge. It labels 33 facing/posture gaps, 21 outfits or states without a
walking family, and 3 water/air actions requiring special entry. Five reusable
bridge clips are also identified separately. These labels
are design evidence, not promises that an unimplemented bridge already exists.

## Current integration boundary

Cooker and basin jobs already select their production rear-work aliases. The
new furniture, door, switch, ladder, stair and workshop clips are game-ready assets but
remain unwired until the corresponding object/path mechanics are implemented.
This prevents a seated or climbing character appearing without matching world
geometry.

## Animation backlog

The next animation work should follow gameplay dependency rather than novelty.

### Priority 0 — everyday playable lighthouse life

- Telephone use, sweep/tidy, generic carry/pick-up/put-down and remaining
  repair/polish variants. Reading, writing, telescope, fishing, watering,
  aquarium care, hammering, welding and sawing are delivered.
- Pet/stroke/play and a standing hand-feed variant for larger animals; bowl
  feeding and egg collection are delivered.
- Receiving/giving an item, thinking and additional idle variants; the
  front-facing wave and yawn reactions are delivered.

### Priority 1 — complete the new adventure actions

- Parachute steering, hanging-descent loop and landing/roll. The delivered jump
  now includes pack opening, pilot chute, canopy inflation and hanging pose.
- Dive splash, underwater entry, floating, climb out and rescue. Directional
  swimming is delivered in both striped and scuba outfits; the platform dive
  ends just before water contact.
- Boat embark/disembark, speedboat acceleration/braking and outboard starting.
- Spacesuit-specific floating for the later expansion; the normal-uniform
  anti-gravity circling loop and three-view spaceman walk are delivered.

### Priority 2 — personality and comedy

- Celebratory jump, spin, shake, shrug and robot walk; dancing is delivered.
- Laugh, cry, hide, headstand and flex.
- Rare bodily/comedy reactions kept separate from ordinary interaction clips.
