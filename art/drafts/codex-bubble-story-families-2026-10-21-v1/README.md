# Codex Bubble-story family expansion V1

This immutable source pack adds 54 independently selectable pictures to the
Bubble stories studio. It expands seven practical and playful areas:

| Family | New pictures |
| --- | ---: |
| Fishing | 6 |
| Garden | 6 |
| Pet care and play | 6 |
| Repair and tools | 12 |
| Pub | 8 |
| Art | 8 |
| Scientific and inventing | 8 |

Every final under `assets/` is a 256 × 256 RGBA PNG with a measured minimum
20-pixel transparent gutter. Each picture owns one object, animal or ordinary
semantic set. `source/` preserves a compact 384 × 384 lossless WebP derivative
of every accepted built-in image-generation result; `source-register.json`
pins the original generated PNG filename, geometry and SHA-256.

The first easel candidate touched the source canvas edges and was rejected. Its
identity and reason remain in the register; the accepted rerender has complete
clearance. No existing picture version or approved authority was overwritten.

The pack is part of the complete Bubble-story catalogue. Rebuild and verify it
with:

```sh
/Users/frank/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 scripts/build_codex_bubble_story_families_v1.py
node scripts/import_activity_story_picture_catalogue.mjs
npm run verify:activity-stories
```

The contact sheet at `evidence/final-assets-contact-sheet.webp` shows every
normalised cell on a checkerboard. The studio groups are intentionally separate
so Frank and Claude can browse Fishing, Gardening, Pet care and play, Fixing
things, Pub, Art, and Scientific and inventing without searching “Other”.
