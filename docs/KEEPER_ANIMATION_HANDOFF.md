# Keeper animation handoff: review, scale and seamless transitions

**Checkpoint:** 10 October 2026
**Purpose:** this is the restart document for the keeper-animation work. A new
Codex task should be able to continue from here without relying on the old chat.

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

- Every costume change happens while the keeper is fully hidden behind a door.
  All relevant doors hinge on the player's side and render in front of him.
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
