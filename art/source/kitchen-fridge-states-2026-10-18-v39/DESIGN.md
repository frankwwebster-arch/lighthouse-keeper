# Kitchen fridge V39 source design

V39 is a full redraw, not an amendment of V32 pixels. The standard and broken
states were generated together as one coordinated family using the approved
V31 room and V21 fridge only as palette, scale and projection references.

The selected V2 source keeps one 21-lp refrigerator carcass, a single lower
ventilation grille and the approved storm-blue, sea-glass, white-enamel and
copper palette. In the broken state the top hinge is absent, a compact copper
lower-right hinge arm visibly joins the fallen door to the carcass, the
lower-left door corner reaches the floor, generic contents remain visible and
the pool is flattened along the floor surface.

The source is reduced into a 136 × 104 transparent interaction cell. At room
placement `(58, 136)`, the standard opaque bounds are exactly
`(84, 140)–(168, 218)`. This matches the measured 21-lp bay and the actual
pixel floor surface in the approved V31 room.

Before either state is composited, the old fridge face is removed by replacing
only `(84, 151)–(168, 218)` with the corresponding prop-free cabinet face from
the adjacent bay. The existing continuous worktop at y=140–150 remains intact.
This makes it impossible for an old white door or old grille to survive under
the new state.

The 40-frame drip/ripple strip is a separate transparent environmental layer.
It contains no fridge pixels and runs at 4 fps for ten seconds.
