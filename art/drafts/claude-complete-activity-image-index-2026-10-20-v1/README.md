# Claude complete activity-image index

This is the authoritative entry point for every image generated or assembled in
this Codex chat through 20 October 2026.

It covers:

- all **15 original image-generation outputs** from this chat;
- all **82 review-ready independent assets** assembled from the activity-cloud
  and BBQ/food work;
- every accepted source, rejected source, unselected intermediate, contact
  sheet, Prime body frame, activity object and comic/action symbol in the two
  immutable Claude packs.

No large image is duplicated unnecessarily. `image-ledger.json` maps each of
the 15 generator cache filenames and original SHA-256 values to its tracked
repository representation. Thirteen were already represented; the two omitted
early generic-symbol attempts are now retained under
`recovered-unselected-generations/` as compact lossless WebP review copies.
Their original PNG hashes and dimensions remain in the ledger. They are
provenance only, not candidate assets.

The two complete asset roots are:

- `../claude-activity-cloud-review-pack-2026-10-20-v1` — 74 usable images,
  including Prime frames, activity objects and all comic/action symbols;
- `../claude-bbq-food-asset-pack-2026-10-20-v1` — 8 usable BBQ/food images.

Claude Code should start with `CLAUDE_REVIEW_PROMPT.md`, then read
`image-ledger.json` and the two linked pack manifests. The ledger takes
precedence only for chat-wide coverage and per-generation source geometry; it
does not alter either immutable pack.

Verification:

```sh
node scripts/build_claude_complete_activity_image_index_v1.mjs
node scripts/verify_claude_complete_activity_image_index_v1.mjs
```
