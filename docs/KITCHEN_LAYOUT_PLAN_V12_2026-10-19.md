# Kitchen Layout Plan V12 — standalone-asset registration

Date: 19 October 2026

Status: reversible geometry-only review draft; unpromoted and unwired

Review route: `/keeper-review/kitchen-layout-plan-v12/`

V12 places the exact approved Kitchen Cabinet Run V11 twice in the established
772 × 224 room before any new appliance artwork is commissioned. “Standalone”
means an independently replaceable sprite. It does not imply another 84-pixel
room bay or require an appliance edge to continue the worktop exactly.

The preserved layout is:

- fridge bounds `x=84–168, y=140–218`;
- approved cabinet run A `x=168–336, y=134–208`;
- oven/hob bounds `x=336–420, y=131–208`;
- approved cabinet run B `x=420–588, y=134–208`;
- independent sink overlay registered to the final cabinet bay;
- table/chair bounds `x=680–764, y=148–222`.

The fridge top is therefore six pixels below the cabinet top and the oven/hob
top three pixels above it. These small offsets are intentional and visible in
the proof. Appliance sprites must remain inside their own exact envelopes, but
they do not inherit cabinet or countertop pixels.

The six Keeper stop/turn anchors remain `[126,218]`, `[210,218]`, `[294,218]`,
`[378,218]`, `[462,218]` and `[546,218]`. Upgrade art may change within a slot
without moving these route anchors.

The page contains no proposed appliance, sink or table art. Its outlined forms
are measurements only. Nothing changes Final or runtime.
