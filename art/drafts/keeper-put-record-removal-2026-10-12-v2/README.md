# Keeper put-record masked removal — 12 October 2026 v2

This reversible amendment applies Frank's supplied removal mask to
`keeper_put_record`. The floating/detached record is removed from frames 5–8;
all unmarked Keeper pixels and frames 1–4 remain from the reviewed 11 October
draft.

Canonical raw/runtime art and the complete v1 draft remain unchanged until
explicit promotion.

## Image-edit provenance

The supplied target and mask were processed with the built-in image editing
tool in `precise-object-edit` mode. No CLI/API fallback was used.

Final prompt:

> Use Image 2 as an exact removal mask for Image 1. In Image 1, erase every
> pixel/object covered by the four white shapes in Image 2, corresponding to
> the detached/floating vinyl-record areas in frames 5, 6, 7 and 8. Make the
> erased regions genuinely transparent. Preserve every pixel outside the
> white mask exactly, including all eight Keeper poses, hands, clothing, faces,
> proportions, positions, spacing, frame order, dimensions and transparency.
> Do not repaint, shift, rescale, crop or regenerate the characters. No fill,
> shadow, text, watermark, background or opaque replacement patch.

The built-in result correctly identified the four intended objects but also
re-rendered unmarked RGB pixels, so those generated RGB pixels are not used in
the review draft. `build.py` reads only the four largest original-alpha to
generated-transparent components inside the marked regions, maps them through
the exact v1 normalization, and makes those v1 pixels transparent. Every
surviving production pixel is copied byte-for-byte from v1.

## Pinned hashes

- Canonical strip: `a29da757c3217dcbe3f8bb6d16526e061f5ba9d8323705fd3f1054ddad315586`
- 11 October v1 strip: `bce7f629d26049b885cd9aab6b268b09487c222b9ca3f48ffbf2fb4845d61911`
- Original generated source: `1274071793997e1b2ff26ac20ae0aa1bd982588b3bb87c2f0e5b7ea043ce57a1`
- Built-in mask interpretation: `0eb254069cd6afc983fd574c1e92a6fdf1b2cf95b7e9627f7195cf1daee40420`
- Deterministically cleaned source: `5b64a17e4c8425a5c1f625c1718f0b15f01efd0e88dc569bcbebc86f71fde449`
- Review draft strip: `56c6b1af150ea96c7cc37c7dc3c3c778137082ec97e1450d7c9bcee3fedfe354`

Run `python3 build.py` from this directory to reproduce the source mask,
normalized draft, contact sheet, animated preview, frame evidence and register.
Rejection remains fully reversible by removing this directory and its single
registry entry.
