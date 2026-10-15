# Keeper Prime stair ascent V6 prompt and decision log

Mode: built-in image generation followed by deterministic contact-sheet splitting, bilinear down-registration, upper-body locking and exact horizontal mirroring.

Authorities:

- `art/drafts/keeper-prime-side-right-rigged-2026-10-13-v1/drafts/keeper_prime_master-neutral-standing-side-right_f1.png`
- `guides/left-leg-step-guide-v6.png`
- `guides/right-leg-step-guide-v6.png`

The first two generated contact sheets are preserved as:

- `sources/generated/left-leg-six-pose.png`
- `sources/generated/right-leg-six-pose.png`

Pixel contact checks found that both first sheets missed the binding one-tread
plant datum: the first right-leg pass ignored it more broadly, while the first
left-leg F4 was eleven registered pixels too low. Both remain rejected
provenance. Their corrected sheets are preserved separately as
`sources/generated/right-leg-six-pose-corrected.png` and
`sources/generated/left-leg-six-pose-corrected.png`.

The corrected left sheet still returned F4 to a near-level floor when measured
after registration, so it also remains intermediate provenance. The binding
left contact pose was therefore generated alone and is preserved as
`sources/generated/left-leg-pose04-contact-corrected.png`.

## Left-leg prompt

> Use case: precise-object-edit. Asset type: six-frame transparent sprite animation contact sheet for Lighthouse Keeper game. Input images: Image 1 is the exact Keeper Prime side-right identity, scale, palette, line quality, clothing and rendering authority. Image 2 is the exact six-pose geometric guide, ordered top-left to top-right then bottom-left to bottom-right; red is the LEFT/near moving leg and cyan is the planted support leg. Primary request: create six complete, polished Keeper Prime side-right sprites, one for each guide pose. The LEFT/near leg alone performs one stair step onto the immediately adjacent tread. The support leg stays planted through poses 1-4; poses 5-6 show a believable weight transfer onto the newly planted left foot and the other foot beginning toe-off. Composition: exact 3-column by 2-row contact sheet, generous transparent gutter around every complete character, identical character scale and identical head/torso anchor in every cell. Style: match Image 1 exactly—smooth high-resolution cartoon rendering, same adult proportions, same cap, beard, face, blue single-stripe jumper, trousers and boots. Constraints: transparent background; six characters only; no stairs, guide lines, labels, text, grid, shadows or props. Keep head, face, beard, cap, torso, clothing colours and arm pose identical across all six. Change only hips/legs as required by Image 2. Each foot travels to one adjacent tread only, never two. Pose 3 high pass should clear the next tread narrowly, not kick high. Boots must remain anatomically connected and never cross through an imaginary tread. Do not change body width or height. No childlike proportions, no eye glints, no grin, no pixelated edges.

## First right-leg prompt

The left-leg prompt was repeated with cyan defined as the RIGHT/far moving leg, red as the planted support leg, and the corresponding anatomical wording changed. That result is preserved but rejected.

## Corrected left-leg prompt

> Use case: precise-object-edit. Asset type: corrected six-frame transparent sprite animation contact sheet for Lighthouse Keeper. Image 1 is the exact Keeper Prime side-right identity, palette, clothing and smooth rendering authority. Image 2 is the binding six-pose geometry guide. Image 3 is the current left-leg six-pose render: preserve its upper body and overall finish, but correct the lower-body geometry wherever it conflicts with Image 2. Return exactly one 3-column by 2-row contact sheet in the same pose order as Image 2. The LEFT/NEAR leg (red in Image 2) alone takes one stair. The RIGHT/FAR leg (cyan in Image 2) stays planted on the lower tread in poses 1–4. In poses 3, 4 and 5, the sole of the moving left/near boot must be visibly and exactly ONE full tread higher than the planted support boot—never level with it and never two treads higher. Pose 4 is the binding contact pose: the support boot sole must sit on the lower horizontal line and the moving left/near boot sole must be flat on the immediately adjacent upper horizontal line, with a clear vertical separation matching Image 2. The present Image 3 pose 4 is too low; raise that moving boot to the upper line. Pose 5 transfers weight forward while retaining the one-tread separation. Pose 6 has the moving left/near boot planted as the new support and the trailing right/far boot beginning toe-off. Preserve identical head, cap, face, beard, torso, jumper, arms, scale, colours and smooth edges in all six cells. Transparent background, generous gutters, no stairs, lines, labels, grid, text, shadows or props in the output. Adult proportions, solid rectangular eye, no eye glint, no grin. Do not swap which leg moves. Do not put both boots on the same level in poses 3–5.

## Corrected right-leg prompt

> Use case: precise-object-edit. Asset type: corrected six-frame transparent sprite animation contact sheet for Lighthouse Keeper. Image 1 is the exact Keeper Prime side-right identity, palette, clothing and smooth rendering authority. Image 2 is the binding six-pose geometry guide. Image 3 is the current right-leg six-pose render: preserve its upper body and overall finish, but correct the lower-body geometry wherever it conflicts with Image 2. Return exactly one 3-column by 2-row contact sheet in the same pose order as Image 2. The RIGHT/FAR leg (cyan in Image 2) alone takes one stair. The LEFT/NEAR leg (red in Image 2) stays planted on the lower tread in poses 1–4. In poses 3, 4 and 5, the sole of the moving right/far boot must be visibly and exactly ONE tread higher than the planted support boot—never level with it and never two treads higher. Pose 4 is the clearest requirement: lower support boot sole on the lower horizontal line; moving boot sole flat on the immediately adjacent upper horizontal line. Pose 5 transfers weight forward while retaining the one-tread separation. Pose 6 has the moving right/far boot planted as the new support and the trailing left/near boot beginning toe-off. Preserve identical head, cap, face, beard, torso, jumper, arms, scale, colours and smooth edges in all six cells. Transparent background, generous gutters, no stairs, lines, labels, grid, text, shadows or props in the output. Adult proportions, solid rectangular eye, no eye glint, no grin. Do not swap which leg moves. Do not put both boots on the same level in poses 3–5.

## Binding single left-contact prompt

> Use case: precise-object-edit. Create ONE complete transparent Keeper Prime sprite for stair contact pose 4 only. Do not create a contact sheet. Image 1 is the exact side-right identity, palette, clothing and smooth rendering authority. Image 2 is the binding pose-4 geometry: red LEFT/NEAR leg is the moving leg, cyan RIGHT/FAR leg is the support. Image 3 supplies the current consistent rendering style. The far/support boot sole must be flat on an imaginary lower tread. The near/moving boot sole must be flat on the immediately adjacent imaginary upper tread, with the full vertical separation shown in Image 2. This is a planted upper contact, not a kick: bend the knee naturally and make the whole moving boot horizontal. The moving boot must not descend toward the lower support level. One stair only. Preserve the exact head, cap, adult face, beard, torso, single-stripe jumper, arm, hand, colours and smooth linework. Transparent background and generous gutter. No stairs, floor, lines, guide colours, labels, text, grid, shadow or props. One character only, full body, side-right, same scale. Solid rectangular eye, no glint, no grin.

## Deterministic registration

Every output is a 256×320 transparent cell with alpha bounds y31–316. The upper body is byte-identical through y212 and feathered to the independently authored legs through y220. The game-facing leftward frames are exact horizontal mirrors of the right-facing authoring cells. No approved, Final or production art is changed.

The isolated left F4 render cleared the tread but registered 12 pixels too high.
Its moving lower leg is therefore warped downward deterministically: zero shift
at y220, increasing linearly to 12 pixels at y260 and below. This puts the flat
sole within the one-riser contact band without changing any upper-body pixel.
