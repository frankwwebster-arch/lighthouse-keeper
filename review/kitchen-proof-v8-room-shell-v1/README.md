# Kitchen v8 UK Cottage — room shell v1

This versioned review candidate builds the empty Kitchen v8 shell around the
completed Day-1 object set. It does not promote the room to runtime or canon.

## Review outputs

- `outputs/kitchen-v8-room-shell-empty-1x.png` — exact 2048 × 576 empty shell.
- `outputs/kitchen-v8-room-furnished-1x.png` — the existing v8 objects on their
  declared stops, plus the exact Prime Keeper in front at `walkY = 502`.
- `outputs/kitchen-v8-room-three-scale.png` — full-room 2× detail, exact 1:1,
  and exact 12.5% tower scale.

## Geometry and visual boundary

- The back wall is flat and front-on; the shallow side walls, ceiling beams and
  floor edges use one-point dolls'-house perspective.
- Both panelled doors sit at the **stage-front** outer edges of the side walls.
  Their near jambs reach the floor front, so neither reads as a back-wall door.
- The cream back wall spans x=290–1995, beyond the required x=360–1995 field.
- Back-wall/floor line is y=460; floor front is y=544; slab is y=544–576.
- Windows occupy the exact 168 × 168 envelopes x=622–790 and x=1294–1462,
  y=106–274. The sill is 1.11 m and the head 2.11 m above the back-wall floor
  line at 168 px/m. The sink meets the sill without covering it; the table and
  chairs remain below the right window.
- Glass is exact `#FF00FF`, applied after antialiasing so there is no fringe.

The shell uses the supplied favourite reference and a generated style concept
for visual direction. Production geometry and every review output are rebuilt
deterministically in `build_room_shell.mjs`; generated concept pixels are not
used in the shell.

## Preserved assets and deferral

All furnishings are composited directly from
`review/kitchen-proof-v8-assets-v1/outputs/` and hash-checked. The Prime Keeper
is inherited unchanged from the Kitchen v3 review authority. The Day-1 cooker
remains the existing 126 px unit. The future 252 px range stays reserved,
deferred and undrawn.

## Rebuild and verify

```sh
npm run build:kitchen-v8-room-shell
npm run verify:kitchen-v8-room-shell
```

`verify_room_shell.mjs` checks output and input hashes, exact module datums,
window dimensions and real-world heights, zero window occlusion, crisp magenta
ownership, both stage-front doors, unchanged inherited furniture and Prime
bytes, and the continued absence of the 252 px range.
