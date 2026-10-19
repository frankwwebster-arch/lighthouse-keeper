# Source-art record

Mode: built-in `image_gen`, precise-object-edit. Both selected outputs are preserved unchanged under `art/source/`. They supply upper-body pixels only; deterministic code registers them to the approved POC V3 motion, maps every visible RGB value to the matching Walk V6 or Turn V9 authority palette, separates torso/head from held arms, and recomposes those layers over byte-identical lower-body authority pixels.

## Selected walk source

- File: `art/source/keeper-prime-hold-shaft-two-hand-layered-2026-10-19-v1/walk-upper-body-grid-prime-authority-generated.png`
- SHA-256: `48630b3be23e1b12b8495817b34ac661752758513bb4688131897f72ba47f828`
- Prompt: preserve the exact eight side-right POC walk poses in 4×2 order; remove only trousers, legs and boots below the ribbed waistband; retain head, beard, torso, waistband, exactly two connected arms and at most two closed hands around an invisible shaft; genuine transparent background; no prop, text, grid, shadow or detached object.

## Selected turn source

- File: `art/source/keeper-prime-hold-shaft-two-hand-layered-2026-10-19-v1/turn-upper-body-grid-prime-authority-generated.png`
- SHA-256: `4048124b01b86155125c39fd11f3b98dda424ce461679e2cf5ccc71e38d22ed2`
- Prompt: preserve the exact nine POC turn orientations in 3×3 order; remove only the lower body below the ribbed waistband; retain the upper body and natural rear-angle hand occlusion; genuine transparent background; no prop or detached object.

## Rejected generation

The first walk attempt (SHA-256 `1847eeb692cb5a9585c1c7c456d2f96f1ac0fef6922c7d5500d52b90c931e21a`) drifted its final two cells into rear views. It was rejected before import and contributes no candidate pixel.
The imported exploratory walk grid `walk-upper-body-grid-generated.png` (SHA-256 `a486ea87d77e9036fdc71c02c852037dd71dc1dc70a838ac2f1e8cfdb0ffd119`) and turn grid `turn-upper-body-grid-generated.png` (SHA-256 `e2bb0a482a1820598f1de10409abf38eb4dbb9ad39d980d980ec23433ea637e1`) were superseded because their broad generated proportions were not close enough to the approved Prime authorities. They remain immutable source evidence and contribute no candidate pixel.
