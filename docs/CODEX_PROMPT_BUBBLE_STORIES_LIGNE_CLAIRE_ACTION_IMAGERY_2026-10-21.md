# Prompt: Bubble stories ligne-claire action imagery

**Decision date:** 21 October 2026

**Status:** active; BBQ, sandwich, washing, General repair and repair hand-tool
packs approved; cooking-core review gate awaiting approval; action-imagery
programme only

Frank approved the six-picture BBQ pilot with “agreed, these are superb”. This
prompt turns that approval into a controlled conversion programme for Bubble
stories pictures and independent comic reaction marks. It deliberately does
not authorise the more ambitious whole-game art-direction change.

**Progress (21 October 2026):** Frank also approved the seven-picture `bbq`
food and seven-picture `bbq-tools` continuation sheets. Their 14 components are
registered as current V2 versions from their immutable packs; all V1 versions
remain byte-identical and selectable. At that gate the library contained 305
pictures and 333 versions.

**Second family approval (21 October 2026):** Frank approved the five-picture
sandwich semantic set at
`art/drafts/activity-story-ligne-claire-sandwich-2026-10-21-v1/`. It covers
`sandwich-bread`, `sandwich-ham`, `sandwich-lettuce`, `sandwich-tomato` and the
shared result `cooking-sandwich`. Its five components are registered as current
V2 versions; all five V1 versions remain byte-identical and selectable. The
library now contains 305 pictures and 338 immutable versions. Continue with a
new family pack rather than rebuilding an approved family.

**Third family approval (21 October 2026):** Frank approved the five-picture
`washing` family at
`art/drafts/activity-story-ligne-claire-washing-2026-10-21-v1/`. It covers
`washing-plate`, `washing-liquid`, `washing-sponge`, `washing-droplets` and
`washing-cutlery`, exactly the cast of Claude's unchanged `washing-up` story.
The approved `sandwich-tomato` V2 remains the primary flat-colour/detail
calibration because Frank identified it as the most successful translation.
All five washing candidates are registered as current V2 versions, taking the
library to 305 pictures and 343 immutable versions. Frank especially approved
the plate's minor shape imperfection and hand-drawn feel; its controlled
ellipse/rim asymmetry is now the primary shape calibration. Every V1 remains
selectable and byte-identical.

**Fourth family approval (21 October 2026):** the five object pictures used
by Claude's unchanged `general-repair` story are isolated at
`art/drafts/activity-story-ligne-claire-general-repair-2026-10-21-v1/`. The
sheet covers `repair-toolbox`, `repair-boat-hull-patch`,
`repair-hammer-nails`, `repair-wrench-cog` and `repair-rope-knot`. All five are
registered as current V2 versions, taking the library to 305 pictures and 348
immutable versions. Frank approved the exact sheet with “approved. tool chest
the best”, then clarified that the plate, tool chest and tomato are all style
champions. This family adds two recipe rules: inspect ambiguous counts enlarged
before prompting, and preserve the exact topology/parts of knots and mechanical
assemblies rather than merely matching their generic category.

**Fifth family approval (21 October 2026):** eight related adult hand tools
are isolated at
`art/drafts/activity-story-ligne-claire-repair-hand-tools-2026-10-21-v1/`:
`repair-adjustable-spanner`, `repair-c-clamp`, `repair-combination-pliers`,
`repair-flat-head-screwdriver`, `repair-phillips-screwdriver`,
`repair-hand-saw`, `repair-spirit-level` and `repair-tape-measure`. The pack is
immutable. Frank approved seven with “others all approve”; their V2s are
registered as current while every V1 remains selectable. He rejected the
spirit level with “this is too cartoonish”, so that first candidate remains
unregistered. Frank then selected the earlier, fuller correction with “this
one is good”. Its exact source and deterministic production derivative are in
`art/drafts/activity-story-ligne-claire-repair-spirit-level-user-selected-2026-10-21-v1/`;
the derivative is registered as current V2 and V1 remains selectable. The
library now has 305 pictures / 356 versions. A later immutable correction at
`art/drafts/activity-story-ligne-claire-repair-spirit-level-correction-2026-10-21-v1/`
remains unregistered historical exploration. The gate makes “ligne claire,
not cartoon” an explicit acceptance boundary: credible adult-tool proportions
and working construction without cute, toy-like, inflated, caricature, mascot,
sticker or glossy game-icon treatment.

**Sixth family review gate (21 October 2026):** the next unconverted
**Food and meals** semantic set is isolated at
`art/drafts/activity-story-ligne-claire-cooking-core-2026-10-21-v1/`. It
covers `cooking-bacon`, `cooking-cheese-slicing`, `cooking-gravy`,
`cooking-knife`, `cooking-pan`, `cooking-seasoning`, `cooking-spoon`,
`cooking-steam` and `cooking-vegetables`. All nine deterministic candidates
are unregistered pending Frank's review, so their current V1s and the library's
305 pictures / 356 versions remain unchanged. Count audits rejected two
plausible outputs whose prompts misstated the cheese knife's three rivets and
the vegetables' one whole tomato plus one wedge. Surface audits rejected a
speckled knife blade and distressed copper pan. The evolved recipe therefore
forbids accepting correct-looking pixels when provenance is wrong and treats
speckling, patina and decorative distress as modelling rather than useful
hand-drawn imperfection.

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
- Work in small, immutable, reviewable family batches. The BBQ, BBQ-tools,
  sandwich, washing, General repair and eight-piece repair hand-tools families
  are complete. All eight hand tools have approved current V2s, including
  Frank's explicitly selected fuller spirit level; every V1 remains selectable.
  The nine-picture cooking-core pack is the current unregistered review gate;
  do not register it before Frank's verdict. Continue later work in fresh
  immutable family packs.
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
  art/drafts/activity-story-ligne-claire-bbq-pilot-2026-10-21-v1/drafts/components/
  remain supporting visual authority for contour, flat colour, detail density
  and game-scale readability. Use the approved
  art/drafts/activity-story-ligne-claire-sandwich-2026-10-21-v1/drafts/components/sandwich-tomato.png
  as the primary flat-colour/detail calibration for subsequent families. Use
  the approved
  art/drafts/activity-story-ligne-claire-washing-2026-10-21-v1/drafts/components/washing-plate.png
  as primary calibration for lively contour and controlled minor asymmetry.
  Use the approved
  art/drafts/activity-story-ligne-claire-general-repair-2026-10-21-v1/drafts/components/repair-toolbox.png
  as the co-equal calibration for construction, detail hierarchy and confident
  object presence. Plate, tomato and tool chest are all champions; none
  supersedes either of the others.
- Draw original artwork: lively near-black contour of mostly even weight,
  simplified accurate shapes, flat opaque spot colours and minimal decisive
  interior lines. Use no gradients, glossy highlights, painterly modelling,
  airbrush, haze, bloom, cast shadow, thick sticker rim, emoji treatment or
  miniature scenic background.
- Ligne claire is observational simplification, not cartoon styling. Keep
  credible adult proportions, mechanisms, material transitions and practical
  construction. Reject cute, toy-like, inflated, caricature, mascot and
  sticker-like interpretations even when their palette and outline are clean.
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
- Inspect ambiguous counts and construction enlarged before writing the
  prompt. For knots and mechanical assemblies, preserve topology, crossings,
  parts and overlap order—not merely the generic object category.
- Allow small, deliberate irregularities in ellipses, rims, rings, teeth and
  curves where they create the approved hand-drawn feel; never let them alter
  identity, construction, viewpoint, contact logic or 64 px readability.
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
