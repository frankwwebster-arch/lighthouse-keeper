# Bubble stories ligne-claire repair hand-tools family V1

**Status:** review gate awaiting approval

This pack translates eight closely related hand tools from the `repair` picture
family into the approved ligne-claire language. It is the first pack built
after Frank's clarification that the washing plate, sandwich tomato and repair
tool chest are co-equal style champions. Their roles remain distinct:

- plate: living hand-drawn shape and controlled minor imperfection;
- tomato: flat-colour economy and selective readable detail;
- tool chest: construction, detail hierarchy and confident object presence.

The governing distinction for this set is **ligne claire, not cartoon**.
Candidates use credible adult-tool proportions, working mechanisms, mostly-even
near-black ink, flat opaque spot colour and minimal decisive construction
lines. Cute rounding, toy inflation, caricature, mascot cues, sticker rims and
decorative exaggeration are rejection conditions.

| Picture id | Preserved content | Proposed version |
| --- | --- | --- |
| `repair-adjustable-spanner` | adjustable jaws, worm screw, two-pin grip and hanging hole | V2 |
| `repair-c-clamp` | C frame, threaded screw, pressure pad and T handle | V2 |
| `repair-combination-pliers` | serrated jaws, cutting notch, pivot and two separated grips | V2 |
| `repair-flat-head-screwdriver` | slotted tip, long shaft, ferrule and teal fluted handle | V2 |
| `repair-phillips-screwdriver` | cross-head tip, long shaft, plain ferrule and coral handle | V2 |
| `repair-hand-saw` | tapering blade, fine tooth row, tip hole and two-fastener handle | V2 |
| `repair-spirit-level` | brass-ended body and exactly three correctly oriented vial stations | V2 |
| `repair-tape-measure` | blue case, belt clip, controls and one extended hooked tape | V2 |

`evidence/current-vs-ligne-claire-contact-sheet.png` shows each prior-current
V1, candidate V2 on warm white, candidate V2 on dark, V1 at 64 px and V2 at
64 px. No candidate is registered before Frank approves this exact sheet;
every V1 remains current and byte-identical.

One rejected Phillips pass is retained under `rejected/`: it invented a round
button on the brass ferrule and made the cross-head tip read as a broad diamond
spear. The accepted targeted correction removes that hardware and restores the
current construction. `PROMPT_LOG.md` records every exact prompt.

The deterministic builder crops visible alpha, scales into a 216 px target,
maps each source to a fixed flat palette, integer-centres it in a transparent
256 x 256 RGBA cell, measures at least a 20 px gutter, pins prior/source/output
hashes, verifies one-owner geometry, and rebuilds the five-column sheet.

```bash
/Users/frank/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 scripts/build_activity_story_ligne_claire_repair_hand_tools_2026_10_21_v1.py
/Users/frank/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 scripts/build_activity_story_ligne_claire_repair_hand_tools_2026_10_21_v1.py --verify
```

On approval, add each candidate as immutable V2 with the official
`activity-stories:add-picture` command. Never overwrite V1, and do not edit any
story or `src/activityStories/` runtime file.
