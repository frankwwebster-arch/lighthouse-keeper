# Kitchen v15 painted-room v5 — actual-edge gate report

Authority: `docs/layout/kitchen_v15_schematic.json` (v15, 2048 × 576).

## Correction proved

| Gate | Result |
|---|---|
| Ordinary base cupboards | PASS — five byte-identical 168 × 137 PNGs |
| Wall cupboards | PASS — two byte-identical 136 × 101 PNGs |
| Wall-cupboard / cooker spacing | PASS — 16 px visible gap on both sides |
| Worktops | PASS — two byte-identical 504 × 31 PNGs |
| Furniture transparency | PASS — every piece contains true transparent pixels |
| Base cut lines | PASS — x454, 622, 790, 958, 1126, 1294, 1462, 1630 |

The gate distinguishes two things that v4 conflated: the required PNG canvas
and the actual painted alpha bounds inside it. Both are recorded for every part
in `gate-report.json`. Repeated cabinets are not separate coordinate crops;
they are copies of a single processed master.

## Piece-by-piece v15 fit

| Piece | v15 canvas | Actual alpha bounds | Result |
|---|---:|---:|---|
| clock | 60 × 60 | 2, 2, 58, 58 | PASS |
| calendar | 60 × 70 | 2, 2, 58, 68 | PASS |
| fridge_t1 | 168 × 302 | 23, 0, 145, 302 | PASS |
| cupboard_A1 | 168 × 137 | 0, 1, 168, 137 | PASS |
| sink_cabinet | 168 × 137 | 0, 1, 168, 137 | PASS |
| dw_slot_cupboard | 168 × 137 | 0, 1, 168, 137 | PASS |
| wall_cupboard_1 | 136 × 101 | 0, 1, 136, 100 | PASS |
| runA_worktop | 504 × 31 | 0, 1, 504, 30 | PASS |
| teapot | 44 × 36 | 2, 2, 42, 34 | PASS |
| cooker_t1 | 168 × 336 | 0, 63, 168, 336 | PASS |
| cupboard_B1 | 168 × 137 | 0, 1, 168, 137 | PASS |
| wall_cupboard_2 | 136 × 101 | 0, 1, 136, 100 | PASS |
| cupboard_B2 | 168 × 137 | 0, 1, 168, 137 | PASS |
| cupboard_B3 | 168 × 137 | 0, 1, 168, 137 | PASS |
| runB_worktop | 504 × 31 | 0, 1, 504, 30 | PASS |
| dresser | 213 × 336 | 17, 0, 208, 331 | PASS |
| toaster | 52 × 34 | 2, 0, 49, 34 | PASS |
| mixer | 64 × 59 | 0, 18, 64, 59 | PASS |
| prime_keeper | 120 × 298 | 9, 0, 111, 298 | PASS |

Result: **19/19 exact canvases and actual-edge transparent pieces**. No larder
cut exists.

## Three room checks

| Check | Evidence | Result |
|---|---|---|
| Everything at full upgrade | `outputs/kitchen-v15-check-1-full-upgrade-fit.png` | PASS |
| Both doors open and clear | `outputs/kitchen-v15-check-2-both-doors-open-clear.png`; 118 px left / 37 px right | PASS |
| Day-1 room | `outputs/kitchen-v15-check-3-day1-room.png`, assembled only from transparent cuts | PASS |

Hard datums, exact-magenta checks, source hashes, per-piece cut methods and
placements are in `gate-report.json` and `manifest.json`.
