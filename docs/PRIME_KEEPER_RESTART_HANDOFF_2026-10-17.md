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

Prime `keeper_sweep_broom` V2 is the active review candidate at
`/keeper-review/keeper-prime-sweep-broom-v2/`. It preserves V1 byte-for-byte
and changes only the named action defects: every generated action pose receives
pose-relative lower-hem cleanup from an exact Prime jumper-blue swatch, while a
separately owned traditional broom replaces the simplified prop (wood handle,
iron ferrule, timber stock, bindings and individual straw bundles). The exact
side-right neutral, common 315 floor, four-pixel gutters, two-hand contact,
eleven disjoint material gates and all historical-art restrictions remain
unchanged. Alongside the original 47-frame contract route, V2 adds a
cupboard-proxy context: approved standard walk right → a 100%-hidden state
swap → root-moving, leg-cycling sweep left → directional turnaround proxy →
root-moving, leg-cycling sweep right → a second 100%-hidden swap → mirrored
approved standard walk left. V2 is live from review-only deploy commit
`08c9cc6`; live review on 18 October decoded all 98 unique images before
controls enabled, reached the explicit frame-9 fully-hidden handoff, and
played the moving-leg outward sweep with no browser-console errors. The shell
fetches the full reviewer from immutable candidate commit `55c5615`, not from
mutable `main`. V2 remains unapproved and unpromoted.

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

Stop for Frank's visual decision on the already-live Prime `keeper_sweep_broom`
V2 reviewer. The direct production link is
`https://lighthouse-keeper-mu.vercel.app/keeper-review/keeper-prime-sweep-broom-v2/`.
If he approves it, write a separate hash-pinned decision and still promote
nothing without another explicit instruction. If he requests changes, create
V3 and preserve V1 and V2 byte-for-byte. After that decision, decide whether
to continue the standard standing-interaction queue or first audit whether the
approved turn network makes separate rear-angle sit/stand transitions
unnecessary. One accepted family at a time remains the safe cadence.
