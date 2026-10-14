# Keeper Prime Walk V4 — image-generation prompt log

Mode: built-in image generation, precise-object-edit. All outputs requested a genuinely transparent background and smooth antialiased edges. Each frame used its Walk V3 frame as the edit target and preserved the approved head, face, cap, beard, torso, near/front arm, legs, boots, palette, scale, floor anchor and transparent gutter.

## Selected prompts

- **F2 — halfway arm:** Change only the screen-left rear arm. Put it clearly halfway between the preceding F1 rearward pose and the following F3 vertical passing pose: less backward than F1, more backward than F3, attached at the same shoulder and behind the torso.
- **F3 — passing arm:** Change only the screen-left rear arm to a distinct vertical passing position: upper arm nearly straight down, slight elbow bend, cuff below the jumper hem and hand beneath the rear shoulder near the rear hip.
- **F5 — reappearing arm:** Keep the rear upper arm behind the torso, with only a short lower sleeve/cuff and a small part of the hand beginning to reappear low at the left/back jumper edge near the hip.
- **F6 — passing on return:** Continue the rear arm's return into a clear vertical passing pose, with the full hand visible beneath and slightly behind the rear shoulder. Make it more exposed than F5.
- **F7 — rearward arm:** Continue from passing into a clear backward swing. Move the elbow and cuff leftward behind the torso, with the hand visibly farther left and slightly higher than the hip, but short of the loop's maximum.

Common avoid list: redesign; camera or scale change; crop; blur; pixelation; extra or detached limbs; moving the front arm; changing legs, face or colours; background; shadow.

## Rejected iteration

- `sources/rejected-f2-maximum-rearward.png`: the first F2 attempt moved the arm farther back than F1, creating a second rearward maximum rather than a transition toward F3.
- `sources/rejected-f4-shoulder-loop.png`: the first F4 attempt left a circular sleeve/shoulder loop rather than a cleanly occluded rear arm.
- `sources/rejected-f4-full-occlusion-model-shift.png`: the clean occlusion pass required a full-frame redraw and produced an unacceptable body-model shift, so V4 retains exact Walk V3 F4 instead.

## Deterministic post-processing

F2, F3 and F5–F7 are uniformly scaled from significant-alpha height, aligned to the existing floor and horizontally registered by the cap badge, then composited only through frame-specific rear-arm masks. This retains every V3 pixel outside those masks. F1, F4 and F8 remain byte-identical to Walk V3.
