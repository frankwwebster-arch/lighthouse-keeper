# Keeper scale and interaction contract

The keeper is the measuring stick for every room, prop and interaction. The
authoritative machine-readable data is `data/keeper_asset_contract.json`; this
page explains it in ordinary language.

## Baseline anatomy and reviewed production size

- One logical pixel is four source-image pixels (`density: 4`).
- The normal keeper canvas is 32 × 40 logical pixels with his feet anchored at
  `(16,40)`.
- The approved eight-frame side walk is the identity and baseline-anatomy
  reference. The old modular `keeper_reference` drawing is not a production
  reference.
- Frank's saved per-animation width and height are the final production sizing
  authority. They are applied after source anatomy normalisation, recorded as
  `reviewScale` in each reviewed sidecar and must not be replaced by an
  automatic measurement. The baseline measurements below remain useful for
  identity, proportion and contact diagnostics.
- His inferred skull top is 32.5 logical pixels above the supporting sole.
  The ordinary cap makes the visible silhouette 36.5–38 pixels high, but cap,
  party hat, helmet, sou'wester, raised hands, tools and props are never part of
  the body measurement.
- Canonical secondary checks are: eye line 28.5 px, shoulders 24.5 px and hips
  14.5 px above the floor; side core depth 13 px; front/rear core width 19 px;
  head width 14.5 px; hand diameter 4 px; boot length 8 px. Anatomical landmark
  tolerance is 0.5 px and core-width tolerance is 1 px.
- Beard length, lower-edge silhouette, width and its relationship to the chin
  are fixed identity features. Compare every newly drawn or rebuilt frame with
  `keeper_walk` at the closest facing/head angle; posture, costume and props do
  not justify a longer or shorter beard. Per-animation exported notes remain
  authoritative for identifying the clips and frames that require correction.
- Side-on beards require a full-library, frame-by-frame audit: several clips
  have made the beard too smooth, rounded or bulbous. Preserve the canonical
  stepped, slightly ragged outer and lower margins and its taper around the
  mouth and chin in left-facing, right-facing and mirrored frames, including
  seated, reclined and head-tilted poses.
- The vertical dive starts from a 48 × 56 canvas with anchor `(24,56)`. Full
  parachute deployment starts from 48 × 84 with anchor `(24,84)`. Transparent
  space is expanded before the saved review sizing is applied.
- Bed entry and snoring use 48 × 40 with anchor `(24,40)` so the horizontal
  body fits without rescaling.
- Press-ups use a 64 × 40 extended horizontal canvas. Their 47–52 px changing
  silhouette is checked together with the canonical head height, core depth
  and articulated body-axis landmarks; silhouette width alone is not scale.
- Fishing now starts from a 96 × 88 interaction canvas with anchor `(48,56)` so
  the rod, line, float and catch can extend below the feet. Frank's saved sizing
  may expand the delivered canvas further; for example, seated fishing is
  delivered on 135 × 115 after its 139% × 130% review scale.
- Left/right swimming uses an 80 × 48 canvas and movement anchor `(40,24)` so
  the horizontal body keeps canonical scale without width-fitting shrinkage;
  every frame must retain at least 32 logical pixels of visible actor thickness.
  Up/down swimming remains centred
  on 48 × 48 at `(24,24)`. Party headwear uses 32 × 48 with feet anchor `(16,48)`.
- Costumes, hats, handheld props and equipment are overlays on approved
  canonical keeper frames. They never justify regenerating the actor. Only a
  genuinely new body pose may be newly authored, and it must pass the full
  anatomy audit before acceptance. The party clips inherit their body and
  motion from the relevant wave, walk, turn, rear-work/raised-arm, seated-eat
  and dance families; only the hat/cake prop layers change. Contract version 7
  enforces this project-wide rule.
- Never scale the keeper automatically to make him meet an object. Apply
  Frank's saved size, transform the interaction points with it, then position
  and size the object from those delivered points.
- Never scale a crouched, seated, horizontal or prop-carrying silhouette to fill
  its canvas. Measure the articulated skull–shoulder–hip–sole chain and head
  unit, then enlarge the transparent canvas if a prop or limb needs more room.

## Mandatory original-comparison audit

Every keeper delivery must run the audit again over all sheets; a previous
`corrected` label is evidence of history, not permission to skip the check.
Run the authoring script first when source art changes, publish runtime sprites,
then run `scripts/audit_keeper_scale.py` with the bundled Python runtime.

The audit uses the untouched approved `keeper_walk` as its primary reference:

1. It measures every frame in all 191 sheets (1,475 frames at present).
2. It prints the original first in every contact-sheet row, followed by the
   tested sheet's first, middle and last representative frames at exactly the
   same fixed scale. No image is fitted to its available canvas.
3. Directly comparable full-body walks without a saved visual resize receive a
   fail-closed skull-to-sole ratio check. They must be 0.960–1.040 of the
   original's 38 px visible maximum or the audit command exits unsuccessfully.
   Unobscured side walks without a saved resize also receive a torso-width scan
   and must remain within 1 logical pixel of the original. A saved review scale
   is reported as `user-visual-size-authority`, not failed by this gate.
4. Costumes with headwear and compressed/rotated actions are checked with the
   canonical head unit, core width and articulated skull–shoulder–hip–sole
   landmarks. Hats, tools, props, water and raised limbs remain excluded.
5. Every accepted sheet records its method, original reference, verdict and
   warnings in `keeper-scale-metrics.json`; verification requires zero failures
   and refuses reports that omit an animation.

Open `docs/keeper-scale-audit/review.html` and select **Original ghost on** to
overlay the untouched original behind any clip without resizing either one.
The nine printable contact sheets remain the permanent evidence for the
complete visual pass.

The coordinate origin is the top-left. X increases rightward and Y increases
downward. A side-facing point at X mirrors with `mirroredX = canvasWidth - X`.

## Object placement heights

| Object or surface | Height above his foot line | Authoritative keeper point |
|---|---:|---:|
| Light switch / small wall button | 23 px | side `(27,17)`; rear `(26,17)` |
| Door handle | 20 px | side `(25,20)`; rear `(24,20)` |
| Rear worktop / basin / cooker | 19 px | `(16,21)` |
| Chair, sofa or toilet seat | 11 px | `(16,29)` |
| Animal food bowl target | 6 px | side `(27,34)` |
| Soil contact for spade | 2 px | side `(27,38)` |
| Seed-scatter target | 6 px | side `(27,34)` |
| Low vegetable harvest | 4 px | side `(26,36)` |
| Fruit harvest | 26 px | side `(25,14)` |
| Welding contact | 18 px | side `(27,22)` |
| Sawing contact | 17 px | extended side canvas `(35,23)` |
| Bed mattress surface | 9 px | extended bed canvas `(24,31)` |
| Fish-feed opening / tank top | 41 px | raised canvas `(26,7)` |
| Aquarium brush target | 23 px | extended side canvas `(34,17)` |
| Aquarium net target | 19 px | extended side canvas `(34,21)` |
| Hammering workbench | 17 px | extended side canvas `(32,23)` |
| Writing surface | 19 px | extended side canvas `(34,21)` |
| Turntable platter | 13 px | extended side canvas `(34,27)` |
| Potter's-wheel hand position | 17 px | `(20,23)` on 40 × 40 canvas |
| Dining / meal / cake table surface | 19 px | tray canvas `(39,21)` |
| Machete plant-cut contact | 12 px | long-tool canvas `(50,28)` |
| Low coffee-table surface | 12 px | reserved low-furniture datum; not used by meal/cake placement |
| Watering target | 9 px | extended side canvas `(35,31)` |
| Barometer / instrument control | 23 px | side `(27,17)`; rear `(26,17)` |
| Lift button | 23 px | front `(27,17)` |
| Exercise-bike handlebar centre | 21 px | front `(24,27)` on 48 × 48 canvas |
| Exercise-bike seat | 13 px | front `(24,35)` on 48 × 48 canvas |
| Exercise-bike pedal centre | 6 px | front `(24,42)` on 48 × 48 canvas |
| Toilet bowl vomit target | 5 px | rear extended canvas `(32,35)` |
| Shower-door handle | 22 px | rear-right extended canvas `(35,18)` |
| Hot-drink worktop / mug base | 12 px | right extended canvas `(40,28)` |
| Boat gunwale grip | 25 px | right extended canvas `(39,23)` on 48 × 48 |
| Boat bench seat | 13 px | right extended canvas `(36,35)` on 48 × 48 |

These are interaction datums, not mandatory object sizes. For example, a light
switch can have any suitable plate size, but its button centre must be 23 px
above the floor when the keeper stands on the same floor line.

## Placement recipe

1. Choose the named interaction profile from
   `data/keeper_asset_contract.json`.
2. Give the object a stable world-space interaction point, such as the centre
   of a switch or the lip of a bowl.
3. Place the keeper so the selected profile's point lands on the object point.
4. Keep his scale and feet anchor unchanged.
5. Mirror only clips marked `mirrorSafe`; use the corresponding mirrored point.

Example: the right-facing switch hand is `(+11,-23)` from his feet. If a
switch centre is at world position `(200,100)`, place his feet at `(189,123)`.

For television seating, place the seat contact at the clip's `(16,29)`. Put
the screen centre 24 logical pixels to the right and 15 pixels above that seat
for the right-looking pose, or mirror the strip and use 24 pixels left. The
chair/sofa should support the keeper's seat point but must not extend across the
screen sightline.

For beds, align the mattress surface with `(24,31)` on the 48 × 40 bed-action
canvas and the pillow centre with `(38,22)` for a right-facing layout. Mirror
both the clip and points for a left-facing bed. The bed frame, mattress,
blanket and pillow remain separate layers; play `keeper_get_into_bed` backward
for getting out.

## Rig landmarks

The shared pivot landmarks are neck `(16,11)`, shoulders `(10,15)` and
`(22,15)`, and hips `(13,25)` and `(19,25)`. New outfits must preserve these
landmarks. The striped swimming costume, parachute harness, light powder-blue pyjamas and yellow sou'wester oilskins
therefore change clothing only, never body proportions. Knight, spaceman,
pirate, Tarzan, Halloween and mechanic sets use the same three-view movement
contract: side/right (mirror for left), direct rear and direct front. Headwear
costumes use 32 × 48; bare-headed Tarzan uses the standard 32 × 40 canvas. The
body scale is unchanged in either case.

Fitness clips use the `old-school-workout-kit` outfit: blue terrycloth
headband, white sleeveless vest, blue shorts, white socks and blue-and-white
trainers. This applies to trampoline, weight lifting and press-ups. The clothes
may change the silhouette, but the canonical head, hands, feet and body scale
must remain unchanged.

Rear weightlifting uses a 48 × 56 overhead-action canvas anchored at `(24,56)`.
The extra height belongs to raised arms and the barbell; it must never be
obtained by shrinking the keeper's body below the canonical reference scale.

The stationary exercise-bike loop is actor-only in the same workout kit. Its
48 × 48 canvas preserves the canonical head unit while allowing the bent legs.
Build the bike as a separate object and align its handlebar centre, saddle and
crank to `(24,27)`, `(24,35)` and `(24,42)` respectively. The keeper remains
fixed in place; only his knees, feet and small exertion bob animate.

Directional underwater movement reads `movementVector` from the manifest:
right `(1,0)`, mirrored left `(-1,0)`, up `(0,-1)`, and down `(0,1)`. Water,
bubbles and splashes remain separate effects. The extended party canvas adds
transparent room above his head for the cardboard cone; the same 32 × 48
contract holds the broad sou'wester brim. His body is not scaled down to make
either hat fit. Sou'wester movement vectors are right `(1,0)`, rear/up
`(0,-1)` and front/down `(0,1)`; mirror the side strip for left.

Wide held instruments and reclined poses use the 48 × 40
`extendedHeldInstrument` canvas without changing body scale. Raised drumsticks
use the 32 × 48 `extendedRaisedArmsAction` canvas. Front drumming is the timing
and anatomy master; rear drumming is the same eight-frame motion viewed through
180 degrees. Both align the stool at `(16,37)` and drum surface at `(16,27)`,
and paired neutral frames may differ by no more than 0.75 px in visible height.
Movie seating aligns
at `(24,29)` on its wider canvas; the screen centre is 32 pixels to the viewed
side and 15 pixels above that seat point.

Snow clearing uses the 48 × 40 `extendedSnowToolAction` canvas. Place the
right-facing shovel/snow contact at `(43,37)` and mirror to `(5,37)` for left.
The reusable crouched rear-work loop uses the normal canvas and reaches ground
objects at `(16,38)`. Snow banks, shoveled piles and spray remain separate
layers; the thick winter coat is recorded as `winter-coat` outfit metadata.

Cake retrieval and carrying use the 48 × 40 `extendedTrayAction` canvas. Align
the oven rack to `(24,30)` for the direct-rear retrieval. The connected turn
holds the tray at `(34,20)` for right and mirrored `(14,20)` for left. The
mitts, tray and cake stay on the actor; oven casing, door and rack stay on the
object so different ovens can reuse the same animation.

The cake and plated-meal walking loops use that same 48 × 40 canvas and carry
point: `(34,20)` facing right, mirrored to `(14,20)` facing left. Their trays
remain level while the feet follow the canonical walk rhythm. This lets the
oven retrieval, cake turn, carry loop and table placement connect without
rescaling or shifting the held food.

For table placement, align the invisible standard tabletop to `(39,21)` on the
right-facing `keeper_place_cake` or `keeper_meal_place_side` canvas and mirror
to `(9,21)` for left. Each one-shot lowers and releases its food before the
keeper returns to a fully upright empty-handed final frame.

Any new prop-based animation must add its hand, seat or ground point to the
JSON contract and its sprite sidecar. Verification rejects changes that break
the established switch heights, canvas scale or feet anchors.

The complete starting dimensions for chairs, sofas, tables, beds, toilets,
baths, showers and object stations are in
`data/keeper_object_dimensions.json`. The per-frame measurement evidence for
all 191 sheets is in `docs/keeper-scale-audit/keeper-scale-metrics.json`; the
nine contact sheets render every sample at one fixed display scale so a larger
transparent canvas can never make its keeper look smaller.

For interactive comparison, open `docs/keeper-scale-audit/review.html`. On this
Mac, `Open Keeper Review Offline.command` at the repository root launches the
same page and all of its local sprite strips without Wi-Fi. Leave the launcher’s
Terminal window open during review; saved browser progress and the exported
`keeper-scale-choices.json` work normally at its stable `127.0.0.1:8765`
address. The reviewer puts
the untouched `keeper_walk` in a dedicated identity-baseline panel, followed by
all 173 accepted animation sheets in one filename-ordered gallery. Review-state
filters cover Needs my input, Happy, Awaiting new draft review, Review later,
Unreviewed and Has Codex response. For standard upright cap poses, its gold badge
crossing the blue skull-top line is a convenient calibrated proxy; it does not
replace anatomical landmarks for altered posture, head angle or headwear.
Every card prints both its runtime PNG and authored source-strip filename. The
shared controls pause or play every animation at once, apply pose-aware
comparison ghosts to every card, and draw the shared
skull/shoulder/hip/seat/floor rulers. The focused view steps through animations
one at a time on a much larger card using Previous/Next or Left/Right arrows;
navigation stays inside the selected filter and wraps at its ends. Switching
views preserves in-progress card state. A compact canonical reference stays
pinned beside it and can show standing side/front/back or sitting side/front/back.
These fixed ghosts are identity/anatomy comparisons, not a replacement for the
reviewed clip's saved production size. A
1×–12× display-size slider magnifies gallery stages or the focused reviewed
stage and never changes source or relative sprite scale. The page can
independently stretch an individual reviewed action from 50% to 150% in width
and height around its fixed contact anchor. The reference, ruler, ghost,
approach walk and bridge remain at 100%; earlier uniform choices migrate to
both axes.
Each card also has a read-only Codex response field, blank where no production
qualification was needed. Export version 9 produces `keeper-scale-choices.json`
with the complete status/response register for an authoring pass; it never
silently changes production sprites. The page can also play the matching
same-outfit walk immediately before an action. The raw seam, known-bridge and
onion-skin modes make transition problems visible. Flying and swimming cards
align the bottom of the first-frame figure to the red floor line for comparison.
Global Pause always resets every card to the action's first frame.
Per-card Previous/Next frame controls pause playback, switch that card to its
action and step without wrapping across every frame. Frame inspection does not
change the saved review. A top-right badge inside the pane always shows the
displayed clip filename and exact frame; seam-freeze mode identifies both frames.
The adjacent `Play animation` button previews only that card from frame 1. Its
selector either plays once and holds the final frame or loops until paused;
this review-only choice does not dirty the saved review.
The same teal panel has a per-animation proposed game-speed slider from 1–20fps,
with −0.5fps/+0.5fps buttons, an authored-speed reset and a live full-cycle
duration. It changes the reviewed action's preview only; approach walks and
bridge clips continue at their own authored speeds. Unlike play-once/loop, the
proposed FPS is a production decision, so it dirties, saves and exports with the
card.
Every multi-frame keeper clip defaults to the 4fps authored baseline. Accepted
review overrides now range from 1fps to 10.5fps and are read from the current
manifest; the page's authored-speed reset therefore returns each card to its
own delivered cadence. Older browser defaults are migrated once, while later
saved proposals are retained.
At 1500px browser width or above, focused mode lays out the pinned canon, stage
and compact two-column control console horizontally. Size controls are amber,
ghost mirror, rotation and position controls purple, action transforms blue, frame navigation teal, and
review/notes green or red.
Each character-width and character-height slider also has −0.5% and +0.5%
buttons for precise adjustment. These buttons update the same saved/exported
per-animation values as the sliders and obey the same 50%–150% limits.
The display zoom is retained immediately in browser-local progress. Saving a
card records it as the latest completed animation; reloading restores that zoom
and opens focused mode on the next filename-ordered card, clamped to the final
card when the most recently saved animation has no successor.
Seated cards automatically use the canonical front, side or rear sitting endpoint;
other cards use the standing reference. Per-card controls can select a different
reference, including the canonical back-to-camera standing endpoint (frame 6 of
`keeper_turn_back`), rotate/reset it, place it alongside and fade only the
reviewed action. That rear endpoint retains the standard outfit, 32 × 40 canvas,
[16, 40] feet anchor and 38-pixel standing height used by the canonical keeper.
The menu also offers the neutral arms-down first frame of `keeper_wave_camera`
as the canonical standard-outfit facing-front ghost; the exact-inheritance
party front idle is derived from this same frame.
The canonical rear-sitting reference is frame 6 of `keeper_sit_back`; it uses
the standard rear identity and the shared `[16,29]` seat point.
Each card's Save button persists its width, height, proposed runtime FPS, horizontal/vertical position,
comparison-ghost mirror, rotation and position controls, reviewed-animation rotation/opacity, free-text notes,
happy checkbox and mutually exclusive full-re-draft or re-review-later request in the browser.
Orange denotes unsaved changes, green a saved happy decision and red a saved
re-draft request. Export is blocked until every changed card is saved, and
version 8 of `keeper-scale-choices.json` contains the saved review register,
notes, re-draft list and re-review-later list as well as independent width/height/position production proposals.
Its `animationFps` value is intended for the clip's source JSON sidecar and the
generated `public/sprites/manifest.json`; it is not baked into the PNG pixels.
Existing legacy uniform choices are retained and applied to both axes.
The reviewed animation has its own −180° to +180° rotation control, independent
of the ghost. It rotates every action frame around the fixed review anchor and
is persisted/exported as comparison evidence, not silently applied to sprites.
Every animation-transform slider has matching −0.5/+0.5 buttons: degrees for
rotation, logical pixels for position and percentage points for opacity. These
buttons update the same saved/exported values and respect the same limits.
Horizontal and vertical position controls move only the reviewed action relative
to that anchor; a dedicated button resets both offsets to zero.

The sad, hungry, bored and cross reactions share one enforced upright scale:
their visible height is 38 logical pixels (152 pixels in the density-4 source)
inside the standard 32 × 40 canvas. The rear vomiting clip uses that identical
body scale on a 40 × 40 canvas; its visible height decreases only because the
keeper bends and kneels. Align a separate toilet's bowl target to `(32,35)`.
The keeper, small vomit effect and bracing hand are in the actor strip; the
toilet and room remain separate assets.

The cream bathrobe sequence uses the same canonical body scale and pale-blue
slippers throughout. `keeper_bathrobe_walk` supplies the reusable side walk.
For the door action, align a separate shower handle to `(35,18)` on the 40 × 40
right-hand canvas (mirror to `(5,18)` for a left-hand layout). The connected
entry clip begins at the 40 × 40 feet/threshold anchor `(20,40)`, moves upstage
and ends direct rear. The shower door, tray and cubicle remain separate. Once
the cubicle occludes the keeper, switch to `keeper_shower_wash`; no uncovered
transition frame is shown.

Spiral-stair movement uses paired 40 × 48 clips anchored at `(20,48)`. Align
the separate staircase tread path to the visible foot-contact datum `(20,46)`.
The up clip moves `(0,-1)` while turning from right three-quarter to rear; the
down clip moves `(0,1)` while turning from rear to front-right. These are
distinct animations, not reversed playback, so weight transfer and leading
feet remain correct. Treads, railing and central post stay out of actor strips.

The hot-drink sequence uses five connected 48 × 40 strips. The ten-frame pour
keeps the cream mug fixed at the invisible worktop point `(40,28)`, uses a clean
two-hand kettle grip, then lowers and releases the kettle beside the mug;
stirring keeps that same mug position; pickup moves
that same mug into the keeper's hand; sipping holds it at `(34,17)`; put-down
returns it to `(40,28)` and leaves it visible after release. Mirror the worktop
point to `(8,28)` for a left-facing layout. The enamel kettle, teaspoon and mug
are included in their applicable actor strips; the counter remains separate.

Boat entry and exit use independently drawn 48 × 48 clips rather than reversed
playback. Align the separate hull's gunwale to `(39,23)` and bench to `(36,35)`
for the right-side layout, mirrored to `(9,23)` and `(12,35)` for left. The
keeper climbs over the invisible gunwale with baseline anatomy; the taller
canvas provides movement clearance before Frank's saved review size is applied. Boat,
dock, water and oars remain separate world assets.

Bath, shower and hot-tub clips use their individual saved review scales and
carry explicit privacy metadata. Entry and exit frames use `towel-privacy`; washing uses
`mosaic-privacy`, and the hot-tub loop uses `privacy-foam`. The opaque coverage
is part of every relevant actor frame, so pausing or skipping frames cannot
reveal an uncovered intermediate pose. The bath, shower and tub remain separate
objects aligned to the usual feet or seat point.

Welding uses the normal 32 × 40 canvas. The hand saw needs the 40 × 40
`extendedSideTool` canvas so its full stroke remains visible without shrinking
the keeper; its feet anchor is `(20,40)`. Align a separate metal workpiece to
the welding contact or a separate timber/sawhorse assembly to the sawing
contact. Do not bake either work surface into the character strip.
