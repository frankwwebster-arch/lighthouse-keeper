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
| Chair / sofa / toilet seat | Legacy runtime datum: 11 px above floor; superseded for approved Prime side-right authoring, but unchanged in runtime until separately promoted |
| Basic armchair / rocking chair / Lazyboy-style recliner | Approved side-right Prime authoring datum: measured support surface 7.75 px above floor; other orientations must be measured from their approved seated underside rather than inheriting the rejected 11-px row |
| Bed mattress | 9 px above floor |
| General dining, writing and standing kitchen surface | 19 px above floor |
| Kitchen V21 side-right table for one | 14.5 px above floor; 1.5 px thick; 20 px wide; exactly one V6-sized chair |
| Workbench | 17 px above floor |
| Low coffee table | 12 px above floor |
| Door handle | 20 px above floor |
| Light switch, instrument and lift control | 23 px above floor |
| Rear lift entry | opening at least 24 × 40 px; `keeper_walk_into_lift` bakes a 100%→75% depth scale and 0→−6 px vertical path |
| TV screen centre from a seated keeper | 26 px above floor |
| Machete plant-cut contact | 12 px above floor; 18 px right of keeper anchor |
| Guitar rack grip | 31 px above floor; keeper hand `(45,25)` on the 64 × 56 pickup canvas; prop transfers on frame 6 |

The current V6 side-sitting review candidate records the corrected Prime-derived
chair registration in `data/keeper_prime_seat_geometry_v3.json`. Live review
proved that the former 11-pixel row passed through the pelvis and therefore was
not the top support surface. The final side-right silhouette ends at source
y=257, so the chair top begins on the first transparent row y=258: world
y=44.25, or **7.75 px above the floor**. The earlier review also proved that
the `[7,29]` back/spine contact had been used as the rear edge of the backrest
rather than its front face, and `[18,29]` did not keep the seat rim behind the
visible shins. At the fixed V6 action root, the
backrest front is world x=76.625 and exactly meets the visible back/spine
contact plane; the front rim is x=83.75; and the measured rear shin plane is
x=84.25, leaving 0.5 px clearance. The review proxy therefore has an 8.625-px
total side depth and 7.125 px usable depth ahead of the backrest front. These
values were approved with exact V6 on 17 October 2026 and are the side-right
Prime furniture-authoring authority. They do not rewrite the immutable runtime
contract until a separate promotion is instructed. V1–V5 remain
rejected/superseded measurement provenance rather than a furniture-authoring
authority. The approval record is
`docs/review/keeper-prime-sit-stand-side-v6-approval-2026-10-17.json`.

These are baseline contact dimensions, not object-fitting suggestions. Object
silhouettes and tiers may change, but their keeper-facing contact points follow
the reviewed pose. The keeper is never automatically resized to make an object
work; Frank's saved visual resize is applied first. In particular, the
cake and plated-meal placement strips now use the 19 px standard table datum;
the 12 px datum is reserved for genuinely low coffee tables.

Kitchen V21 adds one deliberately narrower scope rather than silently changing
the general table contract. Its side-right table for one follows the approved
V6 seated pose: a 7.75-px chair support, 8.625-px chair depth and 0.5-px shin
clearance, with the tabletop at the visible seated hand line, 14.5 px above
the floor. The 20-px table has a 1.5-px top and exactly one chair. These values
are recorded as `kitchenTableForOneV21` in
`data/keeper_object_dimensions.json`; they do not alter the 19-px general
dining/writing/standing-worktop datum or any runtime contract.

Widths and depths marked `provisional-envelope` may still be refined when final
object artwork is made. Heights and contact points marked
`authoritative-datums` are already locked for asset creation.
