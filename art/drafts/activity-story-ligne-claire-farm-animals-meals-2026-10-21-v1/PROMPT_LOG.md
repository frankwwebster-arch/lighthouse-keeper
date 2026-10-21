# Prompt log

## User direction

Frank: “the animals looked VERY cartoon like, so need a full redraft, not just
a re-render in a new style”.

Frank then supplied `references/frank-horse-ligne-claire-reference.png` and
said: “can't find a cow or sheep in Tintin, but here's a horse”. The horse is
used only for anatomically legible quadruped construction, confident lively
contour, flat colour and sparse interior marks. Its subject, pose, rider, dog
and motion are not copied.

Three earlier observational redrafts made before that reference arrived are
retained under `rejected/` and excluded from the review gate.

## Shared animal prompt frame

Built-in image generation. Style inputs, in order: Frank's horse reference,
approved `washing-plate`, approved `sandwich-tomato`, approved
`repair-toolbox`.

> Use case: illustration-story. Asset type: transparent 256px Bubble-story
> picture. Image 1 is the primary animal-drawing reference supplied by Frank:
> use its anatomically legible weight-bearing quadruped construction,
> confident lively contour, flat colour and very sparse purposeful interior
> marks. Do not copy the horse, rider, dog, pose or motion. Images 2–4 are the
> approved project style references: plate for controlled hand irregularity,
> tomato for flat-colour economy, tool chest for construction hierarchy.
> Draw the named mature farm animal from scratch as a new observational
> ligne-claire animal. This must be a full anatomical redraft, not a restyle,
> tracing or re-render of the existing cartoon animal. Use fine mostly-even
> near-black contour with slight hand life, flat opaque spot colour and only a
> few decisive anatomy lines. One complete isolated adult animal, centred with
> clear transparent gutter, readable at 64 px. Genuinely transparent
> background; no base, grass, ground line, shadow, text or watermark. Avoid
> cartoon, mascot, children's illustration cuteness, character acting, smile,
> oversized head, glossy eyes, white eye surround, toy proportions, sticker,
> game icon, gradients, airbrush, bevels, texture speckling, patina and
> decorative distress.

### `cooking-cow`

Cache: `exec-6faf94f0-7779-4cd6-ad3e-c98a74cbaed0.png`

> One adult black-and-cream dairy cow standing calmly, body left-to-right and
> head at right turned only slightly toward us; long bovine torso; articulated
> shoulder, hip, knees and hocks; four weight-bearing legs with cloven hooves;
> modest udder; long tail with dark switch; two small horns; natural ears; one
> small plain brass neck bell. Realistically proportioned head, long bovine
> muzzle, small dark bead eyes and no visible sclera.

### `cooking-pig`

Cache: `exec-c2b3e5e0-9a11-4bd9-bbe8-034a77f1e064.png`

> One adult warm-pink farm pig standing calmly, body left-to-right and head at
> right; credible heavy low-slung barrel body; articulated shoulder and
> hindquarter; four short weight-bearing legs with cloven dark hooves; natural
> jowls; broad disk snout with two nostrils; medium folded ears; one small
> curled tail. Realistically proportioned head, small dark bead eyes, no
> visible sclera and neutral unperformed expression.

### `cooking-sheep`

Cache: `exec-7d2b1254-faaf-42eb-941c-35612c749727.png`

> One adult cream-fleeced sheep standing calmly, body left-to-right and head
> at left turned slightly toward us; credible ovine torso and shoulder/hip
> structure beneath dense fleece; narrow charcoal face with gentle Roman-nose
> profile; natural sideways ears; four slender weight-bearing dark legs with
> cloven hooves; short natural tail. Small dark bead eyes with no visible
> sclera. Describe fleece with a few irregular grouped masses and breaks rather
> than repetitive scallops.

## Shared meal prompt frame

Built-in image generation. Inputs, in order: exact current V1 as sole
semantic/compositional authority, then approved plate, tomato and tool-chest
champions.

> Use case: style-transfer. Asset type: transparent 256px Bubble-story
> picture. Redraw Image 1 as observational ligne claire, not a glossy food
> icon. Preserve the specified plate or bowl, food counts, viewpoint, overlap,
> arrangement and broad silhouette. Fine mostly-even near-black contour, flat
> opaque spot colours, a few decisive food and edge lines, slight controlled
> hand irregularity. Genuinely transparent background; no added food,
> utensils, table, base, cast shadow, text or watermark; readable at 64 px.
> Avoid cartoon, mascot, sticker, glossy game icon, photoreal food advertising,
> gradients, airbrush, bevels, shine streaks, repeated texture, speckling,
> patina and decorative distress.

### `meal-breakfast`

Cache: `exec-9a039209-2f7e-4eff-b66a-169f412ff34e.png`

> Preserve one low cream plate with two blue rim lines, exactly two overlapping
> toast slices at rear, exactly three separate wavy bacon rashers at left,
> exactly one fried egg at front-right with one intact golden yolk, and exactly
> two tomato halves with restrained green herb leaves.

### `meal-dinner`

Cache: `exec-7a397300-d4f4-4fd0-8615-ee07e77a9f6f.png`

> Preserve one cream plate with two blue rim lines; three overlapping slices
> of roast poultry across the front under one continuous gravy pool; exactly
> three roast potatoes, two broccoli florets and three orange carrot pieces;
> preserve the small upper-right green sprig.

### `meal-lunch`

Cache: `exec-23c9785e-370f-45ea-b919-88b8b546554a.png`

> Preserve one large cream footed bowl with two blue horizontal bands, orange
> vegetable soup, four pale potato cubes, two carrot chunks, restrained dark
> green leaves/beans and flat parsley garnish; exactly one thick round bread
> slice leaning at right and one parsley sprig in front.

### `meal-steak-fries`

Cache: `exec-2dbe2575-79dd-401c-8304-b9ee3b8e4682.png`

> Preserve one thick rectangular grilled steak at left/front of one cream
> plate with two blue rim lines; retain the steak orientation, fat edge and
> five dark diagonal grill bands; preserve the compact pile of thick golden
> fries at right/rear with its current overlap and broad mass.
