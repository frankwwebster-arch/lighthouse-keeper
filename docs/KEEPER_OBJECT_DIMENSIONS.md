# Keeper-derived object dimensions

The keeper's delivered reviewed pose is the ruler for the world. The baseline
machine-readable dimensions are in `data/keeper_object_dimensions.json`; they
are derived from the anatomy and interaction contacts in
`data/keeper_asset_contract.json`. Frank's saved per-animation width and height
remain authoritative, and authoring transforms the pose's contact points with
that saved size before runtime object placement.

The main furniture datums are:

| Object | Authoritative datum |
| --- | ---: |
| Chair / sofa / toilet seat | 11 px above floor |
| Basic armchair / rocking chair / Lazyboy-style recliner | 11 px above floor for every tier; rocking/recline occurs on the furniture layer |
| Bed mattress | 9 px above floor |
| Dining, writing and kitchen surface | 19 px above floor |
| Workbench | 17 px above floor |
| Low coffee table | 12 px above floor |
| Door handle | 20 px above floor |
| Light switch, instrument and lift control | 23 px above floor |
| Rear lift entry | opening at least 24 × 40 px; `keeper_walk_into_lift` bakes a 100%→75% depth scale and 0→−6 px vertical path |
| TV screen centre from a seated keeper | 26 px above floor |
| Machete plant-cut contact | 12 px above floor; 18 px right of keeper anchor |
| Guitar rack grip | 31 px above floor; keeper hand `(45,25)` on the 64 × 56 pickup canvas; prop transfers on frame 6 |

The current V5 side-sitting review candidate records the corrected Prime-derived
chair registration in `data/keeper_prime_seat_geometry_v2.json`: **11 px is the
top surface of the seat**, not its centre or underside. Live review disproved
V1's 11-pixel placement: the `[7,29]` back/spine contact had been used as the
rear edge of the backrest rather than its front face, and `[18,29]` did not keep
the seat rim behind the visible shins. At the fixed V5 action root, the
backrest front is world x=76.625 and exactly meets the visible back/spine
contact plane; the front rim is x=83.75; and the measured rear shin plane is
x=84.25, leaving 0.5 px clearance. The review proxy therefore has an 8.625-px
total side depth and 7.125 px usable depth ahead of the backrest front. These
horizontal values remain review-only until Frank approves V5; they do not
rewrite the immutable runtime contract. V1 remains rejected measurement
provenance rather than a furniture-authoring authority.

These are baseline contact dimensions, not object-fitting suggestions. Object
silhouettes and tiers may change, but their keeper-facing contact points follow
the reviewed pose. The keeper is never automatically resized to make an object
work; Frank's saved visual resize is applied first. In particular, the
cake and plated-meal placement strips now use the 19 px standard table datum;
the 12 px datum is reserved for genuinely low coffee tables.

Widths and depths marked `provisional-envelope` may still be refined when final
object artwork is made. Heights and contact points marked
`authoritative-datums` are already locked for asset creation.
