# Bubble stories ligne-claire washing family V1

**Status:** immutable review gate; awaiting Frank's approval; not registered

This pack translates the five `washing` pictures used by Claude's existing
`washing-up` Bubble story into the approved ligne-claire language. The current
V1 pictures remain the semantic and compositional authority. The approved
`sandwich-tomato` V2 is the primary calibration for confident contour,
restrained flat colour and selective game-scale detail; approved BBQ artwork
is supporting style authority only.

| Picture id | Preserved content | Proposed version |
| --- | --- | --- |
| `washing-plate` | one oval cream plate, blue double rim and existing bubbles | V2 |
| `washing-liquid` | one green squeeze bottle, cap construction and existing bubbles | V2 |
| `washing-sponge` | one yellow/orange sponge, modest front-left foam and five detached bubbles | V2 |
| `washing-droplets` | exactly four rinse-water droplets in the existing arrangement | V2 |
| `washing-cutlery` | one three-pronged fork and one spoon, crossed with the spoon in front | V2 |

`evidence/current-vs-ligne-claire-contact-sheet.png` shows, for every id, the
prior-current V1, proposed V2 on warm white, proposed V2 on dark, V1 at 64 px
and proposed V2 at 64 px. Nothing in `data/activity-stories/pictures.json` has
been changed at this gate.

Three rejected attempts are retained under `rejected/`: a plate with excessive
tonal modelling, a sponge with excessive foam/bubbles, and a cutlery pass whose
image was sound but whose prompt incorrectly described the current three-prong
fork as four-tined. `PROMPT_LOG.md` records every exact prompt and rejection.

The deterministic builder crops visible alpha, scales into a 216 px target,
maps the result to a fixed flat palette, integer-centres it in a transparent
256 × 256 RGBA cell, measures at least a 20 px gutter, pins prior/source/output
hashes, and rebuilds the five-column contact sheet. It also pins Claude's
unchanged `washing-up.json` story hash.

```bash
/Users/frank/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 scripts/build_activity_story_ligne_claire_washing_2026_10_21_v1.py
/Users/frank/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 scripts/build_activity_story_ligne_claire_washing_2026_10_21_v1.py --verify
```

After explicit approval, add each component with the official
`activity-stories:add-picture` command so it becomes immutable V2. Never
overwrite V1, and do not edit the story or `src/activityStories/` runtime.
