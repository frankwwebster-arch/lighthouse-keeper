# Lighthouse Keeper: status write-up (26 Oct 2026)

## What it is
A Sims-style web game for Ralph (7) and Eddie (11). A keeper lives in a lighthouse; kids type commands (typo-tolerant, curated, no live AI) or click objects (Sims-style menus, auto-zoom camera). Needs and mood, credits, phone, bedtime, multi-day play, a day report, quiz pop-ins, time-aware chat, cheeky humour.

## Where it lives
- Code: github.com/frankwwebster-arch/lighthouse-keeper (branch `main`).
- Live: **https://lighthouse-keeper-mu.vercel.app** (the one address to use and bookmark).
- Vercel project `lighthouse-keeper` (team frankwwebster-4308s-projects). Pushes do not deploy; only a `[deploy]` commit on `main` builds production (`npm run deploy`, or the GitHub Actions "Deploy to production" button). See `docs/DEPLOYMENT.md`.
- The long addresses like `lighthouse-keeper-di4axnjgx-...vercel.app` are one-off links for a single deploy. Ignore them; they are also login-protected.
- Database: Neon Postgres via `DATABASE_URL` (verified: `/api/players` answers `db:true`). Tables are created on first use: players, saves, player_rules, settings (PIN hash).

## Built

The current target graphics authority is `docs/CODEX_BRIEF.md`: Codex-authored,
non-pixel, bright flat 2D illustration on a strict orthographic side elevation;
a straight-sided tower; exact 1536 × 512 master-derived room modules; pure
`#FF00FF` see-through areas; and separate minimal-state item masters. The new
tower kit and `/public/art/keeper/canon/` migration have not been built. Existing
approved/runtime art remains immutable until those migrations receive their own
review and approval.

The required new-art delivery pipeline has not been built either. The legacy
`npm run sprites` path removes `#FF00FF`, so it must not process the only copy
of a tower, island or environment master. A reviewed source/runtime boundary
that retains and verifies exact magenta is a prerequisite to producing the new
tower kit.

The former reproducible local Makko handoff remains a historical snapshot only:
`makko-approved-art-2026-10-25/`. Makko is no longer used. The snapshot contains
27 promoted Prime sprite sheets,
all 14 approved playable Prime routes, the ten approved V12 sequences, the
ten earlier Frank-selected canonical legacy sheets kept in their own section,
the approved kitchen V4 native master and locked fitted run, 84 explicitly approved
current activity-story pictures, the original concept references and the first
production environment batch. Rejected/superseded work and unapproved kitchen
or Keeper candidates are excluded. `npm run export:makko` rebuilds the ignored
binary folder; `npm run verify:makko-export` checks every exported and source
SHA-256 against its generated manifest.

Lighthouse Pixel Style Test V4 is preserved at
`public/art/concepts/pixel/` as rejected historical evidence. Frank rejected
the 8-bit/16-bit direction as too blocky when zoomed in; its tapered tower,
small modules and omitted en-suite are also superseded by the straight-sided
1536 × 512 production brief. It changed no canon or runtime art. See
`docs/LIGHTHOUSE_PIXEL_STYLE_TEST_2026-10-26.md`.

The approved installed legacy kitchen art/geometry authority is Warm
Ligne-Claire Family V4, and Runtime Promotion V1 is now wired into the room
code. All six fitted bodies
remain exact 84 × 74 assets in the approved 772 × 224 coordinate system. The
current fixed-width floor applies one uniform outer transform. Cooker drives
the Oven Off/On/Broken art and its cavity-light-only Broken loop; Fridge drives
the matching V4 states. The Dishwasher light loop is installed but remains
inactive until a gameplay Dishwasher exists. The prior room plate is retained
and hash-pinned for rollback. Full source, state and reversible-promotion
contracts are in `docs/KITCHEN_ASSET_AUTHORITY.md` and
`data/kitchen_runtime_promotion_v1.json`. The 158 earlier formal room/furniture
drafts remain retired. This authority preserves the live and rollback bytes;
it does not govern future module or item art, which now follows the 1536 × 512
and 96/192 px rules in `docs/CODEX_BRIEF.md`.
Engine (seeded, deterministic, 122 tests), SVG cutaway scene with zoom camera, typo matcher, quizzes levels 1-3, credit economy with admin dials (allowance from per-need green bars, prices, gifting, quiz level and breakdown pressure per player), who-is-playing screen, per-player saves (DB or localStorage), grown-ups PIN (starts 1234; change it).

The first three playable floors are now modular fixed-width components: kitchen, living room, and bedroom with en suite. Objects have a runtime `standard` / `on` / `broken` contract, state-specific strip support, shared broken effects, keyboard/touch hit areas, and rear-facing cooker/basin keeper fallbacks. Random keeper-owned breakdowns are off by default and controlled by grown-ups' frequency and maximum-concurrent dials; broken assets block normal use until repaired. Floor 3 reserves an invisible two-door changing zone for the later diving-board extension.

Missions (`src/game/missions.ts`, list in `config.ts`) are all open at once and count in parallel, so floors arrive in any order: Fishy Business → aquarium, Storm Chaser → weather station, Strange Rumblings (a mystery until he makes a start) → hidden lair underground, and Puffed Out → lift (opens once the tower has 5 floors). Goals count things he already does (fishing, nature channel, telescope, ships kept safe, digging, visitors, quiz answers, good days). A finished mission pays credits (10 by default) at once; its floor is built overnight and appears the next morning, furnished (one new floor a morning; the lift goes in at once). Each new floor takes a random middle place, saved for good: kitchen always at the bottom, bedroom always directly under the lamp room, lair below ground. The view zooms out to fit. In the current design both stairs and lift are hidden behind the room entrance; the lift replaces the hidden stair journey and changes only the jamb treatment, not the visible room grid. The live build still shows its older stair/lift stand-ins pending that circulation refactor. 🎯 Mission button shows progress; grown-ups set an overall mission size (% of normal) and reward, then can override any single goal or reward, and can finish any open mission. Typing about a floor he has not got gets a hint. `?floors=all` previews every floor. New floors and furniture are stand-ins until Codex's art (hooks in docs/FOR_CODEX.md).

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

V40 is rejected because its oven was too tall/insufficiently wide and its
smoke rose as bubbles. V41's exact-size local correction and the broader
asset-by-asset replacement method are also rejected. V32–V41 remain immutable,
unpromoted evidence; V39's earlier fridge approval is historical rather than
the current construction authority.

Rebuild V1 established the accepted coherent room/cabinet/table construction:
exact `772 × 224` room, six equal `84-px` bays at x=84–588, y=134 worktop,
y=151 fascia and y=208 foot line. Frank called it excellent subject to changing
the fridge door to white.

Layout V12's room registration and white-goods envelopes were approved, but
its proposed sink overlay was immediately superseded. The sink must not sit on
an existing cabinet. V13 established one complete independent 84 × 74 px sink
cabinet with its own worktop, basin and intact tap, but its perspective is
rejected because it does not match approved V11. V14's On stream is also
rejected in registration because it begins a few pixels below the outlet. Its
Broken upward-basin-spout animation is approved and retained. Both older routes
remain immutable.

Cabinet Join Backfill V21 remains immutable predecessor evidence: its blue
body mask concealed the cream wall slit, but the two sprites' overlapping
softened worktop end contours still made a jagged double-width seam.

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

1. Install Frank-approved Keeper references at `/public/art/keeper/canon/` before any new Keeper pose is authored. The current Prime bank remains immutable and must not be silently relabelled: its stripe geometry, palette and source scale do not match the new absolute brief.
2. Establish an exact-magenta-preserving source/runtime delivery path, then build the native non-pixel modular tower kit from `docs/CODEX_BRIEF.md`: one 1536 × 512 master module, recoloured room variants, straight shell walls, dividers, gallery/cap pieces, empty magenta lantern and code-assembled 4 × 1 / 3 × 2 proof previews. The legacy `npm run sprites` cleanup route is not valid for these masters. Do not start room items until their base/upgraded bay plan fits all 13 bays.
3. The evidence-based beard/hand audit classifies every manifest frame and pins `keeper_clear_snow` as the canonical fuller stepped beard. A landmark-aligned beard-mask comparison passes with a symmetric silhouette difference of at most one logical pixel. It remains fail-closed for unavailable evidence: 163 side-on standing/sitting sheets are inventoried, eight zero-difference reference self-comparisons match, and 994 different-pose frames—including `keeper_darts` 3–6—are non-comparable because no approved beard masks, facial landmarks or hand-depth/component ownership evidence exists. Frank reviewed Darts 3–6 visually on 11 October and accepted the beards with no amendment required; no beard draft is active or promotable. Next, use GPT-5.6 Sol to establish comparison inputs for any future claim, then run the later frame-isolation and released-prop audits.
4. Preserve the historical neutral-endpoint repair queue in `docs/KEEPER_NEUTRAL_ENDPOINT_AUDIT.md`, but do not continue it while the new Keeper canon gate is unresolved. After Frank-approved references populate `/public/art/keeper/canon/`, a reviewed migration must decide whether each Prime-era repair remains applicable before any draft is created. Frank's immutable second visual review recorded 96 of 173 animations Happy, 68 Awaiting new draft review, 3 Review later and 6 Unreviewed; the current reviewer has 97 Happy and 67 Awaiting after Frank selected the Darts draft as his preferred candidate.
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
5. Art for the mission floors (aquarium, weather station, hidden lair), their furniture, the lift and a floor-arrival effect (Codex; hooks in docs/FOR_CODEX.md).
6. Tier art for upgrades (Codex; list in docs/FOR_CODEX.md). Typed commands for upgrading ("upgrade the TV") are not in yet; upgrades are bought from the tap menu.
7. Mini games: fishing, cooking, telescope spotting.
8. Day/night palette, non-skippable ~30s night recap.
9. Replace the temporary on-island shop fallback with an early off-island unlock and boat travel through an indoor water-filled boathouse/dry dock. Boat tiers: rowing boat, tug, speedboat. The external shop never breaks; the keeper's boathouse, jetty and boat may.
10. Workshop floor that reduces breakdown pressure; tune its effect only after Ralph's playtesting shows whether faults are fun or irritating.

## Housekeeping for Frank
- Change the grown-ups PIN from 1234.
- Add Ralph and Eddie on the Who is playing screen (none exist yet).

## Verification and delivery

The review-payload housekeeping pass was refreshed for Lighthouse Pixel Style
Test V4 on 26 October 2026. The content-addressed sweep archives every review
image plus JSON/JSON.GZ at or above 24 KiB, leaving HTML and small JSON public.
The current index has 152 set manifests resolving 4,504 references to 2,452
immutable objects; 5,484 literal page references resolve and `public/` is
48.87 MiB, below the unchanged 50 MiB guard. Runtime `public/sprites` is
40.2859 MiB, including the 27 versioned Prime sheets.
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
