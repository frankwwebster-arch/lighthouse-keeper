# V3 activity-object generation log

**Tool:** built-in image generation, 19 October 2026.  All generated images are
callout-source art only. They contribute no Keeper, body, room, counter,
furniture, runtime or Kitchen pixels.

## Shared style and isolation contract

Every selected prompt requested a transparent 2 × 2 source sheet, polished
illustrated Lighthouse Keeper game language, deep navy contours, warm cream,
storm blue, sea-glass, copper and restrained gold/orange, strong reduced-size
silhouettes, no text/logos/UI/question marks, and generous transparent gutters
with no pixel crossing either ownership midline. Style references were the V2
callout sheets and, where useful, the current Kitchen object finish; references
were style-only and were not treated as pixel or geometry authorities.

## Selected sources

| Source | Four requested cells | Generated-image origin |
|---|---|---|
| `proteins-generated-v3.png` | cow; sheep; pig; bacon plate | `exec-19d63bc5-3bc1-40a9-b371-9231158fb33c.png` |
| `kitchen-prep-generated-v3.png` | chef's knife; vegetables; gravy jug; sandwich | `exec-6fd5a114-a9c3-4aa5-976b-0a7c5bcc11e1.png` |
| `meals-flour-generated-v3.png` | breakfast; lunch; dinner; unlabelled flour bag | `exec-7d229b96-d603-4113-b3f7-360dd640f80e.png` |
| `washing-tea-generated-v3.png` | washing-up liquid; kettle; tea mug; milk | `exec-c2aee55e-1897-4d50-8c8a-f6827b1d6f67.png` |
| `dental-generated-v3.png` | toothpaste; water; toothbrush; teeth | `exec-ac6278f3-b25b-47cc-b3f6-954a6a13ef63.png` |
| `bbq-meats-generated-v3.png` | steak; lamb chops; leg of lamb; charcoal BBQ | `exec-64c2d63c-2fd6-44de-a37f-a61ec482c8ca.png` |
| `sandwich-ingredients-generated-v3.png` | bread; ham; lettuce; tomato | `exec-2f14aaa7-cf28-41ec-b7bb-a6bc6b771eed.png` |
| `maintenance-leisure-generated-v3.png` | lamp polish; welding; vinyl; shower | `exec-7d9f8697-2607-431f-8939-b5086c125a97.png` |
| `rest-music-generated-v3.png` | sleep; drums; guitar; piano | `exec-c80640f4-d3ab-4b26-9512-5c586eb05268.png` |
| `harvest-garden-generated-v3.png` | fruit basket; vegetable basket; watering can; seeds/trowel | `exec-8b69fb86-3c3c-481d-8e14-38bf42983766.png` |
| `aquarium-garden-generated-v3.png` | fish food; fish; tank-cleaning tools; seedling | `exec-9db53d8f-e4b8-47ae-877f-7a545afecbb0.png` |
| `story-figures-isolated-generated-v3.png` | sheep jumping fence; fictional rock drummer; fictional psychedelic left-handed guitarist; fictional classical composer | `exec-20ce4418-5b88-49f2-83d3-c3cf5bfdcce1.png` |
| `aquarium-details-generated-v3.png` | tank castle; plants/gravel; treasure chest; aerator | `exec-e0d45051-5f93-48d5-bf2a-fbbd563e6dc9.png` |

The meat prompt explicitly requested clean butcher-shop presentation rather
than gore. The musician prompt requested fictional era/archetype caricatures,
not exact real-person likenesses.

## Rejected source

`story-figures-generated-v3.png` (`exec-2aff879e-3e53-471d-9c51-85155937f1b4.png`)
was retained as rejected provenance. Although the four figures looked separate,
their alpha bounds overlapped every possible horizontal ownership line. It was
not cropped, patched or registered. The replacement prompt required every
figure to fit inside the central 65% of its quadrant and a fully transparent
100-pixel midline band; the selected replacement passes that boundary test.

## Deterministic post-processing

`scripts/build_keeper_prime_back_work_activity_callout_v3.py` discards only
source alpha at or below 8, crops each explicitly declared non-overlapping
source cell, trims its owned visible bounds, proportionally registers it into a
256 × 256 transparent component cell with a 20-pixel target gutter, and fails
if the final gutter is below 16 pixels. No generative edit or manual paint is
performed after selection.
