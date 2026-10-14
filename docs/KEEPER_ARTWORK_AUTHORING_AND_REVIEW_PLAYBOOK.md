# Keeper artwork authoring and review playbook

Last updated: 14 October 2026.

This document records the durable lessons from the bathrobe, artist-smock and
standard-uniform snooker work. It is the operating guide for future Keeper
redrafts requested through the review platform. It separates proven methods,
accepted visual decisions, unresolved work and rejected techniques so that a
fresh Codex context does not repeat the same failures.

## Current authority and status

The review platform is the scope authority. Frank will inspect the complete
platform and mark the exact animation names that need new artwork. That
exact-name reviewed queue—not visual similarity, a family guess, an automated
shortlist or an earlier sample set—defines later correction scope.

| Area | Current status | Consequence |
|---|---|---|
| Keeper Prime identity | Frame 6 remains identity, stance, head-position and endpoint evidence, but its coarse raster was rejected as an animation rendering source. Frank permanently approved `keeper-prime-master-2026-10-12-v1` on 13 October 2026 with “Approved. Make sure this is NEVER forgotten.” | Treat the approved smooth master as the sole identity, rendering, proportion and face authority. Its exact approval and bytes are verifier-pinned. Derive every later direction, pose, outfit and expression from that one smooth family. |
| Orthographic endpoints | V2 achieved an exact front/back alpha match but is rejected because its rear boots still faced the player. V3 proves the historical side passes only 5 of 15 hard internal datums. Frank approved the first smooth rear-boot render for V5 and approved the smooth 15/15 rigged Side-right V1 with “Approve side-right V1 and build Turn V1.” Front ↔ side Turn V1 is approved with its recorded minor 45° cadence limitation. Side ↔ back V4 was approved and pinned by V5. Scale review produced V6, then V7 corrected pale F8 trouser patches and the narrow lower silhouette. V8's eight extra independently drawn poses made the motion significantly jerkier and are rejected. Frank approved exact nine-frame V9 with “approved”; V10 pins that decision. | V5 is the rear endpoint authority, Side-right V1 is the side authority and exact V9 is the approved side-right ↔ back turn authority. Preserve their smooth masters, proxies and V10 hashes. Never infer that a higher frame count is smoother unless the drawings are temporally coherent. V9 retains all V7 frames and adds only one 172.5° rear-quarter pose at 9 fps over one second. |
| KP construction rig | Frank approved KP Rig V1 on 13 October 2026 with “Approve KP Rig V1, let's see it animated”. After viewing Motion V2, he requested more leg movement, more steps and a slower walk while judging the other motion very good. Motion V3 changes only the walk to eight steps/five seconds with greater thigh swing and knee lift. Frank then approved Motion V3 with “Approved, very good indeed”. | Keep V1, V2 and the approved V3 bytes unchanged. Motion V3 at `/keeper-review/keeper-prime-rig-v3/` is the construction-motion authority; idle, reach and planted-ankle sit/stand are exact V2 records. Its approval produced the approved Side-right V1, approved front ↔ side Turn V1 and approved side ↔ back Turn V4. Widths remain projections; beard, hair and clothing are redrawn around the rig rather than stretching finished pixels. |
| Finished Prime walk and stop bridge | V1 is the first finished-art walk proposal and V2 its byte-identical routing wrapper. V3 attempted an opposing arm pair. V4 changed only the rear arm and still read as held. V5 correctly derives both arms from the eight accepted leg phases, but its broad F8 mask admitted frame-2 trouser geometry and visibly warped the legs. V6 repairs only that ownership error, and Frank approved it on 14 October 2026. Walk V7 is its artwork-free immutable approval record. Frank then approved exact stop → walk → stop V1; route V2 is its artwork-free approval record. | Exact Walk V6 is the approved right-facing locomotion artwork authority at `/keeper-review/keeper-prime-walk-v7/`. Exact stop → walk → stop V1 is the approved core transition authority at `/keeper-review/keeper-prime-stop-walk-stop-v2/`: exact approved neutral, three registered bridge poses, exact Walk V6 F1, then the same bridge byte-reversed into the identical stop. Root motion starts on the first gait frame and eases 2 → 6 → 12 → 18 → 21 high-resolution px/frame, with the exact inverse when stopping and zero walking-on-the-spot frames. Final and production remain unchanged. |
| Active core route | Walk → stop → turn fully away V1 composes approved authorities only. | Review `/keeper-review/keeper-prime-walk-stop-turn-back-v1/` after the next deployment. Two exact Walk V6 cycles end on F1, the approved deceleration reaches the exact Side-right stop, and the exact V9 turn continues to the exact approved rear. Fast Timing V1 removes the duplicated stationary settle: runtime stitching enters the 13-frame join at frame 2 after the loop's Walk F1, and V9 F1 is a geometric seam authority rather than a replayed frame. No new character drawing, Final entry or production promotion is implied. |
| Render smoothness | Frank requires every approved model at this stage to be super smooth; V4's second, rougher render is not acceptable even though its geometry passed. V5 scale review also exposed that an older low-resolution F8 endpoint looked pixelated when enlarged, even if the defect might be hidden at game scale. | Keep a high-resolution smooth artwork master, use anti-aliased/Lanczos reductions only for registered proxies, and reject rough outer contours or jagged internal linework independently of geometry or intended display size. |
| Standard uniform | Frank preferred the first smooth render and judged the double-stripe jumper too difficult to retain consistently. During the side/back review he established that cap, jumper, cream band, trouser and boot colours must remain consistent in every animation using this outfit. He approved the corrected V4 turn, including its V3-derived palette, with “Approved.” Later scale review found F1's trousers and boots still too dark, then found pale F8 patches caused by overlapping component masks. | The approved Prime Master uses one broad pale chest-and-sleeve band. Double-stripe generated variants are rejected provenance. Every new standard-uniform batch must register component masks and deterministic palette comparisons; no frame may flash darker on reaching a new viewing angle. Adjacent clothing-component masks must also be proven disjoint before colour transfer. V7 corrects the V6 overlap; V8 applies the same disjoint component registration to every new intermediate while retaining each V7 pose exactly. |
| Animation workbench | Final and active Draft both contain zero animations. | Historical V1/V2 transition assets remain recoverable provenance only; do not present or reuse them as active candidates. |
| Timing lab | Frank judged walk → stop → turn to camera V1 excellent, tuned a much faster child-focused profile in the Timing Lab and approved it with “approve fast timing v1” on 14 October 2026. | **Fast Timing V1** is the locomotion/transition authority: walk 10 fps, deceleration 12 fps, zero neutral pause, turn 16 fps and a 625 ms endpoint hold. It applies only to walks, stopping bridges and turns. Action entry, loops, exits, comic beats and prop choreography retain independent, activity-specific timing so enjoyable actions can be savoured. Artwork, Final entry and production promotion remain separate gates. |
| Artist-smock design | The V10 costume design is accepted; seven V11 authored animations are active review drafts | Keep this family internally consistent and await exact-name platform decisions before production promotion |
| Standard-uniform snooker route | The complete route is visually accepted and is an active `keeper_snooker` review draft | The platform verdict is still required; production remains the old eight-frame strip |
| Bathrobe | No replacement family is accepted | Do not revive head transfer, beard transfer or procedural redraw experiments; wait for exact-name platform requests |
| Other costumes and activities | Not implied by the work above | Start only from a reviewed exact-name request |

### Face-to-camera amendment decision — 12 October 2026

Frank withdrew every newly rendered face-to-camera candidate from handoff
`d9081e53-2808-4b1f-8422-2df09cf38c3c`; the generated results were judged
completely wrong. They remain rejected provenance only and must not be
reactivated by a family rebuild. Canonical front-facing art remains authoritative
until Frank gives a new explicit direction. For retained side and
three-quarter amendments, do not introduce a generic smile or open grin;
action-specific mouths are allowed only when the physical action requires one.
The rejected `keeper_count_money` source, normalized strip and review evidence
were subsequently deleted at Frank's explicit request; only their SHA-256
values and deletion record remain. Never regenerate that amendment implicitly.
The rejected `keeper_pyjamas_turn_back-v2-neutral.png` is a pinned negative
example: its front pose erases the moustache/mouth definition and turns the
remaining line into the cutesy curved "pixie grin" Frank rejected. Never use
that source as a face, moustache or expression reference.
The complete eight-pose `keeper_water_plants_front-v1-neutral.png` amendment is
also rejected, not a source from which individual poses may be salvaged; the
previous canonical front-watering strip remains authoritative.

The replacement full-face workstream begins from a clean, separate V1 canon
pack at `art/drafts/keeper-full-face-canon-pack-2026-10-12-v1/`. It does not
reuse the withdrawn images. Its candidate is an exact copy of the selected
standard front neutral, and its V11 artist-smock reference is comparison-only.
Frank approved the pack on 12 October 2026 for small-batch authoring. It still
cannot authorize production promotion by itself. The first two-animation batch
is limited to the standard-uniform side-to-front turns. Its V1 F5-only head
transplants were rejected; V2 redraws the complete moving models in F1–F5 and
locks F6 to exact canon, with deterministic endpoint-geometry checks. Frank
initially approved both V2 turns on 12 October, but running-route review later
rejected their joins and then rejected the coarse Frame 6 raster as an
animation endpoint. The workbench has consequently been reset to zero Final
and zero active Draft animations; the approval remains historical provenance,
not a current lane entry. Their exact right-turn F6 remains **Keeper Prime
(KP)** identity and geometry evidence. The first KP transition Draft at
`art/drafts/keeper-prime-core-transitions-2026-10-12-v1/` remains rejected
review history except for its accepted walk→stop deceleration. The current V2
proposal is `art/drafts/keeper-prime-core-transitions-2026-10-12-v2/`: it
preserves those walk/stop bytes, removes the duplicated stationary acceleration
frame, and derives each turn and sit from one coherent six-pose source. Live
review found it still visually unchanged because every route returned to the
coarse Prime pixels. It is rejected provenance, not an active Draft. Frank
permanently approved `art/drafts/keeper-prime-master-2026-10-12-v1/` on 13
October 2026: a smooth density-8 front neutral based on Frank's preferred first
generated render, with one broad pale band and explicit face/landmark guides.
Its approval is a permanent authority record, but not production promotion.
Orthographic V2 remains immutable: its side is byte-identical to V1 and its
180° rear elevation copies the approved front alpha channel exactly. The later
finding that its boots face the player proves silhouette agreement alone is not
an orientation check. V3 registers 15 horizontal
front-to-side datums spanning the cap, badge, ear, shoulder, beard base, arm and
midriff stripes, hand, knee and floor. That historical side passes only five
and was therefore redrafted before turn authoring. Two earlier guided
generation attempts are rejected provenance because exact total height did not
prevent internal drift. The replacement rigged side-right V1 keeps a smooth
1122 × 1402 source, uses uniform Lanczos registration only and passes all 15
datums exactly. Frank approved Side-right V1 on 13 October 2026; the approved
artwork remains outside Final and production.
Frank later selected that first rounded rear-heel treatment, stating that it
does not look like toe caps and approving it. V5 pins the exact source without
regeneration, keeps V2 rows 0–272 byte-identical, replaces only rows 273–315,
and retains the zero-mismatch alpha overlay. Its 1122 × 1402 source is the
smooth artwork master; the registered 256 × 320 proxy is Lanczos-resampled.
V4's rougher, over-squared substitute remains historical provenance. The full
cream rear mass is hair, not beard. V1 and the later hair-cut-too-short mistake
are retained provenance. The full read-only
62-asset scope is recorded in
`docs/KEEPER_FULL_FACE_INVENTORY.md` and
`data/keeper_full_face_inventory.json`.

The legacy production side-right gameplay raster is:

- `art/raw/keeper-first-batch/keeper_neutral_standing-side-right_f1.png`
- SHA-256 `02106cfc54b224c8d4e9985e58420f1350f114d24e2e6c6258cad68e513657ce`
- 128 × 160 source pixels, representing a 32 × 40 logical cell at density 4
- logical anchor `[16, 40]`

It remains unchanged in production, but is no longer an identity authority.
Use it only for pose/choreography and current-runtime comparison. The proposed
Keeper Prime side stop is versioned separately and must be approved through the
new complete-route Draft before any promotion.

The fuller canon is a linked identity system, not merely a beard outline. The
compact rectangular eye, stepped forehead, compact angular nose, ear,
sideburn, moustache, beard, neck attachment, head/body ratio, hands, outline
weight, legs and boots all contribute to recognition and continuity.

## The most important visual lesson

Absolute output size is adjustable in the reviewer. Internal ratios are not.
The eye-relative and head-relative geometry must survive every pose:

- compact dark rectangular eye rather than a rounded or highlighted eye;
- compact stepped nose rather than a bulbous or lengthened one;
- full, firm beard with a broad cheek connection, forward chin mass and a
  stepped downward termination rather than a soft outward balloon;
- canonical forehead without an eyebrow-induced central bump;
- coherent skin and hair palettes rather than pasted colour patches;
- broad outline weight relative to the eye and facial features;
- stable hand, boot, limb and head/body proportions.

Uniformly resizing a different head does not repair these ratios. Animations
that meet in the same outfit will expose even a small internal mismatch as a
visual jump.

## Two continuity standards

### Standard uniform

An activity in the ordinary blue Keeper uniform must connect directly to the
canonical walk, stop, neutral and turn system. There is no hidden costume
change to excuse a different beard, face or body. The activity must therefore
begin and end on exact canonical route poses, and the generated action poses
must preserve the standard-uniform identity throughout.

Snooker is the reference example:

`walk right → stop → exact neutral → reach → cue contact → lower → aim/stroke
loop → rise → release → exact neutral → turn → walk left`

### Special outfits

Costume changes occur out of sight behind a door. A special-outfit family may
therefore differ slightly from the standard-uniform model at the hidden
handover, but every animation used while that outfit is visible in the room
must form one internally consistent set.

For the artist studio, family consistency is more important than forcing each
old artist animation to preserve a different legacy costume rendering. The
accepted smock language is a warm-ivory mid-thigh painter's coat with navy V
binding and cuffs, two low patch pockets, and separated, clearly defined
vermillion, ochre, teal and green paint marks. The garment must hang low enough
and its front and rear designs must belong to the same coat.

This principle does not authorize a family automatically. The review queue
still controls which exact animations are redrafted and later promoted.

## Proven authoring method

The successful method has two separate stages: generative drawing and
deterministic normalization. Do not ask either stage to do the other's job.

### 1. Resolve exact scope first

Before authoring:

1. Read the newest claimed review-platform handoff.
2. List only the exact requested animation names.
3. Determine whether they belong to a standard-uniform continuity route or a
   special-outfit family.
4. Inspect related front, rear, side, walk, sit and turn clips in the reviewer.
   The rear smock design was discoverable only by looking at the back-facing
   animation; it should not be guessed from the front.
5. Identify the exact route seams that will be visible in play.
6. Create a new dated, versioned draft directory. Never overwrite canonical,
   raw, runtime, reviewer-export or previously reviewed draft files.

### 2. Establish a strict reference hierarchy

References have separate jobs and must not be allowed to compete:

1. **Identity authority:** the approved canonical Keeper, preferably both a
   clean high-resolution source and an exact gameplay raster.
2. **Family continuity authority:** an already accepted source from the same
   outfit or action family.
3. **Pose/action authority:** the matching legacy action, used only for stance,
   movement, prop direction and choreography.
4. **Costume authority:** the accepted costume model for a special outfit.

Identity takes priority over defects in an action or costume source. Pose
takes priority over the neutral stance. Costume takes priority over the
identity reference's clothing. A prompt should state those priorities
explicitly.

Useful pinned standard-uniform sources are:

- `art/source/keeper-first-batch/keeper-walk-generated-source.png` — SHA-256
  `637b3c4e66b4019730eaa7354812b18df788aedc4ab3e3b7c619589854e0da5f`;
- `art/source/keeper-first-batch/keeper-snooker-generated-source.png` — action
  geometry only, SHA-256
  `d78fd0505de0fa0b4dd477a6fb035ec1eed1fd241694d11b93a8c2210cf08d58`.

The accepted artist-smock costume authority is:

- `art/drafts/keeper-canon-model-pack-artist-smock-2026-10-11-v10/generated/artist-smock-fresh-source.png`
- SHA-256 `0101b38c45a406cbe49dd5cbca4da0fd1592a7b185807afbb5f98bd898af937b`

The nine-model canon pack and its perimeter outlines remain useful comparison
references for facing, envelope and outline weight. They are not a drawing
mechanism. An outline alone cannot specify a coherent costume, hidden crown,
neck junction, surface shading or action anatomy.

### 3. Generate a coherent full character

Use the built-in image generator in referenced-image, identity-preserve mode.
Ask for a fresh, coherent full-character render on genuine transparency. The
head, neck, costume and body must be authored together.

The prompt should specify:

- exact identity and ratio authority;
- the allowed pose or action change;
- the accepted costume authority, if any;
- exact limb and hand count;
- which hand owns a prop and where that prop enters the frame;
- one continuous rear torso silhouette;
- the complete eye, nose, beard, skin, palette and outline constraints;
- generous transparent clearance;
- no scenery, text, borders, guides, shadows, glow, detached fragments,
  duplicate headwear, duplicate ears or residual clothing;
- smooth high-resolution source art rather than deliberately enlarged pixel
  art.

For a single difficult action, generate one isolated pose at a time. This was
the reliable approach for cue acquisition and deep snooker leans. It makes
anatomy count and prop ownership easy to inspect before spending effort on the
rest of the sequence.

For a coherent costume clip, one isolated source sheet per animation can work.
This was successful for the V11 artist family, but only after rejecting source
grids in which long brushes crossed implied frame boundaries. Props and limbs
must have transparent separation around every source cell. A crop must never
be used to disguise overlap.

### 4. Inspect source art before normalization

Reject the source immediately if it has any of these defects:

- wrong beard, eye, nose, forehead, cap or skin tone;
- changed head/body ratio;
- an extra arm, hand, sleeve, ear, headwear element or beard outline;
- a missing rear torso or a flattened back caused by erasing a limb;
- a costume that ends too high, has undefined paint marks or contradicts its
  rear view;
- a prop crossing a source-cell boundary;
- cropped clothing, cue, brush, hand, foot or headwear;
- coarse pixel enlargement where smooth source art was requested.

Do not try to rescue a structurally wrong source with deterministic patches.
Generate a new coherent pose with more explicit anatomy instructions.

### 5. Normalize mechanically

Normalization may isolate, uniformly scale, align, harden alpha and place the
accepted source. It must not redraw anatomy or resize individual body parts.

Required rules:

- isolate valid foreground using native alpha;
- remove low-alpha glow by a recorded threshold;
- use one uniform scale for the complete character;
- use one shared scale for all frames extracted from the same source sheet;
- when individually authored poses belong to one action family, keep one
  controlled source-to-game scale rather than forcing every pose to the same
  height;
- align by the feet/baseline and declared logical anchor;
- harden alpha only after the single resize;
- preserve binary alpha in the normalized draft;
- expand the logical canvas for long tools or raised props rather than
  shrinking the Keeper;
- require a transparent gutter on all four edges of every frame;
- record crop, scale, placement, bounds, hashes and a byte-identical rerun.

The accepted snooker action uses:

- foreground threshold: alpha 32;
- fixed uniform scale: `0.14204545454545456`;
- final alpha threshold: 128;
- common source-pixel foot anchor: `[128, 158]`;
- 320 × 160 review canvas, equivalent to an 80 × 40 logical cell at density 4.

The lean poses are naturally shorter than the standing poses. Normalizing each
pose to the same height would destroy the action's internal proportions.

The V11 artist family uses one shared uniform scale per generated source sheet,
calculated from its first pose and matching action reference, then applied
unchanged to every pose in that sheet. Painting clips use expanded 40 × 48
logical canvases so brushes remain isolated without shrinking the Keeper.

### 6. Build routes from exact seam authorities

The first and last frames of adjoining animations should be byte-identical
whenever they represent the same physical pose. Similar-looking frames are not
enough.

If two legacy endpoints disagree, Frank's preferred frame is the authority.
Reuse that complete normalized raster at both sides of the seam. Do not copy
only its head or beard.

Examples:

- The final frame of V11 `keeper_artist_smock_turn_front` is the complete first
  frame of `keeper_artist_smock_sit_front`, which Frank preferred. Their RGBA
  difference is zero.
- Both V11 artist turns begin on the complete walk-neutral raster.
- The snooker stop ends on the exact canonical side-right neutral; that same
  neutral begins the canonical right-to-back turn.
- The canonical right turn and left-turn bridge share the exact back pose.
- The back-to-left turn ends on the exact mirrored walk-start pose.

Props need acquisition and release transitions. A cue should not jump from
absent to a fully leaned playing pose. The accepted sequence uses a single
reach, cue contact, lower, aim/stroke loop, rise, cue-held and release path.

### 7. Review complete routes, not isolated art only

Present both:

- source-art comparisons for illustration quality; and
- native/gameplay-scale animation at an intentionally slow review speed.

The slow route reveals ratio drift, extra limbs, abrupt prop changes and seam
jumps that a contact sheet can hide. Frank's visual verdict is authoritative.
Automated measurements prove registration, containment and repeatability; they
do not declare a likeness successful or unsuccessful.

This distinction matters: the snooker robustness images initially looked
questionable to the authoring process, but Frank judged both usable. Their
visual acceptance overrides the historical filename
`deep-lean-v1-failed.png`. Status belongs in the manifest and handoff, not in
an old filename.

## Rejected methods and why they failed

### Beard-only reshaping

Mask transfer, row terraces and inward/downward deformation did not solve the
bathrobe identity mismatch. Some changes were invisible at gameplay scale;
others produced spikes or changed the wrong contour. The forehead, eye, nose,
moustache, beard and neck are coupled, so beard-only editing is too narrow when
the complete head system differs.

### Head transplantation

Exact canonical head transfer still looked visibly pasted onto the bathrobe
and smock bodies. Neck, collar, costume occlusion, palette and torso geometry
did not integrate. Frank explicitly rejected this method: do not attempt it
again.

A capped canonical head also cannot reveal a correct capless crown. A future
capless outfit needs its own coherent, visually approved capless identity
source; hidden crown geometry cannot be inferred safely by deleting the cap.

### Repeated targeted generator corrections

Requests such as “make the beard fuller,” “make the eye rectangular” or “fix
the nose” did not converge when the underlying generated head ratios were
already wrong. Each edit could change cap, skin, forehead or proportions while
repairing another feature. Once the structural identity drifts, restart from
the reference hierarchy with a fresh coherent render.

### Procedural or manual redraw from measurements

The hand-authored full-character trial produced a different illustration
rather than the established Keeper. Measurements and masks are valuable for
validation, but they are not a substitute drawing system for this character.

### Repainting the canonical jumper into a costume

The canonical-outline smock repaint produced a repeatable face but a garment
that was too short and inadequately defined. A costume has its own silhouette,
coverage and rear design; recolouring the existing jumper cannot create a
longer coat coherently.

### Multi-pose grids without ownership gutters

The first snooker and painting grids allowed cues or brushes to cross implied
cell boundaries. That makes component ownership ambiguous and invalidates the
sheet. Use isolated poses, wider cells or grids with genuine transparent
separation.

### Removing the wrong arm or only part of an arm

The first cue-acquisition pose had three arms. Removing the wrong arm, then
only its hand, produced progressively worse anatomy and erased back definition.
The successful correction was a fresh render with explicit requirements:
exactly two anatomically connected arms, exactly two hands, one reaching arm,
one naturally lowered arm, no rear limb, and a continuous rounded back.

### Treating scale as the main defect

The review platform can resize a coherent character. It cannot fix a rounded
eye, wrong nose, shortened beard, thin outline or altered head/body ratio.
Prioritize internal ratios and transitions over matching an arbitrary bounding
box.

## Accepted reference implementations

### Artist-smock V11 family

The family is documented at:

- `art/drafts/keeper-artist-smock-family-redraw-2026-10-11-v11/HANDOFF.md`;
- `art/drafts/keeper-artist-smock-family-redraw-2026-10-11-v11/evidence/validation.json`;
- `art/drafts/keeper-artist-smock-family-redraw-2026-10-11-v11/prompts/`;
- `art/drafts/keeper-artist-smock-family-redraw-2026-10-11-v11/normalize_family.py`.

It contains seven authored animations and eight deterministic neutral/bridge
derivatives. The seven authored clips are active review comparisons; the eight
technical derivatives are intentionally excluded from the 173-animation
gallery. Production is unchanged.

### Standard-uniform snooker route

The accepted route and full provenance are documented at:

- `art/drafts/keeper-standard-snooker-complete-sequence-2026-10-11-v1/HANDOFF.md`;
- `art/drafts/keeper-standard-snooker-complete-sequence-2026-10-11-v1/build_preview.py`;
- `art/drafts/keeper-standard-snooker-complete-sequence-2026-10-11-v1/evidence/build-manifest.json`;
- `art/drafts/keeper-standard-snooker-single-reach-2026-10-11-v1/`;
- `art/drafts/keeper-standard-snooker-authoring-robustness-test-2026-10-11-v1/`.

The visually accepted half-speed preview has SHA-256
`b5ae7a9cdf99918628c4a45867713bb9e738682e138f2a4302c82c3913b62e89`.
The 65-frame, 4 fps review strip has SHA-256
`01bb338512f37561efd86ceb4256c855e4f7b3e250a49b1b5e275d528a25eab0`.
It is registered as an active `keeper_snooker` comparison. The canonical
eight-frame production strip is unchanged.

## Assembly and transition review

The separate `/animation-workbench` surface complements, but does not replace,
the exact-name `/keeper-review/` workflow. The established reviewer remains the
source for amendment decisions and handoffs. The workbench is the place to
assemble immutable history and versioned proposals into editable Draft recipes
and judge complete ingress and egress routes.

Final workbench items are immutable and repository-backed. Frame copying,
removal, reordering and section repetition begin only after **Copy to Draft**;
these operations change frame references, never approved sprite bytes. Every
animation must expose `walk → moving stop → optional front/back turn → action`
and return compatibly through `action → exact stop → reversed start → walk`.
The stop/start preview retains per-frame root motion so no walking pose is held
stationary. The
game engine alone extends the walk deterministically from world placement; no
distance-specific walk count belongs in an authored recipe. Walking begins
while the Keeper is still fully hidden behind the departure door, so his first
visible state is already mid-stride. Closed doors may
hide costume swaps but do not exempt the resulting action from its ingress.
Workbench Final approval never implies raw or runtime promotion.

Every dedicated core-animation review page must provide previous-frame and
next-frame stepping as well as play, reverse, loop and pause controls. It must
show the same frame simultaneously in a large inspection view and at the exact
proposed game display box derived from the logical cell and renderer scale. For
the standard 32 × 40 Keeper cell at the current `PX=4`, that view is exactly
128 × 160 CSS pixels. Both views must use one frame index and one set of source
URLs so they cannot drift apart.

The complete contract is in `docs/KEEPER_ANIMATION_WORKBENCH.md`.

Timing is a separate approval layer. `/keeper-timing-lab` compares the reviewed
profile with a live proposal over the exact same frame URLs. Walk,
deceleration, neutral settle, turn and endpoint-hold timing are independent.
Frank's approved repository-backed **Fast Timing V1** applies to locomotion and
turn transitions only. Action animations never inherit it automatically; each
action keeps its own entertaining performance rhythm. Personal proposals and
personal preview defaults remain device-local until exported as JSON; that
export records the immutable artwork-register hash and only the changed timing
fields. Never redraw or re-promote pixels merely to change fps or a deliberate
hold.

## Review-platform workflow for future amendments

1. Frank reviews the deployed platform and records decisions against exact
   animation names.
2. Frank uses **Hand back to Codex**.
3. Codex claims the newest handoff before changing mutable art or metadata.
4. Codex treats the exact-name delta as the complete scope for that pass.
5. Each amendment is created in a new versioned draft directory with its
   canonical comparison, hashes, prompt, generator output and deterministic
   normalization evidence.
6. Canonical and draft variants are exposed side by side under the same exact
   animation name.
7. Production art remains unchanged while the item is an
   `active-review-draft`.
8. Frank manually chooses a preferred promotion candidate and hands the review
   back again.
9. Only a later explicit promotion copies accepted bytes into raw/runtime
   production, updates manifests and retains the previous version for rollback.

Do not infer a whole correction family from one marked animation unless Frank
explicitly requests a consistent family. Conversely, when Frank requests the
whole special-outfit family, inspect and cover every manifest entry in that
family, including technical neutral and bridge dependencies, while exposing
only real authored animations as gallery rows.

## Mandatory evidence checklist

Every new or amended sheet must preserve:

- exact input paths and SHA-256 values;
- exact prompt text and reference order;
- untouched generator output;
- selected and rejected candidate disposition;
- normalization script and settings;
- uniform scale and anchor placement;
- canvas, density, frames and FPS metadata;
- per-frame alpha bounds;
- binary-alpha result;
- zero opaque pixels on all cell edges;
- no ambiguous cross-cell component ownership;
- source, normalized and published-review hashes;
- exact seam comparisons where routes meet;
- deterministic byte-identical rerun;
- a rollback statement;
- explicit status: draft, visually accepted, active review, rejected or
  promoted.

The deterministic verifier must reject geometry/metadata mismatch, empty
frames, shared-edge alpha, stale hashes, missing evidence and detached
exact-name registration.

## Practical decision rules

- If identity is wrong, regenerate the complete character; do not transplant
  the head.
- If one generated pose has wrong anatomy, discard it and render that pose
  again with explicit limb ownership.
- If a prop will not fit, enlarge the cell; do not shrink the Keeper.
- If two route endpoints represent the same pose, reuse one complete frame.
- If a costume source conflicts with the accepted family, the accepted family
  wins.
- If an action source conflicts with canonical identity, canonical identity
  wins and the source supplies choreography only.
- If an automated result and Frank's visual verdict differ, Frank's verdict
  controls acceptance.
- If the review queue does not name an animation, do not begin it.
- If a visually accepted item has not received a later platform promotion
  decision, keep production unchanged.

## Documentation and handoff rule

At the end of every accepted draft pass, update this playbook only when the
method itself has gained new evidence. Update the ordinary README, status and
animation handoff whenever reviewer state, accepted family state or production
state changes. Chat history is not an authoritative record.
