# Keeper animation image-generation record — 2026-10-09

This records the durable prompt briefs for the generated source art used in the
production pass. Generation used the built-in ImageGen tool in sprite-sheet
mode. These source images are inputs to the deterministic normalisation,
contract metadata and export work in
`art/source/keeper-first-batch/author_keeper.py`; the generated bitmap was never
accepted directly as runtime art without that pass.

## Shared prompt contract

Every request included the same core constraints:

> Produce a clean, evenly spaced animation pose sheet on a plain background for
> the existing Lighthouse Keeper. Preserve the approved short, stocky elderly
> man: identical skull and body scale, white eyebrows/hair, large stepped ragged
> white beard, navy keeper clothing where applicable, hand size and boot size.
> No scenery, labels, borders, duplicate body parts or cropped props. Keep the
> whole figure and all held equipment visible in every pose. Read left to right
> as a coherent animation with stable costume, face, beard and equipment.

The closest supplied production/reference art was included where the request
needed a particular outfit, facing or endpoint. Prompts asked for pose
continuity, not a new character design. `keeper_walk` and canonical sitting
references remained the production scale authorities even when generated source
spacing or proportions needed deterministic correction.

## Final source briefs

| Source file | Poses | Additional prompt brief |
|---|---:|---|
| `keeper-scuba-walk-side-generated-source.png` | 8 | Right-facing walk along a wooden jetty in mask, regulator, air tank, buoyancy vest and fins; clear alternating gait and stable equipment. |
| `keeper-scuba-jetty-dive-generated-source.png` | 12 | Start in the same scuba standing pose, stride and launch head-first from the jetty, enter water cleanly and finish prone facing right; no jetty or water scenery baked into the actor. |
| `keeper-scuba-horizontal-generated-source.png` | 8 | Canonical-scale right-facing horizontal scuba swim with coherent kick, tank, hoses, mask and fins; bubbles separate. |
| `keeper-scuba-up-generated-source.png` | 8 | Direct rear/upward scuba swim, stable tank and fins, coherent alternating kick; bubbles separate. |
| `keeper-scuba-down-generated-source.png` | 8 | Direct front/downward scuba swim, stable mask/regulator and fins, coherent alternating kick; bubbles separate. |
| `keeper-swim-costume-horizontal-generated-source.png` | 8 | Right-facing horizontal swim in the established striped costume; retain the full canonical body and complete limbs in every frame. |
| `keeper-parachute-landing-generated-source.png` | 10 | Begin hanging beneath a fully open round canopy, descend to feet-first touchdown, compress through knees, let the canopy collapse behind and finish standing; no landscape. |
| `keeper-fish-stand-generated-source.png` | 16 | Full standing fishing cycle: cast, line/float settle below the feet datum, bite, rod bend, reel and visible catch; never crop rod, line, float or fish. |
| `keeper-fish-sit-generated-source.png` | 16 | Same complete fishing cycle while canonically seated; chair and water remain separate; keep rod, line, float and catch complete. |
| `keeper-hot-drink-pour-generated-source.png` | 10 | Two-handed kettle pickup/pour/lower/release at a fixed mug and worktop contact, with a stable kettle and no hand/handle swaps. |
| `keeper-bath-enter-generated-source.png` | 8 | Discreet towel-covered bath entry, maintaining the approved figure and opaque privacy throughout; bath remains separate. |
| `keeper-bath-exit-generated-source.png` | 8 | Reverse-compatible towel-covered bath exit, fully opaque privacy coverage; bath remains separate. |
| `keeper-shower-enter-bathrobe-generated-source.png` | 8 | Cream bathrobe approach turning from rear-right to direct rear and crossing a shower threshold; cubicle and door separate. |
| `keeper-shower-exit-generated-source.png` | 8 | Towel-covered shower exit with stable opaque privacy, coherent turn and no cubicle baked in. |
| `keeper-pressups-side-generated-source.png` | 8 | Right-facing old-school workout-kit press-up loop, full articulated horizontal body visible, consistent hands/feet and beard silhouette. |
| `keeper-weights-back-generated-source.png` | 8 | Direct rear overhead barbell press in the old-school workout kit; complete bar and hands visible, stable rear identity. |
| `keeper-lift-button-front-generated-source.png` | 8 | Front-facing right-hand lift-button reach and return, actor only, stable feet and canonical front face. |
| `keeper-meal-oven-back-generated-source.png` | 8 | Direct rear oven retrieval with mitts and complete plated meal/tray; oven separate, no clipped plate. |
| `keeper-meal-place-side-generated-source.png` | 8 | Right-facing approach, lower and release the complete plate at fixed table height, then straighten; table separate and plate never cropped. |
| `keeper-mechanic-front-generated-source.png` | 8 | Direct front mechanic walk matching the established overalls and canonical gait/identity. |
| `keeper-snooker-generated-source.png` | 8 | Right-facing cueing cycle with a complete straight cue and stable two-hand grip; table and balls separate; allow a wider transparent canvas. |
| `keeper-spaceman-side-generated-source.png` | 8 | Right-facing three-quarter spacesuit walk matching the existing suit family, with full boots/pack and canonical actor scale. |
| `keeper-write-back-generated-source.png` | 8 | Rear writing loop at a fixed desk-height contact, stable paper/pen hand and canonical rear head/beard; desk separate. |

## Deterministic follow-up

The authoring pass extracted equal cells, removed the plain background, forced
hard alpha, aligned anchors, retained/expanded transparent prop space, repaired
individual continuity faults and replaced required endpoints with exact
production frames. In particular, the final scuba-dive frame is the exact first
horizontal scuba-swim frame. The parachute drift was built deterministically
from the deployed jump endpoint, and its neutral frame was inserted as the
landing start. A generated crouch replacement was rejected because of opaque
white artefacts; the existing source remained and its faulty frame was repaired
deterministically instead.
