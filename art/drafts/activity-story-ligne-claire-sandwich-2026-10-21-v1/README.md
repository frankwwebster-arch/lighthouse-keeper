# Bubble stories ligne-claire sandwich family V1

This immutable, reversible review pack translates the complete five-picture
sandwich story set into the approved ligne-claire language. It contains the
four `sandwich` ingredients and the existing `cooking-sandwich` result used by
the same story. The pack is **unapproved**: all five library pictures remain on
their byte-identical V1 versions, and no story or runtime file has changed.

| Picture | Preserved content | Proposed version |
| --- | --- | --- |
| `sandwich-bread` | two overlapping square white-bread slices | V2 |
| `sandwich-ham` | two stacked folded ham slices with curled ends | V2 |
| `sandwich-lettuce` | three overlapping ruffled lettuce leaves | V2 |
| `sandwich-tomato` | one whole tomato and two overlapping slices | V2 |
| `cooking-sandwich` | two triangular finished sandwiches with lettuce, tomato and ham | V2 |

`evidence/current-vs-ligne-claire-contact-sheet.png` shows, for every id, the
prior current image, candidate on warm cream, candidate on dark ink, and both
versions at 64 px. `batch-register.json` pins every prior, source, component,
rejection and evidence hash and records measured alpha bounds, gutters,
palettes and ownership.

Three finished-sandwich attempts are retained under `rejected/`. The first two
drifted from triangular quarters into square full-slice sandwiches. The third
restored the triangular construction but invented cheese that is absent from
the current asset. The accepted source preserves the triangular pair and
removes the extra filling.

Build and verify with:

```sh
/Users/frank/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 scripts/build_activity_story_ligne_claire_sandwich_2026_10_21_v1.py
/Users/frank/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 scripts/build_activity_story_ligne_claire_sandwich_2026_10_21_v1.py --verify
```

Stop at the contact-sheet gate. If Frank approves this exact sheet, add each
component as a new immutable V2 with the activity-story picture tool. Until
then, rejection remains reversible by discarding only this directory.

The built-in image generator supplied one transparent source at a time. The
builder then performed deterministic fixed-palette normalisation; it did not
repaint, repair or invent missing source content.
