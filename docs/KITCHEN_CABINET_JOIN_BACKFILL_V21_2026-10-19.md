# Kitchen Cabinet Join Backfill V21 — 19 October 2026

## Purpose

V21 tests a small dynamic structural layer behind adjacent cabinets so
partially transparent edge pixels resolve against cabinet colour rather than
the pale wall. It does not amend, regenerate or bake pixels into either asset.

Review route: `/keeper-review/kitchen-cabinet-join-backfill-v21/`

## Layer order

1. room background;
2. join backfill; and
3. independently movable cabinet sprites.

The source room, exact approved V11 two-bay run and complete V19 sink cabinet
are copied byte-for-byte into the review set.

## Semi-dynamic rule

For neighbouring cabinet bodies A and B:

- compute the horizontal gap from `A.right` to `B.left`;
- when that gap is between -6 and +8 pixels, draw the backfill from
  `A.right - 3` through `B.left + 3`;
- begin below the worktop, then restrict its remaining height to the
  intersection of the neighbours' declared cabinet body bounds; and
- draw nothing when the units separate by more than eight pixels.

The three-pixel underlap means translucent antialiased edge pixels see cabinet
colour behind them. The maximum-gap rule prevents a floating blue bridge when
the player deliberately moves a unit away.

## Visual treatments

- **Colour matched:** one solid row colour derived deterministically from the
  corresponding row of the exact approved V11 cabinet.
- **Shadow seam:** the same approved row palette darkened by 24%, making the
  join read as a narrow structural recess.

Both are separate 14 × 63 px templates expanded only across the live small-gap
span. Neither contains or replaces any cabinet pixel.

## Review interaction

The page lets Frank drag the sink horizontally, enter its exact body X,
switch backfill style, adjust the maximum small-gap threshold, disable the
backfill and show logical body bounds. It demonstrates the proposed runtime
relationship without wiring any runtime scene.

## Boundaries

V21 is reversible, unapproved and unpromoted. V11, V19, V20, the room
background, Final art and runtime remain unchanged. Rejection requires deleting
only the V21 raw/draft/review directories and archive manifest.
