# Bubble stories ligne-claire BBQ pilot V1

This immutable, reversible pack records Frank's approved ligne-claire
direction on six existing BBQ pictures. He approved the contact sheet on
21 October 2026 with “agreed, these are superb”. It translates the prior
current pictures' drawing language without changing what they depict.

| Picture | Preserved content |
| --- | --- |
| `bbq-grill-unlit` | compact open round grill, cold coals, same viewpoint |
| `bbq-grill` | same grill model and viewpoint, lit coals |
| `bbq-charcoal` | open bag, visible coals, loose lumps and flame motif |
| `bbq-sausages` | five linked raw sausages, no plate |
| `bbq-hotdogs` | two overlapping served hot dogs with mustard |
| `bbq-tongs` | diagonal closed tongs, blue grips and hanging loop |

The generated sources are deterministically reduced to small per-picture flat
palettes, normalised into 256 × 256 RGBA cells and given at least 20 pixels of
transparent gutter. The builder pins the SHA-256 of every current reference so
the comparison cannot silently drift.

`evidence/current-vs-ligne-claire-contact-sheet.png` shows prior-current and pilot
pictures side by side on warm cream, pilot pictures on dark ink, and both at
64 px. All six approved components are registered as later immutable versions
and are current in the Studio picture list. Every earlier version remains
byte-identical and selectable for undo.

Two loose-charcoal attempts are retained under `rejected/`. Frank rejected
them because they removed the current asset's bag and therefore redesigned the
content instead of refining its style.

Rebuild with:

```sh
/Users/frank/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 scripts/build_activity_story_ligne_claire_bbq_pilot_v1.py
```

The user-supplied comic images were used only as high-level evidence for flat
ink, spot colour, panel grammar and reaction marks. No character, setting,
panel, lettering or exact arrangement is reproduced.
