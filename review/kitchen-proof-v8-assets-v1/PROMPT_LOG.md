# Kitchen v8 Day-1 assets — image-generation record

Tool: OpenAI built-in image-generation/edit tool.

Modes: `stylized-concept` for isolated object masters and
`precise-object-edit` for proportion, open-interior, removable-door and burnt
contents corrections. All outputs remain candidates in this review folder.

## Shared visual contract

> Draw one isolated British cottage kitchen object in the approved rich,
> friendly hand-painted ligne-claire family established by the v8 Belfast
> sink, dresser and corrected old-school cooker. Use confident navy/near-black
> outlines, warm cream enamel, restrained duck-egg/sage painted wood, honey
> pine and copper/orange accents. Straight-on orthographic game-asset view with
> only the shallow reveal necessary to read the object. Preserve the supplied
> exact game-boundary guide, genuine transparent alpha and generous safety
> gutter. No room, floor, wall, character, text, logo, external cast shadow,
> pink or magenta.

## Selected visible-object sources

| Source | Final prompt subject |
|---|---|
| `sources/selected/cream_larder_fridge.png` | broad one-unit rounded cream larder fridge, copper handle, one dark status bezel |
| `sources/selected/painted_base_cupboard.png` | one-unit framed duck-egg/sage cupboard, honey-pine worktop, copper knobs |
| `sources/selected/scrubbed_pine_table.png` | sturdy two-unit scrubbed-pine cottage table, readable apron and legs |
| `sources/selected/wooden_chair_side.png` | simple sturdy honey-pine kitchen chair in exact side view |
| `sources/selected/enamel_pedal_bin.png` | compact cream enamel pedal bin with navy base and one copper accent |
| `sources/selected/enamel_electric_kettle.png` | cream enamel electric kettle, dark handle, copper joints, one status bezel |
| `sources/selected/cream_toaster.png` | compact cream two-slot toaster, copper control, one status bezel |
| `sources/selected/stand_mixer.png` | compact duck-egg stand mixer with cream bowl, copper control and one bezel |
| `sources/selected/painted_wall_cupboard.png` | one-unit framed painted wall cupboard with restrained copper knobs |

The Belfast sink, painted dresser and corrected cooker are copied byte-for-byte
from `review/kitchen-proof-v8-style-test-v2/`; they were not regenerated.

## Technical-layer final prompts

### Fridge fixed body

> Derive only the fixed body of the same cream larder fridge, with its outer
> casing, cap, plinth and a complete open refrigerated interior: rear/side
> walls, shelves, lower drawer and a restrained handful of readable food. Do
> not draw the door. Preserve the v8 palette, outline character, straight-on
> view and transparent background.

Selected source: `sources/layers/fridge_body_open.png`.

### Fridge door

> Derive only the complete removable cream refrigerator door from the same
> master, including rounded cream face and copper handle. No body, shelves,
> food, room or floor. Straight-on isolated transparent sprite, suitable for a
> right-side hinge.

Selected source: `sources/layers/fridge_door.png`.

### Cooker fixed body

> Create only the fixed body of the same corrected old-school British cream
> gas cooker. Preserve its exact silhouette, eye-level hood/grill, four
> burners, exactly four copper controls and one dark status bezel. Remove the
> lower oven door entirely and show a complete integrated cavity with side
> walls, runners, shelf, rear wall, base and warm interior-light zone. No food,
> separate parts or background.

Selected source: `sources/layers/cooker_body_open.png`.

### Cooker door

> Create only the removable lower oven door: cream rounded frame, wide copper
> handle and dark smoked-glass window, matching the corrected cooker. No body,
> hob, controls, grill, food or background. The complete part must be isolated
> for a bottom hinge. The deterministic build converts the glass region to
> genuine partial alpha.

Selected source: `sources/layers/cooker_door.png`.

### Oven contents

> Draw a small separate cream enamel roasting dish containing a golden-brown
> cottage pie with a gently ridged toasted potato top, in the same v8
> ligne-claire family. No cooker, shelf, smoke, fire or background.

Selected source: `sources/layers/cottage_pie_cooking.png`.

> Edit only the food surface of that same dish to a visibly overcooked state:
> dark brown to nearly black scorched patches and cracked charred ridges.
> Preserve the dish, silhouette, viewpoint, scale and transparent canvas. Add
> no smoke, flame or external soot.

Selected source: `sources/layers/cottage_pie_burnt.png`.

Status-on lamps, mirrored-chair orientation, registered compositions and all
scale sheets are produced deterministically by `build_assets.py`, not by image
generation. No Keeper artwork was generated.
