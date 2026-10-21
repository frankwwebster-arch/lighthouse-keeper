# Bubble stories symbol redraws V1

Immutable, reversible source and normalized picture pack for the four Bubble
stories marks requested on 21 October 2026.

The pack contains new versions of `symbol-heat-shimmer`,
`symbol-pleasant-aroma`, and `symbol-welding-sparks`, plus the new
`symbol-clean-glint`. Nothing in an older pack is overwritten.

Run the deterministic builder with:

```bash
UV_CACHE_DIR=/tmp/lighthouse-uv-cache uv run --with pillow python scripts/build_activity_story_symbol_redraws_v1.py
```

The builder fits each generated source into a fresh 256 × 256 transparent cell,
targets a 20 px output gutter, records hashes and ownership geometry in
`batch-register.json`, and writes a light/dark inspection sheet under
`evidence/`. `data/activity-stories/pictures.json` is updated only through
`npm run activity-stories:add-picture`.

Rejected work can be rolled back by removing this pack and the corresponding
picture-library versions; older picture versions remain available.
