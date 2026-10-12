# Keeper review amendments — 2026-10-11 v1

This directory is the reversible working area for handoff `d9081e53-2808-4b1f-8422-2df09cf38c3c`.

- Scope is limited to the 81 exact animation names in the immutable handoff snapshot.
- Canonical raw sprites, runtime sprites, manifests, and earlier active drafts remain unchanged.
- `generated/` stores immutable image-model output copied into the repository.
- `drafts/` stores normalized review candidates and sidecars once they pass frame-isolation checks.
- A candidate becomes production art only after a separate explicit promotion instruction.

The batch currently exposes 41 active amendment candidates. Thirteen generated
face-to-camera candidates were withdrawn by Frank on 12 October and are retained
only as rejected provenance; `withdrawn-face-camera-drafts.json` is the exact
decision record. The other exact handoff names are either verified canonical
keeps or explicit iterative/deferred responses. `sync_review_registry.py`
publishes only registers whose status remains `active-review-draft`.

The party outfit rule is one red-and-cream conical paper party hat replacing the
navy cap; the hat does not expose or invent a bald dome and remains stable
across every retained side/rear pose.

## Face rule added during review

No retained side or three-quarter candidate may use a generic smile or open
grin. Action-specific mouth changes are allowed only when the action physically
requires them (for example, taking a bite), and must return to a restrained
endpoint. Frank subsequently rejected every newly rendered face-to-camera
candidate, so those candidates are not active even where they used the neutral
reference. Canonical front-facing art remains the comparison authority until a
later explicit direction.

## Rebuild order

Run the five `build_*_family.py` scripts, then
`withdraw_face_camera_drafts.py`, then `sync_review_registry.py`. Rebuild the
reviewer with `scripts/audit_keeper_scale.py` and verify it with
`npm run verify:keeper-review-drafts` plus
`scripts/verify_floor_asset_catalogue.py`.
