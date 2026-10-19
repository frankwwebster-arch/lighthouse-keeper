# Kitchen Sink Cabinet V13 — standalone fit gate

Date: 19 October 2026

Status: reversible visual-review draft; unapproved, unpromoted and unwired

Review route: `/keeper-review/kitchen-sink-cabinet-v13/`

V13 supersedes Layout V12's proposed sink-overlay registration. The sink is a
complete standalone one-bay unit with its own 84 × 74-pixel cabinet body,
worktop, basin and tap. No approved cabinet is placed beneath it and it does
not contain a copied room, wall, floor or neighbouring cabinet.

The fit proof places the exact approved 168 × 74-pixel V11 two-cabinet run at
`x=168–336/y=134–208` and the independent sink body immediately beside it at
`x=336–420/y=134–208`. Their bounds meet but never overlap.

Frank rejected a snapped-tap broken state because the detached section appeared
to float. The corrected standard, On base and Broken base therefore use one
byte-identical intact sink unit. Later separate reusable water strips—not
object changes—will distinguish On from Broken. V13 deliberately adds no water
animation until the static unit and its perspective join are visually approved.

The generated three-state first pass is retained only under `rejected-sources/`
as provenance. It is not shown as a candidate and must not be reused for the
broken state.
