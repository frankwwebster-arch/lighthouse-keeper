# Standard-uniform single reach pose V1

Status: **unnormalized single-pose visual study awaiting Frank's verdict**.

Frank authorized exactly one image-generation attempt after rejecting the
four-pose cue-acquisition grid for an extra arm. This attempt used one isolated
high-resolution canonical standing Keeper and the exact gameplay neutral as
references. The request explicitly replaced the visible lowered near arm with
one reaching arm, left the far arm hidden, and prohibited a cue or duplicate
limb.

The result contains one visible reaching arm and one visible hand, so the
extra-limb defect is absent. It also changed the rendering into visibly coarse
pixel art and should not be normalized or continued unless Frank explicitly
accepts its visual character.

Provenance:

- `PROMPT.txt` — SHA-256
  `9ec68ced387eca6beaeb4384498ce82972c3dc54ae40a5c21b42f2afcc36dcf4`;
- `inputs/canonical-standing-highres-single.png` — deterministic crop from the
  approved high-resolution walk source, SHA-256
  `3f57bb341b20cfc9727c6a3c5bc4622a5b6dc60b8b1d6b5811b182a498f97517`;
- `art/raw/keeper-first-batch/keeper_neutral_standing-side-right_f1.png` —
  SHA-256
  `02106cfc54b224c8d4e9985e58420f1350f114d24e2e6c6258cad68e513657ce`;
- `generated/single-reach-pose-v1.png` — untouched built-in image-generator
  output, SHA-256
  `4aa941c43769753b31d56453f3a38658507588d9d852899e4b876df4b6f80f2a`.

No normalization, sequence insertion, review registration, canonical/raw/
runtime amendment, commit, push or deployment occurred.

## V2 smooth-rendering correction

A targeted correction retained the one-arm gesture but again converted the
canonical smooth source art into coarse enlarged pixel blocks and retained
proportion drift. It is therefore recorded as failed rather than presented as
a usable draft:

- `PROMPT-V2-SMOOTH-CORRECTION.txt` — SHA-256
  `9fd8d4f370f1a6d098eb9d044fbb3688fb602485da609877a73dd926fb192734`;
- `generated/single-reach-pose-v2-smooth-correction-failed.png` — SHA-256
  `2ac690766c11bbc469b2d5ad0bf09c390ba628e15b332595a67f209ffda521a3`.

Do not resume with another blind generated correction. The defensible next
method is an arm-only manual redraw on the exact complete canonical raster so
the head, beard, torso, legs and boots remain byte-identical.

## Corrected limb identification and deterministic V3

The first removal request targeted the wrong arm: it removed the normal lowered
foreground arm rather than the small extra rear arm protruding behind the
Keeper's left side. That built-in edit also redrew the full character and is
preserved only as rejected evidence:

- `PROMPT-V3-REMOVE-EXTRA-ARM.txt` — SHA-256
  `e689f4eebe81400bcbc22ecf3aec2cc484dcdacac0e06f0804b4f8a9fa17bc28`;
- `generated/failed-wrong-arm-removed-and-redrawn.png` — SHA-256
  `cced3ae11cf21bc063c3b08b998f7f6752fc683a1119cf89dd4f1aa0297177dd`.

Frank corrected the limb identification. An initial deterministic V3 cleared
only the rear hand and was also rejected because the attached blue sleeve
remained. `remove_extra_rear_arm.py` now starts again from the untouched smooth
first-attempt pose and clears the complete rear limb from its shoulder/sleeve
attachment through the small hand. Pixels outside the recorded removal polygon
are unchanged. The correct reaching arm and normal lowered foreground arm are
both retained; no generated reconstruction is used.

- deterministic result:
  `generated/single-reach-pose-v4-complete-rear-arm-removed.png` — SHA-256
  `c68c0ec394cf8342a8bb2ee542f108eacf5ba3f6480d0236e7d949e12c14a859`;
- rejected hand-only intermediate:
  `generated/single-reach-pose-v3-rear-extra-arm-removed.png`;
- validation and exact polygon: `validation-v4.json`;
- rerun status: byte-identical;
- normalization, sequence insertion, registration and promotion: not started.

## V5 fresh two-arm redraft

Frank rejected the deterministic deletion because removing the complete rear
limb also lost the definition of the back. V5 is therefore a fresh coherent
single-pose referenced-image redraw, not another erasure. Its explicit anatomy
contract requires one forward-reaching arm, one normally lowered arm, exactly
two hands, no rear arm, and a continuous rounded jumper/back silhouette from
collar to waist.

- exact prompt: `PROMPT-V4-FRESH-TWO-ARM-REDRAFT.txt` — SHA-256
  `fd4211229bb4c09d42414487de480e9d82a00bcfb7a22953a743c0848805c0ae`;
- untouched built-in image-generator output:
  `generated/single-reach-pose-v5-fresh-two-arm-redraft.png` — SHA-256
  `edad59744798973b83af65d386261f94e4f8ba4da7fd8eb26fc4614820226539`;
- referenced inputs: isolated canonical high-resolution standing Keeper,
  original smooth three-arm gesture study, and exact gameplay neutral;
- normalization, sequence insertion, registration and promotion: not started;
- status: awaiting Frank's visual verdict.

## V5 route animation preview

At Frank's request, V5 was uniformly normalized to the density-4 gameplay
baseline and inserted into a reversible preview sequence:

`keeper_walk_cycle` → `keeper_walk_stop` → exact standing neutral → V5 reach
pose → existing legacy `keeper_snooker`.

The V5 source foreground was uniformly scaled by `0.14204545454545456` from
776×1056 to 110×150, alpha-hardened, foot-anchored at `[128,160]` on a 256×160
route canvas, and placed at `[96,8]`. It has binary alpha and zero opaque border
pixels. A deterministic rerun is byte-identical.

- normalized pose: `generated/single-reach-pose-v5-normalized.png` — SHA-256
  `be3a7dc28580f976e02be56da8068a4ffe8250a80772f186d8b8dd63fb7f635c`;
- animated preview: `single-reach-v5-in-walk-stop-snooker-preview.gif` —
  SHA-256 `abb38693f63f9ae0781708d3b59912bccb6e22975a306c04c3d37e5339e3c7b2`;
- all-frame sheet: `single-reach-v5-in-walk-stop-snooker-contact-sheet.png`;
- exact normalization and sequence evidence: `validation-v5-preview.json`.

The snooker section remains the old rejected identity and is explicitly
labelled as such. No production, reviewer, manifest or deployment state was
changed.

## Frank's visual verdict

Frank reviewed the animated walk → stop → exact neutral → V5 reach → legacy
snooker preview and marked the V5 reach pose and its timing **good enough**.
This acceptance applies only to the single reach transition pose and its place
in the sequence. It does not accept the legacy snooker identity, authorize a
production replacement, or change the requirement that later cue-ready and
snooker-loop artwork retain the canonical beard and body ratios.
