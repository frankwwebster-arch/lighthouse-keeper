# Image-generation provenance

Tool: OpenAI built-in `image_gen` image editing, 24 October 2026.

## Broken bowl correction source

Prompt: “Edit only the broken mixing bowl near the lower-right centre of this
Kitchen V4 source sheet. Remove the whisk and every artefact to the bowl’s
right. Make the bowl visibly more broken with a larger jagged missing section
through the upper-right rim and side, deeper cracks, and two detached ceramic
shards below and to the left. Preserve the warm ligne-claire style, colours,
lighting, line weight, white paper background, 1536 × 1024 canvas, and all
other artwork exactly.”

Generated source SHA-256:
`799837c86163cbbdeed3a377dfd52ecff28838f50c24980527b168abd356effe`.
Only the declared broken-bowl crop is used.

## Rear-chair correction source

Prompt: “Edit only the small chair at the far lower right. Replace it with a
rear-facing wooden kitchen chair—the back of the chair faces the viewer, for a
Keeper seated facing the back of the room. Preserve the warm ligne-claire
style, orange-brown wood, dark navy outline, lighting, white paper background,
1536 × 1024 canvas, and all other artwork exactly.”

Generated source SHA-256:
`c91b6197f016fff31bb1a884812e0dd236c0b7e1e921061aebef858fa8f605a3`.
Only the declared chair crop is used before native-pixel straight-run extension
to the approved geometry. Two isolated-chair sizing experiments were rejected
and are not copied into the repository or used by V3.
