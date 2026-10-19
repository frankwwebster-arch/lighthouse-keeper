# Activity Cloud Composer V5 prompt log

Generation date: 19 October 2026

Generator: built-in `image_gen` tool (default Image Generation skill path)

Output format: 1536×1024 RGBA PNG, transparent 3×2 source sheets

The final project-bound copies are the ten PNGs in `source/`. The original built-in outputs remain in the Codex generated-image store. Prompts below are recorded exactly as assembled: each numbered prefix was followed by the stated shared suffix with one blank line between them.

## Shared suffix A

```text
Scene/backdrop: genuinely transparent background; no panel, tile, floor, scenery or cast shadow outside each object.
Style/medium: polished hand-painted cartoon game iconography for a cosy maritime Lighthouse Keeper game; chunky dark-navy outline, warm cream highlights, muted brass-gold, sea-teal, coral and storm-blue palette, subtle painterly texture, strong readable silhouettes at thumbnail size.
Composition/framing: exact regular 3-column by 2-row grid; one named object illustration centred alone in each equal cell; at least 16% transparent safety gutter around every cell subject and fully transparent lanes at x=1/3, x=2/3 and y=1/2; nothing crosses or touches a cell boundary.
Constraints: six cells exactly in the requested order; no words, letters, numbers, logos, watermark, border, labels, background glow, opaque backdrop, human figure or Keeper. Each cell has exactly one owned illustration and no stray marks.
```

## Shared suffix B (ownership-safe rerenders)

```text
Scene/backdrop: genuinely transparent background; no panel, tile, floor, scenery or cast shadow outside each object.
Style/medium: polished hand-painted cartoon game iconography for a cosy maritime Lighthouse Keeper game; chunky dark-navy outline, warm cream highlights, muted brass-gold, sea-teal, coral and storm-blue palette, subtle painterly texture, strong readable silhouettes at thumbnail size.
Composition/framing: exact regular 3-column by 2-row grid. Reserve a completely empty transparent margin of at least 80 pixels on every side of every 512 by 512 cell. Keep each complete illustration inside the central 352 by 352 area of its own cell. Fully transparent lanes at x=512, x=1024 and y=512 must contain no part, glow or antialiasing from any illustration.
Constraints: six cells exactly in the requested order; no words, letters, numbers, logos, watermark, border, labels, background glow, opaque backdrop, human figure or Keeper. Each cell has exactly one owned illustration and no stray marks.
```

## Accepted prompt prefixes and files

1. `source/eggs-toast-source-sheet.png` + suffix A

```text
Use case: stylized-concept
Asset type: transparent 3x2 source sheet for household activity-callout sprites
Primary request: six separate illustrations, in reading order: (1) friendly brown hen beside a tiny chicken-coop doorway, (2) straw nest holding several eggs, (3) wicker egg-collecting basket with eggs, (4) compact retro two-slot toaster, (5) two golden toast slices popping upward, (6) butter dish and small unbranded jam jar as one breakfast-condiment arrangement.
```

2. `source/bathroom-source-sheet.png` + suffix B

```text
Use case: stylized-concept
Asset type: transparent 3x2 source sheet for privacy-safe bathroom activity-callout sprites
Primary request: six compact separate illustrations, in reading order: (1) clean old-fashioned white toilet viewed three-quarter angle with lid down, (2) toilet-paper roll on a simple brass holder, (3) small occupied-style brass door latch with a neutral circular indicator and no text, (4) deep freestanding enamel bathtub with brass taps and no person, (5) cluster of pearly soap bubbles, (6) cheerful yellow rubber duck. Keep all imagery clean, discreet and family-friendly.
```

3. `source/rest-reading-source-sheet.png` + suffix B

```text
Use case: stylized-concept
Asset type: transparent 3x2 source sheet for rest and reading activity-callout sprites
Primary request: six compact separate illustrations, in reading order: (1) cosy deep armchair, (2) three floating sleep marks shaped like soft hand-drawn Z forms but without printed typography, (3) folded warm blanket with a small pillow, (4) open illustrated storybook, (5) miniature sailing pirate ship with striped sails and no flag logo, (6) friendly storybook dragon.
```

4. `source/reading-pottery-source-sheet.png` + suffix A

```text
Use case: stylized-concept
Asset type: transparent 3x2 source sheet for reading and pottery activity-callout sprites
Primary request: six separate illustrations, in reading order: (1) storybook treasure chest with brass bands and a few gold coins, (2) friendly miniature fairytale stone castle with blue roofs, (3) compact pottery wheel carrying a centred spinning cone of wet clay, (4) two disembodied clean hands gently moulding one clay vessel, with wrists cropped naturally and no person, (5) single wet earthen clay lump with a simple wooden modelling tool, (6) finished glazed ceramic vase in sea-teal and cream.
```

5. `source/writing-pet-source-sheet.png` + suffix A

```text
Use case: stylized-concept
Asset type: transparent 3x2 source sheet for writing and pet-care activity-callout sprites
Primary request: six separate illustrations, in reading order: (1) classic fountain pen with brass nib, (2) sharpened wooden pencil, (3) open cream notebook with blank pages and no writing, (4) small old-fashioned ink bottle with no label, (5) simple pink-and-blue pencil eraser, (6) upright unbranded paper pet-food bag with a plain paw medallion and a few kibble pieces.
```

6. `source/pet-fishing-source-sheet.png` + suffix B

```text
Use case: stylized-concept
Asset type: transparent 3x2 source sheet for pet-care and fishing activity-callout sprites
Primary request: six compact separate illustrations, in reading order: (1) cheerful dog bone, (2) small whole silver-blue fish, (3) warm coral heart symbol rendered as an object, (4) three abstract curved purr-rumble marks with no letters or text, (5) ceramic pet bowl with a few pieces of food and no label, (6) traditional fishing rod and reel coiled into a compact silhouette with a very short loose line and no caught animal.
```

7. `source/fishing-exercise-source-sheet.png` + suffix A

```text
Use case: stylized-concept
Asset type: transparent 3x2 source sheet for fishing and exercise activity-callout sprites
Primary request: six separate illustrations, in reading order: (1) small silver-blue fish hooked safely at the mouth on a short curved line, (2) friendly cartoon earthworm bait beside a brass fish hook, (3) red-and-cream fishing float with tiny water ripples, (4) compact open tackle box containing floats and hooks, (5) single large sea-teal sweat droplet, (6) stylized flexed arm symbol wearing a navy rolled sleeve, arm only and no person.
```

8. `source/exercise-games-source-sheet.png` + suffix B

```text
Use case: stylized-concept
Asset type: transparent 3x2 source sheet for exercise and tabletop-game activity-callout sprites
Primary request: six compact separate illustrations, in reading order: (1) compact brass-and-navy dumbbell, (2) pair of practical plain sea-teal training shoes with no emblem, (3) tightly coiled skipping rope with wooden handles, (4) coral activity-heart symbol with a simple cream pulse zigzag but no text, (5) fan of five generic playing cards using simple suit pips and no letters or numbers, (6) pair of ivory game dice with dark navy pips.
```

9. `source/games-repair-source-sheet.png` + suffix B

```text
Use case: stylized-concept
Asset type: transparent 3x2 source sheet for tabletop-game and practical-repair activity-callout sprites
Primary request: six compact separate illustrations, in reading order: (1) small colourful board-game path board with four simple pawns and no text, (2) single carved chess knight, (3) timber boat-hull repair patch with two planks, brass rivets and a small caulking mallet, (4) compact unbranded red petrol can beside a dark fuel nozzle, with no words or hazard mark, (5) small blue-and-brass outboard motor viewed three-quarter angle, (6) crossed practical wrench and toothed engine cog.
```

10. `source/repair-source-sheet.png` + suffix A

```text
Use case: stylized-concept
Asset type: transparent 3x2 source sheet for general practical-repair activity-callout sprites
Primary request: six separate illustrations, in reading order: (1) neat sailor's rope knot with two short ends, (2) upright old-fashioned foot-operated tyre pump with coiled hose, (3) open navy metal toolbox containing a few hand tools, (4) small carpenter's hammer beside three brass nails, (5) broad paintbrush beside a small unbranded tin of blue boat varnish with no text, (6) compact navy battery beside one coiled red-and-blue jump lead and clamps, with no letters or symbols.
```

Five first-pass sheets were rejected from the project because visible alpha above threshold crossed a declared ownership line. They were replaced by accepted prompts 2, 3, 6, 8 and 9 using suffix B. The rejected bytes remain only in the tool's generated-image store and are not referenced by V5.
