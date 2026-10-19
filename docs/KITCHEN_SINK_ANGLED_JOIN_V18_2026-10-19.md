# Kitchen Sink Angled Join V18

Date: 19 October 2026

Status: reversible visual-review draft; unapproved and unpromoted

Review route: `/keeper-review/kitchen-sink-angled-join-v18/`

V17 is rejected because adding a broad return outside the V11 bay left the
countertop reading as a uniformly extended left side. The required line is a
single shallow perspective join across the visible depth of the worktop.

V18 preserves the exact approved V11 cabinet front as the visual hero. Only
the nine-row shallow worktop strip above it is reconstructed. At its rear/top
edge the sink worktop begins three native pixels left of the cabinet body. Its
outer boundary then steps one pixel right after every three rows until it meets
the unchanged body at x=4. The original vertical worktop end line is replaced
inside this small region rather than remaining visible beneath the extension.
The sprite retains a fully transparent outer safety gutter.

The intact V17 tap and basin are retained byte-for-byte. The basin supplies the
opposing perspective cue requested for the fixture: its rear rim spans native
x=20–70 while its front lip spans x=18–73, so both side edges splay slightly
toward the player. The wider front remains deliberately restrained so the
cabinet face, not the basin, dominates the asset.

Standard, On base and Broken base are byte-identical. The corrected On outlet
stream and approved Broken upward-basin jets remain separate, byte-identical
V17 water-only strips: 40 frames, 4 fps and ten seconds, with SFX placeholders
`kitchen_sink_water_gentle_loop` and `kitchen_sink_pipe_burst_loop`.

The verifier pins the approved V11 source hash, the exact front-elevation
pixels, every row of the down-right join, the opposing basin spans, all four
transparent cell gutters, identical static bases, unchanged animation hashes
and the content-addressed review archive. V11, V17, Final and runtime remain
unchanged.
