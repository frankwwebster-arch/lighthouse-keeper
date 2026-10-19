# Kitchen Snap Grid Join V23 — 19 October 2026

## Question answered

The approved V22 visual join remains valid when furniture is player-movable,
provided free dragging is only a preview and never the persisted placement.
V23 proves the required placement contract.

Review route: `/keeper-review/kitchen-snap-grid-join-v23/`

## Canonical bay grid

- horizontal grid origin: x=84;
- bay width: 84 pixels;
- bay origins: 84, 168, 252, 336, 420 and 504;
- Prime stop/turn centres: 126, 210, 294, 378, 462 and 546; and
- interaction foot line: y=218.

The exact approved two-bay run occupies origins 168 and 252. Those positions
are therefore illegal destinations for the 84-pixel sink. Its legal origins in
this proof are 84, 336, 420 and 504.

## Drag and snap algorithm

1. While the pointer is down, show a translucent free-position preview.
2. Continuously calculate and highlight the nearest legal grid origin after
   footprint and occupancy checks.
3. On pointer release, discard the raw pointer coordinate and commit the exact
   legal origin.
4. Derive the interaction target from the committed body midpoint, never from
   the pointer or artwork's transparent cell.
5. Recalculate neighbouring logical bounds and activate the join treatment
   only for exact adjacency.

For the default sink position, the committed origin is x=336 and its midpoint
is `336 + 84 / 2 = 378`, exactly matching the established Prime stop/turn
anchor. Its left edge equals the cabinet run's right edge, so the logical gap
is exactly zero and V22 uses canonical registration.

## Upgrades

A two-bay 168-pixel appliance upgrade uses the same grid. Its start must have
two contiguous legal bays, and its Prime interaction point is the midpoint of
the full snapped body. The occupancy solver rejects placements that overlap a
fixed or already placed component.

## Boundaries

V23 is a reversible interaction proof. It reuses the exact approved V22 source
images and join templates byte-for-byte. It does not alter V22, Final art or
runtime and performs no promotion.
