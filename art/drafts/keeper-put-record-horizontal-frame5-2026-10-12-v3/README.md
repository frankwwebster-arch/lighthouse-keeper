# Keeper put-record horizontal held-record correction — 12 October 2026 v3

This reversible amendment corrects only frame 5 of `keeper_put_record`. The
Keeper retains one record between both hands while bending, with the record
edge-on and parallel to ground level like frame 4. Frames 1–4 and 6–8 are
byte-identical to v2, so the record is still absent after its release in frames
6–8.

Canonical raw/runtime art, the complete 11 October v1 draft and the complete
12 October v2 draft remain unchanged until explicit promotion.

## Image-edit provenance

The exact v2 frame 5 was edited with the built-in image tool in
`precise-object-edit` mode. The exact v1 frame 4 supplied the held-record
orientation reference, and exact v2 frame 6 supplied the following pose. No
CLI/API fallback was used.

Final prompt:

> Use case: precise-object-edit
> Asset type: transparent single-frame game sprite
> Input images: Image 1 is the exact frame-5 edit target; Image 2 is the exact
> preceding frame-4 reference for the record orientation and hand contact;
> Image 3 is the exact following frame-6 reference for continuity.
> Primary request: In Image 1 only, restore one black vinyl record held
> securely between both of the Keeper's hands. The record must be
> edge-on/foreshortened as a thin horizontal oval and parallel to ground
> level, matching the orientation, size, black rim and red centre detail of
> Image 2. Preserve Image 1's bent-forward body pose.
> Constraints: change only the hands-and-record region; keep the Keeper's cap,
> face, beard, torso, arms, trousers, boots, scale, position, pixel-art style,
> transparent background, and all other pixels unchanged. The record remains
> connected to and supported by both hands. One record only. No detached or
> floating object. Do not rotate the record upright and do not show its full
> circular face. No background, text, shadow, crop, rescale, or watermark.

`build.py` normalizes the generated pose to the exact v2 frame-5 height and
cap/body alignment, then composites only the tight hands-and-record box
`(139, 78, 193, 118)`. It rejects any change in frames 1–4 or 6–8 and rejects
alpha on any shared cell edge.

## Pinned hashes

- Canonical strip: `a29da757c3217dcbe3f8bb6d16526e061f5ba9d8323705fd3f1054ddad315586`
- 11 October v1 strip: `bce7f629d26049b885cd9aab6b268b09487c222b9ca3f48ffbf2fb4845d61911`
- 12 October v2 strip: `56c6b1af150ea96c7cc37c7dc3c3c778137082ec97e1450d7c9bcee3fedfe354`
- Built-in edit: `949c7ee7c4287999b169449327fe199272b23938db67c050fee3cc0caae2a04c`
- Review draft strip: `5a1b160cf91db8c53edd4b5433fad767c49aac71cb818a4b099a62d5ee637157`

Run the bundled Python runtime against `extract_inputs.py`, then `build.py`, to
reproduce the exact edit inputs, normalized draft, contact sheets, animated
preview, frame evidence and register. Rejection remains fully reversible by
removing this directory and its single registry entry.
