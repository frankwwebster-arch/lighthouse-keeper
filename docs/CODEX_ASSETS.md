# Production sprites — current route

The first production Pixel batch is live for the shell stripes and the three implemented room plates. Objects, characters, effects and any missing room art still draw vector fallbacks. Existing files under `style_b_pixel/` remain concept/prototype references and must not be sliced into production sprites.

The authoritative art inputs are:

- `docs/CODEX_BRIEF.md` — exact Pixel style, filenames and base dimensions.
- `docs/PRODUCTION_ASSET_KIT.md` — anchors, pivots, z-order, frame counts, fps, interaction points and first-batch delivery order.
- `art/asset_inventory.json` — factual inventory of the existing prototype PNGs only.

## Bringing art into the game

Put delivered PNGs in `art/raw/` (subfolders fine) and run `npm run sprites`. It removes `#FF00FF` backgrounds, snaps each picture to one source pixel per logical pixel, writes it to `public/sprites/`, rebuilds `public/sprites/manifest.json` (with `w`, `h`, `frames`, `fps`, and keeper pivots from the asset kit), and lists any file whose size differs from `docs/CODEX_BRIEF.md` / `docs/PRODUCTION_ASSET_KIT.md`. Snapped entries draw at their own size × 4 on whole pixels.

## Runtime manifest

Production PNGs end up in `public/sprites/`, mapped in `public/sprites/manifest.json`. Hand-written entries still work:

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

Delivery-order item 1 is complete: `tower_stripe_{red,white}.png` and `room_{kitchen,living,bedroom}.png`. Exact normalized deliveries are in `art/raw/first-production-batch/`, published exports are in `public/sprites/`, and untouched generated sources plus prompt notes are in `art/source/first-production-batch/`. `room_bedroom.png` includes the en-suite partition and doorway.

Do not treat this as permission to begin keeper clips, object-state strips, lamp-room art, `tower_base.png`, `tower_lamproom.png`, `tower_roof.png`, `ground_strip.png`, or later aquarium, weather-station, hidden-lair, lift, pet, visitor, ship and weather batches. The next production item remains delivery-order item 2 in `docs/PRODUCTION_ASSET_KIT.md`.
