# Activity callout dynamic choreography — next review gate

**Recorded:** 20 October 2026
**Status:** V1 candidate built on 20 October 2026 and awaiting visual review; no choreography candidate is approved

## Starting authority

Prime Rear Action Sequence V1 is the immutable continuity authority for:

```text
approved walk → stop/deceleration → turn to exact rear neutral
→ complete 24-frame Prime rear-work action
```

Do not edit that candidate. Its simple orbit/bustle callout motion proved timing,
layer separation and placement, but it is not the final activity-cloud motion
language. Frank's direction is to make the cloud substantially more interesting
and dynamic, using the liveliness of the earlier Claude sketch as directional
inspiration while producing a more polished, deterministic result in the game's
established illustrated language.

## Next deliverable

Build three to five new immutable, reversible choreography examples over the
approved sequence. Start with a useful spread such as BBQ/cooking, sandwich
assembly, washing up and general repair. Each example must exist in both:

- an open, non-bubble composition; and
- a compact bubble/cloud composition.

The treatment is not merely a container switch. Each version needs authored
staging suited to its silhouette and available space.

## Motion language

The result must read as a tiny visual story, not an inventory halo. Use a clear
beginning, working phrase, resolution and quiet tail. Combine:

- a hero object that establishes the activity;
- supporting objects with purposeful mobile paths, not equal-speed rotation;
- associated comic symbols and marks—heat curls, sparks, droplets, bubbles,
  scent wisps, motion ticks, impact stars or musical notation as appropriate;
- object-to-object interactions, such as ingredients assembling into a
  sandwich, bubbles washing a plate, a tool striking or tightening a fastener,
  or food moving from preparation to cooked result;
- anticipation, acceleration, overshoot and settle;
- controlled crossings, depth changes, scale and rotation where they clarify
  the story;
- deliberate pauses and a clean five-frame quiet tail before the loop.

Avoid a constant carousel, equal spacing, uniform bobbing, simultaneous entry,
or a screen full of unrelated objects. Four or five semantic objects remain a
good default, but small supporting symbols are additional punctuation rather
than counted as full objects.

## Component and ownership rules

- Keeper body, activity objects, symbols/marks, bubble treatment and SFX remain
  independently controllable.
- No prop, icon, symbol, context or counter is baked into the Keeper.
- New symbols are first-class hash-pinned components with their own semantic
  owner; do not paint them into object cells merely for convenience.
- Every sprite cell must pass the existing deterministic transparent-gutter,
  connected-component ownership and metadata/geometry checks.
- Keep all existing Prime, route and Activity Composer V6 bytes unchanged.
- Timelines are deterministic and declared as data, including z-order, path,
  scale, rotation, opacity, timing and quiet-tail state.
- Provide reduced-motion playback that preserves the same story beats without
  continuous circling.

## Review requirements

The next page should show the approved synchronized sequence automatically and
allow recipe, bubble/non-bubble treatment, body, object layer, symbol layer,
SFX declaration, speed, loop and reduced-motion mode to be switched separately.
It must preload and decode every unique frame before playback.

Present at least one frame-by-frame or path-overlay diagnostic so mobile assets
and symbol ownership can be inspected rather than inferred. Pin every source,
generated component, timeline, page and verifier by SHA-256. The candidate must
be discardable by deleting only its new versioned directories and files.

## Browser delivery boundary

The existing V1 path is a local review route and was deliberately not deployed,
so it is not expected to load from the production site in an external browser.
Do not deploy the next review without explicit permission. If external review
is needed without deployment, add a separately versioned self-contained export
whose asset resolution does not depend on the app server; do not rewrite V1.

## Exclusions

Do not promote runtime or Final assets, change Kitchen work, alter the approved
sequence, or treat any new choreography as approved before explicit visual
review.

## Current candidate

`/keeper-review/keeper-prime-rear-action-choreography-v1/index.html` now implements this
gate as four immutable examples: Garden BBQ, sandwich assembly, washing up and
general repair. Each has separately authored open and bubble staging rather
than a shared path inside two containers. The 42-frame full-motion and
reduced-motion timelines are explicit catalogue data, including every object
and symbol's position, scale, rotation, opacity and z-order. Frames 38–42 are a
settled quiet tail.

Six new first-class symbols—heat curls, sizzle spark, motion ticks, water
droplets, soap bubbles and an impact star—come from one ownership-safe 3 × 2
source sheet. Each is separately hash-pinned and normalised to a 256 × 256
cell with at least 20 pixels of transparent gutter. The review can hide the
body, hero/result, supporting objects, symbols, treatment marks and SFX
declaration independently, switch speed/loop/reduced motion, and expose both a
path overlay and exact frame-state table.

The candidate inherits Prime Rear Action Sequence V1 and Composer V6
byte-for-byte. It is review-only, unapproved, unpromoted and undeployed. See
`docs/KEEPER_PRIME_REAR_ACTION_CHOREOGRAPHY_V1_2026-10-20.md`.

## Bubble refinement candidate

Frank preferred the bubble approach and requested a focused V2 refinement.
`/keeper-review/keeper-prime-rear-action-choreography-v2/index.html` preserves
the complete V1 open treatment and every inherited image hash, lightens the
bubble, aligns its connector with the Keeper's head, widens object lanes and
makes comic marks functional motion grammar. Each supporting object owns a
velocity-aligned tick trail and an interaction-timed contact star; these marks
remain independent from objects and treatment geometry. The verifier measures
58.0% more bubble-object travel and 38.9% greater working-phrase spacing than
V1 while retaining the five-frame quiet tail and reduced-motion limits.

V2 also supplies a self-contained 68-asset Claude Code model-test pack under
`art/drafts/keeper-prime-rear-action-choreography-2026-10-20-v2/`. It remains
review-only, unapproved, unpromoted and undeployed. See
`docs/KEEPER_PRIME_REAR_ACTION_CHOREOGRAPHY_V2_2026-10-20.md`.
