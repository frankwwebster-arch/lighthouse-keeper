# Kitchen Sink Perspective Correction V15

Date: 19 October 2026

Status: reversible visual-review draft; unapproved and unpromoted

Review route: `/keeper-review/kitchen-sink-perspective-correction-v15/`

V15 supersedes V13/V14 for active sink review without modifying either older
draft. Frank identified two remaining faults: V14's On water began a few pixels
below the tap and V13's sink cabinet did not share the approved V11 cabinet
projection. Frank approved the V14 Broken basin-spout animation.

The complete sink unit was redrawn from scratch with the exact V11 cabinet run
as the binding projection and palette reference. It remains one independent
84 × 74-pixel bay containing its own cabinet, shallow worktop, basin and intact
tap. It does not overlay an approved cabinet. The 92 × 108-pixel cell retains a
four-pixel transparent gutter and tap headroom. Standard, On base and Broken
base are byte-identical.

The V14 On strip is translated upward by exactly two pixels in every cell,
without recolouring, resizing or changing its 40 frames. This makes the water
meet the outlet. The V14 Broken strip is copied byte-for-byte. Both remain
4-fps, ten-second loops; review playback can vary from 0.1× to 4×. SFX
placeholders remain `kitchen_sink_water_gentle_loop` and
`kitchen_sink_pipe_burst_loop`.

The generated source is
`art/source/kitchen-sink-perspective-correction-2026-10-19-v15/sink-cabinet-perspective-redraw.png`.
The built-in image-generation workflow treated V13 as the subject reference
and exact approved V11 as the strict projection, construction, palette and
pixel-fidelity authority. The final prompt required a fresh, transparent,
straight-on one-bay redraw with parallel sides, a constant-height shallow
worktop, V11 front-plane proportions, an intact tap and basin, and no water.

Deterministic verification pins the generated source and approved V11 hashes,
checks all static state geometry and gutters, proves the On frames are an exact
two-pixel translation of V14, verifies visible tap-outlet contact in every
frame, and requires the Broken strip to remain byte-identical to V14. Final and
runtime art remain unchanged.
