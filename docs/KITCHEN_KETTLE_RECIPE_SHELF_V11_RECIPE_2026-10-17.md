# Kitchen V11 kettle recipe-book shelf recipe

Date: 17 October 2026  
Status: review draft; not approved, promoted or wired

V11 leaves the complete V10 kitchen immutable and adds one decorative wall
child above `obj_kettle`: a deliberately uneven run of recipe books held by a
kitchen jar at each end. The jars are visual bookends, not interaction spots.

- Cell: `21 × 56 lp` at 4× density.
- Opaque width: at most `19 lp`, preserving one-lp side gutters.
- Opaque height: at most `14 lp`.
- Shelf bottom: `19 lp` from the room top, clear of the kettle silhouette.
- Default parent bay: kettle bay 3.
- Transform: `shelfDeltaLp == kettleDeltaLp`, proven at bays 2, 5 and 8.
- Projection: straight-on `flat-cutaway-v1`; horizontal shelf; no convergence.
- Interaction spot: none.
- Runtime wiring: none.

The high-resolution source study and exact built-in prompt are preserved under
`art/source/kitchen-kettle-recipe-shelf-2026-10-17-v11/`. The builder thresholds
faint canvas alpha before measuring, scales within the declared bounds, and
centres the result in the bay without changing V10.
