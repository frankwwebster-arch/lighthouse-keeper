# Prime richer activity-cloud choreography V1

**Date:** 20 October 2026

**Status:** immutable reversible review candidate awaiting visual review; not approved, promoted or deployed

## Outcome

V1 preserves the approved Prime Rear Action Sequence V1 exactly:

```text
16 approved walk poses → 4 approved deceleration poses
→ 8 approved turn-to-rear poses → all 24 Prime rear-work poses
```

The 52 sequence records, every referenced Keeper hash, the fixed turn/action
root, and the exact rear-neutral frames at the turn endpoint and action
F1/F23/F24 are inherited byte-for-byte. Activity Cloud Composer V6 remains the
unchanged object vocabulary.

Only the separate review callout is new. Four examples are included:

- Garden BBQ: grill arrival, charcoal feed, meat flip and cooked resolution;
- sandwich assembly: bread, staggered ingredient stack, compression and final
  sandwich;
- washing up: plate, liquid and droplets, sponge scrub and clean cutlery;
- general repair: toolbox, hull patch, hammer strike, wrench turn and secured
  knot.

Each story has its own open/no-bubble staging and compact bubble staging. The
bubble option is not a container around the open paths: its positions,
silhouettes, entry arcs, crossings and settled composition are separately
authored.

## Deterministic motion and layer control

Every treatment has both full and reduced-motion data. Each mode contains 42
explicit frames at 8 fps. Every object and symbol record declares its owner,
role, x/y position, scale, rotation, opacity and z-order. The common story
grammar is beginning, working phrase, resolution and frames 38–42 as a stable
five-frame quiet tail. Reduced motion uses held story poses, at most one
primary/result and one secondary object, no rotation and no more than one
symbol at a time.

The review independently controls:

- Prime body;
- hero/result object layer;
- supporting-object layer;
- comic-symbol layer;
- open/bubble treatment marks;
- contextual SFX declaration;
- treatment, speed, loop and reduced-motion mode;
- synchronized timeline and body/cloud frame stepping;
- path-overlay and exact current-frame transform diagnostics.

All unique body, object and symbol image URLs preload and decode before any
control unlocks or playback begins. The callout stays hidden until action F1
and remains raised above the cap.

## New owned symbols

One generated 1536 × 1024 RGBA source sheet supplies six semantic owners:

- `symbol-heat-curls`;
- `symbol-sizzle-spark`;
- `symbol-motion-ticks`;
- `symbol-water-droplets`;
- `symbol-soap-bubbles`;
- `symbol-impact-star`.

The accepted source has zero alpha-greater-than-8 pixels on all outer/shared
cell boundaries and measured source gutters of 85–120 pixels. Deterministic
normalisation produces separate 256 × 256 cells with at least 20 pixels of
transparent gutter, zero edge alpha, zero ambiguous pixels and zero unowned
pixels. Exact prompts, two rejected attempts and the accepted source hash are
recorded in the versioned `PROMPT_LOG.md`.

## Review and verification

Local review route:

```text
/keeper-review/keeper-prime-rear-action-choreography-v1/index.html
```

The route is deliberately undeployed. Production/external-browser availability
is not expected without separate deployment permission.

Build with the repository's Pillow-capable Python environment, archive only
this review set, then verify:

```bash
python3 scripts/build_keeper_prime_rear_action_choreography_v1.py
npm run archive:keeper-review:set -- art/drafts/keeper-prime-rear-action-choreography-2026-10-20-v1/batch-register.json HEAD
npm run verify:keeper-prime-rear-action-choreography-v1
```

The verifier checks the approved sequence and authority bytes, V6 catalogue
hash and inherited object hashes, source-sheet geometry/ownership/gutters,
component hashes/gutters, all sixteen explicit timelines, full/reduced-motion
rules, five-frame stable quiet tails, controls, preload/decode gate, page
syntax, archive entries and all pinned source/page/builder/verifier hashes.

## Files and rollback

- Draft/source/register:
  `art/drafts/keeper-prime-rear-action-choreography-2026-10-20-v1/`
- Review shell/catalogue:
  `public/keeper-review/keeper-prime-rear-action-choreography-v1/`
- Archive set:
  `review-archive/sets/keeper-prime-rear-action-choreography-v1.json`
- Builder/verifier:
  `scripts/build_keeper_prime_rear_action_choreography_v1.py` and
  `scripts/verify_keeper_prime_rear_action_choreography_v1.mjs`

Rejection is reversible by deleting only those versioned files, the six new
content-addressed objects and the documentation/package references. No Prime,
Composer V6, runtime, Final or Kitchen source must be reconstructed or changed.

## Documentation audit

The final 20 October audit reconciled this document, README, decisions,
authoring standard, dynamic-choreography brief and the approved-sequence
document with the delivered catalogue, controls, archive paths and verification
commands. They consistently record four examples, six symbols, sixteen
explicit timelines, local-only review, no approval, no runtime/Final/Kitchen
change and no deployment. No setup, recovery or production instructions were
changed because this candidate is a removable review layer only.
