# Keeper carry-shopping right-bag correction — 12 October 2026 v2

This reversible amendment addresses Frank's annotated review of
`keeper_carry_shopping`: the right-hand shopping bag is missing in frames 1 and
7 even though it is present through the surrounding gait.

The authored changes are confined to frames 1 and 7. Frames 2–6 remain
byte-identical to the 11 October amendment draft. The earlier builder made
frame 8 a byte-identical loop endpoint of frame 1, so corrected frame 1 is
copied to frame 8 to prevent the bag vanishing on the final beat. Canonical
raw/runtime art and the complete v1 draft remain unchanged until explicit
promotion.

## Image-edit provenance

The two corrected full-character source poses were made with the built-in image
editing tool in `precise-object-edit` mode. No CLI/API fallback was used.

Frame 1 prompt:

> Add the missing tan paper grocery bag to the character's forward/right hand,
> matching its size, handle, groceries, outline and painterly pixel style to
> the adjacent frame-2 reference. Keep the complete character pose, cap, face,
> beard, jumper, rear/left-hand bag, legs, proportions and transparent
> background unchanged. Add no other objects and no text.

Frame 7 prompt:

> Add the missing tan paper grocery bag to the character's forward/right hand,
> matching its size, handle, groceries, outline and painterly pixel style to
> the adjacent frame-8 reference. Keep the complete character pose, cap, face,
> beard, jumper, rear/left-hand bag, legs, proportions and transparent
> background unchanged. Add no other objects and no text.

The generated full poses are retained as provenance. `build.py` normalizes each
pose to the reviewed v1 geometry, composites only the viewer-right lower
hand/bag quadrant over frames 1 and 7, and copies corrected frame 1 to frame 8.
This keeps the face, beard, torso, rear bag and unannotated gait frames from v1.

## Pinned hashes

- Canonical strip: `14f15ffb437c67ecf613190e7b6c3789c1352a01ca99cee0900af99fd8171128`
- 11 October v1 strip: `8300433ceac02037a105e4e1f97ca2975a3d007771a701a707178acdcc22cc3f`
- Frame 1 generated correction: `c5680c54146f8a30f3cb055ce9395510ea986efe2b1060b34b7d9c476b44343d`
- Frame 7 generated correction: `f673d6998545c6fbb97845b567d70a8e26316cd4c3bee001ed01e3c7881bba47`
- Review draft strip: `c0a38a128b3b14735bc8cd479e238c2c0f1fbd1a35f4f28fa86ca1807f02bc9c`

Run `python3 build.py` from this directory to reproduce the normalized draft,
contact sheet, animated preview, frame evidence and register. Rejection remains
fully reversible by removing this directory and its single registry entry.
