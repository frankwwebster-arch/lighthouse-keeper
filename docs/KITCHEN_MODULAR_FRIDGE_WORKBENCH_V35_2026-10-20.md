# Kitchen Modular Fridge Workbench V35

V35 supersedes rejected V34 as the active reversible fridge review gate. It
does not alter or promote Final/runtime assets.

## Construction

- Standard and Broken were drawn as one coordinated high-resolution family
  against approved Cabinet V11's storm-blue, pale turquoise, deep-navy and
  copper language.
- The logical appliance body is exactly `84 × 74 px`, installed at
  `y=134..208`, matching the approved rear-wall cabinetry datum.
- Each state occupies an isolated `144 × 90 px` transparent cell with body
  offset `(-30,-4)` and a deterministic transparent edge gutter.
- Standard has one white enamel door and one lower grille.
- Broken keeps the same carcass and worktop. The top hinge has failed; the
  door's bottom-right corner is visibly retained by the lower hinge and its
  lower-left corner reaches the floor. Contents and a shallow puddle remain
  static. Door/puddle overflow is limited to four pixels beyond the logical
  bay, preventing meaningful neighbour occlusion.
- The low electrical buzz is sound-only. The inherited effect-only drip/ripple
  remains removable and variable-speed in a new isolated 40-frame, 4-fps,
  ten-second strip.

## Placement and joins

V35 preserves approved V33 snapping. Fridge, sink and oven occupy three
distinct origins from `[84,336,420,504]`; loose dragging is preview-only and
release commits the nearest free exact origin. The Prime stop/turn target is
always the selected asset's logical midpoint `x+42,y=218`.

Join precedence is deterministic:

1. Any pair containing the oven uses the approved V32 triangular resolver.
2. Every other exact adjacency—including fridge↔cabinet and fridge↔sink in
   either order—uses the approved six-pixel blue V22 body backfill plus the
   exact sixteen-pixel V22 countertop cap.
3. An exposed sink left side uses the approved V25 cutout/rounded end.
4. An exposed fridge or oven keeps its own finished end.

The worktop repair is a dynamic compositor layer, embedded in no appliance,
and therefore follows the fridge wherever it snaps.

## Review and verification

- Review route: `/keeper-review/kitchen-modular-fridge-workbench-v35/`
- Builder: `scripts/build_kitchen_modular_fridge_workbench_v35.mjs`
- Native-state builder: `scripts/build_kitchen_modular_fridge_assets_v35.py`
- Verifier: `npm run verify:kitchen-modular-fridge-workbench-v35`

The verifier checks all 24 legal three-appliance layouts, exact body/cell
geometry, the four-pixel broken-state overflow ceiling, per-frame effect
gutters, archive hashes, V33 byte identity and the universal non-oven V22 join.
