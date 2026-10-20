# Kitchen Dishwasher Workbench V39

Date: 20 October 2026

Status: rejected and superseded by V40; immutable, unpromoted and unwired.

Review: `/keeper-review/kitchen-dishwasher-workbench-v39/`

Frank rejected V39 because its generated countertop outline was too heavy and
appeared one native row too high beside Cabinet V11. The exact rejection is
pinned in
`docs/review/kitchen-dishwasher-workbench-v39-rejection-2026-10-20.json`.
V40 corrects only the worktop and preserves V39 as historical evidence.

## Appliance family

V39 adds one standalone `84 × 74 px` dishwasher using the approved modular
kitchen geometry. It has a shallow cabinet-matched turquoise top, restrained
navy rails and a clearly silver/stainless front.

- **Off:** closed door, dark display and lamp.
- **On:** the identical closed silhouette with aqua LCD-style glyphs and one
  solid green lamp.
- **Broken:** the same carcass and door dimensions. The door still opens toward
  the camera on its bottom hinge, but the lower-right hinge has failed. The
  surviving lower-left hinge leaves the door conspicuously twisted and
  skew-whiff; the handle bends, the fascia is cracked and a red error lamp is
  visible.

All three states use a `98 × 82 px` transparent cell with offset `(-7,-4)` and
a four-pixel safety gutter. The logical body and Prime anchor remain one exact
bay regardless of visible Broken-state detail.

## Reusable suds

Soap suds are not baked into the appliance. V39 adds compact, regular and
emphatic effect-only models to the animation library. Each is a `40`-frame,
`4 fps`, ten-second transparent strip in `112 × 104 px` cells. The review
starts with one regular layer drafted across the open door and as a broad
soapy puddle spanning beyond the dishwasher bay on the floor, while
also allowing the user to:

- drag the library card onto another preferred point;
- add multiple suds layers;
- choose a model;
- move relative to the dishwasher;
- resize, crop and vary speed from `0.1×` to `4×`;
- remove any layer.

Named placeholders are `kitchen_dishwasher_running_low_loop`,
`kitchen_dishwasher_broken_rattle_loop` and
`kitchen_dishwasher_suds_bubble_loop`.

## Movement and healing

V39 carries V38 forward unchanged and adds the dishwasher as a sixth movable
one-bay object. Because all six canonical origins are occupied, dropping an
object on another swaps the two; no free pointer coordinate persists. Every
swap keeps the Prime interaction point at the snapped footprint midpoint.

The dishwasher uses its native finished ends when exposed, V22 flat healing
with ordinary fitted neighbours and V32 triangular healing beside the oven.
The body never embeds a neighbour. All `6! = 720` arrangements are verified.

The governing method is
`docs/KITCHEN_MODULAR_ASSET_AND_JOIN_STANDARD_2026-10-20.md`.

## Provenance and boundary

The two high-resolution built-in image-generation outputs are retained under
`art/source/kitchen-dishwasher-workbench-2026-10-20-v39/generated/`. The V39
builder deterministically normalises them into the state cells and isolated
suds strips; generated source art is never served directly.

V38, approved Cabinet V11, existing appliance sources, Final and runtime are
unchanged. Kettle, toaster and mixing bowl remain unstarted.

Verify with:

```sh
npm run verify:kitchen-dishwasher-workbench-v39
npm run build
```
