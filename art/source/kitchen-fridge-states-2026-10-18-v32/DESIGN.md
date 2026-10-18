# Kitchen V32 fridge construction

V32 is a reversible review draft for the fridge only. It does not promote or
wire any art into Final or runtime.

- Standard and broken states come from one coordinated generated source sheet.
- Both use one 120 × 96-pixel transparent review/runtime candidate cell.
- The fitted body retains the 21-lp / 84-pixel bay alignment at density 4.
- The shared source windows reduce to 116 × 80 px inside that cell so the
  sea-glass cap meets the approved V23 worktop and the foot line stays fixed.
- The broken top hinge is detached; the lower-right hinge remains attached.
- The fallen door's lower-left corner rests on the floor.
- Sparse unlabelled milk, jar and produce silhouettes make the open cavity read
  as a used fridge rather than an empty box.
- The door and leaked pool are static object pixels.
- A separate reusable 120 × 96-pixel strip contains only the falling drip and
  restrained pool ripple.
- The environmental strip has 40 isolated frames at 4 fps: one seamless,
  sedate ten-second loop.
- `kitchen_fridge_low_electrical_buzz_loop` is the required named SFX
  placeholder. There are no visible electrical effects.

The deterministic build is `scripts/build_kitchen_fridge_states_v32.py`. V1 is
the initial coordinated source, V2 is the contents revision, and V3 is the
selected one-change floor-contact correction.
