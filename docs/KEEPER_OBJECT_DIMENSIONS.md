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

The current V2 side-sitting review candidate records a stricter Prime-derived
chair envelope in `data/keeper_prime_seat_geometry_v1.json`: **11 px is the top
surface of the seat**, not its centre or underside. The measured side-right
envelope is also 11 px deep, from the spine/back contact at cell `[7,29]` to
the back-of-knee line at `[18,29]` (source pixels `[56,232]` to `[144,232]` at
density 8). A chair may be shallower, but it must not project beneath or beyond
that knee line. This new depth rule remains review-only until Frank approves
V2; it does not rewrite the immutable runtime contract.

These are baseline contact dimensions, not object-fitting suggestions. Object
silhouettes and tiers may change, but their keeper-facing contact points follow
the reviewed pose. The keeper is never automatically resized to make an object
work; Frank's saved visual resize is applied first. In particular, the
cake and plated-meal placement strips now use the 19 px standard table datum;
the 12 px datum is reserved for genuinely low coffee tables.

Widths and depths marked `provisional-envelope` may still be refined when final
object artwork is made. Heights and contact points marked
`authoritative-datums` are already locked for asset creation.
