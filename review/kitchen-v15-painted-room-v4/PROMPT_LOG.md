# Kitchen v15 painted-room v4 — image-generation record

Tool: OpenAI built-in image generator (`image_gen`), not the CLI/API fallback.

## 1. v15 room-wide layout edit

Input 1 was the unchanged liked 2172 × 724 kitchen and sole style authority.
Input 2 was `kitchen_v15_schematic_1x.png`, explicitly geometry-only. The prompt
kept the shell, brighter duck-egg palette, joinery, beams, doors, floor, windows
and props; removed the larder; requested three joined B cupboards with one
continuous worktop; moved the dresser to the far right; placed toaster left and
mixer right on its counter; prohibited redesign, new objects and shadows; and
listed every v15 x/y datum.

Selected result:
`sources/imagegen/kitchen-v15-painted-master.png`

## 2. Empty-shell subtraction companion

The v15 painted master was the edit target. The prompt removed only furniture,
appliances, worktops, cupboards and kitchen props while keeping the complete
beamed shell, both side doors, floor, walls and magenta windows. This companion
is used only for assembly/masking and is not replacement room art.

Selected result:
`sources/imagegen/kitchen-v15-empty-shell-companion.png`

## 3. Clear-counter dresser derivative

The v15 painted master was the authority. The prompt isolated the same far-right
duck-egg dresser on true transparency, preserved its shelves, crockery, pine
counter and hardware, removed only the baked-in toaster and mixer, and required
the v15 width:height proportion. This lets toaster and mixer remain separate
stop-centred cuts.

Selected result:
`sources/imagegen/dresser-clear-counter-transparent.png`

All generated inputs, roles, canvas sizes and SHA-256 values are pinned in
`manifest.json`. The original liked source remains separate and byte-identical.
