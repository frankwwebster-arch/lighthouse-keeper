# Bubble stories symbol colour semantics V1

This immutable, reversible pack responds to Frank's colour-language review on
21 October 2026. It gives each effect its own immediately readable story cue:

| Mark | New colour language | Library action |
| --- | --- | --- |
| Heat shimmer | coral-red, vermilion, orange and hot cream | add as V3 |
| Pleasant aroma | warm cream/blush curls carrying flowers and a sparkle | add as V3 |
| Welding sparks | electric blue-white, cyan and cobalt with tiny molten droplets | add as V3 |
| Cold snowflake | ice blue, cyan, white and storm-blue facets | add as new V1 mark |

The existing V1 and V2 picture files and the complete
`activity-story-symbol-redraws-2026-10-21-v1` pack remain byte-identical,
separate and selectable. Nothing is overwritten. The picture library merely
adds later immutable versions and points `current` at each latest drawing.

Every component is a 256 × 256 transparent PNG with at least 20 pixels of
measured clear gutter. `batch-register.json` records source/output hashes,
ownership, geometry, prompts and library intent. The light/dark contact sheet
is under `evidence/`.

An initial teal/coral two-ribbon aroma candidate was rejected after Frank
pointed out that colour alone did not say “good smell”. It remains under
`rejected/` as reversible provenance and is not added to the picture library.
The accepted version uses classic comic shorthand—graceful fragrance curls,
small flowers and a clean sparkle—in explicit contrast to the existing murky
green `symbol-foul-odour` mark.

Rebuild with:

```sh
/Users/frank/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 scripts/build_activity_story_symbol_colour_semantics_v1.py
```

The three V3 versions and the new cold V1 mark were registered only through
`npm run activity-stories:add-picture`. Verify them with
`npm run verify:activity-story-symbol-colour-semantics-v1` and
`npm run verify:activity-stories`.
