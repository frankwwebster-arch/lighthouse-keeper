# Empty tea mug V1

**Status:** Frank-requested immutable variant

This pack adds `tea-mug-empty` without altering the approved filled `tea-mug`
V2 or any story that already uses it. The exact approved mug pixels are the
authority. Only the flat brown tea fill becomes the mug's existing flat cream;
silhouette, line, rim, handle, alpha and antialiasing remain byte-identical.

The first built-in image-editing attempt was rejected because it redrew the mug
and introduced tonal modelling. It is retained under `rejected/` as provenance;
the production candidate is the deterministic exact-pixel edit.

Build and verify both requested variants with:

```sh
/Users/frank/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 scripts/build_activity_story_requested_tea_toast_variants_2026_10_22_v1.py
/Users/frank/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 scripts/build_activity_story_requested_tea_toast_variants_2026_10_22_v1.py --verify
```

Rollback is selecting or removing this new picture ID only. No existing asset
is overwritten.
