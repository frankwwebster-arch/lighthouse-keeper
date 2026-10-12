# Keeper rear-drumming hand-plane correction — 12 October 2026 v2

This reversible amendment addresses Frank's annotated review of
`keeper_play_drums_back`: frame 6 places both hands and crossed sticks behind
the Keeper's back. The replacement must keep both hands in the playable
front/side plane and connect naturally between frames 5 and 7.

Only frame 6 may be authored. Canonical raw/runtime art and the complete 11
October draft remain unchanged until explicit promotion.

## Image-edit provenance

The corrected full-character source pose was made with the built-in image
editing tool in `precise-object-edit` mode. No CLI/API fallback was used.

Final prompt:

> Correct only the arm, hand and drumstick action in frame 6. Remove the hands
> and crossed drumsticks from behind the Keeper's lower back. Repose both
> forearms so they wrap forward naturally at the outer sides of his torso
> toward an unseen drum kit. The hands must be partly occluded by the body from
> this rear view, never displayed across the back. Keep one wooden drumstick in
> each hand and make this a transitional low stroke between frame 5 and frame
> 7. Preserve the rear-facing character, cap, hair, head, torso, cream stripe,
> waistband, trousers, legs, boots, proportions, palette, outline style and
> transparent background. Exactly two hands and two sticks; no drum kit, extra
> props, text, shadow or background.

Input roles: frame 6 was the edit target; frames 5 and 7 were the immediately
adjacent motion references. `build.py` alpha-crops and height-matches the
result to the reviewed v1 frame-6 geometry, while frames 1–5 and 7–8 are copied
byte-for-byte from v1.

## Pinned hashes

- Canonical strip: `a280e810808293c475755329cb85f008e0b134ec8b74430de119a8a212393adb`
- 11 October v1 strip: `ff9057711d7f866a51bb8e38e777eaa6bcea855a2d4b5e5de6241c16fc33f85b`
- Generated frame-6 correction: `1a100944bcffc6f3434ee609ef7d15c53e697a2af40b4d8498124cccb7850e10`
- Review draft strip: `275f716e57ac1bcfa77da0cd646c8b3a72746a9963449b4be5bf465088d47d52`

Run `python3 build.py` from this directory to reproduce the normalized draft,
contact sheet, animated preview, frame evidence and register. Rejection remains
fully reversible by removing this directory and its single registry entry.
