# Bubble stories ligne-claire BBQ food continuation V1

This immutable, review-only pack translates the seven BBQ-family pictures not
covered by the approved six-picture pilot. It changes drawing language only:
the current picture for each id remains the semantic and compositional source.

| Picture | Preserved content | Proposed version |
| --- | --- | --- |
| `bbq-burgers` | two overlapping completed burgers with bun, lettuce, tomato and patty | V2 |
| `bbq-ketchup` | red squeeze bottle and cream bowl of ketchup | V2 |
| `bbq-lamb-chops` | two overlapping raw bone-in chops | V2 |
| `bbq-leg-lamb` | tied roast, rosemary and oval plate | V2 |
| `bbq-steak` | one long low irregular raw steak, plate-free | V2 |
| `bbq-raw-burger-patties` | three raw patties in a triangular overlap | V2 |
| `bbq-raw-steak` | one thick rounded rectangular raw steak, plate-free | V2 |

`evidence/current-vs-ligne-claire-contact-sheet.png` shows the prior-current
picture, candidate on warm cream, candidate on dark ink, and both versions at
64 px for every id. `batch-register.json` pins all current, source, component
and evidence hashes and records measured alpha bounds, gutters and palettes.

The pack is stopped at the contact-sheet gate. Nothing here has been added to
`data/activity-stories/pictures.json`; every existing picture version remains
current and byte-identical. Approval can be rejected by discarding this draft
directory alone.

Two first passes are retained in `rejected/`: the initial `bbq-leg-lamb`
drawing matched the source's three ties but came from a prompt that incorrectly
asserted four, and the first `bbq-steak` became too rectangular and confused
its read with `bbq-raw-steak`.

Build and verify with:

```sh
/Users/frank/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 scripts/build_activity_story_ligne_claire_bbq_family_2026_10_21_v1.py food
/Users/frank/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 scripts/build_activity_story_ligne_claire_bbq_family_2026_10_21_v1.py food --verify
```

The built-in image generator supplied the source drawings one at a time. The
builder then performed deterministic fixed-palette normalisation; it did not
repaint, repair or invent missing source content.
