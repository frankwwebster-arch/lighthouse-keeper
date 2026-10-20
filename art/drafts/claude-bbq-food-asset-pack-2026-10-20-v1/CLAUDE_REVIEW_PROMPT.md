# Claude Code review prompt

Review the immutable pack at
`art/drafts/claude-bbq-food-asset-pack-2026-10-20-v1`.

Do not modify, regenerate, promote or deploy any file. This is a visual/model
review only.

Inspect `evidence/final-assets-contact-sheet.webp`, every PNG under `assets/`,
`asset-manifest.json`, and `PROMPT_LOG.md`. Assess:

1. consistency with the established Lighthouse Keeper activity-callout style;
2. immediate reduced-size readability and clean transparent silhouettes;
3. whether the raw patties, raw linked sausages and raw steak read unmistakably
   uncooked;
4. whether the BBQ reads unmistakably cold and unlit;
5. whether cheese being sliced reads as an action rather than a static cheese
   object;
6. whether the steak-and-fries plate reads as the finished outcome of the raw
   steak state;
7. whether the ketchup and mustard work as a matched pair while remaining
   independently controllable;
8. adherence to the food-state rule: loose ingredients are unplated and plates
   are reserved for finished meals;
9. any likely overlap, scale, hierarchy or choreography problems when these
   assets move through bubble and open-radial treatments.

Return:

- overall verdict: approve / approve with changes / redraw;
- strongest aspects;
- Critical, Important and Optional issues;
- one short note per asset;
- precise choreography suggestions for a raw → cooking → plated BBQ story;
- a list of files that should remain untouched.

Treat all prior assets and all Prime/Kitchen/runtime authorities as immutable.
