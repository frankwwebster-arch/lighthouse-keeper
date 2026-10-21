# Bubble stories ligne-claire spirit-level correction V1

**Status:** review gate awaiting approval

Frank rejected the first repair hand-tools spirit level as “too cartoonish”
while approving the other seven tools. This separate immutable pack corrects
only `repair-spirit-level`; the rejected drawing remains preserved in the
original eight-tool pack and the current V1 remains registered.

The correction retains exactly one low horizontal teal level and three vial
stations in the same order and orientations: vertical left, horizontal centre,
diagonal right. It removes the inflated casing, porthole-like housings, giant
screw heads, neon/gloss, decorative damage and game-icon bevels. The replacement
uses a thinner straight adult-tool extrusion, restrained functional fittings,
fine mostly-even ink, subdued flat spot colour and minor human line variation.

`evidence/current-vs-correction-contact-sheet.png` shows current V1, the
candidate on warm white, the candidate on dark, V1 at 64 px and the correction
at 64 px. The candidate is unregistered pending Frank's approval.

Three rejected sources are retained: the original too-cartoonish drawing, a
first correction that remained too polished and visually overbuilt, and a
second correction whose technical restraint became illegibly thin at 64 px.
Exact prompts and reasons are in `PROMPT_LOG.md`.

```bash
/Users/frank/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 scripts/build_activity_story_ligne_claire_repair_spirit_level_correction_2026_10_21_v1.py
/Users/frank/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 scripts/build_activity_story_ligne_claire_repair_spirit_level_correction_2026_10_21_v1.py --verify
```

On approval, register this exact component as immutable V2 with the official
add-picture command. Never overwrite V1 and do not edit Claude's story or
`src/activityStories/` runtime.
