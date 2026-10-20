# Activity callout dynamic choreography — next review gate

**Recorded:** 20 October 2026
**Status:** approved follow-up direction; no candidate has been built or approved

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
