# Keeper Prime orthographic views V2 — image-generation prompt log

Generated on 13 October 2026 with the built-in OpenAI image-generation tool.
The output is a reversible source for a review draft, not production art.

## Exact-silhouette rear source

`sources/keeper-prime-back-exact-silhouette-generated.png`

The permanently approved Prime Master front was supplied as the geometry and
outer-body-shape authority. The selected V1 full-rear-hair back was supplied as
the edit target and rear-detail authority.

The prompt requested a true 180° rear elevation with the same adult, gently
rotund proportions, scale, head position, shoulder/torso/hip widths, arm fall,
leg stance, boot spread, cap and floor contact as the front. It required full
cream rear hair (explicitly hair, not beard), no facial features, one pale band,
smooth Prime rendering, transparency and no perspective, second stripe, shadow,
text or watermark.

Generation was not trusted to provide exact geometry. The V2 builder normalizes
the result, fits its rear RGB detail row by row and then copies the approved
front alpha channel exactly. The verifier rejects even one differing alpha
value among the 81,920 pixels.
