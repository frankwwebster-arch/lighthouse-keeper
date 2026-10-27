# Image-generation prompt record

Built-in image generation was used for six style references before the final
deterministic v14 cut: a chunky cream fridge-freezer, a sage larder, a broad
painted wall cupboard, a Brown Betty teapot with two cups, a wall clock and a
game-day calendar. Each prompt requested transparent-background adult ligne
claire art matching the approved v8 cottage family: clean dark outlines, matt
flat fills, restrained internal detail, no cast shadow, no gloss, no watermark.

The generated files are preserved, unmodified, in `sources/imagegen/`. They are
style/proportion references only; the exact v14 canvases are redrawn
deterministically by `build_kitchen_v14.py` so geometry and state layering can
be verified pixel-for-pixel.
