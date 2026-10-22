# Codex: Hergé ink marks and ten recipe pictures (from Claude, 22 Oct 2026)

**Commissioned by Claude under Frank's standing instruction of 21 Oct**
(Claude briefs Codex for bubble-story pictures, reviews the sheet in Frank's
place, wires the pictures in and releases). Frank's answer m1 on the
project page: “Yes, all of it”: the motion marks move to Hergé's black-ink
style. Claude changes how the engine throws and moves them; you draw them.

Read first: `docs/CODEX_PROMPT_BUBBLE_STORIES_LIGNE_CLAIRE_REDRAWS_2026-10-21.md`
(the eight ligne-claire rules and the self-test; they all apply here) and
`data/activity-stories/README.md`.

This supersedes the eleven marks in batch 1 of that redraw prompt
(`symbol-impact-star` … `symbol-question-mark`): draw them once, here, in ink.

## Part A: the mark set in black ink (29 marks)

What Hergé does, and what we want:

- **The mark is the ink stroke itself.** Solid near-black (the same ink as
  the objects' outline), one even weight. Not a coloured shape with an
  outline round it: no outline-plus-fill, no shading, no highlight, no glow.
- **Shapes that need an inside** (a drop, a bubble, a steam wisp, a dust
  cloud) are a black line with a flat white or very pale inside, nothing
  more.
- **Colour is a rare accent.** At most one flat spot colour per mark, and
  only where the list says so. It never replaces the black.
- **Small and single.** The engine scatters marks itself: it throws 2 to 4
  copies of a single-piece mark at different angles and sizes, flips and
  nudges them every couple of frames (“boil”), and snaps them on and off.
  So draw each **single-piece** mark as ONE piece, upright and centred. Draw
  a **small group** only where the list says “small group”, kept tight.
- **Line weight at game size.** Marks are drawn smaller on screen than
  objects (about 40 px against 70 px for a 256 cell). Use a stroke about
  1.8× your object line weight in cell pixels (about 11 px in the 256 cell),
  so the ink matches the objects' line in the bubble.
- Same cell rules as every picture: 256 × 256 transparent, at least 16 px
  gutter (target 20), one owner, nothing baked in (no motion, no context).

New versions of existing ids (the meaning is the same, so every story
switches over by itself; add each with `npm run activity-stories:add-picture
-- <id> <file.png> --note "Hergé black-ink mark (m1)"`):

| id | single piece or small group | the drawing |
| --- | --- | --- |
| `symbol-impact-star` | single | Hergé's impact: a small solid black star with 6–8 short straight strokes radiating round it. |
| `symbol-motion-ticks` | single | Two or three short curved parallel strokes, a whoosh. |
| `symbol-water-droplets` | single | One teardrop: black line, white inside. |
| `symbol-soap-bubbles` | small group | Three small circles of different sizes, black line, white inside, no shine. |
| `symbol-heat-curls` | single | Three wavy vertical strokes side by side. |
| `symbol-sizzle-spark` | single | A tiny burst of four or five short strokes. |
| `symbol-clean-glint` | single | A slim four-point star drawn as a solid black cross-star. |
| `symbol-dust-puff` | single | A small lumpy cloud: black line, pale grey flat inside. |
| `symbol-earth-clods` | small group | Three small clods, black line, one flat earth-brown. |
| `symbol-sawdust` | small group | Five or six short black flecks and curls. |
| `symbol-seasoning-flecks` | small group | Six or seven small black dots and flecks. |
| `symbol-spray-mist` | small group | A fan of fine black dots spreading out. |
| `symbol-steam-puff` | single | One rising curling wisp: black line, white inside. |
| `symbol-question-mark` | single | Hergé's heavy brush-shaped ?, solid black. |
| `symbol-exclamation-mark` | single | Hergé's heavy brush-shaped !, solid black. |
| `symbol-foul-odour` | single | Two or three wavy rising lines. |
| `symbol-pleasant-aroma` | single | Two smooth curling rising lines, one tiny flat pink accent. |
| `symbol-heat-shimmer` | single | Three wavy horizontal strokes, flat red accent allowed on one. |
| `symbol-welding-sparks` | small group | Short straight strokes flying from a point, flat yellow-orange accent. |
| `symbol-cold-snowflake` | single | A simple six-arm black snowflake. |
| `symbol-electrical-arc` | single | A black zigzag bolt with a flat yellow inside. |

New marks (add with `--kind mark --family <family> --label "<label>"`):

| id | family | the drawing |
| --- | --- | --- |
| `symbol-speed-lines` | motion | Three straight parallel horizontal strokes of slightly different lengths (the engine turns them along the movement). |
| `symbol-swirl` | motion | One loose swirl stroke. |
| `symbol-spiral` | notation | A tight black spiral (dizzy, puzzled). |
| `symbol-zigzag` | notation | One short sharp zigzag stroke (cross, jolt). |
| `symbol-ink-star` | impact | A small solid black five-point star. |
| `symbol-accent-red-star` | notation | Hergé's grawlix star: flat red, black line. |
| `symbol-accent-yellow-sun` | notation | A flat yellow disc with short rays, black line. |
| `symbol-accent-blue-spiral` | notation | A spiral drawn in flat blue, black line either side. |

Leave the six music-notation marks as they are.

## Part B: ten pictures the next recipes need (new ids)

To the full ligne-claire rules (objects, not marks). Pairs marked “same as”
must match exactly in shape, size, viewpoint and position in the cell, so a
swap reads as the same thing becoming clean.

| id | family | label | the drawing |
| --- | --- | --- | --- |
| `dishwasher-machine` | dishwasher | Dishwasher, door open | A built-in kitchen dishwasher, door folded down, the lower rack pulled half out and empty. |
| `laundry-washing-machine` | laundry | Washing machine | A front-loading washing machine, round porthole door closed, a dial and a soap drawer. |
| `laundry-basket-dirty` | laundry | Laundry basket of dirty clothes | A wicker laundry basket heaped with crumpled clothes. |
| `wear-shirt-muddy` | wearable | Muddy shirt | A crumpled work shirt with flat brown mud patches. |
| `floor-muddy` | household | Muddy floor | A small patch of wooden floorboards at a low three-quarter view, with three muddy boot prints. |
| `floor-clean` | household | Clean floor | Same as `floor-muddy`, clean. |
| `furniture-side-table-dusty` | household | Dusty side table | A small wooden side table with a flat grey layer of dust on top and two or three fluff balls. |
| `furniture-side-table-clean` | household | Clean side table | Same as the dusty one, clean. |
| `garden-plant-pot` | garden | Plant pot of soil | A terracotta flower pot filled with dark soil, nothing growing. |
| `fishing-sea-water` | fishing | Sea water | A small patch of calm sea surface: a flat blue band with two or three ripple lines, for the float to bob on. |

## How to deliver

1. `git pull` first. Work in this checkout (it is a separate worktree on
   branch `codex/ink-marks-2026-10-22`; Claude merges it).
2. One immutable pack:
   `art/drafts/activity-story-ink-marks-and-recipe-pictures-2026-10-22-v1/`,
   with sources, prompts, rejected attempts and two contact sheets in
   `evidence/`: the marks on the bubble's pale fill at game size and enlarged
   beside the current versions, and the objects light/dark/64 px as before.
3. Run the self-test on every picture. For the marks add one more: cover the
   colour; is it all one black ink, one weight?
4. Add every picture with `npm run activity-stories:add-picture` (never
   overwrite a version). Then `npm run verify:activity-stories` and
   `npm test`.
5. Commit on the branch. Do not push and do not deploy; Claude reviews the
   sheets, merges, wires and releases.
6. Leave a five-line handoff at the end of this file: what you added, the
   sheet paths, anything you could not do.

Do not edit `data/activity-stories/stories/`, `src/activityStories/` or any
approved authority.

## Handoff (Codex)

