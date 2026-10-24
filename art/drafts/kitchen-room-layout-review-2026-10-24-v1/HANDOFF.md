# Kitchen room layout review V1

Status: rejected on 24 October 2026. Retained only as immutable rejection
evidence; never use this page as a kitchen art reference.

Review route: `/keeper-review/kitchen-room-layout-v1/`.

The page composes the already-approved exact 84 × 74 fitted bodies in the full
772 × 224 room grid. Loose toaster, kettle, bin, bowl, table and chair images
are CSS-clipped directly from the approved high-resolution master. No pixels
are extracted into a candidate asset and no old superseded kitchen draft is
restored.

Movement rules follow `data/kitchen_room_grid_contract_v2.json`: fitted units
swap exact bays, kettle/toaster follow cupboard/drawer identity, the bowl stays
on the worktop, and bin/table/chair snap to declared floor sections. Broken
appliances remain locked until repaired.

The page was rejected because it used reduced 84 × 74 runtime bodies for visual
review, resized source crops, applied a colour-changing multiply blend and
placed the result on an invented schematic canvas. V2 replaces it at native
source resolution. Runtime Promotion V1, the approved V4 package and the legacy
rollback sprite remain byte-identical.
