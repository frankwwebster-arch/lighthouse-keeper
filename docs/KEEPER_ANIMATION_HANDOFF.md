# Keeper animation handoff: review, scale and seamless transitions

**Checkpoint:** 10 October 2026
**Purpose:** this is the restart document for the keeper-animation work. A new
Codex task should be able to continue from here without relying on the old chat.

## Neutral endpoint contract checkpoint — 10 October 2026

`scripts/keeper-contract.ts` is now the authority for recipe-facing pose
metadata, neutral stills, reusable derived bridges and the real-RGBA endpoint
audit. `npm test` runs its read-only check first. The current contract has 325
keeper sheets: the reviewed 191-sheet source batch plus deterministic neutral
and bridge derivatives. All full-body sidecars carry registered `startPose` and
`endPose`; technical component/reference sheets are explicitly excluded.

The priority sample flows now have exact walk start/stop/cycle,
right/left-to-front and right/left-to-back turns (with reverse routes to all
four facings), side/front/back sits, crouch/stand, reach high/low,
pick-up/put-down, seated back-to-rear TV turn, seated nap, rear brush and
pyjama bed-entry/sleep endpoints. `watch_tv.json` uses the new seated bridge;
`standard_bridge_review.json` exercises the reusable standard set. The exact
failure queue remains in `docs/KEEPER_NEUTRAL_ENDPOINT_AUDIT.md`, standard
first and then the costume-audit order. Its 300 current legacy failures are
frozen in `data/keeper_endpoint_exceptions.json`; any new failure or regression
fails `npm test`. Do not add an exception instead of drawing or repairing a new
sheet.

## Start here in the next task

1. Read this document in full.
2. Open `docs/keeper-scale-audit/review.html`. For a reliable no-Wi-Fi session
   on this Mac, double-click `Open Keeper Review Offline.command` at the
   repository root and leave its Terminal window open; it serves the same page
   and local sprite strips only on `127.0.0.1:8765`, while browser saves and the
   version-9 JSON export/import continue to work normally. Offline and online
   browser storage do not synchronise automatically: Export on one copy, then
   Import review JSON on the other. A dedicated panel first shows
   the untouched `keeper_walk` identity/anatomy baseline, followed by all 173 accepted
   clips at one unchanged relative scale in filename order. Filter the register
   by Needs my input, Happy, Awaiting new draft review, Review later,
   Unreviewed or Has Codex response. Switch View to `One animation at a time`
   for a much larger card. Previous/Next and Left/Right stay inside the active
   filter and wrap from its final result to its first. A compact reference stays
   pinned alongside; standing side/front/back and sitting side/front/back
   canons are available. These are fixed identity/anatomy comparison ghosts;
   they do not replace the saved production size of the reviewed clip.
3. Every card has a read-only Codex response field. All 68 `Awaiting new draft
   review` cards have a specific narrative naming the delivered production
   change. Any genuine qualification is stated explicitly; a generic response
   is not evidence that work was completed.
4. Frank's supplied exports are preserved byte-for-byte at
   `docs/review/frank-keeper-animation-review-2026-10-09.json` and
   `docs/review/frank-keeper-animation-review-2026-10-10.json`; do not edit or
   replace either file. The current complete 173-row disposition is
   `docs/review/KEEPER_ANIMATION_REVIEW_RESOLUTION_2026-10-10.md`, and agent
   responses live separately in the two dated
   `keeper-animation-codex-responses-*.json` files. The exact second-round
   comparison and implementation scope is recorded in
   `docs/review/KEEPER_ANIMATION_SECOND_ROUND_DELTA_2026-10-10.md`.
5. The display-size slider magnifies the reviewed stage from 1× to 12× without
   changing art. Global controls pause/play everything and apply pose-aware
   comparison ghosts.
   Every card also has Previous/Next frame controls. They pause playback,
   select the action itself and step without wrapping from frame 1 to the final
   frame; inspection alone does not alter or dirty the saved review. A prominent
   top-right pane badge continuously names the displayed clip and exact frame,
   including during playback; seam-freeze mode names both compared frames.
   The same control block has `Play animation` plus a `Play once`/`Loop`
   selector. It starts the reviewed action at frame 1, animates only that card
   and does not dirty the saved review.
   At browser widths of 1500px or more, focused mode uses the monitor width:
   pinned reference left, large viewport-height stage centre, and a compact
   two-column control console right. Amber means size, purple ghost, blue
   animation transform, teal frame navigation, and green/red review decisions.
   Display zoom and filter are saved immediately in browser-local progress.
   Saving or advancing from the final result wraps to the first result in the
   same filter.
6. For the next review round, ask Frank for the newly exported
   `keeper-scale-choices.json`.
   Each card's Save button persists independent width/height, rotation,
   horizontal/vertical position, ghost settings, opacity and the
   happy/not-yet-happy decision, free-text notes and full-re-draft request in
   his browser. Version 9 includes production proposals, the complete review
   register/statuses and the read-only Codex response, but it does not alter
   production art by itself.
7. Record every new comment by exact `keeper_*` filename before changing art.
   Triage it as `keep`, `fix`, `rebuild`, `delete`, or `decision needed`, and
   distinguish an art fault from a missing transition or missing object.
8. Resolve identity, anatomy and transition gaps against the untouched
   `keeper_walk` reference. Frank's saved visual width and height are the final
   production sizing instruction and must not be overruled by automatic
   measurement. Never resize merely to fit a canvas, prop, costume or object.
9. Rebuild, publish and rerun the complete all-sheet audit after every keeper
   art pass. It must finish with zero failures.

The per-card character-width and character-height sliders and adjacent ±0.5%
buttons reshape only the reviewed action around its declared feet/seat/contact
anchor. The untouched
reference, rulers, original ghost, matching walk and bridge clips remain at
100%, so Frank can judge the proposed shape against fixed evidence. Earlier
uniform percentages migrate to both axes. A saved proposal is not a production
change; ingest both exported percentages before rebuilding art.
Flying and swimming review clips align the bottom of their first-frame figure
to the red floor line. Pressing global Pause resets every card to frame 1 of its
action, even when a route or onion-skin mode is selected.
Seated cards automatically use the canonical direct-front, side or rear sitting
endpoint as their ghost; other cards use the standing reference. Each card can
override the ghost reference with a standing side, standing facing-front,
standing back-to-camera, sitting side, sitting front or sitting back figure, rotate it, reset
it, place it alongside on a wider stage and reduce only the reviewed animation's
opacity. The standing front ghost is the neutral arms-down frame 1 of
`keeper_wave_camera`; this is the same canonical front identity used as the
source for the exact-inheritance party idle. The standing
back ghost is frame 6 of `keeper_turn_back`, the audited standard-outfit rear
endpoint with the same 32 × 40 canvas, [16, 40] feet anchor and 38-pixel height
as the canonical standing keeper. The rear-sitting ghost is frame 6 of
`keeper_sit_back`, with the same standard uniform and `[16,29]` seat point as
the side and front sitting standards.
Every card has `Happy with this animation`, `Save this review`, `Save & re-review later`
and an explicit saved/unsaved state. The re-review button saves immediately and
advances in focused mode. Orange means unsaved; green means saved and happy;
blue means saved for later review. Export
is blocked until changed cards are saved. Existing browser-saved size choices
are loaded into the new workflow rather than discarded.
The reviewed animation itself can rotate from −180° to +180° around its fixed
review anchor, independently of ghost rotation. This is a comparison aid for
horizontal clips such as `keeper_anti_gravity`; its saved angle is included in
the review export and is not automatically a production-art instruction.
Every blue transform slider also has precise −0.5/+0.5 buttons: degrees for
rotation, logical pixels for horizontal/vertical position, and percentage
points for opacity. They share the slider limits and saved/exported values.

The exact human-readable clip inventory is in `docs/KEEPER_ANIMATIONS.md`.
The machine-readable runtime inventory is `public/sprites/manifest.json`.

## Non-negotiable rules

### Identity and scale

- `keeper_walk` is the untouched identity and baseline anatomy reference. The
  old modular parts and `keeper_reference` are not production references.
  Frank's saved review width/height is authoritative for the delivered size of
  each reviewed clip, including accepted costume families and redrafts.
- Every frame in a clip must depict the same man consistently: the same
  head/face, beard, shoulder-to-hip body, fatness, hand size and boot size.
  Perspective does not create an unrequested within-clip size change.
- Beard length and silhouette are identity-locked, not pose-dependent styling.
  Match the beard root, lower edge, width and chin relationship to the approved
  `keeper_walk` identity at the nearest comparable facing/head angle. Do not
  let the beard become longer or shorter between clips unless Frank's exported
  note explicitly requests a deliberate design change.
- A smooth, rounded or bulbous beard in side profile is a known recurring
  defect across multiple animations, not an isolated nap-animation problem.
  The canonical side beard has a stepped, slightly ragged outer and lower edge
  with the approved taper around the mouth and chin. Audit every frame of every
  left- or right-facing clip (including mirrored, seated, reclined and
  head-tilted poses) for this silhouette; nominally correct beard height alone
  is not sufficient.
- The corridor is effectively a flat, front-of-screen movement plane. Use the
  reviewed production size for each clip; do not add runtime perspective
  scaling unless a transition explicitly requires it.
- Measure the anatomical keeper, not the outer alpha box. Hats, helmets,
  sou'westers, raised arms, tools, props, water, furniture and privacy effects
  do not count toward body scale.
- Baseline anatomical measurements are locked in
  `data/keeper_asset_contract.json` and explained in
  `docs/KEEPER_ASSET_SCALE.md`: inferred skull top 32.5 logical
  pixels above the supporting sole, shoulders 24.5, hips 14.5, side core depth
  13, front/rear core width 19, head width 14.5, hand diameter 4 and boot length
  8. Landmark tolerance is 0.5 logical pixel; core-width tolerance is 1 pixel.
  These measurements diagnose source-art identity drift; they do not overrule
  Frank's saved visual resize.
- For an upright keeper wearing the normally seated standard cap, the gold cap
  badge crossing the blue skull-top guide is a calibrated, easy visual proxy.
  It is not valid for head tilt, bending, sitting, crouching, horizontal poses,
  bare heads or alternate headwear; those still require anatomical landmarks.
- Costumes, hats, handheld props and equipment are overlays on canonical body
  frames. Do not redraw the keeper because his clothing or prop changes. A new
  drawing is justified only by a genuinely new body pose; it must then pass the
  complete anatomy and identity audit.
- Never shrink him merely to fit a long pose or prop. Expand the transparent
  canvas, then apply Frank's saved visual size as a separate final instruction.
  This is the rule used for swimming, press-ups, fishing, weights, parachuting,
  diving, records, watering cans and long tools.
- The keeper's reviewed production pose is the ruler for the world. Objects
  move or change size to meet its transformed interaction points; automatic
  object fitting must never replace Frank's visual size.

### Transitions

- A clip is not gameplay-ready merely because its isolated frames look good.
  Every activity must have a seamless, reversible route from idle/walking into
  the activity and back to idle/walking.
- No route may contain a scale change, foot-anchor jump, body-width jump,
  facing snap, unexplained prop appearance, unexplained costume change or
  furniture/contact-point jump.
- Every clip needs declared `startPose` and `endPose`. Loops also need a clean
  loop seam. Reversed playback swaps the declared endpoints.
- The first and last body poses of a bridge/action must match the named neutral
  pose: exact supporting-foot/contact anchor and body landmarks within 0.5
  logical pixel, ignoring only a legitimately transferred prop.
- A `direct-test` label in the current viewer means only “same outfit and a
  plausible facing”. It is a candidate seam, not proof that the transition is
  acceptable.
- Left-facing side movement is normally a safe mirror of right-facing art, but
  the interaction point, held prop and object layout must mirror too. Do not
  mirror text, asymmetric machinery or unsafe hand choreography.

### Costumes and privacy

- Every costume change happens while the keeper is fully hidden behind a door.
  All relevant doors hinge on the player's side and render in front of him.
- The keeper enters in the old outfit; the foreground door creates full-body
  occlusion; runtime swaps outfit while no part of him is visible; he emerges
  in the new outfit. There is no visible morph or dressing animation.
- The party hat follows this rule. `keeper_party_hat_put_on_back` remains
  optional flavour/reference art, not required gameplay plumbing.
- Between rooms, use two hidden changes: costume to standard at the exit door,
  then standard to the target costume at the destination door. This keeps him
  in standard uniform on shared stairs, ladders, lift and slide.
- Bathroom privacy can use the same door/cubicle occlusion. Privacy mosaic,
  foam and towels are privacy states, not outfits, and should eventually move
  from manifest `outfit` to a separate `privacy` field.

## Current evidence and files

- 191 keeper sheets and 1,475 frames are in the technical review batch.
- 173 animation sheets are accepted into the review gallery.
- 18 obsolete modular/reference sheets are excluded from review and must not
  return to production.
- 81 sheets are recorded as rebuilt or anatomy-normalised in the latest full
  audit.
- The audit currently reports zero unresolved original-comparison failures.
- Imported review state is 96 Happy, 68 Awaiting new draft review, 3 Review
  later and 6 Unreviewed. “Awaiting new draft review” means the requested
  production work is now present and awaits Frank's verdict.
- Directly comparable full-body families without a saved visual resize are
  constrained to a 0.960–1.040 skull-to-sole ratio; unobscured side torsos
  without a saved visual resize must be within one logical pixel of the
  original torso scan. Reviewed sizing is recorded as
  `user-visual-size-authority`, not failed by this automatic gate.
- The permanent evidence is in `docs/keeper-scale-audit/`: nine fixed-scale
  contact sheets, `keeper-scale-metrics.json`, `keeper-scale-summary.csv` and
  the unified review page.
- Runtime sprites are under `public/sprites/`; authored source strips and JSON
  sidecars are under `art/raw/keeper-first-batch/`; deterministic authoring is
  in `art/source/keeper-first-batch/author_keeper.py`.
- Object scale and contact authority lives in
  `data/keeper_asset_contract.json`, `data/keeper_object_dimensions.json`,
  `docs/KEEPER_ASSET_SCALE.md` and `docs/KEEPER_OBJECT_DIMENSIONS.md`.
- The non-standard-outfit inventory and next bridge batch are in
  `docs/KEEPER_COSTUME_ROUTE_AUDIT.md`.
- Frank's first and second animation reviews are preserved byte-identically in
  the dated files under `docs/review/`. Their SHA-256 values are respectively
  `c19129f8419df2c046f3abb06de9f339f1cd8edb31c2d505dea8e79562d5f486` and
  `e72a6ddf3e7c30e3093195b5044ebd2b9d9af62ba94c9e493158af49b1e7ace7`.
  New review comments must be captured as another dated export rather than
  silently overwriting either one. Earlier floor-catalogue evidence remains in
  `docs/review/frank-floor-review-2026-10-09.json`.

## The route every ordinary activity needs

The controller, not the furniture, should assemble this graph:

```text
idle/standing
  <-> walk start <-> walking <-> phase-aware walk stop
  <-> optional facing turn
  <-> optional posture change (sit/crouch/prone/climb)
  <-> optional prop acquire / object handover
  <-> action entry <-> action loop <-> action exit
  <-> prop release
  <-> reverse posture/facing bridge
  <-> standing/walking
```

The common named poses should be explicit rather than inferred from filenames:

- `stand-side-right` and mirrored `stand-side-left`
- `stand-front`
- `stand-back`
- `walk-side-right/left`, including gait phase/lead foot
- `seated-side-right/left`
- `seated-front`
- `seated-back` or rear three-quarter
- `crouched-side`, `crouched-front`, `crouched-back`
- `prone-horizontal`
- `lying-bed`
- ladder/stair top and bottom contacts
- water-edge, swimming-horizontal, swimming-up and swimming-down
- `hidden`, used only while a foreground door/cubicle fully occludes him
- carry poses such as `carry-tray`, `carry-bags`, `carry-mug` and `carry-tool`

### Essential transition clips, in implementation order

#### P0: needed before any large-scale gameplay wiring

1. **Production neutral/idle poses.** The old `keeper_idle` was rejected. Make
   an accepted standard side neutral, plus front and back neutrals as required.
   Every costume that is visible while standing also needs an inherited neutral
   pose based on the matching canonical body, not a mid-stride walk frame.
2. **Phase-aware walk start and stop, right and mirrored left.** Either author
   two settle variants for the two lead-foot phases or have the controller wait
   for the compatible gait phase before playing the correct settle. Do not snap
   any arbitrary walk frame directly to a single standing frame.
3. **Side ↔ front turn** and **side ↔ back turn**, reversible and mirrored where
   safe. `keeper_turn_back` exists but needs a true endpoint/seam audit. A
   general side-to-front bridge is still missing.
4. **Pose metadata and route validation.** Add `startPose`, `endPose`, facing,
   outfit, anchor, movement vector and legal bridge data to the manifest or an
   authoritative sidecar. The game must reject a route with unmatched poses.
5. **Seam checks.** Add a fixed-frame onion-skin comparison for every legal
   handover and a test that every activity has a path from standing/walking and
   back. A clean isolated loop is insufficient.
6. **Object/prop events.** Declare the exact frame where an object is acquired,
   released, switched, opened, hidden or transferred. Props may appear or
   disappear only at a declared handover or full occlusion.

#### P1: shared posture bridges

7. `stand-side ↔ seated-side`, mirrored left/right. `keeper_sit_side` exists;
   verify exact endpoints and reuse it in reverse to stand.
8. `stand-front ↔ seated-front`. `keeper_sit_front` exists; verify endpoints and
   reuse it in reverse.
9. Add a true rear/rear-three-quarter seating route where the activity requires
   it. Do not automatically route rear drumming, rear writing or TV/movie poses
   through a generic side sit unless their endpoints really match.
10. `stand-side ↔ crouched-side`, `stand-back ↔ crouched-back`, and front crouch
    only where gameplay needs it. Digging, feeding, sowing and harvesting need
    visible bend-down and straighten-up bridges.
11. Reversible reach/withdraw joins for switches, barometers, lift buttons,
    doors and similar controls, with hand height and object contact exact.
12. Costume-specific turns, sits or crouches only when an activity needs them.
    The door hides the clothing change, but it does not remove the need to move
    naturally after the keeper emerges.

#### P1: complete object/action chains

- **Cake:** walk/stop → turn back → retrieve from oven → turn holding cake →
  carry walk → place on 19 px table datum → release → straighten empty-handed
  → return to walk. Keep the approved cliché cake: two sponge layers, jam
  sandwich, white icing and one central cherry.
- **Plated meal:** the same complete chain, with plate and meal preserved
  throughout carry and placement.
- **Hot drink:** empty-handed stand → acquire kettle → pour → visibly lower and
  put kettle down → stir → pick up mug → drink → put mug down → empty-handed
  stand. Kettle, cup, hand and worktop positions must not merge between frames.
- **Shopping:** acquire two bags → carry walk → put both bags down → straighten
  empty-handed. The existing carry has two hands; pickup and set-down still need
  explicit routes if no object occlusion supplies them.
- **Record:** acquire record → hold by its edge → lay it flat on the platter →
  release → withdraw empty hand. No cropped record and no unexplained prop pop.
- **Tools:** approach → acquire tool at its station or begin with hand hidden at
  the tool rack → action → replace/release tool → withdraw → stand. This covers
  welding, sawing, hammering, machete, fishing, painting and cleaning tools.
- **Table/chair activities:** approach an object-owned marker → stop/turn → sit
  → loop → reverse sit/stand → leave. Seat height is always 11 px above floor;
  dining/writing/kitchen surfaces are 19 px.
- **Doors:** approach → phase-aware stop → reach/open or automatic open → pass
  under foreground leaf/mask → optional hidden costume swap → emerge/close.
  Side left/right and direct rear object layouts must match the hand/handle.
- **Bath/shower:** bathrobe approach → foreground door/cubicle occlusion →
  private entry/wash/exit states → towel or bathrobe emergence. No uncovered
  body-transition frame is allowed.
- **Boat:** use the dedicated `keeper_boat_enter` and `keeper_boat_exit`, aligned
  to the gunwale and bench. Do not substitute generic sitting unless the seam
  is proven. Rowing, speedboat and outboard actions need their own seated/hand
  handovers and a route back to the dock.
- **TV/movie/video game:** use the rear three-quarter seating offset that leaves
  the screen visible. Chair/sofa geometry, recline and sightline must be built
  from the keeper's seat and look points.

#### P2: special locomotion and environment entries

- Straight stairs: bottom approach/landing, ascent/descent and top exit.
- Spiral stairs: bottom/top mounts and exits for both up and down clips.
- Ladder: mount/dismount at both floor and upper landing; reverse climb only if
  hand/foot order still reads correctly.
- Slide: sit/launch, slide and landing/stand.
- Platform dive: walk/stop at board → ready → full head-first dive → splash and
  water entry → directional swim; also provide the water-exit route.
- Swimming/scuba: hidden costume/equipment change, then
  `keeper_scuba_walk_side` along the jetty → `keeper_scuba_jetty_dive` → exact
  hand-off to `keeper_scuba_swim_horizontal`; directional turns, ladder/edge
  exit and the hidden change back are still required at runtime.
- Parachute: platform approach → `keeper_parachute_jump` deployment → optional
  repeat of `keeper_parachute_drift` for the required fall height →
  `keeper_parachute_landing` → stand. The neutral open-canopy hand-off frame is
  byte-identical at both clip boundaries.
- Anti-gravity: chamber entry/door closure, float takeoff, prone goggle loop
  with back flip, settle, landing and chamber exit. Never show a parachute.
- Boat: dock approach plus dedicated climb in/out as above.

## Current transition inventory

These labels are generated into the review page. They describe the current
evidence, not final acceptance.

| Kind | Count | Meaning |
|---|---:|---|
| `bridge-clip` | 11 | Existing reusable bridge artwork |
| `direct-test` | 51 | Same-outfit walk can be juxtaposed for review; seam unproven |
| `known-bridge` | 47 | Viewer can insert an existing turn/sit/bed/water bridge; full route still needs endpoint proof |
| `locomotion` | 13 | Walking source/family |
| `missing-bridge` | 33 | Known facing/posture bridge does not exist |
| `no-walk` | 15 | Outfit/privacy state has no walking family; may instead require an occlusion route |
| `special-entry` | 3 | Air/water/horizontal action needs a bespoke environment entry |

### Existing bridge clips (11)

- `keeper_turn_back`
- `keeper_sit_side`
- `keeper_sit_front`
- `keeper_get_into_bed`
- `keeper_party_hat_put_on_back` — optional flavour only under the door rule
- `keeper_artist_smock_turn_back`
- `keeper_artist_smock_turn_front`
- `keeper_artist_smock_sit_front`
- `keeper_scuba_jetty_dive`
- `keeper_parachute_drift`
- `keeper_parachute_landing`

### Locomotion families (13)

- `keeper_walk`
- `keeper_bathrobe_walk`
- `keeper_pyjamas_walk`
- `keeper_party_walk`
- `keeper_souwester_walk_side`
- `keeper_knight_walk_side`
- `keeper_spaceman_walk_side`
- `keeper_pirate_walk_side`
- `keeper_tarzan_walk_side`
- `keeper_halloween_walk_side`
- `keeper_mechanic_walk_side`
- `keeper_artist_smock_walk`
- `keeper_scuba_walk_side`

### Missing facing/posture bridges (33)

- Side/front reactions and actions: `keeper_bored`, `keeper_cross`,
  `keeper_dance`, `keeper_hungry`, `keeper_lift_button_front`, `keeper_sad`,
  `keeper_water_plants_front`, `keeper_wave_camera`.
- Crouch/straighten: `keeper_dig`, `keeper_feed_animals`,
  `keeper_pick_vegetable`, `keeper_sow_seeds`.
- Outfit side/back/front connections: `keeper_halloween_walk_back/front`,
  `keeper_knight_walk_back/front`, `keeper_mechanic_walk_back/front`,
  `keeper_pirate_walk_back/front`, `keeper_souwester_walk_back/front`,
  `keeper_spaceman_walk_back/front`, `keeper_tarzan_walk_back/front`.
- Party: `keeper_party_dance`, `keeper_party_eat_cake`, `keeper_party_idle`,
  `keeper_party_turn_back`. Recheck the exact routing label on the party turn;
  the current generated wording is not a substitute for a pose-endpoint test.
- Pyjamas: `keeper_pyjamas_turn_back`.
- Bathrobe/shower: `keeper_shower_door_open_bathrobe`,
  `keeper_shower_enter_bathrobe`.

### States without a walking family (15)

- Bath/shower/privacy: `keeper_bath_enter`, `keeper_bath_exit`,
  `keeper_bath_wash`, `keeper_hot_tub`, `keeper_shower_enter`,
  `keeper_shower_exit`, `keeper_shower_wash`. These may be valid through full
  door/tub/cubicle occlusion rather than requiring a towel walk.
- Winter: `keeper_clear_snow`.
- Workout kit: `keeper_lift_weights_back`, `keeper_pressups_side`,
  `keeper_ride_bike_front`, `keeper_trampoline_front`.
- Striped swimsuit: `keeper_swim_costume_down`,
  `keeper_swim_costume_horizontal`, `keeper_swim_costume_up`.

The artist-smock family now has its reviewed-size walk, front/rear turns and
front sit/stand bridge. For winter/workout clothing, author canonical-overlay
neutral and walking/turning coverage where he traverses visible room space.

### Garden shed and lawn mower route

`keeper_lawn_mower_push` is an eight-frame, standard-uniform, baseline-anatomy
right-facing loop; runtime mirroring supplies left. The manual reel mower is
part of the animated strip so wheel/step timing cannot drift. The shed is not
baked into the sprite: start the complete moving unit behind the shed door's
foreground layer, translate it into view, and keep that occluder in front until
the keeper and mower have cleared the doorway.

### Cleaning cupboard and three-tier tool route

The `broom` upgrade family now selects one of three eight-frame,
standard-uniform, baseline-anatomy right-facing loops; runtime mirroring
supplies left:

- tier 1 `keeper_sweep_broom`, with a traditional wooden broom;
- tier 2 `keeper_hoover_basic`, with an ordinary upright hoover;
- tier 3 `keeper_hoover_super`, with an original eccentric brass-and-teal
  inventor machine, pressure gauge, bellows and powered brushes.

Each tool is part of every animation frame so hands, wheels/bristles and steps
cannot drift apart. Fetching and returning uses the mower rule: approach the
cupboard with `keeper_walk`, put the keeper wholly behind the cupboard door's
foreground layer, swap to the selected keeper-plus-tool clip only while fully
hidden, and translate the complete unit back into view. Reverse that route
when cleaning ends. Never bake the cupboard into a keeper strip and never
show a visible tool morph or pop.

All three clips use the standard uniform, so this is equipment routing rather
than a new costume family. The non-standard outfit audit therefore gains no
new missing walking or turning requirement.

## Artist-smock and guitar routes added in this pass

- Artist: `keeper_artist_smock_walk` → optional
  `keeper_artist_smock_turn_front` → `keeper_artist_smock_sit_front` →
  `keeper_pottery_front`; painting uses the same walk and the side or rear turn
  before `keeper_paint_side` / `keeper_paint_back`. Each one-shot reverses only
  where the endpoints are identical.
- The smock walk's generated frame 4 was undersized. Every production frame is
  now independently height-matched to the corresponding canonical walk pose,
  and the full walk passes the direct height and torso-width gates.
- Guitar tier 1 is acoustic, tier 2 is the black Gretsch and tier 3 is the red
  1967 Flying V. Each tier has a 12-frame rack-pickup one-shot and its own
  eight-frame playing loop.
- Pickup clips start in the canonical side stance, turn fully rearward, reach
  the separate rack, acquire the instrument on one-based frame 6, turn back
  and end on the exact first frame of their matching play loop. Runtime must
  hide/remove the rack prop on `propHandoffFrame`; it must not infer transfer
  from alpha pixels.
- The Gretsch source was enlarged after all eight original figures were marked
  undersized. Production remains canonically measured rather than scaled by
  its transparent source canvas.

Scuba now uses the explicit visible-water route
`keeper_scuba_walk_side` → `keeper_scuba_jetty_dive` →
`keeper_scuba_swim_horizontal`. The equipment change before that walk and the
change back after water exit must still happen under full door/locker
occlusion; never jump directly from standard walking to a horizontal swimmer.

### Special entries (3)

- `keeper_anti_gravity`
- `keeper_platform_dive`
- `keeper_slide_side`

### Known-bridge routes (36)

- Rear turn routes: `keeper_bbq_back`, `keeper_cake_from_oven_back`,
  `keeper_cake_turn_right`, `keeper_check_instrument_back`,
  `keeper_collect_eggs_back`, `keeper_crouch_work_back`, `keeper_hammer_back`,
  `keeper_lean_table_back`, `keeper_meal_from_oven_back`,
  `keeper_operate_outboard`, `keeper_search_boxes`,
  `keeper_spiral_stairs_down`, `keeper_spiral_stairs_up`,
  `keeper_switch_press_back`, `keeper_vomit_loo_back`,
  `keeper_water_plants_back`.
- Seated routes: `keeper_boat_enter`, `keeper_boat_exit`,
  `keeper_count_money`, `keeper_drink_pint`, `keeper_drive_speedboat`,
  `keeper_eat_seated`, `keeper_fish_seated`, `keeper_piano`,
  `keeper_play_drums_back`, `keeper_play_drums_front`, `keeper_read_front`,
  `keeper_read_side`, `keeper_row_boat`, `keeper_type_computer`,
  `keeper_video_game`, `keeper_watch_movie`, `keeper_watch_tv`,
  `keeper_write_back`, `keeper_write_side`.
- Bed route: `keeper_pyjamas_snore` via `keeper_get_into_bed`.

The boat entries and several rear-seated activities are especially important
to reclassify after endpoint testing; the viewer's generic sit bridge is not
automatically the correct physical route.

### Direct seam candidates (47; not yet certified)

`keeper_aquarium_brush`, `keeper_aquarium_net`, `keeper_bowling`,
`keeper_brush_teeth_back`, `keeper_carry_cake`, `keeper_carry_meal`,
`keeper_carry_shopping`, `keeper_check_instrument_side`, `keeper_cook_back`,
`keeper_darts`, `keeper_door_open_back`, `keeper_door_open_side`,
`keeper_fish_feed_up`, `keeper_fish_standing`, `keeper_hammer_side`,
`keeper_hot_drink_drink`, `keeper_hot_drink_pickup`,
`keeper_hot_drink_pour`, `keeper_hot_drink_put_down`,
`keeper_hot_drink_stir`, `keeper_ladder_climb`, `keeper_machete_side`,
`keeper_meal_place_side`, `keeper_mechanic_fix`, `keeper_parachute_jump`,
`keeper_pick_fruit`, `keeper_place_cake`, `keeper_play_guitar`,
`keeper_put_record`, `keeper_saw_wood`, `keeper_snooker`,
`keeper_spiral_stairs` (legacy alias), `keeper_stairs_down`,
`keeper_stairs_up`, `keeper_switch_press_side`, `keeper_table_tennis`,
`keeper_telescope`, `keeper_urinate_back`, `keeper_wash_back`,
`keeper_water_plants_side`, `keeper_weld`, `keeper_work_back`, `keeper_yawn`.

Audit every one in pause/onion-skin mode. Some rear-facing items in this list
are likely misclassified until `startPose`/`endPose` replace filename/facing
heuristics.

## Object binding: what an asset must declare

Do not give an oven a hard-coded instruction to “play frame strip X”. Give the
object an interaction profile and let the keeper controller construct the legal
route. Each interactive object needs, at minimum:

- semantic interaction/action ID;
- world-space approach point for the keeper's feet;
- required approach facing and permitted mirrored layout;
- keeper hand, seat, look, ground or tool contact point;
- required outfit and privacy state;
- required named start/end pose;
- action loop and entry/exit recipe;
- exact frame events for prop acquire/release and object state changes;
- foreground/background layer and any door/object occlusion mask;
- movement vector or root-motion rule;
- whether reverse playback and mirroring are safe;
- loop speed and whether interruption is allowed;
- recovery/fallback if the object is moved, blocked or unavailable.

A proposed shape—not yet implemented—is:

```json
{
  "interaction": "place-cake",
  "approach": { "feetPoint": [0, 0], "facing": "right" },
  "keeperContact": { "kind": "table", "heightAboveFloor": 19 },
  "requiredOutfit": "standard",
  "entryPose": "carry-tray-right",
  "action": "keeper_place_cake",
  "exitPose": "stand-side-right",
  "events": [
    { "name": "release-cake", "frame": 5 }
  ],
  "mirrorSafe": true
}
```

The exact schema should be settled with the runtime implementation, but the
data must remain object-relative and based on the existing keeper contract.

## Complete requested animation scope

The following is the durable record of what Frank requested. The majority has
art in `docs/KEEPER_ANIMATIONS.md`; “delivered” never waives transition review.

### Core movement and interaction

- Standard walk right and mirrored left.
- Turn to back and return to camera/front.
- Rear work with visibly animated arms as the reusable proxy for washing,
  cooking and lamp polishing.
- Separate urination pose with hands down at the groin.
- Sit/get up side left/right and facing camera, including sofa and toilet use.
- Eat while seated, with cutlery moving from table surface to mouth.
- Piano and other seated instruments.
- Open/close doors side left/right and back-to-camera.
- Climb ladder up/down; straight stairs up/down; spiral stairs up/down.
- Reach for switch/control side left/right and back, with identical hand height
  in side and back views; front lift-button press.
- General walk-stop, turn, sit, crouch, carry, climb and object-handover
  transitions described above.

### Adventure, water and transport

- Parachute jump with parachute visibly deploying from the back.
- Platform dive in a traditional full-length red/white striped swimsuit, no
  hat, ending fully head-first with arms extended.
- Matching scuba versions; horizontal/up/down swimming in swimsuit and scuba.
- Row boat, drive speedboat, operate outboard motor, climb into/out of boat.

All multi-frame keeper animations are now authored at a global 4fps baseline.
Runtime animation speed remains clip-specific manifest metadata, and the shared
sprite renderer reads it independently for each animation. Faster accepted
review choices belong in `KEEPER_FPS_OVERRIDES` in `author_keeper.py`; rebuilding
then writes those values to the source sidecars and runtime manifest.
The unified review page therefore exposes a separate 1–20fps proposed game-speed
slider for every action, with 0.5fps fine controls, an authored-speed reset and
a live cycle-duration readout. The chosen `animationFps` saves and exports with
the card. It affects only the reviewed action during seam previews, leaving the
approach walk and bridge at their own authored speeds (currently also 4fps by
default). When Frank returns the
export, write accepted values into the corresponding
`art/raw/keeper-first-batch/*.json` source sidecars and rebuild
`public/sprites/manifest.json`; the PNG sprite strips themselves do not contain
timing. This keeps later in-game tuning to a metadata edit rather than a redraw.
- Fishing standing and seated, including reeling in a fish.
- Anti-gravity flight: on his front in goggles, bobbing/circling and performing
  a back flip, with no parachute.
- Ride down slide.

### Garden, animals and outside work

- Dig garden; sow seeds; pick vegetables and fruit.
- Feed animals by bending to place food in a bowl; reuse for chickens, cat/dog.
- Collect eggs in a low rear crouch.
- Water plants in all directions.
- Chop plants with a machete.
- Clear snow with a shovel in a thick winter coat.

### Domestic life, food and objects

- Carry shopping bags.
- Retrieve cake from oven from the rear, turn left/right, walk carrying it,
  place it on a table, release it and straighten again.
- Cake design: two sponge layers, jam in the middle, white icing and one cherry
  centred on top.
- Retrieve/serve a plated meal with the same carry/place/straighten completeness.
- Make tea/coffee: kettle to mug, put kettle down, stir, pick mug up, drink and
  put mug down.
- BBQ from the rear.
- Feed fish by reaching up; clean fish tank with brush and net/caught fish.
- Brush teeth from the rear.
- Bath and shower entry/washing/exit, with opaque blur/coverage from stomach to
  knees and towel on exit; bathrobe walk, shower-door opening and cubicle entry.
- Soak in hot tub.
- Vomit into toilet from the rear.
- Search boxes; lean over table; check wall instrument/barometer.
- Put a record flat on a turntable platter.
- Count money.

### Work, making and repair

- Weld; saw wood; hammer on workbench side and rear.
- Paint side/rear and use potter's wheel seated front, wearing a paint-splodged
  artist's smock.
- Type at computer, reusing the piano hand rhythm where appropriate.
- Fix car/boat in mechanic clothing.

### Leisure, music, sport and reactions

- TV watching slightly offset rear-left/rear-right so the screen stays visible;
  seating must match.
- Movie watching more reclined, eating popcorn.
- Dance; guitar; drums seated front and rear as the same motion rotated 180°.
- Read book seated side/front; write side/rear; telescope.
- Snooker, table tennis, darts and ten-pin bowling.
- Trampoline, rear weights, side press-ups and front stationary exercise bike.
  All use old-school workout kit: headband, vest, shorts, socks and trainers.
  The exercise bike is a separate static object, never drawn into actor frames.
- Video game while holding controller, based on TV seating.
- Drink beer from a traditional handled pint glass.
- Wave to camera and yawn.
- Sad facial/body reaction; hungry with tummy rub; bored with foot tap; cross
  with angry face/folded arms or stamp.

### Clothing families

- Light powder-blue pyjamas: side walk left/right, side-door opening/closing,
  turn rear, get into bed and snore. `keeper_door_open_side_pyjamas` is a clean
  six-frame redraw following the standard side-door progression and retaining
  its `(25,20)` handle point. It must be visibly lighter than the normal uniform.
- Full yellow sou'wester: side/rear/front movement.
- Party: a small pale-pink conical cardboard hat with red fringe and pom-pom,
  never the previously oversized cone; canonical keeper face/body; idle, walk,
  turn, cake eating and dancing. Hat is an overlay, not a new keeper.
- Knight armour, spaceman, pirate captain, family-friendly Tarzan, Halloween
  costume and mechanic: canonical side/rear/front movement.

### Lift depth transition

- `keeper_walk_into_lift` is the deliberate exception to the otherwise fixed
  within-clip actor scale. Frames 1–5 walk directly away while shrinking from
  100% to 75% and rising 6 logical pixels into the rear lift. Frames 6–8 retain
  the 75% depth scale while turning through three-quarter to a full-front,
  arms-down neutral endpoint. The baked change is recorded as
  `depthScaleRange: [1.0, 0.75]` and `depthOffsetY: [0, -6]`; do not “correct”
  it back to a common per-frame height during scale review.
- Costume changes are always door-hidden, as defined above.

## Correction history that must not regress

The following user-reported faults were addressed in the latest authored
batch. New comments may still reject the aesthetic result, but none of these
technical regressions may return:

- rear crouch restored to canonical width; both hands work in front;
- back switch press hand matches the side press height;
- dive extended to true vertical head-first pose; parachute gained a canopy;
- pyjamas made lighter blue;
- fitness clips use one old-school kit; press-ups, weights and bike were restored
  to canonical scale; the bike itself was removed from actor art;
- cake/meal carry walks and table placement/straightening added; cake replaced
  with the approved jam/icing/cherry design;
- swimsuit horizontal and all three scuba directions rebuilt to canonical
  anatomy; long swimmers use an 80 × 48 canvas rather than being shrunk;
- spiral-stairs-down frame 4 third hand removed;
- all Tarzan views and the front exercise-bike keeper rebuilt to scale;
- shopping third-hand fault removed;
- records, watering can, plated meal and machete expanded/adjusted to avoid
  right-edge cropping; machete no longer turns into a saw;
- front/rear drumming share scale, contacts and timing;
- party face/body inherits the canonical keeper; hat reduced and treated as an
  overlay; cake eating and dancing use the same rule;
- hot-drink drink/put-down and snooker frames isolated so neighbours do not
  bleed/merge; kettle hand/cup placement fixed and pour includes kettle set-down;
- anti-gravity frames reordered and rebuilt as prone goggle float/back flip with
  no parachute;
- front sit width, bath/hot-tub anatomy, costume families and standing fishing
  were normalised;
- no keeper is regenerated solely for a prop or costume.

The comprehensive per-sheet correction list is in
`docs/keeper-scale-audit/README.md`.

## Review-comments workflow for a later feedback round

1. Obtain Frank's newly exported `keeper-scale-choices.json` and read every saved
   per-animation note before triage or drawing. A full-re-draft flag authorises
   rebuilding the clip; it never authorises ignoring that clip's written notes.
   Treat beard-length and side-silhouette comments as identity corrections that
   must be checked frame by frame against `keeper_walk` and the nearest approved
   side-pose reference. Specifically flag smooth/bulbous outlines that lose the
   canonical stepped, slightly ragged margins. Prefer exact filenames from the
   review cards.
2. Save a dated, immutable source copy under `docs/review/`, then create a
   working resolution table with columns: filename, frame(s), comment, class,
   decision, proposed change, status, verification and commit.
3. Check whether each comment concerns identity/scale, drawing quality,
   frame-order/timing, crop/bleed, object geometry, or route/transition.
4. Delete rejected/obsolete art from the review/runtime inventory rather than
   leaving it available for accidental use; keep provenance/history only where
   needed to rebuild or understand a replacement.
5. Resolve P0 neutral/walk-stop/turn metadata and art before bulk object wiring.
6. Test complete routes, not just actions: walk in, settle, turn/posture change,
   act, reverse/exit and walk away.
7. Rerun all verification, inspect the viewer with global pause and ghost, and
   update this handoff plus the ordinary animation index before pushing `main`.

## Rebuild and verification

Use the bundled workspace Python runtime when available. The intended sequence
after art/source changes is:

```sh
python3 art/source/keeper-first-batch/author_keeper.py
npm run sprites
python3 scripts/audit_keeper_scale.py
python3 scripts/verify_floor_asset_catalogue.py
npm test
npm run typecheck
npm run build
```

Also inspect `docs/keeper-scale-audit/review.html` visually:

- every one of the 173 accepted cards is present and named;
- all seven review-state filters show the expected subset;
- filtered Previous/Next and Left/Right navigation wrap at both ends;
- each card has a read-only Codex response box, blank where no response exists;
- global Pause and Original-ghost controls affect every card;
- each card's ghost mirror, rotation and position choices save and export independently;
- no card scales its sprite to fit;
- all directly comparable bodies retain identity and scale;
- first/last/loop seams and complete routes are checked in frozen onion-skin;
- props and costumes change only at declared handovers or full occlusion.

## Ready-to-paste opening prompt for the new Codex task

> Continue the keeper-animation review in `/Users/frank/Documents/ChatGPT/Lighthouse Keeper` on `main`. Read `docs/KEEPER_ANIMATION_HANDOFF.md`, `docs/review/KEEPER_ANIMATION_SECOND_ROUND_DELTA_2026-10-10.md` and `docs/KEEPER_COSTUME_ROUTE_AUDIT.md` before changing anything. Frank's immutable 2026-10-09 and 2026-10-10 source reviews, current 173-row resolution register and separate dated Codex responses are under `docs/review/`; preserve them and capture any new export as a separately dated immutable record. Compare by exact `keeper_*` name, never list position. Treat Frank's saved width/height as authoritative and untouched `keeper_walk` plus the canonical sitting references as identity/anatomy authorities. Preserve source-cell isolation, exact scuba and parachute hand-offs, cleaning cupboard occlusion, seated nap, mower shed, artist-smock and guitar frame-6 hand-off. Rerun the full 191-sheet/1,475-frame scale audit and project verification, update the documentation, commit and push the completed work to remote `main`.
