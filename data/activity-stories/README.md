# Bubble stories: the shared formats

**Status:** draft formats, version 1 (20 October 2026). Review-only: nothing here is in the game yet.

**Picture-library update (21 October 2026):** the heat-shimmer, pleasant-aroma
and welding-sparks marks now also have colour-semantic V3 drawings;
`symbol-cold-snowflake` is available as a new `cold` mark and
`symbol-clean-glint` remains available as a `clean` mark. The earlier V1/V2
versions remain selectable and byte-identical for undo.

**Complete-catalogue update (21 October 2026):** the library now exposes all
298 review-ready isolated source components from Activity Cloud Composer
V1–V7, Prime rear-work activity-callout V2/V3 and every component-bearing
Claude or Codex picture pack. The Studio therefore has 305 pictures and 338
immutable versions, including
every V5 album homage, the complete aquarium and bedroom sets, and 54 new
fishing, gardening, pet-play, fixing, pub, art and inventing pictures. Run
`node scripts/import_activity_story_picture_catalogue.mjs` to reconcile those
immutable source packs; `npm run verify:activity-stories` fails if any source
component is absent or has lost its pinned version.

**Ligne-claire pilot (21 October 2026):** Frank selected flat near-black ink,
opaque spot colour and expressive comic notation as the candidate next visual
direction. Six BBQ pictures were translated and approved under
`art/drafts/activity-story-ligne-claire-bbq-pilot-2026-10-21-v1/`. They
preserve each current asset's subject, count, state, container, viewpoint and
broad composition. They are registered as new current versions while all
earlier versions remain selectable and byte-identical. The action-imagery
continuation prompt is
`docs/CODEX_PROMPT_BUBBLE_STORIES_LIGNE_CLAIRE_ACTION_IMAGERY_2026-10-21.md`.
The pilot prompt and the proposed opaque
rounded-rectangle activity panel / expressive emotion-envelope / free reaction
layer grammar are in
`docs/CODEX_PROMPT_BUBBLE_STORIES_LIGNE_CLAIRE_PILOT_2026-10-21.md`.

**First family continuation approval (21 October 2026):** Frank approved the
seven remaining `bbq` pictures and seven remaining `bbq-tools` pictures in
their separate ligne-claire V1 packs at
`art/drafts/activity-story-ligne-claire-bbq-food-2026-10-21-v1/` and
`art/drafts/activity-story-ligne-claire-bbq-tools-2026-10-21-v1/`. Each pack
pins the prior-current hashes and includes deterministic 256 px candidates,
prompt/rejection provenance, a verifier and a five-column light/dark/game-scale
contact sheet. All 14 are registered as current V2 versions, taking the library
to 305 pictures and 333 immutable versions. Every V1 predecessor remains
selectable and byte-identical; no story definition or activity-story runtime
file changed.

**Sandwich family approval (21 October 2026):** Frank approved the immutable pack at
`art/drafts/activity-story-ligne-claire-sandwich-2026-10-21-v1/`. It provides
V2 translations for the four `sandwich` ingredients and the shared
`cooking-sandwich` result, with exact current-content preservation, prompt and
rejection provenance, deterministic 256 px normalization, pinned hashes and a
five-column light/dark/64 px contact sheet. All five are registered as current
V2 versions, taking the library to 305 pictures and 338 versions. Every V1
predecessor remains selectable and byte-identical; no story definition or
`src/activityStories/` file changed.

**Pace:** the game takes its time. Activities never rush, however mundane;
the game world's clock and life management are central (Frank, 20 Oct). A
story has no upper length, only a five-second floor. Frank sets each
activity's length himself; the studio just shows how many times a story
would play in a 20–30 second activity.

A bubble story is the little animated picture story above the keeper's head
while he works with his back to us: the grill arrives, the charcoal drops in,
the sausages flip on, the burgers appear, a quiet moment, then it starts
again. **The order of the steps is the story.**

Three people share this folder, each with one job:

| Who | Owns | Where they work |
| --- | --- | --- |
| **Frank** | What each story says: its steps, their order and pace, which pictures | The recipe studio: Grown-ups → Recipe studio → **Bubble stories** (`/studio/stories`) |
| **Claude** | The motion rules, the drafts and the tools | `src/activityStories/`, `stories/*.json`, `scripts/*activity_stor*` |
| **Codex** | The pictures and marks themselves | `pictures.json`, via `npm run activity-stories:add-picture` |

The approved Prime keeper is never touched: the library only *points* at its
24 rear-work frames by hash.

## Files

```text
data/activity-stories/
  pictures.json        the picture library (every picture, every version)
  stories/<id>.json    one draft story per file
```

Frank's saved edits live in the database (`studio_docs`, id `story-<id>`) and
win over the draft file, exactly like recipes. Claude copies them back into
`stories/` with `node --env-file=.env.local scripts/pull_activity_stories.mjs`.

## The picture library (`lighthouse-keeper/activity-picture-library@1`)

```json
{
  "pictures": {
    "bbq-grill": {
      "kind": "object",
      "family": "bbq",
      "label": "Barbecue grill",
      "current": 1,
      "versions": [
        { "v": 1, "url": "/keeper-review/…/bbq-grill-8984470c007ff8a3.png", "sha256": "8984…",
          "cell": [256, 256], "bounds": [20, 43, 236, 213], "added": "2026-10-19",
          "source": "keeper-prime-back-work-activity-callout-v3", "by": "codex" }
      ],
      "review": { "status": "rework-requested", "note": "…" }
    }
  }
}
```

- **kind**: `object` (a thing in the story: grill, sponge) or `mark` (comic
  punctuation: stars, ticks, heat curls, smells, ? and !).
- **versions** are never edited or removed. A new drawing is a new version.
- **current** is the version every story uses. Change it and every story
  switches at once. A story can pin an older one (`"version": 1` on a cast
  member): that is Frank's one-tap undo.
- **bounds** are measured, never typed: the engine uses them so a touch mark
  lands exactly where two pictures meet.
- A picture's file is an archived `/keeper-review/…` URL (the seeded
  pictures), a file in an immutable `art/drafts/` pack referenced in place as
  `/activity-stories/repo/art/drafts/…` (served from GitHub, so push the pack
  to main first), or, for anything else, a copy the add tool makes in
  `public/activity-stories/pictures/<id>-v<N>-<hash>.png`.
- When something is replaced on the grill, raw food sinks into it, while a
  finished dish (cast role `result`) is served: it lifts up and away.
- Picture rules are the activity-callout standard's: a 256 × 256 transparent
  cell, at least 16 px of clear gutter on every side (target 20), one owner,
  no baked marks or context (`docs/ACTIVITY_CALLOUT_AUTHORING_STANDARD.md`).

## A story (`lighthouse-keeper/activity-story@1`)

```json
{
  "id": "garden-bbq",
  "label": "Garden BBQ",
  "appliesTo": { "assetId": "outdoor.bbq", "label": "Garden barbecue" },
  "afterStory": "loop",
  "pace": 1,
  "cast": {
    "grill":   { "picture": "bbq-grill",   "role": "hero" },
    "charcoal": { "picture": "bbq-charcoal", "role": "support" },
    "burgers": { "picture": "bbq-burgers", "role": "result" }
  },
  "steps": [
    { "do": "arrive",  "who": "grill" },
    { "do": "drop-in", "who": "charcoal", "onto": "grill" },
    { "do": "reveal",  "who": "burgers",  "onto": "grill" },
    { "do": "settle" }
  ],
  "ambient": [{ "picture": "symbol-heat-curls", "on": "grill", "fromStep": 2, "toStep": 3 }],
  "sfx": [{ "step": 2, "at": "contact", "cue": "charcoal-rattle", "owner": "outdoor.bbq", "kind": "asset-state" }]
}
```

- **cast** names each picture once by a short role name; steps refer to those
  names, never to files.
- **steps** run in order. Each has a verb, who acts, what it acts on, an
  optional speed (`quick`, `normal`, `slow`) and an optional mark to use at
  each touch instead of the usual one.
- **afterStory**: `loop` keeps retelling it while he works (Frank's choice);
  `hold` tells it once and keeps the result showing; `hide` tells it once and
  the bubble goes.
- **pace** speeds the whole story up or down (0.75–1.5).
- **ambient** marks ride on one picture for a range of steps.
- **flow**: `left-to-right` brings every picture in from the left and serves
  finished things off to the right (Frank's BBQ); `around` uses both sides.
- **loopFrom** (optional): retellings start again from this step, so
  setting-up steps (the cold BBQ, the charcoal) play only the first time.
- **props**: small scene-setting pictures (tools, sauces) for a range of
  steps, either `orbit` (circling inside the bubble all the way round,
  beneath the main action, one lap per retelling, each turning gently on the
  spot) or fixed in a corner. In a retold story, a prop whose range reaches
  the last step before the quiet moment persists: it stays up through the
  quiet moment and carries straight on into the retelling (it is shown from
  the retelling step, or its own first step if earlier), fading in only on
  the first telling.
- **sfx** names a sound and its owner; the story never contains audio.

The bubble's edge is loose and hand-drawn: `bubbleOutline()` in
`src/activityStories/compile.ts` gives the shape (the `BUBBLE` oval, grown
from V2's so the orbit fits all the way round, with gentle, slowly drifting
lobes), so the studio and the game draw the same bubble.

Before the first telling the bubble opens: its two rings pop up from his cap
and the bubble swells out of them. Retellings skip the opening, so the bubble
never disappears between them.

### The verbs

| Verb | Studio says | What happens |
| --- | --- | --- |
| `arrive` | arrives | Pops out of his head and takes the middle. |
| `present` | takes the middle | Moves to the middle; whatever was there steps aside. |
| `land-on` | lands on | Pops up at its side, swings in and stays stacked on top. |
| `flip` | flips onto | The same, with a somersault. |
| `drop-in` | drops into | Falls in and disappears inside. |
| `strike` | strikes | Hits it two or three times, then leaves. |
| `scrub` | scrubs | Rubs back and forth across it, then leaves. |
| `pour` | pours onto | Tips over it so drops fall, then leaves. |
| `tighten` | tightens | Turns in place on its edge, then leaves. |
| `reveal` | appears from | Bursts out; anything stacked on it is used up. `replace: true` takes its place. |
| `serve` | is served | Leaves the bubble: off to the right in a left-to-right story, otherwise upwards. |
| `pause` | pause | A beat where nothing new happens; heat, marks and props carry on. |
| `settle` | quiet moment | Nothing in the story moves (at least five frames); circling props carry on. Always last. |

## What the engine guarantees

`src/activityStories/compile.ts` turns a story into frames at 8 fps for full
and reduced motion. The tests (`compile.test.ts`) hold every draft to these
rules, which came out of the 20 October review of the V2 examples:

1. A support first pops up at its own side of the bubble, so you see what's
   coming, then swings in. Only one thing is on its way at a time.
2. A touch mark appears on the frame two pictures actually meet (gap ≤ 4 px),
   at the touching edge, for four frames.
3. Things that stack land and stay; tools do their job and leave.
4. Motion trails show only while something moves fast, and always draw
   beneath the pictures.
5. The quiet moment is completely still, with no marks; only persisting
   props keep circling.
6. Reduced motion has the same steps, timing and ending, with at most two
   pictures and one mark, and nothing travels.
7. A story never rushes: the studio warns below five seconds.

## Workflows

**Frank adjusts a story.** Studio → Bubble stories, unlock with the PIN,
change, Save. Saved for everyone on the live site.

**Codex replaces a picture.** Draw the new version to the standard, then:

```bash
npm run activity-stories:add-picture -- bbq-grill path/to/new.png --note "Warmer coals, cleaner lid"
npm run verify:activity-stories
```

Every story that uses `bbq-grill` now plays the new drawing. To go back:
`npm run activity-stories:add-picture -- bbq-grill --current 1`.

**Codex adds a new picture.** The same command with `--kind object` (or
`mark`), `--family` and `--label`. It appears in the studio's picture list
for Frank and Claude to use in a story.

**Codex adds a new picture.** Pick its `--family` from the table below:
that decides which fold-out group it appears in, in the studio and on the
command line. If no family fits, add one to `PICTURE_GROUPS` in
`src/activityStories/format.ts` (a one-line change Codex may make); a test
fails if any picture would land in “Other”.

| Studio group | Families |
| --- | --- |
| BBQ | `bbq` |
| BBQ tools | `bbq-tools` |
| Food and meals | `meal`, `sandwich`, `cooking`, `ingredient`, `baking`, `eggs`, `food-provenance`, `mixing`, `tea`, `toast` |
| Condiments and seasoning | `condiment`, `seasoning` |
| Knives and prep | `kitchen-tools`, `preparation-action` |
| Washing up and dishwasher | `washing`, `dishwasher` |
| Bathroom and personal care | `bathroom`, `dental`, `hygiene` |
| Cleaning products | `cleaning-products`, `cleaning-chemical` |
| Cleaning tools | `cleaning-tools` |
| Sponges, cloths and bags | `cleaning-cloths`, `consumable` |
| Laundry | `laundry` |
| Aquarium | `aquarium` |
| Fishing | `fishing` |
| Gardening | `garden` |
| Harvest | `harvest` |
| Music | `music` |
| Reading and writing | `reading`, `writing` |
| Bedtime | `sleep` |
| Clothes | `wearable` |
| Pockets and accessories | `personal-accessory` |
| Grooming | `grooming` |
| Books and music | `bedroom-leisure`, `leisure` |
| Pet care and play | `pet-care` |
| Exercise and games | `exercise`, `games` |
| Pottery | `pottery` |
| Rest | `rest` |
| Fixing things | `maintenance`, `repair` |
| Pub | `pub` |
| Art | `art` |
| Scientific and inventing | `inventing` |
| Marks | every `--kind mark`, whatever its family |

## The command-line tool (Claude and Codex)

The same engine and library as the studio, so what it checks and draws is
exactly what Frank sees. `npm run stories -- help` lists everything.

```bash
npm run stories -- pictures sponge        # find a picture's id (grouped, searchable)
npm run stories -- list                   # every story: length, how often it plays, problems
npm run stories -- check washing-up       # steps with frame numbers, and every problem
npm run stories -- render washing-up      # a PNG sheet of frames to look at
npm run stories -- render washing-up --from 20 --to 40 --every 1   # one stretch, every frame
npm run stories -- render washing-up --reduced
npm run stories -- new sweep-floor --label "Sweeping the floor" --like washing-up
```

`check` and `render` also take a path to any story `.json`, so a trial
story can be tried without listing it. Sheets go to `tmp/activity-stories/`
(not committed). Rendering uses Chrome (or the Playwright headless shell);
set `CHROME_PATH` if neither is found. Frame numbers include the bubble's
opening, as in the studio's frame counter.

**Who does what with it.** Claude drafts and changes stories (`new`, edit
the JSON, `check`, `render`, look, commit). Codex uses `pictures`,
`check` and `render` to see its pictures in motion, and may start a trial
story with `new` to show one off; Claude or Frank decides whether it
becomes a real draft. Frank's saved studio edits win over the files: run
`node --env-file=.env.local scripts/pull_activity_stories.mjs` before
changing a story he has edited.

Checks: `npm run verify:activity-stories` (library and references),
`npx vitest run src/activityStories` (motion rules) and
`npm run stories -- list` (every story at a glance).
