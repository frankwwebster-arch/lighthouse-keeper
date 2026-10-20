# Kitchen Modular Fridge Workbench V34

Date: 20 October 2026

Status: reversible visual-review draft; awaiting visual review, unpromoted and
unwired.

Review page: `/keeper-review/kitchen-modular-fridge-workbench-v34/`

## Purpose

V34 adds the fridge to the exact modular placement and join system approved in
V33. It does not redraw the fridge: the exact approved V39 Standard, Broken and
40-frame drip/ripple sprites are reused byte-for-byte. This preserves the white
door, one lower grille, failed top hinge, attached lower hinge, visible generic
contents, floor-contacting door corner and static floor puddle.

The exact approved V33 cabinet, sink, oven, fault and join pixels are also
unchanged. V34 is a new reversible compositor and review shell only.

## Three-asset placement contract

- Canonical bay origins remain `[84,168,252,336,420,504]`.
- The exact V11 two-bay cabinet run remains fixed at origins 168 and 252.
- Fridge, sink and oven each occupy one distinct origin from
  `[84,336,420,504]`.
- Loose pointer movement is preview-only. Release commits to the nearest legal
  origin not occupied by either other movable appliance.
- Each logical collision body is 84 pixels wide; each Prime stop/turn anchor is
  the committed origin plus 42, at y=218.
- The broken fridge's fallen door and puddle may extend outside its logical
  body as foreground art without changing its collision or anchor geometry.

## Pair-aware join resolver

The V33 precedence remains authoritative and gains one fridge-specific rule:

1. Any pair containing the oven uses the V32 triangular join.
2. Cabinet↔sink uses the V22 flat join.
3. A pair containing the fridge but no oven receives only the six-pixel blue
   body backfill. No foreground cap is drawn: the fridge has a complete
   standalone top and a natural four-pixel neighbour overlap.
4. A sink with no exact left neighbour uses the V25 cutout and rounded end.
5. Exposed oven and fridge edges remain standalone; no bridge is invented.

## States, motion and sound

The fridge has Standard and Broken states. Broken door, contents and floor
puddle are static. `fx-fridge-drip-ripple-f40.png` remains a separate,
removable, reusable 40-frame strip at 4 fps for a ten-second loop, with review
speed from 0.1× to 4×. The named placeholders are
`kitchen_fridge_low_electrical_buzz_loop` and
`kitchen_fridge_water_drip_slow`; the low buzz has no visible electrical
effect.

## Verification

Run:

```sh
npm run verify:kitchen-modular-join-workbench-v33-approval
npm run verify:kitchen-modular-fridge-workbench-v34
npm run build
```

The V34 verifier checks byte identity against V33 and V39, all 24 legal
three-appliance placements, exact Prime midpoints, state gutters, 40 isolated
effect frames, archive integrity, preload/decode locking and the reversible
Final/runtime boundary.

Documentation audit completed against the delivered catalogue, review shell,
archive manifest, route, approved V33/V39 authorities, tests, deployment rules
and no-promotion boundary. README, STATUS and DECISIONS now identify V33 as the
approved placement/join authority and V34 as the only active fridge successor.
