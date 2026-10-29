# Kitchen v15 painted room v5 — actual-edge correction

Status: **review candidate awaiting Frank**. This folder is review-only. No
runtime art, canon, production manifest, public asset or deployment changed.

This revision answers the v4 review note: the wall cupboards were visibly
unequal around the cooker, and the v4 piece sheet proved only rectangular
canvas sizes. It did not prove that those rectangles were clean cuts at the
painted objects' real edges.

V5 retains the unchanged brighter duck-egg 2172 × 724 source (SHA-256
`404c4b095ee64b1b5ba37f5cea23d24081b0e1a6c70f824563e5edef93846e15`)
and the v15 layout. Furniture is now assembled from genuinely transparent
painted-edge parts:

- the five ordinary 168 × 137 base cupboards are byte-identical copies of one
  master and meet at exact v15 divides;
- the two 136 × 101 wall cupboards are byte-identical copies of one master;
- their visible gaps to the cooker are exactly 16 px left and 16 px right;
- the two 504 × 31 worktops are byte-identical copies of one clean master;
- every furniture part has real transparency—no wall, floor or neighbouring
  furniture is baked into its PNG.

## What the piece gate means

Each card in `outputs/kitchen-v15-piece-gate-sheet.png` shows one standalone
PNG on checkerboard transparency. The green statement is its required v15
canvas. The cyan rectangle is the bounding box of its actual non-transparent
paint. These are no longer arbitrary crops from room coordinates.

`outputs/kitchen-v15-cabinet-edge-gate.png` is the cabinet-specific proof. Its
vertical cyan lines are the exact v15 module divides at x454, 622, 790, 958,
1126, 1294, 1462 and 1630. The lower enlargement shows the identical wall
cupboards and the measured equal gaps to the cooker.

## Review order

1. `outputs/kitchen-v15-cabinet-edge-gate.png`
2. `outputs/kitchen-v15-check-3-day1-room.png`
3. `outputs/kitchen-v15-piece-gate-sheet.png`
4. `outputs/kitchen-v15-check-1-full-upgrade-fit.png`
5. `outputs/kitchen-v15-check-2-both-doors-open-clear.png`
6. `outputs/kitchen-v15-two-viewing-scales.png`

The full-upgrade image is a geometry-reservation check, not unapproved tier-3
art. Its five translucent boxes come directly from v15 `upgradeSlots`.

## Gate result

- 19/19 transparent pieces have the exact v15 canvas and placement box.
- Five ordinary base cupboards: one 168 × 137 byte-identical master.
- Two wall cupboards: one 136 × 101 byte-identical master.
- Visible cupboard-to-cooker spacing: 16 px left / 16 px right.
- Unit base y = 485; worktop box y = 317–348; surface datum y = 326.
- Keeper remains byte-identical at 120 × 298, soles y = 502.
- Both 168 × 336 doors open clear: 118 px left / 37 px right.
- Exact-magenta glass pixels: 30,752; near-magenta outside glass: 0.

Full per-piece evidence is in `GATE_REPORT.md` and `gate-report.json`.

## Rebuild and verify

```sh
/Users/frank/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 review/kitchen-v15-painted-room-v5/build_kitchen_v15_v5.py
/Users/frank/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 review/kitchen-v15-painted-room-v5/verify_kitchen_v15_v5.py
```

Stop here for Frank. Do not promote, integrate or deploy this review candidate.

## Documentation audit

Completed before handoff. The review folder, `docs/SPEC.md`, root `README.md`,
v15 schematic, deployment guard, generated manifests and runtime state were
compared. Root documentation and section 19 identify v5 as the current
review-only candidate; runtime and deployment remain untouched.
