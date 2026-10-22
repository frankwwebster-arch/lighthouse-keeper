# Mark-free toast slices V1

**Status:** Frank-requested immutable `toast-slices` V3

This pack removes the five detached action slashes below the approved toast
slices because those marks will be added separately. The connected two-slice
object is retained byte-for-byte. Approved marked V2 and legacy V1 remain in
the picture library for exact rollback; no story IDs or animation behaviour
change.

Build and verify both requested variants with:

```sh
/Users/frank/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 scripts/build_activity_story_requested_tea_toast_variants_2026_10_22_v1.py
/Users/frank/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 scripts/build_activity_story_requested_tea_toast_variants_2026_10_22_v1.py --verify
```
