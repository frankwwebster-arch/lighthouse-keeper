# Standard turn full-motion redraw — V2

Status: **awaiting Frank's explicit visual approval; production unchanged**.

V2 replaces the rejected F5-only transplant approach with a complete moving-model redraw for frames 1–5 of `keeper_turn_front` and `keeper_turn_left_front`. Both sequences use the approved full-face model as their identity authority. Frame 6 is restored byte-for-byte from the approved canon, and frame 5 is constrained to the same baseline, centreline, opaque height and near-matching width so the final rotational step cannot become a model-swap jump.

The generated source sheets were created with the built-in image-generation tool. The exact prompts, input hashes and source hashes are recorded in `batch-register.json`. Normalization into 128×160 cells is deterministic, binary-alpha and gutter-checked. Native width is retained; any extra rotundness remains a separate review-app scale choice.

V1 remains unchanged as rejected historical evidence. No raw/runtime sprite, manifest, prior draft or immutable review export was overwritten.

Rebuild:

```sh
/Users/frank/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 scripts/build_keeper_full_face_turn_redraw_v2.py
node scripts/verify_keeper_full_face_turn_redraw_v2.ts
```
