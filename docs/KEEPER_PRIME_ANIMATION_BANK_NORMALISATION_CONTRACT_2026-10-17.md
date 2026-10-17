# Keeper Prime animation-bank normalisation contract

**Authority date:** 17 October 2026  
**Status:** mandatory for every new action-animation draft; no promotion is
authorised by this document.

## One Keeper, one measurable body

Every visible character frame must be derived from the approved **Prime
Keeper** authorities, not merely made to resemble the earlier character.
Existing animation artwork may contribute only motion information: joint
paths, weight shifts, contact order, prop timing and useful occlusion ideas.
It is never an authority for rendered anatomy, scale, colour, line weight,
face, beard, hair, cap, clothes or endpoints.

The following must remain stable unless an action makes a measured deviation
unavoidable:

- logical scale and registered floor anchor;
- cap top, badge, eyes, ears, beard base, shoulders, stripe boundaries, waist,
  hands, knees and boot-contact landmarks;
- Prime Keeper body volume, including the approved rotundity;
- standard-outfit blues, cream stripe, trouser and boot colours;
- smooth antialiasing and outline treatment;
- the approved face rules: adult restrained expression, solid dark
  rectangular eyes without glints, separate moustache, readable mouth and the
  established beard mass.

The approved standing, walking, stopping and turning frames are endpoint
authorities. A frame that is close by eye is not an endpoint match. The
registered entry and exit images must be byte-identical to the named approved
authority wherever no prop or occlusion requires otherwise. Any necessary
prop-bearing endpoint must retain the Keeper pixels exactly and declare the
prop pixels separately.

## Context is part of every action

No action may be reviewed as an isolated loop. Its candidate page must show
the complete route in which the game will use it:

1. an approved, phase-correct walk;
2. a real deceleration into the registered stop;
3. an approved turn when the action facing requires it;
4. a short posture or prop handoff only where necessary;
5. action entry, action and any repeatable action section;
6. a controlled action exit returning to the exact registered neutral;
7. an approved turn when required;
8. a phase-correct acceleration into walking away.

The complete route must be inspectable at a useful large scale and at the
declared game scale, with play/pause, previous/next frame, phase labels and
independent action-loop controls. Timing for locomotion/turns and timing for
the enjoyable action loop must remain independently adjustable.

Costume changes happen only behind the approved door occlusion. A costume
action therefore needs both a standard-Keeper door route and a complete
costume-specific neutral/action route; it does not require a visibly morphing
costume transition.

## Triage of earlier animation art

Each historical animation receives one of four treatments:

- **motion-skeleton candidate:** joint/contact paths may be measured and
  retained, but every Keeper pixel is redrawn as Prime Keeper;
- **partial motion salvage:** only a sound subset of timing, prop or limb
  mechanics survives;
- **full redraw:** no visible or motion authority is accepted;
- **held for dependency:** object, costume or environment geometry must be
  fixed before a meaningful action draft can be built.

Frank explicitly rejected the earlier swimming, gym and scuba families as
incongruous. They are **full redraw** families. Do not trace, rescale or
recolour those characters. Their files remain historical provenance only.

Previously withdrawn face-camera amendments remain rejected provenance. The
explicitly deleted `keeper_count_money` amendment must not be regenerated
without a new direct instruction.

## Mechanical acceptance gates

Every candidate must have deterministic evidence for:

- source, draft and registered SHA-256 values;
- cell size, density, frame count, timing and sidecar agreement;
- a transparent safety gutter on every cell edge;
- one unambiguous ownership set for actor, clothing, prop and effect pixels;
- fixed floor anchor and declared root motion;
- landmark deltas against the relevant Prime authority;
- palette drift in invariant standard-outfit regions;
- unchanged pixels outside the explicitly declared edit region when a
  surgical amendment is claimed;
- exact entry and exit endpoint hashes;
- continuity into the preceding and following approved clips;
- no prop pop, costume pop, scale flash or duplicate/missing limb;
- preload and decode of every unique review image before playback starts.

Visual acceptance remains essential: passing geometry does not prove natural
weight, organic motion, readable intent or good comic timing.

## Reversibility and release

Every proposal lives in a new versioned directory under `art/drafts/`, with a
register that identifies all authorities, hashes, prompts or construction
steps, declared edits and known risks. Canonical raw/runtime art, Final art,
existing drafts, immutable review exports and old review pages are never
overwritten. Nothing is promoted without Frank's explicit approval.

Review media must use the content-addressed archive. A batch is deployed only
after its complete review pages, deterministic checks, documentation audit and
ordinary commit are ready; the release then uses the repository's explicit
`[deploy]` workflow once for that review batch.

