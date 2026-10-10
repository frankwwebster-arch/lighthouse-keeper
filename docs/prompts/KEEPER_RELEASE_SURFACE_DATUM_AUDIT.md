# Keeper release-surface datum audit

## When to run this

Run this **third**, only after the canonical side-on beard/hand audit and the
exhaustive sprite-frame isolation audit have completed, passed their verifiers,
and are committed on remote `main`. This is a placement-contact audit, not a
beard or frame-packing pass; preserve both earlier audit results.

## Recommended model

Use **GPT-5.6 Terra with High reasoning**. The task requires frame-by-frame
visual classification, coordinate/contract reconciliation, ownership hand-off
checks and cautious reversible amendments across the whole animation library.

## Ready-to-paste prompt

```text
Continue the Lighthouse Keeper work in:

/Users/frank/Documents/ChatGPT/Lighthouse Keeper

Work from current remote `main`. This is the THIRD audit in a fixed sequence.
First confirm that the canonical beard/hand-occlusion audit and the exhaustive
sprite-frame isolation audit have each completed, passed their permanent
verifiers and been committed to remote main. If either prerequisite is missing,
stop and report it; do not combine or redo either audit.

Read: .cursor/rules/sprite-sheet-frame-isolation.mdc,
docs/KEEPER_ANIMATION_HANDOFF.md, docs/KEEPER_ASSET_SCALE.md,
docs/KEEPER_OBJECT_DIMENSIONS.md, data/keeper_asset_contract.json,
data/keeper_object_dimensions.json, and both preceding audit prompts.

Establish and enforce one permanent standard tabletop release datum in this
flat gameplay plane:

- floor = 0 logical pixels above the keeper walking plane;
- purple seat-contact guide = 11 logical pixels above floor;
- standard tabletop support surface = 19 logical pixels above floor: exactly
  8 logical pixels above the seat guide, tolerance 0.5 logical pixel.

This is the height of the supporting surface and the released prop's base, not
the top of a cake, plate, mug, record, stack or another object. A tall prop can
extend upward; its lowest supporting pixels must visibly meet the 19-pixel
tabletop with no gap, sinking or floating. Never scale the keeper to make a
contact fit; Frank's saved width/height remains authoritative.

Audit EVERY exact-name animation and derived/mirrored consumer that can place,
put down, set down, release, serve, lay, deposit or hand off a held prop to a
surface or object layer. Do not rely only on interaction names: search the
manifest, raw sidecars, contract, routes, comments and final strips. Include at
minimum `keeper_place_cake`, `keeper_meal_place_side`, `keeper_put_record`, all
hot-drink pickup/put-down routes, food/tray routes, shopping/prop put-downs and
any future or derived release action. Classify every candidate by exact
`keeper_*` name and frame as:

1. standard tabletop release (must use 19 px);
2. expressly different named physical surface (low coffee table, oven rack,
   floor, bed, turntable platter or workbench) with its own written datum; or
3. not a release action because the prop remains held.

Cake, plated meal and record placement need special scrutiny. If a record
player is table-mounted in gameplay, its released record must visibly land at
the 19-pixel tabletop datum; do not preserve the older 13-pixel turntable value
just because it exists. A genuinely lower or higher appliance must be given a
named surface datum and presented to Frank as a decision, never guessed.

Before changing art, produce an exact-name inventory and delta: animation,
holding/releasing/after-release frames, surface class, intended height, measured
base-contact height, keeper/object ownership, hand-off verdict and proposed
deterministic/art repair. Never associate a comment, contact or animation by
list position, filter order or display order.

For every table-height release inspect the final production strip frame by
frame. The held prop must stay supported by the correct hand until release; its
base must meet y=19 relative to the stable floor/feet anchor; the object-layer
prop must begin at that exact contact with no vertical pop, duplicate,
disappearance or float; and the hand only becomes empty after hand-off.
Preserve prop orientation, hand layering, beard silhouette, anatomy, cupboard
occlusion and frame-isolation gutters. Mirrors use the same height and a true
horizontal mirror. Do not force genuinely low/ground/oven/workbench/bed actions
onto the tabletop datum.

Draft-first is mandatory. For a real defect create
`art/drafts/keeper-release-surface-datum-<date>-v1/`, copy the current
canonical source and sidecar byte-for-byte, record canonical and draft SHA-256
values, and work only in that draft. Never overwrite `art/raw/`,
`public/sprites/`, the runtime manifest, immutable review exports or existing
previews. Show exact-name Canonical versus Draft cards with both hashes. Do not
create a draft for a passing sheet. Stop for Frank's explicit promotion choice;
rejection must be deleting that draft directory and registry entry only.

Verify the permanent `standardTabletopSurfaceHeightAboveFloor` contract value
of 19 and extend the verifier so future standard tabletop releases cannot
differ from 19 px by more than 0.5 px, lose a declared hand-off, or
assign a released component to two frames. Add an exact-name machine register
such as `data/keeper_release_surface_audit.json` and a human summary. The
reviewer must display the purple 11-pixel seat guide and a named 19-pixel
tabletop guide for relevant cards; they are visual aids, not resizing controls.

After the delta is stable, generate only affected draft strips, previews,
contact sheets and reviewer artifacts. Inspect final draft strips at 1x and
zoomed scale. Run the release-surface verifier, beard/hand verifier,
frame-isolation verifier, scale/identity audit, tests, typecheck and production
build. Commit and push only draft-only evidence, verifier and comparison-review
work to remote main, wait for Vercel success and verify the canonical reviewer
returns HTTP 200. Do not promote canonical art without Frank's explicit approval.

Report only: sheets inspected; table-height releases corrected in drafts;
different-surface cases needing a decision; verification; commit; deployment.
```
