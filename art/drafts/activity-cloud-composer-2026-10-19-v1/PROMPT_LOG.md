# Activity Cloud Composer V1 image-generation log

**Tool:** built-in image generation, 19 October 2026.

## Selected source

`source/bbq-expansion-generated-v1.png` was copied from:

`/Users/frank/.codex/generated_images/01a154f0-ac07-7f81-94e1-95c7e71e3d54/exec-300f2956-1a1a-418d-8118-efb4fd781a3f.png`

Image 1 (`exec-64c2d63c-2fd6-44de-a37f-a61ec482c8ca.png`) was
used as a **style reference only**, not as an edit target or pixel authority.

## Final prompt

> Use case: stylized-concept. Asset type: transparent game
> activity-callout component source sheet. Create five new BBQ objects matching
> the polished Lighthouse Keeper game design language: browned British-style
> sausages, finished hot dogs, grilled burgers, unbranded ketchup bottle and
> dollop, and a charcoal bag with loose briquettes. Use a 1536 × 1024 three-by-two
> sheet, leave the sixth cell empty, keep strong reduced-size silhouettes, use
> deep navy contours with warm cream, storm blue, sea-glass, copper and restrained
> gold/orange accents, and include no Keeper, people, animals, gore, furniture,
> counter, BBQ appliance, text, brands, UI or shared background. Keep every object
> inside its own ownership cell with transparent separation.

The generated sheet supplied genuine alpha and a completely empty sixth cell.
Its nominal x=512 divider was not clear because a few antialiased plate pixels
extended beyond it, so the deterministic builder selected the first completely
transparent separator at x=520. The second divider is x=1028 and the horizontal
divider is y=512. All three selected boundaries contain zero alpha. No source
pixels were hidden with a tighter crop.

## Deterministic post-processing

`scripts/build_activity_cloud_composer_v1.py` thresholds source alpha only at
8, crops the five disjoint declared ownership cells, trims each owned object,
registers it proportionally into a 256 × 256 transparent cell and rejects any
result with edge alpha or less than a 16-pixel gutter. No generative or manual
paint operation follows source selection.
