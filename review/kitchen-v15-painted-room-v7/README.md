# Kitchen v15 painted room v7 — common furniture depth correction

Status: **review candidate awaiting Frank**. This folder is review-only. No
runtime art, canon, production manifest, public asset or deployment changed.
V6 remains unchanged and is the reversible predecessor.

V7 corrects the remaining dresser-depth fault without changing the approved
v15 furniture layout or any other v6 part:

- the complete lower dresser carcass—drawers, doors, plinth and feet—now fills
  local y199–336, which is room y348–485;
- its painted front/base contact is therefore y485, exactly matching the
  fridge, cooker, sink cabinet and every ordinary 0.60m base cabinet;
- the gate checks all nine floor-standing kitchen units individually and fails
  unless every painted alpha bottom is exactly room y485.

V7 inherits v6's earlier corrections:

- the structural room shell no longer contains a door leaf; the same approved
  168 × 336 compass-rose leaf is transformed into a closed side-wall quad or
  placed unmodified at the 90-degree open endpoint, never both;
- the side-door apertures and moving leaves share y208–544, so the shell and
  door contract are the same 336 px high;
- the approved v8 Belfast sink is split at the existing v15 piece boundary:
  taps/rim are set into run A's 504 × 31 worktop and the apron continues in the
  168 × 137 sink cabinet; its lower body is the standard cupboard master;
- the dresser still uses the same 31 px worktop-depth band at room y317–348 as
  the fitted run.

The original brighter duck-egg 2172 × 724 source remains byte-identical
(SHA-256 `404c4b095ee64b1b5ba37f5cea23d24081b0e1a6c70f824563e5edef93846e15`).

## Review order

1. `outputs/kitchen-v15-correction-gate.png`
2. `outputs/kitchen-v15-check-3-day1-room.png`
3. `outputs/kitchen-v15-check-2-both-doors-open-clear.png`
4. `outputs/kitchen-v15-piece-gate-sheet.png`
5. `outputs/kitchen-v15-cabinet-edge-gate.png`
6. `outputs/kitchen-v15-check-1-full-upgrade-fit.png`
7. `outputs/kitchen-v15-two-viewing-scales.png`

The focused correction gate shows the closed and open shell states together,
the shared cupboard/sink body, the dresser/run depth band and the complete
dresser carcass ending on y485. The piece sheet
still distinguishes the exact v15 canvas from the painted alpha bounds; no
coordinate-only room crops are presented as assets.

## Gate result

- 19/19 transparent pieces have the exact v15 canvas and placement box.
- Five ordinary 168 × 137 cupboards remain byte-identical.
- Two 136 × 101 wall cupboards remain byte-identical; cooker gaps remain
  16 px on both sides.
- Sink rows y42–137 equal the standard base cupboard byte-for-byte.
- Dresser local y168–199 is the shared 31 px worktop band at room y317–348.
- Dresser lower carcass local y199–336 is room y348–485.
- All nine 0.60m floor units have painted front/base contact y485.
- The jamb-only shell, closed leaves and open leaves are state-exclusive.
- Both open 168 × 336 leaves clear furniture by 118 px left / 37 px right.
- Unit base y485, worktop y317–348, surface datum y326, Keeper soles y502.
- Exact-magenta glass pixels: 30,752; near-magenta outside glass: 0.

Run A and run B worktops are intentionally no longer byte-identical: run A
contains the approved sink rim/taps, while run B remains the clean worktop
master. Their canvas, depth and front-edge datums remain identical.

## Rebuild and verify

```sh
/Users/frank/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 review/kitchen-v15-painted-room-v7/build_kitchen_v15_v7.py
/Users/frank/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 review/kitchen-v15-painted-room-v7/verify_kitchen_v15_v7.py
```

Stop here for Frank. Do not promote, integrate or deploy this review candidate.

## Documentation audit

Completed before handoff. The review folder, `docs/SPEC.md`, root `README.md`,
v15 schematic, door handoff, deployment guard, manifests and runtime state were
compared. V7 is documented as review-only; runtime and deployment are untouched.
