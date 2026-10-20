# Claude household cleaning-cupboard pack V1 prompt log

**Tool:** built-in image generation, 20–21 October 2026.

The accepted outputs used the existing Kitchen-condiments and BBQ-tools contact
sheets as style-only references unless the prompt entry says “fresh sprite
render”. The pack records each original generated PNG cache filename, SHA-256
and geometry, proportionally fits visible alpha inside a 384 × 384 transparent
canvas, and stores that review source as lossless WebP. Final 256 × 256 PNG
normalization is deterministic.

The main accepted-generation specification was:

> Use case: stylized-concept. Asset type: independently controllable 2D Lighthouse Keeper household-cleaning activity-callout prop. Input images: style references only; do not copy or combine their subjects. Style/medium: polished friendly hand-drawn game illustration matching the references, bold deep-navy outer contour, warm saturated colour, restrained painterly texture and dimensional highlights. Scene/backdrop: genuinely transparent background. Composition/framing: exactly one complete isolated object centered in a compact three-quarter view with generous transparent safety gutter on every side; nothing touches or crosses the canvas edge. Lighting/mood: cheerful, practical and immediately readable at small size. Constraints: actual alpha transparency; one independently owned prop; generic domestic packaging; no dangerous-use depiction; no spill; no cast shadow patch; no glow field; no shelf; no floor; no text; no letters; no numbers; no logo; no brand; no watermark; no frame; no checkerboard; no background; no unrelated extra objects.

The accepted primary requests were:

1. **Bleach:** sturdy opaque warm-cream bottle, integrated handle, short angled neck, navy child-resistant cap, orange accent and blank sparkle label.
2. **Disinfectant:** squat deep-navy bottle, orange cap, curved shoulders, grippy sides and blank shield-and-sparkle label.
3. **Multi-surface spray:** translucent aqua bottle, pale liquid, navy trigger, orange collar and blank sparkle label.
4. **Glass spray:** transparent blue bottle and liquid, cream trigger, navy collar and blank window-sparkle label.
5. **Furniture polish:** warm yellow-orange aerosol can, navy cap/nozzle and blank polished-wood pictogram.
6. **Washing-up liquid:** translucent emerald squeeze bottle, orange flip cap and blank plate-and-bubbles pictogram.
7. **Washing powder:** open aqua-and-cream cardboard box of powder with its blue scoop tucked inside, treated as one semantic group.
8. **Liquid laundry detergent:** teal handled bottle, orange measuring cap and blank shirt-and-bubbles pictogram.
9. **Fabric conditioner:** curved lavender handled bottle, navy measuring cap and blank towel-and-flower pictogram.
10. **Stain remover:** squat cream tub, orange lid and blank shirt-and-sparkle pictogram.
11. **Dishwasher tablets:** open navy tub with orange lid and visible tablets, treated as one semantic group.
12. **Dishwasher salt:** tall cream carton, navy top, orange pour spout and blank crystal-and-rack pictogram.
13. **Rinse aid:** slim translucent sky-blue squeeze bottle, orange dispensing cap and blank glass-and-sparkle pictogram.
14. **Toilet cleaner:** deep-aqua bottle with clearly curved neck, orange child-resistant cap and blank toilet-sparkle pictogram.
15. **Dustpan:** empty warm-orange plastic pan with navy rubber lip and short integrated handle; no brush or debris.
16. **Hand brush:** warm-cream wooden handle, navy grip and alternating teal/orange bristles; no dustpan or debris. Fresh sprite render.
17. **Broom:** complete diagonal wooden handle and wide orange/teal bristle head; no dustpan or debris.
18. **String mop:** complete diagonal navy handle, orange collar and clean cream cotton head; dry, with no bucket or puddle.
19. **Bucket:** empty deep-aqua bucket, orange swing handle, pouring lip and unnumbered molded ridges.
20. **Rubber gloves:** matched pair of long yellow gloves with orange cuffs as one semantic pair.
21. **Cellulose sponge:** standalone warm-yellow porous foam with rounded corners and waisted profile. Fresh sprite render.
22. **Scouring pad:** standalone thick dark-teal fibrous abrasive pad with rounded corners. Fresh sprite render.
23. **Microfiber cloth:** neatly folded sky-blue cloth with orange stitched edging and one turned corner. Fresh sprite render.
24. **Feather duster:** complete diagonal cream-and-navy handle with orange and teal synthetic feathers.
25. **Scrub brush:** arched warm-orange grip, deep-navy base and short dense teal bristles.
26. **Bin-bag roll:** black roll, short attached perforated tail, visible cream core and blank orange paper band.

Ten earlier attempts for the hand brush, sponge, scourer and cloth retained an
exterior ambient glow or colour field. Direct clean-alpha edits also retained
the field. They were rejected rather than silently promoted, and compact
lossless representations are kept under `evidence/rejected/`. The final four
accepted replacements used fresh prompts without style-image inputs:

> Create one isolated 2D game prop as a transparent PNG sprite. Friendly hand-drawn Lighthouse Keeper style: bold deep-navy contour, warm saturated colours, restrained painterly texture. There must be absolutely no pixel, colour, light, haze, shadow, halo, glow or aura outside the object's navy outline. Fully transparent alpha begins immediately outside that outline. Wide empty transparent margin to all four canvas edges. No background of any kind, no vignette, no spotlight, no floor, no cast shadow, no checkerboard, no frame, no text, no logo, no other object.

Low-alpha generation residue (alpha at or below 8) was removed during the
documented source-isolation pass. No accepted subject was manually redrawn.
