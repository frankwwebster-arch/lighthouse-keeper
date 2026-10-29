# Kitchen v15 painted-room v6 — gate report

Authority: `docs/layout/kitchen_v15_schematic.json` (v15, 2048 × 576).

## Requested corrections

| Gate | Result |
|---|---|
| Structural shell | PASS — jamb-only base, no baked leaf |
| Door state contract | PASS — closed/open leaves exclusive; y208–544 |
| Open-door clearance | PASS — 118 px left / 37 px right |
| Sink integration | PASS — approved rim/taps in run A worktop |
| Sink cabinet family | PASS — body equals base master below local y42 |
| Dresser depth | PASS — shared 31 px band at room y317–348 |
| Ordinary base cupboards | PASS — five byte-identical 168 × 137 PNGs |
| Wall cupboards | PASS — two byte-identical 136 × 101 PNGs |
| Wall-cupboard / cooker spacing | PASS — 16 px both sides |

Run A's worktop intentionally differs from run B because it contains the sink
rim and taps. Both remain exact 504 × 31 pieces with the same depth/front-edge
datums. The dresser's depth band is a resized-width copy of the clean worktop
master and occupies the same y interval.

## Piece-by-piece v15 fit

| Piece | v15 canvas | Actual alpha bounds | Result |
|---|---:|---:|---|
| clock | 60 × 60 | 2, 2, 58, 58 | PASS |
| calendar | 60 × 70 | 2, 2, 58, 68 | PASS |
| fridge_t1 | 168 × 302 | 23, 0, 145, 302 | PASS |
| cupboard_A1 | 168 × 137 | 0, 1, 168, 137 | PASS |
| sink_cabinet | 168 × 137 | 0, 0, 168, 137 | PASS |
| dw_slot_cupboard | 168 × 137 | 0, 1, 168, 137 | PASS |
| wall_cupboard_1 | 136 × 101 | 0, 1, 136, 100 | PASS |
| runA_worktop | 504 × 31 | 0, 0, 504, 31 | PASS |
| teapot | 44 × 36 | 2, 2, 42, 34 | PASS |
| cooker_t1 | 168 × 336 | 0, 63, 168, 336 | PASS |
| cupboard_B1 | 168 × 137 | 0, 1, 168, 137 | PASS |
| wall_cupboard_2 | 136 × 101 | 0, 1, 136, 100 | PASS |
| cupboard_B2 | 168 × 137 | 0, 1, 168, 137 | PASS |
| cupboard_B3 | 168 × 137 | 0, 1, 168, 137 | PASS |
| runB_worktop | 504 × 31 | 0, 1, 504, 30 | PASS |
| dresser | 213 × 336 | 0, 0, 213, 329 | PASS |
| toaster | 52 × 34 | 2, 0, 49, 34 | PASS |
| mixer | 64 × 59 | 0, 18, 64, 59 | PASS |
| prime_keeper | 120 × 298 | 9, 0, 111, 298 | PASS |

Result: **19/19 exact canvases and actual-edge transparent pieces**. No larder
cut exists.

## Three room checks

| Check | Evidence | Result |
|---|---|---|
| Everything at full upgrade | `outputs/kitchen-v15-check-1-full-upgrade-fit.png` | PASS |
| Both doors open and clear | `outputs/kitchen-v15-check-2-both-doors-open-clear.png` | PASS |
| Day-1 room | `outputs/kitchen-v15-check-3-day1-room.png` | PASS |

Machine-readable source hashes, cut methods, placements, door quads, datums
and per-piece metrics are in `gate-report.json` and `manifest.json`.
