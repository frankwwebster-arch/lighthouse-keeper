# Claude complete activity-image index V2

This is the authoritative entry point for every image generated or assembled
in this Codex chat through the BBQ tools and ephemera batch on 20 October 2026.

It covers:

- all **23 original image-generation outputs** from this chat;
- all **90 review-ready independent assets** across three immutable packs;
- all accepted sources, rejected or unselected provenance, contact sheets,
  Prime body frames, activity objects, symbols, food, tools and BBQ ephemera.

The three complete asset roots are:

- `../claude-activity-cloud-review-pack-2026-10-20-v1` — 74 usable assets;
- `../claude-bbq-food-asset-pack-2026-10-20-v1` — 8 usable assets;
- `../claude-bbq-tools-ephemera-pack-2026-10-20-v1` — 8 usable assets.

V1 remains byte-unchanged. `image-ledger.json` carries its 15 mappings forward
and adds the eight tool/ephemera generations. No large image is duplicated.

Claude Code should start with `CLAUDE_REVIEW_PROMPT.md`, then read
`image-ledger.json` and each linked pack's review prompt and manifest.

Verification:

```sh
node scripts/build_claude_complete_activity_image_index_v2.mjs
node scripts/verify_claude_complete_activity_image_index_v2.mjs
```
