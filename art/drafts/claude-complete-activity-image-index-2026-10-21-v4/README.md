# Claude complete activity-image index V4

This is the authoritative entry point for every image generated or assembled
in this Codex chat through the household cleaning-cupboard batch on 21 October
2026.

It covers:

- all **73 original image-generation outputs** from this chat;
- all **130 review-ready independent assets** across five immutable packs;
- a direct **89-image bubble-only catalogue** that excludes Prime body frames,
  source-only art and rejected evidence;
- accepted sources, rejected or unselected provenance, contact sheets, Prime
  body frames, activity objects, comic symbols, BBQ food and tools, Kitchen
  pantry/preparation props, and household-cleaning products and tools.

The five complete asset roots are:

- `../claude-activity-cloud-review-pack-2026-10-20-v1` — 74 usable assets;
- `../claude-bbq-food-asset-pack-2026-10-20-v1` — 8 usable assets;
- `../claude-bbq-tools-ephemera-pack-2026-10-20-v1` — 8 usable assets;
- `../claude-kitchen-condiments-prep-pack-2026-10-20-v1` — 14 usable assets;
- `../claude-household-cleaning-cupboard-pack-2026-10-21-v1` — 26 usable assets and ten rejected attempts retained for provenance.

V1, V2 and V3 remain byte-unchanged. `image-ledger.json` carries their mappings
forward and adds all 36 cleaning-task generation outputs. No large original is
duplicated.

Claude Code should start with `CLAUDE_REVIEW_PROMPT.md`, then read
`bubble-assets.json` for the exact bubble vocabulary, followed by
`image-ledger.json` and each linked pack's review prompt and manifest.

The requested reference link appears to have `and` accidentally appended to
`activity-cloud-composer-v5`. The canonical repository page is
`public/keeper-review/activity-cloud-composer-v5/index.html`; this handoff does
not rewrite or deploy that immutable page.

Verification:

```sh
node scripts/build_claude_complete_activity_image_index_v4.mjs
node scripts/verify_claude_complete_activity_image_index_v4.mjs
```
