# Kitchen Oven V41 design record

V41 corrects rejected V40 without modifying it. The binding measurement and
colour authority is the initially approved V21 isolated oven:
`art/raw/kitchen-final-assets-2026-10-17-v21/basic-oven.png`, SHA-256
`45658c2649d10efc896d646821b16e12d3a19fc401d04168e00ace3a6f016ba8`.

Every Off, On and Broken state uses the exact original `108 × 120` review cell
and exact exclusive opaque bounds `[12,31,96,108]`, an `84 × 77` footprint.
The approved hob and sea-glass surround in rows `31:48` are copied
byte-for-byte into every state. The coordinated generated fascia below it is
normalized to `84 × 60` and restricted to a 48-colour palette derived only
from visible V21 oven pixels.

At native room scale the exact footprint sits at x=`336:420`, y=`131:208`.
The prior oven and hob are cleared first. The fitted cabinet plinth remains
visible below the appliance to the room's y=218 floor line.

The object states remain static. Broken smoke is a connected, curling,
semi-transparent plume constructed without circular puff primitives. Hob
flames and the intermittent angry warning/internal flicker are also separate
40-frame, 4-fps, ten-second effect strips.

