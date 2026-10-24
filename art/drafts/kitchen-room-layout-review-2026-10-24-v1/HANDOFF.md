# Kitchen room layout review V1

Status: interactive review surface awaiting Frank's requested amendments to the
loose assets shown along the bottom of the approved V4 source sheet.

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

This is not an artwork approval or runtime promotion. Remove only this draft,
`data/kitchen_room_layout_review_v1.json`, the versioned public review shell and
its content-addressed archive entry to reject it. Runtime Promotion V1, the
approved V4 package and the legacy rollback sprite remain byte-identical.
