# Claude BBQ tools and ephemera pack V1

This immutable, review-only folder gives Claude Code direct access to eight
independent transparent activity-callout props.

Tools:

1. `assets/bbq-tongs.png`
2. `assets/bbq-slotted-turner.png`
3. `assets/bbq-basting-brush.png`
4. `assets/bbq-grill-fork.png`

Ephemera:

5. `assets/bbq-heatproof-mitt.png`
6. `assets/bbq-charcoal-chimney.png`
7. `assets/bbq-skewer-bundle.png`
8. `assets/bbq-charcoal-bag.png`

All usable assets are 256 × 256 RGBA PNGs with at least 20 transparent pixels
of gutter. The compact 384 × 384 lossless review sources, exact generation
prompts, original generated PNG hashes and geometry, asset hashes, and contact
sheet are retained. Each final prop remains independently controllable.

The existing BBQ food pack is a hash-pinned style authority only. Nothing here
is approved or promoted. No existing asset, runtime file, Prime authority,
Kitchen work, or deployment state is changed.

Claude should read `CLAUDE_REVIEW_PROMPT.md` and inspect
`evidence/final-assets-contact-sheet.webp`, each file under `assets/`, and
`asset-manifest.json`.

Verification:

```sh
/Users/frank/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 scripts/build_claude_bbq_tools_ephemera_pack_v1.py
node scripts/verify_claude_bbq_tools_ephemera_pack_v1.mjs
```
