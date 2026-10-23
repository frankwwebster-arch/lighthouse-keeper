# Kitchen Fixed Shell Layout V10

Date: 23 October 2026

Status: unapproved full-end-perspective and Broken loose-state review; no runtime promotion

Review route: `/keeper-review/kitchen-fixed-shell-layout-v10`

## Correction

V9 is retained as the accepted front-view authority. Its complete cupboard and
drawer top outlines, shared worktop, sink mask, fitted faces, six exact bays
and all support/interaction coordinates remain unchanged.

V10 adds real cabinet depth outside that front grid. Each exposed bookend has
a `16 px` side return comprising one worktop return, one continuous carcass
side and one recessed plinth return. The front run remains exactly `504 px`:
the new returns occupy `x=68–83` and `x=588–603`, never any part of a bay.

The Broken dishwasher keeps the exact approved control panel, three red lamps,
interior, crockery and source water. Its fully horizontal door is removed. A
separate foreground door is attached across the bottom hinge and foreshortened
in a clearly part-open position; drawing it after the fixed shell prevents the
plinth from hiding or severing it.

## Loose Broken states

- Kettle: the accepted broken kettle is extracted from the pinned first-render
  authority. It carries no baked steam.
- Toaster: every accepted V9 casing pixel remains unchanged. A clearly burnt,
  jammed slice is layered behind its existing slot.
- Mixing bowl: the warm dimensional standard state includes its whisk. Broken
  retains the visible spill and places the whisk beside the cracked bowl.
- The bowl is a child of the table: it is centred on the table, moves with it
  and consumes no fitted cabinet or floor slot.
- Broken kettle/toaster states lock their supporting cabinet until repaired,
  matching the existing Broken movement rule.

## Retained contract

- Fitted bodies: exactly `84 × 74 px`.
- Origins: `84, 168, 252, 336, 420, 504`.
- Centres: `126, 210, 294, 378, 462, 546`.
- Worktop support: `y=141`.
- Cabinet floor support: `y=208`.
- Keeper stop/turn plane: `y=218`.
- Internal joins: one narrow ink seam; no blue divider or top fascia.
- Healing layer: absent.
- Approved/static sources, runtime selectors and production assets: unchanged.

## Rebuild and verification

```sh
/usr/bin/python3 scripts/build_kitchen_fixed_shell_layout_v10.py
npm run maintain:keeper-review
node scripts/verify_kitchen_fixed_shell_layout_v10.mjs
npm test
```

The verifier checks the immutable source hashes, V9 top-front boundary, exact
grid, external-return alpha ownership, unchanged dishwasher controls/interior,
foreground door geometry, exact opaque toaster casing pixels, transparent
loose-state canvases, one decoded atlas, review JavaScript and same-origin
archive delivery.

## Boundary

V10 remains reversible review evidence. Delete only its source-reference copy,
draft directory, review route and archive-set entry to reject it. V6–V9 remain
immutable comparison evidence. Frank still approves or rejects this candidate.
