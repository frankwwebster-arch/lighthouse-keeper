# Kitchen v15 — isolated assets v1

This review package presents every Kitchen v15 v7 cut asset as its own high-resolution transparent PNG, like Frank's dresser example. It does not redraw, restyle or alter the v7 source artwork.

## What to review

- `assets-5x/` — all 19 assets, one complete object per RGBA PNG.
- `assets-5x/dresser.png` — the dresser in the requested tall isolated format.
- `isolated-assets-contact-sheet.png` — a labelled preview of all 19 files. Its checkerboard is only a preview background; the individual files have genuine transparency.
- `manifest.json` — source hash, original v15 canvas, actual painted-edge bounds and export dimensions for every asset.
- `CLAUDE_CODE_HANDOFF.md` — the self-contained continuation note for Claude Code.

The five ordinary base cabinets remain separate named files but are verified byte-identical. The two wall cupboards are likewise separate and byte-identical. Worktops and counter props remain separate because they are separate v15 pieces.

## Export rule

Each pinned v7 RGBA source is cropped to its actual non-transparent painted edges and placed inside a 24 px transparent safety gutter. Most pieces are enlarged exactly 5× with alpha-aware Lanczos resampling. The dresser uses its native 999 × 1575 full-resolution source—the format Frank supplied—and the mixer and toaster use their native clean transparent sources because their room-cut v7 PNGs contained unwanted rectangular backdrop pixels. The crop is therefore determined by the asset itself, not by an arbitrary gate-sheet rectangle. The manifest retains both the original v15 canvas and the presentation-source provenance so exact room placement remains recoverable.

This is a non-destructive review export. The source package `review/kitchen-v15-painted-room-v7/`, runtime art and production data are unchanged; nothing was deployed.

## Rebuild and verify

Using the bundled Codex Python runtime (which includes Pillow):

```sh
/Users/frank/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 review/kitchen-v15-isolated-assets-v1/build_isolated_assets_v1.py
/Users/frank/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 review/kitchen-v15-isolated-assets-v1/verify_isolated_assets_v1.py
```
