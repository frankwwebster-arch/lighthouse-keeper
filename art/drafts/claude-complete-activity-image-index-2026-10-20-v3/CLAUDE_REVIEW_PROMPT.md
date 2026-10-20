# Claude Code complete-image review prompt V3

Review every image produced or assembled in this task. Start at:

`art/drafts/claude-complete-activity-image-index-2026-10-20-v3`

Read `image-ledger.json` first. It maps all 37 original image generations and
points to four immutable asset packs:

- `art/drafts/claude-activity-cloud-review-pack-2026-10-20-v1`
- `art/drafts/claude-bbq-food-asset-pack-2026-10-20-v1`
- `art/drafts/claude-bbq-tools-ephemera-pack-2026-10-20-v1`
- `art/drafts/claude-kitchen-condiments-prep-pack-2026-10-20-v1`

Read every pack's `README.md`, `CLAUDE_REVIEW_PROMPT.md`, manifest and evidence.
Inspect all 104 review-ready independent assets. Acknowledge rejected and
unselected generations as provenance, but do not recommend promoting them.

Do not modify, regenerate, promote or deploy anything. Treat all Prime,
Kitchen, runtime and inherited pack authorities as immutable.

Return:

- confirmation that all 37 chat generations are represented;
- confirmation that all 104 usable independent assets were accessible;
- any missing, corrupt or ambiguous mapping;
- visual findings using the detailed prompts in the four source packs;
- choreography suggestions combining pantry, preparation, tools and activity marks;
- an explicit untouched-files list.
