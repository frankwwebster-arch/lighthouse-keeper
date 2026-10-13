# Prompt and construction log

Frank identified pale patches above the Frame 8 boots and a remaining boot mismatch. Two built-in image-editing explorations were made against the smooth rear master and V4 silhouette, but both were rejected internally because they changed the boot design more widely than necessary. Neither generated image is used in V7.

The shipped candidate is deterministic: the approved smooth rear source is widened only below source row 1068, easing to five percent by row 1120 with Lanczos filtering. The normalized trouser and boot masks use disjoint ranges `[202,254)` and `[254,317)`, correcting the V6 four-row overlap `[250,254)` that created the pale bars.
