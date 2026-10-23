# Kitchen Fixed Shell Layout V7

Date: 23 October 2026

Status: unapproved room-fit correction review; no runtime or production promotion

Review route: `/keeper-review/kitchen-fixed-shell-layout-v7`

## Scope

V7 corrects the shared fitted-shell defects visible in V6. It does not redraw
or change the approved sink, dishwasher, oven, fridge, kettle or toaster art.
It also leaves every state mapping, bay position, interaction point and movement
rule unchanged.

The corrected shell has:

- one deterministic `504 × 10` logical-pixel worktop with only two outer ends;
- no sampled blue underside below that worktop, so fascia and door tops remain visible;
- an opaque Belfast-sink overlay that visibly cuts through the worktop front;
- one flat monotone-blue backing and a declared ink/blue carcass palette;
- shared dividers and a continuous plinth containing no sampled highlight pixels;
- no curved source-cabinet patch behind the drawers; and
- no separate healing layer.

V6 remains immutable at `/keeper-review/kitchen-fixed-shell-layout-v6` as the
architecture predecessor and comparison evidence.

## Geometry and behaviour retained

The six fitted bodies remain exactly `84 × 74 px`, with origins
`84, 168, 252, 336, 420, 504`, centres `126, 210, 294, 378, 462, 546`, worktop
support `y=141`, floor support `y=208` and Keeper stop/turn plane `y=218`.
Kettle and toaster remain owned by distinct cupboard/drawers identities and
move with them. Broken appliances remain locked until repaired. The page still
preloads and decodes one lossless atlas before enabling its controls.

## Reproducibility

Build and verify:

```sh
/usr/bin/python3 scripts/build_kitchen_fixed_shell_layout_v7.py
npm run maintain:keeper-review
node scripts/verify_kitchen_fixed_shell_layout_v7.mjs
npm test
```

The verifier checks approved authority hashes, the complete grid contract, the
single archived atlas, exact worktop dimensions, Belfast overlay role, page
JavaScript, route wiring and every pixel in the flat carcass palette.

## Boundary

V7 is reversible review evidence. It changes no approved source, runtime state
behaviour, production sprite, game selector, Kettle V47 motion/audio contract
or deployment architecture. Frank still approves or rejects the assembled room.
