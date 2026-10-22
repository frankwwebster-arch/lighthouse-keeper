# Lighthouse Keeper: status write-up (21 Oct 2026)

## What it is
A Sims-style web game for Ralph (7) and Eddie (11). A keeper lives in a lighthouse; kids type commands (typo-tolerant, curated, no live AI) or click objects (Sims-style menus, auto-zoom camera). Needs and mood, credits, phone, bedtime, multi-day play, a day report, quiz pop-ins, time-aware chat, cheeky humour.

## Where it lives
- Code: github.com/frankwwebster-arch/lighthouse-keeper (branch `main`).
- Live: **https://lighthouse-keeper-mu.vercel.app** (the one address to use and bookmark).
- Vercel project `lighthouse-keeper` (team frankwwebster-4308s-projects). Pushes do not deploy; only a `[deploy]` commit on `main` builds production (`npm run deploy`, or the GitHub Actions "Deploy to production" button). See `docs/DEPLOYMENT.md`.
- The long addresses like `lighthouse-keeper-di4axnjgx-...vercel.app` are one-off links for a single deploy. Ignore them; they are also login-protected.
- Database: Neon Postgres via `DATABASE_URL` (verified: `/api/players` answers `db:true`). Tables are created on first use: players, saves, player_rules, settings (PIN hash).

## Built
Engine (seeded, deterministic, 122 tests), SVG cutaway scene with zoom camera, typo matcher, quizzes levels 1-3, credit economy with admin dials (allowance from per-need green bars, prices, gifting, quiz level and breakdown pressure per player), who-is-playing screen, per-player saves (DB or localStorage), grown-ups PIN (starts 1234; change it).

The first three playable floors are now modular fixed-width components: kitchen, living room, and bedroom with en suite. Objects have a runtime `standard` / `on` / `broken` contract, state-specific strip support, shared broken effects, keyboard/touch hit areas, and rear-facing cooker/basin keeper fallbacks. Random keeper-owned breakdowns are off by default and controlled by grown-ups' frequency and maximum-concurrent dials; broken assets block normal use until repaired. Floor 3 reserves an invisible two-door changing zone for the later diving-board extension.

Missions (`src/game/missions.ts`, list in `config.ts`) are all open at once and count in parallel, so floors arrive in any order: Fishy Business → aquarium, Storm Chaser → weather station, Strange Rumblings (a mystery until he makes a start) → hidden lair underground, and Puffed Out → lift (opens once the tower has 5 floors). Goals count things he already does (fishing, nature channel, telescope, ships kept safe, digging, visitors, quiz answers, good days). A finished mission pays credits (10 by default) at once; its floor is built overnight and appears the next morning, furnished (one new floor a morning; the lift goes in at once). Each new floor takes a random middle place, saved for good: kitchen always at the bottom, bedroom always directly under the lamp room, lair below ground. The view zooms out to fit; the lift makes stairs quicker. 🎯 Mission button shows progress; grown-ups set an overall mission size (% of normal) and reward, then can override any single goal or reward, and can finish any open mission. Typing about a floor he has not got gets a hint. `?floors=all` previews every floor. New floors and furniture are stand-ins until Codex's art (hooks in docs/FOR_CODEX.md).

Upgrades: almost every object has Basic, Middle and Top tiers, listed in `data/upgrades.csv` (Frank's tracker page and Codex both work from it; `npm run upgrades` copies it into the game, and a test fails if the copy is stale). He buys the next tier from the object's tap menu with credits; a new one replaces a broken one. Each tier makes that object's jobs do more good (+25% / +50%) and take less time (−15% / −30%); the bed's tier sets the morning's energy (80 / 90 / 100%). Grown-ups set one price % for all upgrades, can override any single tier's price, and can give any next tier as a present. Tier art is a stand-in (`T2`/`T3` tag) until Codex's `obj_<id>_t<n>_<state>` sprites arrive; `?tiers=3` previews them.

The living-room nap now belongs to an upgradeable passive armchair: basic
armchair → rocking chair → Lazyboy-style recliner. All tiers retain the same
11 px seat contact, and passive furniture is excluded from breakdowns.

The recipe studio now consumes a checked keeper pose contract. The reviewed
191-sheet keeper source batch is unchanged as the visual-history denominator;
73 exact neutral stills and reusable bridge derivatives bring the working raw
inventory to 325 keeper sheets. Standard sample flows, four-facing standing
turns and the TV seated turn have exact neutral joins, approved outfit walks
have neutral-ended cycle/start/
stop derivatives, and every full-body sidecar has registered pose metadata.
The remaining 300 legacy endpoint repairs are measured from real RGBA pixels
and ordered in `docs/KEEPER_NEUTRAL_ENDPOINT_AUDIT.md`. `npm test` rejects new
or regressed endpoint failures against that frozen migration boundary.

The Bubble stories Studio has a complete shared picture catalogue: 339
selectable pictures and 452 immutable versions grouped by activity. This includes every review-ready
isolated source component from Activity Cloud Composer V1–V7, the rear-work
V2/V3 callout packs and every component-bearing Claude or Codex picture pack,
including all V5 album homages, the complete aquarium and bedroom sets, and 54
new pictures across fishing, gardening, pet play, fixing tools, pub, art and
inventing. The importer is idempotent and the verifier fails if any of those
298 pinned source components disappears; existing versions remain immutable.
The new cold mark and later heat/aroma/welding versions are selectable while
all earlier versions remain available. Frank approved the six-picture
ligne-claire BBQ pilot; its six translations are new current versions without
replacing or mutating their predecessors. The family-by-family action-imagery
prompt records the approved flat-ink language and the boundary that defers any
whole-game restyling. The companion display proposal uses an opaque rounded
rectangle activity panel, variable emotion balloons and unenclosed reaction
marks.

Frank stopped the family-by-family ligne-claire conversion on 22 October 2026.
The 222 earlier pictures without a ligne-claire draft are historical catalogue
state, not an active queue. The final recipe remains in
`docs/CODEX_PROMPT_BUBBLE_STORIES_LIGNE_CLAIRE_ACTION_IMAGERY_2026-10-21.md`.
Every asset present at closure is available in the Bubble creation tool: 339
picture ids / 452 versions, all in named Studio groups. The minimum complete
set is recorded in `data/activity-stories/catalogue-closure-2026-10-22.json`;
the importer now includes registered Bubble-specific packs and
`npm run verify:activity-stories` fails if any closure version disappears.

Frank approved the first family continuation on 21 October 2026: seven
remaining BBQ-food candidates and seven remaining BBQ-tool candidates are
isolated into two immutable V1 packs with fixed-palette 256 × 256 RGBA
components, pinned prior hashes, prompt/rejection records, deterministic
verification and light/dark/64 px contact sheets. All 14 are registered as
current V2 versions; their V1 predecessors remain byte-identical and
selectable. At the BBQ gate the shared library therefore had 305 pictures and
333 versions.
No story, `src/activityStories/` file, production/runtime art or deployment
changed.

Frank approved the next five-picture sandwich semantic set at
`art/drafts/activity-story-ligne-claire-sandwich-2026-10-21-v1/`. It proposes
V2 drawings for bread, ham, lettuce, tomato and the finished sandwich, with
pinned V1 references, exact prompt/rejection provenance, deterministic
fixed-palette normalization and light/dark/64 px evidence. All five candidates
are registered as current V2 versions, while every V1 remains byte-identical
and selectable. The catalogue now has 305 pictures / 338 versions; no story,
activity-story runtime, production art or deployment changed.

Frank then approved the five-picture washing family with “approved continue -
update your recipe as you go”. Its immutable pack is
`art/drafts/activity-story-ligne-claire-washing-2026-10-21-v1/`; all five
translations are current V2 versions and all V1 predecessors remain
selectable, taking the catalogue to 305 pictures / 343 versions. The approved
plate's controlled minor irregularity is now shape calibration alongside the
tomato's flat-colour calibration.

Frank then approved the five-object General repair family with “approved. tool
chest the best” and clarified that plate, tomato and tool chest are all style
champions. All five translations are registered as current V2 versions from
`art/drafts/activity-story-ligne-claire-general-repair-2026-10-21-v1/`, while
every V1 remains selectable, taking the catalogue to 305 pictures / 348
versions. The tool chest adds construction, detail hierarchy and confident
object presence to the plate's shape and tomato's colour calibrations. Claude's
story, the activity-story runtime, production art and deployment are unchanged.

Frank approved the eight-piece repair hand-tools pack at
`art/drafts/activity-story-ligne-claire-repair-hand-tools-2026-10-21-v1/`.
Its adjustable spanner, C-clamp, combination pliers, flat-head and Phillips
screwdrivers, hand saw, spirit level and tape measure are current immutable
V2s, taking the catalogue to 305 pictures / 356 versions. “Ligne claire, not
cartoon” remains explicit: adult proportions and credible mechanisms exclude
cute, toy-like, inflated, caricature, mascot and sticker treatments.

Frank subsequently approved the nine-picture cooking core, taking the
catalogue to 305 pictures / 365 versions, then eight baking/eggs/mixing pictures
plus the separate observational hen correction, taking it to 305 pictures / 374
versions. The cartoon-like family-pack hen remains rejected and unregistered.

The latest approval is the seven-picture farm-animals-and-meals pack at
`art/drafts/activity-story-ligne-claire-farm-animals-meals-2026-10-21-v1/`.
Cow, pig and sheep are full observational redrafts informed by Frank's horse
reference rather than restyles of the cartoon-like V1 drawings; the four meals
preserve their exact V1 compositions. All seven are current immutable V2s, so
the catalogue now contains 305 pictures / 381 versions. Every V1 remains
selectable, Claude's story/runtime is unchanged, and nothing was deployed.

The first immutable condiment review gate at
`art/drafts/activity-story-ligne-claire-condiments-2026-10-21-v1/`. The first
honey-pot attempt was rejected for glossy cartoon clip-art modelling; the
evolved recipe uses thinner living contour, controlled asymmetry, fewer flat
colour steps and sparse material cues. It remains unregistered historical
review evidence.

Frank judged the first condiment gate's glass containers “too shiny, not flat
enough”. The complete first gate remains immutable; the approved correction pack is
`art/drafts/activity-story-ligne-claire-condiments-flat-glass-correction-2026-10-21-v1/`.
It supplies seven flatter glass corrections and carries ketchup/mustard forward
byte-for-byte. Frank approved the exact sheet with “yes much better” and set
the binding taxonomy: **one even black outline, flat colour, no shine**. All
nine are current immutable V2s. The catalogue now contains 305 pictures / 390
versions; 77 current pictures are approved ligne-claire conversions and 228
remain. Every V1 remains selectable and nothing was deployed.

Claude's first direct picture commission under Frank's 21 October standing
instruction is complete at
`art/drafts/activity-story-ligne-claire-new-pictures-2026-10-21-v1/`. Nine new
objects and six new action marks are registered as V1 IDs, taking the catalogue
to 320 pictures / 405 versions. Claude reviewed the exact light/dark/64 px sheet
and wired the new pictures into the relevant stories and action demos on 22
October. All 15 pass the
flat-palette, line, 64 px, gutter, ownership and hash checks; nine rejected
attempts remain pinned. The later wiring changed only story/demo data; it did
not change the activity-story runtime or an approved art authority.

The tea-and-toast art gate at
`art/drafts/activity-story-ligne-claire-tea-toast-2026-10-22-v1/`. Its six
flat-colour V2s cover the legacy kettle, milk, mug, butter-and-jam,
toast-slices and toaster pictures. The contact sheet includes light, dark and
64 px proofs. Frank approved the exact sheet with “These are superb, I think
the best yet, and they follow the direction very well”; all six are registered
and every V1 remains selectable. His requested `tea-mug-empty` V1 and clean
`toast-slices` V3 are also current; the latter removes exactly five detached
action-slash components so the marks can be added separately. At that approval
checkpoint the catalogue was 321 pictures / 413 versions, with 83 approved
conversions and 222 earlier pictures without a ligne-claire draft. The later
Claude-reviewed black-ink/recipe commission brings the current totals to 339
pictures / 452 versions without changing the 83 Frank-approved conversion
count or the 222-picture earlier-art remainder. That remainder is paused, not
queued for further conversion.

**Still to do on floors:** the dawn reveal animation (Codex; the `unlocked` happening after `dawn` is the hook), furniture migration and the walking-distance bathroom rule from `docs/EXPANSION_DESIGN.md`. The diving extension now follows the bedroom's height but is not playable yet.

## Not built yet (agreed design)

Keeper review cards now also preview, save and export a proposed per-clip
runtime FPS. Accepted `animationFps` values belong in each animation's source
JSON sidecar and generated runtime manifest, not in the PNG sprite pixels.

The first full-face canon pack remains approved historical geometry evidence,
but live animation exposed that its exact Frame 6 raster is too visibly
pixelated to serve as a modern render endpoint. Frank reset all animations:
the Animation Workbench still contains zero Final and zero active Draft items.
V1/V2 turn and transition work is retained only as reversible provenance.
Frank permanently approved `keeper-prime-master-2026-10-12-v1` on 13 October
2026 with “Approved. Make sure this is NEVER forgotten.” It is the sole smooth
density-8 identity authority and uses one broad pale jumper band. The approved
orthographic authorities are the smooth V5 rear with correctly rear-facing
boots and the 15/15 rigged Side-right V1. KP Rig V1 and Motion V3 are approved
construction authorities. Front ↔ side Turn V1 is approved with its recorded
minor 45° cadence limitation, and exact nine-frame side-right ↔ back V9 is
approved and pinned by V10; the 16-frame V8 experiment remains rejected as
jerkier. Every approved model requires a smooth high-resolution master in
addition to passing geometry.

Frank approved exact Walk V6 and the exact stop → walk → stop V1 bridge on
14 October. The latter uses reversible registered bridge poses and root-motion
deltas 2, 6, 12 and 18 into the 21 px/frame walk cadence, with no walking on
the spot. Walk → stop → turn to camera V1 composes only these approved artwork
authorities and was judged excellent. Frank then approved **Fast Timing V1**:
walk 10 fps, deceleration 12 fps, zero neutral pause, turn 16 fps and a 625 ms
endpoint hold. This is the project timing authority only for locomotion,
stopping bridges and turns. Action entry, loops, exits, reactions and prop
choreography remain independently paced so enjoyable actions can be savoured.
The approved movement foundation entered a separate versioned Prime runtime
bank on 22 October. It installs 27 sprites / 217 registered frames. The game
actively uses Prime side idle, walk start/cycle/stop, stair ascent/descent and
generic rear work. Turns, ladder, four-way sit/stand and darts are installed
but await gameplay choreography. The legacy Workbench Final lane remains
untouched because this promotion has its own hash-pinned register and draft.
Stair-ascent V18 is now a separate corrective review after Frank identified a
contact/passing lower-beard jump in the approved V16 source. It modifies only
two recorded beard masks and has not replaced the V16-derived runtime asset.

The consolidated Prime Keeper animation library is now available at
`/prime-keeper-animations`. It indexes 14 approved playable authorities across
locomotion, turns, stairs, ladder, four-way sit/stand and contextual activity.
Every clip has independent and global transport controls, including exact frame
stepping, and all 213 unique source images are decoded before controls unlock.
Its non-destructive sandbox combines, reorders, reverses and repeats clips,
persists locally, exports JSON and warns when declared endpoint poses need a
bridge. The held-implement POC V3 is linked but correctly excluded from the
playable approved bank because its proxy body artwork is not production-approved.
The library now marks installed clips and shows approved source motion beside
its runtime delivery. See `docs/PRIME_KEEPER_ANIMATION_LIBRARY_2026-10-21.md`.
The complete prioritized gap list—covering every one of the 38 current game
interactions—is `docs/PRIME_KEEPER_ANIMATION_GAPS_2026-10-22.md`.

The approved kitchen full-room authority is
`/keeper-review/kitchen-continuous-run-approved-v23/`. Frank marked exact Image
1 with “this is correct” at `(37.3%, 56.9%)`; its `2170 × 725` PNG is preserved
byte-for-byte with SHA-256 `5d5451…f9707`. V23 keeps the full-height cabinets on
one plane with one uninterrupted sea-glass worktop and common dark base. V21
still supplies the isolated asset inventory: compact single-door basic oven,
V20 double oven as Upgrade 1, standalone pedal bin, and one-person table/chair.
V22 is immutable rejected assembly provenance because its deterministic rebuild
misread the kettle edge as a shallower cabinet body. V23 is approved visually
but is not promoted or wired into the live game; details are in
`docs/KITCHEN_CONTINUOUS_RUN_APPROVED_V23_2026-10-17.md`. The active one-change
successor is `/keeper-review/kitchen-rear-facing-chair-v24/`: its sole chair is
centred on the player-facing side of the table and shown from behind, so seated
Prime faces the rear wall with his back to the player. V24 awaits visual
confirmation and remains unpromoted/unwired.
The preceding follow-up is `/keeper-review/kitchen-narrower-bin-v25/`, which makes
only the standalone turquoise pedal bin 20% less wide while retaining its
centreline, height and floor contact. V24 remains immutable; V25 awaits visual
confirmation and is also unpromoted/unwired.
The subsequent scale review is `/keeper-review/kitchen-game-scale-prime-v26/`. It shows
V25 at the exact `193 × 56-lp` room contract and `4 px/lp` presentation, both
alone and with the `32 × 40-lp` Prime standing and seated rear-facing at the
table. V26 is derived evidence only; V25 and all Keeper sources are unchanged.
Kitchen V27 at `/keeper-review/kitchen-broken-loops-v27/` is retained as
rejected provenance. Its short, fast loops and independently constructed fault
art are not reused as the visual or timing authority for replacement work.
Kitchen V28 at `/keeper-review/kitchen-bin-states-v28/` redraws the pedal bin
from scratch as a coordinated static standard/broken family, adds a restrained
floor spill, and shows both states in the exact 772 × 224 px game-scale room.
Frank approved the bin itself. The current effect-only successor is
`/keeper-review/kitchen-bin-effects-v31/`. V29 established the accepted colour
and ten-second cadence but was too subtle; V30 rose higher but read as an
object-shaped plume rather than an immediately recognisable bad smell. V31
preserves the exact bin and ten-second cadence while replacing both overlays
with young-reader comic grammar: three curling green smell trails, loose broken
haze and three clearer slow flies. V31 is review-only and does not change
runtime, Final art or canonical V20–V30 sources. Frank approved the exact V31
family on 18 October 2026; its hashes are now the kitchen-bin fault authority.
Kitchen V32–V38 are rejected, unpromoted provenance. The deployed review made
clear that the fridge, toaster, oven and bowl replacements had not first
removed the original asset; the fridge pool missed the real floor surface;
kettle effects were unreadable; oven/basin effects and placement were wrong;
and the table hid the chair's lower half. The historical V32 approval is
superseded by `docs/review/kitchen-v32-v38-rejection-2026-10-18.json`.

The active fridge successor is
`/keeper-review/kitchen-fridge-states-v39/`. V39 is a complete from-scratch
standard/broken family, not repaired V32 pixels. The compositor clears the old
fridge before inserting either state. Standard occupies exact room bounds
x=84–168/y=140–218; the broken door and pool reach the actual y=218 floor; a
compact surviving lower hinge is visibly connected; and one grille appears per
state. Generic contents remain visible. The separate 40-frame/4-fps ten-second
drip/ripple strip contains no fridge pixels and is shown both alone and over
the broken state. Frank approved exact V39 on 18 October 2026; its source,
sprites, room proofs, effect strip, catalogue, register, page and archive
manifest are hash-pinned in
`docs/review/kitchen-fridge-states-v39-approval-2026-10-18.json`. Approval is
review authority only; V39 remains unpromoted and unwired.

V40 is rejected because its oven was too tall/insufficiently wide and its
smoke rose as bubbles. V41's exact-size local correction and the broader
asset-by-asset replacement method are also rejected. V32–V41 remain immutable,
unpromoted evidence; V39's earlier fridge approval is historical rather than
the current construction authority.

Rebuild V1 established the accepted coherent room/cabinet/table construction:
exact `772 × 224` room, six equal `84-px` bays at x=84–588, y=134 worktop,
y=151 fascia and y=208 foot line. Frank called it excellent subject to changing
the fridge door to white.

Frank approved the cabinet-only
`/keeper-review/kitchen-cabinet-run-v11/`. Frank rejected V10's cabinet and
appliance art because it ignored the required polished style and flat-cutaway
projection and was unacceptably blocky. V10 remains immutable rejection
provenance. V11 draws one new high-resolution two-cabinet run from scratch in
the storm-blue, sea-glass, navy and aged-copper palette, then derives an exact
168 × 74-pixel installed body with four-pixel transparent cell gutters. The
same native sprite is duplicated at x=168 and x=420 in the exact 772 × 224 room
proof, leaving the 84-pixel standalone-oven gap untouched. The sink is now a
later standalone element like the fridge, oven and dishwasher. Exact V11 is
hash-pinned by
`docs/review/kitchen-cabinet-run-v11-approval-2026-10-19.json`; it remains
unpromoted and unwired.

Layout V12's room registration and white-goods envelopes were approved, but
its proposed sink overlay was immediately superseded. The sink must not sit on
an existing cabinet. V13 established one complete independent 84 × 74 px sink
cabinet with its own worktop, basin and intact tap, but its perspective is
rejected because it does not match approved V11. V14's On stream is also
rejected in registration because it begins a few pixels below the outlet. Its
Broken upward-basin-spout animation is approved and retained. Both older routes
remain immutable.

V15 is rejected because its newly drawn worktop shoulders, drawer/door faces,
rails and plinth remain geometrically different from approved V11. V16 fixed
the front elevation with a literal crop of the approved V11 right-hand bay,
but its countertop ended flush at the join and its basin read too straight.
V17's uniform left worktop return is rejected because it reads as an extension
of the whole left side rather than an angled join across the worktop plane.
V18 remains immutable approved predecessor evidence at
`/keeper-review/kitchen-sink-angled-join-v18/`, but later close inspection
reopened its left worktop finish. The active V19 visual-review draft is
`/keeper-review/kitchen-sink-smooth-join-v19/`. It remains one complete,
independently removable 92 × 108 px sprite and replaces only V18's coarse
three-row staircase with a partial-alpha down-right contour whose final row
curls into a rounded front lip matching the right edge. The exact V11 front
begins unchanged at cell y=43. The basin side edges still splay in the opposite
direction, widening slightly from x=20–70 at the rear rim to x=18–73 at the
front lip. Standard, On base and Broken base are byte-identical. V15's corrected
On strip and approved Broken strip remain byte-for-byte water-only 40-frame/
4-fps ten-second loops with 0.1×–4× review speed. Frank's V18 approval record
remains hash-pinned historical evidence; V19 is reversible, unapproved,
unpromoted and unwired.

The active effect-only successor is Sink Water Workbench V20 at
`/keeper-review/kitchen-sink-water-workbench-v20/`. It leaves the complete V19
sink and room byte-identical, narrows the ON flow to the exact four-pixel tap
outlet and begins it immediately below that outlet, and raises the BROKEN jets
well above the tap for comic emphasis. Both candidates remain separate
40-frame/4-fps ten-second layers. The new asset-first workbench lets Frank add
or remove the relevant animation, drag it, resize it, crop it, nudge it, vary
speed from 0.1× to 4×, persist settings locally and export placement JSON. V20
awaits visual review and changes no Final or runtime asset.

Cabinet Join Backfill V21 remains immutable predecessor evidence: its blue
body mask concealed the cream wall slit, but the two sprites' overlapping
softened worktop end contours still made a jagged double-width seam.

The approved structural-layer correction is Countertop Join Cap V22 at
`/keeper-review/kitchen-countertop-join-cap-v22/`. It leaves the exact V11 run,
complete V19 sink, V21 and room background byte-identical. V22 retains the
dynamic body mask, then draws a separate twelve-row cap over only the shared
worktop after both sprites. Its default treatment restores uninterrupted
horizontal worktop bands; an optional single soft angled seam replaces the two
overlapping staircases. Both layers follow the live small gap and turn off
beyond an eight-pixel separation or six-pixel overlap. Frank approved the exact
seamless treatment and this layered method for future fitted modular kitchen
joins. The approval remains a review authority only and changes no Final or
runtime asset.

The exact-placement predecessor is Kitchen Snap Grid Join V23 at
`/keeper-review/kitchen-snap-grid-join-v23/`. It retains the approved V22 join
and all five source images byte-for-byte. During drag the sink may follow an
imprecise pointer, but release discards that coordinate and commits to the
nearest legal 84-pixel bay origin after occupancy checks. The Prime stop/turn
target is derived from the snapped logical body midpoint: the default sink
commits at x=336 and targets x=378/y=218. The seamless join activates only for
exactly adjacent committed bounds, so its logical gap is guaranteed to be zero.
V23 changes no Final or runtime asset.

The superseded surface-state proof is Kitchen Exposed End Healing V24 at
`/keeper-review/kitchen-exposed-end-healing-v24/`. It preserves V23 snapping,
legal footprints and Prime midpoint anchors. An exact neighbour still selects
the approved V22 body and countertop join repair. When the sink's left edge is
instead exposed, the compositor overlays the exact approved V11 cabinet run's
leftmost 12 × 82 pixels, registered at body origin minus four pixels, to supply
the established rounded teal lip and blue cabinet end. The exposed-end overlay
and joined-edge repair are mutually exclusive and recalculated after every
move. The review defaults to exposed bay 5 and includes a review-only raw/healed
comparison. V24 changes no source sprite, Final or runtime asset.

The accepted sink-edge correction is Kitchen Exposed End Cutout V25 at
`/keeper-review/kitchen-exposed-end-cutout-v25/`. V24's V11 crop was the right
end treatment, but its transparent rounded contour allowed the obsolete V19
sink join triangle to remain visible underneath. V25 draws the movable sink on
an isolated layer, clears the exact 12 × 82 V11 replacement window only when
the left side is exposed, then draws the V11 end before compositing that layer.
Joined placement skips the clear and retains the complete sink for V22. The
page defaults to exposed bay 5 with guides hidden and adds an 8× focus plus a
review-only untreated/corrected comparison. Frank accepted the corrected result
before moving on to the oven. Source sprites, Final and runtime remain unchanged.

Kitchen Standalone Oven V26 is superseded after review exposed three assembly
defects: independently normalised state crops changed the right-hand chassis
width, the warning-light darkening mask produced a black fascia rectangle, and
the browser cleared a guttered oven cell that overlaps neighbouring cabinet
pixels before drawing Broken lighting variants.

Kitchen Standalone Oven V27 at
`/keeper-review/kitchen-oven-standalone-v27/` is now the hash-pinned oven
state-family authority. Frank approved all three states on 20 October 2026
and instructed that they be saved. It retains the coordinated
cream/ivory, navy and copper Off/On/Broken design and exact 84 × 77 px body at
x=336–420/y=131–208, with Prime's interaction anchor fixed at x=378/y=218. Off
and On now use equal source windows and share byte-identical exterior alpha;
only recorded control/cavity regions change. Broken's dormant and lit red lamp
are selected by a compact shape-derived mask, and its internal-light mask
follows amber cavity pixels rather than a rectangle. Every Broken lighting
combination is a complete precomposed 772 × 224 room, so no cabinet or wall
pixel is cleared in the browser. The irregular independent 40-frame/4-fps/
ten-second cavity and lamp schedules start automatically and remain removable
and variable-speed. Its installed room perspective was withheld: the hob top
is substantially deeper and more steeply converged than
Cabinet V11's shallow cutaway worktop, making the oven read from a higher
viewpoint than its neighbours. V28 now supersedes that installed perspective
while retaining V27 as the state-family authority. V27 is
unpromoted and unwired; smoke remains a later reusable effect and no later
kitchen asset has begun. The exact approval boundary is recorded in
`docs/review/kitchen-oven-standalone-v27-state-family-approval-2026-10-20.json`.

Kitchen Standalone Oven V32 at
`/keeper-review/kitchen-oven-standalone-v32/` is the active installed oven
review gate. V31 is rejected because its full-width foreground cap removed the
correct V30 triangular transition and made the worktop look rectangular. V32
preserves every V30 oven state and animation byte-for-byte, restores the V30
triangular underlay behind each snapped edge, and masks only the six-pixel
cabinet-facing end contour with approved V22 row colours. The oven-facing
diagonal remains intact; the adjoining cabinet surface reads as a continuous
slab with no second diagonal seam. The approved V22 cabinet-blue body fill is
still drawn behind both assets to conceal the lower wall gaps. The left and
right repairs activate independently and are embedded in neither asset.
Dimensions, projection, room bounds, Prime anchor, fault schedules and smoke
separation are unchanged. The V9 workbench still demonstrates smoke interaction
against the obsolete pre-modular oven; its successor follows after this static
gate is approved. V32 is reversible, unapproved and unpromoted; V30/V31,
Cabinet V11, V22, Final/runtime and later kitchen assets remain unchanged.

Kitchen Modular Join Workbench V33 at
`/keeper-review/kitchen-modular-join-workbench-v33/` is the approved combined
sink/oven placement and join authority. One exact V11 two-bay cabinet run remains
fixed in bays 2–3; the exact V25 sink and V32 oven can each be selected, dragged
loosely and committed to any two distinct free 84-pixel bays. The other movable
asset and fixed run are excluded from legal destinations. Prime interaction
anchors always equal the committed 84-pixel body midpoint at y=218. Exact
adjacency is classified by pair: cabinet↔sink uses the approved V22 flat cap;
every pair containing the oven uses V32's triangular underlay, blue body fill
and narrow non-oven seam cleanup; and an unjoined sink left side uses V25's
isolated cutout plus rounded V11 end. Sink and oven can therefore sit together
in either order without baking cabinet pixels into either appliance. All 12
legal non-overlapping arrangements are deterministically verified. Frank
approved exact V33 on 20 October 2026; its catalogue, register, shell and
archive manifest are hash-pinned in
`docs/review/kitchen-modular-join-workbench-v33-approval-2026-10-20.json`.
V33 remains unpromoted and unwired.

Kitchen Modular Fridge Workbenches V34–V36 are rejected immutable provenance.
V34 used obsolete registration and incomplete joins; V35 reversed the Broken
hinge side and changed the door dimensions; V36 corrected those mechanics but
its body blue and countertop depth did not match Cabinet V11. The active
successor is V37 at `/keeper-review/kitchen-modular-fridge-workbench-v37/`.
Its complete `84 × 14 px` worktop is constructed from exact Cabinet V11 pixels,
and its blue frame uses Cabinet V11's exact body palette. V36's successful
mechanics remain: both states are left-hinged, Broken rotates the literal
`68 × 52 px` Standard door at scale `1:1` around the surviving lower-left
hinge, the body is `84 × 74 px` at y=134–208 and overflow is at most four
pixels. Three movable assets retain collision-free snapping, exact Prime
midpoints and pair-aware healing. The ten-second drip/ripple remains separate
and removable. All 24 layouts are verified. V37 awaits visual review and
changes no Final or runtime asset.

Kitchen Split Cabinet Workbench V38 at
`/keeper-review/kitchen-split-cabinet-workbench-v38/` establishes Cabinet V11 as two
independently movable 84-pixel units; there is no pair-movement mode. Cabinet A
and B preserve their distinct original bay centres. Each side is selected
dynamically from exact V11 pixels: exposed sides receive the rounded outer end,
while joined sides receive the internal edge before the existing V22/V32 repair
layer is applied. Cabinet A, Cabinet B, fridge, sink and oven occupy five of six
canonical bays, leaving one exact snap destination. All 720 non-overlapping
arrangements and every pixel of all eight edge variants are deterministically
verified. Frank approved the result with “Fantastic” on 20 October 2026; exact
hashes are pinned in
`docs/review/kitchen-split-cabinet-workbench-v38-approval-2026-10-20.json`.
The reusable rule for later appliances and upgrades is now
`docs/KITCHEN_MODULAR_ASSET_AND_JOIN_STANDARD_2026-10-20.md`. V38 remains
unpromoted; V11, V37, Final and runtime are unchanged.

Kitchen Dishwasher Workbench V39 at
`/keeper-review/kitchen-dishwasher-workbench-v39/` established the standalone
one-bay silver dishwasher with coordinated
Off, On and Broken states. Off/On share one exact silhouette; On adds only aqua
LCD glyphs and a solid green lamp. Broken keeps the same carcass and door but
loses the lower-right hinge, leaving the bottom-hinged door strongly twisted
toward the camera with a bent handle, cracked fascia and red error lamp. Three
separate reusable suds models—compact, regular and emphatic—are forty-frame,
4-fps, ten-second strips with drag, resize, crop, speed, multiple-layer and
removal controls. The default Regular placement makes a large soapy floor
puddle rather than a restrained spill. Six objects fill six bays, so moving one swaps it with the
occupant while retaining exact origins, Prime midpoints and V22/V32 healing.
All 720 arrangements are verified. V39 was rejected because its generated
worktop outline was too heavy and appeared one native row too high beside the
approved cabinets. Its immutable hashes are pinned in
`docs/review/kitchen-dishwasher-workbench-v39-rejection-2026-10-20.json`.

Kitchen Dishwasher Workbench V40 at
`/keeper-review/kitchen-dishwasher-workbench-v40/` is the immutable visual
authority inherited by V41. It retains every non-worktop V39 state pixel and replaces only
cell rows `4–15` with exact Cabinet V11 worktop pixels. Twelve state/edge
sprites cover Off/On/Broken across every exposed/joined left/right condition;
the movable review selects the correct one after every swap, then applies the
existing V22/V32 repair. The corrected dishwasher therefore has the approved
restrained outline and exact twelve-row height wherever it is placed. The full
six-object movable tool and reusable suds controls remain available. All 720
arrangements are verified. V40 itself remains unapproved, unpromoted and
unwired; its exact art is accepted through the approved V41 successor. V39,
approved cabinetry, Final and runtime remain unchanged.

Kitchen Dishwasher Workbench V41 at
`/keeper-review/kitchen-dishwasher-workbench-v41/` is approved and inherits
all 49 V40 image files byte-for-byte. A dishwasher
in Broken state is fixed at its exact snapped bay: direct movement, a swap that
would displace it, and whole-run rotation are rejected. Repairing it to Off or
On unlocks movement. Every suds layer now declares the dishwasher as its owner
and stores its placement in appliance-local coordinates. This is the binding
rule for every later broken movable kitchen asset and its separate smoke,
water, suds or similar effects. There is not yet a gameplay kitchen-furniture
controller, so V41 is tested review/specification behaviour rather than a
runtime integration. The exact approval is pinned in
`docs/review/kitchen-dishwasher-workbench-v41-approval-2026-10-20.json`; V41
remains unpromoted, and V40 art, approved cabinetry and Final assets are
unchanged.

Kitchen Kettle Standalone V42–V44 are preserved but rejected. V42 was too
small and floated at y134. V43 seated correctly but crushed its polished
concept into a muddy 44-pixel sprite. V44 fixed the delivery and scale but its
tiny replacement redraw looked poor beside the concept references. Kitchen
Kettle Standalone V45 at `/keeper-review/kitchen-kettle-standalone-v45/` is the
active reversible gate. It promotes the preferred concept pixels themselves:
the intact 588 × 540 and severely Broken 976 × 928 components become the
actual production masters without repainting or source resize. Separate
logical metadata renders them at 56 × 51 and 62 × 59 pixels inside one
84-pixel/60 cm bay; the room uses a 2× backing. Off and On are byte-identical.
Broken has the torn handle, open lid, displaced spout cap, crushed panel and
jagged metal rupture of the strong concept plus a support-pinned ±4.1° rattle,
steam, sparks and debris. The fridge, both cabinets and dishwasher remain
valid support surfaces with dynamic `make-cup-of-tea` stops. Broken locks
itself and its current support until repaired. V45 is unapproved, unpromoted
and unwired. Dishwasher V41, cabinetry, V42–V44, Final and runtime remain
unchanged. The later closed Kitchen Complete Review V44 now supplies separate
unapproved toaster and mixing-bowl candidates without changing this V45
contract.

Kitchen Kettle Bubble Authority V46 is preserved unapproved history. Frank
liked its broken handle but asked for less restrained damage and a fully
detached lid so steam could pour from the top. V47 is the approved immutable
visual authority at
`art/drafts/kitchen-kettle-bubble-authority-2026-10-22-v47/`. Off and On use
the approved Bubble `tea-kettle` V2 body pixel-for-pixel; the builder removes
only its one detached steam component and preserves that component separately.
The new Broken candidate is normalised to the same fixed flat palette and keeps
the failed left handle mount and right-attached handle, while adding a wholly
detached airborne lid, unobstructed open top, broad dent/cracks and larger
enamel loss. Exact V45 support slots, support plane, interaction,
Broken lock/rattle and six 40-frame/4-fps effect strips are hash-pinned or
copied byte-for-byte. A state-family sheet and exact-room Retina proof are
included. Only the Broken steam's asset-local x anchor moves so the unchanged
animation rises from the open top. Frank approved the exact V47 sheet on 22
October 2026. The approval is recorded externally and hash-pins every state,
effect and evidence image without rewriting the immutable pre-approval pack.
V47 remains unpromoted and unwired. V46 now supplies the separately reviewable
lid animation, configurable Broken vibration and replaceable SFX proof while
leaving V45, Bubble V2, runtime and production unchanged.

Kitchen Ligne-Claire Sweep V1 at
`/keeper-review/kitchen-ligne-claire-sweep-v1/` is a separate coordinated
style-only review gate and therefore does not continue or approve the earlier
asset-by-asset construction sequence. It supplies 53 geometry-locked candidate
files across twelve furniture/object families. The exact source canvas, alpha
bytes, alpha bounds, padding and registration are preserved for every file;
anchors, pivots, collisions, movement locks, support ownership, state machines,
healing, interactions and timing remain in the unchanged hash-pinned source
catalogues. Effect-only strips remain byte-identical; the two full-state oven
lighting strips are translated because they contain oven pixels. Complete
family and `772 × 224` Standard/Broken room contact sheets are present. The
recipe also records Frank's five supplied seascape panels as the future
flat-water, rhythmic-wave, rock-plane, weather-layer and boat-treatment
authority without adding exterior pixels to this kitchen gate. The candidate
is unapproved, unregistered, unpromoted and unwired, with a closed
registration guard and immediate directory-only rollback. Frank rejected V1 on
21 October 2026: canvas/alpha preservation alone did not keep every visible
internal shape legible, specifically the fridge worktop and oven depth. Recipe
and historical delivery:
`docs/KITCHEN_LIGNE_CLAIRE_ART_RECIPE_2026-10-21.md` and
`docs/KITCHEN_LIGNE_CLAIRE_SWEEP_V1_2026-10-21.md`.

Kitchen Cabinet Ligne-Claire V2 at
`/keeper-review/kitchen-cabinet-ligne-claire-v2/` is rejected immutable history.
Its narrow scope left the fridge worktop and sink cabinet outside the cabinet
palette, and its nearest-neighbour/CSS pixelated evidence introduced a false
jagged presentation. The rejection and exact V2 hashes are pinned at
`docs/review/kitchen-cabinet-ligne-claire-v2-rejection-2026-10-21.json`.

Kitchen Fitted-Cabinet Ligne-Claire V3 at
`/keeper-review/kitchen-fitted-cabinet-ligne-claire-v3/` is the approved
fitted-family visual authority. It includes eight Cabinet A/B variants, two fridge states, three
sink bases and five compositor healing layers. One shared material palette now
covers every fitted-family worktop, body and fixture while every exact source
interior line and semantic mask remains present. Smooth contact-sheet and web
interpolation replace V2's pixelated enlargement. V19/V37/V38/V41 catalogues,
verifiers, effects and the modular standard are byte-pinned, retaining exact
dimensions, anchors, movement locks, occupied-bay swaps and the 720-layout
healing process. Frank approved the exact static V3 evidence on 21 October
2026; the decision is
`docs/review/kitchen-fitted-cabinet-ligne-claire-v3-approval-2026-10-21.json`.
V3 remains unpromoted and unwired with immediate directory-only rollback. Delivery:
`docs/KITCHEN_FITTED_CABINET_LIGNE_CLAIRE_V3_2026-10-21.md`.

Kitchen Built-In State Ligne-Claire V4 at
`/keeper-review/kitchen-built-in-state-ligne-claire-v4-delivery-v3/` is rejected
immutable provenance from an attempted extension of the approved V3 treatment
to oven and dishwasher On/Broken states. Its seventeen
exact-alpha candidates include all eight dishwasher state/edge variants and
both complete 40-frame broken-oven light strips. Approved V3 fridge, sink,
cabinet and healing files are inherited byte-for-byte; the sink stays at its
existing canvas coordinates and room datum. All separate effects, timing,
movement locks, repair unlocks, ownership and 720-layout healing contracts are
unchanged. Frank rejected V4 because its direct low-resolution RGB remapping
lost sharpness, exaggerated pixel structure and misclassified the dishwasher
fascia into incorrect turquoise blocks. V4 was never registered, promoted or
wired. Rejection:
`docs/review/kitchen-built-in-state-ligne-claire-v4-rejection-2026-10-21.json`.
Delivery:
`docs/KITCHEN_BUILT_IN_STATE_LIGNE_CLAIRE_V4_2026-10-21.md`. The original V4
page is immutable but its external archive redirects did not display in the
review surface. Delivery V2 added same-origin responses but retained relative
image URLs that broke after Vercel removed the page's trailing slash; it remains
immutable failed-delivery provenance. Delivery V3 uses a new page, root-absolute
asset paths and SHA-256-verified same-origin responses for the exact same four
evidence objects. It changes no artwork or behavior. Correction:
`docs/KITCHEN_BUILT_IN_STATE_LIGNE_CLAIRE_V4_DELIVERY_V3_2026-10-21.md`.

Kitchen Built-In State Ligne-Claire V6 is rejected for replacing Frank's
preferred high-resolution oven with a scripted redraw. V7 recovered the exact
authority but its mapping is rejected because byte-exact reuse of the old alpha
trimmed the new top contour. Kitchen Oven Ligne-Claire V8 at
`/keeper-review/kitchen-oven-ligne-claire-v8/` retains the authority's own
complete contour and antialiasing inside the unchanged 92 × 85 canvas and exact
transparent bounds `(4,4)–(88,81)`. Frank approved exact V8 on 21 October 2026;
it is now the current hash-pinned Oven On visual authority. The immutable pack,
closed pre-approval register and V41 source remain byte-identical. Broken states
and the dishwasher are unpropagated; Final, runtime, dimensions, anchors,
movement, interaction, repair and healing remain unchanged. Approval:
`docs/review/kitchen-oven-ligne-claire-v8-approval-2026-10-21.json`; delivery:
`docs/KITCHEN_OVEN_LIGNE_CLAIRE_V8_2026-10-21.md`.

Kitchen Oven Broken Ligne-Claire V9 at
`/keeper-review/kitchen-oven-broken-ligne-claire-v9/` is the new immutable
Broken/flicker review gate. It derives all four Broken lighting states and both
40-frame/4-fps strips from one high-resolution V8-calibrated Broken drawing,
with exact `92 × 85` canvas, `(4,4)–(88,81)` outer padding and identical alpha
in every state/frame. Door glass remains translucent; the attached open door,
blackened roast, failed dial on two wires and warning lamp remain readable.
The V8 On candidate is byte-identical. An optional separate oven-anchored
`92 × 40` comic fault-symbol layer applies Frank's stars/spiral/burst references
without changing oven geometry and is independently removable on repair. V3
healing, exact oven/sink datums, movement locks, repair unlocks and every V41
dishwasher byte are pinned. V9 is unapproved, unregistered, unpromoted and
unwired; `batch-register.json` remains closed. Delivery:
`docs/KITCHEN_OVEN_BROKEN_LIGNE_CLAIRE_V9_2026-10-21.md`.

Kitchen Oven Broken Ligne-Claire V10 at
`/keeper-review/kitchen-oven-broken-ligne-claire-v10/` is the immutable
door-angle successor. Frank judged V9 excellent but preferred the Broken door
not completely open. V10 changes only that authorised visual detail: the same
attached door is now moderately part-open. The exact `92 × 85` canvas,
`(4,4)–(88,81)` alpha bounds, genuine glass transparency, V8 On bytes,
lighting-state geometry, 40-frame/4-fps schedules, room datums, movement and
repair contracts, V3 healing and every V41 dishwasher byte remain pinned. The
V9 symbol effect is reused byte-for-byte and remains independently removable
on repair. V9 is untouched; V10 is unapproved, unregistered, unpromoted and
unwired with its registration gate closed. Delivery:
`docs/KITCHEN_OVEN_BROKEN_LIGNE_CLAIRE_V10_2026-10-21.md`.

Kitchen Oven Broken Ligne-Claire V12 at
`/keeper-review/kitchen-oven-broken-ligne-claire-v12/` is the focused
family-match successor. It rebuilds Broken from the exact approved V8 On
authority rather than preserving V9/V10's globally different cabinet. Only the
failed third dial, burnt roast and shallow ajar-door cue are locally different;
the verifier requires zero pixel drift everywhere else and exact V8 alpha in
all static states and all 40-frame strips. V8, V9 and V10 remain untouched.
Frank approved the exact V12 family on 22 October 2026. Its hash-pinned
approval record changes no immutable pack, source, production or runtime byte;
the pre-approval register remains closed. Delivery:
`docs/KITCHEN_OVEN_BROKEN_LIGNE_CLAIRE_V12_2026-10-21.md`. Approval:
`docs/review/kitchen-oven-broken-ligne-claire-v12-approval-2026-10-22.json`.

Kitchen Oven Off Ligne-Claire V13 at
`/keeper-review/kitchen-oven-off-ligne-claire-v13/` supplies the missing intact
Off state. It starts from approved V8 On and removes only cavity and warning-
lamp illumination. The verifier requires exact V8 pixels everywhere outside
those two masks plus exact `92 × 85` canvas, alpha, `(4,4)–(88,81)` padding and
datum. Approved V8 On and approved V12 Broken are included byte-for-byte in the
family proof. V13 is an immutable, reversible, unregistered and unwired review
candidate behind a closed approval gate; no healing or gameplay behaviour
changed. Delivery: `docs/KITCHEN_OVEN_OFF_LIGNE_CLAIRE_V13_2026-10-22.md`.

Kitchen Oven Broken Ajar Ligne-Claire V15 at
`/keeper-review/kitchen-oven-broken-ajar-ligne-claire-v15/` corrects only the
approved V12 Broken door read. The body remains the exact approved family;
the attached bottom-hinged door uses the established moderate part-open
geometry within one declared local mask. V14 is preserved as rejected proof
because its glass read as a displaced handle. V15 retains exact `92 × 85`
alpha, all four fixed lighting states, both 40-frame/4-fps strips, datums,
separate symbols, dishwasher bytes and all movement, interaction, repair and
healing contracts. It is immutable, reversible, unregistered and unwired with
the approval gate closed. Delivery:
`docs/KITCHEN_OVEN_BROKEN_AJAR_LIGNE_CLAIRE_V15_2026-10-22.md`.

Kitchen Ligne-Claire Complete Review V45 at
`/keeper-review/kitchen-ligne-claire-complete-review-v45/index.html` is the immutable
closed kitchen-wide predecessor. It retains V44 byte-for-byte and contains 60
current/candidate object-state records, 16 effect records, 14 family contact
sheets and nine approved/current condiment V2 calibration references. Approved V3/V8/V12 authorities
remain preserved; V13 Off, V15 ajar Broken, the corrected-control-rail
dishwasher, table/chair, bin, toaster and bowl remain unapproved candidates.
V45's inherited kettle candidate remains unapproved historical evidence and is
superseded by the separately approved V47 Bubble kettle authority. Ten new
mask-locked knives, mills, preparation and tea candidates retain their current
256 × 256 alpha bytes exactly. V41 movement, swapping, Broken position locking,
repair unlocking,
asset-local effects and countertop healing are unchanged and mechanically
verified. Every route is root-absolute through the same-origin archive proxy.
No current selector, production asset, runtime, gameplay, collision or room
layout changed. Delivery:
`docs/KITCHEN_LIGNE_CLAIRE_COMPLETE_REVIEW_V45_2026-10-22.md`.

Kitchen Broken-Appliance Motion Workbench V46 at
`/keeper-review/kitchen-ligne-claire-complete-review-v46/index.html` is the
preserved motion/SFX predecessor. It replaces every selectable historical kettle
candidate with approved V47 Off/On/Broken art and exposes no alternative kettle.
Static pixels are unchanged. Presentation uses separate irregular whole-object
and optional component transform layers: V47's detached lid hovers/vibrates
independently while Broken steam remains anchored over the open top. The same
Off/Subtle/Emphatic whole-object contract is demonstrated on the dishwasher.
An independent, default-off SFX control plays an intermittent metal-rattle
placeholder; dropping an audio file onto its slot or using the file picker
replaces it for that browser session without touching canonical audio. Repair
synchronously zeros transforms, cancels timers, stops active nodes and releases
the V41 movement lock. Frank approved the exact kettle motion/SFX presentation
on 22 October 2026; the dishwasher remains only a reusable demonstration.
Nothing is promoted or wired. The game-wide asset-state SFX implementation is deliberately handed
to Claude in
`docs/prompts/CLAUDE_GAME_WIDE_ASSET_STATE_SFX_SLOTS_2026-10-22.md`. Delivery:
`docs/KITCHEN_BROKEN_MOTION_WORKBENCH_V46_2026-10-22.md`.

Kitchen Ligne-Claire Complete Review V60 remains immutable superseded evidence
at `/keeper-review/kitchen-ligne-claire-complete-review-v60/index.html`. It retains the approved Kettle V47 art and V46
motion/SFX behaviour. The kettle remains anchored to Cabinet A rather than
independently movable and is presented approximately 20% smaller, centred on
the same bay x42 and seated on the same y141 support plane; approved source
bytes are unchanged. Cabinet V11 remains the fitted-carcase authority for
both appliances: its worktop, blue shell geometry/colours and plinth surround
the Dishwasher V8 and approved-oven inserts. Cupboard-only hinges/knobs are
excluded from those appliance shells. The oven's old separate glossy blue slab
is excluded, its approved hob/control/cavity art remains, and its controls now
share the dishwasher's room-height baseline. Closed dishwasher states stop
above the exact common plinth; the failed Broken door may hang in front of it.
All adjacencies use the same flat cabinet join. The healer's former light first
cap row is replaced in all foreground masks by a composite-matched dark row, so
the rear worktop line crosses every placement boundary without interruption.
Registration remains closed; the smaller kettle registration and inherited V59
fitted-carcase integration are unapproved. Source/production art, state semantics,
motion, sound, repair locking, room layout, collision and gameplay remain unchanged.
Delivery: `docs/KITCHEN_DISHWASHER_LIGNE_CLAIRE_V8_2026-10-22.md` and
`docs/KITCHEN_LIGNE_CLAIRE_COMPLETE_REVIEW_V59_2026-10-22.md` and
`docs/KITCHEN_LIGNE_CLAIRE_COMPLETE_REVIEW_V60_2026-10-22.md`.

The active kitchen art programme is High-resolution Foundation V1. The original
style page remains immutable at
`/keeper-review/kitchen-high-resolution-foundation-v1/index.html`. Its sole
primary composition view is the byte-exact `2203 × 714` first fitted-run render
`exec-b28bb76f-bdd9-4d95-bae6-4d25ab665468.png`, selected for its centred,
rear-set sink, coherent fitted-set relationships and retained detail under
zoom. It is also the kitchen style exemplar: retain its warmth and restrained
three-dimensional modelling, with an adult cinematic ligne-claire tone rather
than the later `exec-036d9986-abce-4f47-9e6a-2896bc245f8e.png` exploration's
harsh schematic flatness. Later state atlases are diagnostic history only. The
selected image is not a crop-ready sprite sheet: the basic fridge remains
undercounter, game geometry and anchors stay fixed, and production assets must
avoid cute, juvenile, toy-like or candy-gloss treatment. Approved Kettle V47
art/motion, runtime assets and state behaviour remain unchanged.

Frank approved the exact coordinated six-module cabinetry construction sheet
on 22 October 2026. Its `1536 × 1024` RGBA bytes are preserved at
`art/source/kitchen-cabinetry-foundation-2026-10-22-v1/cabinetry-module-construction-sheet-approved.png`
with SHA-256
`898c212690c2db8a52a6c8ea7bd962afcf12c1df8e577dcc98c4508359cccee3`.
Cupboard, drawers, sink, dishwasher, oven and basic undercounter fridge are now
the approved fitted-family visual/body foundation. Production extraction,
transparent crops, Off/On/Broken layers and runtime registration are not yet
approved. Future states must reuse the exact bodies and change only named
doors, contents, indicator and effect layers; loose countertop objects follow
later. The external approval record is
`docs/review/kitchen-cabinetry-foundation-v1-approval-2026-10-22.json`.
The current `/keeper-review/kitchen` route now opens the fresh immutable
`/keeper-review/kitchen-cabinetry-foundation-v1/index.html` page, which decodes
and presents the approved construction sheet and original authority together.
Contract and delivery:
`docs/KITCHEN_HIGH_RESOLUTION_FOUNDATION_V1_2026-10-22.md`.

Kitchen Cabinetry State Derivatives V1 is the approved fitted-state visual
authority at `/keeper-review/kitchen-cabinetry-state-derivatives-v1/index.html`.
Frank confirmed the exact V4 sheet on 22 October 2026. It pairs Sink On/Broken,
Dishwasher On/Broken, Oven Off/Broken and Fridge standard/Broken beside the
approved body authority. Confirmed state closure also defines Dishwasher Off as
three dark fixed housings, On as three steady green lamps and Broken as three
independently irregular red blink layers. Broken uses the full lower dishwasher
hinge, the selected sagging fridge door and a separate small fridge leak. The
sheet is not a production atlas: transparent extraction, animation,
native-scale proof and runtime remain closed. Approval record:
`docs/review/kitchen-cabinetry-state-derivatives-v1-approval-2026-10-22.json`.
Delivery: `docs/KITCHEN_CABINETRY_STATE_DERIVATIVES_V1_2026-10-22.md`.

Kitchen Cabinetry Room Layout V1 is the active room-fit review at
`/keeper-review/kitchen-cabinetry-room-layout-v1/index.html`. Fourteen
transparent review crops come only from the exact approved cabinetry foundation
and V4 state authority. All six units drag-and-swap between the fixed `84`-pixel
bays; layout, state and zoom persist; Broken appliances cannot move or be
displaced until repaired. Raw and narrow join-only canvases remain synchronized
at `1×`, `2×` and `4×`, rendered from the high-resolution crops without a `1×`
intermediate. Dishwasher Off is intentionally absent until its approved dark
lamp semantics are authored as a separable high-resolution layer. The crop
masks, join diagnostic, production registration and runtime remain unapproved
and unchanged. Delivery:
`docs/KITCHEN_CABINETRY_ROOM_LAYOUT_V1_2026-10-22.md`.

Kitchen Complete Room Layout V2 is now the active complete-room visual gate at
`/keeper-review/kitchen-complete-room-layout-v2`. It preserves all V1 cabinetry
and fitted states byte-for-byte while adding toaster, kettle, bin, table and
chair from one coordinated high-resolution source. The five are independently
movable on fixed worktop/floor support planes; the table is 14.5 lp high and
the chair seat is exactly 7.75 lp above the floor. Both join comparisons and
direct-source `1×`/`2×`/`4×` zoom remain available. Loose-object art, state
derivatives and runtime promotion remain closed; approved Kettle V47 and
existing behaviour are unchanged. Delivery:
`docs/KITCHEN_COMPLETE_ROOM_LAYOUT_V2_2026-10-22.md`.

The active contextual reviewer is now Prime Context Workbench V15. It retains
all eleven Workbench V11 choices and replaces only the active side-right sitting
link with V6. The animation remains the exact V1/V2 six-pose motion inside its
complete approved walk/stop/action/return context. V6 retains V5's corrected
horizontal chair registration: the backrest front meets the visible back/spine
contact and the front rim ends 0.5 px behind the rear shin plane. It replaces
the rejected 11-px plane—which crossed the pelvis—with a measured support top
at source y=258 / world y=44.25, 7.75 px above the floor. Frank approved exact
V6 on 17 October 2026, pinned by
`docs/review/keeper-prime-sit-stand-side-v6-approval-2026-10-17.json`. V1–V5
are immutable history. Frank then separately approved exact side-left V1,
pinned by
`docs/review/keeper-prime-sit-stand-side-left-v1-approval-2026-10-17.json`.
Neither decision performs a runtime, Final or production promotion.

Frank rejected front-facing V1 because sit→stand frames 2/3 widened beyond
Prime canon. Its immutable decision is
`docs/review/keeper-prime-sit-stand-front-v1-rejection-2026-10-17.json`.
Frank rejected V2 because complete-context frames 29 and 30 exposed the
remaining 167→158 px F3→F4 width snap; preserve
`docs/review/keeper-prime-sit-stand-front-v2-rejection-2026-10-17.json`.
Frank rejected V3 because complete-context frames 28–32 still narrowed
elbow-to-elbow 157→156→153→149→143 px. Preserve its exact decision and hashes
at `docs/review/keeper-prime-sit-stand-front-v3-rejection-2026-10-18.json`.
Frank approved exact front-facing V4 on 18 October 2026; preserve
`docs/review/keeper-prime-sit-stand-front-v4-approval-2026-10-18.json`. Its
exact F1/F6 endpoints, 143 px lowering width and complete 59-frame route remain
unpromoted.

Back-facing V1 remains immutable but is rejected: complete-context frames
29–41 visibly darken the jumper and trousers. The exact feedback and V1 hashes
are pinned in
`docs/review/keeper-prime-sit-stand-back-v1-rejection-2026-10-18.json`.
Frank approved exact back-facing V2 on 18 October 2026. Its hash-pinned record
is `docs/review/keeper-prime-sit-stand-back-v2-approval-2026-10-18.json`. It
retains every V1 alpha plane, dimension and all 61 route frames,
including exact approved Turn V9, the separate foreground chair back, sitting,
standing, turning and walking away. F2–F6 now take jumper/trouser RGB samples
from the exact approved rear endpoint. Direct central-region checks read
jumper 94–95 versus Prime 95 and trousers 77–78 versus Prime 77. F2–F6 retain
the 150 px seated elbow width. Back V2's approval does not cover either
rear-angle transition; Final/runtime/production remain unchanged.

Prime `keeper_sweep_broom` V1–V8 are rejected immutable provenance. V8 is
formally rejected at
`docs/review/keeper-prime-sweep-broom-v8-rejection-2026-10-19.json`: it showed
four arms after the held pose was added, broke up through the turn, introduced
pixelation and did not remain visually identical to approved Prime walk art.
The broomless `/keeper-review/keeper-prime-upper-body-override-poc-v3/` is the
approved motion-feasibility foundation for reusable `hold_shaft_two_hand`:
eight alternating gait phases, nine approved turn angles, no more than two
visible hands and zero prop pixels. It is explicitly a phase-matched
full-character proxy rather than pixel-identical production art. Frank approved
its held-implement motion feasibility on 19 October 2026. The hash-pinned decision is
`docs/review/keeper-prime-upper-body-override-poc-v3-approval-2026-10-19.json`.

The active artwork gate is now
`/keeper-review/keeper-prime-hold-shaft-two-hand-layered-v1/`, the first
immutable separable Prime build. Its 17 orientation records and 33-frame route
preserve POC V3 exactly. Declared visible Walk V6/Turn V9 lower-body authority
pixels are byte-identical and live on their own planes; unavailable trouser
pixels formerly hidden by the swinging hand are isolated in a reversible,
explicitly non-authority occlusion-fill plane. Torso/head and held arms are
separate, non-overlapping hash-pinned planes and use only matching Prime
authority colours. The candidate awaits Frank's visual decision. The proxy
artwork, layered V1 artwork, broom and other implements, runtime, Final and
production remain unapproved, unchanged and unwired.

Layered V1 delivery is committed and pushed to remote `main`: candidate
`6fbf0720`, immutable shell pin `68e9b0d0`. No `[deploy]` commit was created,
because this task explicitly prohibited production promotion. The versioned
review route therefore remains repository-ready but is not yet live on the
production site. Its dedicated verifier, typecheck and production build pass;
the complete clean-tree suite reaches only the already-documented public-payload
guard (50.44 MiB against 50 MiB), unrelated to the 1.04 KiB pinned shell.

Held-implement POC V1 remains immutable. Frank described its motion as a very
valuable POC and identified a lateral leap at frames 17→18. V2 preserves every
V1 frame, route root and duration byte-for-byte while correcting only the
reviewer's horizontal-mirror anchor: the 18.75-lp source root becomes 29.25 lp
inside the mirrored 48-lp cell, removing the artificial 10.5-lp displacement.
That V1 feedback remains provenance; Frank's later formal approval applies to
the corrected V3 motion-feasibility POC only.

Held-implement POC V2 delivery is live: candidate `aa833925`, shell pin
`1c06451c`, review-only deploy `04edb860`. The production URL returned HTTP
200 with the shell pinned to `aa833925`; the live reviewer contained the
mirror-aware anchor formula and all 87 unique frame/comparison URLs returned
valid PNG signatures on 19 October 2026. Both POC verifiers, TypeScript and the
production build pass. The complete repository suite reaches the independent
50 MiB public-payload gate at 50.41 MiB after unrelated kitchen review work;
V2 adds only its 1,016-byte shell and no public image media.

Frank then reported that V2 still jumped at frames 17→18 and that the walk read
as walking on the spot. The remaining seam was not root drift: the planted
root was stable, but the generated proxy's full-silhouette centroid moved
1.333 lp at the rear crossing. V3 gives only playback frame 18 a reversible
one-lp presentation registration, reducing the adjacent centroid changes to
+0.333/-0.408 lp. It also replaces the reviewer's modulo loop with one-shot
playback, so the exact standard 2.625-lp-per-frame walk stops after advancing
21 lp instead of snapping back to its starting coordinate. No pixels, gait or
turn order, durations, Final, runtime or production assets change.

Held-implement POC V3 delivery is live: candidate `dedf5af5`, shell pin
`6e4b8d4c`, review-only deploy `ebc362c9`. The production shell returned HTTP
200 pinned to the exact candidate; the live reviewer contains one-shot playback
and the frame-18 registration, and all 87 unique PNG URLs passed signature
checks on 19 October 2026. Dedicated V1/V2/V3 verification, TypeScript and the
production build pass. The later approval verifier also hash-checks the exact
17 frames, 33-frame route and boundary. The complete repository suite reaches the independent
public-payload ceiling at 50.41 MiB versus 50 MiB after concurrent kitchen
review additions. V3 adds no image media and only its 1,016-byte public shell.

Back V1's exact deploy commit `d93c89c` remains delivery provenance only. Back
V2 is live from exact deploy commit `f165576`; its 61-frame route and all 36
unique route/comparison images returned valid PNG data on 18 October 2026.
Live delivery is not approval or promotion.

The next verification-infrastructure priority is the bank-wide per-frame colour
gate specified in
`docs/prompts/KEEPER_PRIME_ALL_FRAME_COLOUR_VERIFICATION.md`. It must select
hash-pinned authorities by outfit/facing/component, use disjoint semantic masks
and pose-relative invariant material regions, compare adjacent frames, and fail
closed when evidence is missing. Rejected Back V1 must fail and corrected Back
V2 must pass. The specification exists; the bank-wide verifier has not yet been
implemented and no artwork change is authorised by it.

1. The evidence-based beard/hand audit classifies every manifest frame and pins `keeper_clear_snow` as the canonical fuller stepped beard. A landmark-aligned beard-mask comparison passes with a symmetric silhouette difference of at most one logical pixel. It remains fail-closed for unavailable evidence: 163 side-on standing/sitting sheets are inventoried, eight zero-difference reference self-comparisons match, and 994 different-pose frames—including `keeper_darts` 3–6—are non-comparable because no approved beard masks, facial landmarks or hand-depth/component evidence exists. Frank reviewed Darts 3–6 visually on 11 October and accepted the beards with no amendment required; no beard draft is active or promotable. Next, use GPT-5.6 Sol to establish comparison inputs for any future claim, then run the later frame-isolation and released-prop audits.
2. Continue the neutral-endpoint repair queue in `docs/KEEPER_NEUTRAL_ENDPOINT_AUDIT.md`: standard outfit first, then one outfit at a time in `docs/KEEPER_COSTUME_ROUTE_AUDIT.md` order. The five studio samples are the early visual gate; the specialised hot-drink prop-state bridges are their remaining seam work. Frank's immutable second visual review recorded 96 of 173 animations Happy, 68 Awaiting new draft review, 3 Review later and 6 Unreviewed; the current reviewer has 97 Happy and 67 Awaiting after Frank selected the Darts draft as his preferred candidate. Frank's saved per-animation width and height remain final production art direction.
   The complete internally consistent V11 artist-smock family is now preserved
   as seven active authored-animation comparisons plus eight deterministic
   technical neutral/bridge assets. Its front-turn final frame is byte-identical
   to the preferred front-sit first frame. Production remains unchanged until
   Frank selects the exact-name candidates in the reviewer. A later
   canonical-identity snooker route was visually accepted and is now an active
   exact-name `keeper_snooker` comparison: walk right, exact stop, acquire the
   cue, play two strokes, release it, return to exact neutral, turn and walk
   left. The production eight-frame snooker strip remains unchanged pending
   Frank's separate platform verdict.
3. Art for the mission floors (aquarium, weather station, hidden lair), their furniture, the lift and a floor-arrival effect (Codex; hooks in docs/FOR_CODEX.md).
4. Tier art for upgrades (Codex; list in docs/FOR_CODEX.md). Typed commands for upgrading ("upgrade the TV") are not in yet; upgrades are bought from the tap menu.
5. Mini games: fishing, cooking, telescope spotting.
6. Day/night palette, non-skippable ~30s night recap.
7. Replace the temporary on-island shop fallback with an early off-island unlock and boat travel through an indoor water-filled boathouse/dry dock. Boat tiers: rowing boat, tug, speedboat. The external shop never breaks; the keeper's boathouse, jetty and boat may.
8. Workshop floor that reduces breakdown pressure; tune its effect only after Ralph's playtesting shows whether faults are fun or irritating.

## Housekeeping for Frank
- Change the grown-ups PIN from 1234.
- Add Ralph and Eddie on the Who is playing screen (none exist yet).

## Verification and delivery

The review-payload housekeeping pass completed on 21 October 2026. The exact
clean-checkout baseline failed at 53.3148 MiB; the content-addressed sweep now
archives every review image plus JSON/JSON.GZ at or above 24 KiB, leaving HTML
and small JSON public. After Kitchen Complete Review V60, 245 set manifests
resolve 7,526 references to 3,217 immutable objects;
6,095 literal page references resolve and `public/` is 49.49
MiB, 0.51 MiB below the unchanged 50 MiB guard. Runtime
`public/sprites` is now 40.1033 MiB, including the 27 versioned Prime sheets.
Use `npm run maintain:keeper-review` after any review builder; it archives,
verifies object and manifest hashes, checks historical URL resolution and then
checks the deployment payload. Repository size, `review-archive/` and
`art/drafts/` are not part of that payload measurement.

### Separate Draft/Final animation workbench

The Keeper Animation Workbench is deployed separately from the established
reviewer at `/animation-workbench`. Its Final and active Draft lanes are both
currently empty. Prime front, Side-right V1, V5 back, front ↔ side Turn V1,
side-right ↔ back Turn V9, Walk V6 and stop ↔ walk are approved artwork
authorities. Walk → stop → turn to camera also has approved Fast Timing V1 for
its transition phases. The approved front ↔ side turn carries one accepted
slight 45° cadence limitation.
Its shared architecture still
supports immutable repository-backed Final items and browser-local,
JSON-exportable Draft recipes that can copy, remove and reorder source-frame references, loop
the whole preview and repeat selected contiguous sections without modifying any
PNG. Every animation has a required ingress player: walk, stop, optional front
or back turn, then action. Closed doors may hide a costume swap but never exempt
the resulting action. The game engine deterministically extends only the walk,
using the Keeper and target asset's world placement. It starts that cycle while
the Keeper is hidden behind the departure door, so the first visible state is
already mid-stride. The ingress player simulates the matching door-side reveal.

Frank's earlier V2 approval is retained as historical provenance, but those
strips no longer seed Final after the visible pixel-density/model jump was
rejected. Raw art, runtime sprites and the runtime manifest are unchanged.
The permanently approved smooth master is at
`/keeper-review/keeper-prime-master-v1/`; the approved rear endpoint is at
`/keeper-review/keeper-prime-orthographic-v5/`, linking back to the V3 side
registration audit and immutable V2 predecessor.
The construction contract is separately reviewable at
`/keeper-review/keeper-prime-rig-v1/`; its current construction-motion revision
is at `/keeper-review/keeper-prime-rig-v3/` and V2 remains immutable provenance.
The exact Motion V3 approval is pinned in
`art/drafts/keeper-prime-construction-rig-2026-10-13-v4/`.
Architecture, limitations and extension points are in
`docs/KEEPER_ANIMATION_WORKBENCH.md`; the deterministic gate is
`npm run verify:keeper-animation-workbench`.

The reusable artwork method, failed approaches, continuity standards, exact
accepted references and future review-platform workflow are consolidated in
`docs/KEEPER_ARTWORK_AUTHORING_AND_REVIEW_PLAYBOOK.md`. Future correction scope
comes only from Frank's exact-name platform handoffs.

The keeper review batch is 191 sheets / 1,479 frames. The rejected second-round
production pass remains historical evidence after its rollback from commit
`131191c`. Separately, ten exact-name source selections (including the
dependent parachute-landing bridge) were promoted after final-strip inspection;
the online reviewer shows each former canonical strip as `Previous version`.
The original darts selection remains an unpromoted comparison draft. Current
delivery also includes seven reversible V11 artist-smock comparisons and one
reversible complete-route `keeper_snooker` comparison; the artist family's
eight derived neutral/bridge assets remain outside the review-gallery denominator.
Current review evidence is recorded in
`docs/review/KEEPER_ANIMATION_REVIEW_RESOLUTION_2026-10-10.md`.
