# Keeper animation handoff: review, scale and seamless transitions

> **17 October 2026 normalisation authority:** before creating or assessing
> another action draft, read
> `docs/KEEPER_PRIME_ANIMATION_BANK_NORMALISATION_CONTRACT_2026-10-17.md`.
> Earlier animation art supplies motion data only. Every visible character
> frame must be Prime Keeper, and every action must be reviewed inside its
> complete walk/stop/turn/action/return/walk route.
>
> Frank reaffirmed on 17 October 2026 that this applies to **all** first-draft
> animations. Old art is choreography evidence, never reusable visible actor
> art; palette fixes and partial identity patches are not sufficient.

**Checkpoint:** 17 October 2026
**Purpose:** this is the restart document for the keeper-animation work. A new
Codex task should be able to continue from here without relying on the old chat.

## Active side-right sit/stand candidate V2 — 17 October 2026

`/keeper-review/keeper-prime-sit-stand-side-v2/` is the current redrafted
sitting transition. Its complete 45-frame review route is approved Walk V6 →
approved walk-to-stop → six-pose stand-to-sit → 600 ms seated beat → exact
byte-reversed sit-to-stand → approved stop-to-walk → approved Walk V6. The
review page also isolates both action directions and supplies one-frame
stepping, speed controls, Prime/adjacent ghosts, 8× inspection, proposed 4×
presentation and literal 1× scale.

F1 is byte-identical to the approved smooth Prime side-right standing
authority. F6 is byte-identical to the registered Prime side-right seated
endpoint. F2–F5 are newly generated smooth Prime poses; the old six-frame
`keeper_sit_side` supplied joint path only and contributes no visible pixel.
Every action cell is 256 × 320, anchored `[16,40]`, floor-limited at opaque
y=315, seat-registered at `[16,29]` / 11 lp, and checked for a minimum
transparent gutter. The generated frames use a deterministic visible
height/width progression so the model does not widen suddenly after F1.

Frank judged the V1 motion good but rejected its over-deep example chair. V2
keeps all six Keeper cells, both action orders, timings, roots and the complete
route byte-for-byte/motion-for-motion. Only the chair proxy and furniture
contract change: the seat top is world y=41, exactly 11 lp above the y=52
floor, and its 11-lp usable depth runs from world x=77 at the spine/back
contact to world x=88 at the back-of-knee line. In the seated 32 × 40 cell
those landmarks are `[7,29]` and `[18,29]` (source `[56,232]` and
`[144,232]`). The seat cannot extend farther forward.

The versioned pack is
`art/drafts/keeper-prime-sit-stand-side-2026-10-17-v2/`; Workbench V11 replaces
only V10's active sitting link and preserves V1 as immutable history. V2 is
awaiting Frank. Nothing is Final, runtime or production, and the other sitting
directions must not be inferred from it.

## Darts Prime complete redraw and contextual route — 17 October 2026

Frank found the jump from Prime Keeper into the inherited Darts throw core
visibly irritating: the old action family has a narrower cream band, slimmer
torso, finer outline and different shading. Palette correction alone is
therefore rejected as insufficient. The historical Darts cells remain
choreography-only evidence.

`/keeper-review/keeper-prime-darts-redraw-v1/` was the first visual-family gate.
It contains three new high-resolution identity-preserve renders—wind-up,
release and recovery—made with the approved smooth side-right Prime as the sole
identity, anatomy, outfit, palette, outline, shading and rendering authority.
Each complete figure is uniformly registered into a 448 × 320 action cell with
the foot axis at x=128, cap top y=18, floor y=315 and zero edge alpha. The
expanded width preserves Prime scale around the extended throwing arm. Frank
approved that exact three-pose drawing family on 17 October 2026. The
hash-pinned decision is
`docs/review/keeper-prime-darts-redraw-v1-approval-2026-10-17.json`.

`/keeper-review/keeper-prime-darts-context-v5/` preserves all 213 Darts V4
route slots, roots, timings, sprite sources and state byte-for-byte except for
new content-addressed URLs. It adds browser-local, reversible controls to skip
one occurrence or every recurrence of the same pose, step through hidden
frames for inspection, restore all frames and export the skip recipe as JSON.
Skipping never deletes or reorders source art. V5 also replaces the crude CSS
flight/impact marks with one shared detailed dart component—red flights, dark
ribbed barrel, steel shaft and point—used identically while airborne and stuck
in the board. The inherited hand-held darts remain part of the superseded core
until the full Prime redraw is approved.

`/keeper-review/keeper-prime-darts-redraw-v2/` is the resulting complete
fourteen-slot core candidate. It contains nine unique visible drawings: exact
Prime neutral, the three approved V1 poses and five new Prime-derived bridges.
Every cell is 448 × 320 with clear edges; V1 wind-up, release and recovery are
byte-identical. Historical Darts contributed choreography only.

`/keeper-review/keeper-prime-darts-context-v6/` applies V2 to all 84 core uses
across six throws. All 213 V5 route positions, roots, durations, board state,
projectile timing, collection and turns remain exact. Its associated selector
was `/keeper-review/keeper-prime-context-workbench-v7/`, which retained ten
choices and linked both the complete route and registered core. Nothing entered
Final, runtime or production.

Frank's moving review then exposed two linked V6 faults at old frames 20–29.
Old frames 21–28 were an inherited camera-facing posture turn with no action
purpose, and the old F28→F29 join jumped backward because the 448-pixel action
cells were positioned on a false 28-lp midpoint. Their actual Prime foot axis
is source x=128, or 16 lp. V6 is therefore immutable superseded evidence.

`/keeper-review/keeper-prime-darts-context-v7/` is the corrective candidate.
It removes all four instances of that redundant bridge—old frames 21–28,
71–78, 156–163 and 206–213—rather than fixing only the first visible symptom.
All 84 throw-core anchors are corrected to `[16,40]`. Old F20 now joins directly
to old F29/new F21 at the same root; their rendered 8× stages are byte-identical
with zero changed pixels. The resulting route has 181 frames. Throw timing,
dart flight/impact, collection, necessary board/oche turns and every retained
out-of-scope frame remain exact. Its selector was
`/keeper-review/keeper-prime-context-workbench-v8/`. V2/V7/V8 remain candidates;
nothing entered Final, runtime or production. Workbench V9 and Darts Context
V8, described below, are the active review pages.

Production delivery was verified from deploy commit
`baf1f4b8c33bd01c04a09a4ca150d2afc351ab0b`. Darts V7 decoded all 32 unique
sprite images, exposed the expected
181-frame route and rendered live F20 and F21 with no changed stage pixels.
Workbench V8 loaded all ten choices with the corrected Darts V7 route selected
as its playable candidate. This is delivery verification only, not approval.

Frank then found that V7's CSS flight darts were blockier and shorter than the
dart visible in the Prime release pose, crossed the board plane before snapping
back, and landed in a placeholder oval rather than a convincing dartboard.
`/keeper-review/keeper-prime-darts-context-v8/` is the reversible correction.
It preserves all 181 V7 Keeper frames, roots, timing, state and controls. A
single transparent, gutter-safe 7.25-lp dart drawing supplies all 30 airborne
frames and every embedded state. The final airborne and following embedded
renderings have identical image bytes, dimensions and coordinates; the tip is
clamped at the x=168-lp board face. A separate high-resolution acute-angle
board has visible alternating sectors, double/treble rings and bull while
remaining only 3.15 lp deep in the room view. Workbench V9 selects this route
and reuses V8's unchanged inventory. At delivery V8 was an unapproved review
candidate and V9 was review infrastructure; nothing entered Final, runtime or
production.

Production delivery was verified from deploy commit
`eec56b0c0be5fc27fb30cf17c177fe33c8fd6068`. Darts Context V8 loaded and
decoded all 32 unique sprite images and exposed all 181 route frames. Live
frame 30's last airborne dart and frame 31's embedded dart rendered to the same
SHA-256 (`2a69a58447597517248951f540da619a45a888531dabe94f42b66f382bd258ae`)
at identical coordinates. Workbench V9 loaded all ten choices and decoded its
22 unique native-route images before enabling playback. This records delivery
only; it is not Frank's approval of V8 or V9.

Frank subsequently replied “approved” on 17 October 2026. Exact Darts Context
V8 is therefore the approved contextual darts animation authority: all 181
route frames, the harmonised dart, the segmented acute-angle board, the exact
impact seam and the unchanged V7 Keeper/timing/state data are binding. The
immutable decision is
`docs/review/keeper-prime-darts-context-v8-approval-2026-10-17.json`.
Workbench V9 remains review infrastructure rather than animation art. Approval
did not copy or alter artwork and did not change Final, runtime or production.

The superseded V6 delivery was verified on 17 October 2026 from deploy commit
`2e2f39d798bbf65e11e5aa78da7fd5f1d931cc91`. Darts Context V6 loaded and
decoded all 40 unique sprite images; occurrence skip and restore changed the
live route from 0/213 to 1/213 and back to 0/213; the V2 inspector exposed
enabled frame/play controls with decoded 448-pixel poses and its 1,392-pixel
lineup; and Workbench V7 loaded all ten choices and opened the embedded
213-frame Darts V6 route. This is delivery verification only, not approval of
V2/V6/V7.

## Whole-bank audit and prior Context Workbench V5 checkpoint — 17 October 2026

The production bank now has a deterministic 308-row audit in
`data/keeper-prime-animation-bank-audit-v1.json`, with a human summary in
`docs/KEEPER_PRIME_ANIMATION_BANK_AUDIT_2026-10-17.md`. It records every exact
frame range, fps, cell, anchor, runtime SHA-256, category, outfit, facing,
endpoint, prop/seat/movement dependency, inherited face/body family,
recommended treatment and contextual route. Counts are 9 expressions, 82
interactions, 101 locomotion clips, 12 seated actions, 73 technical neutrals
and 31 transitions. There are 159 legacy endpoint risks, 28 explicitly
rejected/excluded entries and no measured strip/sidecar geometry mismatches.

The prior V5 review selector is
`/keeper-review/keeper-prime-context-workbench-v5/`. V5 exposes nine choices:
approved stop/walk/stop; an approved-component walk/stop/180° turn/walk
composition; the corrected Darts V4 candidate; the complete approved stair
ascent;
the approved stair descent; the approved ladder motion route; and the
unapproved six-view seated foundation; a dedicated 30-frame inspector for
the inherited Darts V2 registered strip; and the reversible Darts cell-isolation
corrective draft. Native routes provide optional preceding
and finishing transitions, whole/core looping, speed adjustment, frame
stepping, exact-Prime ghost, adjacent-frame onion skin, and simultaneous 8×,
4× and literal 1× views. The 308-row inventory is linked from the page. Status
labels are binding: inclusion does not convert a candidate into an approval.
V3 retains V2's full-width 8× pane, localised native-route images and
deployment-safe root-absolute URLs. V2 fixed V1's deployed trailing-slash bug,
which returned HTML to its relative
`catalog.json` request and locked the controls. V1 and V2 remain immutable
provenance. V3 and V4 remain immutable. V5 replaces the playable Darts V3 link
with Darts V4 while retaining both diagnostic pages; it adds no approval or
promotion.

The strip inspector is
`/keeper-review/keeper-prime-darts-strip-inspector-v1/`. It changes no art.
Every V2 cell is selectable at exact 448 × 320 source pixels and 1.5×/2×/3×
enlargements, with previous/next buttons, keyboard arrows, exact-Prime and
adjacent-frame overlays, difference blending, thumbnails, and the complete
strip. It also reports deterministic median RGB measurements for saturated
uniform blue, dark blue/navy and warm cream. Those values are diagnostic, not
automatic approval thresholds. The initial audit confirms visible blue drift:
Prime F01 is median RGB (0,86,202), while multiple generated core frames are
around (1,62–68,171–195).

The new corrective review is
`/keeper-review/keeper-prime-darts-isolation-v1/`. The generated 1774 × 887
pose source was laid out visually as 7×2 but was not cell-safe. Deterministic
whole-sheet segmentation found 14 actor components and four detached projectile
components. Rectangular cropping assigned 51 foreign actor pixels to core F07
(registered F15), 42 to core F11 (registered F19) and 163 to core F12
(registered F20); it also split the detached darts across core F08–F12
(registered F16–F20). The
candidate reconstructs each of the fourteen throw-core cells from exactly one
whole actor component, excludes all four detached projectiles because the V3
route already draws flights as independent effects, and enforces a two-source-
pixel transparent gutter. Registered F01–F08 and F23–F30 remain byte-identical
to V2. The page provides immutable-V2/candidate/overlay comparisons and both
complete strips. This fixes ownership only: it deliberately does not apply the
separate palette correction and remains unapproved.

Darts V1 is preserved rejected provenance only: its action frames drifted
toward three-quarter view and snapped against the exact side endpoint. Darts
V2 is immutable superseded provenance. Darts V3 remains the immutable
pre-isolation contextual candidate. Darts V4 is an earlier reversible playable
candidate at `/keeper-review/keeper-prime-darts-context-v4/`. It substitutes
the fourteen isolated core cells into V3's route but keeps all 213 frame slots,
timings, roots, ranges and approved transition assets unchanged.
The cupboard door is closed and seen edge-on, so only the thin door rim and
dartboard edge are visible. The board centre is y=30.5 lp and the collection
root x=155.5 lp, aligning its plane with the approved full-reach hand. The
Keeper approaches the x=125-lp oche, throws three darts whose five-position
flights visibly reach and stick in the board, walks one complete 30.5-lp
stop-to-stop route to collect them, turns once at the board, walks the same
full stride back, turns once at the oche and throws three again. The 213-frame
route contains exactly two turn events. Its repeatable range starts and ends
on identical Prime pixels, x=125 root and three-darts-on-board state. V4 uses
the corrected core 84 times across its six throws and retains full-route,
activity-loop, first-set and once-through playback plus frame stepping and
speed controls. This
remains unapproved and changes no Final, runtime, production or approval
record.

Next visual gate: Frank reviews the cell-isolation candidate and identifies any
Darts V2 cells requiring palette correction in the strip inspector. After
isolation approval, palette correction must be a new masked candidate layered
on the isolated cells; do not alter V2, V3 or isolation V1.
After that, build exact Prime stand↔sit transition strips against the seated
foundation if its endpoints are approved, then process interaction families in
small contextual batches. Swimming, gym and scuba require complete redesign;
`keeper_count_money` remains excluded without a new direct instruction.

## Current core-transition checkpoint — 16 October 2026

### Seated Six-View V2 loading and contact correction — 17 October 2026

V1 remains immutable historical evidence. Its all-or-nothing preload gate could
leave the main inspection blank if any auxiliary comparison image failed. V2
renders the first primary seated view immediately, uses `Promise.allSettled`
for the six primary images only, reports failed views by name and never lets an
auxiliary comparison block the endpoint review.

V2 changes no Keeper pixels. It adds a deterministic physical-seat proof: the
chair top is exactly y=29 logical pixels / y=232 source pixels, eleven logical
pixels above the floor; it is rendered behind the Keeper. Every one of the six
images has an opaque pelvis at `[16,29]` and a continuous opaque band across
y=231–233, so the chair surface has neither a visible air gap nor a foreground
edge cutting through the body. Review route:
`/keeper-review/keeper-prime-seated-six-view-v2/`.

The staircase itself is now preserved independently of any review-page CSS at
`art/drafts/keeper-staircase-geometry-2026-10-16-v1/`. Its geometry-only
authority records all fourteen tread rectangles, the exact 7-lp tread run,
30/7-lp riser rise, 98 × 60-lp flight, 60-lp floor pitch, 105-lp reserved core,
landing roots and Keeper contact centres. The included SVG stores the plain
test staircase as construction evidence, not final scenery. Later staircase
art must add two newels, foreground balusters and a continuous rail while the
geometry verifier prevents any size, tread, riser, landing or contact drift.

Stair Descent V1 is rejected provenance. Its reverse-order/mirrored ascent
drawings made the visible left leg remain airborne while the right leg took
every descending step. Do not reactivate or promote it. The replacement is the
reversible V2 review candidate at
`/keeper-review/keeper-prime-stair-descent-v2/`. The complete door-to-door route
is unchanged, but the stair section now uses four descent-specific side-right
drawings in the exact repeating cycle RIGHT contact → LEFT passing → LEFT
contact → RIGHT passing. Across fourteen risers this produces seven right-foot
and seven left-foot contacts. The approved V16 root path, stored 98 × 60-lp
staircase, turn, walk, bridge and door-reach assets remain unchanged. Raw and
registered candidate hashes, image-editing prompts, registration parameters
and deterministic tests are stored in
`art/drafts/keeper-prime-stair-descent-2026-10-16-v2/`. Frank approved V2 with
its slight overstride accepted; the decision is pinned in
`docs/review/keeper-prime-stair-descent-v2-approval-2026-10-16.json`. No Final,
runtime or production art changed.

Keeper Prime's upward stair route is complete and approved at
`/keeper-review/keeper-prime-stair-transitions-v6/`: lower-room emergence,
walking join, full climb, landing, clockwise turn, upper-floor walk/stop,
right-hand door reach, outward opening and fully hidden exit. Approved Stair
Ascent V16 remains its climb authority.

The approved ladder motion/layering authority is Ladder Transition V4. Frank
also approved all Keeper motion in Ladder Transition V5, pinned by
`docs/review/keeper-prime-ladder-transitions-v5-animation-approval-2026-10-16.json`.
V5 extends V4 into the same complete upward room-to-room journey. Its first 88
route frames and 29 V4 Keeper images are exact; its 23-frame tail adds only the
upper stop/reach/open/restart/exit. The V5 perspective door is rejected and is
not part of the motion approval.

The active reversible V6 page changes only that door presentation. It uses the
same 111 Keeper frames, roots and timing byte-for-byte. The door is a flat,
constant-size 20 × 48-lp opaque rectangle, right-hinged as viewed, with no
perspective widening or gradient; only its handle protrudes. Every door is
two-way and opens away from the approaching Keeper. Its leaf supplies the real
crossing occlusion, and the scenery controller closes it automatically only
after the Keeper fully clears the doorway. The rule is pinned in
`docs/review/keeper-two-way-door-contract-2026-10-16.json`. Frank approved the
complete animation flow; V6 remains unpromoted. The separately requested
two-times-faster V4 turn remains deferred.

The remaining core transition work is bounded:

1. certify the mirrored opposite stair-flight layout against the approved V2
   contact/root rules;
2. downward ladder with direction-specific top mount and lower dismount/door
   exit (the central rung cycle may reverse, the route joins may not);
3. complete Prime lift call/enter and lift-exit/walk flows;
4. Prime stand↔sit joins for side, front and rear furniture approaches;
5. explicit left/right or opposite-hand variants wherever mirroring would
   break a door, prop, furniture or hand relationship.
6. one deterministic open-door room emergence/return handoff, reusing standard
   walking and occlusion rather than creating costume-specific door art.

Action-specific object handoffs follow these core routes. Do not restart room
placement by redrawing any approved walking, stair or ladder source.

## Exact-name amendment checkpoint — 12 October 2026

Handoff `d9081e53-2808-4b1f-8422-2df09cf38c3c` is preserved byte-for-byte at
`docs/review/keeper-review-handoff-2026-10-11T221440Z.json` (SHA-256
`cfd889542743b2febdfb5bdfa79e54149a377bf1bd9cfbbe0d73a2116dfc6e75`).
Its 81 `changedAnimationNames` are the sole scope of this amendment round.

The reversible batch lives at
`art/drafts/keeper-review-amendments-2026-10-11-v1/`. It exposes 41 active
side/rear, timing or object-action candidates. Each register pins the original
and draft SHA-256 values, sidecar geometry and per-frame alpha evidence. No raw
or runtime keeper sprite has been replaced. The reviewer publishes comparison
images by content hash, allowing a current amendment and a retained prior
version with the same exact filename to coexist safely.

`keeper_party_hat_put_on_back` additionally has a second reversible comparison
in `art/drafts/keeper-party-hat-put-on-back-hands-2026-10-12-v2/`: only frame 2
changes, replacing the impossible front-plane hands with connected rear-plane
arms holding the hat at the nape. Frames 1 and 3–8 are byte-identical to the
first draft, and neither variant is promoted.

Its follow-up is a third reversible comparison in
`art/drafts/keeper-party-hat-put-on-back-front-arm-plane-2026-10-12-v3/`:
frame 2 now keeps both connected forearms and hands entirely in the front/near
plane, clear of the head silhouette, while lifting one hat above the crown
toward frame 3. Frames 1 and 3–8 are byte-identical to v2. Canonical art and
all three review variants remain unpromoted.

`keeper_carry_shopping` also has a second reversible comparison in
`art/drafts/keeper-carry-shopping-right-bag-2026-10-12-v2/`: the missing
right-hand shopping bag is restored in annotated frames 1 and 7. Corrected
frame 1 is copied to frame 8 because the first draft established those frames
as byte-identical loop endpoints; frames 2–6 are byte-identical to the first
draft. Canonical art and both review variants remain unpromoted.

`keeper_play_drums_back` has a second reversible comparison in
`art/drafts/keeper-play-drums-back-hands-2026-10-12-v2/`: only frame 6 changes,
removing the hands and crossed sticks from behind the Keeper's back and
wrapping both forearms forward at his sides toward the unseen drum kit. Frames
1–5 and 7–8 are byte-identical to the first draft. Canonical art and both
review variants remain unpromoted.

`keeper_put_record` has a second reversible comparison in
`art/drafts/keeper-put-record-removal-2026-10-12-v2/`: Frank's supplied mask
removes only the floating record regions in frames 5–8. Frames 1–4 and every
surviving pixel in the changed frames are byte-identical to the first draft;
the built-in edit's regenerated RGB is discarded. Canonical art and both review
variants remain unpromoted.

The follow-up correction is a third reversible comparison in
`art/drafts/keeper-put-record-horizontal-frame5-2026-10-12-v3/`: frame 5 keeps
one record supported between both hands, edge-on and parallel to ground level
like frame 4, while frames 6–8 retain the detached-record removals. Frames 1–4
and 6–8 are byte-identical to v2. Canonical art and all three review variants
remain unpromoted.

Frank withdrew all newly rendered face-to-camera candidates on 12 October.
Twelve registers are marked `withdrawn-by-user` and excluded from
`data/keeper_review_drafts.json`; their files remain only as rejected
provenance. Frank subsequently ordered the complete `keeper_count_money`
amendment deleted and the previous canonical version retained; only its hashes
and deletion decision remain in the withdrawal record. This withdrawal includes the frontal party, money, button,
costume/down-axis, outfit-walk, watering, trampoline and pyjama-turn candidates.
Do not reactivate them without a new explicit instruction. Side and
three-quarter candidates must not use a generic smile or open grin; action
mouths are permitted only where physically required.

`docs/review/keeper-animation-codex-responses-2026-10-12.json` has one response
for each of the 81 exact names. `keeper_fish_seated`, `keeper_shower_exit` and
`keeper_shower_wash` request another iteration rather than presenting an
unreliable amendment; `keeper_slide_side` remains deferred until the
helter-skelter route exists, and `keeper_shower_enter` remains Review later.
Canonical gutters for `keeper_guitar_pickup_gretsch`, `keeper_machete_side` and
`keeper_saw_wood` were measured directly and already pass without a new draft.

Rebuild this batch by running its five `build_*_family.py` scripts, followed by
`withdraw_face_camera_drafts.py`, `sync_review_registry.py`,
`scripts/audit_keeper_scale.py`, `npm run verify:keeper-review-drafts` and
`scripts/verify_floor_asset_catalogue.py`. Explicit visual approval is still
required before any active amendment may be promoted.

## Full-face canon decision — 12 October 2026

Frank selected two aligned frontal references as the foundation for normalising
all face-to-camera Keeper animation:

- primary canonical geometry:
  `art/raw/keeper-first-batch/keeper_neutral_standing-front_f1.png`;
- recent rendering-quality reference:
  `art/drafts/keeper-artist-smock-family-redraw-2026-10-11-v11/drafts/keeper_artist-smock_neutral_standing-front_f1.png`.

These references intentionally converge on the same adult, restrained facial
system: solid dark rectangular eyes, a defined separate moustache, a readable
closed mouth, the established beard mass, and no generic smile or pixie grin.
The standard neutral is the geometric authority; the V11 endpoint is the
quality and finish reference. Emotion and action-specific expressions must be
controlled deviations from this neutral base, never substitute neutral models.

The first phase is now delivered as the reversible
`art/drafts/keeper-full-face-canon-pack-2026-10-12-v1/` pack. It inventories 62
direct or near-direct front manifest assets in
`docs/KEEPER_FULL_FACE_INVENTORY.md` and
`data/keeper_full_face_inventory.json`, including exact frame ranges, current
face families, outfits, endpoints, edge evidence and transition risks. The V1
standard neutral is byte-identical to the selected primary geometry authority;
the V11 smock neutral remains an unmodified rendering-quality comparison.
Exact eye masks, beard/moustache/mouth guides and deterministic geometry,
binary-alpha and gutter checks are included. Review it online at
`/keeper-review/full-face-canon-v1/`. Frank explicitly approved V1 on 12 October
2026 with “Approve full-face canon pack V1. These are excellent.” This approval
authorizes small reversible authoring batches, not production promotion. The
first batch contains only `keeper_turn_front` and `keeper_turn_left_front`.
Frank rejected the V1 F5-only transplant and requested a complete moving-model
redraw with a non-jumping exact-canon endpoint. V2 is at
`art/drafts/keeper-full-face-standard-turn-redraw-2026-10-12-v2/`: F1–F5 are
new approved-model rotations, F6 is byte-identical to canon, and F5/F6 share
the same baseline, height and centreline with at most two source pixels of
width difference. Frank initially approved both V2 turns on 12 October, then
rejected their live route joins and reset the workbench to zero Final and zero
active Draft animations. The old approval is provenance only and does not
authorize raw/runtime promotion. No withdrawn face-camera work was reactivated.

### Keeper Prime checkpoint — 12 October 2026

Running the assembled ingress exposed unacceptable joins at the old
walk/stop→V2-turn boundary and at the V2 near-front→exact-front endpoint. Frank
therefore selected **Turn right profile to front F6**—the same pixels as ingress
preview F19 and `keeper_neutral_standing-front_f1.png`—as the sole model from
which every other Keeper image must stem. Its durable name is **Keeper Prime**
(`KP`, slug `keeper_prime`). The V2 approval remains historical provenance,
but no longer appears in Final and those complete turn strips are superseded as
a route foundation.

The first reversible proposal at
`art/drafts/keeper-prime-core-transitions-2026-10-12-v1/` is retained intact as
review history. Frank accepted route 1 and particularly its small deceleration,
but found route 2's acceleration stationary for too long; routes 3 and 4 changed
perspective, height and width at route steps 19→20; and routes 5 and 6 exposed
an apparent-pixel-density mismatch around Keeper Prime.

The later unapproved V2 replacement is
`art/drafts/keeper-prime-core-transitions-2026-10-12-v2/`. It preserves V1 walk
and stop strips byte-for-byte, removes the duplicated exact-stop frame from the
acceleration sequence, and rebuilds front turn, back turn and sit from one
coherent six-pose generated source each. Stand remains the exact reverse of
sit. Numeric seam
checks now cover width, height, centre, baseline and opaque area, including the
three specifically rejected F2→F3 joins. Production art and manifests remain
unchanged. Live review found that its return to the coarse Frame 6 pixels still
produced an unacceptable density/model jump, so V2 is now rejected provenance,
not an active Draft.

Frank then reset the foundation. Frame 6 remains identity, stance, head-position
and endpoint evidence, but its pixelated raster is not the render master. The
sole current proposal is
`art/drafts/keeper-prime-master-2026-10-12-v1/`, reviewed at
`/keeper-review/keeper-prime-master-v1/`. It uses Frank's preferred first smooth
render, normalized to a 256 × 320 density-8 cell with the same logical anchor,
and replaces the difficult-to-maintain double stripe with one broad pale band.
All animations await redrafting from this family after explicit master approval.

The 12 October V2 documentation audit reconciled this handoff, the authoring
playbook, the workbench guide and `README.md` with the generated catalogue,
browser Draft migration, deterministic checks and unchanged production state.
Setup, verification, deployment boundary, rollback path and next approval gate
are current.

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
2. Open the deployed online reviewer at
   `https://lighthouse-keeper-mu.vercel.app/keeper-review`. It is the only
   reviewer and the only place to save feedback or use **Hand back to Codex**;
   the collapsed version-11 JSON backup/import is only for exceptional browser
   recovery. A dedicated panel first shows
   the untouched `keeper_walk` identity/anatomy baseline, followed by all 173 accepted
   clips at one unchanged relative scale in filename order. Filter the register
   by Needs my input, Happy, Awaiting new draft review, Review later,
   Unreviewed or Has Codex response; independently filter pose as standing,
   sitting or crouching (with direction subcategories) and use list as active,
   reserve-only or all. Switch View to `One animation at a time`
   for a much larger card. Previous/Next and Left/Right stay inside the active
   filter and wrap from its final result to its first. A compact reference stays
   pinned alongside; standing side/front/back and sitting side/front/back
   canons are available. These are fixed identity/anatomy comparison ghosts;
   they do not replace the saved production size of the reviewed clip.
3. Every card has a read-only Codex response field. All 68 `Awaiting new draft
  review` cards have a specific narrative naming the delivered production
   change. Any genuine qualification is stated explicitly; a generic response
   is not evidence that work was completed. The reviewer now also marks the
   ten user-selected canonical promotions with their exact `Previous version`
   comparison; this is distinct from an unpromoted draft.
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
   Display zoom and all three filters are saved immediately in browser-local progress.
   Saving or advancing from the final result wraps to the first result in the
   same filter.
6. For the next review round, ask Frank to press **Hand back to Codex** in the
   deployed reviewer, then read the newest queue entry before starting work.
   Each card's Save button persists independent width/height, rotation,
   horizontal/vertical position, ghost settings, opacity and the
   happy/not-yet-happy decision, free-text notes, full-re-draft request,
   pose override and reversible reserve membership in his browser. Version 11
   includes production proposals, the complete review register/statuses,
   preferred candidate, pose/reserve values and the read-only Codex response,
   but it does not alter production art by itself. Cards with retained draft
   variants can compress/expand those comparisons without removing any draft.
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
blue means saved for later review. Hand back to Codex
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

- Every costume change happens while the keeper is fully hidden behind the
  opaque door leaf. Room-boundary clipping is not a substitute for the leaf.
- Room doors swing both ways and always open away from the approaching Keeper.
  The flat leaf renders in front of him during the crossing, then the scenery
  controller closes it automatically only after his complete bounds clear the
  doorway. It does not remain open throughout the activity. Never draw a
  separate closing animation for every costume.
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
- Frank's 11 October review established the visual acceptance rule for special
  outfits: a special-outfit family must be internally consistent across every
  animation used in its room, while a small standard-to-costume difference is
  tolerable only across the complete door occlusion where the change is never
  visible. This does not relax any same-outfit seam. End/start frames used
  consecutively in one outfit must still be identical where declared.
- Standard-uniform activities have no such tolerance. Their visible approach
  and exit use the standard walk family, so head, eye, nose, beard, hands and
  body ratios must remain compatible with `keeper_walk`; a one-off action is
  cheaper to rebuild than to accept a visible identity jump.

## Current evidence and files

- The evidence-based side-on beard/hand audit (2026-10-11) is recorded in
  `data/keeper_side_on_beard_occlusion_audit.json`. It classifies every
  manifest Keeper frame and inventories 163 standing/sitting true-side source
  sheets. The pinned `keeper_clear_snow` raw SHA-256
  `fd866ef8f433211946b596c27cd1941dfdcc0bf40e0efb8555cb87c375a39d96` is the
  authoritative fuller, stepped side-on beard. The result is intentionally
  fail-closed: a landmark-aligned beard-mask silhouette may differ by at most
  one logical pixel and still pass. The eight reference self-comparisons have
  zero difference; 994 different-pose frames are non-comparable because no
  approved beard masks, facial landmarks, or hand depth/component ownership
  evidence exists. In
  particular, `keeper_darts` frames 3–6 are not a confirmed occlusion defect.
  Frank visually reviewed those displayed frames on 11 October and accepted
  their beards as fine with no amendment required. No new beard draft is
  active or promotable. v1 and v2 draft files remain
  historical, non-promotable evidence under their existing draft directories.
- The permanent check is `node scripts/verify_side_on_beard_occlusion.ts` and
  is included in `npm test`. It pins the canonical reference, source/sidecar
  hashes, classifications and frame-edge gutter evidence, and rejects any
  unsupported match or mismatch. The reviewer shows canonical Darts beside
  Frank's selected draft and explicitly states the evidence gate; it does not
  show the historical v2 colour-predicate image as an active draft.
- Frank subsequently selected the same original 14-pose image as a good darts
  animation and explicitly requested a new review comparison. That selection
  is independently preserved under
  `art/drafts/keeper-darts-user-selected-2026-10-10-v1/`, extracted into 14
  isolated 56 × 40 frames, and registered by exact `keeper_darts` name in
  `data/keeper_review_drafts.json`. It is not the rejected altered v1 strip;
  canonical raw/runtime darts remain byte-identical and appear beside it.
- Frank also explicitly selected nine other source replacements: three guitar
  pickups, standing and seated fishing, clear snow, meal placement, parachute
  drift and machete. A matching `keeper_parachute_landing` bridge was promoted
  solely to keep the resized drift hand-off pixel-identical. These ten exact
  names are canonical after final-strip inspection. Their former canonical
  raw/runtime strips, sidecars and SHA-256 values are retained under
  `art/drafts/keeper-user-selected-batch-2026-10-10-v1/` and appear as
  `Previous version` beside the current strip in the reviewer. They are not
  evidence that the rejected second-round batch was restored.
- Frank accepted the internally consistent V11 artist-smock family on 11
  October, with one exact seam condition: the final frame of
  `keeper_artist_smock_turn_front` must be the complete first frame of
  `keeper_artist_smock_sit_front`. The normalized cells are byte-identical and
  `scripts/verify_keeper_review_drafts.ts` now rejects any regression. All
  seven artist animations present in the review gallery are registered as
  active `V11 consistent artist set` comparisons; the five neutral stills and
  three walk start/stop/cycle strips remain deterministic technical assets and
  therefore do not create phantom gallery rows. Production is unchanged.
- An earlier referenced-image standard-uniform `keeper_snooker` redraw study
  was rejected because it failed to hold the canonical `keeper_walk` beard.
  Frank then accepted a new canonical-identity route assembled pose by pose:
  walk right → exact stop/neutral → reach → cue contact → lower → two snooker
  strokes → rise/release → exact neutral → canonical turns → walk left. Its
  exact successful prompts, generator outputs, fixed-scale normalization,
  source/output hashes and seam checks are preserved under
  `art/drafts/keeper-standard-snooker-complete-sequence-2026-10-11-v1/`.
  The 65-frame constant-4-fps review representation is registered by exact
  `keeper_snooker` name as an active comparison. The canonical eight-frame
  raw/runtime snooker strip remains unchanged until Frank makes a later manual
  decision in the deployed reviewer.
- `node scripts/verify_keeper_review_drafts.ts` checks source, previous/current
  canonical or draft and published-review hashes, geometry, transparent gutters,
  detached-prop ownership, the V11 whole-frame front seam and exact-name
  reviewer attachment.
- `docs/KEEPER_ARTWORK_AUTHORING_AND_REVIEW_PLAYBOOK.md` consolidates the
  durable method learned from the bathrobe failures, accepted V11 artist-smock
  family and accepted standard-uniform snooker route. It is the starting point
  for future exact-name artwork requests from the review platform.
- The deployed reviewer is online only at `/keeper-review/`; its review-only
  media is content-addressed under `review-archive/objects/`, while legacy
  `/keeper-review/drafts/...` URLs resolve through archive manifests and
  permanent cached redirects. The media is not runtime sprite art. The
  generated audit artifact remains byte-identical for
  verification, but sends any local opening to the deployed reviewer.
  Browser progress remains tied to that single origin, and the deployed
  reviewer submits a complete exact-name batch to the durable handoff queue
  through Hand back to Codex.
  Gallery cards are deliberately animation-first: name, current review state,
  latest local save/redraft timestamp, playback and frame stepping, with an
  `Open close review` action. Close review exposes an exact-name canonical/draft
  selector that records an exportable preferred-promotion candidate only; it
  never silently promotes or overwrites production art.
- 191 keeper sheets and 1,479 frames are in the current technical review batch.
- 173 animation sheets are accepted into the review gallery.
- 18 obsolete modular/reference sheets are excluded from review and must not
  return to production.
- 81 sheets are recorded as rebuilt or anatomy-normalised in the latest full
  audit.
- The audit currently reports zero unresolved original-comparison failures.
- The immutable imported review remains 96 Happy, 68 Awaiting new draft review,
  3 Review later and 6 Unreviewed. The current reviewer is 97 Happy and 67
  Awaiting after Frank selected the retained Darts draft as his preferred
  candidate; that preference is not a canonical promotion. The ten selected
  replacements are a narrow, separately documented canonical promotion; all
  other affected awaiting rows still require a fresh versioned draft and are
  not claimed as implemented.
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

The artist-smock family now has its complete internally consistent V11 walk,
front/rear turns, front sit/stand, painting and pottery set plus deterministic
neutral/walk bridge derivatives. Seven authored animations are active reviewer
drafts; no V11 pixels are production yet. For winter/workout clothing, author
complete internally consistent room families where the keeper traverses
visible space, and keep every within-outfit hand-off exact even though the
door-hidden standard-to-costume swap may tolerate a small appearance change.

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

## Separate Draft/Final animation workbench (updated 13 October 2026)

Frank initially approved both complete moving-model V2 turn redraws with the
exact wording “I am very happy with your V2.” Subsequent live-route review
superseded that decision. The new `/animation-workbench` surface now contains
zero Final and zero active Draft animations. This is deliberately separate from
`/keeper-review/`: it does not consume that platform's saved reviews, handoff
queue or locks, and Final-lane acceptance is not production promotion.

The V1/V2 strips and approval record remain content-addressed provenance without
being listed in either active lane. Browser storage moved to the `v3` namespace
so rejected local route state is not automatically restored; older storage is
left untouched for recovery. Future local edits use the same recipe structure
as Final and remain browser-local/JSON-exportable.
Draft controls copy, remove and reorder frame references, loop a complete
animation, and repeat a selected contiguous section. They never rewrite source
strips. Overlapping section loops fail closed.

Complete transition preview is mandatory for every animation: `walk → moving
stop → optional front/back turn → action`, with a compatible `action → exact
stop → reversed walk-start → walk` egress. The game engine deterministically chooses the walk
cycle count from the Keeper's starting position and the target asset's world
placement; the workbench shows one representative cycle and authors no
distance-specific count. The walk cycle begins while the Keeper is fully
hidden behind the departure door; his first visible state is already in motion,
and the workbench simulates that door-side reveal. New core drafts must carry
residual translation through stop/start so the Keeper never walks on the spot. A door
may hide a costume swap, but the resulting action still requires the same
complete transition preview. Metadata diagnostics check pose and outfit
agreement at joins.

Full architecture, extension points and verification are in
`docs/KEEPER_ANIMATION_WORKBENCH.md`. The authoritative catalogue is
`data/keeper_animation_workbench.json`; its public copy is byte-identical.
`scripts/verify_keeper_animation_workbench.ts` checks the zero-lane approval
gate, content hashes, historical strip/sidecar geometry, transparent cell
gutters and preserved editor framework. `scripts/verify_keeper_prime_master_v1.ts`
checks the selected/rejected generated provenance, normalized candidate,
landmarks, masks, hashes and public comparison. Raw/runtime sprites and the
manifest remain unchanged.

Frank permanently approved the smooth, single-band Prime Master V1 on 13
October 2026 with the exact wording “Approved. Make sure this is NEVER
forgotten.” The builder and verifier pin both that wording and the approved PNG
hash. V2 remains immutable rejected provenance. Its back copies all 81,920
approved-front alpha values, but later inspection found that the rendered boots
still face the player. V3's 15-point front-to-side skeleton separately proves
the selected side passes only five hard internal datums. Frank explicitly
approved the first, smooth rear-boot render for V5: it keeps rows 0–272
byte-identical to V2, changes only rows 273–315, and retains zero alpha
mismatches. The 1122 × 1402 source is the rendering-quality authority; the 256
× 320 registered endpoint is an anti-aliased proxy. V4's rougher, over-squared
alternative remains historical provenance. The new rigged side-right V1 at
`/keeper-review/keeper-prime-side-right-rigged-v1/` is a smooth 1122 × 1402
master with a uniformly registered 256 × 320 proxy, exact zero delta at all 15
datums and a transparent gutter. Frank approved it with “Approve side-right V1
and build Turn V1.” The resulting Turn V1 review pack joins the exact approved
front and side endpoints with six smooth intermediate poses and an exact
reverse strip. Frank approved that turn with “it is ever so slightly jumpy at
about 45deg in the turn but I am happy”. Its immutable V2 approval record keeps
the slight 45° cadence change as an accepted minor limitation. The separate
side-right ↔ back Turn V1 joins the exact approved side and V5 rear endpoints
through six independently drawn rear-quarter poses and an exact reverse strip.
During review Frank identified a visible palette discontinuity: the jumper
darkened at its exact rear F8 endpoint. V2 corrected only the jumper. Frank then
identified that the cap, trousers and boots also darkened and established a
general rule: every standard-uniform animation must use consistent component
colours. V3 at `/keeper-review/keeper-prime-turn-side-back-v3/` retains exact
prior bytes for F1–F7 and changes only 12,014 pixels inside six registered F8
component masks: cap crown, cap band, jumper blue, cream band, trousers and
boots. Its alpha and geometry remain exact. Frank then identified a remaining
F7 → F8 boot-shape jump. V4 at
`/keeper-review/keeper-prime-turn-side-back-v4/` retains F1–F7 byte-for-byte
from V3, retains exact V3 F8 pixels above y=250, and redraws only the rear boot
assemblies below that boundary. It preserves the palette, cap top and common
floor. Frank approved the exact V4 turn on 13 October 2026 with “Approved.” Its
immutable V5 approval record and enhanced page at
`/keeper-review/keeper-prime-turn-side-back-v5/` pin every V4 frame, both strips,
the standard-uniform palette and rear boot endpoint. The page adds previous/next
frame controls and synchronized large and exact 128 × 160 game-scale animation
views; it changes no artwork. Reviewing at both scales exposed three residual
issues: F1 trousers/boots are too dark, F7 is slightly too tall and F8 carries
pixelated edges from its older low-resolution proxy. The separate V6 candidate
at `/keeper-review/keeper-prime-turn-side-back-v6/` changes only those points.
F1 receives masked palette offsets with unchanged alpha and geometry; F2–F6 are
byte-identical; F7 is uniformly reduced from 298 to 296 opaque pixels while
retaining floor y=316; and F8 is uniformly Lanczos-registered from the already
approved 1122 × 1402 smooth rear master before its six outfit masks are matched
to the approved palette. V1–V5 and the approved rear master are untouched. V6
review exposed a four-row overlap between the F8 trouser and boot colour masks,
which double-corrected the pale patches above the boot cuffs, and a smooth F8
lower silhouette roughly five percent narrower than the accepted V4 endpoint.
V7 at `/keeper-review/keeper-prime-turn-side-back-v7/` keeps F1–F7 byte-identical
to V6. Its F8 uses disjoint `[202,254)` trouser and `[254,317)` boot masks and
eases the high-resolution master to five-percent lower-leg expansion before
normalization. The resulting lower bounds exactly match V4 at
`[75,260,180,316]`; the floor and full F8 bounds remain unchanged. V6 remains
immutable provenance. After review exposed that the far-left ear appeared too
abruptly at the 180° endpoint, V8 at
`/keeper-review/keeper-prime-turn-side-back-v8/` retained every V7 pose
byte-for-byte and inserted eight smooth 1122 × 1402 authored intermediates.
It runs 16 poses at 16 fps over the same one-second duration as V7's eight poses
at 8 fps. Frank found the result significantly jerkier, so V8 is rejected
provenance and must not establish a general higher-frame-rate rule. V9 at
`/keeper-review/keeper-prime-turn-side-back-v9/` returns directly to V7, keeps
all eight V7 frames byte-identical and adds only one controlled 172.5° pose
between 165° and 180°. It runs nine poses at 9 fps over the same one-second
duration; the midpoint is 297 pixels high between its 296- and 298-pixel
neighbors, with the common floor at y=316. Frank approved exact V9 on 13
October 2026 with “approved”. V10 at
`/keeper-review/keeper-prime-turn-side-back-v10/` pins the nine frame hashes,
midpoint source and masks, 9 fps / one-second strips and sidecars, V8 rejection
and approval wording without changing artwork. Both workbench lanes remain
empty; no production sprite or runtime animation has changed.

Frank authorized and then approved a **Keeper Prime Construction Rig (KP Rig
V1)** before animation redrafting. His exact 13 October 2026 approval was
“Approve KP Rig V1, let's see it animated”. The immutable versioned V1 review
pack registers a posable 2D
bone/joint skeleton, fixed segment lengths, front/side/back body-volume
envelopes, head/ear/shoulder/chest/waist/hip measurements, beard/hair and
clothing datums, prop contacts, pose limits, occlusion order and floor anchoring.
Its public pose lab rotates limbs without changing their registered lengths.
The rig distinguishes invariant anatomy from view-dependent projected widths
and never mechanically stretches finished beard, hair or clothing art. Its
separate V2 construction-motion proof remains immutable provenance. Frank
judged it otherwise very good but asked for more leg movement, more steps and a
slower walk. V3 at `/keeper-review/keeper-prime-rig-v3/` changes only that walk:
eight steps over five seconds at 168 px/s rather than two steps over two seconds
at 420 px/s, with greater thigh swing and knee lift. Idle, reach and planted-
ankle sit/stand are exact V2 records. This deliberately simplified mannequin
deforms no finished raster and promotes nothing. Frank approved Motion V3 on 13
October 2026 with “Approved, very good indeed”. Its first authorized derived-art
task produced the separate rigged Side-right V1, now approved as an artwork
authority. Its first animation derivative is the eight-pose front ↔ side Turn
V1, now approved with its slight 45° cadence limitation recorded. Its second
animation derivative is the approved eight-pose side-right ↔ back V4 turn,
pinned by V5. V6 records the first separate scale-review refinement; V7 is the
current unapproved correction of its F8 lower-leg mask and geometry defects.
V1–V9 remain reversible provenance; V8 is rejected and exact V9 is the approved
side-right ↔ back authority pinned at
`/keeper-review/keeper-prime-turn-side-back-v10/`. Every
rig-derived model must keep a super-smooth high-resolution
master; rough edges or jagged internal linework fail even when all geometry
datums pass.

Frank approved exact Walk V6 on 14 October 2026. The artwork-free immutable V7
record at `art/drafts/keeper-prime-walk-2026-10-14-v7/`, reviewed at
`/keeper-review/keeper-prime-walk-v7/`, pins all eight V6 frame hashes, the strip
and 8 fps timing. V1–V5 remain immutable provenance; V2 is still V1's
byte-identical routing wrapper. V4's rear-arm-only correction did not solve the
gait. Frank's decisive observation was that the accepted legs already define
the arm timing: the two arms must be derived together from those eight phases,
not improved independently.

V5 therefore records a deterministic joint map with the near/foreground arm
back at F1, passing vertically at F3, forward at F5, passing again at F7, and
returning back through F8→F1; the far/background arm is always opposite. F1 and
F5 are byte-identical V4 endpoints. F2–F4 and F6–F8 are registered from smooth
generated sources and composited only inside declared two-arm/immediate-
occlusion masks. The two failed direct F8 attempts are rejected provenance
because both reversed the foreground/background roles; F8 deliberately reuses
the successful F2 arm source as its symmetric loop partner. The verifier rejects
out-of-mask changes and separately proves that the complete lower-leg/boot rows
remain exact V4 pixels.

Frank then identified a clear V5 F8 failure: the legs were warped. The cause was
not the accepted leg art or the arm phase map; V5 reused the successful F2 arm
source for the symmetric F8 pose but allowed one broad mask to own part of the
lower body. That admitted F2 trouser geometry into F8. V6 keeps F1–F7 exact V5
bytes and rebuilds only F8 from the accepted V4 F8 base. Two separate tightened
polygons admit the back-swinging near arm and forward-swinging far arm without
owning the central trousers or legs. The verifier proves the central trouser
region and every row containing the lower legs and boots are byte-identical to
accepted V4 F8.

The V6 page keeps absolute asset paths, preventing Vercel's trailing-slash
canonicalization from resolving frames under `/keeper-review/assets/`. It
synchronizes V5 and V6 at exact 128 × 160 game size, retains previous/next
stepping, and translates the same strip at 168 high-resolution pixels per second
for five seconds from fully hidden to fully hidden. V6 is approved locomotion
artwork, but it has not been promoted to Final or production.

Frank approved exact stop → walk → stop V1 on 14 October 2026. The artwork-free
V2 approval record at `art/drafts/keeper-prime-stop-walk-stop-2026-10-14-v2/`,
reviewed at `/keeper-review/keeper-prime-stop-walk-stop-v2/`, pins the complete
candidate. Its five-pose forward bridge
is exact approved Side-right stop, three new registered in-betweens at 15%, 50%
and 75%, and exact approved Walk V6 F1. Walk → stop is the byte-reverse of those
same five frames, so the return endpoint is the identical stop rather than a
similar redraw. Root motion is a separate deterministic schedule: acceleration
uses 2, 6, 12 and 18 high-resolution px/frame before the approved 21 px/frame
walk cadence; deceleration uses 18, 12, 6 and 2 px. Every gait pose therefore
translates, and only the deliberate four-frame start/end stop holds have zero
motion. The 32-frame review route runs two exact Walk V6 cycles and travels 412
high-resolution pixels. Large and exact 128 × 160 players, frame stepping,
route looping and isolated bridge direction controls are provided. Deterministic
verification pins source hashes, exact endpoints, transparency gutters,
forward/reverse strip order, sidecars, public assets and displacement. The route
is now an approved core transition authority; the left mirror, workbench Final
and production remain unchanged.

The completed one-at-a-time route is walk → stop → turn to camera V1 at
`art/drafts/keeper-prime-walk-stop-turn-front-2026-10-14-v1/`, reviewed at
`/keeper-review/keeper-prime-walk-stop-turn-front-v1/`. It introduces no new
character drawing. Two exact Walk V6 cycles end on Walk F1 and feed the approved
18, 12, 6, 2 px/frame deceleration into the exact Side-right neutral. That
neutral is held for one additional frame (125 ms); root motion is already zero
before the approved side-right → front turn begins. The route ends on the exact
Prime front neutral. The standalone 13-frame join strip includes Walk F1 as its
entry contact for evidence; when stitched after a complete walk loop, runtime
enters at strip frame 2 so Walk F1 is not duplicated. The route has 32 review
frames, travels 374 high-resolution pixels, and provides synchronized large and
exact 128 × 160 playback plus frame stepping. Deterministic verification pins
all three approval records, every source/public hash, endpoint equality,
transparent gutters, strip/sidecar order and the condition that translation has
stopped before rotation. Frank judged the route excellent, then approved the
separate Fast Timing V1 profile described below. The frame sequence, joins and
root motion remain unchanged. Final and production remain unchanged.

Keeper Timing Lab V1 is deployed at `/keeper-timing-lab` and its original
10 fps turn-only proposal remains immutable history in
`art/drafts/keeper-timing-lab-2026-10-14-v1/`. Frank used that platform to save
`Fast walk to front turn`, then explicitly approved it with “approve fast
timing v1” on 14 October 2026. The separate immutable approval record is
`art/drafts/keeper-fast-transition-timing-2026-10-14-v1/` and its V2 catalogue
is `public/keeper-timing-lab/catalog-v2.json`.

**Fast Timing V1** sets walk to 10 fps, deceleration to 12 fps, the neutral
settle to 0 ms, the seven-frame turn to 16 fps and the front endpoint hold to
625 ms. The complete 32-frame review route lasts approximately 2.996 seconds
instead of 4.000 seconds. It is the project timing authority only for
locomotion, stopping bridges, facing turns and their brief readable endpoint
hold. It deliberately does not govern action entry, action loops, action exit,
comic reactions, prop choreography or any activity-specific performance;
those remain independently timed so entertaining actions can be savoured.
Artwork pixels, frame order, root motion and endpoints remain exact. The
profile does not enter Workbench Final or promote production sprites.

The next one-at-a-time composite was walk → stop → turn fully away V2 at
`art/drafts/keeper-prime-walk-stop-turn-back-2026-10-14-v2/`, prepared for
review at `/keeper-review/keeper-prime-walk-stop-turn-back-v2/`. It introduces
no new drawing and is pixel/timing-identical to V1. V2 uses fresh versioned
archive paths and waits for every moving frame to load and decode before
playback, correcting V1's delivery flicker without altering the animation.
Two exact Walk V6 cycles feed the approved 18, 12, 6 and 2 px
deceleration, after which all root motion is zero. The exact Side-right stop is
the geometric turn seam; Fast Timing V1's zero settle means the visually
equivalent V9 F1 is not replayed, and playback proceeds directly into exact V9
F2 through F9. The route therefore contains 32 playback frames, travels 374
high-resolution pixels and lasts approximately 3.058 seconds, including the
625 ms rear hold. The 13-frame standalone join starts with Walk F1 for evidence
but runtime enters at frame 2 after the loop. Deterministic verification pins
all four approval authorities, per-frame timing and displacement, exact source
and public hashes, transparent gutters, strip/sidecar order, aligned side-entry
alpha bounds, the exact rear endpoint and unchanged Workbench/production
hashes. Its large and exact-game-scale travel lanes are full width. Frank
approved that exact preload-safe route on 14 October 2026 with “good now
working fine. approved.” The approval-only V3 record is
`art/drafts/keeper-prime-walk-stop-turn-back-2026-10-14-v3/`. It is now a core
transition authority but has not entered Final or production. V1 stays
unchanged as historical provenance.

The active review batch is now the movement foundation documented in
`docs/CODEX_TO_CLAUDE_VERTICAL_CIRCULATION_2026-10-14.md`: exact-pixel root
Gate 1 plus measured construction motion for alternating stairs, a straight
ladder and lift entry/exit. Its 60-lp finished-floor pitch and 105-lp stair core
are proposals awaiting Frank's review, not runtime geometry.

The first finished-art stair gate is
`/keeper-review/keeper-prime-stair-ascent-v1/`. It joins one exact approved
mirrored Walk V6 cycle directly into an advancing eight-pose climb with zero
pause frames, then repeats the cycle eight times over the exact 16-riser,
84-lp-run, 60-lp-rise flight. Deterministic root closure is 84 ku × 60 ku per
cycle and 672 ku × 480 ku per flight. The V1 endpoint remains in continuous
climb; landing dismount, descent and opposite parity are not yet proposed.
Nothing is approved, in Final or in production.

Frank rejected Stair Ascent V1's visual execution on 15 Oct 2026 because the
approach sprite faced backwards relative to its leftward root motion and the
second climbing leg remained too static. V1 remains immutable rejected
provenance. `/keeper-review/keeper-prime-stair-ascent-v2/` was the first
unapproved correction attempt: its approach frames are exact horizontal mirrors of
approved Walk V6, while its eight-pose climb is redrawn to follow Walk V6's
first-leg F1–F4 and opposite-leg F5–F8 phase authority. The measured route,
zero-pause join, Final and production remain unchanged.

Frank rejected V2 after motion review because its declared phase change still
did not produce a readable opposite-leg transfer and the left boot dropped
below the stair surface. V2 remains immutable rejected provenance.
`/keeper-review/keeper-prime-stair-ascent-v3/` redraws and registers each
pose separately against a deterministic two-step contact rig: near leg F1–F4,
far leg F5–F8. The prepared left/right cells are 256×320 with transparent
gutters, exact mirrors and a fixed lowest-sole y=316 datum. Review placement
maps that sole to the mathematical top of its active tread; the review UI can
show the contact line and loop only one two-step cycle. V1/V2, approved walk
pixels, route geometry, Final and production remain unchanged.

Frank rejected the unmasked V3 presentation after motion review because the
distance visible between its boots reads as jumping two treads at once. V3 is
immutable rejected provenance as an unmasked presentation.
`/keeper-review/keeper-prime-stair-ascent-v4/` is a deliberately
cheap presentation test: it reuses the exact V3 artwork hashes, timeline,
timing, root motion, stair geometry and contacts, and adds only a foreground
closed stringer plus bannister at z-index 7. This layer hides the boots and
lower shins while leaving the knees and body readable. It is enabled by
default and toggleable for direct masked/unmasked comparison. V4 owns 17
versioned archive aliases, all resolving to the same 17 immutable V3 objects;
no binary art is duplicated and nothing has moved to Final or production.

Frank accepted V8’s vertical registration but rejected the remaining
horizontal overlap between the forward toe and each next riser. V8 remains
immutable rejected provenance. The active unapproved
`/keeper-review/keeper-prime-stair-ascent-v9/` shifts only the complete Keeper
root 1.5 lp/12 source pixels back/right. Pixel measurement now leaves at least
0.25 lp/2 source pixels of transparent clearance ahead of the toe. Both image
hashes, all vertical coordinates, support/target guide positions, 320-ms
timing and stair dimensions remain exact V8 values. V9 is still a four-contact
mechanical gate only, not the complete ascent, and nothing is approved, in
Final or in production.

V11 is rejected after live review. Its frame 7 support sole is exactly one
60÷14-lp riser above the stair, and its largest arm displacement is only seven
source pixels/0.875 logical pixels, so neither arm reads as moving. The V11
verifier checked that lower-body pixels did not penetrate the stairs but failed
to require a sole to make positive support contact. Preserve V11 unchanged as
evidence of that rejected contract.

The accepted geometry/contact foundation is
`/keeper-review/keeper-prime-stair-ascent-v12/`. V12 returns to two binding
contact drawings before intermediates are reintroduced. The flight keeps the
exact 60-lp rise and fourteen equal risers but deepens each tread from 6 to 7
lp, producing a 98-lp run inside the reserved 105-lp stair core. The V6/V7
contact-lock process is retargeted to a measured 55.5-source-pixel/6.9375-lp
foot separation. Every support sole touches its tread exactly; the upper sole
is within 0.036 lp of the next tread; and the next frame inherits that upper
foot within 0.063 lp horizontally and 0.036 lp vertically. Generated studies
contribute only the declared arms, producing plainly opposite silhouettes;
the Prime head and contact legs remain protected. V12 deliberately contains
no weight-transfer intermediates yet. Frank accepted this construction on 15
October 2026 with “yes you've got it”, pinning the geometry and contact basis
without promoting a complete animation to Final or runtime.

The superseded V13 review gate is
`/keeper-review/keeper-prime-stair-ascent-v13/`. It preserves those contact
frames and all V12 geometry exactly, then inserts one raised V6 pose-3 passing
drawing per leg: LEFT contact → RIGHT passing → RIGHT contact → LEFT passing →
LEFT contact. This makes each step span two frame intervals. The support boot
is mathematically locked to the same tread through each handover, while the
arms travel from one V12 opposing extreme through the neutral passing pose to
the other. Built-in image generation supplied two alternative midpoint-arm
studies, but both reached an endpoint-like extreme too early; they are saved
as rejected provenance and contribute no candidate pixels. V13 remains
reversible, unapproved and absent from Final, runtime and production. Live
review found that its arms reached overly large endpoints without quite
matching the leg phase, and that F4's extended left boot entered the stair
profile before its flat F5 contact.

The V14 art correction is
`/keeper-review/keeper-prime-stair-ascent-v14/`. It preserves the V12 geometry
and V13 five-frame cadence while replacing only masked arm and moving-lower-leg
regions. Contact hands are ±14.55 source pixels from the x=137 vertical datum;
the far/right arm has at most 100 sampled visible skin pixels and reads as
torso-occluded. The compact passing boots rise before extending. Deterministic
per-pixel comparison against the complete 14-riser stair reports zero
penetration in both passing frames, including 1.59 lp minimum F4 clearance.
Out-of-mask pixels, Final, runtime and production remain exact and unchanged.

The V15 full-flight review is
`/keeper-review/keeper-prime-stair-ascent-v15/`. It introduces no new artwork
and repeats the exact four V14 candidate bytes across the binding V12 stair
geometry. One initial tread-1 contact is followed by thirteen passing/contact
pairs, producing 27 frames, fourteen alternating landings and a final contact
on tread 14 at the 80-lp upper-floor datum. The review player stops and holds
at the top; it never teleports back to the floor. V15 is an unapproved,
reversible timeline candidate only and leaves Final/runtime/production
unchanged.

The approved V16 stair-ascent authority is
`/keeper-review/keeper-prime-stair-ascent-v16/`. It preserves every V15
timeline/root/timing value and changes only three declared pixel masks. RIGHT
compact passing now shares LEFT's y=270 moving-region lower boundary while
keeping 1.59 lp of minimum stair clearance and zero penetration. LEFT contact's
detached flesh remnant is restored to the exact V6 base pixels. RIGHT contact's
forward boot gains a complete toecap while its y=282 sole/contact row remains
byte-identical. Frank accepted exact V16 on 15 October 2026 with “OK let's say
that's done, had enough of refining it.” V17 is an approval-only pack: it pins
the exact V16 register, rig, page and four frame hashes without duplicating art
or changing Final/runtime/production.

For the later staircase build, retain the approved fourteen-riser, 7-lp-tread,
98 × 60-lp flight and add exactly two newel posts, at the lower entrance and
upper landing. Join them with a continuous handrail over a foreground
open-side balustrade of regularly spaced balusters. The balustrade is an
architecturally honest occlusion layer above the Keeper, deliberately covering
parts of the boots and lower legs; stair treads and rear structure remain
behind him. Review this scenery separately at large and exact game scale.

The first door/stair transition proposal is the immutable candidate page
`/keeper-review/keeper-prime-stair-transitions-v1/`, backed by
`art/drafts/keeper-prime-stair-transitions-2026-10-15-v1/`. It has two focused
routes plus a complete door-to-door playback:

1. Begin an exact mirrored Walk V6 cycle while the Keeper is hidden behind the
   lower door, emerge, complete one full visible cycle from x=140.5 to x=119.5,
   then advance from Walk F8 into Stair V16 F1 without a stop or repeated root.
2. Show the final five approved stair frames, transfer the trailing foot onto
   the flat landing with exact mirrored Walk V6 F3, establish the exact side
   neutral at x=14.5, turn through the Prime full-face frame to side-right,
   accelerate and cross the upper hallway door at x=140.5 before finishing
   fully hidden at x=161.5.

The landing-to-door distance is 126 lp, exactly twelve 10.5-lp step intervals;
door-to-hidden is one further 21-lp cycle. Walk and turn playback use approved
Fast Timing V1 (10 fps and 16 fps); the approved stair cadence remains 110 ms.
The continuing route suppresses V16's terminal 900-ms review hold because the
Keeper is exiting rather than stopping on the landing. The four acceleration
frames carry proposed candidate-42 root deltas 3, 7, 13 and 19 ku; their art is
exact approved bridge art, but the new root schedule is not approved.

The builder rejected both generated landing studies. One redrew the silhouette
too broadly and the other was wrong-facing with three arms. They remain only
under the draft pack's `sources/rejected/` provenance folder. The timeline,
public asset list and verifier contain no rejected-study bytes. The review page
preloads all 27 unique images, supports pause/previous/next/restart/loop,
sequence selection, root guides and door-occlusion removal, and displays both
a 960-pixel inspection world and exact game scale. Run
`npm run verify:keeper-prime-stair-transitions-v1`; it fails on authority hash,
cell geometry/gutter, join/root, route/page, rejected-source or approval-boundary
drift. No strip is emitted for this composition-only gate; source strips and
sidecars remain unchanged and separately verified. Final, runtime and
production remain unchanged pending Frank's explicit visual approval.

V2 at `/keeper-review/keeper-prime-stair-transitions-v2/` supersedes only the
lower walk-to-stair seam after Frank identified a brief size flash between V1
frames 16 and 17. The cause was a broad mirrored Walk V6 F8 silhouette changing
directly to compact Stair V16 F1. V2 preserves both complete eight-frame walk
cycles, every root, every approved source byte and the full upper route. It
rotates each cyclic walk order to F8,F1,F2,F3,F4,F5,F6,F7, then inserts the
exact approved Stair V16 LEFT compact passing cell at the unchanged floor
baseline before first-tread contact. The focused nine-frame seam is the default
review sequence. No frame is held, redrawn or rescaled, and V1 remains
immutable. Run `npm run verify:keeper-prime-stair-transitions-v2`; Final,
runtime and production are still unchanged pending visual approval.

V3 at `/keeper-review/keeper-prime-stair-transitions-v3/` changes only the
reviewer after Frank reported whole-page movement and an unusably small game
preview. The per-frame readout now occupies a fixed 3.1-em block, preventing
long labels from shifting either stage. The unchanged second stage is rendered
at four screen pixels per logical pixel—the Studio's actual default `zoom=4`,
so a 32 × 40 Keeper cell appears at 128 × 160 screen pixels—and is stacked
below the 6× inspection stage. V2 route JSON is exact apart from its versioned
asset prefix; all 27 source hashes, timing and roots are unchanged. Run
`npm run verify:keeper-prime-stair-transitions-v3`.

V4 at `/keeper-review/keeper-prime-stair-transitions-v4/` corrects the
remaining visible size contraction at lower-route F16→F17. The last walk pose
has a measured 293-source-pixel cap-to-root span; every Stair V16 drawing has a
285-pixel span. Rather than resizing only the join and creating a new F17→F18
flash, V4 applies one uniform 293/285 (1.028×) display registration to every
stair and stair-mount frame around the shared `[16,39.5]` logical-pixel root.
The four approved stair PNGs, all other source hashes, route order, timing,
world roots and tread geometry remain unchanged. V1–V3 remain immutable. Run
`npm run verify:keeper-prime-stair-transitions-v4`; Final, runtime and
production are unchanged pending Frank's visual decision.

Live review showed that V4 still read smaller: matching only the cap-to-root
span did not match the mass of the complete character. V5 at
`/keeper-review/keeper-prime-stair-transitions-v5/` therefore uses the full
opaque silhouette. Walk F7 contains 27,322 opaque source pixels and the Stair
V16 LEFT compact passing authority 24,299; the common stair-family linear
registration is `sqrt(27322/24299) = 1.060381…`. It applies around the same
registered root to every stair and mount frame in every route. No source PNG,
timing, root, tread, Final or runtime record changes. V4 remains immutable but
is superseded for review. Run `npm run verify:keeper-prime-stair-transitions-v5`.

Before V5 was published for review, Frank chose the stronger architectural
solution: scale reconciliation may occur while the Keeper is completely hidden
behind a room door, but never at a visible walk/stair join. V6 at
`/keeper-review/keeper-prime-stair-transitions-v6/` leaves Stair V16 at native
scale 1. Every walk, turn, acceleration/deceleration bridge and door-reach
frame from lower-door emergence through upper-door disappearance uses one
constant `sqrt(24299/27322) = 0.943057…` circulation scale. The departure
handoff finishes before he becomes visible and the inverse handoff occurs only
after full arrival-door occlusion. Thus the visible door-to-door route has zero
scale changes. V5 is retained as rejected provenance; source PNGs, timing,
roots, tread geometry, Final and runtime remain unchanged. Run
`npm run verify:keeper-prime-stair-transitions-v6`.

Frank approved exact Stair Transition V6 on 16 October 2026 with “Approved.
Move on to ladder.” The immutable approval record is
`docs/review/keeper-prime-stair-transitions-v6-approval-2026-10-16.json`.
This is approval for later Final preparation only; no runtime or production
promotion occurred.

## Keeper Prime ladder transition V1 (16 Oct 2026)

The first reversible ladder gate was
`/keeper-review/keeper-prime-ladder-transitions-v1/`. The legacy 8-frame ladder
strip is retained only as rejected/comparison provenance; no legacy pixel is
used. V1 derives its rear identity, palette and rear-facing boots from the
approved smooth back master. Five generated high-resolution studies supply the
first-rung mount, one asymmetric contact, one compact passing pose, a rightward
top transfer and its flat-footed landing completion. Contact B and passing B
are exact deterministic mirrors, guaranteeing equal left/right participation.

The ladder is vertical and 18 lp wide. Eight 7.5-lp rung intervals close the
approved 60-lp floor pitch, using four complete gait cycles with a 3.75-lp rise
per displayed transition frame. The continuous route hits the next floor
exactly on frame 17 and carries on without resetting phase. The lower-door
approach spans exactly 84 lp/eight walking intervals before the approved stop
and side-to-back turn. The upper route transfers right, establishes both boots
on the landing, turns back-to-side and walks 42 lp/four intervals into the
upper door. All visible art uses the approved 0.943057 circulation scale; any
room-scale handoff stays under complete door occlusion.

The page preloads and decodes all 29 unique image URLs before playback, keeps
large and 4× panes stacked, and supplies route selection, pause/play, one-frame
stepping, speed, looping and contact guides. Run
`npm run verify:keeper-prime-ladder-transitions-v1`. The draft is unapproved;
Final, runtime and production remain unchanged.

## Keeper Prime ladder transition V2 (16 Oct 2026)

Live V1 review found the animation generally sound, but central ladder rungs
flashed through the changing transparent gaps of the Keeper during the bottom
turn. Frank requested that the turn run faster and the climb significantly
slower. He accepted the residual hand/foot-to-rung mismatch as tolerable,
particularly at game scale, so V2 does not redraw or reposition any body part.

V2 at `/keeper-review/keeper-prime-ladder-transitions-v2/` keeps all 29 V1
image hashes, every route frame, root position, art scale, rung dimension and
contact point unchanged. A 12 × 38-lp central-rung occluder is rendered at
z=3—above ladder z=2 and below Keeper z=4—only while their bodies overlap. It
uses the stage background and hides the central rung segments that caused the
flash while leaving both side rails visible. Turn frames change from 62.5 ms
to 50 ms (20 fps); ladder mount, contact, passing and dismount frames use 150
ms (6.67 fps). V1 remains immutable. Run
`npm run verify:keeper-prime-ladder-transitions-v2`; V2 is unapproved and
Final, runtime and production remain unchanged.

Frank rejected the V2 presentation on 16 October 2026 because its rectangular
occluder removed the middle of every rung as the Keeper climbed. His explicit
correction was to make the Keeper opaque, not remove any part of the ladder.
V2 remains immutable rejected presentation provenance.

## Keeper Prime ladder transition V3 (16 Oct 2026)

V3 at `/keeper-review/keeper-prime-ladder-transitions-v3/` removes the rung
occluder completely, so both rails and every full rung are constructed in
every frame. It creates new versioned derivatives of all 29 unique registered
Keeper review images using the established post-resize alpha threshold: alpha
values at or above 128 become 255; lower alpha becomes zero. Every retained
RGB value is byte-identical to V1/V2, and no alpha reaches a cell edge.

Frame order, roots, visible scale, ladder geometry, rung contacts and route
dimensions remain exact. V2's requested timing remains: 50 ms per turn frame
(20 fps) and 150 ms per ladder mount/contact/passing/dismount frame (6.67 fps).
Run `npm run verify:keeper-prime-ladder-transitions-v3`; V3 is unapproved and
Final, runtime and production remain unchanged.

Frank then reported persistent flickering throughout the complete V3 route.
V3 remains immutable rejected presentation provenance. Two causes were pinned:
its binary threshold discarded the source antialiased fringe, and the review
runtime removed/recreated the ladder and Keeper image on every playback frame.

## Keeper Prime ladder transition V4 (16 Oct 2026)

V4 at `/keeper-review/keeper-prime-ladder-transitions-v4/` restores the smooth
pre-V3 source fringe while making the Keeper's solid paint genuinely opaque:
source alpha ≥240 becomes 255, alpha 1–239 remains exact and every RGB byte is
unchanged. The complete ladder remains present with no occlusion mask.

All 29 unique images are decoded and mounted in both review stages before the
controls unlock. The ladder, floors, doors, guides and image nodes persist for
the life of the page; playback performs only an atomic visibility switch and
position update. Deterministic verification rejects image/architecture DOM
creation during `renderStage`, stale asset prefixes, broken alpha mapping,
geometry/timing drift and promotion. Run
`npm run verify:keeper-prime-ladder-transitions-v4`; the V4 candidate leaves
Final, runtime and production unchanged.

Frank approved exact V4 on 16 October 2026 with: “Approved. Turn should be
twice as fast but that can be fixed another time.” The immutable record is
`docs/review/keeper-prime-ladder-transitions-v4-approval-2026-10-16.json`.
This approves all 29 exact frame hashes, the smooth opaque-paint treatment,
complete-ladder persistent compositor, roots, geometry, frame order and route
choreography. It explicitly does not finalise turn cadence. A future
timing-only version must change turn frames from 50 ms to 25 ms (20 to 40 fps)
without modifying pixels, roots or geometry. Run
`npm run verify:keeper-prime-ladder-transitions-v4-approval`; approval itself
changes no Final, runtime or production asset.

## Stair Descent V2 approval and seated foundation (16 October 2026)

Frank approved the exact Stair Descent V2 review route, accepting its slight
visible overstride because the future foreground stair treatment will help
mask the feet. Preserve the complete candidate and its hashes. The finished
staircase remains a separate unapproved art task: it requires two newel posts,
a foreground balustrade and a continuous handrail, but may not change the
stored fourteen-riser, 7-lp-tread, 98-by-60-lp geometry. The decision is pinned
at `docs/review/keeper-prime-stair-descent-v2-approval-2026-10-16.json`. No
Final, runtime or production promotion was performed.

The current corrected gate is
`/keeper-review/keeper-prime-seated-six-view-v2/`. It reuses the six V1 images
byte-for-byte, fixes the V1 loader and proves physical chair contact at y=29
lp; V1 remains historical evidence. The endpoint set defines
six new smooth Prime Keeper seated endpoints: direct front, direct back,
side-left/right and rear-left/right. “At an angle either side” means the rear
three-quarter pair used for TV, gaming and furniture-facing activity. All six
use a 32 × 40 logical cell at density 8, `[16,40]` floor anchor, `[16,29]` seat
point and 11-lp seat height. Their registered opaque bounds share y=52…315;
the left profile and rear-left are exact completed-cell mirrors of the right
views. The character is isolated from all furniture. Prime standing art is the
identity/rendering authority and the old seated neutrals are pose mechanics
only.

Do not build all motion blindly from the historical strips. After Frank
approves these endpoints, author the actual transition clips in three small
gates: side right plus exact mirrored left; front and back; then the rear-angle
pair. Each begins on the relevant approved standing authority, follows the
approved planted-ankle sit/stand rig, and lands byte-exactly on this seated
endpoint. Timing remains a review-tool parameter. No endpoint in this pack is
yet approved or promoted.

## Review-comments workflow for a later feedback round

1. Do not process another review export until the beard evidence gate is
   resolved with GPT-5.6 Sol: author/pin normalized beard masks, facial
   landmarks and hand depth/component ownership evidence, then rerun the
   fail-closed audit. Only after that may the remaining audits run in order:
   `docs/prompts/KEEPER_SPRITE_FRAME_ISOLATION_AUDIT.md` with GPT-5.6 Terra
   High, followed by
   `docs/prompts/KEEPER_RELEASE_SURFACE_DATUM_AUDIT.md` with GPT-5.6
   Terra High: it audits every release hand-off and makes standard tabletop
   support 19 logical pixels above floor, 8 pixels above the purple 11-pixel
   seat guide. Then use `docs/prompts/KEEPER_POST_AUDIT_REVIEW_DELTA.md` for the next
   review round.
2. Read the latest submitted review-handoff queue entry and every saved
   per-animation note before triage or drawing. A full-re-draft flag authorises
   rebuilding the clip; it never authorises ignoring that clip's written notes.
   Treat beard-length and side-silhouette comments as identity corrections that
   must be checked frame by frame against `keeper_walk` and the nearest approved
   side-pose reference. Specifically flag smooth/bulbous outlines that lose the
   canonical stepped, slightly ragged margins. Prefer exact filenames from the
   review cards.
3. Save a dated, immutable source copy under `docs/review/`, record its
   SHA-256, then create a
   working resolution table with columns: filename, frame(s), comment, class,
   decision, proposed change, status, verification and commit.
4. Check whether each comment concerns identity/scale, drawing quality,
   frame-order/timing, crop/bleed, object geometry, or route/transition.
5. Delete rejected/obsolete art from the review/runtime inventory rather than
   leaving it available for accidental use; keep provenance/history only where
   needed to rebuild or understand a replacement.
6. Resolve P0 neutral/walk-stop/turn metadata and art before bulk object wiring.
7. Test complete routes, not just actions: walk in, settle, turn/posture change,
   act, reverse/exit and walk away.
8. Rerun all verification, inspect the viewer with global pause and ghost, and
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

## Ready-to-paste opening prompt for the next review iteration

> Continue the Lighthouse Keeper amendment review in `/Users/frank/Documents/ChatGPT/Lighthouse Keeper` on `main`. Read `docs/KEEPER_ANIMATION_HANDOFF.md`, `docs/KEEPER_ARTWORK_AUTHORING_AND_REVIEW_PLAYBOOK.md`, `docs/review/keeper-animation-codex-responses-2026-10-12.json`, `art/drafts/keeper-review-amendments-2026-10-11-v1/README.md`, `art/drafts/keeper-party-hat-put-on-back-hands-2026-10-12-v2/README.md`, `art/drafts/keeper-party-hat-put-on-back-front-arm-plane-2026-10-12-v3/README.md`, `art/drafts/keeper-carry-shopping-right-bag-2026-10-12-v2/README.md`, `art/drafts/keeper-play-drums-back-hands-2026-10-12-v2/README.md`, `art/drafts/keeper-put-record-removal-2026-10-12-v2/README.md` and `art/drafts/keeper-put-record-horizontal-frame5-2026-10-12-v3/README.md`. Treat handoff `d9081e53-2808-4b1f-8422-2df09cf38c3c` and its 81 exact names as the only scope. Review the 41 exact-name amendment candidates plus retained v2/v3 comparisons for `keeper_party_hat_put_on_back` and `keeper_put_record`, the `keeper_carry_shopping` frames-1/7 correction and the `keeper_play_drums_back` frame-6 correction. The party-hat v3 keeps frame-2 arms clear of the head; the put-record v3 keeps a level record in frame 5 and removes it in frames 6–8. Preserve canonical art, all historical variants and the 12 retained `withdrawn-by-user` face-to-camera candidates. The deleted `keeper_count_money` amendment must not be regenerated without a new explicit instruction. Do not reactivate, regenerate or promote any other face-to-camera amendment without an explicit new instruction. Iterate with Frank on `keeper_fish_seated`, `keeper_shower_exit` and `keeper_shower_wash`; leave `keeper_slide_side` deferred until helter-skelter geometry exists. Promote nothing without explicit approval.

## Ready-to-paste opening prompt for full-face normalisation

> Work in `/Users/frank/Documents/ChatGPT/Lighthouse Keeper` on `main`. Read `docs/KEEPER_ARTWORK_AUTHORING_AND_REVIEW_PLAYBOOK.md` and `docs/KEEPER_ANIMATION_HANDOFF.md` completely before changing anything. The new objective is to normalise every full-face/front-facing Keeper animation around the full-face canon Frank has selected. Use `art/raw/keeper-first-batch/keeper_neutral_standing-front_f1.png` as the primary geometry authority and `art/drafts/keeper-artist-smock-family-redraw-2026-10-11-v11/drafts/keeper_artist-smock_neutral_standing-front_f1.png` as the recent rendering-quality reference. The canon is an adult, restrained face with solid dark rectangular eyes, a clearly defined separate moustache, a readable closed mouth and the established beard mass. Do not use the cheesy pixie grin, a generic smile, oversized or round childlike eyes, white eye glints, or a mouth merged into the moustache. Action-specific expressions are allowed only as controlled deviations that return cleanly to the neutral canon.
>
> Start with a read-only inventory of every production animation and technical neutral whose pose is full-face/front-facing, grouped by standard uniform, outfit/costume, seated, locomotion, interaction and expression. Identify exact frame ranges, current face families, outfit dependencies, endpoints and transition risks. Treat the previously withdrawn face-camera amendments as rejected provenance only; do not reactivate them, and do not regenerate the explicitly deleted `keeper_count_money` amendment without a new direct instruction. Then create a versioned, reversible full-face canon pack from the two selected references: at minimum a standard standing neutral, its exact head/face landmarks, beard/moustache/mouth masks or guides, and comparison evidence against both references. Show that canon pack for Frank's approval before applying it across the inventory.
>
> After the canon pack is approved, normalise the animations methodically in small reviewable batches. Preserve each animation's accepted body, outfit, prop, timing, emotion and action wherever possible; amend only the head/face region unless anatomy or occlusion makes a wider change unavoidable. Keep identity, scale, floor anchor and head position stable across adjacent frames, and design first/last frames for seamless transitions into the registered neutral and neighboring clips. Every frame's character, clothing, props and effects must remain isolated inside its declared cell with a transparent safety gutter. Add deterministic verification for cell edges, geometry, unchanged out-of-scope pixels, endpoint continuity and strip/sidecar agreement.
>
> Make every proposal in a new versioned draft directory. Never overwrite canonical raw/runtime art, existing drafts, manifests, immutable review exports or current previews. Record original and draft SHA-256 values and publish canonical, historical drafts and each new candidate side by side in the existing online review platform. Promote nothing without Frank's explicit approval. Keep the repository documentation current, test the complete reviewer and sprite contract, commit and push finished review batches to remote `main`, verify the public deployment and leave the work ready for iterative visual review.
