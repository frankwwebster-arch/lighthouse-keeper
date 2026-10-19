# Kitchen Sink Cabinet Extension V16

Date: 19 October 2026

Status: reversible visual-review draft; unapproved and unpromoted

Review route: `/keeper-review/kitchen-sink-cabinet-extension-v16/`

V15 is rejected because a newly drawn cabinet can remain stylistically close
to approved V11 while still having different structural perspective. Its
sloped worktop shoulders, drawer/door proportions, side rails and plinth do not
form a continuous cabinet system beside V11.

V16 treats the sink as an extension of the approved cabinetry and also as an
independently removable asset. Its complete 84 × 74-pixel structural shell is
a literal crop of the approved V11 right-hand bay. Only a central inset basin
and intact tap fixture amend those pixels. At runtime or review, V16 is one
complete 92 × 108-pixel transparent sprite; there is no separate cabinet
underneath it.

This construction makes the adjoining worktop, fascia, drawer, doors, rails,
outlines and plinth byte-exact V11 geometry. The sink body's bounds remain
x=336–420 and y=134–208 in the native room proof. Standard, On base and Broken
base remain byte-identical.

No image-generation redraw was used for V16 because exact geometry—not visual
approximation—is the binding requirement. V15's corrected On strip and its
approved Broken strip are both retained byte-for-byte. They remain water-only
40-frame, 4-fps, ten-second loops with named SFX placeholders
`kitchen_sink_water_gentle_loop` and `kitchen_sink_pipe_burst_loop`.

The verifier compares all 6,216 structural pixels directly with the approved
V11 crop, proves the finished asset is exactly that bay plus the isolated
fixture, pins both animation-strip hashes, and verifies the reversible review
archive. V11, V15, Final and runtime remain unchanged.
