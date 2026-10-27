# Kitchen v14 verification report

- Source: approved v14 schematic and section 19 GO note.
- Scope: tier-1 review candidate only; no installed/runtime changes.
- Geometry: exact 2048 × 576 room; exact per-item canvases from the schematic.
- Standard module: 168 px / 1.0 m for every ordinary kitchen unit.
- Tall-item gate: fridge, cooker, dresser and larder all have height no greater
  than twice width.
- Shell: symmetric ordinary doors at the stage-front side walls; windows remain
  168 × 168 at y106–274 with exact `#FF00FF` panes.
- Layers: removable fridge, cooker and larder doors over complete interiors;
  separate cooking/burnt contents, oven-light and electrical status overlays.
- Deferred: the 252 px range is not drawn.

Run `verify_kitchen_v14.py` after every rebuild. Frank's visual verdict remains
the approval gate.
