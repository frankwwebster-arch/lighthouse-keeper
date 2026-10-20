# Claude complete activity-image index V3

This is the authoritative entry point for every image generated or assembled
in this Codex chat through the Kitchen condiments and preparation batch on
20 October 2026.

It covers:

- all **37 original image-generation outputs** from this chat;
- all **104 review-ready independent assets** across four immutable packs;
- accepted sources, rejected or unselected provenance, contact sheets, Prime
  body frames, activity objects, symbols, BBQ food and tools, Kitchen pantry
  items and preparation tools.

The four complete asset roots are:

- `../claude-activity-cloud-review-pack-2026-10-20-v1` — 74 usable assets;
- `../claude-bbq-food-asset-pack-2026-10-20-v1` — 8 usable assets;
- `../claude-bbq-tools-ephemera-pack-2026-10-20-v1` — 8 usable assets;
- `../claude-kitchen-condiments-prep-pack-2026-10-20-v1` — 14 usable assets.

V1 and V2 remain byte-unchanged. `image-ledger.json` carries their mappings
forward and adds the fourteen Kitchen generation outputs. No large image is
duplicated.

Claude Code should start with `CLAUDE_REVIEW_PROMPT.md`, then read
`image-ledger.json` and each linked pack's review prompt and manifest.

Verification:

```sh
node scripts/build_claude_complete_activity_image_index_v3.mjs
node scripts/verify_claude_complete_activity_image_index_v3.mjs
```
