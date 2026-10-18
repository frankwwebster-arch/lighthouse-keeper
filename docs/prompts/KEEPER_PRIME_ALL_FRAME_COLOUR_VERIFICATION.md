# Prompt brief: Prime Keeper all-frame colour verification

Use this document as the source brief for a fresh Codex task that implements
colour verification across the complete Keeper animation bank. It records the
failure exposed by back-facing sit/stand V1 and the outcome the new layer must
produce. This document authorises verification infrastructure and reports only;
it does not authorise an artwork correction, approval or promotion.

## Ready-to-paste opening prompt

> Work in `/Users/frank/Documents/ChatGPT/Lighthouse Keeper` on `main`.
> Read `AGENTS.md`,
> `docs/PRIME_KEEPER_RESTART_HANDOFF_2026-10-17.md`,
> `docs/KEEPER_PRIME_ANIMATION_BANK_NORMALISATION_CONTRACT_2026-10-17.md`,
> `docs/KEEPER_ARTWORK_AUTHORING_AND_REVIEW_PLAYBOOK.md`,
> `docs/prompts/KEEPER_PRIME_ALL_FRAME_COLOUR_VERIFICATION.md` and
> `docs/DEPLOYMENT.md` completely before changing anything.
>
> Build a deterministic Prime Keeper colour-verification layer for every visible
> Keeper frame in every animation. Use exact, hash-pinned Prime authorities
> selected by outfit, facing and component. Measure uncontaminated pose-relative
> material regions for the cap, jumper, cream band, trousers, boots, skin, hair,
> beard and outline wherever each is visible. Compare every frame to its named
> authority and to adjacent frames. Do not treat palette membership, a global
> whole-character statistic or a whole-garment median as proof of a visual match.
> Fail closed if the authority, component ownership or invariant comparison
> region is missing or too small.
>
> The verifier must reproduce the known regression: back-facing sit/stand V1
> must fail because its action block has jumper medians 73–74 versus Prime 95
> and trouser medians 52–53 versus Prime 77; back-facing sit/stand V2 must pass
> with jumper 94–95 and trousers 77–78. If the verifier cannot distinguish those
> two immutable candidates, it is not valid.
>
> Produce machine-readable per-frame evidence, a bank-wide summary, deterministic
> tests and a reviewer that exposes authority, candidate, component masks,
> swatches, measurements and failures side by side. Integrate the hard gate into
> `npm test` for every new or changed Keeper sheet. Audit unchanged historical
> and production sheets without silently approving or rewriting them. Preserve
> every pinned approval, old draft and immutable review page. Create only new
> versioned reversible outputs. Promote and correct nothing without Frank's
> explicit approval. Archive review media, verify the build, commit and push the
> finished verification batch to `main`, deploy its reviewer, verify every live
> image, and send Frank the production link before asking for any visual verdict.

## Why this work is required

Back-facing sit/stand V1 demonstrated a false-positive verification design.
Every action-frame RGB value belonged to an approved Prime palette and the
whole component medians matched the selected palette image, yet the jumper and
trousers visibly became much darker during complete-context frames 29–41.

The failure had two causes:

1. the palette source was not the exact same-facing endpoint displayed beside
   the candidate; and
2. whole-component statistics mixed stable material surfaces with outlines,
   folds, shadows, anti-alias pixels and different pose proportions.

Direct pose-relative readings exposed the defect:

| Candidate | Jumper central-region median | Trouser central-region median |
| --- | ---: | ---: |
| Exact approved Turn V9 rear endpoint | 95 | 77 |
| Rejected Back V1 action F2–F6 | 73–74 | 52–53 |
| Corrected Back V2 action F2–F6 | 94–95 | 77–78 |

Therefore these statements are forbidden as sole acceptance evidence:

- “all output RGB values occur somewhere in an approved image”;
- “the whole garment median matches an approved image”;
- “the generated source was recoloured”;
- “the endpoint itself is exact”;
- “the contact sheet looks broadly consistent.”

Each can be true while intermediate frames still flash darker.

## Scope

The completed layer must cover:

- every frame of every standard-uniform Keeper animation;
- every frame of every special-outfit family, using that outfit's own accepted
  authority rather than the standard uniform;
- action intermediates, holds, reverses, turns, walk phases, prop-bearing
  frames and transition bridges;
- high-resolution authored frames and their registered gameplay cells;
- existing approved authorities, active drafts, production assets and rejected
  regression fixtures, each with an explicit status;
- both per-frame authority matching and temporal colour continuity.

An audit finding is not an artwork verdict. Existing immutable approvals remain
hash-pinned authorities. Existing non-authority sheets may be marked `pass`,
`fail` or `blocked`, but must not be edited by the audit task.

## Authority selection hierarchy

Every measured component must name one exact authority file and SHA-256. Never
average conflicting authorities or silently choose the most convenient image.
Use this order:

1. Frank's latest explicit, hash-pinned approval for the same outfit, facing
   and visible component;
2. the exact approved entry or exit endpoint used in the candidate route;
3. an approved adjacent turn frame at the same viewing angle;
4. the accepted costume-family authority for a special outfit;
5. if none exists, mark the component `blocked-no-colour-authority`.

The exact same-facing route endpoint outranks an older generic orthographic
palette when their visible clothing shades disagree. Record the conflict; do
not blend the two. Historical animation art and generated-source colour are
never authorities.

Each animation register must state:

- outfit and facing for every frame;
- exact authority file and hash for every visible component;
- why that authority wins under the hierarchy;
- whether the authority is an exact endpoint, approved turn angle or costume
  family source;
- any intentional lighting or material deviation and its separate approval.

## Component ownership and comparison regions

Colour must be measured within semantic components, not arbitrary vertical
bands. At minimum support:

- cap crown, cap band/brim and badge;
- jumper blue and cream band;
- trousers;
- boots;
- skin;
- hair, moustache and beard;
- outline;
- each special-outfit material;
- prop/effect pixels as separately owned, excluded layers.

Every visible component in every frame needs a deterministic ownership mask.
Masks must be disjoint where materials touch. A pixel may not belong to both
jumper and trousers or both beard and skin. Save mask hashes and pixel counts.

Inside each component, derive one or more pose-relative invariant material
regions. A valid region contains the stable interior surface used to judge the
material itself. It must exclude:

- black/dark outlines;
- semi-transparent anti-alias fringe;
- cream stripe contamination from the jumper-blue region;
- skin, beard, hair, prop and neighbouring garment pixels;
- cast shadows and occlusion boundaries unless the authority shows the same
  shadow;
- bright specular/fold accents unless measured as their own subregion;
- transparent pixels.

Use normalized coordinates relative to the component mask or landmark-defined
interior polygons, not a whole-frame rectangle. Pose-specific regions are
allowed and expected, but their derivation must be deterministic and recorded.
If a component is visible but no clean region meets the minimum sample count,
return `blocked-insufficient-invariant-pixels`; never substitute the entire
garment and call it a pass.

For registered 256 × 320 review cells, default to fully opaque pixels and
require at least 64 invariant pixels per visible major garment component. A
different threshold is allowed only when recorded and tested for that canvas.

## Required measurements

For each visible component region in each frame, record at least:

- pixel count and mask SHA-256;
- median and 25th/75th percentile luminance;
- median sRGB colour;
- median perceptual colour in one declared colour space such as OKLab;
- perceptual distance from the named authority;
- dominant approved swatches and their coverage;
- previous-frame and next-frame deltas;
- pass, fail or blocked status with machine-readable reasons.

Use one declared colour-management path for authority and candidate images.
Un-premultiply alpha where necessary, ignore non-opaque fringe for material
measurements, and never include the transparent review background.

Default hard gates for a newly registered standard-uniform raster are:

- invariant-region median luminance within 2 points of its authority on the
  declared 0–255 scale;
- invariant-region 25th and 75th percentiles each within 4 points;
- median OKLab Euclidean distance no greater than 0.02 and 95th-percentile
  distance no greater than 0.05, calculated after the same declared colour
  conversion for authority and candidate;
- no unapproved hue-family change;
- no adjacent-frame median-luminance jump above 2 points for the same material
  unless the matching approved turn/lighting authority demonstrates it;
- zero visible pixels derived solely from historical animation art;
- zero unowned or multiply owned visible Keeper pixels.

These are defaults, not loopholes. If a frame visibly flashes while technically
inside a threshold, the test is incomplete and must be tightened. Any exception
must name the exact frame, component, reason and approved authority; exceptions
may not be animation-wide wildcards.

## Two independent gates

Do not conflate provenance with visible matching.

### 1. Provenance gate

Prove where every visible Keeper pixel came from. For a deterministic palette
transfer, candidate colours must be exact samples or a recorded deterministic
derivation from the named Prime authority. Historical and generated-source
colours are non-authoritative and must not survive accidentally.

### 2. Visible-match gate

Measure clean material regions and temporal continuity. Palette membership does
not imply that the right swatches were used in the right proportions or places.
A frame passes only when both gates pass.

## Bank-wide outputs

Create versioned outputs with stable schemas:

- a colour-authority manifest keyed by outfit, facing and component;
- per-animation and per-frame JSON evidence;
- a bank summary listing passes, failures and blocked frames;
- a human-readable report grouped by animation and failure reason;
- a review page with animation/frame selection, authority/candidate images,
  component-mask overlays, swatches and numeric readings;
- deterministic unit/regression tests;
- a verifier command such as
  `npm run verify:keeper-prime-frame-colour`;
- an `npm test` gate for every new or modified Keeper animation sheet.

The review page must preload and decode every unique displayed image before it
enables playback or controls. It must support previous/next frame, play/pause,
useful large scale, declared game scale, literal raster scale, adjacent-frame
ghosting and a component-mask toggle.

## Mandatory regression fixtures

The test suite must include immutable known outcomes:

1. Back sit/stand V1 fails for the jumper and trousers in action F2–F6 and the
   corresponding complete-context frames 29–41.
2. Back sit/stand V2 passes its regional jumper/trouser gate.
3. Exact approved endpoints compare to themselves with zero delta.
4. A deliberately darkened synthetic fixture fails.
5. A palette-membership fixture using only dark approved swatches still fails
   the visible-match gate.
6. A mask contaminated by outline or a neighbouring component is rejected.
7. A visible component with too few invariant pixels is blocked, not passed.
8. A hidden component is recorded as `not-visible`, not failed or fabricated.

The implementation is invalid if it reports Back V1 and Back V2 as equivalent.

Pin the regression inputs exactly:

- rejected V1 register:
  `art/drafts/keeper-prime-sit-stand-back-2026-10-18-v1/batch-register.json`,
  SHA-256
  `3d76c2681dc56e159e9537553afd7e3018904a29e5d92df9bf2a4be7a6548bc6`;
- corrected V2 register:
  `art/drafts/keeper-prime-sit-stand-back-2026-10-18-v2/batch-register.json`,
  SHA-256
  `a5cce0ee2a10a8123e0b10e49939080da96363d0d392643e6e82780bcdfa55a4`;
- exact approved rear endpoint:
  `art/drafts/keeper-prime-turn-side-back-2026-10-13-v9/drafts/frames/keeper_prime_turn_side-right_to_back_f09.png`,
  SHA-256
  `31dbac4efc00089fe6f831dc23f8397b4e3a8faf4d4aaa09a92b2ff407eebc35`.

## Review and correction boundary

The verification task may identify defects but must not silently correct them.
For every failed animation:

- preserve the failed bytes and immutable review page;
- record exact frame/component failures;
- propose a separately versioned correction batch only when instructed;
- use historical frames only for choreography;
- derive every visible correction pixel from approved Prime authorities;
- show the complete walk/stop/action/return context and ghost overlays;
- promote nothing without Frank's explicit approval.

## Completion criteria

Do not call the verification layer complete until:

- every inventoried Keeper animation and every frame has a pass/fail/blocked
  record;
- every visible component has an authority or an explicit blocked reason;
- the V1-fail/V2-pass regression is enforced in tests;
- new/changed animation sheets cannot bypass the colour gate;
- review media is content-addressed and the live reviewer is verified;
- setup, verification, deployment, rollback and correction boundaries are
  documented for a fresh Codex context;
- all work is committed and pushed to remote `main` without changing Final,
  runtime or production artwork.

## Cost-conscious model strategy

This task should not require GPT-5.6 Sol High end to end. The authority rules,
inventory, masks, measurements, schemas, verifier code, regression tests,
reviewer and documentation are deterministic engineering work. GPT-5.6 Terra
High is the recommended primary model for that implementation.

Use Sol High only for genuinely ambiguous visual-authority decisions, difficult
mask failures or subtle art-direction disputes that remain after the metrics and
side-by-side evidence are available. Once the verifier and schemas are stable,
Luna High may handle bounded mechanical batches such as running the audit,
updating generated reports and fixing straightforward test plumbing. Do not use
Luna alone to resolve conflicting authorities or declare a subtle visual match.

The quality safeguard is the contract and its regression fixtures, not a promise
that a cheaper model will “notice” every visual problem unaided. Start on Terra
High, require the known V1 failure and V2 pass, and escalate only the ambiguous
exceptions to Sol High.
