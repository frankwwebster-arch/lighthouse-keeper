# Claude complete activity-image index V5

This immutable, review-only index extends V4 with the complete bedroom prop
task from 21 October 2026.

It covers:

- all **99 original image-generation outputs** represented across the linked
  activity-asset work;
- all **156 review-ready independent assets** across six immutable packs;
- a direct **115-image bubble-only catalogue** that excludes Prime body frames,
  source-only art and rejected evidence;
- all 26 accepted bedroom sources and finals, with no rejected bedroom attempt.

V4 and every earlier pack remain byte-unchanged. V5 adds only the new bedroom
pack inventory, its 26 accepted generation records and the 26 final PNGs in
`bubble-assets.json`. The earlier catalogue and ledger are hash-pinned.

Claude Code should begin with `CLAUDE_REVIEW_PROMPT.md`, then read
`bubble-assets.json` for direct asset locations and `image-ledger.json` for full
generation provenance. The canonical reference Composer page is recorded for
context only; no existing Composer page was edited or deployed.

Verification:

```sh
node scripts/build_claude_complete_activity_image_index_v5.mjs
node scripts/verify_claude_complete_activity_image_index_v5.mjs
```
