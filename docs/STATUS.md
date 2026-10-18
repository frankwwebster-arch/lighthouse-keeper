# Lighthouse Keeper: status write-up (18 Oct 2026)

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
The fridge successor is
`/keeper-review/kitchen-fridge-states-v32/`. V32 draws standard and
hinge-failed states together from one construction, keeps the lower-right hinge
attached, rests the fallen door's lower-left corner on the floor, shows sparse
generic contents, and keeps its shallow pool static. A separate 40-frame,
4-fps, ten-second drip/ripple strip supplies the only motion; the named low
electrical buzz has no visible electrical effect. Frank called the fridge
excellent on 18 October 2026, visually approved it and released the remaining
sequence. It remains unpromoted and unwired.

Kitchen V33–V38 now complete the remaining coordinated review families:
kettle, toaster, oven, mixing bowl, basin and table. Each page shows the
current authority beside the new standard, all required states at 4×, and all
states in the exact 772 × 224-pixel kitchen. Steam, heat, smoke, hob flame,
gentle flow and upward spray are separate reusable 40-frame/4-fps ten-second
strips; the bowl and table remain static. The table's failed leg stays partly
attached and no intact table is drawn beneath it. All six versions are
reversible, unpromoted and awaiting visual review. The active kitchen review
lineage is exact V5 plus every storm-blue version from V20 through V38; older
cream/brown sets remain offline in `review-archive/retired/`. Full record:
`docs/KITCHEN_ASSET_FAMILIES_V33_V38_2026-10-18.md`.

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

Prime `keeper_sweep_broom` V1 remains immutable, unapproved review history:
Frank found lower-jumper artefacts across its action reuse and asked for a more
clearly traditional broom. V2 is the active gate at
`/keeper-review/keeper-prime-sweep-broom-v2/`. It rebuilds the named lower hem
against an exact Prime swatch in every action pose, retains the separately
owned prop and per-frame material evidence, and adds the kitchen cupboard
handoff: standard walk right → fully obscured swap → moving sweep-walk left →
turnaround proxy → moving sweep-walk right → fully obscured swap → standard
walk left. It awaits Frank and is not promoted. Review-only deploy `08c9cc6`
was live-checked on 18 October: all 98 unique images decoded before controls,
the fully obscured handoff and moving-leg sweep playback worked, and no browser
console errors appeared. The full reviewer is hash-pinned to candidate
`55c5615`.

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
