# Bubble stories ink marks and recipe pictures V1

**Status:** commissioned by Claude on Frank's behalf; all 39 pictures are
registered as immutable library versions and await Claude's contact-sheet
review and story wiring.

This pack implements
`docs/CODEX_PROMPT_BUBBLE_STORIES_INK_MARKS_AND_RECIPE_PICTURES_2026-10-22.md`.
It contains 29 Hergé black-ink marks and ten new recipe pictures. Older picture
versions remain untouched and selectable.

The binding rules are **one even black outline, flat colour, no shine** and
**ligne claire, not cartoon**. Marks use the ink stroke itself, with only the
brief's permitted flat accents. Every accepted picture passed the colour,
line, 64 px, gutter and ownership self-tests; marks also passed the 40 px and
colour-covered black-ink tests. The floor and side-table pairs share locked
normalisation geometry so each clean swap reads as the same object.

Review the exact accepted bytes in:

- `evidence/marks-pale-game-size-and-current-contact-sheet.png`
- `evidence/objects-light-dark-64-contact-sheet.png`

Three failed first attempts remain under `rejected/`: an overworked basket, an
independently redrawn muddy floor, and a textured dusty table. Their reasons
and hashes are recorded in `batch-register.json`.

Build or verify with:

```sh
/Users/frank/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 scripts/build_activity_story_ink_marks_and_recipe_pictures_2026_10_22_v1.py
/Users/frank/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 scripts/build_activity_story_ink_marks_and_recipe_pictures_2026_10_22_v1.py --verify
```

`HASHES.sha256` content-addresses the complete pack. Treat it as immutable;
any correction belongs in a fresh versioned directory.
