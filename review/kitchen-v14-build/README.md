# Kitchen v14 review build

This folder is the review-only Kitchen v14 candidate authorised by the newest
GO note in section 19 of `docs/SPEC.md`. It is built from
`docs/layout/kitchen_v14_schematic.json` and does not alter the installed
kitchen or runtime.

The ordinary fridge, cupboards, sink, dishwasher-slot cupboard and cooker are
all exact 168 px / 1.0 m units. The 252 px range remains deferred. The dresser
and larder use their bespoke approved rectangles and all tall pieces pass the
rule that height may not exceed twice width.

Review these four files in `outputs/`:

- `kitchen-v14-assembled-room-1x.png`
- `kitchen-v14-contact-sheet.png`
- `kitchen-v14-three-scale.png`
- `kitchen-v14-door-light-contents-demos.png`

The contact sheet is the only assembled output with dashed future-upgrade
slots. The room itself contains tier-1 art only. Door leaves, complete interiors,
oven contents, oven light and status lamp overlays are separate in `states/`.

Rebuild and verify with Codex's bundled Python runtime (which includes Pillow):

```sh
/Users/frank/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 review/kitchen-v14-build/build_kitchen_v14.py
/Users/frank/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 review/kitchen-v14-build/verify_kitchen_v14.py
```

Status: review candidate. Stop for Frank; no runtime promotion.
