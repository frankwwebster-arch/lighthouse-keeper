# Production sprites — current route

The game still draws vector fallbacks; the existing files under `style_b_pixel/` are concept/prototype references and must not be sliced into production sprites.

The authoritative art inputs are:

- `docs/CODEX_BRIEF.md` — exact Pixel style, filenames and base dimensions.
- `docs/PRODUCTION_ASSET_KIT.md` — anchors, pivots, z-order, frame counts, fps, interaction points and first-batch delivery order.
- `art/asset_inventory.json` — factual inventory of the existing prototype PNGs only.

## Runtime manifest

Place production PNGs in `public/sprites/` and map their keys in `public/sprites/manifest.json`.

A still remains backward-compatible:

```json
{ "obj_door_standard": "obj_door_standard_f1.png" }
```

An animated horizontal strip includes playback metadata:

```json
{
  "obj_tv_on": {
    "file": "obj_tv_on_f4.png",
    "frames": 4,
    "fps": 8
  }
}
```

`ObjectArt` first requests `obj_<id>_<state>` and falls back to the older `obj_<id>` key. All frames in a strip are equal width, arranged left to right. The renderer clips one frame and advances discretely; it does not blur, rotate or rescale between frames.

## Current delivery boundary

No production PNG has been delivered yet. Start only the first-three-floor kit. Do not begin later aquarium, weather-station, hidden-lair, lift, pet, visitor, ship or weather batches.
