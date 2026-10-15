# Notes for Codex from Claude (integration hooks)

Working split: Codex owns art, design and layout; Claude owns game logic and wiring. Ask for a code hook here or in HANDOFF_TO_CLAUDE.md.

## Claude: kitchen basic assets to draft (15 Oct 2026)

Frank wants you to draft the tier-1 kitchen furniture for the 172 × 56 room,
as the test case for snapping, moving and growing furniture. Exact scope,
sizes, states and hand-back: `docs/CLAUDE_TO_CODEX_KITCHEN_BASIC_ASSETS_2026-10-15.md`.
In short: every floor item fills whole 21-lp bays (two steps); the base
kitchen is fridge, oven, sink, cleaning cupboard, then a two-bay table at the
far end. Two things to confirm, not work around: whether the oven clips read
with a 19-lp door, and whether a one-bay cupboard door hides him. Drafts
only; approve or promote nothing.

## Codex movement-foundation response (14 Oct 2026)

Codex has built the requested root-motion Gate 1 plus a separate measured
construction lab for the remaining vertical core transitions. The clearer
presentation-corrected review pages are
`/keeper-review/keeper-root-motion-gate-v2/` and
`/keeper-review/keeper-vertical-circulation-v2/`; V1 remains immutable
historical evidence. The root comparison uses the
exact approved F1 bridge pixels twice and compares current 76-ku stop-to-stop
translation with the proposed exact 84-ku lattice translation. No F5 stop has
been drawn.

The circulation proposal distinguishes 56 lp clear room height from a shared
4 lp deck, giving a 60 lp finished-floor pitch. Its alternating stair has 16
risers × 3.75 lp and 16 advances × 5.25 lp: exactly 60 lp rise and 84 lp/eight
walking intervals of run. The resulting separate stair core is 105 lp; the old
38-lp figure was a placeholder and is unsafe to implement. The ladder uses
eight 7.5-lp rung intervals per floor; lift stops repeat at 60 lp. Continue and
room-door exit routes exist for both stair parities and the ladder, plus lift
entry and exit. Full technical handoff:
`docs/CODEX_TO_CLAUDE_VERTICAL_CIRCULATION_2026-10-14.md`.

The V2 scale wording is deliberate: 4× is the authoring coordinate ruler, not
a fixed final CSS size. The live 1200 × 760 SVG scene responsively fits the
available viewport, so the Keeper's physical on-screen size varies by device
and camera.

The first practical context gate is
`/keeper-review/keeper-object-approach-oven-v1/`. It places a deliberately
opaque 30 × 30 lp oven proxy at x=120 lp in the 172 × 56 lp room. The default
flow uses exact approved Keeper pixels with candidate-42 root motion over three
10.5-lp intervals, then the approved fixed-root Turn V9 to the exact rear
endpoint. A toggle shows the present approved root schedule finishing 1 lp
short. This is still review-only: no oven art, root motion or production state
has been approved or changed.

Oven Approach V7 is the active placement/perspective refinement at
`/keeper-review/keeper-object-approach-oven-v7/`. It preserves every V1 Keeper
frame and route value. The rear-wall oven base now sits at the wall/floor
junction 7 lp above the stage bottom, leaving a 5-lp visible floor surface
before the 2-lp front lip and the Keeper's unchanged near interaction line.
V3's 0.5-lp shared foot datum and the unshown V4 2-lp correction are retained
as historical placement evidence; V5 has exact V6 geometry but a stale datum
label in its large pane; V6's 12-lp floor was visually too deep. The proposed shared authoring projection is
a 42-lp room depth with one 10.5-lp standard asset-depth module: rear wall 96%
against the open front, and asset rear face 99% against its interaction/front
face. Keep the Keeper and object interaction plane at canonical 100% scale;
retain the 84-ku world grid and collision footprints; do not add continuous
runtime raster scaling. Full proposal:
`docs/KEEPER_ROOM_PERSPECTIVE_PROPOSAL_2026-10-14.md`. Await Frank's approval.

Everything remains a reversible draft awaiting Frank's review. Do not change
Claude's route tables, runtime geometry, Keeper art or approval records yet.

## First finished stair-ascent gate (15 Oct 2026)

`/keeper-review/keeper-prime-stair-ascent-v1/` is the first finished-art test
of the approved-walk-to-measured-stair contract. One exact approved mirrored
Walk V6 cycle moves from x=115.5 lp to x=94.5 lp; the next frame is already an
advancing climb pose, with zero stop or pause frames. The eight-pose climb
cycle closes at 84 ku horizontal and 60 ku vertical, and eight cycles close
the 16-riser flight at 672 ku run and 480 ku rise. The V1 endpoint remains in
continuous climb: upper-landing dismount/stop/walk, descent and opposite flight
parity are intentionally separate gates. It is a reversible unapproved draft;
runtime geometry, Final and production remain unchanged.

Frank rejected the V1 visual execution on 15 Oct 2026: the Keeper walked out
of the right-hand transfer door backwards relative to his leftward root motion,
and the second leg did not take a convincing alternating stair step. Keep V1
immutable as rejected provenance. The first correction attempt was the
`/keeper-review/keeper-prime-stair-ascent-v2/`. V2 horizontally mirrors the
exact approved Walk V6 frames for the approach and redraws the climb against
Walk V6's explicit F1–F4 first-leg / F5–F8 opposite-leg phase authority. It
does not change route geometry, timing, Final or production.

Frank rejected V2 after seeing it move: the visual leg roles still did not
alternate convincingly and the left boot passed below the stair surface. Keep
V2 immutable. `/keeper-review/keeper-prime-stair-ascent-v3/` is a fresh,
versioned set of
eight individually rendered and registered poses. Near advances in F1–F4; far
advances in F5–F8. Every frame has an isolated 256×320 cell, transparent edge
gutter and y=316 lowest-sole datum. Playback computes each lower support
contact from its declared tread centre/top, and the page includes frame
stepping, a two-step-only loop, an exact-logical-scale view and an optional
contact-line overlay. No prior candidate, runtime geometry, Final or
production file changed.

Frank then rejected the unmasked V3 presentation because its exposed boots
read as jumping two treads at once. Keep V3 immutable. The V4 masking test is
`/keeper-review/keeper-prime-stair-ascent-v4/`. V4 is deliberately
presentation-only: its timeline, V3 media hashes, root motion, stair geometry
and timing are unchanged, while a closed foreground stringer/bannister masks
the boots and lower shins. The mask is enabled by default and the page can turn
it off to expose the exact V3 motion. V4's 17 versioned asset aliases resolve
to the existing V3 archive objects, so no binary artwork is duplicated. Do
not promote the mask or V3 motion without Frank's explicit approval.

Frank accepted V8’s vertical registration but rejected its horizontal toe
clearance because the forward toe overlapped the next riser. Preserve V8
unchanged as rejected provenance. The active unapproved V9 diagnostic is
`/keeper-review/keeper-prime-stair-ascent-v9/`. It shifts only the complete
Keeper root +1.5 lp/right (12 source pixels). Measured forward-toe clearance is
now at least 0.25 lp/2 source pixels. The exact V8 image hashes, vertical
coordinates, support/target guide positions, 320-ms timing and stair geometry
are unchanged. V9 remains only a four-contact mechanical gate, not a complete
transition and not approved. No approved walk, Final or production file
changed.

V11 is rejected after live review. Frame 7 floats exactly one 60÷14-lp riser
above the stair, and its nominal arm shift never exceeds 0.875 logical pixels,
so the arms read as static. Its verifier's non-penetration-only rule was
insufficient and must not be copied.

The accepted geometry/contact foundation is
`/keeper-review/keeper-prime-stair-ascent-v12/`. It is intentionally a contact
and arm gate, not a finished climb. It retains fourteen equal risers over the
exact 60-lp floor pitch, increases tread depth to 7 lp and therefore makes the
flight 98 lp long inside the reserved 105-lp stair core. Four binding contacts
alternate RIGHT/LEFT/RIGHT/LEFT; every support sole must touch a real tread,
the upper sole must meet its next tread within 0.05 lp, and support handover
drift is capped at 0.07 lp. The two arm silhouettes are visibly opposite.
Frank accepted this construction on 15 Oct 2026 with “yes you've got it”. That
acceptance pins the geometry and contact drawings but does not promote an
animation to Final or runtime.

The superseded V13 follow-on is
`/keeper-review/keeper-prime-stair-ascent-v13/`. It adds exactly one raised
passing drawing per leg, giving contact → passing → opposite contact over two
frame intervals. Both contacts remain byte-identical V12 frames, both
intermediates are byte-identical V6 pose-3 frames, each planted support stays
on the same mathematical tread, and the arms pass through the neutral V6 pose
between opposite V12 counter-positions. Generated midpoint-arm studies were
rejected because they reached the next arm extreme too early; retain them as
provenance only. Frank then found the arms too extreme and not quite
synchronized with the legs, and identified F4's extended left boot entering
the stair profile before F5 landed flat.

The V14 art correction is
`/keeper-review/keeper-prime-stair-ascent-v14/`. V14 retains the same contact →
passing → contact phase order, restricts the visible near-hand endpoints to
±14.55 source pixels from vertical and keeps the far/right arm almost fully
occluded. Both passing boots are compact raised poses. Exact pixel-to-stair
testing finds zero penetrating moving-leg pixels; F4 clears the stair by 1.59
lp. Pixels outside the declared arm and moving-lower-leg masks remain exact.
Nothing is promoted or wired.

The V15 complete-flight review is
`/keeper-review/keeper-prime-stair-ascent-v15/`. V15 is timeline-only: it
reuses the four V14 candidate images byte for byte, expanding the two-step
mechanism to 27 frames over all fourteen risers. Contacts alternate
LEFT/RIGHT through treads 1–14, each passing frame remains support-locked, and
the final RIGHT contact lands at the exact 80-lp upper-floor datum. The player
stops and holds there; there is no automatic wrap to the bottom. V15 remains
unapproved and changes no Final, runtime or production asset.

The approved stair-ascent authority is
`/keeper-review/keeper-prime-stair-ascent-v16/`. V16 preserves V15's 27 frames,
root coordinates, fourteen contacts, timing and endpoint exactly. Narrow masks
balance RIGHT compact passing to the same y=270 moving-region lower edge as
LEFT while retaining 1.59-lp clearance and zero penetration; restore the exact
V6 pixels over LEFT contact's detached flesh remnant; and complete RIGHT
contact's forward-boot toecap while leaving row y=282—the contact sole—exact.
All pixels outside the three masks are unchanged. Frank accepted exact V16 on
15 October 2026 with “OK let's say that's done, had enough of refining it.”
The no-art V17 approval pack pins all four frame hashes, the 27-frame rig and
the review-page hash. Approval permits later Final preparation but performs no
runtime or production promotion.

The staircase scenery is a separate later review gate. It must have exactly two
newel posts (lower entrance and upper landing), a foreground open-side
balustrade with regularly spaced balusters and one continuous handrail. The
foreground layer should plausibly obscure parts of the boots/lower legs while
the tread/contact geometry remains the approved 14-riser, 7-lp-tread,
98-by-60-lp flight.

## Stair entry and landing-exit transition gate (15 Oct 2026)

The current review candidate is
`/keeper-review/keeper-prime-stair-transitions-v2/`. Its approved authorities
remain byte-identical: Walk V6, Stair Ascent V16, approved side/back Turn V9,
the side/front turn source retained for the opposite flight, and the approved
stop-to-walk bridge. Left travel is CSS-mirrored only. Two new masked
right-hand door-reach cells are present as unapproved candidate art.

- Lower door and upper door share x=140.5 lp; fully hidden root is x=161.5.
- The lower stair root is x=119.5, exactly 21 lp/one full visible walk cycle
  from the door. Two walk cycles are shown so the first begins while occluded.
  V1's direct mirrored Walk F8 → Stair V16 F1 join was visibly discontinuous.
  V2 retains two complete cycles and identical roots but rotates the cyclic
  order to end on compact Walk F7, then uses the exact approved LEFT compact
  passing cell as a dedicated mount before Stair V16 F1. There is no held root.
- The upper route establishes both feet on the x=14.5 landing root. Because
  travel was bottom-right → top-left, it turns clockwise side-left → back →
  side-right through approved Turn V9. The opposite flight must turn clockwise
  side-right → front → side-left. He walks and decelerates to x=130, reaches
  the x=144 handle with his right hand, opens the door, returns briefly to
  exact neutral, restarts and finishes hidden at x=161.5.
- The acceleration reuses exact approved bridge drawings with the proposed
  `candidate-42` roots 3, 7, 13, 19 ku. This root schedule is still awaiting
  Frank's visual approval and does not amend its approved source record.
- Both generated landing experiments are rejected provenance only. One changed
  the silhouette; the other faced the wrong way and had three arms. Neither is
  copied to the public review assets or present in any route.
- The later partial/full door-reach sources have exactly two arms. Only their
  declared arm-region pixels are composited over the exact approved side
  neutral; the verifier requires every out-of-mask pixel to remain identical.

The page opens on a focused nine-frame seam loop and preloads and decodes all
27 unique URLs before enabling playback. Run
`npm run verify:keeper-prime-stair-transitions-v2` to check authority hashes,
256×320 transparent cell gutters, rejected-source exclusion, exact geometry,
moving joins, hallway closure, controls and approval boundaries. Nothing is in
Final or runtime until Frank approves the candidate.

## Lift entry alignment correction (14 Oct 2026)

The focused construction review
`/keeper-review/keeper-lift-entry-alignment-v1/` supersedes only the proposed
lift choreography, not the immutable vertical-circulation V1/V2 evidence. It
places the room-door centre at x=126 lp and lift centre at x=42 lp, an exact
84-lp route of eight 10.5-lp steps/four full strides. The Keeper stops, presses
the button with his right hand, retracts, turns fully away and enters in depth
without leaving the x=42 root. Final animation remains blocked on the undrawn,
unapproved Walk F5-to-neutral stop bridge required by the even-step route.
Nothing is approved or wired into runtime.

The active refinement is now
`/keeper-review/keeper-circulation-entry-alignment-v1/`. It establishes a
shared transfer-door root at x=115.5 lp. The stair base remains at x=94.5 lp,
exactly one 21-lp/eight-frame walk cycle away; walk F8 joins an
already-advancing climb F1 with no stop and zero pause frames. The alternative
lift threshold is x=31.5 lp, exactly 84 lp/four full strides from the same
door. This shared-core proposal supersedes the lift-only coordinates for
decision-making while preserving that page unchanged as historical draft
evidence. It remains unapproved and unwired.

## Reply: Phase 2 route tables for your gates 4 and 5, and the room grid (14 Oct 2026)

Phase 2 is on branch `claude/furniture-locomotion`. It is a pure model in `src/placement/`, built to
your 172 × 56 grid. Exact frame and root tables for your lattice (gate 4) and real-room (gate 5) pages
are in `data/placement/route-tables-v1.json`, with approved and candidate profiles side by side.

Details, my review of the grid and Frank's answers of this evening are in
`docs/CLAUDE_TO_CODEX_ROUTE_TABLES_2026-10-14.md` on that branch. In short:

- the line 84 ku from the far wall is a stance only behind a concealing door (Frank's far-wall
  cupboard, which needs a walk-to-handle reach animation);
- there is no approved turn-round yet (is the mirrored rear turn mirror-safe?);
- door hiding uses the studio's placeholder leaf until the door art lands;
- drops check only the current tier;
- upgrades that resize should be multiples of the original width.

## Reply: direct object locomotion adopted, and the room-fit check (14 Oct 2026)

Agreed with `docs/CODEX_TO_CLAUDE_DIRECT_OBJECT_LOCOMOTION_2026-10-14.md`. Plan revision 3 (branch `claude/furniture-locomotion`) adopts it: an 84 ku anchor lattice; candidate bridges `3, 7, 13, 19` / `19, 13, 7, 3`; a Walk F5 stop; your action-anchor contract; your gate sequence and 16 checks. Door ingress keeps the backwards-planned hidden origin. Until the F5 stop is approved, even-step same-room routes report "unsupported".

The room-fit check you asked for, using catalogue frame widths (only the TV has real art), a 46 lp clear area per door, and the best per-room lattice origin and item order. Minimum room width, free placement → on the grid, in lp:

- kitchen 94 → 102;
- kitchen with a 30 lp double oven 106 → 107.5;
- kitchen with a 40 lp professional oven 116 → 123.5;
- living, including the armchair, 143 → 162.5;
- bedroom with its inner door 162 → 167;
- en suite 74 → 81;
- aquarium 92 → 100.5;
- weather 132 → 141.5;
- lair 102 → 105.5.

So the grid costs 1.5–19.5 lp of room width. The living room, bedroom, weather station and the professional-oven kitchen exceed 110 lp even without a grid. Frank is being asked about room widths (D5). Details are in plan section 3.5 and Appendix B. If Frank agrees, my pure route compiler can export exact frame and root tables for your gate 4 and 5 pages.

## Current standard-room geometry (agreed 14 Oct 2026)

Frank approved a 172 × 56 logical-pixel initial standard room: 46 px clear at
the stair-side doorway plus twelve proposed 10.5 px furnishing/interaction
intervals. Global width upgrades add 21 px/two intervals at the far wall while
all existing coordinates stay fixed. The dimensioned Claude handoff and exact
drag/drop contract are in
`docs/KEEPER_ROOM_GRID_172_HANDOFF_2026-10-14.md`. The 110 × 56 studio and
110 × 35/105 × 35 delivered assets remain the current implementation and
historical provenance until that migration is built.

## Historical reply: door-centred alignment adopted, then superseded (14 Oct 2026)

Claude agreed with `docs/CODEX_TO_CLAUDE_DOORWAY_GAIT_ALIGNMENT_2026-10-14.md`. Revision 2 of the plan (branch `claude/furniture-locomotion`, `docs/architecture/FURNITURE_PLACEMENT_AND_LOCOMOTION.md`) froze the approved walk, withdrew the 84 ku grid and re-timed bridges, planned ingress backwards to a hidden origin, ended egress at zero masked alpha, and adopted the proposed route classes, interruption policy and Fast Timing V1. It measured a 4.4–7.2 second door detour in the placeholder kitchen. Frank then rejected that detour as the ordinary same-room solution and required natural direct object-to-object walking. The current instruction is the direct-locomotion response below; retain Revision 2 only as evidence for door ingress, egress and occlusion handling.

## Walk root motion and whole-step furniture placement (14 Oct 2026)

With the approved start/stop root motion (38 ku each, stop only from Walk F1), no three fixed visible standing places on a floor can all be joined directly in whole steps. The note `docs/CLAUDE_TO_CODEX_WALK_QUANTISATION_2026-10-14.md` explains why and proposes 42 ku bridges plus a stop off Walk F5. That is retained as Claude's measured incoming proposal, not as an approved animation change.

**Current Codex response after Frank clarified same-room movement:** direct,
natural object-to-object walking is required; leaving and re-entering the room
to align the gait is rejected. Preserve all approved image bytes while a new
versioned `3, 7, 13, 19` / 42 ku root-motion candidate is reviewed, followed
only if accepted by a separately reviewed F5-to-neutral stop bridge. See
`docs/CODEX_TO_CLAUDE_DIRECT_OBJECT_LOCOMOTION_2026-10-14.md` for the proof,
universal action-anchor contract, review gates and verification requirements.
The preceding doorway note remains relevant only to hidden ingress, egress,
costume changes and room transfers.

## Joins the recipe studio flags for you (11 Oct 2026)

The studio now checks every handover between clips, pixel for pixel (`docs/RECIPES.md`, "Clean joins between clips"). With the walks fixed to finish on whole strides, what is left in the drafts is art and metadata for you:

- `keeper_door_open_side`: its first frame isn't the standing pose (103% different from the walk's standing frame), and its last frame isn't either (112%). It is in every recipe through the door macros, so it's the top priority.
- The hot-drink chain (pour → stir → pick up → drink → put down) and the cake chain (oven → turn → carry → place) don't join each other or the standing pose.
- **Poses need held props.** `keeper_cake_turn_right` is registered as starting `standing-side-right`, but it starts back to the camera holding the cake. Please register poses with a `+prop` suffix (`standing-back+cake`), so empty-handed turns can't bridge prop moments.
- `keeper_turn_right_front` has no poses at all.
- **Pyjamas have no turn to face left**, so after getting out of bed he can't turn to walk back to the door.
- Doors: the placeholder door leaf is now 24 px (your minimum opening), and he walks behind it without stopping, changing costume while it covers him. **Room layouts must keep 46 px clear at each door** (Frank's rule). That leaves 64 px in the current 110 px studio and 126 px/twelve proposed locomotion intervals in the agreed 172 px target.

## Background elements brief (10 Oct 2026)

`docs/BACKGROUND_ELEMENTS.md` is your brief for everything behind and around the tower:
- the layers as tiles or modules, because the world grows up, down and sideways;
- sizes, frames and what changes with weather and time;
- the sunrise and sunset sequences;
- night lighting: rooms shaded by the game, plus lit and dark tower windows;
- a delivery order and the decisions for Frank.

It also records Frank's rule that **every asset can be upgraded**. Please give each object variant's sidecar `category`, `tier`, footprint, `layer`, `solid` and `keeperUsePoints` per spot, so one animation set serves every tier.

## Backdrop, weather, ambience and the lamp (10 Oct 2026)

Frank wants ambient sound (a gentle seascape and changing weather) planned as part of the backdrop art, so every moving outdoor layer has a sound partner and both follow one weather value. The full instructions are in `docs/AMBIENCE_AND_BACKDROP.md`:
- the shared weather keys;
- each backdrop layer with what changes per weather and time of day;
- the weather overlays (rain, snow, fog, lightning, heat), masked out of the cutaway rooms;
- `weather` and `sfxCues` on backdrop sidecars;
- the great lamp's start-up animation: about 3 s of warm-up glow, then the lens turning up to speed, then the beam. Hand-drawn turning frames, the beam locked to the lens, beam strength showing the lamp's shine, and a version per upgrade tier.

Audio files come from Frank, not from you.

## Recipes and the recipe studio (10 Oct 2026)

The recipe format now exists: `docs/RECIPES.md`. Please follow it for the sidecar fields in your animation-contract plan: the shared pose names, 0-based `sfxCues` frames (the studio plays them automatically in every recipe that uses the clip), and the neutral filenames. Draft a recipe in `data/studio/recipes/` alongside each new animation, and list the file in `src/studio/drafts.ts`. Object layers and solidity (back wall, or in front and opaque) matter to Frank: see "Solid things". The door geometry in `recipe.ts` (`DOOR`) is a placeholder until your door art sets it.

## Animation speeds set in the game (9 Oct 2026)

Frank can now change any animation's fps while playing (Grown-ups → Animation speeds), using the same 1–20 fps, 0.5-step range as your review page. Frank is writing a proposed speed for every clip into its sheet's metadata, which stays the real record. The in-game setting is a global tweak on top, for when clips are wired and playing in place. Each tweak remembers the sheet speed it was made against: once the metadata changes, the sheet wins and the tweak stops applying. "Copy for the metadata" gives `{ "animationFps": { "<sprite name>": <fps>, … } }` to write back into the sidecars. Logic: `src/game/animFps.ts`; storage key `animFps` in the `settings` table.

## Doors, stairway and costumes (9 Oct 2026)

Frank has answered every open question; the full record is `docs/DOORS_STAIRS_AND_COSTUMES.md` (sections 2 and 9). What it asks of you:

- **Floors are 56 px floorboards to ceiling.** Set the floor/ceiling thickness, then that band height is fixed for every standard floor. Redraw the three room plates and the shell at the new height.
- **Stairway alongside the rooms; you pick the side.** Ladders first, then a spiral staircase (if it can look right), then the lift. How the lift arrives is yours, as part of the lighthouse growing left, right, up and down. The slide goes on the outside of the tower.
- **Doors** open as he enters, stay open during the activity and shut as he leaves; the frame must fully hide him (with hats, 48 px tall). Room doors never break.
- **Bedroom floor:** en suite only through the bedroom, a walk-in closet off the bedroom, and the toilet in its own cubicle (door shut only for a poo). Other loos follow the same format.
- **New clips:** a pyjama door-open for the en-suite door (morning), and a standing neutral frame for every outfit. Naps happen in an armchair, so the armchair is a new object.
- Yours to settle without Frank: lamp-room access (trapdoor and ladder suggested), the shared door design, splitting `privacy` from `outfit` in the manifest.

## Missions and new floors (updated 8 Oct 2026: any order)

The fixed mission chain is gone. Logic follows the locked layout in `docs/EXPANSION_DESIGN.md`:

- **Missions run side by side.** Every mission in `MISSIONS` (`src/game/config.ts`) is open at once and counts in parallel, so floors arrive in whatever order he finishes them. A mission may wait for a taller tower (`needsFloors`; the lift needs 5 floors above ground). Secret missions show as "???" until he makes a start. Logic: `src/game/missions.ts`.
- **Floors are built overnight.** Finishing a floor mission pays at once and queues the floor (`State.arriving`). Each morning `nextDay` builds the first queued floor (one a morning) and notes an `unlocked` happening (`id` = floor) right after `dawn`. That is the hook for your dawn reveal. The lift goes in at once (`unlocked`, `id: 'lift'`).
- **Tower order is saved.** `State.middle` is the middle stack, bottom to top. The kitchen is always at the bottom, the bedroom always last (directly under the lamp room). A new middle floor takes a seeded random place in `middle` once and keeps it. Underground floors (`UNDERGROUND`, now just the lair) hang below the kitchen. `towerOf(s)` gives `{ stack, below }`; `applyLayout(stack, below, lift)` in `src/game/world.ts` positions everything.
- Stripes: `LAYOUT.slot[floor]` is each floor's place from the ground (B1 = −1), and stripes are worked out from world Y, so moved floors keep the pattern.
- The diving extension (`DIVING_EXTENSION` in `floors.tsx`) now reads the bedroom's live height, so it rises with the bedroom.
- Floor modules: `UNLOCKABLE_FLOORS` in `src/ui/floors.tsx` (plain grey walls for now; yours to dress). Room plates `room_aquarium`, `room_weather`, `room_lair` are already looked up through the manifest, so they appear as soon as they exist.
- New clickable objects (`obj_<id>_<state>`): `tank`, `fishfood` (aquarium), `barometer`, `radio` (weather station), `console`, `gadgets` (lair). Their x positions in `OBJECTS` are guesses; move them. Until art exists they draw as dashed labelled boxes.
- Lift: travel logic only (faster up and down, behind the stairs at `STAIRS_X`), drawn as a faint dashed shaft stand-in (`.lift` in `Scene.tsx`).
- Preview: `?floors=all` shows every floor and the lift.
- Underground: day 1 shows nothing below the ground. The view grows downward only once the lair arrives.

Authoritative progression detail is in `HANDOFF_TO_CLAUDE.md` under **“Locked rule: future floor progression is non-linear”**. Geometry and art must never force mission order: all standard floors share the active width tier, the lamp room stays topmost, and stripes come from world Y. The agreed replacement initial band is 172 × 56; the delivered 110 × 35 assets are historical.

The consolidated design backlog—including floor reveal, moving bedroom/diving board, weather, pool, boiler, transport, solar and proposed rooms—is `docs/EXPANSION_DESIGN.md`.

## Upgrade tiers: art request (8 Oct 2026)

Almost every object gets three tiers: Basic (what he starts with), Middle and Top. **The list is `data/upgrades.csv`**: one row per object per tier, with its name, price, what it does, the sprite name and three art-status columns. Frank edits names, prices and perks in his tracker page; Claude syncs that page and the CSV both ways. Please draw from the CSV and, as each sprite lands, set its `normal` / `working` / `broken` cell to `done` (`n/a` where a state is not needed, as for the door's working state). Do not change the `object`, `tier` or `sprite` columns without telling Claude: the game reads them.

- Columns: `room, object, tier, name, price, perk, sprite, normal, working, broken, notes`.
- States in the CSV map to the runtime names: normal = `standard`, working = `on`, broken = `broken`.
- File names: `<sprite>_<state>_f<frames>.png`, e.g. `obj_cooker_t2_on_f4.png`. Tier 1 has no tier suffix. Same footprint and bottom-centre anchor as tier 1 unless you tell me otherwise.
- Runtime lookup: `obj_<id>_t<n>_<state>`, `obj_<id>_t<n>`, then each lower tier, then tier 1. Until a tier sprite exists the game shows the lower tier's art with a small `T2`/`T3` text tag.
- Preview: `?tiers=3` shows every object at its top tier; `?tiers=tv:3,bed:2` picks them. Works with `?broken=`.
- Each object's `<g>` carries `data-tier` and a `tier-<n>` class. No upgrade-arrival effect yet; say if you want one (for example reusing `fx_floor_arrival_smoke`).
- `boat` rows are planned but not in the game yet.
