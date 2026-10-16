# Keeper Prime seated six-view V1

Status: **draft foundation awaiting Frank's visual approval**. Nothing is in
Final, runtime or production.

This pack establishes the six neutral seated endpoints from which the actual
standing-to-sitting, sitting-to-standing and seated action animations will be
built:

- direct front;
- direct back;
- strict side-left and side-right;
- rear-left and rear-right three-quarter.

“At an angle either side” is interpreted as the rear three-quarter pair. That
is the useful neutral for television, gaming and other activities where the
Keeper must face furniture while remaining readable to the player.

All six candidates occupy a 256 × 320 (32 × 40 logical pixel at density 8)
cell, share the `[16,40]` floor anchor and `[16,29]` seat point, and use the
standard 11-logical-pixel seat height. Their registered alpha bounds are
exactly 264 pixels high, from y=52 through y=315, leaving a four-pixel bottom
safety gutter. Side-left is an exact registered-pixel mirror of side-right;
rear-left is the same exact mirror of rear-right. No separate redraw can
introduce scale drift into either pair.

The approved Prime front, side-right, rear-right and back standing views are
the identity, palette and rendering authorities. First-generation seated
neutrals are retained only as pose and seat-contact references. Four new
smooth transparent sources were made with the built-in image-editing workflow,
then registered deterministically with Lanczos resampling. Every original and
candidate SHA-256 is pinned in `batch-register.json`.

After approval, build transition clips in three review gates: side-right and
its exact mirrored left partner; front and back; then the rear-three-quarter
pair. Each clip must use the approved planted-ankle rig, preserve the relevant
standing authority as frame 1, and land byte-exactly on the corresponding
endpoint in this pack. Timing stays tunable in the review tool. Furniture and
chair art remain separate object-owned layers.

Review: `/keeper-review/keeper-prime-seated-six-view-v1/`.

