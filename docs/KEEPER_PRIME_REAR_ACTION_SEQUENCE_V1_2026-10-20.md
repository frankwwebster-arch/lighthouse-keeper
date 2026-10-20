# Prime walk → stop → turn → rear action sequence V1

**Date:** 20 October 2026

**Status:** exact sequence continuity approved and hash-pinned; separate richer choreography candidate built and awaiting review; not promoted or deployed

## What this review proves

V1 presents the requested sequence as one synchronized playback:

```text
approved walk → approved stop/deceleration → approved turn to 180° rear
→ complete 24-frame Prime rear-work action
```

The page ends after the action rather than continuing through the existing
reverse-turn/walk-away evidence. The route contains 52 body poses over 8.433
seconds:

- 16 exact approved walk poses at 10 fps;
- four exact approved deceleration poses at 12 fps;
- eight exact approved turn-away poses at 16 fps;
- all 24 Prime rear-work action poses at 4 fps.

The 180° turn endpoint, action F1, action F23 and action F24 are the same exact
approved rear-neutral bytes. The root remains fixed across the turn-to-action
seam and the complete action.

## Synchronized activity layer

The callout is hidden throughout walk, stop and turn. It begins on the first
rear-work action pose and follows one 42-frame, 8 fps phrase with a five-frame
quiet tail. V1 offers five rear-work-compatible sets:

- garden BBQ;
- sandwich assembly;
- washing up;
- making tea;
- general mending.

Both the open radial/no-bubble and compact bustle/bubble treatments remain
switchable. Body, callout, treatment, SFX declaration, timeline and looping are
separate controls. The body is silent, no prop or icon is baked into it, and no
counter or contextual surface has been added.

All Keeper frames and 256 × 256 activity components are inherited from the
hash-pinned Activity Cloud Composer V6 catalogue. V1 creates no new image
media; its page and catalogue are separately hash-pinned and discardable.

## Review and verification

Frank approved the synchronized walk → stop → turn → complete rear-action
result on 20 October 2026 after reviewing the generated preview. That approval
pins the exact sequence and its separable above-cap activity layer. It does not
make the current simple orbit/bustle choreography the final callout-motion
authority. The separate, unapproved Prime Rear Action Choreography V1
candidate now provides richer mobile assets, comic symbols and authored object
interactions without editing this sequence. See
`docs/ACTIVITY_CALLOUT_DYNAMIC_CHOREOGRAPHY_NEXT.md`,
`docs/KEEPER_PRIME_REAR_ACTION_CHOREOGRAPHY_V1_2026-10-20.md` and the
hash-pinned decision at
`docs/review/keeper-prime-rear-action-sequence-v1-approval-2026-10-20.json`.

Review locally or after an explicitly authorised deployment at:

```text
/keeper-review/keeper-prime-rear-action-sequence-v1/
```

The page decodes all 65 unique inherited images before unlocking controls and
automatically begins the complete sequence. Use Replay to restart from the
walk, or the timeline and pose buttons to inspect the exact turn/action seam.

Run:

```bash
npm run verify:keeper-prime-rear-action-sequence-v1
npm run verify:keeper-prime-rear-action-sequence-v1-approval
```

## Boundary and rollback

This review changes no Prime authority, Kitchen work, Final/runtime asset or
gameplay recipe. It does not deploy. Rejection requires deleting only the V1
draft directory, public review directory, builder, verifier and this document;
all inherited media remain untouched.
