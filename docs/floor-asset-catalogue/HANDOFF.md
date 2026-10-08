# Review batch handoff

Branch: `codex/floor-asset-catalogue`. Do not merge before Frank reviews `review.html`.

Use [ART_STYLE_GUIDE.md](ART_STYLE_GUIDE.md) as the visual acceptance contract for every subsequent asset. The finished CRT/BB Sea TV is the concrete style reference; the guide records its pixel density, palette, readability, state, animation and anchor rules.

The catalogue covers 71 spaces/variants and 1,531 rows. Proposed benefits and unlock challenges are review data, not implemented progression. Unresolved product choices are labelled in the design cards and decision register. Middle floors have no prescribed vertical order. The inset lantern surround is 95 × 35 logical pixels; ordinary floors remain 110 × 35. ON is required for operating devices; passive furniture such as tables and chairs does not need an artificial ON state.

Art-only integration adds the original box CRT, the supplied BBC NEWS reference reworked to literally read `B B SEA`, with NEWS and a newsreader head, plus football and animal broadcasts, the inset lantern surround and shared broken smoke/sparks. Channel choices call existing `tv_watch` / `tv_nature` actions. Shared effects use each asset's `effectOrigin`; TV attaches at its damaged top-right corner. Keep this per-item attachment metadata when adding other objects. Body vibration remains the existing CSS animation.

Detailed source frames use density 4 while logical dimensions, interaction anchors and nearest-neighbour rendering remain stable. `scripts/sprites.ts` still accepts legacy density-1 assets. Density sidecars are validated before existing exports are removed. No concept plate has been sliced.

Engine, missions, saves, floor ordering and progression have not been edited. `data/upgrades.csv` changes only basic TV art-status cells; higher-tier art remains pending. These exports are review candidates, not blanket approval for the catalogue.

Frank can annotate spaces/assets, add proposals, adjust pixel block size and paint individual frames in the standalone review canvas. Export annotation JSON and PNG strips to preserve edits. This session has no native Codex Canvas publishing capability; the repository HTML is the review artifact.

The BB Sea channel preview has review-only Shimmer strength and Shimmer speed sliders. They tune the visible broadcast highlight without changing the committed sprite or runtime logic; export the review JSON if a preferred setting should be carried forward.

The keeper continuation is included in the same review canvas. It preserves the established identity, beard, palette and proportions across his uniform, swimming costume and navy pyjamas. Frank approved the aligned identity, walk and current action direction. The 56-export kit covers domestic actions, doors/travel, adventure, gardening, shopping, boating, TV, workshop tools, emotional reactions and bedtime. Runtime cooker and basin work select the appropriate rear strip; most newer clips remain reserved for their future world objects and the current loo remains hidden by its privacy door. `docs/KEEPER_ANIMATIONS.md` is the human-readable application index; `data/keeper_asset_contract.json` and `docs/KEEPER_ASSET_SCALE.md` are authoritative for character scale, object-use heights, bed alignment and TV sightlines.

Rebuild and verification commands are in [README.md](README.md). Review screenshots and native-size contact sheet are beside the HTML. Do not infer four separate objects from ON frames: they form one animation. The broken TV is one damaged image, with reusable overlays.
