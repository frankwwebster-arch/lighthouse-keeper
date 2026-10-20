# Claude Code complete-image review prompt V2

Review every image produced or assembled in this task. Start at:

`art/drafts/claude-complete-activity-image-index-2026-10-20-v2`

Read `image-ledger.json` first. It maps all 23 original image generations and
points to three immutable asset packs:

- `art/drafts/claude-activity-cloud-review-pack-2026-10-20-v1`
- `art/drafts/claude-bbq-food-asset-pack-2026-10-20-v1`
- `art/drafts/claude-bbq-tools-ephemera-pack-2026-10-20-v1`

Read every pack's `README.md`, `CLAUDE_REVIEW_PROMPT.md`, manifest and evidence.
Inspect all 90 review-ready independent assets. Acknowledge rejected and
unselected generations as provenance, but do not recommend promoting them.

Do not modify, regenerate, promote or deploy anything. Treat all Prime,
Kitchen, runtime and inherited pack authorities as immutable.

Return:

- confirmation that all 23 chat generations are represented;
- confirmation that all 90 usable independent assets were accessible;
- any missing, corrupt or ambiguous mapping;
- visual findings using the detailed prompts in the three source packs;
- choreography suggestions that combine tools, ingredients and activity marks;
- an explicit untouched-files list.
