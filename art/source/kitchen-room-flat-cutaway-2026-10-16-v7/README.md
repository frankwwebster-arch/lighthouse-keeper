# Kitchen Room V7 source record

This review-only room redraw applies `flat-cutaway-v1` to the kitchen shell.
Kitchen V6 Option B furniture is the unchanged object baseline. The approved
straight-on room mockup and
`docs/KITCHEN_FLAT_CUTAWAY_PROJECTION_SPEC_2026-10-16.md` are the projection
authority.

The built-in image-generation tool produced
`reference/imagegen-flat-room-study.png` as a composition and material study.
It contributes no candidate pixels. The normalized prompt is retained in
`imagegen-prompt.txt`. Final room modules and the sink porthole are constructed
deterministically by `scripts/build_kitchen_room_flat_cutaway_v7.py` from
`data/kitchen_room_flat_cutaway_recipe.json`.

The builder writes only versioned source/raw/draft/review paths. It reads but
does not alter Kitchen V6 furniture, Keeper art, runtime sprites, Final or
manifests.
