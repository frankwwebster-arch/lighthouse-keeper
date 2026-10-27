# Kitchen v8 Step 1 — image-generation record

Tool: OpenAI built-in image-generation/edit tool.

Use case: `stylized-concept` for the three new objects, then
`precise-object-edit` for finish/control/proportion corrections.

## References

| File | Role | SHA-256 |
|---|---|---|
| `review/kitchen-proof-v3-rebuild/sources/v7-oven-authority.png` | sole line/style authority | `0a8f0cbeb8fda75bc2da9948da8f2c7fc5a54f14d8202ef5bc2c89d8c0bb5538` |
| `reference/kitchen-mood/kitchen-mood-03.png` | Belfast sink, painted wood and plate-display subject reference | `eec4bddd620599e6745dece2698be72d7f876c4f3bd1dc46fb8b46558adb5e6b` |
| `reference/kitchen-mood/kitchen-mood-04.png` | compact British cooker/range subject mood only | `36e61f0cd475314c87b7e63578c4a4cbf082dfe84b78d449f30ca9efefa8dcf2` |
| `review/kitchen-proof-v3/sources/prime/keeper_prime_master-neutral-standing-side-right_f1.png` | exact 1:1 comparison; composited, never generated | `a172a8a01a387a21d14c092d2a9eb53b938a44574279108a5776e2cc67f2fff3` |

## Shared final prompt contract

> Draw one isolated British cottage kitchen piece in the approved adult yet
> playful modern ligne-claire manner. Use confident uniform near-black ink,
> quiet hand-drawn charm, matt flat colour and no more than one hard-edged
> shadow tone per material. Preserve the supplied real-world proportion guide
> and baseline. Use genuine transparent alpha and generous gutter. No room,
> floor, wall, character, cast/contact shadow, exterior glow, gloss highlight,
> white shine streak, chrome sparkle, soft gradient, photorealism, American
> diner styling, excessive ornament, text, logo, watermark, pink or magenta.

### Belfast sink cabinet

> A 1.00 m-wide freestanding matt duck-egg painted-wood cabinet with a scrubbed
> honey-pine top, deep cream apron-front Belfast sink, restrained traditional
> aged-copper crosshead taps, two simple framed doors and small copper knobs.
> Substantial construction; shallow straight-up 1/6 top reveal.

Selected source: `sources/sink-pass-02-final.png`. The final edit preserved the
tall/narrow construction while removing the generated background atmosphere
and simplifying the finish toward the shared matt treatment.

### Painted dresser

> A narrow freestanding British cottage dresser, 0.89 m wide and about 2.00 m
> high: matt duck-egg painted wood, two-door lower cupboard, one shallow drawer,
> scrubbed honey-pine counter, open two-shelf plate rack, a few simple cream
> plates with restrained cobalt-blue decoration, and small aged-copper pulls.
> Avoid a broad squat silhouette and country-kitsch scallops.

Selected source: `sources/dresser-pass-02-final.png`. The final edit preserved
the tall/narrow silhouette and restrained plate arrangement while removing the
generated background atmosphere.

### Small cream cooker

> A compact British freestanding cooker, exactly 0.60 m wide × 0.90 m counter
> height, with no tall back and no eye-level grill. Cream matt enamel; shallow
> top reveal; four dark burners/pan supports; exactly four copper/orange knobs;
> one separate dark-grey unlit indicator bezel; copper handle; closed dark unlit
> oven window with minimal shelf linework; cream plinth. It must read as a
> narrow 600 mm cooker, never a wide range.

Selected source: `sources/cooker-pass-03-final.png`. Two targeted edits first
removed the lit indicator and established four knobs, then corrected the body
to the deliberately narrow/tall 0.60:0.90 proportion.

## Deterministic review preparation

`build_style_test.py` discards generated exterior alpha below 32, crops the
remaining silhouette, reduces each source uniformly into its declared 1:1
canvas, keeps a two-pixel transparent edge gutter, and builds the comparison
sheet. The three-scale gate prepares the 2× candidates directly from the
selected high-resolution sources, uses the exact 1:1 candidates for room view,
and makes the 1/8 tower reductions from those reviewed 1:1 images. The Prime
Keeper is composited unchanged at 1:1 and resized uniformly for the other two
review scales. It does not palette-snap, re-ink, stretch, assemble a room or
promote an asset.

The cooker's one generated indicator bezel is the only status lamp. Runtime
light is specified as steady green while working and flashing red when broken;
no second lamp is to be added. The colour-choice swatches are current sampled
sage `#96B0A5` and proposed duck-egg `#A8CEC6`.
