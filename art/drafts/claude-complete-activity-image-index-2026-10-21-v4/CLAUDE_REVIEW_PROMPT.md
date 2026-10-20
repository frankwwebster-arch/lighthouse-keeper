# Claude Code complete-image review prompt V4

Review every image produced or assembled in this task. Start at:

`art/drafts/claude-complete-activity-image-index-2026-10-21-v4`

Read `bubble-assets.json` first. It is the exact 89-image vocabulary that may
be placed inside activity bubbles and excludes Prime body frames, source-only
art and rejected evidence. Then read `image-ledger.json`; it maps all 73
original image generations and
points to five immutable asset packs:

- `art/drafts/claude-activity-cloud-review-pack-2026-10-20-v1`
- `art/drafts/claude-bbq-food-asset-pack-2026-10-20-v1`
- `art/drafts/claude-bbq-tools-ephemera-pack-2026-10-20-v1`
- `art/drafts/claude-kitchen-condiments-prep-pack-2026-10-20-v1`
- `art/drafts/claude-household-cleaning-cupboard-pack-2026-10-21-v1`

Read every pack's `README.md`, `CLAUDE_REVIEW_PROMPT.md`, manifest and evidence.
Inspect all 130 review-ready independent assets. Acknowledge rejected and
unselected generations as provenance, but do not recommend promoting them.

Do not modify, regenerate, promote or deploy anything. Treat all Prime,
Kitchen, runtime and inherited pack authorities as immutable.

Return:

- confirmation that all 73 chat generations are represented;
- confirmation that all 130 usable independent assets were accessible;
- confirmation that all 89 bubble-ready object and symbol images were accessible;
- any missing, corrupt or ambiguous mapping;
- visual findings using the detailed prompts in the five source packs;
- choreography suggestions combining food, preparation, cleaning tools and activity marks;
- an explicit untouched-files list.
