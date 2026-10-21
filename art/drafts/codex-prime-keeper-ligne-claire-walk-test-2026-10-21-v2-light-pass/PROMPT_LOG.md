# Prompt log

**Status:** FEASIBILITY TEST — NOT APPROVED PRODUCTION ART

The built-in image-generation tool was used for two visual-language studies.
Both studies are retained as provenance under `sources/generated-studies/` and
were rejected as geometry sources. The final V2 review assets were rebuilt
deterministically from approved Prime authority pixels with exact alpha and a
minimal blend: 28% palette consolidation for broad materials, 62% deep-navy
ink correction for existing dark drawing.

## Static side-right study

Use case: style-transfer  
Asset type: review-only character-art feasibility study  
Input images: Image 1 is the exact edit target and side-right dimensional
authority; Image 2 is the exact Prime Keeper face, identity, palette, and
front-view authority; Image 3 is the exact approved walk family and side-on
likeness reference.  
Primary request: redraw only Image 1's rendering treatment as polished classic
European ligne-claire comic illustration. This is the same Lighthouse Keeper,
not a redesign and not an existing copyrighted character.  
Style/medium: clean confident continuous deep-navy contours, tightly controlled
uniform line weight, flat well-separated colour areas, minimal restrained
interior fold lines, calm surfaces, no painterly rendering, no soft gradients,
no airbrushing, no texture, nearly no shading.  
Subject: retain the adult, slightly rotund Lighthouse Keeper; exact cap, badge,
white hair, stepped full beard, separate moustache, compact profile eye,
angular nose, broad single cream jumper band, blue jumper, navy trousers, and
navy boots.  
Geometry invariants: preserve the exact side-right pose and silhouette, body
construction, overall height and width, head and beard dimensions, head/body
ratio, shoulder/hip/hand/knee/boot positions, foot contact, floor baseline,
registration, and transparent 256×320 canvas. Do not change or reinterpret any
contour position. Preserve transparent background and safety gutter.  
Palette: retain the established bright/dark marine blues, warm cream beard and
stripe, warm skin, gold badge, deep navy outline; avoid pure black.  
Avoid: no Tintin hairstyle or costume, no Captain Haddock resemblance, no
caricature, no enlarged eye, no smile, no pose change, no scale change, no new
object, no shadow beneath feet, no text, no watermark.

Output retained as `sources/generated-studies/static-style-study.png`, SHA-256
`bb5bebd2c28f77b3dea452699761bc271aeb4ab29b4d9b8f3c6b8f511935aba3`.

## Eight-frame walk study

Use case: style-transfer  
Asset type: review-only eight-frame side-on walk sprite-sheet visual study  
Input images: Image 1 is the exact eight-frame Walk V6 motion, pose, frame
order, and geometry authority; Image 2 is the intended ligne-claire
rendering-language reference only.  
Primary request: deliberately redraw the complete visible Lighthouse Keeper in
all eight cells of Image 1 with one coherent classic European ligne-claire
treatment. Retain Image 1's exact contact, down, passing, up,
opposite-contact, opposite-down, opposite-passing, opposite-up poses and the
exact same character in every frame.  
Style/medium: clean continuous deep-navy contours, controlled consistent line
weight, flat separated colour shapes, almost no modelling, no gradients,
minimal intentional fold lines, calm clear surfaces, print-comic precision.  
Identity: the adult slightly rotund Prime Keeper; stable cap, badge, compact
rectangular profile eye, angular nose, stepped full beard, separate moustache,
white rear hair, single cream jumper band, blue jumper, navy trousers and
boots. Beard geometry, head size, torso volume, limb thickness, hands, knees
and boots must remain consistent across all frames.  
Geometry invariants: preserve all eight poses, silhouette extents, cell
registration, foot-contact positions, baseline, overall construction and
8-cell ordering from Image 1. No bounce, squash/stretch, perspective scaling,
smear, pose invention, crop, reflow, label, or background. Keep every character
isolated inside its cell with transparent gutters.  
Palette: established marine blues, cream white, warm skin, gold badge and deep
navy contour; avoid pure black.  
Avoid: no likeness drift, no line boil, no changing beard length/profile, no
eye enlargement, no grin, no extra or missing limbs, no new props, no text, no
watermark.

Output retained as `sources/generated-studies/walk-style-study.png`, SHA-256
`0783f169dd28c7c001724ee5aeba764d708f743b22bf2603ac3ba2ee975c80d6`.

## Final construction decision

The generated studies captured the intended graphic flattening but did not
hold exact silhouettes, canvases or registration. They were not cropped or
warped into production-like assets. `build.py` instead nudges the approved side
endpoint and every exact Walk V6 cell toward a named Keeper-specific palette
while copying each source alpha plane byte-for-byte. Broad materials retain
72% of their original RGB. This preserves the physical construction and tests
only the lightest useful finishing treatment.
