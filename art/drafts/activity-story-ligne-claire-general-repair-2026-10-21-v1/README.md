# Bubble stories ligne-claire General repair family V1

**Status:** approved and registered as current V2

This pack translates the five object pictures used by Claude's existing
`general-repair` Bubble story into the approved ligne-claire language. The
current V1 pictures remain the semantic and compositional authority. The
approved `washing-plate` V2, `sandwich-tomato` V2 and this pack's
`repair-toolbox` V2 are co-equal style champions. The plate calibrates living
hand-drawn shape and controlled minor imperfection; the tomato calibrates flat
colour economy and selective readable detail; the tool chest calibrates
construction, detail hierarchy and confident object presence.

| Picture id | Preserved content | Proposed version |
| --- | --- | --- |
| `repair-toolbox` | one open blue toolbox, its brass fittings and visible tools | V2 |
| `repair-boat-hull-patch` | four hull planks, two battens, two straps, six fasteners and one mallet | V2 |
| `repair-hammer-nails` | one diagonal claw hammer and exactly three nails | V2 |
| `repair-wrench-cog` | one cog behind one combination spanner with its two-pin grip | V2 |
| `repair-rope-knot` | one compact knot with the current over-under route and two bound ends | V2 |

Frank approved this exact five-picture contact sheet on 21 October 2026 with
“approved. tool chest the best”, then clarified that “plate and tool chest and
tomato are the style-champions”. `evidence/current-vs-ligne-claire-contact-sheet.png` shows, for every id, the
prior-current V1, proposed V2 on warm white, proposed V2 on dark, V1 at 64 px
and proposed V2 at 64 px. All five candidates are registered as immutable
current V2 versions; every V1 remains byte-identical and selectable.

The recipe evolved during this family in two useful ways. First, ambiguous
counts and structures must be inspected enlarged before prompting: the hull
has four planks and six visible fasteners, not the initially inferred three
and four. Second, mechanical assemblies and knots require topology-level
preservation, not merely a generic category match. The plate's successful
minor imperfection remains deliberate: contours, rings and teeth may have
controlled hand-drawn asymmetry, while identity, construction, viewpoint,
parts, overlaps and readability remain exact.

Two rejected attempts are retained under `rejected/`: a hull pass whose image
was visually sound but whose prompt had incorrect counts, and an overcomplicated
rope pass that invented upper braided loops. `PROMPT_LOG.md` records every
exact prompt and rejection.

The deterministic builder crops visible alpha, scales into a 216 px target,
maps the result to a fixed flat palette, integer-centres it in a transparent
256 x 256 RGBA cell, measures at least a 20 px gutter, pins prior/source/output
hashes, and rebuilds the five-column contact sheet. It also pins Claude's
unchanged `general-repair.json` story hash.

```bash
/Users/frank/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 scripts/build_activity_story_ligne_claire_general_repair_2026_10_21_v1.py
/Users/frank/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 scripts/build_activity_story_ligne_claire_general_repair_2026_10_21_v1.py --verify
```

Rollback by setting any picture's `current` selector to V1 with the official
`activity-stories:add-picture` command. Never overwrite a version, and do not
edit the story or `src/activityStories/` runtime.
