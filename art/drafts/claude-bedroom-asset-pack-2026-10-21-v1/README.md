# Claude bedroom activity-bubble pack V1

This immutable, review-only folder gives Claude Code direct access to 26
independently controllable, generic and timeless bedroom props. It does not add
furniture, people, room context or branded products.

Sleep and bedside objects:

1. twin-bell alarm clock;
2. bedside lamp;
3. folded pyjamas;
4. bedroom-slipper pair;
5. covered hot-water bottle;
6. sleep eye mask.

Clothing and personal items:

7. sock pair;
8. leather-shoe pair;
9. folded shirt;
10. necktie;
11. leather belt;
12. flat cap;
13. reading glasses;
14. wristwatch;
15. wallet;
16. two house keys on one ring;
17. pocket notebook;
18. fountain pen.

Grooming and quiet leisure:

19. comb;
20. hairbrush;
21. electric shaver;
22. cologne bottle;
23. deodorant stick;
24. over-ear headphones;
25. hardcover book;
26. portable bedside radio.

Every usable asset is under `assets/` as a 256 × 256 RGBA PNG. Visible alpha
is proportionally fitted within 216 × 216 pixels, centred without distortion,
and separated from every edge by at least 20 fully transparent pixels. Natural
pairs or groups—the slippers, socks, shoes, glasses, keys and headphones—are
single semantic units; tools and unrelated items remain separate files.

`source/` preserves one 384 × 384 lossless WebP review source per accepted
generation. `source-register.json` records the original generated PNG cache
filename, geometry, SHA-256 and exact subject request. All 26 generated
candidates passed alpha and visual screening, so no rejected attempt exists;
that zero-rejection result is explicit rather than represented by invented
provenance.

The primary visual reference, its prompt log and the previous complete bubble
catalogue are hash-pinned in `asset-manifest.json`. `protected-authorities.json`
pins aggregate hashes for all tracked Kitchen, Prime, animation, deployment and
existing Composer-page authorities at the start commit. The verifier recomputes
those memberships and hashes and rejects unrelated committed paths.

The labelled checkerboard sheet is
`evidence/final-assets-contact-sheet.webp`. Nothing in this folder is approved
or promoted. Runtime assets, Kitchen, Prime, animation authorities, deployment
configuration and every existing Composer page remain unchanged. No deployment
was performed.

Build and verification:

```sh
/Users/frank/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 scripts/build_claude_bedroom_asset_pack_v1.py
node scripts/verify_claude_bedroom_asset_pack_v1.mjs
```

Recorded result (21 October 2026): the final contact sheet was visually
inspected at original resolution; all 26 props passed silhouette, transparency,
ownership and small-scale readability review. The pack verifier passed with
26/26 sources and finals represented, visible bounds no larger than 216 × 216,
gutters of at least 20 pixels, complete hash coverage and all five protected
authority groups unchanged. The V5 complete-index verifier passed with 99/99
generated outputs and 115/115 bubble-ready assets represented.

The repository-wide test chain was also exercised after fast-forwarding to the
latest `origin/main`: the review archive passed at 44.90 MiB, all Kitchen,
Prime, animation and archive gates passed, and all 229 Vitest tests passed.
After the final upstream kettle update, `npm test` passed again with the review
archive at 44.93 MiB and all 19/19 Vitest files and 229/229 tests passing.

Documentation audit (21 October 2026): the pack README, manifest, prompt log,
review prompt, source register and V5 complete index describe the delivered
review-only state. The repository root README, product behaviour, setup,
deployment guide and backlog remain accurate because this delivery adds no
runtime, UI, deployment or approved-authority behaviour.
