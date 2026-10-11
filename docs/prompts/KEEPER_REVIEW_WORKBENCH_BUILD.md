# Keeper review workbench build

## When to run this

Run this as a dedicated product build after the current Keeper reviewer is
stable. It expands the existing animation reviewer for this project; it does
**not** turn it into a general-purpose product or alter canonical art as part of
the first delivery.

## Recommended model

Use **GPT-5.6 Terra with High reasoning**. The task spans durable review data,
sprite-sheet geometry, safe draft generation, scene composition and existing
runtime metadata. It must favour reversible review drafts over clever implicit
production changes.

## Ready-to-paste prompt

```text
Continue the Lighthouse Keeper work in:

/Users/frank/Documents/ChatGPT/Lighthouse Keeper

Work from current remote main. Build the next stage of the existing online
Keeper review platform: an asset-review workbench for the current project.
Do not attempt to productise it for arbitrary games yet. However, design the
data model with typed asset records and relationship records so a later generic
version does not need to discard the project’s review history.

Read first:

1. README.md
2. docs/CODEX_HANDOFF.md
3. docs/KEEPER_ANIMATION_HANDOFF.md
4. docs/KEEPER_ASSET_SCALE.md
5. data/keeper_asset_contract.json
6. art/manifest.json and the published sprite manifest
7. the existing public/keeper-review and docs/keeper-scale-audit reviewer code
8. docs/prompts/KEEPER_SPRITE_FRAME_ISOLATION_AUDIT.md

The existing reviewer already has animation filtering, pose overrides, reserve
entries, canonical/draft comparisons, a Hand back to Codex queue, and a
non-destructive review-only size reset. Preserve all of it. No new feature may
overwrite canonical source, raw strips, runtime sprites, manifests, immutable
review evidence, or any existing draft. Every art/crop/frame amendment must be
a new versioned draft with canonical and draft SHA-256 values, exact-name
provenance, visible comparison, discard/undo, and an explicit later promotion
step. Enforce sprite-cell isolation and transparent shared-edge gutters for
every generated or edited draft.

Build these connected capabilities.

1. Asset workbench tabs

Keep the existing Animations tab. Add Rooms/Floors and Furniture/Objects tabs,
plus a Context preview tab. Each tab must support compact gallery, search,
direct open-close review, review state, annotations, reserve/review handoff and
draft comparison appropriate to that asset type. Rooms and furniture are often
single images but must still have an exact asset id, source/runtime filenames,
dimensions, logical anchor/contact data, current candidate, review status and
history. Do not fake a review card when an asset has no trustworthy source
mapping: flag it as unmapped for review.

2. Precise visual annotations

Add a review-only overlay tool for an animation frame, static room or furniture
asset. The reviewer can draw rectangular or freehand regions, attach a concise
comment, choose a frame number where applicable, and inspect/edit/delete their
own annotations. Store annotation coordinates in logical canvas coordinates,
not screen pixels, tied to exact asset id, candidate SHA and frame index. They
must rescale correctly at every zoom level and remain attached to the right
canonical/draft variant. Include annotations in Hand back to Codex. Annotations
are comments only: they never paint or mutate pixels.

3. Full sheet and crop/anchor review

For every sheet, provide a full-strip view as well as isolated frames. Permit
the reviewer to propose crop bounds, frame grid/cell geometry and anchors at
either whole-sheet or single-frame level. Preview the proposal without changing
art. Validate frame count, strip geometry, opaque-pixel gutters, component
ownership and manifest compatibility. Saving a crop/anchor proposal creates a
draft request record only; applying it to a sprite strip must be a later,
explicit, reversible draft-generation action with canonical/draft hashes and
side-by-side comparison.

4. New animation requests

Add a request form that creates a durable queue item rather than inventing art.
It must select closest existing reference clip(s), outfit, facing/start/end
pose, intended object, target frame count/FPS, loop behaviour, route/transition
need, scene/furniture trigger, and free-text brief. A request is a review
artifact and must appear in Hand back to Codex. It cannot silently create or
promote art.

5. Routines, triggers and relationship graph

Create a small explicit relationship model—not inferred display order—for:

- animation routines (for example walk → stop → turn → action);
- preconditions and postconditions such as held/released prop and facing;
- object/furniture triggers that invoke routines;
- room/floor/backdrop placement and logical surface/contact anchors;
- character, object and backdrop scale/z-order relationships.

Use exact stable asset ids. A routine is a versioned directed sequence of clips
and transition rules, not a hard-coded animation name string in a UI component.
Expose an inspectable graph/table and flag missing clip, missing bridge,
incompatible pose/outfit, impossible anchor/contact, or unresolved asset id.
Do not change gameplay wiring automatically; production binding remains an
explicit reviewed proposal.

6. Context preview

Provide one screen where the reviewer can place a selected keeper animation,
room/backdrop, and relevant furniture/object at their declared logical anchors
and scale. It must preview routine playback, first/last-frame contacts, prop
handoffs, z-order and crop bounds. Use the existing data where reliable; show
unmapped/missing relationships rather than guessing. The preview is review-only
until an explicit downstream production change is approved.

7. Frame duplicator/mover foundation

Do not build an unrestricted pixel editor in this first workbench delivery.
Instead prepare a safe foundation: frame selection, onion-skin viewing,
duplicate-frame proposal, frame order/timing proposal and logical translation
proposal. Each is recorded as a draft request with exact input frame(s), output
frame count and intended geometry. The next dedicated task may turn these
requests into a constrained draft sprite editor with undo and deterministic
repacking. No canonical strip may be changed by this foundation.

8. Handoff, safety and delivery

Extend Hand back to Codex so it submits annotations, asset reviews, crop/anchor
proposals, animation requests, routines and relationship proposals together in
one durable, exact-id batch. Preserve the online-only reviewer as the single
source of truth; do not add an offline review mode or a second browser storage
origin. Add deterministic verifiers for every new schema and every
sprite-sheet proposal invariant. Update README, handoff documents, architecture
notes and the prioritized backlog. Verify with focused unit tests, the existing
catalogue/sprite verifiers, typecheck, production build, public deployment and
live route checks. Commit and push to remote main, deploy, and report the
finished commit, deployment and known limitations.

For this first delivery, report a concise proposed data model and UI map before
implementing any mutable-draft tool. If a required asset mapping, runtime
trigger, crop rule or user intent is genuinely ambiguous, preserve existing
art/data and present it as a review decision rather than guessing.
```

## Deliberately deferred generic product work

After the Keeper workbench is proven, generalisation can separate project
adapters (sprite-sheet conventions, manifest format, runtime bindings) from the
shared review core (assets, variants, annotations, routines, contexts, requests
and handoff queue). Do not perform that extraction in the first workbench task.
