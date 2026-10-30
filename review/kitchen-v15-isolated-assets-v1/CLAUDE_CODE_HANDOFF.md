# Claude Code handoff — Kitchen v15 isolated assets v1

Frank asked for every asset separately, in the same transparent isolated-image format as his supplied dresser example. This entire handoff is contained in this folder.

## Files to use

- `assets-5x/` contains all 19 delivered RGBA PNGs, one asset per file.
- `isolated-assets-contact-sheet.png` is preview evidence only; its checkerboard and labels are not artwork.
- `manifest.json` records every output's hash, dimensions, original v15 room-cut source, actual alpha bounds and presentation-source provenance.
- `README.md` explains the export contract.
- `verify_isolated_assets_v1.py` is the acceptance gate.

Do not cut assets back out of a room or from the contact sheet. Use the individual files in `assets-5x/`.

The five ordinary cabinet files are intentionally separate names with byte-identical art. The two wall-cupboard files are likewise byte-identical. The dresser uses its native full-resolution transparent source. The mixer and toaster use clean native transparent donors because their v7 room-cut files contained rectangular backdrop pixels.

This is a review-only, reversible export. The Kitchen v15 painted-room v7 source, runtime art and production data remain unchanged. Do not promote, replace runtime files or deploy without a later explicit GO from Frank.

Verification:

```sh
/Users/frank/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 review/kitchen-v15-isolated-assets-v1/verify_isolated_assets_v1.py
```

Expected result: `PASS: 19 isolated transparent assets; pinned sources; exact-edge crops; native high-res donors; repeated cabinets identical`.
