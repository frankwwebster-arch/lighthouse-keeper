# Kitchen final assets V21 recipe

**Status:** complete final review candidate; awaiting visual acceptance; not
promoted or wired.

**Review:** `/keeper-review/kitchen-final-assets-v21/`

V21 completes the V20 fitted-galley asset family in response to Frank's review.
V20 remains immutable. Its storm-blue fronts, sea-glass worktop, aged-copper
hardware, navy outlines, rectangular projection, `21-lp` bay and `52-lp` foot
line remain the visual and construction authority.

## Complete basic set

The default room contains, left to right:

1. simple standalone pedal bin;
2. undercounter fridge;
3. kettle counter;
4. toaster counter;
5. compact basic oven;
6. mixing-bowl counter;
7. sink;
8. table for one with exactly one chair.

The six cabinet assets form one fitted run. The bin and table/chair are
standalone floor items. The former V20 double oven remains available only as
Upgrade 1 and is shown in a separate, otherwise identical room state.

## Oven tiers

| Tier | Cabinet bay | Appliance | Doors |
| --- | ---: | ---: | ---: |
| Basic | 21 lp | about 15 lp inset | 1 |
| Upgrade 1 | 21 lp | V20 oven/grill | 2 |

The basic appliance is visibly narrower than its cabinet frame, with
storm-blue stiles on both sides. Its compact hob, controls, handle and single
door are one appearance. The Upgrade 1 image is byte-derived from the immutable
V20 appearance; it is not redrawn.

## Standalone pedal bin

The bin is a closed `10 × 13-lp` floor item with one centred copper pedal. It
has no cabinet, countertop, rubbish, open state or bay-wide body in the basic
appearance.

## Table and one chair

The V6 side-right sitting review is the geometry authority:

| Datum | Value |
| --- | ---: |
| Seat support above floor | 7.75 lp |
| Total chair depth | 8.625 lp |
| Seat-rim clearance behind shin | 0.5 lp |
| Chair top above seat | 12 lp |
| Tabletop above floor | 14.5 lp |
| Tabletop thickness | 1.5 lp |
| One-person table span | 20 lp |

The tabletop height is fixed to the seated Prime hand line in the exact V6
final pose. The draw order is chair, Keeper, table. This leaves the chair
behind him and the table in front of his hands and knees.

The generated source deliberately separates chair and table. The deterministic
builder crops them independently and normalizes the chair in two vertical
segments around the seat plane, so generated proportions cannot move the V6
support datum. Both pieces share the exact foot line.

## Room proof

The complete room is `193 × 56 lp` (`772 × 224 px` at density 4): one open bay
for the bin, six fitted cabinet bays, and two bays for the table/chair. Cabinet
and furniture pixels stop at the `52-lp` foot line; rows `208–223` remain the
clear 4-lp foreground channel.

Five internal fitted-run seams receive only narrow worktop/plinth continuity
bridges. The outer bay images remain intact, and no end cap is added at an
internal join. The basic and Upgrade 1 room proofs differ only inside the oven
bay.

## Rebuild and verification

Use the bundled Python runtime with Pillow, or any Python environment providing
Pillow:

```sh
python3 scripts/build_kitchen_final_assets_v21.py
npm run archive:keeper-review
npm run verify:kitchen-final-assets-v21
npm test
```

The verifier pins all three generated sources and fourteen deterministic
outputs; checks dimensions, alpha gutters, V6 measurements, clear foreground,
five worktop joins and oven-only room variation; and verifies archived media
when the set manifest exists.

Rollback is deletion of only the V21 source/raw/draft/review files, its scripts
and docs, and its archive manifest/objects. V20, exact V5, Keeper art, Final and
runtime assets remain unchanged.
