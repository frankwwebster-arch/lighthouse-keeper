# Review batch handoff

> **26 October 2026 art supersession:** This handoff remains a record of the
> legacy Pixel review batch and installed behaviour. Do not use its style,
> dimensions, broken-state art or Keeper-generation instructions for new
> graphics. `../CODEX_BRIEF.md` and `AGENTS.md` are current; historical review
> assets remain immutable.

Delivery branch: `main`. The review artefact and its sources live together in
the ordinary project folder; no separate review branch or worktree is required.

For this frozen legacy batch, [ART_STYLE_GUIDE.md](ART_STYLE_GUIDE.md) records the visual acceptance contract that was used. The finished CRT/BB Sea TV is the concrete historical style reference; the guide records its pixel density, palette, readability, state, animation and anchor rules.

The catalogue covers 71 spaces/variants and 1,579 rows. Proposed benefits and unlock challenges are review data, not implemented progression. Unresolved product choices are labelled in the design cards and decision register. Middle floors have no prescribed vertical order. For this historical batch the inset lantern surround was 95 × 35 logical pixels and ordinary floors were 110 × 35. New modules use 1536 × 512; new operating-item art uses only the minimal states in `../CODEX_BRIEF.md`, while passive furniture still uses its standard layer plus the seated Keeper.

Art-only integration adds the original box CRT, the supplied BBC NEWS reference reworked to literally read `B B SEA`, with NEWS and a newsreader head, plus football and animal broadcasts, the inset lantern surround and shared broken smoke/sparks. Channel choices call existing `tv_watch` / `tv_nature` actions. Shared effects use each asset's `effectOrigin`; TV attaches at its damaged top-right corner. Keep this per-item attachment metadata when adding other objects. Body vibration remains the existing CSS animation.

Detailed source frames use density 4 while logical dimensions, interaction anchors and nearest-neighbour rendering remain stable. `scripts/sprites.ts` still accepts legacy density-1 assets. Density sidecars are validated before existing exports are removed. No concept plate has been sliced.

Engine, missions, saves, floor ordering and progression have not been edited. `data/upgrades.csv` changes only basic TV art-status cells; higher-tier art remains pending. These exports are review candidates, not blanket approval for the catalogue.

Frank can annotate spaces/assets, add proposals, adjust pixel block size and paint individual frames in the standalone review canvas. Export annotation JSON and PNG strips to preserve edits. This session has no native Codex Canvas publishing capability; the repository HTML is the review artifact.

The BB Sea channel preview has review-only Shimmer strength and Shimmer speed sliders. They tune the visible broadcast highlight without changing the committed sprite or runtime logic; export the review JSON if a preferred setting should be carried forward.

The keeper continuation is included in the same review canvas. The 184-export kit includes a canonical side-seated nap, lawn-mower push loop, artist-smock walk/turn/sit route and three guitar pickup/play tiers. `docs/KEEPER_ANIMATIONS.md` is the application index; `docs/KEEPER_COSTUME_ROUTE_AUDIT.md` records remaining outfit bridges; the machine-readable contracts remain authoritative for scale and contacts.

Rebuild and verification commands are in [README.md](README.md). Review screenshots and native-size contact sheet are beside the HTML. Do not infer four separate objects from ON frames: they form one animation. The broken TV is one damaged image, with reusable overlays.
