# Keeper-derived object dimensions

The keeper is the ruler for the world. The authoritative machine-readable
dimensions are in `data/keeper_object_dimensions.json`; they are derived from
the fixed anatomy and interaction contacts in `data/keeper_asset_contract.json`.

The main furniture datums are:

| Object | Authoritative datum |
| --- | ---: |
| Chair / sofa / toilet seat | 11 px above floor |
| Bed mattress | 9 px above floor |
| Dining, writing and kitchen surface | 19 px above floor |
| Workbench | 17 px above floor |
| Low coffee table | 12 px above floor |
| Door handle | 20 px above floor |
| Light switch, instrument and lift control | 23 px above floor |
| TV screen centre from a seated keeper | 26 px above floor |
| Machete plant-cut contact | 12 px above floor; 18 px right of keeper anchor |

These are contact dimensions, not suggestions. Object silhouettes and tiers may
change, but their keeper-facing contact points remain fixed within 0.5 logical
pixel. The keeper is never resized to make an object work. In particular, the
cake and plated-meal placement strips now use the 19 px standard table datum;
the 12 px datum is reserved for genuinely low coffee tables.

Widths and depths marked `provisional-envelope` may still be refined when final
object artwork is made. Heights and contact points marked
`authoritative-datums` are already locked for asset creation.
