# Lighthouse Keeper

A Sims-style lighthouse game for Ralph and Eddie: tell the keeper what to do by typing or tapping objects, then keep him happy through the day. The playable cutaway currently has a kitchen, living room, bedroom with en suite, and lamp room.

The current Keeper-art review gate is the six-direction smooth seated
foundation at `/keeper-review/keeper-prime-seated-six-view-v1/`: front, back,
both profiles and both rear-three-quarter angles. Every endpoint shares the
32 × 40 logical cell, 11-lp seat height and registered floor anchor. It is a
reversible draft only; after visual approval it will become the exact target
for the stand ↔ sit transition clips. Stair Descent V2 is approved with its
slight overstride accepted; the future finished staircase must retain its
locked geometry while adding two newel posts, a foreground balustrade and a
continuous rail. The approval record is
[`docs/review/keeper-prime-stair-descent-v2-approval-2026-10-16.json`](docs/review/keeper-prime-stair-descent-v2-approval-2026-10-16.json).

The current runtime still uses the first-generation room plates. The agreed
replacement standard-room geometry is **172 × 56 logical pixels**, with a
46-pixel doorway exclusion and twelve 10.5-pixel furnishing/interaction
intervals. Drag/drop, expansion and pacing requirements are in
[`docs/KEEPER_ROOM_GRID_172_HANDOFF_2026-10-14.md`](docs/KEEPER_ROOM_GRID_172_HANDOFF_2026-10-14.md);
implementation is pending and must not rescale the historical room art.

A new reversible movement-foundation batch is ready for review, but is not
approved or wired into the game. `/keeper-review/keeper-root-motion-gate-v2/`
plainly compares the exact approved stop/walk images under the current 76-ku
and proposed 84-ku stop-to-stop schedules. The separate
`/keeper-review/keeper-vertical-circulation-v2/` construction lab establishes
a proposed 60-lp finished-floor pitch (56 clear + 4 shared deck), 16-step
alternating flights, a straight ladder and lift entry/exit routes before any
finished animation art is drawn. Its 4× pane is an authoring ruler, not a fixed
device-size promise: the live 1200 × 760 scene responsively fits its viewport.
The V1 pages remain immutable historical evidence. Technical details are in
[`docs/CODEX_TO_CLAUDE_VERTICAL_CIRCULATION_2026-10-14.md`](docs/CODEX_TO_CLAUDE_VERTICAL_CIRCULATION_2026-10-14.md).
The practical `/keeper-review/keeper-object-approach-oven-v1/` page places a
30 × 30 lp opaque oven proxy in the 172 × 56 lp room and shows the exact
approved walk/stop/turn-away pixels under the candidate 252-ku route. Its
comparison toggle proves that the current root schedule stops 1 lp short from
the same origin. The proxy is not oven artwork and nothing is promoted.
`/keeper-review/keeper-object-approach-oven-v7/` and its calculated 4% room /
1% furnishing convergence remain historical evidence, not the current kitchen
projection authority. The active
[`flat-cutaway-v1`](docs/KITCHEN_FLAT_CUTAWAY_PROJECTION_SPEC_2026-10-16.md)
contract uses a straight-on camera, rectangular functional fronts, constant
Keeper/object scale, no runtime depth scaling, an exact 5-lp horizontal floor
band and the real 19-lp cooker/hob datum. Kitchen V5 remains the sole visual
baseline at `/keeper-review/kitchen-basic-assets-v5/`. Frank selected
calibration Option B (1.5-lp visible top), and the replacement full-family V6
draft is now at `/keeper-review/kitchen-basic-assets-v6-option-b/`. The earlier
gate remains immutable at `/keeper-review/kitchen-countertop-calibration-v6/`;
it shows the exact V5 kettle
counter, cooker/hob and sink beside three common 1–2-lp countertop
constructions, with logical-scale, ghost, edge and measured 21-lp-bay seam
proofs. V6 applies B across every compatible unit, keeps exact 20-lp art inside
each 21-lp bay, narrows the pedal bin to 15 lp, and locks every animation base
outside declared masks. The reusable recipe is
[`docs/KITCHEN_COUNTERTOP_OPTION_B_RECIPE_2026-10-16.md`](docs/KITCHEN_COUNTERTOP_OPTION_B_RECIPE_2026-10-16.md),
and the full hand-back is
[`docs/CODEX_TO_CLAUDE_KITCHEN_BASIC_ASSETS_V6_OPTION_B_2026-10-16.md`](docs/CODEX_TO_CLAUDE_KITCHEN_BASIC_ASSETS_V6_OPTION_B_2026-10-16.md);
the complete V5 measurements remain in
[`docs/CODEX_TO_CLAUDE_KITCHEN_BASIC_ASSETS_V5_2026-10-16.md`](docs/CODEX_TO_CLAUDE_KITCHEN_BASIC_ASSETS_V5_2026-10-16.md).
The matching review-only room redraw is at
`/keeper-review/kitchen-room-flat-cutaway-v7/`. It rebuilds the 56-lp shell as
parallel ceiling, wall, skirting and exact 5-lp floor bands for every 6–12-bay
width. Its 15-lp porthole is a separate wall child of the sink, so both move by
the same bay translation. The exact reusable architecture recipe is
[`docs/KITCHEN_ROOM_FLAT_CUTAWAY_RECIPE_2026-10-16.md`](docs/KITCHEN_ROOM_FLAT_CUTAWAY_RECIPE_2026-10-16.md)
and the hand-back is
[`docs/CODEX_TO_CLAUDE_KITCHEN_ROOM_FLAT_CUTAWAY_V7_2026-10-16.md`](docs/CODEX_TO_CLAUDE_KITCHEN_ROOM_FLAT_CUTAWAY_V7_2026-10-16.md).
The broad room-and-family correction draft is
`/keeper-review/kitchen-wall-anchored-v8/`. It keeps the V7 shell but anchors
the complete furniture composition to a common 52-lp rear-wall foot line,
leaving 4 lp of foreground floor clear. It also repairs chipped countertop
wings, replaces the fridge's wood top with bright-white appliance enamel,
reduces the bin to a 10 × 12-lp envelope, and enlarges the sink-owned porthole
to 19 lp. The porthole frame now has an alpha-clear aperture; day, sunset,
night and rain are separate swappable underlays rather than baked scenery.
The exact recipe is
[`docs/KITCHEN_WALL_ANCHORED_V8_RECIPE_2026-10-16.md`](docs/KITCHEN_WALL_ANCHORED_V8_RECIPE_2026-10-16.md)
and the hand-back is
[`docs/CODEX_TO_CLAUDE_KITCHEN_WALL_ANCHORED_V8_2026-10-16.md`](docs/CODEX_TO_CLAUDE_KITCHEN_WALL_ANCHORED_V8_2026-10-16.md).
The latest focused fridge-only correction is
`/keeper-review/kitchen-fridge-shelf-v9/`. It keeps the exact V8 room and object
family, restores dimensional light/shadow detail to the bright-white
counterless fridge, and adds a separate 19 × 17-lp plant-and-pots wall child
which receives the fridge's exact bay translation. Its reusable recipe is
[`docs/KITCHEN_FRIDGE_SHELF_V9_RECIPE_2026-10-17.md`](docs/KITCHEN_FRIDGE_SHELF_V9_RECIPE_2026-10-17.md)
and its hand-back is
[`docs/CODEX_TO_CLAUDE_KITCHEN_FRIDGE_SHELF_V9_2026-10-17.md`](docs/CODEX_TO_CLAUDE_KITCHEN_FRIDGE_SHELF_V9_2026-10-17.md).
V5, V6, Room V7, V8 and V9 remain unapproved, unpromoted and unwired.
V9 is rejected visual provenance: its flat fridge, poor shelf and wing-only
countertop repair are not a baseline. The replacement family and porthole
construction correction is `/keeper-review/kitchen-porthole-backdrop-cutout-v10/`.
V10 uses Frank's attached approved family as its visual authority, restores the
detailed white fridge and a fitted polished shelf, and draws every compatible
countertop as one uninterrupted Option-B slab across every state. It rejects the former
kitchen-owned day/sunset/night/rain illustrations: it cuts a genuine 14-lp
alpha opening through the room wall and places only the separate 19-lp brass
ring above it. The global lighthouse backdrop is therefore visible directly
through the room. The exact recipe is
[`docs/KITCHEN_PORTHOLE_BACKDROP_CUTOUT_V10_RECIPE_2026-10-17.md`](docs/KITCHEN_PORTHOLE_BACKDROP_CUTOUT_V10_RECIPE_2026-10-17.md)
and the hand-back is
[`docs/CODEX_TO_CLAUDE_KITCHEN_PORTHOLE_BACKDROP_CUTOUT_V10_2026-10-17.md`](docs/CODEX_TO_CLAUDE_KITCHEN_PORTHOLE_BACKDROP_CUTOUT_V10_2026-10-17.md).
V10 is also unapproved, unpromoted and unwired.
Kitchen V11 adds a review-only kettle-owned wall shelf of uneven recipe books
held by jar bookends. It remains inside one exact 21-lp bay, has no interaction
spot, and moves by the kettle's identical whole-bay delta. Review:
`/keeper-review/kitchen-kettle-recipe-shelf-v11/`; recipe:
[`docs/KITCHEN_KETTLE_RECIPE_SHELF_V11_RECIPE_2026-10-17.md`](docs/KITCHEN_KETTLE_RECIPE_SHELF_V11_RECIPE_2026-10-17.md).
The focused `/keeper-review/keeper-lift-entry-alignment-v1/` construction page
corrects the earlier lift choreography without rewriting it. The room-door
centre at x=126 lp and lift threshold at x=42 lp are exactly 84 lp apart:
eight 10.5-lp steps or four full two-step strides. Stop, right-hand button
press, turn-away and depth-only entry all retain the same x=42 root, so there
is no post-stop sideways slide. This placement still depends on a separately
drawn and approved Walk F5-to-neutral stop bridge before final Keeper art or
runtime wiring.
The subsequent `/keeper-review/keeper-circulation-entry-alignment-v1/` page is
the active shared-core proposal. It registers one doorway at x=115.5 lp: the
measured stair base at x=94.5 is exactly one 21-lp/eight-frame walk cycle away,
and walk F8 hands directly to an already-advancing climb F1 with zero pause
frames. The alternative lift centre at x=31.5 is exactly 84 lp/four full
strides from that same doorway. The preliminary lift-only page remains intact
as historical draft evidence; neither proposal is approved or wired.
The first finished-art circulation gate is now available at
`/keeper-review/keeper-prime-stair-ascent-v1/`. It uses one exact approved
mirrored Walk V6 cycle from the transfer door to the measured stair base, then
enters an advancing eight-pose climb with zero pause frames. Eight climb cycles
close the full 16-riser flight at exactly 84 lp run and 60 lp rise. This V1
deliberately ends in continuous climb; the upper-landing dismount, descent and
opposite zigzag parity remain separate review gates. Nothing is in Final or
production.
Frank rejected V1's visual execution because its sprite faced opposite its
leftward door-exit motion and its second leg barely moved. The immutable V1
remains as historical evidence. The first correction attempt, V2, is at
`/keeper-review/keeper-prime-stair-ascent-v2/`: its approach is an exact
horizontal mirror of approved Walk V6, and the climb redraw follows Walk V6's
first-leg F1–F4 / opposite-leg F5–F8 phase structure. Route geometry and the
zero-pause join are unchanged; nothing is in Final or production.
Frank rejected V2 after motion review because the labelled phases still did
not read as a genuine leg transfer and the left boot struck below the stair
surface. The reversible, unapproved
`/keeper-review/keeper-prime-stair-ascent-v3/` uses eight individually
registered poses: the near leg completes F1–F4 and the far leg completes
F5–F8. Each lowest contact sole is fixed at cell y=316 and mapped to the actual
tread top, while a toggle exposes that datum in the review page. V1 and V2
remain immutable rejected evidence. Frank rejected the unmasked V3
presentation because the visible boot separation reads as climbing two stairs
at once. The V4 masking experiment at
`/keeper-review/keeper-prime-stair-ascent-v4/` preserves every V3 character
pixel, root position, timing value and stair dimension, but adds a closed
foreground stair stringer and bannister above the boots/lower shins. Its mask
is on by default and can be toggled off for an exact V3 comparison. V4 reuses
the 17 V3 media hashes without adding archive objects.

Frank accepted V8’s vertical registration but rejected its horizontal toe
clearance: the forward toe overlapped each next riser. Preserve V8 as rejected
provenance. The active unapproved V9 diagnostic is
`/keeper-review/keeper-prime-stair-ascent-v9/`. V9 moves only the complete
Keeper root 1.5 lp (12 source pixels) back/right. The forward opaque toe now
keeps at least 0.25 lp/2 source pixels of transparent clearance from the next
riser. The V8 images, vertical positions, support/target markers, timing and
stair dimensions remain exact. This is still a four-contact proof, not a
complete transition. Nothing has entered Final or production.

V11 is now rejected: live review found its frame 7 support sole floating one
complete 60÷14-lp riser above the stair, while its claimed arm motion peaked at
only 0.875 logical pixels and was visually static. Its verifier proved only
non-penetration, not positive support contact; that incomplete contract is
retained as rejected provenance.

The accepted geometry/contact foundation is
`/keeper-review/keeper-prime-stair-ascent-v12/`. It resets to four binding
RIGHT/LEFT/RIGHT/LEFT contacts before any intermediates are attempted. The
finished-floor rise remains exactly 60 lp over fourteen equal risers, but tread
depth increases from 6 to 7 lp; the resulting 98-lp flight fits inside the
reserved 105-lp stair core. Each support sole must touch a real tread, each
upper sole must touch the next tread within 0.05 lp, and successive support
handovers may drift by no more than 0.07 lp. Two opposite arm silhouettes are
now plainly visible. Frank accepted that foundation on 15 October 2026 with
“yes you've got it”; this is acceptance of its stair and contact construction,
not a promotion to Final or runtime.

The superseded V13 smoothing candidate is
`/keeper-review/keeper-prime-stair-ascent-v13/`. Its five-frame proof reads
LEFT contact → raised RIGHT-foot passing frame → RIGHT contact → raised
LEFT-foot passing frame → LEFT contact. The contact endpoints are exact V12
bytes and each intermediate is an exact same-family V6 raised passing pose.
Thus every step takes two frame intervals, the planted boot stays registered
to its tread, and the arms pass from one opposing V12 extreme through neutral
to the other. Two generated arm studies are retained as rejected provenance
and contribute no candidate pixels. V13 remains review-only and changes no
Final art, runtime sprite or production geometry. Live review found its arm
endpoints insufficiently synchronized and too extreme, while F4 extended its
left boot into the stair profile before the flat F5 contact.

The V14 art correction is
`/keeper-review/keeper-prime-stair-ascent-v14/`. It keeps the same five-frame
cadence but constrains each visible hand to about 14.55 source pixels either
side of the vertical datum, leaving the far/right arm as a small torso-occluded
sliver. Both passing boots now rise before extending: deterministic comparison
against every tread and riser reports zero penetrating pixels, and F4 retains
1.59 lp of clear air above the stair profile. Only declared arm and moving
lower-leg masks change; all out-of-mask pixels are exact. Nothing is approved,
in Final or in runtime.

The V15 full-flight review is
`/keeper-review/keeper-prime-stair-ascent-v15/`. It creates no new drawings:
the four exact V14 candidate PNGs repeat across the complete fourteen-riser
flight. Its 27-frame timeline contains fourteen strictly alternating foot
contacts and thirteen passing poses, mathematically registered to every tread.
Playback reaches tread 14 and holds there rather than wrapping back to the
floor. V15 is a review-only timeline candidate; neither it nor V14 is approved
or promoted to Final/runtime.

The approved stair-ascent authority is
`/keeper-review/keeper-prime-stair-ascent-v16/`. It keeps V15's complete
timeline, placements and timing exact while correcting only three masked art
regions: RIGHT compact passing now matches LEFT's y=270 moving-region lower
edge and retains 1.59-lp stair clearance; the detached flesh remnant is removed
from LEFT contact; and RIGHT contact receives a complete forward-boot toecap
without changing its sole/contact row. Frank accepted exact V16 on 15 October
2026; the no-art V17 approval pack pins its four images, 27-frame rig and page.
Nothing is wired into runtime yet.

The later staircase scenery must use two newel posts—one at the lower entrance
and one at the upper landing—with a foreground balustrade and continuous
handrail between them. That foreground architecture may naturally cover parts
of the Keeper's boots and lower legs, but it may not change the approved
fourteen-riser contact geometry.

The approved reversible stair-transition authority is
`/keeper-review/keeper-prime-stair-transitions-v6/`. It composes exact approved
authorities plus two clearly labelled candidate door-reach cells into two
reviewable sequences: lower transfer door → two walk cycles → moving Stair V16
F1, and final Stair V16 contacts → flat landing → clockwise
side-left/back/side-right turn → hallway walk → stop/reach/open → walk through
to complete door occlusion.
The lower door is one complete 21-lp visible walk cycle from the stair root;
the upper landing is 126 lp/twelve step intervals from the matching door, with
one additional 21-lp cycle behind it. The page preloads all 27 unique cells,
offers frame stepping, root guides, door-occlusion toggling, a 960-pixel-wide
inspection pane and the Studio's default four-screen-pixels-per-logical-pixel
playback. Its
candidate-42 acceleration/deceleration roots (3, 7, 13, 19 ku) and two-frame
right-hand door reach are explicitly unapproved.
Two generated landing studies—including a wrong-facing three-armed result—are
quarantined as rejected provenance and contribute no displayed pixels. The
selected reach sources have exactly two arms and are composited only inside a
declared arm mask over the byte-identical approved side neutral. No Final,
runtime or production asset has changed.

V2 supersedes only V1's visible lower walk-to-stair seam. V1 jumped from the
broad mirrored Walk F8 silhouette directly to compact Stair V16 F1. V2 keeps
two complete approved walk cycles and the identical roots, rotates the cyclic
phase to finish on compact Walk F7, then reuses the exact approved LEFT compact
passing drawing before first-tread contact. The page opens on a nine-frame
focused seam loop. No Keeper source pixel is redrawn or rescaled; V1 remains
immutable review history.

V3 changes no route or Keeper pixel. It fixes the moving review text to a
constant height so frame-label wrapping cannot move the page, and replaces the
misleading 1× logical-pixel thumbnail with the Studio's real default 4× screen
presentation (a standard 32 × 40 logical Keeper cell appears at 128 × 160
screen pixels). The large and game views are stacked so neither is squeezed.

V4 removes the remaining visible F16→F17 size contraction. The final compact
walk pose measures 293 source pixels from cap top to the registered root; the
approved stair family measures 285. Every stair and stair-mount frame now uses
one uniform 293/285 (1.028×) display registration around the same root, so the
fix cannot move to F17→F18 or the upper landing. Source PNGs, timing, route
roots, Final, runtime and production remain unchanged. Live review showed that
matching height alone did not remove the perceived whole-body contraction.

V5 therefore matches whole-silhouette mass instead. Walk F7 contains 27,322
opaque source pixels and the stair mount authority 24,299; one uniform
sqrt(27,322/24,299), or 1.060×, root-anchored registration is applied to every
stair-family route frame. This preserves internal proportions and avoids a
one-frame patch while making the transition visibly equal in overall scale.
Frank rejected scaling the stair family as the visible solution: the size
handoff can instead occur invisibly behind the room doors.

V6 leaves Stair V16 at native scale. Every walk, turn, bridge and reach frame
between the departure and arrival doors uses one constant 0.943× circulation
scale, matching the walk pose's opaque mass to the native stair mount. Normal
room scale changes only while the Keeper is fully hidden behind the departure
door and resets only after he is fully hidden at the arrival door. There are no
visible scale changes anywhere in the door-to-door route.

Frank approved exact Stair Transition V6 on 16 October 2026. The immutable
approval record is
`docs/review/keeper-prime-stair-transitions-v6-approval-2026-10-16.json`;
approval changes no Final, runtime or production pixels.

The original reversible ladder gate is
`/keeper-review/keeper-prime-ladder-transitions-v1/`. It derives seven smooth
rear-view cells from the approved back master: first-rung mount, asymmetric
contact and passing poses, their exact mirrors, a rightward top transfer and a
flat-footed landing completion. The route uses eight 7.5-lp rung intervals per
60-lp storey, four complete alternating gait cycles, an exact 84-lp/eight-step
door-to-ladder walk, uninterrupted continuation above the landing, and a
matching dismount/turn/walk-to-door sequence. All visible circulation frames
use the approved V6 0.943057 scale; room-scale reconciliation remains hidden
behind doors. The legacy ladder strip is comparison provenance only.

Live review found the V1 motion generally sound but exposed ladder colour
showing through semi-transparent Keeper paint. Frank also requested a faster
turn and substantially slower climb while accepting the small hand/foot-to-rung
mismatch at game scale. V2's rectangular central-rung occluder is rejected: it
made rung segments disappear at each step. V3 restored the complete ladder but
is also rejected presentation provenance because its binary alpha edges and
per-frame DOM reconstruction flickered through the full route. The active V4
gate at `/keeper-review/keeper-prime-ladder-transitions-v4/` keeps every ladder
pixel, raises only solid Keeper paint (source alpha ≥240) to 255, preserves the
original antialiased fringe and mounts all decoded frame images before
playback. Frame changes are atomic visibility switches; the Keeper and scene
DOM are never rebuilt during playback. V2's 50-ms turns and 150-ms climb phases
remain exact, as do all roots, geometry and rung contacts. V1/V2/V3 remain
immutable. The V4 candidate changed no Final, runtime or production asset.

Frank approved exact V4 on 16 October 2026. The immutable approval record is
`docs/review/keeper-prime-ladder-transitions-v4-approval-2026-10-16.json`.
The 29 frame hashes, complete-ladder layering, persistent compositor, roots,
geometry and route choreography are approved. The current 50-ms turn frames
are not the final timing: a later timing-only pass must halve them to 25 ms
(40 fps), without changing artwork or geometry. Approval itself changes no
Final, runtime or production asset.

The V5 Keeper animation is approved. The immutable partial approval record is
`docs/review/keeper-prime-ladder-transitions-v5-animation-approval-2026-10-16.json`:
all 111 Keeper frames, roots, timing and choreography are accepted, while the
V5 perspective door presentation is explicitly rejected. Its default
route runs lower-room emergence → measured walk/stop → turn → full ladder
climb → dismount → turn → upper-hall walk/stop → right-hand reach → door opens
→ restart → complete occlusion. Frames 1–88 and all 29 Keeper assets
from approved V4 remain exact; only two already accepted stair-route door-reach
drawings are added, with V4's opacity rule. The doorway is explicitly 90° to
the straight-on dollhouse camera.

The reversible door-only V6 candidate is at
`/keeper-review/keeper-prime-ladder-transitions-v6/`. It reuses all 111
approved V5 Keeper frames byte-for-byte and replaces only the rejected door.
The new contract is a flat, constant-size 20 × 48-lp rectangular leaf with no
perspective gradient or widening; only the handle protrudes. Doors swing both
ways and always open away from the approaching Keeper. The opaque leaf itself
provides the crossing mask. The scenery controller closes it automatically
only after the Keeper has fully cleared the doorway, so closing requires no
costume-specific Keeper frames. The rule is pinned in
`docs/review/keeper-two-way-door-contract-2026-10-16.json`. V6 awaits door-only
visual approval and changes no Final, runtime or production art.

This means a complete upward room-to-room flow is now reviewable for both
stairs (approved Stair Transition V6) and ladder (approved V5 Keeper motion;
V6 door presentation awaiting review). Stair Descent V1 is retained as rejected
provenance: reversing and mirroring the ascent made the visible left leg remain
airborne while the right repeatedly took each step. Frank approved its
replacement Stair Descent V2 at
`/keeper-review/keeper-prime-stair-descent-v2/`, accepting the slight visible
overstride. V2 adds four descent-specific poses and repeats the explicit gait
RIGHT contact → LEFT passing → LEFT contact → RIGHT passing, giving exactly
seven contacts per leg over the unchanged 14-riser flight. The remaining core
transition families are: the six-view seated endpoint gate and subsequent
stand↔sit joins; downward ladder travel and dismount/exit; complete Prime lift
call/enter and lift-exit/walk routes; and any asymmetric left/right door or
interaction reach that cannot be certified as a safe mirror.
The shared open-door room emergence/return handoff also needs a deterministic
route, but reuses standard walking and occlusion rather than new costume art.

The staircase construction geometry is stored independently at
`art/drafts/keeper-staircase-geometry-2026-10-16-v1/`. Its JSON is the source
of truth for the 14-riser, 7-lp-tread, 98 × 60-lp flight and 105-lp reserved
core; the accompanying SVG preserves the plain test staircase. Future rail,
balustrade and newel artwork must conform to it rather than resizing the flight.

## Run it
```
npm install
npm run dev      # Next.js 14; open http://localhost:3000 (or this computer’s address on the same wifi, for the iPad)
npm test         # full verification suite
npm run upgrades # copy data/upgrades.csv (the upgrade list) into the game
npm run build    # production build
npm run sprites  # snap Codex's PNGs in art/raw/ into public/sprites/ (docs/CODEX_ASSETS.md)
npm run keeper-contract # rebuild neutral stills, bridges and the endpoint audit
npm run archive:keeper-review # deduplicate new review media before committing
npm run verify:keeper-prime-stair-transitions-v1 # exact frames, gutters, roots, joins and review-page contract
npm run verify:keeper-prime-stair-transitions-v2 # focused walk-to-stair seam and unchanged-source checks
npm run verify:keeper-prime-stair-transitions-v3 # fixed reviewer layout and default Studio 4× presentation
npm run verify:keeper-prime-stair-transitions-v4 # uniform root-anchored stair-family height registration
npm run verify:keeper-prime-stair-transitions-v5 # whole-silhouette stair-family scale registration
npm run verify:keeper-prime-stair-transitions-v6 # door-hidden room/circulation scale handoff
npm run verify:keeper-prime-ladder-transitions-v1 # measured alternating ladder, approach, continuation and dismount
npm run verify:keeper-prime-ladder-transitions-v2 # V1-exact art with corrected rung layering and tuned turn/climb cadence
npm run verify:keeper-prime-ladder-transitions-v3 # complete ladder plus alpha-opaque Keeper frames
npm run verify:keeper-prime-ladder-transitions-v4 # smooth opaque paint plus persistent no-rebuild playback
npm run verify:keeper-prime-ladder-transitions-v4-approval # exact V4 approval plus deferred 2× turn timing
node --import ./scripts/review_archive_fs_hook.mjs scripts/verify_keeper_prime_ladder_transitions_v6.ts # approved V5 Keeper motion plus flat two-way door-only candidate
npm run verify:keeper-prime-ladder-transitions-v5 # complete room-to-room ladder flow and side-on outward-door occlusion
```
On an iPad: open the address in Safari, Share, Add to Home Screen for full screen.

The keeper animation reviewer is online only at
`https://lighthouse-keeper-mu.vercel.app/keeper-review/`. Use **Hand back to
Codex** whenever a batch is ready: its
confirmation explains that it will first save any edited cards locally, then
sends the complete exact-name review register to the durable handoff queue. The
queue records an authoritative exact-name delta, so a later Codex task reviews
only animation decisions or notes changed since the previous hand-back (or the
shipped saved-review baseline for the first server hand-back); the receipt
reports that count on-screen—no JSON download is needed. The collapsed
Advanced backup/import control remains only for exceptional browser recovery.
When Codex claims a queued batch to make amendments, the online reviewer polls
that server state and becomes read-only until the amended delivery is marked
complete. Playback and inspection remain available, but no review decisions can
diverge while work is in progress. The repository’s generated audit page is not
a second review workspace: opening it outside the deployed route sends the
viewer to the online reviewer, keeping saved feedback and the work lock in one
place.

The separate Keeper Animation Workbench is at
`https://lighthouse-keeper-mu.vercel.app/animation-workbench`. It has immutable
**Final** and browser-editable/exportable **Draft** lanes for frame sequencing,
whole-animation and section looping, and complete transition previews. Both
lanes are currently empty by explicit decision: the earlier V1/V2 routes are
rejected provenance, not active candidates. Frank permanently approved the
smooth, single-band Prime Master V1 on 13 October 2026 with “Approved. Make sure
this is NEVER forgotten.” The V2 back copies all 81,920 approved-front alpha
values, but its boots were later found to face the player and the image is now
rejected provenance. The approved V5 rear endpoint is at
`/keeper-review/keeper-prime-orthographic-v5/`; it records Frank's selected
smooth first rear-boot render without regeneration, changes only rows 273–315,
and keeps the complete front/back alpha match. Its 1122 × 1402 source is the
rendering-quality master; the 256 × 320 orthographic image is only its
anti-aliased registration proxy. The historical V3 side remains blocked at 5
of 15 hard internal datums. Its replacement is the new reversible
`/keeper-review/keeper-prime-side-right-rigged-v1/` candidate: a smooth
1122 × 1402 master uniformly registered into a 256 × 320 proxy with exact
zero-delta evidence at all 15 datums. Frank approved it on 13 October 2026 with
“Approve side-right V1 and build Turn V1.” The immutable approval record is at
`/keeper-review/keeper-prime-side-right-rigged-v2/`. It is an artwork authority,
not a production promotion.

The separate Keeper Timing Lab is at `/keeper-timing-lab`. It keeps approved
frame bytes, frame order, root motion and endpoint contracts locked while walk,
deceleration, neutral beats, turns and endpoint holds remain independently
tunable. Frank approved **Fast Timing V1** for brisk movement between
activities: walk 10 fps, deceleration 12 fps, no neutral pause, turn 16 fps and
a 625 ms endpoint hold. It applies to locomotion, stopping bridges and turns
only; action animations retain independent timing so their entertaining
performance can be savoured. The lab supports synchronized A/B playback, large
and exact game-scale views, section loops, frame stepping, repository-backed
approved defaults, device-local personal proposals and JSON export. Timing
approval is separate from artwork, Final and production approval.

Frank approved KP Rig V1 on 13 October 2026 with “Approve KP Rig V1, let's see
it animated”. The immutable measurement pack remains at
`/keeper-review/keeper-prime-rig-v1/`; it defines 24 front/back bones, 24 side
projection bones, fixed bilateral limb lengths, body-volume envelopes and all
15 target y-datums. After reviewing Motion V2, Frank requested more leg
movement, more steps and a slower walk while judging the rest very good. The
separate V3 construction-motion revision is at
`/keeper-review/keeper-prime-rig-v3/`: its walk now uses eight steps over five
seconds instead of two steps over two seconds, with greater thigh swing and
knee lift. Idle, reach and planted-ankle sit/stand are unchanged from V2. Frank
approved Motion V3 on 13 October 2026 with “Approved, very good indeed”. That
approval authorized the now-approved smooth 15/15 side-right artwork. The
separate eight-pose Turn V1 at
`/keeper-review/keeper-prime-turn-front-side-v1/` joins the exact approved front
and side endpoints. Frank approved it with “it is ever so slightly jumpy at
about 45deg in the turn but I am happy”; the slight 45° cadence change is an
accepted recorded limitation, not an unmentioned perfection claim. The
side-right ↔ back Turn V1 remains reversible provenance at
`/keeper-review/keeper-prime-turn-side-back-v1/`. During review Frank identified
that its exact approved rear endpoint made the jumper darken visibly at F8. V2
corrected the jumper alone and remains reversible provenance. Frank then
identified the same discontinuity in the cap, trousers and boots and established
that every standard-uniform animation must use a consistent outfit palette. V3
corrected all six registered F8 outfit components but exposed a remaining boot-
construction jump at F7 → F8. V4 keeps F1–F7 byte-identical to V3, keeps F8
exact above y=250 and redraws only the rear-facing boots below that boundary.
Frank approved that exact turn on 13 October 2026 with “Approved.” The immutable
V5 approval and enhanced review page at
`/keeper-review/keeper-prime-turn-side-back-v5/` pins V4 and shows synchronized
large and 128 × 160 proposed game-size views with previous/next frame controls.
That scale review exposed three remaining issues: F1's trousers/boots were too
dark, F7 was slightly too tall and F8 used a visibly coarse registered proxy.
The separate V6 candidate at
`/keeper-review/keeper-prime-turn-side-back-v6/` changes only those points: a
masked lower-uniform palette correction in F1, a floor-anchored two-pixel
height reduction in F7, and a fresh uniform Lanczos registration of the already
approved 1122 × 1402 smooth rear master for F8. F2–F6 remain byte-identical.
V6 review then exposed pale F8 trouser patches caused by a four-row overlap
between the trouser and boot colour masks, plus a lower-leg silhouette roughly
five percent narrower than the approved V4 endpoint. The separate V7 candidate
at `/keeper-review/keeper-prime-turn-side-back-v7/` keeps F1–F7 byte-identical
to V6 and corrects only F8: disjoint colour masks remove the double correction,
and a source-resolution Lanczos registration broadens the lower legs to the V4
bounds while retaining the same floor and overall frame bounds. The new V8
cadence trial at `/keeper-review/keeper-prime-turn-side-back-v8/` retained all
eight V7 poses and inserted eight drawings at 16 fps, but Frank found it
significantly jerkier; V8 is rejected provenance and disproves any automatic
rule that more frames make motion smoother. V9 at
`/keeper-review/keeper-prime-turn-side-back-v9/` returns directly to V7, retains
all eight V7 frames byte-for-byte and inserts only one controlled 172.5° pose
between 165° and 180°. It runs nine poses at 9 fps over the same one-second
duration, with the intermediate fixed at 297 pixels high between the 296- and
298-pixel endpoints on floor y=316. Frank approved exact V9 on 13 October 2026
with “approved”. The immutable V10 approval record at
`/keeper-review/keeper-prime-turn-side-back-v10/` pins all nine frames, both
strips, 9 fps timing, midpoint source and V8 rejection. V5–V9 and all earlier
versions remain unchanged provenance.
Neither turn has entered workbench Final or production.
The game engine will extend only the
walk from world placement, beginning the cycle while the Keeper is still hidden
behind the departure door. The workbench does not share data with the existing
reviewer and cannot promote art into production; see
`docs/KEEPER_ANIMATION_WORKBENCH.md`.

The four-hour review hand-back monitor is deliberately outside Codex: the
per-user macOS `launchd` job installed by
`scripts/install_keeper_review_handoff_monitor.sh` reads only the public queue
and shows a native notification only for a new batch with a non-zero semantic
change count. It keeps its own local “already notified” list under Application
Support and never edits review data or sprite assets. The older Codex heartbeat
must remain paused to avoid duplicate alerts.

## Current implementation

- Floors 1–3 are modular fixed-width components in `src/ui/floors.tsx`: kitchen, living room, and bedroom with en suite. The first production Pixel batch now supplies the red/white shell bands and those three 105 × 35 room plates; interactive furniture remains separate. The toilet and wash basin are both in the en suite.
- Future standard floors are intentionally non-linear: kitchen anchors the base, lamp room stays topmost, bedroom stays directly below it, and each other floor receives a one-time random saved middle position. Concept-art taper is decorative and never fixes room width or unlock order.
- Missions run side by side, so floors arrive in any order; a finished floor appears the next morning in a random middle place that the save keeps (kitchen at the bottom, bedroom under the lamp room).
- Every object renderer accepts `standard`, `on`, and `broken`; active gameplay drives `on`. Broken objects share integer-step casing wobble, smoke and sparks. Add `?broken=tv,cooker` (or `?broken=all`) to the URL for the internal art-state preview.
- Objects can be upgraded with credits from their tap menu. The tier list is `data/upgrades.csv`; the living-room armchair now progresses from basic armchair to rocking chair to Lazyboy-style recliner, always on the same 11 px seat datum. Higher tiers do more good, faster; the bed's tier sets the morning's energy. Grown-ups set upgrade prices (overall %, then per tier) and can gift upgrades. Tier sprites are `obj_<id>_t<n>_<state>`; until they exist a `T<n>` tag stands in. `?tiers=3` previews top tiers.
- The recipe studio (`/studio`, linked from Grown-ups) is the design tool for how each activity plays. It covers walks, doors and hidden costume changes, clips, timing, sounds (drop audio files onto placeholders, then trim and set volume) and solid-object checks against each frame's real pixels. Format and workflow: `docs/RECIPES.md`.
- Grown-ups can change any animation's speed while playing (Grown-ups → Animation speeds): search the animated sprites, watch one in a preview, and step its fps from 1 to 20 in halves. One setting for the whole game, saved with the PIN (database `settings`, else the browser), is applied live. The sprite sheets' metadata remains authoritative: a tweak only lasts while its sheet keeps the speed it was made against, and "Copy for the metadata" gives `{ "animationFps": { … } }` to write back into the sheets.
- Keeper-owned assets can now break during play, block their normal actions, and be repaired. Grown-ups control average fault frequency and maximum concurrent faults; defaults are off / one. Breakdown events expose placeholder SFX categories for later audio. The shop is excluded because it is not the keeper's asset.
- The reviewed production keeper batch remains 191 aligned exports: 173 animation sheets (1,479 frames) plus 18 technical component/reference sheets. The visually rejected second-round production pass was rolled back as a unit to commit `131191c`; that history and Frank's immutable comments remain intact. Separately, Frank explicitly selected nine named source replacements on 10 October, plus the dependent `keeper_parachute_landing` bridge; these ten exact-name clips are now canonical after final-strip inspection, while their previous canonical strips stay visible in the reviewer. The neutral contract adds deterministic derived stills and bridges without changing the 173-sheet review denominator; the current raw contract contains 325 keeper sheets and publishes 339 total pictures including room/effect art. Every full-body sheet has registered `startPose` / `endPose`, walk sounds are authored once as zero-based `sfxCues`, and `npm test` rejects new or regressed endpoint failures. The exact-pixel migration audit is `docs/KEEPER_NEUTRAL_ENDPOINT_AUDIT.md`; 300 legacy endpoints remain an explicit, costume-ordered bridge/frame repair queue rather than being silently treated as exact.
- Every sprite-sheet workflow must keep each frame's character, props, effects and projectiles wholly inside its declared cell, with a transparent safety gutter at shared edges. The side-on beard audit now classifies every manifest frame and inventories 163 standing/sitting side-on sheets. `keeper_clear_snow` is SHA-256-pinned as the canonical fuller stepped beard. An eligible, landmark-aligned beard-mask comparison passes with a symmetric silhouette difference of at most one logical pixel; 994 different-pose frames remain non-comparable until approved beard masks, facial landmarks and depth/component ownership evidence exist. No beard correction is justified or promoted.
- `data/keeper_side_on_beard_occlusion_audit.json` and `scripts/verify_side_on_beard_occlusion.ts` provide the reproducible evidence audit, source hashes, classifications and gutter evidence. Historical v1 and v2 Darts draft files are preserved but are non-promotable evidence only; the v2 colour-predicate edit is not a confirmed fix.
- The immutable 11 October review-platform handoff contains an 81-name amendment delta. Forty-one exact names have new side/rear, timing or object-action candidates available as reversible drafts; `keeper_carry_shopping` and `keeper_play_drums_back` also have second variants from the 12 October annotated review, respectively correcting frames-1/7 bag continuity with a synchronized loop endpoint and frame-6 hands crossed behind the back. `keeper_party_hat_put_on_back` retains v2 and v3 frame-2 comparisons; v3 keeps both connected arms in the front/near plane, clear of the head, while lifting the hat toward frame 3. `keeper_put_record` likewise has retained v2 masked-removal and v3 horizontal-held-record comparisons. Thirteen newly rendered face-to-camera candidates were withdrawn on 12 October: twelve remain as rejected provenance, while the complete `keeper_count_money` amendment was explicitly deleted and the previous canonical version retained. Canonical production sprites remain unchanged pending explicit per-candidate promotion. The reviewer carries an exact-name Codex response for all 81 rows, including iterative requests for seated fishing, shower privacy/exit and the helter-skelter-dependent slide.
- Frank approved the V1 full-face canon pack on 12 October 2026, then selected exact V2 right-turn F6 / ingress F19 as **Keeper Prime (KP)** identity evidence. Running previews exposed that its coarse raster itself caused pixel-density and model jumps. He therefore reset every animation: Final and active Draft are both empty, and all V1/V2 routes are provenance only. `keeper-prime-master-2026-10-12-v1` is now the permanently approved identity: a smooth density-8 neutral based on Frank's preferred first render, with one broad pale jumper band rather than the harder-to-maintain double stripe. Orthographic V2 achieved an exact front/back alpha match but is rejected because its rear boots still faced the player. Orthographic V3 records why the historical side failed 10 of 15 internal points. Frank explicitly approved the first smooth rear-boot render for Orthographic V5 on 13 October; V5 pins that exact 1122 × 1402 source, integrates only rows 273–315, and retains zero alpha mismatch. The smooth rigged Side-right V1 is the approved 15/15 side authority. The eight-pose front ↔ side turn is approved with one recorded minor 45° cadence limitation. Exact side ↔ back V4 is preserved through its V5 approval record; V6 records the first scale-review refinement, V7 corrects the F8 lower legs, V8's global cadence increase is rejected, and exact V9 is the approved nine-frame authority pinned by V10. Orthographic V4's rougher, over-squared alternative is historical provenance. Every approved model must retain super-smooth outer contours and internal linework at master resolution; geometry alone cannot approve art. No production sprite or manifest has changed.
- Frank approved exact Keeper Prime Walk V6 on 14 October 2026; the artwork-free V7 approval record pins its eight frames, strip and 8 fps timing at `/keeper-review/keeper-prime-walk-v7/`. He then approved exact stop → walk → stop V1; its artwork-free V2 approval record is at `/keeper-review/keeper-prime-stop-walk-stop-v2/`. The route joins the exact approved Side-right neutral to exact Walk V6 F1 through three registered bridge poses, reuses those poses byte-reversed on stopping, begins root motion on the first gait frame, and returns to the byte-identical neutral. Deterministic checks pin both authorities, cell gutters, 5-frame strips and sidecars, the 32-frame/412-pixel displacement schedule, zero walking-on-the-spot frames and all public assets. It is now a core transition authority, but the left mirror, workbench Final and production remain unchanged.
- Frank judged walk → stop → turn to camera V1 excellent and approved Fast Timing V1 on 14 October 2026. Its artwork remains exact at `/keeper-review/keeper-prime-walk-stop-turn-front-v1/`; the timing authority is reviewed at `/keeper-timing-lab` and pinned in `art/drafts/keeper-fast-transition-timing-2026-10-14-v1/`. The 32-frame route now previews in approximately 2.996 seconds with the approved 10/12/16 fps transition cadence and zero neutral pause. Root motion and exact endpoints remain unchanged. Action timing is explicitly excluded. The route remains outside Final and production.
- Frank approved walk → stop → turn fully away V2 on 14 October 2026 with “good now working fine. approved.” Its Keeper artwork, Fast Timing V1 schedule, 32-frame route, 374-pixel travel, zero turn root motion and exact rear endpoint remain byte-identical to V1. V2 changes delivery only: fresh versioned asset paths preload and decode every moving frame before playback, eliminating the blank/stale-frame flicker exposed in V1. The approval-only V3 record pins that exact route in `art/drafts/keeper-prime-walk-stop-turn-back-2026-10-14-v3/`. It is a core transition authority but remains outside Final and production; V1 is unchanged historical provenance.
- The movement-foundation V2 presentation correction adds two non-promotable review gates while preserving V1 unchanged. `/keeper-review/keeper-root-motion-gate-v2/` uses the same five archived, byte-identical approved neutral/bridge/Walk-F1 images to explain the current 76-ku root schedule versus Claude's proposed 84-ku schedule in plain English. `/keeper-review/keeper-vertical-circulation-v2/` is deterministic construction motion—not finished Keeper art—for stairs continue/exit from both landing parities, ladder continue/dismount-to-walk, and lift entry/exit. Its proposed vertical module is 60 lp floor-to-floor (56 clear + 4 shared deck); the stair is 16 × 3.75 lp rise and 16 × 5.25 lp run inside a separate 105-lp core. The 4× pane is an authoring ruler; runtime screen scale is responsive. Nothing has entered Final, production or runtime.
- The separate `/keeper-review/keeper-object-approach-oven-v1/` context gate applies the candidate root schedule to a complete three-interval approach: 42-ku acceleration, one exact eight-frame Walk V6 cycle, 42-ku deceleration, a fixed-root approved Turn V9 and its exact rear endpoint. A solid 30 × 30 lp oven proxy is centred on the 120-lp interaction anchor in a 172 × 56 lp room. The page reuses 20 archived approved frame URLs, preloads them before playback and can switch to the current 244-ku route, which finishes exactly 1 lp short. This remains an unapproved, reversible layout/root-motion review; the oven proxy is not art.
- Oven Approach V7 (`/keeper-review/keeper-object-approach-oven-v7/`) preserves the exact Keeper route and records the former calculated-depth experiment. Its 42-lp notional depth, 4% room convergence, 1% furnishing convergence and raised 30-lp proxy are now historical evidence only. Kitchen and standard-room authoring instead follows `flat-cutaway-v1`: constant Keeper/asset scale, parallel geometry, no vanishing point or runtime depth scaling, a 5-lp floor cue and the real object/contact dimensions. V3–V7 remain immutable unapproved placement provenance.
- The separate `/keeper-review/keeper-lift-entry-alignment-v1/` construction gate corrects the V2 lift path without altering the immutable V2 page. Door centre x=126 lp to lift centre x=42 lp is 84 lp: eight grid steps/four full strides. The Keeper remains on x=42 while stopped, pressing the button with his right hand, turning away and entering in depth; the doors close only after occlusion. The even-step route explicitly remains blocked on separately reviewed Walk F5-to-neutral stop art. No runtime geometry or approved pixels changed.
- The active `/keeper-review/keeper-circulation-entry-alignment-v1/` shared-core construction gate refines the preliminary lift-only geometry and adds the walk-to-stair join. One transfer-door root at x=115.5 lp serves both alternatives. The stair base stays at its measured x=94.5 lp, exactly one 21-lp/eight-frame walk cycle away; the last walk frame is followed by an already-advancing climb frame with zero pause frames. The lift centre is x=31.5 lp, exactly 84 lp/four full strides from the same door, and retains the fixed-root right-hand-button choreography. Final lift stopping still needs F5 bridge art; no runtime or approval state changed.
- Frank's original 14-pose darts source remains a separate byte-identical `keeper-darts-user-selected-2026-10-10-v1` visual comparison. The reviewer shows it beside canonical and explicitly marks the beard audit evidence gate; it is not a beard reference. `data/keeper_review_drafts.json` also records the ten selected canonical promotions, each with SHA-256-pinned prior-version evidence, seven active V11 artist-smock comparisons, and one active `keeper_snooker` complete-route comparison. V11 covers the full 15-asset family, while its eight neutral/bridge derivatives remain technical assets outside the 173-animation gallery. The accepted snooker route retains the canonical standard-uniform Keeper from walk through stop, cue acquisition, two strokes, release, turn and departure; production artist and snooker sprites remain unchanged pending review.
- Multi-frame keeper animations use 4fps by default. Frank's accepted timing changes are explicit `KEEPER_FPS_OVERRIDES` values from 1fps to 10.5fps, written to each clip's source JSON sidecar and regenerated into the runtime manifest without changing sprite pixels. The shared sprite renderer reads each manifest FPS independently, and the keeper review page can preview, save and export a later 1–20fps proposal for every action.
- Sprite manifest entries may be old string paths or metadata objects with frames, fps and optional loop/mirror/reverse/interaction-point contracts. Horizontal strips animate without CSS scaling or rotation.
- All SVG object targets work by touch, mouse, Enter and Space. At a 1024 × 768 iPad viewport, the first-three-floor targets were verified at a minimum 82 × 94 CSS px.

## Where things are

- `src/game/` — rules (`config.ts` has every number, `commands.ts` the command book and silly reactions, `engine.ts` the rules).
- `src/ui/floors.tsx` — fixed-width room definitions and the reserved diving geometry, which follows the bedroom.
- `src/ui/art.tsx` and `src/ui/Sprite.tsx` — vector fallbacks, the three-state renderer, and production strip playback.
- `public/sprites/` — production room, TV/effect and keeper review PNGs plus their runtime manifest.
- `art/source/keeper-first-batch/` — the generated keeper turnaround, deterministic density-4 authoring script, contact sheet and provenance notes.
- `art/source/first-production-batch/` — untouched generated sources and prompt/provenance notes; `scripts/build_first_asset_batch.py` rebuilds the exact `art/raw/` deliveries, then `npm run sprites` publishes them.
- `docs/PRODUCTION_ASSET_KIT.md` — exact Pixel filenames, dimensions, anchors, pivots, z-order, frame counts, fps, and delivery order.
- `docs/KEEPER_ANIMATIONS.md` — plain-English animation index, direction rules and object-alignment instructions.
- `docs/KEEPER_ANIMATION_WORKBENCH.md`, `data/keeper_animation_workbench.json` and `src/animation-workbench/` — the separate Draft/Final framework for non-destructive frame editing, section loops and complete transition previews. Its editor remains implemented and the library remains intentionally empty until the approved core turns are assembled into complete transition routes. Front ↔ side Turn V1 is approved with one accepted minor 45° cadence limitation. Exact nine-frame side ↔ back V9 is approved and pinned by V10; V8's 16-frame cadence trial remains rejected as jerkier. Only world-distance walking will vary in runtime, beginning hidden behind the departure door; production remains unchanged.
- `docs/CODEX_TO_CLAUDE_HANDOFF_2026-10-14.md` — current cross-agent handoff: public review links, exact Keeper Prime approval boundaries, next core-animation gates and a bounded furniture-placement/phase-aware-locomotion architecture task for Claude.
- `docs/CODEX_TO_CLAUDE_VERTICAL_CIRCULATION_2026-10-14.md`, `art/drafts/keeper-movement-foundation-2026-10-14-v1/` and `scripts/verify_keeper_movement_foundation_v1.ts` — the reversible 84-ku root gate and measured 60-lp stair/ladder/lift construction proposal, with exact authority hashes and no runtime promotion.
- `src/keeper-timing-lab/`, `data/keeper_timing_policy.json`, the immutable `public/keeper-timing-lab/catalog.json` V1 history, current `public/keeper-timing-lab/catalog-v2.json`, and `art/drafts/keeper-fast-transition-timing-2026-10-14-v1/` — the phase-specific timing platform and approved Fast Timing V1 transition record. Artwork hashes remain locked; the repository supplies the project transition default while personal alternatives can still be compared, looped, saved locally and exported. The policy explicitly prevents action animations from inheriting transition timing.
- `docs/KEEPER_ANIMATION_HANDOFF.md` — complete keeper review checkpoint, correction history, exact transition-gap inventory, object-binding design and ready-to-paste next-task prompt.
- `docs/KEEPER_ARTWORK_AUTHORING_AND_REVIEW_PLAYBOOK.md` — proven Keeper artwork recipe, continuity rules, rejected methods, accepted artist/snooker case studies, evidence checklist and exact-name review workflow.
- `docs/KEEPER_FULL_FACE_INVENTORY.md`, `data/keeper_full_face_inventory.json` and `art/drafts/keeper-full-face-canon-pack-2026-10-12-v1/` — the complete read-only front-facing inventory and approved, reversible full-face canon pack. The first two unpromoted V2 redraws are isolated in `art/drafts/keeper-full-face-standard-turn-redraw-2026-10-12-v2/`; their rejected V1 predecessor remains historical and unmodified.
- `scripts/keeper_review_handoff_monitor.py` and `scripts/install_keeper_review_handoff_monitor.sh` — independent macOS notification monitor and its per-user `launchd` installer; it reads the hand-back queue every four hours without opening Codex.
- `docs/prompts/KEEPER_SIDE_ON_BEARD_OCCLUSION_AUDIT.md` — first-stage ready-to-paste audit/fix prompt for beard, hand and arm layer order across every side-on standing and sitting animation.
- `docs/prompts/KEEPER_SPRITE_FRAME_ISOLATION_AUDIT.md` — second-stage ready-to-paste exhaustive audit/fix prompt for frame overlap and future enforcement.
- `docs/prompts/KEEPER_POST_AUDIT_REVIEW_DELTA.md` — ready-to-paste exact-name, JSON-ingestion prompt for Frank's next review after all three audits.
- `docs/prompts/KEEPER_RELEASE_SURFACE_DATUM_AUDIT.md` — third-stage ready-to-paste audit prompt for consistent tabletop release height and prop hand-off.
- `docs/prompts/KEEPER_REVIEW_WORKBENCH_BUILD.md` — ready-to-paste separate build prompt for the project-specific next stage of the reviewer: rooms, furniture, annotations, crop proposals, routines, triggers and context preview, with later generic productisation deliberately deferred.
- `docs/KEEPER_ASSET_SCALE.md` — human-readable keeper measurements and the rules for sizing/placing objects.
- `data/keeper_asset_contract.json` — authoritative machine-readable scale, pivots and interaction points.
- `data/keeper_pose_registry.json`, `data/keeper_endpoint_audit.json` and `data/keeper_endpoint_exceptions.json` — shared pose vocabulary, current real-pixel endpoint evidence, and the frozen legacy migration boundary.
- `data/keeper_object_dimensions.json` and `docs/KEEPER_OBJECT_DIMENSIONS.md` — keeper-derived furniture, fixture and station dimensions.
- `public/keeper-review/index.html` — canonical online-only reviewer deployed at `/keeper-review/`; `docs/keeper-scale-audit/review.html` is the generated audit artifact and must be byte-identical, but when opened outside `/keeper-review` it sends the viewer to the live platform instead of presenting a second workspace. Its gallery is a compact visual scan (name, review state, last local save/redraft, playback and frame stepping); `Open close review` opens any chosen card immediately. `Find animation` searches names and overrides all other filters; otherwise independently filter by review state, pose and active/reserve use list. Close review lets Frank override the inferred pose tag, relegate a likely duplicate to the reversible reserve list, expand/compress retained draft comparisons, and select canonical or every exact-name draft as an exportable preferred-promotion candidate—without mutating production. **Hand back to Codex** always asks for confirmation, saves any unsaved cards to that browser if confirmed, then submits the full batch to the durable server-side queue. The server records a semantic exact-name delta (ignoring save timestamps), comparing the first server hand-back to the shipped review baseline and later ones to the prior hand-back; the receipt reports only the changed animation count for later Codex work. When Codex claims a batch, the online reviewer becomes read-only until the delivery is completed, while retaining playback and inspection; JSON backup/import is collapsed as an exceptional browser-recovery option.
- `review-archive/`, `docs/REVIEW_ARCHIVE.md` and `scripts/archive_keeper_review_media.mjs` — content-addressed storage for review-only images and GIFs. All 748 review paths resolve through 54 set manifests to 327 unique SHA-256 objects hosted outside Vercel deployments. Immutable page bytes and old URLs remain preserved; short-lived redirects keep the media host replaceable, and new animations preload every moving frame before playback. `public/` is 43.62 MiB instead of roughly 115 MiB.
- `data/keeper_side_on_beard_occlusion_audit.json`, `art/drafts/keeper-side-on-beard-occlusion-2026-10-10-v2/`, and `art/drafts/keeper-side-on-beard-occlusion-2026-10-10-v1/` — completed draft-only v2 beard/hand audit and preserved rejected v1 history. The active reviewer shows v2 beside canonical and the separate Frank-selected darts draft; the verifier prevents implicit promotion.
- `data/keeper_review_drafts.json` and `art/drafts/` — SHA-256-pinned, exact-name review comparisons: the draft-only darts candidate, seven active V11 artist-smock candidates, the accepted complete-route `keeper_snooker` candidate, the 41 exact-name 11 October amendment candidates and the separate party-hat frame-2 v2 variant, plus the ten selected canonical promotions and their reversible previous versions. Hash-addressed reviewer copies prevent same-name historical and current variants from overwriting one another. `scripts/verify_keeper_review_drafts.ts` checks every registered source, canonical/current comparison, sidecar, gutter, publication and reviewer attachment.
- `docs/keeper-scale-audit/` — all-sheet/all-frame metrics, CSV register and nine printable contact sheets; rebuild every output, including the viewer, with the bundled Python runtime and `scripts/audit_keeper_scale.py`.
- `docs/DOORS_STAIRS_AND_COSTUMES.md` — agreed stairway, door and costume-change rules, seamless clip joins, and the decisions still to make.
- `docs/BACKGROUND_ELEMENTS.md` — Codex's brief for every background layer, sunrise and sunset, night lighting, and the every-asset-can-be-upgraded rule for objects.
- `docs/AMBIENCE_AND_BACKDROP.md` — backdrop layers, weather overlays, ambient sound, the lamp's start-up, audio file specs and the decisions still to make.
- `docs/CLAUDE_WORKBENCH_NOTES.md` — Claude's plan of approach for the shared review workbench (the next major build).
- `docs/RECIPES.md` — the recipe format, the recipe studio and what each animation sheet needs for it.
- `docs/EXPANSION_DESIGN.md` — living write-up of agreed room ideas, random floor placement, night reveals, weather, transport, island expansions and energy systems.
- `art/manifest.json` and `art/asset_inventory.json` — facts about the concept/prototype image pack; these are not a production rig.

## Stack
Next.js 14 (App Router), React 18, TypeScript, Vitest. Neon Postgres (optional; falls back to browser localStorage). Deploy on Vercel; set `DATABASE_URL` (pooled) for Production. Pushes do not deploy: release with `npm run deploy` (see `docs/DEPLOYMENT.md`). Review media is served from the content-addressed Git archive described in `docs/REVIEW_ARCHIVE.md`, not copied into every deployment.

## Players and the database
A "Who is playing?" screen lets each child have their own game and their own grown-ups' dials (allowance, prices, quiz difficulty). With `DATABASE_URL` set (Neon via Vercel's Storage tab) saves live in Postgres and follow the player to any device; the tables are created automatically on first use. With no `DATABASE_URL` everything stays in the browser. Grown-ups' PIN starts as 1234 (Menu, then Grown-ups), and is checked on the server when the database is on.


## More

`docs/STATUS.md` is the full write-up. `docs/CODEX_BRIEF.md` is the authoritative art brief. `HANDOFF_TO_CLAUDE.md` separates implemented runtime work from missing production artwork.

## Verification

Last verified on 14 October 2026 (176 tests, type-check and production build):

```sh
npm test
npm run typecheck
npm run build
```

The verification commands above cover the game and sprite pipeline; `npm test` begins with the keeper contract check. Keeper-scale verification additionally runs `scripts/audit_keeper_scale.py` and `scripts/verify_floor_asset_catalogue.py`; finished asset work is committed directly to the repository's main branch.
