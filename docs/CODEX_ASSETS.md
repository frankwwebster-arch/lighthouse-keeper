# Production sprites — current route

The first production Pixel batch is live for the shell stripes and three implemented room plates. The review catalogue adds the CRT television, shared broken effects and inset lantern surround. The keeper review batch adds aligned front/back master parts and the initial movement/action set; unbuilt objects, character actions, effects and room art retain vector fallbacks. Existing files under `style_b_pixel/` remain concept/prototype references and must not be sliced into production sprites.

The authoritative art inputs are:

- `docs/CODEX_BRIEF.md` — exact Pixel style, filenames and base dimensions.
- `docs/PRODUCTION_ASSET_KIT.md` — anchors, pivots, z-order, frame counts, fps, interaction points and first-batch delivery order.
- `art/asset_inventory.json` — factual inventory of the existing prototype PNGs only.
- `docs/KEEPER_ANIMATIONS.md` — plain-English clip names, direction reuse and object-alignment recipe.
- `docs/KEEPER_ASSET_SCALE.md` and `data/keeper_asset_contract.json` — authoritative character scale, pivots and object-use datums.

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

Delivery-order item 1 is complete: `tower_stripe_{red,white}.png` and `room_{kitchen,living,bedroom}.png`. Delivery-order item 2 and the keeper subset of item 3 are review candidates: the CRT/channel strips, shared broken overlays, keeper master parts, and a 171-export keeper set spanning domestic, tea/coffee preparation and drinking, boat entry/exit, explicit spiral-stair travel, emotional/needs reactions, toilet sickness, bathrobe/shower entry, fish-tank, reading/writing, workshop/craft, meal service/carry/placement, game, exercise, bathing, fishing, watering, travel, costume, adventure, garden, boat, performance, bedtime, swimming and weather actions. Their authored sources are under `art/source/floor-asset-catalogue/` and `art/source/keeper-first-batch/`; exact raw deliveries are under matching `art/raw/` folders.

Frank approved the identity-preserving keeper walk and current action direction in chat. Other review candidates still require explicit approval. The prioritized remaining keeper clips are recorded in `docs/KEEPER_ANIMATIONS.md`; object sets, shell pieces, later rooms, pets, visitors, ships and weather batches stay pending.
