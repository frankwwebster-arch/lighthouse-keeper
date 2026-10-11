# Canon keeper walk-to-snooker complete sequence — review draft

Status: **visually accepted by Frank on 2026-10-11 and registered as an active review-platform draft; not promoted to production**.

Frank accepted the complete half-speed sequence whose SHA-256 is `b5ae7a9cdf99918628c4a45867713bb9e738682e138f2a4302c82c3913b62e89`. That acceptance covers the walk-right → stop → reach → cue contact → snooker → release → neutral → turn → walk-left route shown in the preview. Nothing in canonical, raw, runtime, or review-platform assets has yet been replaced.

Frank subsequently authorized registration in the review platform. The generated `draft-register.json` attaches the complete route to the exact existing name `keeper_snooker` as an `active-review-draft`. This is a review-only comparison: it does not replace the canonical eight-frame strip, runtime sprite or manifest entry. The review platform's later manual verdict remains authoritative.

## Intended route

The half-speed review loop is:

1. canonical `keeper_walk_cycle_f9` facing right;
2. canonical `keeper_walk_stop_f5` ending on the exact canonical side-right neutral;
3. single reach, cue contact, lower, aim, two snooker strokes, rise, cue release;
4. the exact same canonical side-right neutral;
5. canonical turn from right to back, canonical bridge from back to left;
6. mirrored canonical walk-start and walk-cycle facing left.

The cue is intentionally introduced after the canonical stop and removed before the canonical turn. No legacy `keeper_snooker_f8` pixels are used.

## Immutable and authored inputs

Canonical strips and their SHA-256 values are recorded in `evidence/build-manifest.json`.

The accepted reach source is:

- `../keeper-standard-snooker-single-reach-2026-10-11-v1/generated/single-reach-pose-v5-fresh-two-arm-redraft.png`

The two robustness-test sources visually accepted by Frank are:

- `../keeper-standard-snooker-authoring-robustness-test-2026-10-11-v1/generated/cue-contact-v1.png`
- `../keeper-standard-snooker-authoring-robustness-test-2026-10-11-v1/generated/deep-lean-v1-failed.png` (the historical filename is retained; Frank explicitly accepted the image)

The two additional sources authored for this complete route are:

- `generated/mid-lean-v1.png`
- `generated/stroke-forward-v1.png`

Their exact ImageGen prompts are preserved verbatim as `PROMPT-MID-LEAN.txt` and `PROMPT-STROKE-FORWARD.txt`. Source and normalized SHA-256 values are in the build manifest.

## Reproducible normalization

Run:

```sh
/Users/frank/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 art/drafts/keeper-standard-snooker-complete-sequence-2026-10-11-v1/build_preview.py
```

All authored sources use one immutable source-to-preview scale, `0.14204545454545456`. Foreground is cropped at alpha 32, resized once with Lanczos, hardened to binary alpha at 128, and placed by the centre and baseline of the boots on the shared anchor `(128, 158)`. The script records every crop, resized dimension, placement, hash, alpha bounding box, and border-gutter check.

Canonical 128×160 frames are not rescaled. They are placed on the same anchor. Left-facing locomotion is a deterministic mirror of the mirror-safe canonical locomotion clips; the asymmetric left/back turn uses its dedicated canonical strip.

## Timing

- canonical 8 fps locomotion is shown at 4 fps (`250 ms` per frame);
- canonical 10.5 fps turns are shown at approximately 5.25 fps (`190 ms` per frame);
- authored action key poses are held for `500 ms` each for a readable half-speed method review.

This draft is deliberately reversible: rejecting it requires deleting this directory only.
