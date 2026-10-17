# Prime Keeper back sit/stand V1 prompt log

Built-in image generation was used in `identity-preserve` edit mode on
18 October 2026. Four complete transparent sources were generated separately;
the exact standing-back and seated-back geometry sources were not generated.

Inputs for every call:

- edit target and width authority: exact registered Prime seated-back F6,
  `art/drafts/keeper-prime-seated-six-view-2026-10-16-v1/drafts/frames/keeper_prime_neutral_sitting-back_f01.png`
- identity, palette and render authority: approved Prime standing-back,
  `art/drafts/keeper-prime-orthographic-views-2026-10-13-v5/drafts/keeper_prime_master-neutral-standing-back_f1.png`
- choreography-only evidence: historical `keeper_sit_back_f6.png`; each call
  used only the matching F2–F5 joint progression and required zero visible
  historical pixels

All four prompts required: one complete rear-facing Keeper, transparent
background, planted feet, decreasing height through articulated knees and hips,
the exact F6 outer elbow/upper-body envelope, no chair, no props, no face, no
whole-character scaling and no crop.

Retained outputs:

- F2: `sources/generated/back-f2-generated.png` — first small lowering movement
- F3: `sources/generated/back-f3-generated.png` — second lowering movement
- F4: `sources/generated/back-f4-generated.png` — middle-to-late lowering pose
- F5: `sources/generated/back-f5-generated.png` — near-seated pose immediately before exact F6

The builder registers F2–F5 to 150 px width with heights 286, 276, 270 and
266 px. It then replaces the non-authoritative generated colour in F2–F5 and
the visibly darker seated-source colour in F6. Each clothing/component value
is mapped by luminance quantile to an exact RGB sample from approved rear Prime
V5. Jumper, trouser and boot medians are checked independently; every visible
RGB triplet in F2–F6 must belong to that approved authority. F6 retains the
exact 150 × 264 px seated-back alpha plane and geometry. The chair is not part
of any generated image; the reviewer draws its rear as a separate foreground
layer so the Keeper visibly passes behind it.
