# Activity-callout art and authoring standard

**Status:** binding authoring standard for future Lighthouse Keeper activity-callout work

**Revision:** 1.1 — 20 October 2026

**Machine-readable contract:** `data/activity_callout_style_contract.json`

This is the single starting point for extending the activity-callout vocabulary.
It records what Frank accepted as the right direction across the V2–V6 work,
what failed, and the exact method required to make later additions look and
behave like one family.

An activity callout is animated pictorial narration of an action whose detail
is hidden or too small to read. It is not dialogue, a thought bubble, a want,
an inventory display or a gameplay decision. The game or activity recipe owns
the action and its result; the callout only communicates it.

## Authority and precedence

Use references for their declared purpose rather than blending them
indiscriminately:

1. **Product and separation authority:**
   `KEEPER_BACK_WORK_ACTIVITY_CALLOUT_BRIEF_2026-10-19.md`.
2. **Validated visual direction:** the illustrated V2/V3 activity components,
   followed by the retained V5/V6 token sources and their exact prompt logs.
3. **Current data and timing authority:** Composer V6's catalogue. A future
   immutable composer may supersede this only through an explicit new version.
4. **General world palette and material language:**
   `floor-asset-catalogue/ART_STYLE_GUIDE.md`. Callout tokens deliberately use
   smooth illustrated contours rather than the world's final production-pixel
   rendering, but they must still feel made for the same lighthouse.
5. **Directional composition only:** Claude's sketch and Frank's supplied
   reference pictures. They explain the idea or subject; they are not pixel,
   layout, identity or final-style authorities.

V1's flat generic symbols are pinned rejection provenance. Never use them as
the style source merely because they are earlier. A newer accepted component
does not silently approve a body pose, runtime recipe or household asset.

## The visual language

The concise style phrase is:

> Polished hand-painted 2D game iconography for a cosy maritime Lighthouse
> Keeper game: smooth dark-navy outer contours, warm cream highlights, aged
> brass and copper, sea-glass teal, storm blue and restrained coral; tactile
> materials, compact silhouettes and clear reading at game scale.

Every token must have:

- one strong, immediately recognisable silhouette;
- a substantial dark-navy exterior contour, with lighter material-coloured
  interior seams where appropriate;
- two or three purposeful material values rather than noisy texture;
- restrained painterly highlights that describe form and material;
- rounded, friendly construction without becoming an emoji;
- enough simplification to survive thumbnail display, but enough specific
  hardware or texture to avoid generic clip art;
- a compact centre of mass that can orbit, hop and tilt without visual chatter;
- genuine transparency around the complete object.

Reference colour roles are `#14243a` deep ink, `#f3e7cc` warm cream,
`#e6b955` brass/light, `#267da0` sea teal, `#68a7c5` sea glass,
`#c8463c` restrained coral/red and `#23262b` charcoal. These are anchors, not
a requirement to flatten every subject into seven colours. Natural subject
colours remain welcome when the shared contour, highlight and saturation
discipline keep them in the family.

### Token scope

Prefer exactly one object or one readable story cue per token. A combined token
is allowed only where the parts form one ordinary semantic unit, such as a loo
brush in its holder, butter with a jam jar, or a hammer with nails. Do not pack
a miniature activity cloud into one component; recipe assembly supplies the
story.

Human or animal story figures must be fictional, warm and caricatured. Use
archetypes and era cues rather than an exact living or historical person's
likeness. Album art uses recognisable motif-only homages: no copied cover,
title, logo, typography, photograph or identifiable performer. Bathroom,
sleeping and washing cues stay discreet, family-safe and non-anatomical.

Food presentation must communicate state rather than decorate every token.
Loose ingredients and food awaiting cooking stand alone without a plate, tray
or garnish. Reserve plates and serving vessels for finished meals or for foods
whose vessel is part of their ordinary semantic read. When an inherited token
breaks this rule, preserve it as pinned history and propose the correction in a
new immutable draft; never overwrite the earlier component.

### Never introduce

- flat generic symbols, stock icon language or emoji treatment;
- photorealism, glossy mobile-app icons, hard extruded 3D or neon rendering;
- weak grey outlines, uncontrolled black crush or airbrushed background haze;
- a panel, tile, floor, room, vignette, glow or cast shadow in the transparent
  margin;
- words, letters, numbers, brands, labels, signatures or watermarks;
- a Keeper, full room, household context or unrelated second object;
- stray fragments, duplicate parts or decoration that becomes a second owner;
- a contextual prop painted into the Keeper body or household asset.

## Generation method

Generative drawing and deterministic normalisation have different jobs. The
generator draws a coherent object with ample clearance. The builder measures,
crops, scales, centres, hashes and verifies it. A builder must never repaint a
bad generation, invent missing pixels or disguise overlap with a tighter crop.

### Before generation

1. Start a new dated, numbered immutable draft directory. Never overwrite an
   earlier source, component, page, catalogue, manifest or review export.
2. Name the requested tokens and identify their families before drawing.
3. Check the latest component catalogue for an existing reusable token.
4. Decide whether each concept is one semantic object or should be split into
   several independently selectable objects.
5. Identify which existing accepted tokens provide the closest material and
   silhouette references. Reference images remain directional unless their
   authority is explicitly stated.

### Single-token prompt scaffold

Use this when quality or isolation matters more than batch economy:

```text
Use case: stylized-concept
Asset type: isolated game activity-callout token
Primary request: Create exactly one [SUBJECT], immediately recognisable as [READ]. [SUBJECT-SPECIFIC CONSTRUCTION AND MATERIAL CUES].
Input images: The supplied images are directional reference only for subject and the established illustrated Lighthouse Keeper game language; do not copy their layout, text, branding or identifiable people.
Scene/backdrop: genuinely transparent background.
Style/medium: highly polished hand-painted 2D game illustration; smooth anti-aliased contours; strong dark-navy outer line; warm cream highlights; aged brass/copper, sea-glass teal, storm blue and restrained coral where appropriate; subtle tactile painterly texture; matching the established Lighthouse Keeper activity-callout tokens.
Composition/framing: exactly one owned illustration, centred, compact and readable at thumbnail size, with generous transparent margin on all four sides.
Constraints: preserve actual alpha transparency; no Keeper, person unless explicitly requested, room, floor, panel, text, letter, number, logo, watermark, frame, vignette, background glow, cast shadow into the margin, detached fragment or additional object.
```

For symbols such as odour, bubbles, sparks or notation, replace painterly volume
with clean flat hand-painted marks while retaining the navy contour, restrained
palette and hard transparent cutout. Explicitly prohibit aura, haze and glow.

### Six-token source-sheet scaffold

Use a 1536 × 1024 RGBA sheet with a regular 3 × 2 grid only when all six
objects are compact and unlikely to cross cells:

```text
Use case: stylized-concept
Asset type: transparent 3x2 source sheet for household activity-callout sprites
Primary request: six compact separate illustrations, in reading order: (1) [A], (2) [B], (3) [C], (4) [D], (5) [E], (6) [F].
Scene/backdrop: genuinely transparent background; no panel, tile, floor, scenery or cast shadow outside each object.
Style/medium: polished hand-painted cartoon game iconography for a cosy maritime Lighthouse Keeper game; chunky dark-navy outline, warm cream highlights, muted brass-gold, sea-teal, coral and storm-blue palette, subtle painterly texture, strong readable silhouettes at thumbnail size.
Composition/framing: exact regular 3-column by 2-row grid. Reserve a completely empty transparent margin of at least 80 pixels on every side of every 512 by 512 cell. Keep each complete illustration inside the central 352 by 352 area of its own cell. Fully transparent lanes at x=512, x=1024 and y=512 must contain no part, glow or antialiasing from any illustration.
Constraints: six cells exactly in requested order; no words, letters, numbers, logos, watermark, border, labels, background glow, opaque backdrop, human figure or Keeper. Each cell has exactly one owned illustration and no stray marks.
```

Rerender an affected token or sheet if alpha crosses an ownership line. Do not
crop the overlap away and pretend the source was isolated.

### Prompt and source record

Every version keeps a `PROMPT_LOG.md` containing:

- generation date and tool;
- exact prompt text, not a paraphrase;
- which input references were supplied and their declared roles;
- accepted source filenames and SHA-256 values;
- rejected attempt count and concrete rejection reason;
- any edit prompt, with before/after source identity;
- the deterministic normalisation rule used afterward.

Copy accepted generated output into the versioned draft. The external tool
store is not the project record. Never rewrite an accepted source in place.

## Deterministic raster, gutter and ownership contract

The standard component cell is 256 × 256 RGBA. A visible source pixel is alpha
greater than 8. All four source outer edges must have zero visible pixels.

For a single-token source:

1. Find the alpha-greater-than-8 bounding box.
2. Reject an empty source or any visible outer-edge pixel.
3. Scale uniformly into the central area of a fresh transparent 256 × 256 cell.
4. Require at least 16 transparent pixels to every cell edge; target 20 pixels
   for all new work.
5. Centre deterministically using integer coordinates. Record bounds, scaled
   size and final offset.
6. Save losslessly and record the final SHA-256.

For a 3 × 2 source sheet, each 512 × 512 cell has an explicit owner. The exact
shared boundary lines at x=512, x=1024 and y=512 must contain no visible alpha.
Assign pixels geometrically to their declared cell; never assign disconnected
components by visual or list order.

Every batch register must record, per output:

- stable component id and family;
- one and only one owner;
- source file and source bounds;
- normalised width, height and `[x, y]` offset;
- output cell dimensions and measured minimum gutter;
- source and output SHA-256 values;
- `ambiguousPixels: 0`, `unownedVisiblePixels: 0` and `edgeAlphaPixels: 0`.

The deterministic verifier rejects metadata/image geometry disagreement,
wrong hashes, visible shared-edge alpha, inadequate gutter, missing owners,
multiple owners, unowned fragments and inherited-byte drift.

## Naming and catalogue metadata

Component ids are stable lowercase kebab case:

```text
<family>-<specific-object-or-cue>
```

Examples are `bathroom-flush-handle`, `bbq-charcoal` and
`music-notation-treble-clef`. Use the semantic object, not an appearance such
as `blue-thing` or a batch position such as `sheet-2-cell-4`. Do not rename an
existing id; add a new immutable component if its meaning changes.

Each catalogue entry declares at least `src`, `sha256`, `family`,
`cellPixels: [256, 256]` and `sourceSet`. Source-set ancestry must be explicit,
so a new composer can inherit old tokens byte-for-byte without copying their
ownership.

## Recipe and story grammar

A normal package contains four or five ordered components. The first is the
hero read. Later elements support, transform or resolve it. Good phrases tell a
tiny story rather than showing five synonyms:

- **source → process → result:** pig, heat/pan, bacon;
- **ingredients → assembly → result:** bread, ham, lettuce, tomato, sandwich;
- **place/tool → action cue → outcome:** tank, food, fish, bubbles/clean water;
- **instrument → performer archetype → notation:** guitar, fictional rocker,
  musical marks.

The package declares a human-readable activity label, household-asset label,
stable asset id, body compatibility, ordered elements and optional named SFX.
Time-of-day or recipe variations belong in package metadata and selection
logic, not in the component pixels.

Body compatibility is explicit:

- `rear-work-with-context`: the approved generic rear-work body may be shown
  only when the real asset geometry and use point make the motion convincing;
- `dedicated-pose-required`: the vocabulary is valid but the generic body is
  automatically withheld until an appropriate body performance exists.

Vocabulary never proves body compatibility. A guitar, bath or loo package can
be useful before its dedicated Keeper pose exists.

SFX belongs to the contextual recipe, not the silent body and not the icon.
Asset-state sound, activity beat and completion sound must each have one owner.

## Animation and placement grammar

Until Frank selects one, every review presents both treatments equally:

- **open radial/orbit:** no enclosing bubble; objects travel through a raised,
  loose fan of arcs, flicks and swirls;
- **activity bustle/bubble:** a compact cloud/puff groups the same separately
  controlled objects.

The current phrase contract is 42 frames at 8 fps with five quiet tail frames.
One hero arrives first, supporting objects enter on staggered beats, components
travel through short readable arcs or bounces, and the phrase resolves before
the quiet tail. Do not display every object at once for the entire loop.
Reduced motion holds one primary and one secondary object with minimal marks.

The callout sits above the Keeper's cap with a verified clear gap, inside the
room safe zone, and moves to the clearer side if a wall, ceiling or UI would
clip it. It begins only after the work pose is reached and ends before the
turn-away. No review-only counter or foreground surface may be added. The real
household asset supplies context and owns its own effects.

The Prime rear-work body remains a separate 24-frame, 4 fps layer whose first,
23rd and 24th cells are the exact approved rear neutral. Walk, stop, turn,
rear-neutral and route authority bytes are never redrawn by a callout version.

Music packages may add the separate notation layer. The current grammar shows
three symbols in deterministic six-frame phrases using the `fnv1a32-v1` seed.
The notation layer can be disabled independently and is never baked into an
instrument, performer, album sleeve, body, asset or SFX.

## Required review controls

A review must let Frank independently:

- show or hide the Keeper body;
- show or hide the treatment/cloud marks;
- show or hide primary/resolved and supporting/story objects;
- switch open-radial and bustle/bubble presentations;
- switch deterministic music notation where applicable;
- mute SFX declarations;
- pause, replay and step the animation;
- inspect the tokens alone on a contrasting background;
- edit, reorder, import and export the four/five-element recipe.

All unique frame URLs must preload and decode before controls unlock or
playback starts.

## Acceptance and rejection checklist

Accept a new token only when all answers are yes:

- Does it look like the validated V2–V6 illustrated family at native game size?
- Is its subject unmistakable without a label?
- Does it retain a strong silhouette while moving and overlapping cloud marks?
- Is it one semantic owner with no stray or context pixels?
- Is the background genuinely transparent, with no halo or cast shadow?
- Does it pass alpha, gutter, ownership, geometry and SHA-256 verification?
- Is its exact prompt and accepted source hash recorded?
- Is it still independent of the Keeper, household asset, other tokens and SFX?
- Is its recipe storytelling clear in both callout treatments?
- Is body compatibility honestly classified?
- Is the old composer and every inherited authority unchanged?

Reject or rerender when any of these known failures appears:

- V1-style flat generic symbols that do not belong to the game;
- any source alpha crossing a source-cell ownership line;
- aura, haze or opaque glow around a symbol, as in the rejected smell attempts;
- a tight crop used to conceal source overlap;
- a foreground counter introduced only to hide body/contact problems;
- a callout low enough to collide visually with the cap;
- a contextual prop or icon baked into Keeper pixels;
- an attractive vocabulary package being used to imply that the generic body
  is suitable for its action;
- stochastic placement that cannot be replayed from the same recipe data.

## Immutable extension workflow

1. Read this standard, its JSON contract, the latest composer document and the
   general artwork playbook.
2. Create `activity-cloud-composer-<date>-vN` and a new Vn review route. Do not
   edit the previous version.
3. Copy catalogue metadata in code, inherit unchanged component URLs and
   hashes, and add only the new sources/components/recipes.
4. Generate and inspect source art; record every accepted and rejected attempt.
5. Run deterministic isolation; inspect every final 256 × 256 cell at native
   size and enlarged against light and dark backgrounds.
6. Add a version-specific builder and verifier. Pin all inherited bytes as well
   as the new ownership, gutter, timing and separation rules.
7. Build the immutable page, archive review media with
   `npm run archive:keeper-review`, then rerun the version verifier.
8. Browser-check preload/decode, both treatments, layer switches, dedicated
   body withholding, recipe import/export and deterministic replay.
9. Update the version document, README and decisions record. Run the relevant
   tests and the documentation audit.
10. Commit and push the review candidate without a `[deploy]` subject. Do not
    promote runtime/Final assets or deploy unless Frank explicitly requests it.

Rejection must remain recoverable by deleting only the new draft directory,
public page, archive set and new content-addressed objects. Never make rejection
depend on reconstructing an older version.

## Canonical worked evidence

- V2/V3 demonstrate the accepted visual move away from flat V1 symbols and the
  raised two-treatment phrase grammar.
- V5 `PROMPT_LOG.md` is the canonical ownership-safe 3 × 2 batch example. Five
  first passes crossed a declared line and were rerendered rather than cropped.
- V6 `PROMPT_LOG.md` is the canonical single-token example. Two smell attempts
  were rejected for haze; the accepted source was normalised into a measured
  20-pixel-gutter cell without repainting.
- Composer V6 is the current catalogue and recipe-interface evidence: 149
  independently selectable components, four/five-element packages, dedicated
  pose withholding and separate SFX/notation controls.
- Prime Rear Action Choreography V1 is the first richer-motion worked example:
  four explicit stories, independently authored open/bubble treatments,
  mobile object interactions, separate owned comic symbols, full/reduced
  42-frame data, path diagnostics and the required settled five-frame tail.

Run the stable contract check before extending the family:

```bash
npm run verify:activity-callout-authoring-standard
```
