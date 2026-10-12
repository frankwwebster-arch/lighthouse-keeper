# Keeper review amendments — 2026-10-11 v1

This directory is the reversible working area for handoff `d9081e53-2808-4b1f-8422-2df09cf38c3c`.

- Scope is limited to the 81 exact animation names in the immutable handoff snapshot.
- Canonical raw sprites, runtime sprites, manifests, and earlier active drafts remain unchanged.
- `generated/` stores immutable image-model output copied into the repository.
- `drafts/` stores normalized review candidates and sidecars once they pass frame-isolation checks.
- A candidate becomes production art only after a separate explicit promotion instruction.

The batch currently exposes 41 active amendment candidates. Thirteen generated
face-to-camera candidates were withdrawn by Frank on 12 October. Twelve remain
as rejected provenance; Frank explicitly ordered the complete
`keeper_count_money` amendment deleted and reverted to canonical.
`withdrawn-face-camera-drafts.json` is the exact hash and decision record. The other exact handoff names are either verified canonical
keeps or explicit iterative/deferred responses. `sync_review_registry.py`
publishes only registers whose status remains `active-review-draft`.

Frank's later annotated frame-2 correction for `keeper_party_hat_put_on_back`
is preserved as a separate sibling candidate in
`art/drafts/keeper-party-hat-put-on-back-hands-2026-10-12-v2/`; this batch's
first variant remains unchanged for direct comparison and rollback.

Frank's later annotated right-hand-bag correction for `keeper_carry_shopping`
is likewise preserved as a separate sibling candidate in
`art/drafts/keeper-carry-shopping-right-bag-2026-10-12-v2/`. It authors the
missing bag in frames 1 and 7 and synchronizes frame 8 to corrected frame 1 so
the established exact loop endpoint remains seamless. This batch's first
variant remains unchanged for direct comparison and rollback.

Frank's later annotated hand-plane correction for `keeper_play_drums_back` is
preserved as a separate sibling candidate in
`art/drafts/keeper-play-drums-back-hands-2026-10-12-v2/`. Only frame 6 changes:
the crossed hands and sticks are removed from the back plane and both forearms
wrap forward at the sides toward the unseen drum kit. This batch's first
variant remains unchanged for direct comparison and rollback.

Frank's supplied removal mask for `keeper_put_record` is preserved as a
separate sibling candidate in
`art/drafts/keeper-put-record-removal-2026-10-12-v2/`. Only the marked
floating-record regions in frames 5–8 become transparent; frames 1–4 and every
surviving v1 pixel remain byte-identical. This batch's first variant remains
unchanged for direct comparison and rollback.

Frank's follow-up clarification is preserved as a third sibling candidate in
`art/drafts/keeper-put-record-horizontal-frame5-2026-10-12-v3/`. Frame 5 again
holds one record between both hands, now edge-on and parallel to ground level;
frames 1–4 and 6–8 remain byte-identical to v2. Canonical, v1 and v2 remain
unchanged for direct comparison and rollback.

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
