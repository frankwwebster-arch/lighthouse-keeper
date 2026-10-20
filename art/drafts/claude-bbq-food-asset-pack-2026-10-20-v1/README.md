# Claude BBQ and food asset pack V1

This immutable, review-only folder gives Claude Code direct access to eight
independent transparent activity-callout assets:

1. `assets/bbq-raw-burger-patties.png`
2. `assets/bbq-sausages.png` — raw linked sausage string
3. `assets/bbq-grill.png` — cold and unlit
4. `assets/cooking-cheese-slicing.png`
5. `assets/bbq-raw-steak.png`
6. `assets/meal-steak-fries.png`
7. `assets/condiment-ketchup-bottle.png`
8. `assets/condiment-mustard-bottle.png`

All usable assets are 256 × 256 RGBA PNGs with at least 20 transparent pixels
of gutter. Their 384 × 384 review sources, exact generation provenance, hashes,
and one rejected cooked-sausage attempt are included. Each final object remains
independently controllable.

Food-state rule: loose ingredients and food awaiting cooking are unplated;
plates are reserved for finished meals. This is why the raw steak, patties and
sausages stand alone while the steak-and-fries outcome uses a plate.

Nothing here is approved or promoted. The prior plated sausages and lit BBQ are
unchanged and hash-pinned as proposed supersession authorities. Runtime, Prime,
Kitchen and deployment are untouched.

Claude should read `CLAUDE_REVIEW_PROMPT.md` and inspect
`evidence/final-assets-contact-sheet.webp`, the individual files in `assets/`,
and `asset-manifest.json`.

Verification:

```sh
/Users/frank/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 scripts/build_claude_bbq_food_asset_pack_v1.py
node scripts/verify_claude_bbq_food_asset_pack_v1.mjs
```
