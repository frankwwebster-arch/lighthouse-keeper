# Prime Keeper restart handoff

**Checkpoint:** 17 October 2026
**Purpose:** the shortest safe entry point for a fresh Codex task. The task must
be able to continue without this chat.

## Read these first

1. `AGENTS.md` and `docs/DEPLOYMENT.md` for repository and release rules.
2. This checkpoint for the current state and next gate.
3. `docs/KEEPER_PRIME_ANIMATION_BANK_NORMALISATION_CONTRACT_2026-10-17.md`
   for the binding redraw method.
4. `docs/KEEPER_ARTWORK_AUTHORING_AND_REVIEW_PLAYBOOK.md` and
   `docs/KEEPER_ANIMATION_HANDOFF.md` only when deeper construction history is
   needed.
5. `data/keeper-prime-animation-bank-audit-v1.json` and
   `docs/KEEPER_PRIME_ANIMATION_BANK_AUDIT_2026-10-17.md` when selecting an
   inherited animation family.

Do not reconstruct decisions from filenames or Git chronology when an
approval/rejection record exists under `docs/review/`.

## Permanent Prime Keeper identity

`keeper-prime-master-2026-10-12-v1` is the sole smooth, density-8 identity
authority. Frank approved it on 13 October with: “Approved. Make sure this is
NEVER forgotten.” It is the adult, restrained, slightly rotund Keeper with one
broad pale jumper band. Required face rules are solid dark rectangular eyes,
no eye glints, a separate moustache, a readable closed mouth and the established
beard mass. Never introduce a pixie grin, generic smile, childlike round eyes
or a mouth merged into the moustache.

The approved view/construction authorities are:

- Prime front from the approved master;
- smooth rear V5 with rear-facing boots;
- rigged Side-right V1, which passes all 15 internal horizontal datums;
- KP Rig V1 and construction Motion V3;
- front ↔ side Turn V1, with its accepted slight 45-degree cadence limitation;
- exact nine-frame side-right ↔ back Turn V9, pinned by V10;
- exact Walk V6, pinned by its artwork-free V7 record;
- exact stop ↔ walk V1, pinned by V2;
- Fast Timing V1 for locomotion, deceleration and turns only: walk 10 fps,
  deceleration 12 fps, no neutral pause, turn 16 fps and 625 ms endpoint hold.

Standard-uniform cap, jumper, cream band, trousers and boots must retain the
approved palette in every animation. Smooth high-resolution contours are an
independent acceptance requirement; a geometrically correct but rough or
pixelated render fails.

The original full-face references remain historical geometry evidence:
`art/raw/keeper-first-batch/keeper_neutral_standing-front_f1.png` and
`art/drafts/keeper-artist-smock-family-redraw-2026-10-11-v11/drafts/keeper_artist-smock_neutral_standing-front_f1.png`.
They do not supersede the smooth Prime master.

## Approved transition and action library

Preserve the exact approved candidate bytes and their versioned predecessors:

- Walk V6 and stop → walk → stop V1;
- walk → stop → turn to front and walk → stop → turn fully away compositions;
- Stair Ascent V16, Stair Transition V6 and Stair Descent V2. Descent V2's
  slight overstride is an accepted limitation. The eventual staircase must
  retain its stored 98 × 60-lp, fourteen-riser, 7-lp-tread geometry and add two
  newel posts, a foreground balustrade and a continuous rail;
- Ladder Transition V4 as the motion/layering authority and the V5 full Keeper
  motion approval. The requested twice-faster turn remains a later timing
  adjustment, not permission to redraw the motion;
- Darts redraw V1 as the throwing-pose drawing authority and Darts Context V8
  as the approved 181-frame contextual route, detailed dart and segmented
  board authority;
- side-right sit ↔ stand V6 as the approved six-pose motion and 45-frame
  contextual route. Its measured chair support is 7.75 lp above floor at world
  y=44.25; backrest front x=76.625 meets the back/spine, seat rim x=83.75 ends
  0.5 lp behind shin rear x=84.25. The immutable decision is
  `docs/review/keeper-prime-sit-stand-side-v6-approval-2026-10-17.json`.

Approval means the hash-pinned draft is an authority. It does **not** mean the
art has entered Workbench Final, runtime or production. No promotion is allowed
without a separate explicit instruction from Frank.

The six-view seated V2 pack supplies registered endpoints only. Side-right V6
does not approve another direction. Frank separately approved exact side-left
V1 on 17 October 2026; preserve
`docs/review/keeper-prime-sit-stand-side-left-v1-approval-2026-10-17.json`.

Frank rejected front-facing V1 because sit→stand-only frames 2 and 3 widened
significantly beyond Prime canon. Preserve V1 and its exact decision at
`docs/review/keeper-prime-sit-stand-front-v1-rejection-2026-10-17.json`.

Frank rejected front-facing V2 because complete-context frames 29 and 30 still
exposed action F3 snapping from 167 px to 158 px F4. Preserve V2 and its exact
decision at
`docs/review/keeper-prime-sit-stand-front-v2-rejection-2026-10-17.json`.

Frank rejected V3 because complete-context frames 28–32 still narrowed
elbow-to-elbow 157→156→153→149→143 px. Preserve its exact decision and hashes
at `docs/review/keeper-prime-sit-stand-front-v3-rejection-2026-10-18.json`.

Frank approved exact front-facing V4 on 18 October 2026. Preserve the
hash-pinned decision at
`docs/review/keeper-prime-sit-stand-front-v4-approval-2026-10-18.json`, its
exact F1/F6 endpoints, 143 px width lock and 59-frame context. Approval did not
promote it.

Back-facing V1 is immutable and rejected because complete-context frames 29–41
visibly darken the jumper and trousers. Preserve the exact record at
`docs/review/keeper-prime-sit-stand-back-v1-rejection-2026-10-18.json`; do not
rewrite V1. The prior whole-garment medians were a misleading acceptance test:
direct stable-region readings were jumper 73–74 versus approved Prime 95 and
trousers 52–53 versus Prime 77.

Frank explicitly approved exact Back V2 on 18 October 2026. Its immutable
decision is `docs/review/keeper-prime-sit-stand-back-v2-approval-2026-10-18.json`.
It pins every V1 alpha plane, dimension, the 150 px lowering width, all 61 route
frames, exact reverse, ghost overlay and foreground chair depth cue. F2–F6 use
hue-constrained exact RGB samples from the exact approved Turn V9 rear
endpoint; direct central-region checks read jumper 94–95 versus Prime 95 and
trousers 77–78 versus Prime 77. Historical `keeper_sit_back` contributes
choreography only and zero visible pixels. The approval does not approve either
rear-angle transition and did not promote anything into Final, runtime or
production.

Back V1's exact production deploy `d93c89c` and its 31-image live verification
remain delivery provenance only. Back V2 is live from exact deploy commit
`f165576`; the 61-frame production route and all 36 unique route/comparison
images returned valid PNG data on 18 October 2026. Live delivery is never
artwork approval.

Prime `keeper_sweep_broom` V1 remains immutable, unapproved review history at
`/keeper-review/keeper-prime-sweep-broom-v1/`. Frank found lower-jumper
artefacts across its repeated action range and a mop-like broom read. The V1
live-delivery record at deploy commit `84c8f6b` remains evidence only.

Prime `keeper_sweep_broom` V1–V8 are rejected immutable provenance. Frank
rejected V8 because the held state visibly retained the standard swinging
limbs (four arms), broke up during the turn, introduced pixelation and did not
remain visually identical to the approved walk. Preserve the exact hashes and
decision at
`docs/review/keeper-prime-sweep-broom-v8-rejection-2026-10-19.json`.

The active gate is the prop-free `hold_shaft_two_hand` motion-feasibility POC
at `/keeper-review/keeper-prime-upper-body-override-poc-v3/`. It contains eight
alternating gait phases, nine approved turn angles, never more than two visible
hands and no broom or other prop pixels. Because the approved PNG authorities
do not contain separable torso/arm layers, this smallest proof uses clean
phase-matched full-character proxies and is explicitly not pixel-identical
production art. V3 reuses every immutable V1 frame and duration. It retains
V2's mirror-aware anchor, adds a one-lp presentation registration at the
remaining rear seam, and uses one-shot playback so the standard advancing walk
does not wrap immediately to its start. Frank approved this held-implement
motion-feasibility foundation on 19 October 2026. Preserve its exact hashes and
approval boundary at
`docs/review/keeper-prime-upper-body-override-poc-v3-approval-2026-10-19.json`.
The next gate is a newly authored layered Prime torso/arm construction. The
proxy artwork, that future layered artwork, every implement, runtime, Final and
production promotion remain unapproved and unchanged.

## Binding method for every inherited animation

Every first-draft animation must be redrafted. Historical frames may supply
only choreography: joint paths, weight transfer, contact order, prop timing,
occlusion and staging. They are never visible-art authority. Do not recolour,
resize, patch a face or retain an old torso. Redraw the complete visible Keeper
from the approved Prime authorities while preserving sound motion evidence.

For each family:

1. Classify it using the 308-animation audit as motion-skeleton candidate,
   partial motion salvage, full redraw or held for dependency.
2. Select the exact approved Prime facing and neutral endpoints before drawing
   an intermediate.
3. Register one logical scale, floor anchor, root, head position and landmark
   set. Use ghost overlays against Prime and adjacent frames throughout.
4. Preserve accepted action, emotion, outfit, prop and timing where possible,
   but never at the cost of Prime identity, palette, smoothness or anatomy.
5. Build the complete game route: phase-correct walk → real deceleration →
   turn if required → action entry → repeatable action → controlled exit to the
   exact neutral → turn if required → acceleration into walking away.
6. Make entry and exit endpoints byte-identical to the named approved
   authorities unless a separately declared prop or occlusion makes that
   impossible. Keep actor and prop ownership separate.
7. Inspect at useful large scale, proposed presentation scale and literal 1×.
   Provide play/pause, previous/next frame, phase labels, speed control, ghosts
   and independent action-loop controls.
8. Verify deterministically: source/draft/registered SHA-256; cell dimensions,
   density, frame count and sidecar agreement; transparent gutters on every
   cell edge; unambiguous actor/clothing/prop/effect ownership; floor/root and
   landmark deltas; pose-relative invariant colour regions for every visible
   material in every frame; adjacent-frame colour continuity; unchanged
   out-of-scope pixels; endpoint hashes; adjacent-clip continuity; and
   preload/decode of every unique moving image before controls or playback
   start. Palette membership and whole-garment medians are not colour-match
   evidence. Follow
   `docs/prompts/KEEPER_PRIME_ALL_FRAME_COLOUR_VERIFICATION.md`.
9. Put every proposal in a new versioned `art/drafts/` directory. Never rewrite
   raw, runtime, Final, an existing draft, an immutable export or an old review
   page. Publish the new candidate beside canonical and historical evidence.
10. Record Frank's verdict in a separate hash-pinned `docs/review/` decision.
    Promote nothing unless he separately directs promotion.

Action-specific expressions are controlled deviations that must return cleanly
to the neutral face. Costume changes may be hidden by the approved door
occlusion, but each costume still needs its own internally consistent neutral,
entry, action and exit route.

The withdrawn face-camera amendments are rejected provenance only. Swimming,
gym and scuba are rejected full-redraw families. Never regenerate the deleted
`keeper_count_money` amendment without a new direct instruction.

## World and transition constraints worth retaining

- The game is a straight-on dollshouse cutaway with restrained perspective.
- Walking begins while the Keeper is hidden behind the departure door, so he
  emerges already in stride. The engine extends only the approved walk cycle.
- Normal action grammar is walk → stop → turn if relevant → action → neutral →
  turn/walk. Direct room-to-room/object-to-object travel must not force an
  absurd exit merely to re-quantise the gait.
- Doors are side-wall leaves hinged on the viewer's right, open away from the
  approaching Keeper, provide the occlusion, and close magically only after he
  has fully crossed.
- Costume transitions happen behind that door occlusion.
- Stairs zigzag through the tower; ladder travel is vertical. Their stored
  pitches and contact geometry must not be casually resized to fit a redraw.
- The approved dartboard eventually mounts on the right-hand cupboard-door
  leaf: edge-on when closed and face-to-camera when opened.

## Review, archive and deployment

Review pages are immutable and versioned. Media belongs in the
content-addressed `review-archive/objects` store, with set manifests under
`review-archive/sets`; do not commit new review PNG/GIF/JPEG/WebP/AVIF files
under `public/keeper-review`. Run `npm run archive:keeper-review` after a builder
creates review media, then run `npm test` and `npm run build`.

Ordinary pushes do not deploy. Release one complete review batch from current
`main` with `npm run deploy -- "short note"`; only the resulting commit whose
subject ends in `[deploy]` triggers Vercel. Never deploy every small correction.

Current live inspection:

- `https://lighthouse-keeper-mu.vercel.app/keeper-review/keeper-prime-context-workbench-v15/`
- `https://lighthouse-keeper-mu.vercel.app/keeper-review/keeper-prime-sit-stand-side-v6/`
- `https://lighthouse-keeper-mu.vercel.app/keeper-review/keeper-prime-sit-stand-side-left-v1/`
- `https://lighthouse-keeper-mu.vercel.app/keeper-review/keeper-prime-sit-stand-front-v1/` (rejected immutable provenance)
- `https://lighthouse-keeper-mu.vercel.app/keeper-review/keeper-prime-sit-stand-front-v2/` (rejected immutable provenance)
- `https://lighthouse-keeper-mu.vercel.app/keeper-review/keeper-prime-sit-stand-front-v3/` (rejected immutable provenance)
- `https://lighthouse-keeper-mu.vercel.app/keeper-review/keeper-prime-sit-stand-front-v4/` (current frame-32 elbow-width-locked review candidate)

Front-facing V2 was deployed from exact commit `8fb6614`, reviewed in the full
context and rejected. V3 was deployed from exact commit `07be590`, verified
live, then rejected because frames 28–32 still narrowed elbow-to-elbow. V4's
59-frame `Complete context` view loads all 28 unique images before enabling
controls. Its frames 28–32 all use exact frame 32/F6's 143 px elbow span, and
the exact frame-32 seated ghost is enabled by default to expose any future
drift. This remains a review candidate only: V1–V3 stay rejected and V4 has not
been approved or promoted.

V4 is committed at `fd81f83` and its exact production review deployment is
`e1ea5d0`. The live page was verified on 18 October 2026 at frame 28 through
frame 32 with all 28 unique images decoded and the frame-32 seated ghost
enabled. Publishing this reviewer is not artwork approval or promotion.

For every subsequent versioned review candidate, publishing and verifying the
review page is part of preparing it for Frank. Open the live frame reviewer and
send its production link before requesting comments or an approval decision;
do not ask Frank to authorise the review-page deployment. Promotion of artwork
remains a separate explicit-approval gate.

Workbench V15 is review infrastructure, not a Final-art ledger. At this
checkpoint no Prime animation has been promoted into Final/runtime/production.

## Exact next-task boundary

Sweep-broom V1–V3 are rejected immutable provenance. Frank rejected V3 because
the Keeper slid rather than walked while sweeping, the cupboard leaf did not
demonstrate full physical occlusion, the reversal did not visibly use the core
turn, and the broom read as a mop. Do not revise or promote those sets.

V4 is rejected immutable provenance: its left-facing turn endpoint incorrectly
left the broom trailing behind the Keeper, and its closed cupboard leaf did not
make the claimed occlusion visually unambiguous.

V5 is rejected immutable provenance at
`/keeper-review/keeper-prime-sweep-broom-v5/`. Frank found that its repeated
three-pose action still skimmed rather than walked, its nine-frame reversal was
too sparse, and the complete route ran implausibly fast. Frank additionally
rejected parking the broom beside the body during the pivot: the broom must
remain in the Keeper's working space in front of his torso or it will visibly
skip back to the front on the final frame. Preserve V5, candidate commit
`3548d09`, shell pin `e643fd3` and deployment `772b9e9` as evidence only.

V6 is the fresh unapproved corrective candidate at
`/keeper-review/keeper-prime-sweep-broom-v6/`. Its 67-frame route is approved
Walk V6 right → fully covered cupboard swap → two complete eight-cell
walking-sweep cycles left → a planted 17-frame reversal → two complete
walking-sweep cycles right → fully covered cupboard swap → approved Walk V6
left. The eight action cells are keyed frame-by-frame to approved Walk V6 gait
phases and show visible boot travel without lower-jumper splice artefacts. The
reversal follows the nine approved V9 angles out and the eight intermediates
back. The rigid-stock broom stays in front of the Keeper throughout, becomes
progressively occluded as his back faces the viewer, is centred between the
boots at the direct rear frame, and reappears on the new leading side without
a position jump. The straight shaft, metal ferrule, rigid timber crossbar,
separately bound straw bundles and broad working edge remain separately owned
prop evidence. Directly visible grip contact is measured in frames turn1–7;
turn8–9 record `occluded-carried` because the body hides the hands and handle.

V6 authored timing is deliberately slower: 150 ms per standard-walk frame,
220 ms per sweeping step, 180 ms per intermediate turn angle, 270 ms at each
planted turn endpoint and 300 ms for each fully hidden state swap. Its reviewer
includes large, gameplay-scale and literal 1× playback, previous-frame ghosts,
the complete cupboard route, and frame-by-frame sweep/approved-Walk
comparisons. Every classified visible Prime material pixel is checked against
an envelope derived from exact approved Walk V6 authority pixels; this is not a
whole-garment average. Prop dimensions and per-frame bounds remain recorded in
`art/drafts/keeper-prime-sweep-broom-2026-10-18-v6/batch-register.json` for
future hoovering, lawn-mowing or other tool variants. V6 changes no
Final/runtime artwork or game logic and may not be promoted without a later,
separate explicit instruction. The immutable V6 candidate is commit
`59990fcc`; shell-pin commit `a69b5bc4` fetches that exact candidate rather
than mutable `main`.

Review-only deployment commit `1c1ac67a` was verified live on 18 October 2026
at `/keeper-review/keeper-prime-sweep-broom-v6/`: the production shell served
the exact `59990fcc` pin, the pinned reviewer loaded, and every unique
actor/prop/contact/comparison URL returned successfully. The dedicated V6
verifier, TypeScript check and production build pass. At that delivery the
repository-wide `npm test` stopped at the independent public-payload ceiling
(50.06 MiB versus 50 MiB) introduced by the already-present kitchen V4 review
shell; all earlier pretest verifiers, including V6, passed before that gate.

Frank subsequently rejected V6. Its advertised gait interlacing was not what
the delivered route played: the mirrored walk-away ran F8→F1, the carried
locomotion was redrawn rather than being the approved walk with only different
arms, and the result was jerky and physically impossible. The broom also
changed shape and tone. Preserve V6 only as rejected provenance.

V7 is now rejected immutable provenance. Frank found that its Keeper broke up
during the reversal and that its opening walk did not read as the approved
Prime walk. Inspection confirmed two deterministic causes: V7 advanced 7.4
logical pixels every 125 ms (59.2 lp/s) instead of approved Walk V6's 2.625
logical pixels every 125 ms (21 lp/s), and its turn edit mask extended into the
trousers and boots where transparent source pixels could erase authority.

V8 was the movement-first review candidate at
`/keeper-review/keeper-prime-sweep-broom-v8/`. Its construction claims and
delivery hashes remain immutable evidence, but Frank's complete visual review
rejected the result: adding the held pose left four arms, the Keeper broke up
during the turn, the held sequence pixelated and the walk ceased to read as
the approved Prime walk. The provisional broom is also unapproved. The exact
decision is
`docs/review/keeper-prime-sweep-broom-v8-rejection-2026-10-19.json`.

Do not repair V8 in place. The successor removes the prop and asks one smaller
question: can a single two-hand held pose survive the approved gait phases and
turn angles? The POC answers that with a clean phase-matched proxy while making
its non-production status explicit. Any eventual production solution must
start from newly separable Prime torso/arm artwork rather than another raster
mask over complete Walk/Turn frames.

The immutable V7 candidate is commit `bdceae4d`; shell-pin commit `c22ded68`
fetches that exact candidate rather than mutable `main`. Review-only deployment
commit `e5a9cd03` was verified live on 19 October 2026 at
`/keeper-review/keeper-prime-sweep-broom-v7/`: the production shell returned
the exact `bdceae4d` pin, the pinned reviewer returned HTTP 200 with the
movement-first gate, and all 74 unique content-addressed image URLs returned
valid PNG data. The dedicated V7 verifier, TypeScript check and production
build pass. At V7 delivery the repository-wide suite reached the independent
archive payload gate after all preceding checks and stopped because the then
existing public payload was 50.26 MiB against the 50 MiB ceiling; V7 itself
left no review media in `public/` beyond its 995-byte shell.

V8 candidate commit `fc082d1c` was corrected before delivery by `0de604da`,
which removes a duplicated 21-high-resolution-pixel displacement before the
walk-to-stop bridge. Shell-pin commit `c5ec0054` fetches the exact corrected
reviewer from `0de604da`. The dedicated V8 verifier, TypeScript check and
production build pass. The full repository run passes its pretest and all
checks before the independent archive gate; the current unrelated kitchen V10
public archive state then fails because archived kitchen media is still
physically present, and the standalone archive verifier additionally reports
the pre-existing public payload at 55.63 MiB against its 50 MiB ceiling. V8
leaves only its small HTML shell in `public/`; all 94 V8 media references are
content-addressed under `review-archive/objects`.

Review-only deployment commit `319a10a9` was verified live on 19 October 2026
at `/keeper-review/keeper-prime-sweep-broom-v8`: production returned the exact
995-byte shell (SHA-256
`aeca73e78ba37a8db723876666ee2e42630fcece36462af51f84fdd229649487`),
the shell pinned corrected reviewer commit `0de604da`, that reviewer returned
HTTP 200 with the exact movement contract, and all 94 unique content-addressed
image URLs returned valid PNG signatures. This deployment exposes only the
review page; it does not approve or promote the candidate or change Final,
runtime or production artwork.

Documentation audit updated on 19 October 2026: README, STATUS, this restart
handoff and the artwork/review playbook agree that Sweep Broom V1–V8 are
rejected, held-implement POC V1/V2 remain immutable, and V3 is approved only as
the held-implement motion-feasibility foundation. Production still requires
newly authored separable Prime torso/arm layers; no proxy art, implement,
runtime or production asset is approved or promoted. Back Sit/Stand V2 remains
separately approved and hash-pinned without any production-art promotion.

Held-implement POC V1 delivery is immutable: candidate commit `98892f9c`,
shell-pin commit `d8529ece`, reconciled archive-manifest commit `7fbced02` and
review-only deploy commit `65506b56`. The live static shell at
`/keeper-review/keeper-prime-upper-body-override-poc-v1/index.html` returned
HTTP 200, pinned exact reviewer commit `98892f9c`, and all 87 unique archived
PNG URLs returned valid PNG signatures on 19 October 2026. The dedicated POC
verifier, sequential TypeScript check and production build pass. The complete
repository run passes the POC and all checks before the independent archive
payload ceiling; the existing tracked public payload is 50.39 MiB against its
50 MiB limit. The POC itself leaves only its 1,016-byte HTML shell in public.

Held-implement POC V2 is immutable superseded review history. Frank identified a
lateral leap between V1 frames 17 and 18: the reviewer mirrored each 48-lp cell
but still subtracted the unmirrored 18.75-lp root anchor. V2 subtracts the
mirrored 29.25-lp anchor for mirrored frames, keeping the declared root fixed.
It reuses every V1 frame and duration byte-for-byte and carries no new art.
Candidate commit `aa833925`, shell-pin commit `1c06451c` and review-only deploy
commit `04edb860` are on `main`. The live V2 shell returned HTTP 200, pinned the
exact candidate, exposed the corrected anchor formula, and all 87 unique PNG
URLs passed signature checks on 19 October 2026. Dedicated V1/V2 verification,
TypeScript and production build pass. The complete repository suite stops at
the independent public-payload ceiling (50.40 MiB versus 50 MiB); V2 itself
contains no new image media and adds only a 1,016-byte public shell.

Frank then reported that V2 still jumped at frames 17→18 and appeared to walk
on the spot. Diagnostics separated the causes: the mathematical/planted root
was continuous, but full-silhouette centroid moved 1.333 lp at the generated
rear seam; and modulo playback reset the advancing walk directly to frame 1.
V3 changes no image, order, duration or standard root-motion speed. Frame 18
receives a one-lp presentation offset, reducing adjacent seam deltas to
+0.333/-0.408 lp, and playback stops at the translated endpoint. V1 and V2
remain immutable.
Candidate commit `dedf5af5`, shell-pin commit `6e4b8d4c` and review-only deploy
commit `ebc362c9` are on `main`. The live V3 shell returned HTTP 200, pinned the
exact reviewer, contained the one-shot and rear-seam corrections, and all 87
unique PNG URLs returned valid signatures on 19 October 2026. Dedicated
V1/V2/V3 verification, the approval verifier, TypeScript and production build
pass. The complete suite
reaches the independent 50 MiB public-payload ceiling at 50.41 MiB after
concurrent kitchen review additions; V3 owns no new image media.
