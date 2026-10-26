# Production sprites — legacy runtime route

> **26 October 2026 art supersession:** This page documents the installed
> pixel-era sprite pipeline and remains useful for maintaining existing runtime
> assets. It is not the authoring route for new graphics. New visual style,
> 1536 × 512 module geometry, exact-magenta masters, Keeper gates and 96/192 px
> item rules come from `docs/CODEX_BRIEF.md` and `AGENTS.md`. In particular,
> `npm run sprites` removes `#FF00FF` and must not receive the only copy of a
> new tower or environment master.

The first legacy production Pixel batch is live for the shell stripes and three implemented room plates. The review catalogue adds the CRT television, shared broken effects and inset lantern surround. The keeper review batch adds aligned front/back master parts and the initial movement/action set; unbuilt objects, character actions, effects and room art retain vector fallbacks. Existing files under `style_b_pixel/` remain concept/prototype references and must not be sliced into production sprites.

For the legacy runtime route, the relevant records are:

- `docs/CODEX_BRIEF.md` — current non-pixel graphics authority; it supersedes
  the future-authoring parts of this legacy route.
- `docs/PRODUCTION_ASSET_KIT.md` — historical anchors, pivots, z-order, frame counts, fps, interaction points and first-batch delivery order.
- `art/asset_inventory.json` — factual inventory of the existing prototype PNGs only.
- `docs/KEEPER_ANIMATIONS.md` — plain-English clip names, direction reuse and object-alignment recipe.
- `docs/KEEPER_ASSET_SCALE.md` and `data/keeper_asset_contract.json` — approved legacy character scale, pivots and object-use datums.

## Maintaining legacy art in the game

For existing legacy assets only, put delivered PNGs in `art/raw/` (subfolders fine) and run `npm run sprites`. It removes `#FF00FF` backgrounds, snaps each picture to one source pixel per logical pixel, writes it to `public/sprites/`, rebuilds `public/sprites/manifest.json` (with `w`, `h`, `frames`, `fps`, and keeper pivots from the legacy asset kit), and reports size mismatches. Snapped entries draw at their own size × 4 on whole pixels. Do not use this route for new tower/environment masters.

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

Delivery-order item 1 is complete. Delivery-order item 2 and the keeper subset of item 3 are review candidates: the CRT/channel strips, shared broken overlays, keeper master parts, and a 187-export keeper set spanning domestic actions, seated nap, lawn-mower pushing, three-tier cupboard-fetched cleaning, activity-outfit routing, three-tier guitar pickup/play, travel, performance, bedtime and water actions. Authored sources are under `art/source/`; exact raw deliveries are under matching `art/raw/` folders.

Frank approved the identity-preserving keeper walk and current action direction in chat. Other review candidates still require explicit approval. The prioritized remaining keeper clips are recorded in `docs/KEEPER_ANIMATIONS.md`; object sets, shell pieces, later rooms, pets, visitors, ships and weather batches stay pending.
