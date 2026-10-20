# Lighthouse Keeper: status write-up (20 Oct 2026)

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
No Prime artwork has entered Workbench Final or production, and the runtime
sprite manifest remains unchanged.

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

Kitchen Modular Fridge Workbenches V34 and V35 are rejected immutable
provenance. V34 used obsolete registration, a heavy dark contour and incomplete
join handling. V35 corrected placement and joins but reversed the Broken hinge
side and changed the apparent door dimensions. The active successor is V36 at
`/keeper-review/kitchen-modular-fridge-workbench-v36/`. It uses a coordinated
thin-navy-outline family: both states are left-hinged, and Broken rigidly rotates
the literal `68 × 52 px` Standard door at scale `1:1` around the surviving
lower-left hinge. The opposite lower corner reaches the floor and total
horizontal overflow stays within four pixels. The body remains exactly
`84 × 74 px` at y=134–208. All three movable assets still snap collision-free
to distinct free origins and preserve exact Prime midpoint anchors on y=218.
Oven pairs retain V32 triangular healing; every other fridge adjacency receives
the V22 blue backfill and exact countertop cap. The 40-frame/4-fps ten-second
drip/ripple remains separate, removable and variable-speed. All 24 layouts are
verified. V36 awaits visual review and changes no Final or runtime asset.

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

The production Next.js build and the focused Modular V10 verifier pass. The
full repository suite currently stops only at the pre-existing review-payload
budget check: `public/` is 50.42 MiB against its 50 MiB target. Review media is
correctly content-addressed outside `public/`; a later housekeeping pass must
recover the remaining 0.42 MiB without deleting active review evidence.

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
