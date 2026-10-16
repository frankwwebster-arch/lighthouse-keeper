# Kitchen V6 countertop calibration source record

This folder records the first approval gate for the replacement Kitchen V6.
Kitchen Basic Assets V5 is the sole visual and geometric input. The removed,
rejected former V6 is not read, copied, transformed or imitated.

The candidate pixels are produced deterministically by
`scripts/build_kitchen_countertop_calibration_v6.py` from the exact V5
standard kettle, cooker and sink rasters. Only each declared countertop/hob
mask may change. Cabinet, oven and sink fronts outside those masks remain exact
V5 bytes.

An exploratory built-in image-generation study was used only to check the
visual brief. It contributes no candidate pixel. The normalized prompt is in
`imagegen-prompt.txt`; the generated preview remains outside the repository.

This is a review-only calibration gate, not a full Kitchen V6 family.
