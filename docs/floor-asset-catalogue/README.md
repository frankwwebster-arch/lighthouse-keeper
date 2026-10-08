# Frank’s floor and asset review

Open **[review.html](review.html)**. This self-contained review canvas works without a server or network connection. It contains 71 documented spaces/variants, searchable design cards and diagrams, a 1,531-row CSV-style catalogue, mechanical tier proposals, required states, production thumbnails and annotation tools.

Native Codex Canvas publishing is unavailable in this session. This is a durable standalone HTML review artifact, not a claimed native Canvas publication. It can be imported or published there when that capability is available.

## Annotating

- Use each space’s note field and Reviewed checkbox.
- In CSV catalogue, record asset notes and select `changes-requested` or `approved`.
- Use Decisions & additions to add rooms or items.
- **Export my changes** downloads `frank-floor-review.json`. Share or commit that file to carry annotations between sessions. Notes also persist in the current browser; they do not automatically sync with Frank’s Claude tracker or rewrite game data.
- Import changes merges exported annotations. Download catalogue CSV exports the underlying design table; review annotations are deliberately exported separately.

Pixel studio lets Frank adjust pixel block size, paint or erase individual frames, undo changes and export PNG strips with their exact dimensions preserved. The TV channel preview also exposes **Shimmer strength** and **Shimmer speed** controls; those settings persist locally and travel in the exported annotation JSON. Pixel edits also travel in the annotation JSON.

BB Sea news literally reads `B B SEA`, adapted from the supplied BBC NEWS reference, followed by NEWS lettering and a tiny newsreader head. Sport shows football; Nature shows animals. Four ON frames are one animated state, not four asset variants. Broken TV uses one damaged image plus shared smoke/sparks and existing body vibration. Channel selection reuses existing watch/nature actions; no new gameplay effect is claimed. The production guide now requires ON only for operating devices; passive furniture remains standard and is designed around keeper poses.

The Completed assets and Pixel studio tabs also contain the keeper continuation: 65 aligned exports spanning domestic movement, doors/travel, adventure, gardening, shopping, boating, TV, workshop tools, reactions, bedtime, directional swimming, scuba and party variants. Search `keeper_` to isolate them. The large turnaround is a style reference; normal runtime strips are 32 × 40 at density 4, rowing and long-tool actions may use 40 × 40, bed actions use 48 × 40, swimming uses centred 48 × 48, party headwear uses 32 × 48, and dive/parachute poses expand vertically without changing the keeper's scale.

The production walk is an eight-frame right-facing side cycle at 10 fps. The
runtime mirrors it for left-facing movement. `keeper-walk-preview.gif` is an
enlarged loop of those exact frames for quick review.

The other quick-review animations are `keeper-turn-back-preview.gif`,
`keeper-work-back-preview.gif`, `keeper-sit-side-preview.gif`,
`keeper-sit-front-preview.gif` and `keeper-piano-preview.gif`. Side sitting is
mirrored for a left-hand chair; both sitting strips reverse for standing up.
Furniture should align its seat to the manifest `seatPoint`, not alter the pose.
`keeper-eat-seated-preview.gif` adds the fork-to-mouth dining loop, and
`keeper-urinate-back-preview.gif` is the separate hands-low bathroom proxy.
Door previews cover side and rear opening, ping-ponging only to demonstrate the
reverse-to-close contract. Ladder climb likewise ping-pongs to demonstrate
up/down. Stair ascent and descent have separate looping previews.
`keeper-switch-press-right-preview.gif` and `keeper-switch-press-left-preview.gif`
show the two directions (the left review animation mirrors the shared side
strip); `keeper-switch-press-back-preview.gif` covers a rear approach and mirrors to
swap the reaching hand. The rear fingertip now shares the side press's Y=17
height. `keeper-parachute-jump-preview.gif`, `keeper-platform-dive-preview.gif`,
`keeper-dig-preview.gif`, `keeper-feed-animals-preview.gif`, the gardening,
shopping and boat previews cover the newer actions. TV has separate
`keeper-watch-tv-right-preview.gif` and `keeper-watch-tv-left-preview.gif`
reviews from one mirrored rear-three-quarter strip, with the seat offset far
enough to keep the screen visible. See `../KEEPER_ANIMATIONS.md` for the index and
`../KEEPER_ASSET_SCALE.md` for authoritative object-alignment measurements.

## Art corrections recorded from this review

Frank’s later directions supersede earlier coarse one-source-pixel exports:

1. The original `style_b_pixel/obj_tv_{standard,on,broken}_ai.png` images establish the correct CRT style. The original casing is now reused as the production master, preserving aspect ratio, feet, aerial and cabinet across every state. No wide-screen stretching.
2. The lamp room is an **inset glazed iron lantern chamber with a wraparound outside walkway**, matching `art/background/lighthouse_master_day_pixel.png`. It is not a full-width timber domestic room. The existing renderer’s 95 × 35 logical glass footprint is retained; ordinary standard floors remain 110 × 35 with 105 × 35 plates. Lamp stays topmost; bedroom stays directly beneath it.
3. Operating devices at every upgrade level require **standard + ON + broken** where fault behaviour applies. Tables, chairs and passive furniture do not need artificial ON frames; they use standard art plus an actor-layer occupied/seated pose when useful. The shop is proprietor-owned and has no keeper-repair broken state. Decorative noninteractive dressing does not acquire arbitrary upgrades.
4. Sharp detail is retained with **density 4**: a 28 × 23 logical TV uses a 112 × 92 source frame; its display footprint stays 112 × 92 CSS px at the existing logical 4× scale. A 95 × 35 lamp surround uses 380 × 140 source pixels. No fractional object positioning or raster rotation is introduced. Legacy density-1 deliveries continue unchanged.
5. Coarse exports and the full-width lamp study are rejected and retained outside `art/raw/`. Their presence is provenance, never approval or runtime readiness.

New assets are delivery candidates pending Frank’s review. The remaining space and tier artwork is a catalogue proposal, not a claim that all art or mechanics exist.

## Durable files

| Purpose | Location |
|---|---|
| Review canvas | `docs/floor-asset-catalogue/review.html` |
| Space list | `spaces.csv` |
| Requested full CSV columns | `catalogue.csv` |
| Machine-readable review data | `catalogue.json` |
| Detailed designs and decision register | `DESIGNS.md` |
| Runtime-size asset contact sheet | `completed-assets-4x.png` |
| Authored source data | `art/source/floor-asset-catalogue/spaces.json`, `item-profiles.json` |
| Baseline runtime evidence | `art/source/floor-asset-catalogue/runtime-evidence.json` |
| Source authoring script | `art/source/floor-asset-catalogue/author_catalogue.py` |
| Source images, provenance and rejected studies | `art/source/floor-asset-catalogue/` |
| Exact source/frame/anchor contracts and SHA-256 | `art/source/floor-asset-catalogue/export-contract.json` |
| Raw PNGs and density sidecars | `art/raw/floor-asset-catalogue/` |
| Runtime exports | `public/sprites/` and `manifest.json` |
| Pipeline extension | `scripts/sprites.ts` |
| Production art style guide | [ART_STYLE_GUIDE.md](ART_STYLE_GUIDE.md) |
| Asset-only integration handoff | `HANDOFF.md` |

## Rebuild and verification

From `/workspace/lighthouse-keeper` with Node 24 and Python/Pillow (validated with Pillow 12.3):

```sh
# Only after changing the authored Python space/profile definitions:
python art/source/floor-asset-catalogue/author_catalogue.py

# Reproduce source-to-runtime exports and the review artifact:
python scripts/build_catalogue_asset_batch.py
npm run sprites
python scripts/build_floor_asset_catalogue.py
python scripts/verify_floor_asset_catalogue.py

# Verify game and pipeline:
npm test
npm run typecheck
NEXT_TELEMETRY_DISABLED=1 npm run build
```

Editing the authored `spaces.json` / `item-profiles.json` directly is also supported; do not rerun the authoring script afterward unless you have incorporated those edits there. Rebuild the catalogue directly instead.

The density-contract tests exercise mixed legacy/detailed deliveries, preserved logical bounds, source detail, repeatability and invalid-delivery protection. Browser checks cover canvas filtering, pagination, notes, status changes, exported/imported annotations, additions and mobile layout, plus CRT standard/ON/broken rendering in the game.

## Coverage and authority

All eight requested documents were read in full before design work. `spaces.csv` records source references. The catalogue includes both separately discussed choices (aquarium/marine lab, weather/radio room, greenhouse/conservatory), six imagination themes, annex bathrooms, optional heating/laundry concepts, transport/service cores, exterior bays, roof/parachute idea, all listed island/underground facilities and the retired garage. Unresolved alternatives remain explicit; they do not become a fixed unlock order.

Current engine behaviour is labelled `Runtime:` with measured baseline minutes/effects. Other numbers are labelled **PROPOSED, not coded** or **proposed specialist perk**. Prices, names and perks in Frank’s existing `data/upgrades.csv` are preserved; only the basic TV’s three art-status columns are updated. No mission, world layout, floor progression, allowance, savings or fault logic is changed.

The branch started at `origin/main` commit `cdb109b2904ce0834fa559760e5d34e1ddc8f4f2`. The review batch belongs on `codex/floor-asset-catalogue`; it must not be merged into `main` before Frank’s review.
