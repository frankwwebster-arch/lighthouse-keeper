# Bubble stories: what changes for Codex

**From:** Claude · **Date:** 20 October 2026 · **Status:** draft platform, review only, not in the game

## What Frank decided

After Claude's review of the Prime Rear Action Choreography V2 pack, Frank
decided that the bubble tells a quick story in order (about 5–10 seconds) and
that **Claude assembles the story patterns while Codex supplies the pictures**.
Frank adjusts stories himself in the recipe studio. His five choices:

| Question | Frank's answer |
| --- | --- |
| First build | Phase A: the story engine and the four stories, with controls for him |
| While he keeps working | Keep retelling the story (`afterStory: "loop"`) |
| How he adjusts | A list of steps: picture, what it does, speed; drag to reorder |
| Where | The recipe studio (`/studio/stories`) |
| When Codex replaces a picture | Every story switches automatically; old versions stay for a one-tap undo |

So, for bubble stories only, the 8 Oct split moves: **Codex keeps the
pictures, the symbols and the Keeper; Claude owns the bubble motion.** V1, V2,
the V7 composer and every approved authority stay exactly as they are;
nothing here edits them.

## The shared formats

Read `data/activity-stories/README.md`. In short:

- `data/activity-stories/pictures.json` is the picture library. It points at
  your existing archived pictures by URL and SHA-256 (33 pictures: V2's 20
  objects and 6 symbols, plus the 7 V7 symbols) and the approved 24-frame
  rear-work loop. Nothing was copied or redrawn.
- `data/activity-stories/stories/*.json` are the four drafts: Garden BBQ,
  Sandwich assembly, Washing up and General repair, rebuilt from the review
  fixes (stars on real touches, ingredients that land and stay, the hammer
  strikes the patch, soap bubbles instead of crash stars, endings in reduced
  motion).

## What Codex does from now on

**To replace a picture** (for example after a redraw):

```bash
npm run activity-stories:add-picture -- symbol-heat-shimmer path/to/new.png --note "Horizontal ripples, no flame read"
npm run verify:activity-stories
```

The tool checks the 256 × 256 cell and the 16 px gutter, copies the file under
a hash-stamped name into `public/activity-stories/pictures/`, adds version 2
and makes it current. Every story using it changes at once. Roll back with
`--current 1`. Never edit a listed file in place: the checker will fail.

**To add a new picture**, add `--kind object` or `--kind mark`, `--family`
and `--label`. It appears in the studio's picture list.

**Please don't** edit `stories/*.json`, `src/activityStories/` or the motion
rules; tell Claude (or Frank) what should change instead. Review pages
remain yours as before.

## First requests

1. Redraw the three V7 symbols the review flagged, as new versions (they
   carry `review.status: "rework-requested"` in the library):
   - `symbol-heat-shimmer`: reads as small flames and twins the heat curls.
     Try horizontal rippling lines above a hot surface.
   - `symbol-pleasant-aroma`: reads as two question marks at game size. Use
     open S-shaped wisps with no closed hook, in cream and brass.
   - `symbol-welding-sparks`: blurs into the sizzle spark. Give it a
     hot-white core and a one-sided spray from a contact point.
2. Draw one new mark, `symbol-clean-glint`: a small sparkle for things that
   are now clean or finished (the cutlery at the end of washing up). None of
   the 13 marks says “clean”.

3. **Garden BBQ redraws (Frank, 20 Oct evening).** Frank revised the story:
   the charcoal flies in, the sausages go on, then the finished hot dogs fly
   in and the sausages sink into the grill. Burgers no longer appear on top
   of the hot dogs; they need uncooked burgers first and will be their own
   follow-on story.
   - Add the redrawn sausages (no plate underneath) as a **new version of
     `bbq-sausages`**, not a new id, so the story picks them up at once.
   - Add uncooked burgers as a new picture: `--kind object --family bbq
     --label "Uncooked burgers"`, id `bbq-burgers-raw`. Claude then drafts
     the burger story (raw patties go on, the cooked burgers replace them).

4. **The full BBQ story (Frank, 20 Oct evening).** Frank is drawing new
   pictures. The story will run: unlit BBQ → charcoal → lit BBQ → raw
   sausages → hot dogs → raw burgers → tomato, lettuce, cheese → completed
   burgers → raw steak → finished steak meal with fries. Add each with
   these ids so Claude's draft picks them up:

   | Picture | Id | How |
   | --- | --- | --- |
   | Unlit BBQ | `bbq-grill-unlit` | new, `--kind object --family bbq` |
   | Lit BBQ | `bbq-grill` | new version of the existing grill |
   | Raw sausages (no plate) | `bbq-sausages` | new version |
   | Hot dogs | `bbq-hotdogs` | existing (new version if redrawn) |
   | Raw burgers | `bbq-burgers-raw` | new |
   | Tomato, lettuce | `sandwich-tomato`, `sandwich-lettuce` | existing (new versions if redrawn) |
   | Cheese | `food-cheese` | new, `--family food` |
   | Completed burgers | `bbq-burgers` | existing (new version if redrawn) |
   | Raw steak | `bbq-steak-raw` | new |
   | Finished steak meal with fries | `bbq-steak-meal` | new |

All of these follow `docs/ACTIVITY_CALLOUT_AUTHORING_STANDARD.md`. Once added, Frank
can put them into stories himself.

## Prompt Frank can paste into Codex

```text
Continue Lighthouse Keeper as Codex: pictures for bubble stories.

Read docs/CLAUDE_TO_CODEX_BUBBLE_STORIES_2026-10-20.md and
data/activity-stories/README.md on main.

1. Redraw symbol-heat-shimmer, symbol-pleasant-aroma and
   symbol-welding-sparks as described there, to the activity-callout
   authoring standard, and add each as a new version with
   npm run activity-stories:add-picture.
2. Draw and add a new mark, symbol-clean-glint (kind mark, family clean).
3. Add Frank's plate-free sausages as a new version of bbq-sausages, and
   uncooked burgers as a new picture, bbq-burgers-raw.
4. Run npm run verify:activity-stories and npm test.

Do not edit data/activity-stories/stories/, src/activityStories/ or any
approved authority. Do not overwrite existing versions. Commit and push
without [deploy], then tell Frank the new pictures are in the studio's
Bubble stories picture list.
```
