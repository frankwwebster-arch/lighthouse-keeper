# Kitchen room flat-cutaway construction recipe

**Authority:** Frank's straight-on doll's-house direction, 16 October 2026

**Machine record:** `data/kitchen_room_flat_cutaway_recipe.json`

**Builder:** `scripts/build_kitchen_room_flat_cutaway_v7.py`

Use this recipe for kitchen rooms and as the starting architecture recipe for
later standard rooms. It defines projection and construction only; it does not
approve the V7 drawing or promote it into the game.

## Coordinate system

- Author at 4 source pixels per logical pixel (`lp`).
- Measure x from the left edge and y from the top edge. Boxes are half-open:
  `[left, top, right, bottom)`.
- Room height is exactly 56 lp; the Keeper support/foot line is y = 56 lp.
- One furniture bay is exactly 21 lp. Width for `n` bays is exactly
  `4 + 21n` lp, giving 193 lp at nine bays and 256 lp at twelve.
- The Keeper, furniture and architecture remain at scale 1 everywhere. There
  is no runtime depth scaling or alternate rear-wall scale.

## Projection

Draw the back-wall elevation first. Every structural vertical is vertical and
every corresponding horizontal is horizontal and parallel. Horizontal and
vertical convergence are both exactly 0 lp; there is no vanishing point.

Depth may be conveyed only by categorical layer order, parallel value bands,
small contact shadows and the already selected shallow Option B furniture
tops. Do not taper posts, narrow rear edges, angle floorboards, introduce a
stage lip or make V-shaped module joints.

## Exact horizontal zones

| Zone | Top | Height | Bottom |
| --- | ---: | ---: | ---: |
| ceiling beam | 0 lp | 5 lp | 5 lp |
| wall field | 5 lp | 44.5 lp | 49.5 lp |
| skirting | 49.5 lp | 1.5 lp | 51 lp |
| floor band | 51 lp | 5 lp | 56 lp |

These boundaries are invariant at every supported width. Timber grain and
floor detail may be horizontal; a vertical plank joint is permissible, but no
line used as a depth cue may be diagonal or convergent.

## Modular construction

### Stair-side cap

- Cell: 46 × 56 lp.
- The review source retains the flat ladder inside x = 8–24 lp and y = 5–49
  lp, with rung centres at y = 8, 14, 20, 26, 32, 38 and 44 lp.
- The kitchen assembly uses only `[42, 0, 46, 56)`: the rightmost 4 lp.
- Therefore the cap contributes exactly 4 lp to room width and never changes
  the bay lattice.

### Repeat module

- Cell and contribution: exactly 21 × 56 lp.
- Three plaster-texture variants are permitted, selected cyclically.
- Texture stays at least 2 lp from either module edge.
- The left and right edge columns must be pixel-identical at every y for every
  variant. A join is an ownership boundary, not a visible groove.
- Repeat modules are copied whole. Never stretch, crop or distribute a width
  remainder among them.

### Far cap

- Cell: 38 × 56 lp; contribution to room width: 0 lp.
- Place it as a right-aligned overlay on the already assembled repeats.
- The right side-wall strip is `[34, 0, 38, 56)` and the cupboard hinge is
  x = 37 lp in this local cell.
- With the cupboard closed, no frontal door leaf is visible. When open, the
  exact rectangular V6 leaf rotates into the foreground around the fixed
  hinge; the room itself does not acquire perspective.

## Sink-owned porthole

The porthole is not baked into a room repeat. It is a separate wall child of
`obj_sink`, allowing the complete sink group to move between bays.

| Datum | Exact value |
| --- | ---: |
| child cell | 21 × 56 lp |
| local anchor | (10.5, 56) lp |
| centre from cell top | (10.5, 18.5) lp |
| centre above floor | 37.5 lp |
| outer diameter | 15 lp |
| glazing diameter | 11 lp |
| nominal brass band | 1.5 lp |
| outer outline | 0.5 lp |
| bolt count | 8 |
| bolt-circle radius | 6 lp |
| side safety gutter | 3 lp each side |
| layer | z 25, behind sink z 40 |

The child uses the same bay origin as the sink. For every move,
`childDeltaLp == parentDeltaLp`; both scales remain 1 and the child has only a
standard state. The porthole may show a decorative sea/sky view, but its
structural ring remains a flat wall-mounted circle with no projected side.

## Deterministic checks

Verify all seven 6–12-bay shells, exact zone rows, identical repeat edges,
unaltered module dimensions, 5-lp floor band, 4-lp stair contribution and
right-aligned far overlay. Verify the porthole's 15 × 15-lp alpha bound, 3-lp
side gutters, centre and parent ownership. Place the sink group in at least
three bays and require equal parent/child translations.

Hash-protect Kitchen V6 furniture, Keeper sources, runtime sprites, Final and
manifests. Publish each revision under a fresh immutable review path, preload
and decode all referenced images before enabling controls, and keep approval
separate from promotion.
