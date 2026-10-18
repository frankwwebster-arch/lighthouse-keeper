# Prime Keeper sweep broom V1 prompt log

Built-in image generation was used in `identity-preserve` mode. Every call used
these references in this order:

1. `art/drafts/keeper-prime-side-right-rigged-2026-10-13-v1/sources/keeper-prime-side-right-rigged-clean-master.png` — sole identity, anatomy, outfit, smooth rendering and colour authority.
2. `art/source/keeper-first-batch/keeper-sweep-broom-generated-source.png` — choreography evidence only; no visible Keeper design or pixels may be copied.

The five returned sources are immutable inputs to the deterministic registration,
ownership-mask and Prime-palette pass. Generated colours are not authorities.

## Shared four-phase prompt

```text
Use case: identity-preserve
Asset type: high-resolution game animation source pose on genuine transparency
Input images: Image 1 is the sole approved Prime Keeper identity, silhouette, face, beard, clothing, smooth-outline, rendering and colour authority. Image 2 is choreography evidence only: use only its joint paths, weight transfer, hand/broom contact and timing; copy zero visible character design or pixels from it.
Subject: the exact same adult, restrained, slightly rotund Prime Keeper in right-facing side profile, wearing the exact single broad cream-band blue uniform, cap, trousers and boots from Image 1, sweeping with a traditional wooden broom.
Style/medium: polished smooth high-resolution 2D character illustration matching Image 1 exactly, not pixel art.
Composition: one isolated full-body pose, full broom visible, centered with generous transparent clearance on all sides; no grid, no sheet, no frame, no floor or shadow.
Identity constraints: solid dark rectangular eye with no glint; compact stepped nose; separate moustache; readable closed mouth; established broad beard and hair mass; exact cap, jumper, single cream band, trousers, boots, rotundity, proportions and outline language of Image 1.
Anatomy constraints: exactly two arms, two hands, two legs and two boots; both hands make anatomically connected contact with the same broom handle; no detached or duplicate parts.
Prop constraint: broom must remain visually separable from the Keeper, with a continuous wooden handle and complete bristle head, and must not touch any canvas edge.
Avoid: generic smile, open grin, round or highlighted eye, moustache merged into mouth, childlike proportions, double jumper stripe, scenery, text, guides, border, glow, particles, cropped body or broom.
```

The following pose line was appended for each call:

1. `Pose: phase 1 of an eight-phase loop. Moderately upright, front/right boot planted slightly ahead, rear/left boot trailing, weight beginning to move forward. Upper hand grips the shaft at lower chest height; lower hand grips at waist height. Broom leans diagonally down toward the floor ahead of the forward boot, bristles planted lightly.`
2. `Pose: phase 2. Shallow forward lean, weight centered over the forward/right boot while the rear/left leg extends back. Hands slide slightly down the same diagonal shaft, pushing the bristle head a short distance forward along the floor.`
3. `Pose: phase 3. Clear forward weight transfer with knees flexed; rear/left heel raised and front/right boot bearing weight. Torso and head tip forward as one coherent body. Both hands firmly grip the diagonal shaft while bristles travel farther forward.`
4. `Pose: phase 4, the deepest forward sweep extreme. Torso leans forward but remains balanced; front/right knee bends, rear/left boot lifts slightly behind. Arms extend down and forward while both hands stay wrapped around the handle; bristle head reaches its farthest forward floor contact.`

## Acquisition prompt

```text
Use case: identity-preserve
Asset type: high-resolution game animation source pose on genuine transparency
Input images: Image 1 is the sole approved Prime Keeper identity, silhouette, face, beard, clothing, smooth-outline, rendering and colour authority. Image 2 is choreography evidence only: use only its hand/broom mechanics; copy zero visible character design or pixels from it.
Primary request: draw the exact same adult Prime Keeper in strict side-right profile at the acquisition pose immediately before sweeping. He has just placed both hands on one traditional wooden broom held almost upright beside the front/right side of his body; the bristle head rests completely on the floor just ahead of his right boot. His torso and legs remain very close to the approved neutral stance, with only the two arms and hands moving to grip the handle. This must bridge cleanly from the exact neutral.
Style/medium: polished smooth high-resolution 2D character illustration matching Image 1 exactly, not pixel art.
Composition: one isolated full-body pose, full broom visible, centered with generous transparent clearance; no grid, sheet, floor or shadow.
Identity constraints: exact adult restrained Prime face; solid dark rectangular eye with no glint; compact stepped nose; separate moustache; readable closed mouth; established beard/hair mass; exact cap, single broad cream-band jumper, trousers, boots, rotundity and outline language.
Anatomy constraints: exactly two arms, two anatomically connected hands, two legs and two boots. Both hands grip the same continuous broom handle. No detached or duplicate parts.
Prop constraint: broom visually separable, complete, no contact with any canvas edge.
Avoid: grin, round/highlighted eye, childlike proportions, double stripe, scenery, text, border, glow, cropped body or broom.
```

## Actor-only ownership edits

Each composite source was then edited once in `identity-preserve` mode using
only that generated image as the edit reference. The complete edit instruction
was:

```text
Keep this exact character, pose, facial expression, anatomy, clothing, scale,
and transparent canvas unchanged. Remove the entire broom—handle, collar,
bristles, every prop pixel and every cast/ground trace. Reconstruct only the
small portions of both closed gripping hands and clothing that the handle had
occluded, while preserving the exact hand positions and closed grip shapes so
a separately rendered prop can pass behind them. Return one isolated actor on
genuine transparency. Add nothing else: no prop, floor, shadow, scenery, text,
guide, border, glow or particle.
```

The builder consumes only these actor-only edits. It renders the broom
deterministically as a separately owned layer behind the hands, so prop
ownership never depends on colour-key extraction or visual component order.

| Pose | Actor-only SHA-256 | Initial composite SHA-256 |
|---|---|---|
| acquire | `0a50a254f1a96e4cb409574fe46d83695c2d93a010f89d537e6da17873dce782` | `088a0cbc25d5b71467870da72fd27b0ab2bd89a6550c88c2258b7b84588e27df` |
| phase1 | `d2c828408b874dd309b204c77eacfb4b521eb1d52e23e45f656bab8a08087bde` | `01f0fe0655ce1dc06a0286a5a127afde457cad610f2dea90df59815422f0513a` |
| phase2 | `e9edb51464a350a730e0be76466676901cc0f9e912dbc4c54240f22d0d6edec4` | `2e2ed819040d59eec4235cfc927dcf8d5af9ad04a85f5efe4ed3be174731d609` |
| phase3 | `1c74d0212f7d926ba42b5ed0200d7b888dd3f450e838a8b9180137575f030891` | `355cac9bb7b92d515a5feeb4f4c88bd35b5448389d1bb5780a86915d3e5b44ec` |
| phase4 | `cbf9f77f2b4f31948a6c302a4cbb2a1e7e29a2b022a54d21b9cba1743a5dd5ba` | `20cf0d4e7f0cadca879fc91986a189d9ae83527b03eea59666ffffa146076ccc` |
