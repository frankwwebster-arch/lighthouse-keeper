# Kitchen v15 painted-room v4 — gate report

Authority: `docs/layout/kitchen_v15_schematic.json` (approved v15, 2048 × 576).

## Piece-by-piece v15 fit

| Piece | Kind | v15 rect (x1, y1, x2, y2) | Exact cut canvas | Result |
|---|---|---:|---:|---|
| clock | wall | 200, 60, 260, 120 | 60 × 60 | PASS |
| calendar | wall | 200, 140, 260, 210 | 60 × 70 | PASS |
| fridge_t1 | freestanding | 286, 183, 454, 485 | 168 × 302 | PASS |
| cupboard_A1 | fitted | 454, 348, 622, 485 | 168 × 137 | PASS |
| sink_cabinet | fitted | 622, 348, 790, 485 | 168 × 137 | PASS |
| dw_slot_cupboard | fitted | 790, 348, 958, 485 | 168 × 137 | PASS |
| wall_cupboard_1 | wall | 806, 140, 942, 241 | 136 × 101 | PASS |
| runA_worktop | worktop | 454, 317, 958, 348 | 504 × 31 | PASS |
| teapot | counter | 852, 290, 896, 326 | 44 × 36 | PASS |
| cooker_t1 | slot-in | 958, 149, 1126, 485 | 168 × 336 | PASS |
| cupboard_B1 | fitted | 1126, 348, 1294, 485 | 168 × 137 | PASS |
| wall_cupboard_2 | wall | 1142, 140, 1278, 241 | 136 × 101 | PASS |
| cupboard_B2 | fitted | 1294, 348, 1462, 485 | 168 × 137 | PASS |
| cupboard_B3 | fitted | 1462, 348, 1630, 485 | 168 × 137 | PASS |
| runB_worktop | worktop | 1126, 317, 1630, 348 | 504 × 31 | PASS |
| dresser | freestanding | 1630, 149, 1843, 485 | 213 × 336 | PASS |
| toaster | counter | 1688, 300, 1740, 334 | 52 × 34 | PASS |
| mixer | counter | 1766, 275, 1830, 334 | 64 × 59 | PASS |
| prime_keeper | keeper | 1150, 204, 1270, 502 | 120 × 298 | PASS |

Result: **19/19 exact canvases; all pieces fit**. No larder cut exists.

## Hard datums

| Gate | Result |
|---|---|
| Module | PASS — 2048 × 576 |
| Unit base | PASS — y 485 |
| Worktop | PASS — box y 317–348; surface datum y 326 |
| Cooker hob | PASS — registered level with the worktop box |
| Keeper | PASS — unchanged 120 × 298; soles y 502 |
| Stop centres | PASS — every declared stop equals its cut-box centre |
| Left window | PASS — x 622–790, y 106–274; no item collision |
| Right window | PASS — x 1294–1462, y 106–274; no item collision |
| Magenta | PASS — 30,752 exact; zero near-magenta outside glass |

## Three room checks

| Check | Evidence | Result |
|---|---|---|
| Everything at full upgrade | `outputs/kitchen-v15-check-1-full-upgrade-fit.png` shows all five maximum-tier reservations from v15 | PASS |
| Both doors open and clear | `outputs/kitchen-v15-check-2-both-doors-open-clear.png`; 118 px left clearance, 37 px right clearance | PASS |
| Day-1 room | `outputs/kitchen-v15-check-3-day1-room.png`, assembled from the exact v15 cuts | PASS |

The full machine-readable measurements, cut methods, hashes and placements are
in `gate-report.json` and `manifest.json`.
