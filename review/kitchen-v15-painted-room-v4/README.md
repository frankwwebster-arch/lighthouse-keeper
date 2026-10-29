# Kitchen v15 painted room v4

Status: **review candidate awaiting Frank**. This folder is review-only. No
runtime art, canon, manifest, public asset or deployment was changed.

This pass starts from the exact 2172 × 724 brighter duck-egg kitchen Frank
liked. That byte-identical source was committed first in `e3af7820`; its SHA-256
is `404c4b095ee64b1b5ba37f5cea23d24081b0e1a6c70f824563e5edef93846e15`.
The room keeps its palette, shell, beamed ceiling, perspective side doors,
joinery and props. The furniture layout alone moves to approved schematic v15:

- the tall larder is gone;
- cupboard B3 fills x 1462–1630;
- run B is a continuous three-cupboard run ending at x 1630;
- the dresser moves to x 1630–1843 and ends the furniture run;
- toaster and mixer are separate cuts on the dresser at stops 17 and 18.

## Review order

1. `outputs/kitchen-v15-liked-source-layout-comparison.png`
2. `outputs/kitchen-v15-check-3-day1-room.png`
3. `outputs/kitchen-v15-piece-gate-sheet.png`
4. `outputs/kitchen-v15-check-1-full-upgrade-fit.png`
5. `outputs/kitchen-v15-check-2-both-doors-open-clear.png`
6. `outputs/kitchen-v15-two-viewing-scales.png`

The full-upgrade image is a geometry-reservation check, not unapproved tier-3
art. Its five translucent boxes come directly from v15 `upgradeSlots`.

## Gate result

- 19/19 cut pieces have the exact v15 canvas and placement box.
- Unit base y = 485; worktop box y = 317–348 with surface datum y = 326.
- Keeper remains byte-identical at 120 × 298, soles y = 502.
- Every declared stop centre is exact.
- Both 168 × 168 windows are clear and contain all exact magenta.
- Both approved 168 × 336 door leaves fit open at 90°.
- Open-door clearance is 118 px to the fridge and 37 px to the dresser.
- Exact-magenta glass pixels: 30,752; near-magenta outside glass: 0.

Full per-piece evidence is in `GATE_REPORT.md` and `gate-report.json`.

## Rebuild and verify

```sh
/Users/frank/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 review/kitchen-v15-painted-room-v4/build_kitchen_v15_v4.py
/Users/frank/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 review/kitchen-v15-painted-room-v4/verify_kitchen_v15_v4.py
```

Stop here for Frank. Do not promote, integrate or deploy this review candidate.

## Documentation audit

Completed before handoff. `docs/SPEC.md`, the approved v15 schematic, the Room
Planner hand-back format, deployment rules, generated manifests, cut canvases
and runtime state were compared. The root `README.md` was updated because it
still called the rejected v14 build current and mentioned its larder. No other
repository document requires a product-state change: this candidate remains
review-only, runtime and deployment are untouched, and `docs/ISSUES.md` is a
Claude-generated read-only mirror rather than a Codex-owned document.
