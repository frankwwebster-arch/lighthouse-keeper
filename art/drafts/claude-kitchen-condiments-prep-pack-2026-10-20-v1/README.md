# Claude Kitchen condiments and preparation pack V1

This immutable, review-only folder gives Claude Code direct access to fourteen
independent transparent activity-callout assets.

Pantry and seasoning:

1. `assets/condiment-wholegrain-mustard-jar.png`
2. `assets/condiment-pickle-jar.png`
3. `assets/condiment-mayonnaise-jar.png`
4. `assets/condiment-salt-mill.png`
5. `assets/condiment-pepper-mill.png`
6. `assets/ingredient-butter-block.png`
7. `assets/condiment-olive-oil.png`
8. `assets/condiment-raspberry-jam.png`
9. `assets/condiment-honey-pot.png`
10. `assets/condiment-malt-vinegar.png`

Preparation and tools:

11. `assets/prep-bread-slicing.png`
12. `assets/knife-chef.png`
13. `assets/knife-bread.png`
14. `assets/knife-paring.png`

All usable assets are 256 × 256 RGBA PNGs with at least 20 transparent pixels
of gutter. Compact 384 × 384 lossless review sources, exact generation prompts,
original PNG hashes and geometry, output hashes, and a contact sheet are
retained. Each final prop is independently controllable; the sliced bread is a
single intentional semantic action group.

The existing Kitchen preparation sheet and BBQ food pack are hash-pinned style
references only. Nothing here is approved or promoted. No existing Kitchen,
Prime or runtime authority is changed, and nothing is deployed.

Claude should read `CLAUDE_REVIEW_PROMPT.md` and inspect
`evidence/final-assets-contact-sheet.webp`, each file under `assets/`, and
`asset-manifest.json`.

Verification:

```sh
/Users/frank/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 scripts/build_claude_kitchen_condiments_prep_pack_v1.py
node scripts/verify_claude_kitchen_condiments_prep_pack_v1.mjs
```
