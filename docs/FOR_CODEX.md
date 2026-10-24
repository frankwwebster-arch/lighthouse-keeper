# Notes for Codex from Claude (integration hooks)

## Bubble stories platform (20 Oct 2026)

Frank has moved bubble-story motion to Claude; Codex keeps the pictures,
symbols and Keeper. Pictures now go into the shared library with
`npm run activity-stories:add-picture` (new versions only, never in place).
Formats: `data/activity-stories/README.md`. Brief and first requests (redraw
three V7 symbols, add `symbol-clean-glint`):
`docs/CLAUDE_TO_CODEX_BUBBLE_STORIES_2026-10-20.md`.

The first symbol request is complete (21 October 2026): heat shimmer,
pleasant aroma and welding sparks are current V2 pictures, and clean glint is a
new current V1 `clean` mark. The immutable authoring pack is
`art/drafts/activity-story-symbol-redraws-2026-10-21-v1/`; the studio picture
list exposes all four while retaining the earlier versions for undo.

The picture-library completeness correction is also finished (21 October
2026). `pictures.json` now has 305 selectable pictures and 374 immutable
versions and includes all 298
review-ready isolated source components from Activity Cloud Composer V1–V7,
the rear-work V2/V3 callout vocabulary and every component-bearing Claude or
Codex picture pack: all V5 album artwork, the aquarium and bedroom sets, and
the 54-picture fishing, gardening, pet-play, fixing, pub, art and inventing
expansion. Reconcile from the immutable packs
with `node scripts/import_activity_story_picture_catalogue.mjs`;
`npm run verify:activity-stories` enforces that complete source set as well as
the original inherited marks.

Frank selected an original ligne-claire-inspired direction on 21 October:
near-black even ink, flat spot colour, no glossy/painterly modelling, and a
style translation that preserves the exact content and broad composition of
each current picture. Frank approved the first six-picture BBQ pilot, and its
six drawings are registered as new current versions in `pictures.json`; inspect
`art/drafts/activity-story-ligne-claire-bbq-pilot-2026-10-21-v1/evidence/current-vs-ligne-claire-contact-sheet.png`.
The ready-to-paste family-by-family continuation prompt is
`docs/CODEX_PROMPT_BUBBLE_STORIES_LIGNE_CLAIRE_ACTION_IMAGERY_2026-10-21.md`.
Activity stories should use a stable opaque rounded-rectangle panel; emotion
balloons may vary their contour; immediate reaction/motion marks may appear
unenclosed around the Keeper or object. Claude still owns the engine/panel
implementation under `src/activityStories/`; Codex owns the picture art.

Frank approved the first continuation gate on 21 October 2026.
`art/drafts/activity-story-ligne-claire-bbq-food-2026-10-21-v1/` contains the
seven unconverted `bbq` pictures and
`art/drafts/activity-story-ligne-claire-bbq-tools-2026-10-21-v1/` contains the
seven unconverted `bbq-tools` pictures. Both have five-column prior/current,
light, dark and 64 px contact sheets plus deterministic verification through
`scripts/build_activity_story_ligne_claire_bbq_family_2026_10_21_v1.py`.
All 14 candidates are registered as current V2 versions. At that gate the
library reached 305 pictures and 333 immutable versions; every V1 predecessor remains
byte-identical and selectable. The registration changed no story definition or
file under `src/activityStories/`.

Frank approved the complete five-picture sandwich semantic set at
`art/drafts/activity-story-ligne-claire-sandwich-2026-10-21-v1/`: four
`sandwich` ingredients plus `cooking-sandwich`. Its five-column contact sheet,
sources, rejected attempts, prompt log, fixed-palette components and verifier
are complete. All five candidates are registered as current V2 versions, while
every V1 remains byte-identical and selectable. The library now totals 305
pictures / 338 versions. Continue with a new family rather than rebuilding an
approved pack.

Frank approved the complete five-picture washing set at
`art/drafts/activity-story-ligne-claire-washing-2026-10-21-v1/` with
“approved continue - update your recipe as you go”. All five candidates are
registered as current V2 versions, taking the library to 305 pictures / 343
versions; every V1 remains selectable. The plate's slight ellipse/rim
irregularity is positive calibration for a controlled hand-drawn feel, while
the tomato remains the flat-colour benchmark. Frank then approved the
five-object General repair set at
`art/drafts/activity-story-ligne-claire-general-repair-2026-10-21-v1/` with
“approved. tool chest the best”. All five are current V2s, taking the library
to 305 pictures / 348 versions. Plate, tomato and tool chest are co-equal style
champions: respectively hand-drawn shape, flat-colour economy, and
construction/detail/object presence. Audit ambiguous counts and topology
enlarged before prompting; preserve exact construction, overlaps and parts
rather than accepting a generic category match.

The eight-piece repair hand-tools pack at
`art/drafts/activity-story-ligne-claire-repair-hand-tools-2026-10-21-v1/`.
It covers adjustable spanner, C-clamp, combination pliers, both screwdriver
types, hand saw, spirit level and tape measure. Its hard boundary is “ligne
claire, not cartoon”: retain credible adult-tool proportions and mechanisms;
reject cute, toy-like, inflated, caricature, mascot and sticker treatment.
Frank approved seven with “others all approve”; their immutable V2s are now
current while every V1 remains selectable. The first spirit-level candidate
was rejected as “too cartoonish” and remains unregistered. Frank selected the
earlier fuller correction with “this one is good”; its immutable pack is
`art/drafts/activity-story-ligne-claire-repair-spirit-level-user-selected-2026-10-21-v1/`
and its component is current V2. The later correction pack at
`art/drafts/activity-story-ligne-claire-repair-spirit-level-correction-2026-10-21-v1/`
remains unregistered history. The library now has 305 pictures / 356 versions.
Do not change Claude's story or `src/activityStories/` implementation for this
gate.

The approved nine-picture cooking-core pack at
`art/drafts/activity-story-ligne-claire-cooking-core-2026-10-21-v1/`. It
covers bacon, cheese slicing, gravy, knife, pan, seasoning, spoon, steam and
vegetables. Frank approved the exact sheet with “approved”; all nine are
immutable current V2s, taking the library to 305 pictures / 365 versions while
every V1 remains selectable. The pack adds two recipe refinements: reject
correct-looking output when prompt provenance misstates counts, and do not
confuse speckling, patina or decorative distress with the plate's useful
hand-drawn irregularity. Its four retained rejections document the two count
corrections and the surface-only knife/pan corrections. Claude's story/runtime
is unchanged. Continue the remaining Food and meals assets in a fresh,
tightly related immutable review pack.

The approved Food and meals baking/eggs/mixing family is
`art/drafts/activity-story-ligne-claire-baking-eggs-mixing-2026-10-21-v1/`.
It covers `baking-flour`, three egg-provenance pictures, butter block and four
mixing pictures. Frank approved the eight unchanged candidates plus the revised
hen with “approved, move on”; the catalogue is 305 pictures / 374 versions. Preserve
literal counts, ingredient state and detached action marks. The first hen pass
was rejected for an enlarged mascot-like eye and dense feather treatment; the
corrected candidate uses restrained adult anatomy, natural expression and
simplified interior detail. The eight family candidates and separate corrected
hen are current V2s; the rejected family hen was never registered. Claude's
stories/runtime remain unchanged.

Frank then said the chicken was “not quite right to my eye”. Preserve the
family pack unchanged and use the fresh correction gate at
`art/drafts/activity-story-ligne-claire-eggs-hen-coop-correction-2026-10-21-v1/`.
Its approved replacement uses a bead eye without sclera, smaller adult head,
weight-bearing legs/toes and irregular feather groups. The rejected family
candidate is hash-pinned inside the correction pack. Frank approved it with
“approved, move on”; it is current V2, the other eight candidates are also
current V2s, and every V1 remains selectable.

The approved Food and meals farm-animals-and-meals pack is
`art/drafts/activity-story-ligne-claire-farm-animals-meals-2026-10-21-v1/`.
It covers cow, pig, sheep, breakfast, roast dinner, vegetable-soup lunch and
steak with fries. Frank said the legacy animals looked “VERY cartoon like” and
required full redrafts rather than style rerenders, then supplied a
ligne-claire horse reference. For animal work, V1 is semantic evidence only:
preserve species, count, orientation and indispensable attributes, but redraw
adult anatomy, stance, proportions, face, contour and interior construction
from observation. Use the horse's weight-bearing construction and economical
marks without copying its horse subject, rider, dog, pose or motion. The meals
still preserve V1 counts, state, viewpoint, overlap and arrangement. Frank
approved the exact sheet with “approved”; all seven are current immutable V2s,
the library has 305 pictures / 381 versions, and every V1 remains selectable.

The first nine-picture condiment gate at
`art/drafts/activity-story-ligne-claire-condiments-2026-10-21-v1/`. It covers
honey pot, ketchup, malt vinegar, mayonnaise, mustard, olive oil, pickle jar,
raspberry jam and wholegrain mustard. The first honey-pot result was rejected
for glossy cartoon clip-art modelling; the evolved recipe uses thinner living
contour, controlled asymmetry, fewer flat colours and sparse glass/material
cues. It remains preserved as unregistered review history.

Frank subsequently judged the first gate's glass containers “too shiny, not
flat enough”. Keep that gate immutable and use
`art/drafts/activity-story-ligne-claire-condiments-flat-glass-correction-2026-10-21-v1/`
as the approved authority. It corrects seven glass containers and carries
ketchup/mustard forward byte-for-byte. Glass is quiet contour with at most two
or three short pale-blue construction ticks—no reflection bands, shine stripes,
colour wedges, gradients, bevels or luminous rims. Frank approved the exact
correction sheet with “yes much better” and set the binding taxonomy: **one
even black outline, flat colour, no shine**. All nine are current immutable
V2s; the library has 305 pictures / 390 versions, with 77 approved conversions
and 228 remaining.

Claude's first direct commission is complete in
`art/drafts/activity-story-ligne-claire-new-pictures-2026-10-21-v1/`: nine new
objects and six new action marks, all registered as V1 IDs. Claude reviewed
`evidence/light-dark-64-contact-sheet.png` and wired the relevant pictures into
stories and action demos on 22 October. At that checkpoint the catalogue was 320 pictures / 405
versions: 77 Frank-approved conversions, 15 Claude-reviewed commissioned new
pictures and 228 earlier pictures then without a ligne-claire draft.
The pack includes exact prompts, accepted sources, nine retained rejections,
flat-palette 256 px components, measured ownership/gutter metadata and its own
verifier. Do not edit this pack; corrections require a fresh immutable version.

The latest approved family is
`art/drafts/activity-story-ligne-claire-tea-toast-2026-10-22-v1/`. It contains
six registered immutable V2s for `tea-kettle`, `tea-milk`, `tea-mug`,
`toast-butter-jam`, `toast-slices` and `toast-toaster`, plus pinned sources,
one rejected first kettle and a five-column current/light/dark/64 px contact
sheet. The commissioned `tea-bag` V1 is deliberately untouched. All six were
approved by Frank on the exact sheet. His later requested `tea-mug-empty` V1
and mark-free `toast-slices` V3 are also current from fresh immutable packs,
while filled mug V2 and marked toast V2 remain byte-identical. At that approval
checkpoint the catalogue was 321 pictures / 413 versions. The later
Claude-reviewed black-ink/recipe commission brings the current library to 339
pictures / 452 versions: 83 Frank-approved conversions, 34 separately
introduced pictures and 222 earlier pictures without a ligne-claire draft.
Frank stopped the conversion programme on 22 October; those 222 are not an
active queue. Keep the recipe document as durable project memory and resume
only if Frank explicitly restarts it. Every one of the 339 ids and 452 versions
is available in the Bubble creation tool and protected as a minimum by
`data/activity-stories/catalogue-closure-2026-10-22.json` and
`npm run verify:activity-stories`.

## Kitchen art authority (24 Oct 2026)

The only continuing kitchen art authority is Warm Ligne-Claire Family V4.
Read `docs/KITCHEN_ASSET_AUTHORITY.md`,
`data/kitchen_asset_contract_v1.json` and
`data/kitchen_room_grid_contract_v2.json` before kitchen work. The exact
native 1536 × 1024 visual master is pinned in the approval record. Never
downscale or resample that art: camera zoom handles presentation, while every
distance the Prime Keeper walks must be an exact whole number of his 10.5-lp
/ 84-ku paces. Runtime Promotion V1 remains live only as a reversible
compatibility boundary; its 84 × 74 derivatives are not visual authority and
must not be used for art review. The fitted units are approved and locked to the
hash in `docs/review/kitchen-fitted-units-lock-approval-2026-10-24.json`; never
change their bodies. The active loose-asset reviewer is
`/keeper-review/kitchen-room-layout-v5/`. V5 keeps one fixed native fitted base,
uses separate state/effect layers, redraws every loose object at target source
size with curved contact shadows, moves worktop placement forward and registers
the approved 256 × 320 Prime at 228/168 display scale into the kitchen's world
density before uniform camera zoom. Kitchen art is never downscaled or
resampled. It changes no gameplay or runtime art. V4's loose family is rejected
evidence, while the fitted-unit subset approved there remains locked.

## Prime Keeper whole-bank normalisation (17 Oct 2026)

Frank has authorised an exhaustive, reversible audit and redraft programme for
the animation bank. The binding art and review rules are in
`docs/KEEPER_PRIME_ANIMATION_BANK_NORMALISATION_CONTRACT_2026-10-17.md`.
Historical animation frames are never character authority: at most they supply
skeleton/contact/prop timing. All candidates must be rendered as Prime Keeper
at fixed scale and palette and reviewed in a complete contextual route. The
old swimming, gym and scuba families are rejected and require full redraws.
`keeper_count_money` remains excluded unless Frank directly reinstates it.

The deterministic inventory is
`data/keeper-prime-animation-bank-audit-v1.json` (308 rows; 159 legacy endpoint
risks; 28 explicitly rejected/excluded; zero strip/sidecar geometry mismatches).
The active selectable contextual reviewer is
`/keeper-review/keeper-prime-context-workbench-v15/`; it includes only eleven
status-labelled routes whose present state can be defended and links the full
inventory. V3 retains V2's fix for V1's deployed relative-URL/trailing-slash
loader failure and localised native-route images, and adds the inspection-only
`/keeper-review/keeper-prime-darts-strip-inspector-v1/`. That page exposes all
30 inherited V2 cells at exact/enlarged source resolution with Prime and
adjacent overlays plus deterministic blue/navy/cream measurements. It confirms
likely blue drift in the generated core but changes no pixels. The historical
corrective isolation candidate is
`/keeper-review/keeper-prime-darts-isolation-v1/`. Whole-sheet connected-
component analysis proved that nominal 7×2 rectangular source cropping put 51
foreign actor pixels in core F07/registered F15, 42 in core F11/registered F19
and 163 in core F12/registered F20, and split four detached dart components
across core F08–F12/registered F16–F20. The candidate assigns every whole actor exactly
once, excludes detached projectiles from character cells because Darts V3
already renders them as independent effects, and preserves registered F01–F08
and F23–F30 byte-for-byte. It does not yet correct the measured palette drift
and remains unapproved. The active playable interaction authority is approved
`/keeper-review/keeper-prime-darts-context-v8/`: its 181-frame route uses the
Prime-redrawn core across six throws, retains the practical full-reach
collection, one turn at the board, one turn at the oche and exact 30.5-lp
return, and uses one harmonised detailed dart for flight and impact against the
segmented acute-angle board. Darts V1–V7 and isolation V1 remain immutable
history. The
separate Darts redraw V1 gate contains three newly generated Prime-derived key
poses, registered to exact cap/floor datums in 448 × 320 action cells. Frank
approved those exact pose hashes as the Darts drawing-family authority. Redraw
V2 adds five Prime-derived bridges and exact neutral holds to form a fourteen-
slot candidate. Darts Context V6 substituted that core into all 84 throw uses,
but is now superseded: it retained four unnecessary inherited camera-facing
posture bridges and placed the 448-pixel action cells on a false 28-lp midpoint
instead of their actual 16-lp Prime foot axis. Darts Context V7 removes old
frames 21–28, 71–78, 156–163 and 206–213, corrects all 84 core anchors, and
deterministically proves that its F20→F21 stop-to-action seam has zero changed
rendered pixels. Workbench V9 links Darts Context V8 and the unchanged core
inspector. Context V8 changes no Keeper pose, root, timing or state from V7:
it adds one gutter-safe hand-matched dart asset used for all 30 flight frames
and all embedded states, clamps every dart tip to x=168 lp, and replaces the
placeholder rim with a segmented acute-angle board. The final airborne and
first embedded renderings are byte-identical. Frank approved exact Context V8
on 17 October 2026; preserve the hash-pinned decision at
`docs/review/keeper-prime-darts-context-v8-approval-2026-10-17.json`.
Workbench V15 retains every Workbench V11 choice and replaces only the active sitting
link with the vertically corrected Prime side-right sit/stand V6 context. Frank
approved exact V6 on 17 October 2026. Its immutable decision is
`docs/review/keeper-prime-sit-stand-side-v6-approval-2026-10-17.json`. Frank
then approved exact side-left V1; preserve its separate decision at
`docs/review/keeper-prime-sit-stand-side-left-v1-approval-2026-10-17.json`.
No Final/runtime/production promotion has occurred. A fresh task should begin with
`docs/PRIME_KEEPER_RESTART_HANDOFF_2026-10-17.md`.

Frank approved exact front-facing V4 on 18 October 2026. Preserve its
hash-pinned decision at
`docs/review/keeper-prime-sit-stand-front-v4-approval-2026-10-18.json` and all
three earlier rejection records. Approval did not promote it.

Frank approved exact back-facing V2 on 18 October 2026. Preserve
`docs/review/keeper-prime-sit-stand-back-v2-approval-2026-10-18.json`. Frank
rejected immutable V1
for visible jumper/trouser darkening across complete-context frames 29–41; keep
its exact decision at
`docs/review/keeper-prime-sit-stand-back-v1-rejection-2026-10-18.json`.
V2 keeps every V1 alpha plane, dimension, foreground-chair depth cue and all 61
route frames. F2–F6 now use exact RGB samples from the exact approved Turn V9
rear endpoint, with central jumper medians 94–95 versus Prime 95 and trousers
77–78 versus Prime 77. Historical `keeper_sit_back` remains choreography-only.
Back V2 is approved as the exact back-facing authority but is not promoted and
does not approve either rear angle. Any further change must be V3 rather than
rewriting V1 or V2.

The active review proposal is Prime `keeper_sweep_broom` V1 at
`/keeper-review/keeper-prime-sweep-broom-v1/`. Preserve its versioned draft,
five actor-only generation sources, deterministic separate broom layers,
11-component masks and complete 47-frame route. The historical sweep strip is
choreography-only and contributes zero visible Keeper pixels. V1 is neither
approved nor promoted; any correction must be a new V2.

Frank has made every-frame colour matching a required verification layer for
the whole animation bank. The implementation prompt is
`docs/prompts/KEEPER_PRIME_ALL_FRAME_COLOUR_VERIFICATION.md`. It requires exact
authority selection by outfit/facing/component, disjoint masks, pose-relative
invariant material regions, adjacent-frame checks and fail-closed results. It
must reproduce rejected Back V1 failing and corrected Back V2 passing. The
specification is complete; the verifier is not yet implemented.

Future pub/games-room layout rule: mount the approved dartboard on the
right-hand cupboard-door leaf. It is edge-on while that door is closed and is
fully revealed face-to-camera when the door opens. The board follows the door
transform and keeps its approved practical reach height. Do not build the room
or cupboard from this note alone; Frank explicitly deferred that work.

Working split: Codex owns art, design and layout; Claude owns game logic and wiring. Ask for a code hook here or in HANDOFF_TO_CLAUDE.md.

## Approved Prime side-right sit/stand V6 (17 Oct 2026)

The approved side-right sitting-motion authority is
`/keeper-review/keeper-prime-sit-stand-side-v6/`. It shows the exact V2 45-frame route:
approved Walk V6 → approved deceleration → new Prime stand-to-sit → a 600 ms
seated beat → the exact byte-reversed stand → approved acceleration → approved
walk away. The six action cells use the exact approved side-right standing
authority as F1 and the exact registered side-right seated endpoint as F6.
F2–F5 are new smooth Prime redraws; first-generation `keeper_sit_side` pixels
are choreography-only evidence. All cells are 256 × 320 at density 8 with a
common `[16,40]` anchor, y=315 opaque floor limit and transparent gutters.
Generated silhouettes are registered to
measured height/width progressions to prevent an abrupt Prime-to-action width
jump. Frank judged the V1 animation good but rejected its example chair. V2's
first correction also failed live inspection because it placed the rear edge
of the backrest at the back/spine contact and allowed the seat front beneath
the shins. V5
preserves every V1/V2 Keeper frame, route root and duration while replacing
only the behind-Keeper proxy. The chair top remains y=29 / 11 lp above floor.
At the fixed action root, the backrest front is world x=76.625 and equals the
visible back/spine contact; the seat front is x=83.75; and the rear shin plane is
x=84.25, leaving 0.5 lp visible clearance. Frank then identified that the
11-lp plane crossed the Keeper's bottom. V6 keeps all Keeper and route bytes,
retains V5's horizontal measurements, and moves only the chair top to the
first fully transparent row beneath the measured rear pelvis: source y=258,
world y=44.25, 7.75 lp above the floor. V1–V5 remain immutable history.
Frank approved the exact V6 motion, contextual route and measured side-right
chair relationship on 17 October 2026. The candidate and Workbench V15 remain
review infrastructure only; approval did not promote them into Final, runtime
or production art, and it did not itself approve another direction. Side-left
has the separate approval recorded above.

## Seated Prime foundation V2 (17 Oct 2026)

Frank approved Stair Descent V2 with its slight overstride accepted. Preserve
the exact V2 art and route. The later finished staircase must add two newel
posts, a foreground balustrade and a continuous rail that can partly mask the
feet, but it must retain the stored fourteen-riser, 7-lp-tread, 98-by-60-lp
geometry. The immutable decision is
`docs/review/keeper-prime-stair-descent-v2-approval-2026-10-16.json`.

The corrected six-direction smooth seated foundation is available
at `/keeper-review/keeper-prime-seated-six-view-v2/`. It contains direct front,
direct back, side-left/right and rear-left/right endpoints. All are 256 × 320
registered cells with one `[16,40]` anchor and one historical `[16,29]` seat
landmark. V2 keeps the six V1 images byte-identical but replaces the brittle
all-or-nothing page loader. Its old opaque-row test is not chair-height proof:
opacity at y=29 did not establish the underside of the pelvis. Side-right V6
is the current measured support evidence. The left pair are exact
mirrors after registration. The
approved standing views supply identity and rendering; first-generation seats
supply pose mechanics only. The side-right and side-left endpoints are now the
exact F6 cells of their separately approved sit/stand authorities. The other
four directions remain endpoint foundations only. Full hashes are in
`art/drafts/keeper-prime-seated-six-view-2026-10-17-v2/`; V1 remains immutable
historical evidence.

## Stair descent V2 approval (16 Oct 2026)

V1 is rejected provenance: reverse-order ascent pixels made the visible left
leg remain airborne while the right took every descending step. Do not promote
or reactivate it. The replacement upper-door → stair descent → lower-door route
is `/keeper-review/keeper-prime-stair-descent-v2/`. It uses four new,
descent-specific side-right poses in the deterministic cycle RIGHT contact →
LEFT passing → LEFT contact → RIGHT passing, producing exactly seven contacts
per leg. The approved route roots, turn, walk, door action and independently
stored staircase geometry are unchanged. Raw and registered artwork hashes,
prompts, normalization data and checks are in
`art/drafts/keeper-prime-stair-descent-2026-10-16-v2/`. Frank approved this
exact candidate with its slight overstride accepted. This is an art/route
approval only: no Final, runtime or production promotion has occurred.

The staircase used by the ascent and descent reviews is no longer implicit in
their page code. Its locked geometry and preserved test-profile SVG are in
`art/drafts/keeper-staircase-geometry-2026-10-16-v1/`. Reuse that JSON for all
future stair scenery and collision/layout work. The grey profile is evidence,
not final art; the future two-newel, balustrade and handrail treatment may add
foreground occlusion but may not change any locked measurement or contact.

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

Oven Approach V7 remains historical placement/perspective evidence at
`/keeper-review/keeper-object-approach-oven-v7/`. Its 96% rear-wall and 99%
rear-face scaling proposal is explicitly superseded. Current kitchen geometry
is defined only by `docs/KITCHEN_ASSET_AUTHORITY.md` and the two machine-readable
kitchen contracts named there.

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

The current corrective review is
`/keeper-review/keeper-prime-stair-ascent-v18/`. Frank identified a visible
lower-beard jump between V16's contact and passing drawings. V18 preserves V16
as immutable authority and uses a deterministic recorded mask to transplant
the exact approved passing-left beard into the two contact drawings. All four
drawings therefore share the same 1,685-pixel beard core and x=79..132,
y=97..157 source bounds. Timing, root motion, stair contacts, other body art,
palette and cell geometry are unchanged. V18 is not approved or promoted.

The staircase scenery is a separate later review gate. It must have exactly two
newel posts (lower entrance and upper landing), a foreground open-side
balustrade with regularly spaced balusters and one continuous handrail. The
foreground layer should plausibly obscure parts of the boots/lower legs while
the tread/contact geometry remains the approved 14-riser, 7-lp-tread,
98-by-60-lp flight.

## Stair entry and landing-exit transition authority (approved 16 Oct 2026)

The approved review candidate is
`/keeper-review/keeper-prime-stair-transitions-v6/`. Its approved authorities
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
27 unique URLs before enabling playback. V3 keeps the V2 route exact, fixes the
moving frame readout to a constant height and shows a stacked 4× game view,
matching the Studio's default `zoom=4`; the former 1× thumbnail was logical
scale, not the useful default on-screen game presentation. Run
`npm run verify:keeper-prime-stair-transitions-v3` to check that immutable
presentation candidate. V4 retains its routes, roots and timing but corrects
the visible F16→F17 scale contraction: Walk F7 measures 293 source pixels from
cap to registered root while Stair V16 measures 285, so every stair-family
route frame receives one uniform 293/285 root-anchored display registration.
Run `npm run verify:keeper-prime-stair-transitions-v4` to check authority hashes,
256×320 transparent cell gutters, rejected-source exclusion, exact geometry,
moving joins, hallway closure, controls and approval boundaries. Nothing is in
Final or runtime until Frank approves the candidate. Frank found that V4 still
read smaller because cap-to-root height did not measure whole-body mass. V5
supersedes it with one constant sqrt(27,322/24,299), or 1.060×, registration
for every stair-family route frame, equating the opaque silhouette area of the
walk F7 and stair-mount authorities. Run
`npm run verify:keeper-prime-stair-transitions-v5` for that historical gate.
Frank then established the cleaner rule: reconcile scale only while the Keeper
is fully obscured behind the departure/arrival doors. V6 leaves approved Stair
V16 at native scale and applies one constant 0.943× circulation scale to every
walk, turn, bridge and reach frame between those doors. The visible route has
zero scale changes; the normal-room scale returns only after full arrival-door
occlusion. V5 is rejected provenance. Run
`npm run verify:keeper-prime-stair-transitions-v6` for the approved stair gate.

Frank approved exact V6 on 16 October 2026 with “Approved. Move on to ladder.”
The immutable approval record is
`docs/review/keeper-prime-stair-transitions-v6-approval-2026-10-16.json`.
This authorizes the stair transition as a later Final source but does not itself
promote or alter Final, runtime or production.

## Ladder transition gate (16 Oct 2026)

The immutable first reversible review candidate is
`/keeper-review/keeper-prime-ladder-transitions-v1/`. It replaces the legacy
pixel ladder as a proposed animation source without using any of its pixels.
Five smooth high-resolution studies are registered with one authority-derived
scale; the two opposite climbing phases are exact horizontal mirrors, producing
seven 256 × 320 cells with transparent gutters.

- Floor pitch is 60 lp/480 ku: eight 7.5-lp/60-ku rung intervals.
- One floor uses four complete left/right gait cycles with no phase remainder.
- Each review-frame rise is 3.75 lp; the exact upper floor occurs on route
  frame 17 and the continue route proceeds another 15 lp without resetting.
- The lower door and ladder are 84 lp/eight walking intervals apart.
- The approach is walk → decelerate/stop → approved side-to-back turn → mount
  → climb; the exit is climb → rightward transfer → both feet on the landing →
  approved reverse turn → walk to the upper door.
- Every visible frame uses Stair Transition V6's constant 0.943057 circulation
  scale. Any room/circulation scale handoff remains fully door-hidden.

Run `npm run verify:keeper-prime-ladder-transitions-v1`. The candidate is not
approved; Final, runtime and production remain unchanged.

Frank found the overall V1 animation sound but reported ladder colour showing
through the semi-transparent Keeper during the bottom turn. He requested a
faster turn and significantly slower climb, while explicitly accepting the
imperfect hand/foot-to-rung match at game scale. V2 preserved V1 art and added
a rectangular central-rung occluder, but Frank rejected that solution because
it made rung segments disappear on every step. Preserve V2 as rejected
presentation provenance.

V3 removed the V2 occluder and retained the complete ladder, but Frank rejected
its presentation because flicker remained throughout the full flow. Preserve
V3 as rejected provenance: its threshold-128 binary edges shimmered and its
review runtime destroyed/recreated the architecture and Keeper image on every
frame.

The active V4 review at
`/keeper-review/keeper-prime-ladder-transitions-v4/` derives its 29 images from
the smooth pre-V3 sources. It raises source alpha ≥240 to 255 while preserving
all lower antialiased alpha and every RGB byte. The page decodes and mounts all
unique images before playback, constructs the ladder only once, and switches
frames by visibility without DOM replacement. Roots, frame order, geometry
and rung contacts remain V1 exact; timing remains V2 exact at 50 ms per turn
frame and 150 ms per ladder frame. Run
`npm run verify:keeper-prime-ladder-transitions-v4`. The V4 candidate changes
no Final, runtime or production asset.

Frank approved exact V4 on 16 October 2026. Pin the decision through
`docs/review/keeper-prime-ladder-transitions-v4-approval-2026-10-16.json` and
`npm run verify:keeper-prime-ladder-transitions-v4-approval`. The artwork,
alpha handling, persistent compositor, roots, geometry, frame order and route
choreography are authority. Turn timing remains deliberately open: a later
timing-only candidate should halve turn frames from 50 ms to 25 ms (20 to 40
fps) without changing pixels or geometry. No Final/runtime/production
promotion was performed by approval.

The V5 Keeper animation is approved and pinned by
`docs/review/keeper-prime-ladder-transitions-v5-animation-approval-2026-10-16.json`.
It preserves approved V4
frames 1–88 and all 29 V4 Keeper images byte-for-byte, then adds a 23-frame
upper-door tail: reverse bridge deceleration, right-hand reach, door
opening, exact side neutral, restart and complete disappearance. The two reach
cells are the already accepted stair-route sources normalized only with V4's
alpha ≥240 →255 rule. The doorway is 90° to the straight-on dollhouse camera;
the V5 perspective door presentation is rejected and is not part of that
approval.

Review the door-only successor at
`/keeper-review/keeper-prime-ladder-transitions-v6/`. All 111 approved Keeper
frames, roots and timings remain exact. V6 uses a flat 20 × 48-lp rectangular
leaf, right-hinged as viewed, with no gradient or perspective widening and only
the handle protruding. It is a two-way door which always opens away from the
approaching Keeper. The opaque leaf—not an artificial room-boundary clip—hides
him while he crosses. The scenery controller closes it only after his bounds
fully clear the doorway and requires no costume-specific closing artwork. The
contract is pinned at
`docs/review/keeper-two-way-door-contract-2026-10-16.json`. Run the V6 verifier
through the archive hook or the complete test suite. V6 is unapproved and
changes no Final/runtime/production asset; V4's requested 25-ms turn pass is
still deferred.

### Core transition gap after the V5 animation / V6 door gate

The approved stair route and candidate ladder route can each demonstrate one
complete upward room-to-room journey. Stair Descent V1 now supplies an
unapproved complete downward candidate, including the opposite zig-zag turn,
lower landing and door exit. Still required before the transitional library is
complete: Frank's approval or corrections for Stair Descent V1; certification
of its mirrored opposite-flight layout; downward ladder and lower dismount/exit;
finished Prime lift call/enter and lift-exit/walk; Prime stand↔sit joins for
side/front/back furniture approaches; and explicit opposite-hand/direction
certification wherever CSS mirroring cannot preserve the door, prop or hand
relationship. A shared deterministic open-door room emergence/return route is
also required, but it must reuse standard locomotion and the persistent door
occlusion rather than introduce costume-specific door animation. Action-
specific object joins remain a later per-action layer.

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

## Doors, stairway and costumes (9 Oct 2026; door rule revised 16 Oct)

Frank has answered every open question; the full record is `docs/DOORS_STAIRS_AND_COSTUMES.md` (sections 2 and 9). What it asks of you:

- **Floors are 56 px floorboards to ceiling.** Set the floor/ceiling thickness, then that band height is fixed for every standard floor. Redraw the three room plates and the shell at the new height.
- **Stairway alongside the rooms; you pick the side.** Ladders first, then a spiral staircase (if it can look right), then the lift. How the lift arrives is yours, as part of the lighthouse growing left, right, up and down. The slide goes on the outside of the tower.
- **Doors** swing both ways, always open away from the approaching Keeper and auto-close only after his complete bounds clear; the opaque leaf must fully hide him (with hats, 48 px tall). They do not remain open during the activity. Room doors never break.
- **Bedroom floor:** en suite only through the bedroom, a walk-in closet off the bedroom, and the toilet in its own cubicle (door shut only for a poo). Other loos follow the same format.
- **New clips:** a standing neutral frame for every outfit. The scenery-controlled two-way leaf removes the former requirement for a dedicated pyjama door-close clip. Naps happen in an armchair, so the armchair is a new object.
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
