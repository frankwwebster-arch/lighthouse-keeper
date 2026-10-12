# Standard turn full-face endpoints — V1

Status: **awaiting Frank's explicit visual approval; production unchanged**.

This first two-animation batch covers `keeper_turn_front` and `keeper_turn_left_front` only. In each strip, F5's oversized smiling head is replaced inside the declared head/face mask with the exact approved neutral pixels. F1–F4 and F6 are byte-identical to canonical production; F6 was already byte-identical to the approved neutral. The standard body, hands, legs, timing, turn direction, floor anchor and sidecar contract remain unchanged outside the mask.

No image-generation call was used: the approved canon is transplanted deterministically. The rejected face-camera provenance and deleted `keeper_count_money` amendment were not used.

Rebuild with the bundled Pillow runtime:

```sh
/Users/frank/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 scripts/build_keeper_full_face_turn_endpoints.py
node scripts/verify_keeper_full_face_turn_endpoints.ts
```

Rollback: delete `art/drafts/keeper-full-face-standard-turn-endpoints-2026-10-12-v1` and `public/keeper-review/full-face-standard-turn-endpoints-v1` only.
