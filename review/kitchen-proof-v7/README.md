# Kitchen proof v7 — whole-room pre-cut review

This folder is the review-only result of the 27 October 2026 Kitchen v7 GO
notes in section 19 of `docs/SPEC.md`.

Open these first:

1. `outputs/kitchen-v7-free-room-with-prime-precut.png` — the 2048 × 576
   freely painted room with the unchanged Prime Keeper at 1:1 for scale.
2. `outputs/calibration-vs-kitchen-v7-precut.png` — the approved line-quality
   calibration beside the candidate.
3. `TECHNICAL_REPORT.md` — the complete art, geometry, layer and post-approval
   cut plan for Claude.
4. `PROMPT_LOG.md` — built-in image-generation references and prompt history.

## Approval boundary

This is deliberately the last stage before cutting. There is no `parts/`
directory, no production item sprite, no runtime manifest and no canon change.
The door/state demonstrations requested in the same GO block cannot truthfully
be made from identical body and door bytes until the approved paint has been
cut into layers. They are therefore specified precisely in the report and are
the first post-approval operation, not faked with independently redrawn state
images.

## Rebuild and verify

The final source is `sources/kitchen-v7-free-pass-05-final.png`. The builder
normalises it to the room canvas, restores structural geometry and exact key
colour, and composites the Prime Keeper without scaling:

```sh
python3 review/kitchen-proof-v7/build_review.py \
  --finalize review/kitchen-proof-v7/sources/kitchen-v7-free-pass-05-final.png
python3 review/kitchen-proof-v7/verify_review.py
```

The script needs Pillow. On a Codex desktop runtime, use the bundled Python if
the system Python does not provide it.
