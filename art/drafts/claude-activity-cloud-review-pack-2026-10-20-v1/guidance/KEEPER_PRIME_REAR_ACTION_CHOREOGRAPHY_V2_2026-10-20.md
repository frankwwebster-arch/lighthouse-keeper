# Prime rear-action bubble choreography V2

**Date:** 20 October 2026

**Status:** immutable reversible bubble-refinement candidate awaiting visual review; not approved, promoted or deployed

## Frank's direction

Frank preferred V1's bubble treatment and requested a focused refinement:

- lighten the main bubble slightly;
- move the connector bubble right so it clearly comes from the Keeper's head;
- increase object travel while reducing overlap;
- use more ticks and stars so the marks actively sell momentum and activity;
- provide a self-contained asset pack for a Claude Code model test.

V2 changes only that boundary. The approved 52-pose Prime sequence, every
Prime authority, all twenty activity-object images, all six symbol images and
V1's complete open/no-bubble timelines remain byte-for-byte unchanged.

## Bubble refinement

The warm bubble fill moves from 0.14 to 0.22 opacity. The 27-pixel connector
moves from local x=48 in V1 to x=168, aligning its centre with the cap/head
rather than floating to the Keeper's left.

Each story's three supporting objects now use distinct authored lanes. Short
sinusoidal acceleration/overshoot accents increase travel without becoming a
uniform carousel. Compared with V1, the deterministic verifier measures:

- 58.0% more full-motion object travel; and
- 38.9% greater mean visible-object spacing during the working phrase.

The five-frame quiet tail and reduced-motion limit of two objects and one
symbol remain unchanged.

## Momentum marks are functional

Ticks and stars are not ambient decoration. Every supporting object owns:

- a `directional-trail` tick instance positioned behind the object's actual
  frame-to-frame velocity and rotated to the travel direction; and
- a `contact-impact` star timed to its authored transfer/contact beat and
  positioned between the support and current hero/result anchor.

These six extra kinetic instances per story remain on the independently
switchable symbol layer. Each record declares `anchorInstance`; impact marks
also declare `interactionWith`. Hiding the marks removes the movement grammar
without changing object paths, Prime pixels or the bubble treatment.

## Claude Code model-test pack

The self-contained pack is:

```text
art/drafts/keeper-prime-rear-action-choreography-2026-10-20-v2/
  claude-code-model-test-pack/
```

Start with `README.md`, `asset-manifest.json` and
`CLAUDE_CODE_MODEL_TEST_PROMPT.md`. The pack contains 68 hash-pinned visual
inputs:

- 41 unique approved Prime body images;
- 20 activity-object images;
- six comic-symbol images; and
- the ownership-isolated symbol source sheet.

It also contains the V1/V2 catalogues, approved sequence metadata and activity
vocabulary. Every copied file is byte-equal to its declared repository source.
The pack is input-only; model output belongs in a new versioned directory.

## Review and verification

Local review route:

```text
/keeper-review/keeper-prime-rear-action-choreography-v2/index.html
```

Build and verify with:

```bash
python3 scripts/build_keeper_prime_rear_action_choreography_v2.py
npm run verify:keeper-prime-rear-action-choreography-v2
```

V2 adds no public image media, so it deliberately has no empty review-archive
set manifest. Its large explicit catalogue is stored as deterministic gzip in
`public/` while the readable full JSON remains in the draft and model-test
pack, avoiding another 1.23 MiB plain deployment file. Its page, catalogue,
predecessor hashes, builder, verifier and model-test manifest are pinned in the
V2 batch register. Browser verification
covered all four stories, bubble-by-default playback, all 67 decoded runtime
image URLs, connector geometry, layer controls and zero console errors.

## Files and rollback

- Draft, register and model-test pack:
  `art/drafts/keeper-prime-rear-action-choreography-2026-10-20-v2/`
- Review page/catalogue:
  `public/keeper-review/keeper-prime-rear-action-choreography-v2/`
- Builder/verifier:
  `scripts/build_keeper_prime_rear_action_choreography_v2.py` and
  `scripts/verify_keeper_prime_rear_action_choreography_v2.mjs`

Rejecting V2 requires deleting only these V2 files, its package command and
documentation references. V1, approved Prime authorities, Composer V6,
runtime, Final and Kitchen remain untouched.

## Documentation audit

The 20 October audit reconciled this record, README, the dynamic-choreography
brief, decisions, package commands and generated register/catalogue. They agree
that V2 is a bubble-only review refinement, the V1 open treatment and all image
authorities are exact, the model pack contains 68 verified visual inputs, and
no runtime, Final, Kitchen or deployment change occurred.
