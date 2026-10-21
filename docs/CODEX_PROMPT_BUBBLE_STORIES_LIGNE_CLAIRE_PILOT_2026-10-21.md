# Prompt: Bubble stories ligne-claire pilot

**Decision date:** 21 October 2026

**Status:** completed pilot prompt; six-picture contact sheet approved by Frank

Frank selected a new direction for Bubble stories after reviewing comic-strip
references: clear black ink, flat spot colour and expressive visual notation.
The first proof used a small BBQ set. Frank approved it on 21 October 2026
with “agreed, these are superb”. It does not authorise a silent redraw of the
complete library.

The reference panels are directional style evidence only. Do not copy their
characters, settings, panels, lettering, composition or exact symbols.

## Ready-to-paste prompt

```text
Continue Lighthouse Keeper: Bubble stories ligne-claire pilot.

Read, in full, on main:
- docs/CLAUDE_TO_CODEX_BUBBLE_STORIES_2026-10-20.md
- data/activity-stories/README.md
- docs/ACTIVITY_CALLOUT_AUTHORING_STANDARD.md
- docs/CODEX_PROMPT_BUBBLE_STORIES_LIGNE_CLAIRE_PILOT_2026-10-21.md

Frank has selected a new visual direction for Bubble stories. Build a small,
review-only BBQ pilot before proposing any whole-library conversion.

Art direction
- Use original ligne-claire-inspired drawing: lively near-black contour of
  mostly even weight, simplified accurate shapes, flat opaque spot colours,
  minimal interior lines and no rendered lighting.
- Give each picture one dominant semantic colour family plus restrained
  secondary colours required by the subject.
- No gradients, glossy highlights, painterly modelling, airbrush, glow,
  cast shadow, thick sticker rim, emoji treatment or miniature scene.
- Preserve the subject's material/state through silhouette and a few decisive
  ink lines rather than texture.
- References explain the visual grammar only. Copy no copyrighted character,
  panel, setting, lettering, exact prop drawing or exact arrangement.
- This is a style translation of the current Lighthouse picture version, not
  a semantic redesign. Preserve its subject identity, viewpoint, object count,
  container/plate/bag, state, recognisable construction and broad composition
  unless Frank explicitly requests a content correction. Change the drawing
  language, not what the picture depicts.

Technical and product rules that remain binding
- Follow the activity-callout standard's isolation contract: one owner,
  genuine alpha, 256×256 RGBA, at least 16 px clear gutter (target 20),
  measured bounds and deterministic normalisation.
- Keep exact prompts, references and source/output SHA-256 values in an
  immutable dated draft pack. Preserve rejected attempts with reasons.
- Never overwrite, delete or mutate an existing picture version. Do not edit
  an approved authority or the existing source packs.
- Do not edit data/activity-stories/stories/.

BBQ art pilot — create exactly these six independent drawings:
1. bbq-grill-unlit — compact round charcoal grill, cold dark coals.
2. bbq-grill — the same grill construction with flat coral-red lit coals;
   no baked-in heat/spark marks.
3. bbq-charcoal — preserve the current open paper charcoal bag, visible loose
   lumps and flame motif; translate that exact asset concept into ligne claire.
4. bbq-sausages — linked raw sausages, no plate, tray or garnish.
5. bbq-hotdogs — two finished hot dogs in buns, restrained mustard line.
6. bbq-tongs — one pair of steel barbecue tongs with a simple coloured grip.

The lit and unlit grills must be visibly the same model and viewpoint. Make
the unlit source first, then derive a separate lit source without overwriting
it. Each of the other four pictures has one semantic owner and no detached
decoration.

Build an immutable pack named
art/drafts/activity-story-ligne-claire-bbq-pilot-2026-10-21-v1/ with:
- original RGBA sources;
- deterministic 256×256 components;
- manifest/register metadata;
- exact PROMPT_LOG.md;
- HASHES.sha256;
- a contact sheet showing old/current and pilot drawings side by side on
  warm-white and dark backgrounds at 256 px and game scale.

Do not run activity-stories:add-picture yet. This is an approval-gated pilot;
existing library versions must remain current until Frank approves the sheet.

Activity panel shell — Claude-owned companion proof
- The current organic translucent/outlined thought bubble is no longer the
  target. In a fresh review-only version, render an opaque warm-white activity
  panel: a compact horizontal rounded rectangle, subtly hand-inked rather than
  mechanically perfect, with a near-black outline and one short pointed tail
  aimed toward the Keeper.
- The panel must resemble original comic narration grammar, not reproduce a
  supplied panel. Use no copied lettering or characters.
- The white interior is fully opaque so room art cannot interfere with the
  pictures. Keep a generous inner safe area and clip all story pictures and
  marks to it.
- Preserve story order, timing, object ownership, contact marks, reduced
  motion and quiet-tail behaviour. Adapt the opening transition to the panel;
  do not retain decorative thought-bubble rings merely out of inertia.
- Keep activity narration and emotion display as two related but distinct
  envelope grammars:
  - an activity always uses the stable opaque rounded-rectangle panel because
    it contains an ordered pictorial story;
  - a standalone Keeper emotion uses an opaque expressive balloon whose outer
    contour carries tone: jagged for alarm or anger, soft/drooping for sadness,
    buoyant/scalloped for joy, trembling for fear, and so on.
- Emotion balloons still contain original pictorial marks, not copied dialogue
  or lettering. Their tails point toward the Keeper and their outlines may
  change with the emotion, while the activity panel geometry stays stable.
- Add a third, unenclosed reaction layer for immediate motion and emotion.
  Stars, droplets, spirals, speed lines, impact ticks, anger scribbles and
  dizzy marks may appear directly around the Keeper or the affected household
  object, outside either envelope. This is free comic punctuation, not a
  second panel.
- Keep those reaction marks as independent sprites with explicit Keeper/object
  anchors, short lifetimes and deterministic z-order. Never bake them into a
  body frame, household asset or story picture. Review controls must be able to
  hide them independently, and reduced motion must preserve meaning without
  orbiting or rapid travel.
- Per repository ownership, Codex supplies the pictures. Claude owns changes
  under src/activityStories/. If one agent is asked to deliver both halves,
  Frank's explicit prompt is the authority to cross that boundary, and the
  changes must still be isolated and reviewable.

Verification
- Add a deterministic pack verifier for source edges, alpha ownership,
  gutters, dimensions, hashes and contact-sheet coverage.
- Run npm run verify:activity-stories, the relevant activityStories tests,
  npm test, npm run build and npm run verify:review-archive.
- Keep public/ below its enforced archive limit with npm run
  archive:keeper-review if a review builder produces media.
- Complete the documentation audit, commit and push to remote main without a
  [deploy] commit. Do not deploy the review pilot unless Frank separately asks.

Hand back the contact sheet, exact pack path, verification results and the
commit hash. Before approval, state clearly that the pilot is not current in
the Studio picture list. After explicit approval, register only the approved
new versions and state that the old versions remain untouched.
```

## What this prompt supersedes—and what it does not

For this pilot, the ligne-claire art direction supersedes the *visual finish*
paragraphs in `docs/ACTIVITY_CALLOUT_AUTHORING_STANDARD.md` that call for
polished painterly modelling, tactile highlights and glossy material volume.
It does not supersede that standard's isolation, alpha, cell, gutter,
ownership, naming, hashing, provenance or review requirements.

The six-picture gate settled line weight, palette, degree of detail,
food readability and the panel relationship before a 305-picture redraw is
estimated or started. Its approval authorises the six new immutable versions
and provides the style source for a separately prompted, versioned,
family-by-family action-imagery programme. It never authorises overwriting an
earlier asset.

Frank approved the contact sheet on 21 October 2026 with “agreed, these are
superb”. The six candidates were consequently added as new current versions;
the earlier versions remain selectable and byte-identical. The next programme
prompt is
`docs/CODEX_PROMPT_BUBBLE_STORIES_LIGNE_CLAIRE_ACTION_IMAGERY_2026-10-21.md`.
