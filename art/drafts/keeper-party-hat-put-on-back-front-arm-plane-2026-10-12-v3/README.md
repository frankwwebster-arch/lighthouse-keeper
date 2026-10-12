# Keeper party-hat front-arm-plane correction — 12 October 2026 v3

This reversible amendment corrects only frame 2 of
`keeper_party_hat_put_on_back`. Both connected arms now begin the lift along
the outer/front plane, wholly clear of the head silhouette, while both hands
hold one party hat above the crown. Frame 3 continues the same upward motion.

Frames 1 and 3–8 are byte-identical to v2. Canonical raw/runtime art and the
complete v1 and v2 drafts remain unchanged until explicit promotion.

## Image-edit provenance

The exact v2 frame 2 was edited with the built-in image tool in
`precise-object-edit` mode. Exact v2 frames 1 and 3 supplied the adjacent motion
references. No CLI/API fallback was used.

Final prompt:

> Use case: precise-object-edit
> Asset type: transparent single-frame game sprite
> Input images: Image 1 is the exact frame-2 edit target; Image 2 is the exact
> preceding neutral frame 1; Image 3 is the exact following raised-hat frame 3.
> Primary request: Replace only the arms, hands and party-hat action in Image 1
> with a physically coherent intermediate between Images 2 and 3. Both arms
> must begin lifting upward in the front/near plane along the outer sides of
> the torso and shoulders. Keep both forearms and hands entirely in front of
> the shoulders and clear of the head silhouette: no arm, forearm or hand may
> pass behind the head, hair or nape. Both hands hold the same red-and-cream
> party hat just above the crown, lower than its position in Image 3, so the
> next frame continues smoothly upward.
> Constraints: preserve the exact head, hair, ears, back-facing body, jumper,
> stripe, trousers, boots, scale, position, pixel-art style and transparent
> background from Image 1. Arms must be anatomically connected at both
> shoulders, elbows lower than the hands, one hand on each side of one hat. No
> duplicated limbs, no hands on the rear torso, no face, no smile, no captain's
> cap, no detached hat, no background, text, shadow, crop, rescale or watermark.

`build.py` keeps only the largest connected generated component, normalizes it
to frame 3's 184-pixel full action height, restores binary alpha, bottom-centres
it in the existing 128×224 cell and rejects any shared-edge alpha. It also
rejects any change in frames 1 and 3–8.

## Pinned hashes

- Canonical strip: `ca3877f5de83830f0e3609b7857f117093908396e5d2ed6ac640357c0823a935`
- 11 October v1 strip: `319b7ea9e97fed22dd0c4cf35b501602b0ea4d054e21593818b3f40ca26d7adf`
- 12 October v2 strip: `f782da08d76f30182c748dd38fddfa9e95b676f4ab772cf10d42303ce9dae31f`
- Built-in edit: `4fbef541ae0d04553e81763a3ea14b56a6fdf337f816088c52180ef04b99a845`
- Review draft strip: `ced7a5b79298f3069aad8b6b0c525a358e87f20af73d639bf94d9b29c317fd2f`

Run the bundled Python runtime against `extract_inputs.py`, then `build.py`, to
reproduce the exact inputs, draft, contact sheets, animated preview, evidence
and register. Rejection remains fully reversible by removing this directory
and its single registry entry.
