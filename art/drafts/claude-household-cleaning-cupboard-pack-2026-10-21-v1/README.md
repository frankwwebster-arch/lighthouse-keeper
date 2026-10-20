# Claude household cleaning-cupboard pack V1

This immutable, review-only folder gives Claude Code direct access to 26
independently controllable household-cleaning activity-callout props.

Cleaning products and machine supplies:

1. bleach;
2. disinfectant;
3. multi-surface spray;
4. glass spray;
5. furniture polish;
6. washing-up liquid;
7. washing-powder box and its scoop as one semantic group;
8. liquid laundry detergent;
9. fabric conditioner;
10. stain remover;
11. dishwasher-tablet tub and its contents as one semantic group;
12. dishwasher salt;
13. dishwasher rinse aid;
14. angled-neck toilet cleaner.

Tools, protection and consumables:

15. dustpan;
16. hand brush;
17. broom;
18. string mop;
19. bucket;
20. rubber-glove pair;
21. cellulose sponge;
22. scouring pad;
23. microfiber cloth;
24. feather duster;
25. handheld scrub brush;
26. bin-bag roll.

Every usable asset is under `assets/` as a 256 × 256 RGBA PNG with at least 20
transparent pixels of gutter. The dustpan and hand brush are separate files.
Packaging is generic and text-free. Compact 384 × 384 lossless review sources,
original PNG hashes and geometry, exact prompts, output hashes, and a contact
sheet are retained.

All 36 generation outputs from this cleaning task are represented: 26 accepted
sources and ten visibly unsuitable glow/field attempts retained under
`evidence/rejected/` for provenance. Rejected evidence is not a candidate asset.

The Kitchen and BBQ-tools contact sheets are hash-pinned style references only.
Nothing here is approved or promoted. No Kitchen, Prime or runtime authority is
changed, and nothing is deployed.

Claude should read `CLAUDE_REVIEW_PROMPT.md`, then inspect
`evidence/final-assets-contact-sheet.webp`, every file under `assets/`,
`asset-manifest.json`, and `PROMPT_LOG.md`.

Verification:

```sh
/Users/frank/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 scripts/build_claude_household_cleaning_cupboard_pack_v1.py
node scripts/verify_claude_household_cleaning_cupboard_pack_v1.mjs
```
