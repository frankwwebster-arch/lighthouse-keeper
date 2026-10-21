# Prompt: Bubble stories ligne-claire action imagery

**Decision date:** 21 October 2026

**Status:** active; pilot plus first two family packs approved; action-imagery programme only

Frank approved the six-picture BBQ pilot with “agreed, these are superb”. This
prompt turns that approval into a controlled conversion programme for Bubble
stories pictures and independent comic reaction marks. It deliberately does
not authorise the more ambitious whole-game art-direction change.

**Progress (21 October 2026):** Frank also approved the seven-picture `bbq`
food and seven-picture `bbq-tools` continuation sheets. Their 14 components are
registered as current V2 versions from their immutable packs; all V1 versions
remain byte-identical and selectable. The library now contains 305 pictures and
333 versions. Continue with a new family pack rather than rebuilding either
approved BBQ pack.

## Ready-to-paste prompt

```text
Continue Lighthouse Keeper: convert the Bubble stories action imagery to the
approved ligne-claire language, family by family.

Read, in full, on main:
- docs/CLAUDE_TO_CODEX_BUBBLE_STORIES_2026-10-20.md
- data/activity-stories/README.md
- docs/ACTIVITY_CALLOUT_AUTHORING_STANDARD.md
- docs/CODEX_PROMPT_BUBBLE_STORIES_LIGNE_CLAIRE_PILOT_2026-10-21.md
- art/drafts/activity-story-ligne-claire-bbq-pilot-2026-10-21-v1/README.md
- art/drafts/activity-story-ligne-claire-bbq-pilot-2026-10-21-v1/PROMPT_LOG.md

First run `npm run stories -- help`. Use the family table in
data/activity-stories/README.md and inspect every current version with the
command-line picture tool before drawing.

Objective
- Translate the Bubble stories picture library into the original
  ligne-claire-inspired language approved in the six-picture BBQ pilot.
- Work in small, immutable, reviewable family batches. Start by completing the
  remaining BBQ and BBQ-tools pictures around the six approved pilot versions.
- The programme covers action objects, ingredients, tools, pictorial states,
  activity marks, emotions and independent comic reaction punctuation used by
  Bubble stories.
- The programme does not cover the Keeper body, approved Keeper animations,
  clothing embedded in animation frames, rooms, furniture production art,
  the game UI, title/album art outside the picture catalogue, or any other
  whole-game asset. Record suggestions for that separate redirection, but do
  not implement them in this task.

Visual authority
- The approved components in
  art/drafts/activity-story-ligne-claire-bbq-pilot-2026-10-21-v1/components/
  are the visual authority for contour, flat colour, detail density and
  game-scale readability.
- Draw original artwork: lively near-black contour of mostly even weight,
  simplified accurate shapes, flat opaque spot colours and minimal decisive
  interior lines. Use no gradients, glossy highlights, painterly modelling,
  airbrush, haze, bloom, cast shadow, thick sticker rim, emoji treatment or
  miniature scenic background.
- Give each picture one dominant semantic colour family, with only the
  restrained secondary colours needed to identify its material or state.
- Supplied comic panels are style and visual-grammar evidence only. Copy no
  copyrighted character, prop drawing, panel, setting, lettering, exact
  symbol or exact arrangement.

Exact-asset translation rule
- Treat the current picture version as the semantic and compositional source.
  This is a refinement of that exact asset, not a redraw from scratch.
- Preserve subject identity, viewpoint, object count, container, plate, bag,
  construction, state, recognisable contents, relative arrangement and broad
  silhouette unless Frank explicitly requests a content correction.
- Change the drawing language, not what the picture depicts. For example,
  `bbq-charcoal` remains the open paper bag with visible charcoal lumps and
  flame motif; loose rocks are not an acceptable substitute.
- Compare candidate and current version before accepting it. If preservation
  is uncertain, reject the candidate rather than rationalising the change.

Comic notation grammar
- Activity narration belongs in Claude's stable, fully opaque warm-white
  rounded rectangular panel with a short tail. Do not bake that panel into any
  picture supplied by Codex.
- Sustained Keeper emotions may use Claude's opaque expressive balloon:
  jagged for anger/alarm, soft or drooping for sadness, buoyant for joy,
  trembling for fear. The mark inside remains an independent picture.
- Immediate motion and reaction punctuation may appear unenclosed around the
  Keeper or affected object: stars, droplets, spirals, speed lines, impact
  ticks, anger scribbles, exclamation/question clusters and dizzy marks.
  Supply each as an independent transparent sprite; never bake it into a body
  frame, household object or activity picture.
- Build new reaction vocabulary only in separately named, review-gated packs.
  Candidate concepts include anger, sadness, fear, delight, delicious,
  amazement, confusion, surprise, exertion, dizziness, good aroma, bad smell,
  hot and cold. Make the pictorial idea instantly legible at 64 px; do not use
  a generic gold star for a specific physical event such as welding.
- Motion and emotion are not all gold. Colour carries meaning: heat can use a
  red/coral family, cold an icy blue family, and electric welding a blue-white
  family. Reserve accent colours rather than making every mark multicoloured.

Batch and approval workflow
- Use one family or one tightly related semantic set per immutable dated V1
  pack, normally 6–12 pictures. Do not attempt the complete catalogue in a
  single pack or approval sheet.
- Generate or draw one asset at a time. Record the exact prompt, tool/model,
  source references and their roles. Preserve every rejected source with a
  concise rejection reason.
- Create deterministic 256×256 RGBA components with genuine transparency,
  one semantic owner and at least 16 px clear gutter (target 20 px). Record
  measured alpha bounds, palette, source/output SHA-256 and derivation.
- Build a contact sheet for every batch showing, for each id: the prior-current
  version, candidate on warm white, candidate on dark, prior at 64 px and
  candidate at 64 px. Label ids and proposed version numbers.
- Stop at the contact-sheet gate. Do not register unapproved candidates.
- After Frank approves a batch, add each candidate with
  `npm run activity-stories:add-picture -- ...`, using the family from the
  README table. Add a new version; never overwrite or delete an earlier one.
- Keep an approved batch reversible by discarding only its new versions or
  draft directory. Existing sources and versions stay byte-identical.

Ownership and prohibited edits
- Codex owns `data/activity-stories/pictures.json` through the add-picture
  command and owns the immutable art packs.
- Do not edit `data/activity-stories/stories/`, any approved authority,
  approved animation source, production sprite sheet or existing picture
  version.
- Claude owns `src/activityStories/`, including the opaque activity panel,
  emotion envelopes, anchors, timing, clipping and reduced-motion behaviour.
  Do not edit that directory unless Frank explicitly authorises a cross-role
  implementation task.

Verification and delivery
- Add a deterministic verifier for every pack: dimensions, RGBA mode, alpha
  edges, gutters, ownership, exact palette where applicable, manifest paths,
  current/prior hashes, source/output hashes and contact-sheet coverage.
- Run the pack verifier, `npm run verify:activity-stories`, `npm test`,
  `npm run build` and `npm run verify:review-archive`.
- If public/ reaches the enforced limit, run `npm run archive:keeper-review`
  and verify the archive again. Never commit review media under public/.
- Audit README.md and the relevant status, decision and handoff documents.
- Commit and push approved work to remote main without `[deploy]`. Do not
  deploy unless Frank separately asks.
- Hand back the contact sheet, exact pack path, registered ids and versions,
  verification results and commit hash. State explicitly that all earlier
  versions remain selectable.

Do not begin the whole-game ligne-claire redirection in this task. That later
programme requires a separate inventory, animation-specific preservation
contract, representative motion tests and explicit approval before any
approved animation or production asset is versioned.
```

## Programme boundary

“Action imagery” here means the independent visual vocabulary available to
Bubble stories: objects, tools, ingredients, states, marks, emotions and free
comic punctuation. The six approved BBQ versions establish the style. A
future whole-game art-direction programme would be much larger because it
must preserve the Keeper's identity, animation timing, contacts, sprite-cell
isolation, rooms, furniture and UI while changing the rendering language. It
therefore remains a separate approval-gated project.
