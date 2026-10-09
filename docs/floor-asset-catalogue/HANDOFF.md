# Review batch handoff

Delivery branch: `main`. The review artefact and its sources live together in
the ordinary project folder; no separate review branch or worktree is required.

Use [ART_STYLE_GUIDE.md](ART_STYLE_GUIDE.md) as the visual acceptance contract for every subsequent asset. The finished CRT/BB Sea TV is the concrete style reference; the guide records its pixel density, palette, readability, state, animation and anchor rules.

The catalogue covers 71 spaces/variants and 1,559 rows. Proposed benefits and unlock challenges are review data, not implemented progression. Unresolved product choices are labelled in the design cards and decision register. Middle floors have no prescribed vertical order. The inset lantern surround is 95 × 35 logical pixels; ordinary floors remain 110 × 35. ON is required for operating devices; passive furniture such as tables and chairs does not need an artificial ON state.

Art-only integration adds the original box CRT, the supplied BBC NEWS reference reworked to literally read `B B SEA`, with NEWS and a newsreader head, plus football and animal broadcasts, the inset lantern surround and shared broken smoke/sparks. Channel choices call existing `tv_watch` / `tv_nature` actions. Shared effects use each asset's `effectOrigin`; TV attaches at its damaged top-right corner. Keep this per-item attachment metadata when adding other objects. Body vibration remains the existing CSS animation.

Detailed source frames use density 4 while logical dimensions, interaction anchors and nearest-neighbour rendering remain stable. `scripts/sprites.ts` still accepts legacy density-1 assets. Density sidecars are validated before existing exports are removed. No concept plate has been sliced.

Engine, missions, saves, floor ordering and progression have not been edited. `data/upgrades.csv` changes only basic TV art-status cells; higher-tier art remains pending. These exports are review candidates, not blanket approval for the catalogue.

Frank can annotate spaces/assets, add proposals, adjust pixel block size and paint individual frames in the standalone review canvas. Export annotation JSON and PNG strips to preserve edits. This session has no native Codex Canvas publishing capability; the repository HTML is the review artifact.

The BB Sea channel preview has review-only Shimmer strength and Shimmer speed sliders. They tune the visible broadcast highlight without changing the committed sprite or runtime logic; export the review JSON if a preferred setting should be carried forward.

The keeper continuation is included in the same review canvas. The 183-export kit includes a canonical side-seated nap, artist-smock walk/turn/sit route and three guitar pickup/play tiers. `docs/KEEPER_ANIMATIONS.md` is the application index; `docs/KEEPER_COSTUME_ROUTE_AUDIT.md` records remaining outfit bridges; the machine-readable contracts remain authoritative for scale and contacts.

Rebuild and verification commands are in [README.md](README.md). Review screenshots and native-size contact sheet are beside the HTML. Do not infer four separate objects from ON frames: they form one animation. The broken TV is one damaged image, with reusable overlays.
