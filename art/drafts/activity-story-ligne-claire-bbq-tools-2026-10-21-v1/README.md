# Bubble stories ligne-claire BBQ tools continuation V1

This immutable pack translates the seven BBQ-tools pictures not covered by the
approved `bbq-tongs` pilot version. Frank approved the contact sheet on 21
October 2026 with “approved”. The candidates are registered as current V2
versions; each V1 remains byte-identical and selectable for rollback.

| Picture | Preserved content | Approved version |
| --- | --- | --- |
| `bbq-basting-brush` | orange silicone head, pale collar and blue holed handle | V2 |
| `bbq-charcoal-bag` | closed blue/orange bag with three-lump motif | V2 |
| `bbq-charcoal-chimney` | filled perforated cylinder and right heat-shielded handle | V2 |
| `bbq-grill-fork` | two steel tines and blue two-rivet handle | V2 |
| `bbq-heatproof-mitt` | blue quilted mitt with orange cuff and loop | V2 |
| `bbq-skewer-bundle` | three pointed skewers with blue loop handles | V2 |
| `bbq-slotted-turner` | four-slot blade and blue two-rivet handle | V2 |

`evidence/current-vs-ligne-claire-contact-sheet.png` shows the prior-current
picture, candidate on warm cream, candidate on dark ink, and both versions at
64 px for every id. `batch-register.json` pins all current, source, component
and evidence hashes and records measured alpha bounds, gutters and palettes.

`data/activity-stories/pictures.json` references each component in place from
this pack. Registration added one immutable V2 per id and changed only the
library's current selectors. Roll back by selecting V1; do not overwrite or
remove either version.

The two retained rejected attempts have visually correct three-skewer and
four-slot counts, but their prompts incorrectly asserted four and five. An
enlarged source audit corrected those facts, after which both pictures were
rerendered with accurate provenance.

Build and verify with:

```sh
/Users/frank/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 scripts/build_activity_story_ligne_claire_bbq_family_2026_10_21_v1.py tools
/Users/frank/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 scripts/build_activity_story_ligne_claire_bbq_family_2026_10_21_v1.py tools --verify
```

The built-in image generator supplied the source drawings one at a time. The
builder then performed deterministic fixed-palette normalisation; it did not
repaint, repair or invent missing source content.
