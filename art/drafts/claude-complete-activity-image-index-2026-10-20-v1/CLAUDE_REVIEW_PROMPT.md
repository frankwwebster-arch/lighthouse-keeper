# Claude Code complete-image review prompt

Review every image produced or assembled in this task. Start at:

`art/drafts/claude-complete-activity-image-index-2026-10-20-v1`

Read `image-ledger.json` first. It is the master map for all 15 original image
generations and points to the two complete immutable asset packs:

- `art/drafts/claude-activity-cloud-review-pack-2026-10-20-v1`
- `art/drafts/claude-bbq-food-asset-pack-2026-10-20-v1`

Read each pack's `README.md`, `CLAUDE_REVIEW_PROMPT.md`, manifest and evidence.
Inspect all 82 review-ready independent assets, not merely the eight food files.
Also acknowledge all rejected and unselected generations as provenance, but do
not recommend promoting them.

Do not modify, regenerate, promote or deploy anything. Treat all Prime,
Kitchen, runtime and inherited pack authorities as immutable.

Return:

- confirmation that all 15 chat generations are represented;
- confirmation that all 82 usable independent assets were accessible;
- any missing, corrupt or ambiguous mapping;
- visual findings using the detailed prompts in the two source packs;
- an explicit untouched-files list.
