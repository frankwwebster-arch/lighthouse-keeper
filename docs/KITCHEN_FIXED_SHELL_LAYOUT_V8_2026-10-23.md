# Kitchen Fixed Shell Layout V8

Date: 23 October 2026

Status: unapproved material/seam and sink-mask review; no runtime promotion

Review route: `/keeper-review/kitchen-fixed-shell-layout-v8`

## Corrections

V8 retains the fixed-shell architecture and approved functional art but
replaces the two treatments Frank rejected in V7.

The internal fitted joins now contain:

- approved cabinet-face shading extending to within one master pixel of each bay boundary;
- one narrow shared ink seam;
- no flat light-blue or dark-blue divider surface;
- no repeated highlight strip or sampled rail; and
- one continuous shaded backing and plinth field across the complete run.

The sink overlay now contains only geometry-selected porcelain, orange
hardware, their adjacent black outlines and approved state water.
It contains no source countertop colour or independent rear boundary. The
single fixed worktop is therefore visible continuously behind the sink and
supplies the same cyan, height and line weight as every other bay.

Only the leftmost and rightmost exposed ends receive shallow darker perspective
planes. Internal bays remain front-on. The room background retains the floor
margin in front of the run without changing the locked interaction geometry.

## Retained contract

- Fitted bodies: exactly `84 × 74 px`.
- Origins: `84, 168, 252, 336, 420, 504`.
- Centres: `126, 210, 294, 378, 462, 546`.
- Worktop support: `y=141`.
- Cabinet floor support: `y=208`.
- Keeper stop/turn plane: `y=218`.
- Kettle and toaster: distinct cupboard/drawers owners, centred and carried with their owner.
- Broken fitted units: locked until repaired.
- State mappings and approved source hashes: unchanged.
- Healing layer: absent.

## Rebuild and verification

```sh
/usr/bin/python3 scripts/build_kitchen_fixed_shell_layout_v8.py
npm run maintain:keeper-review
node scripts/verify_kitchen_fixed_shell_layout_v8.mjs
npm test
```

The verifier rejects any opaque blue surface outside the narrow internal ink
seams and rejects countertop-coloured sink pixels outside the central stream,
while allowing the Broken state's pale overflow. It also checks the approved authority hashes, complete grid,
state map, single archived atlas, JavaScript, delivery route and archive hash.

## Boundary

V8 is reversible review evidence. It changes no approved source, production
sprite, game selector, runtime state behaviour, Kettle V47 motion/audio
contract or deployment architecture. V6 and V7 remain immutable comparison
evidence. Frank still approves or rejects the assembled room.
