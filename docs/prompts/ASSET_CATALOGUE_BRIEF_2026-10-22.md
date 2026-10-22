# Asset Catalogue and Audit tool: Frank's brief (22 Oct 2026)

Frank pasted this brief to Claude on 22 October 2026 (it was written for the
copy of the repo at `~/Documents/ChatGPT/Lighthouse Keeper`, which is Codex's
desk; Claude works in `~/Projects/lighthouse-keeper`, the same GitHub repo).
It is kept here verbatim below the line. **Frank's later answers change parts
of it; where they differ, the answers win:**

- **Phasing (preflight, AMBER → GREEN):** three phases. (1) Bubble catalogue,
  inspector with 64 px preview and every version, automatic checks, scored
  audits, Frank's editable note. (2) Redraft queue and agent API/CLI.
  (3) Kitchen register and the Rooms section. Each phase ends tested and
  documented.
- **ac1:** Claude's half of the repo tidy-up first (one ownership file both
  agents read, a check that flags unsaved leftovers, remove the superseded
  `claude/bubble-choreography-test` branch), then Phase 1. Codex saves its own
  loose ends with the housekeeping prompt on the project page.
- **ac2: release each phase** to the live site (`npm run deploy`), overriding
  the brief's "do not deploy".
- **ac3:** Codex fills in the kitchen register in a format Claude sets; Claude
  checks it against the records and builds the Rooms pages.
- **ac4:** score every asset, not just those the stories use.
- **ac5 (Frank's note, overrides the redraft workflow below):** no redraw ever
  happens by itself. Claude and Codex each score every asset independently
  (Bubble pictures and room furniture are separate libraries), without seeing
  each other's score first. Each asset gets a traffic light (green fine, amber
  worth a look, red = recommended redraw). Frank reviews and ticks which to
  redraw; his ticklist is what sends work to Codex. A redraw becomes current
  only when Frank accepts it.
- **No redraw-everything pass (22 Oct):** the scoring sweep, not a conversion
  programme, decides what Codex redraws. Codex's pause
  (`data/activity-stories/catalogue-closure-2026-10-22.json`) stands.
- Claude's 21 Oct coarse verdicts (`data/activity-stories/style-review.json`)
  stay visible as an earlier, rougher check; they are not turned into scores.

---

Build a permanent Asset Catalogue and Audit tool inside the Lighthouse Keeper Grown-ups Studio. This must be part of the real game/studio application, not a standalone Claude/Codex review artefact.

Start by reading:

- AGENTS.md
- CLAUDE.md
- README.md
- docs/RECIPES.md
- data/activity-stories/README.md
- docs/CODEX_PROMPT_BUBBLE_STORIES_LIGNE_CLAIRE_ACTION_IMAGERY_2026-10-21.md
- src/activityStories/StoryStudio.tsx
- src/activityStories/format.ts
- src/activityStories/store.ts
- data/activity-stories/pictures.json
- data/activity-stories/style-review.json
- the current kitchen manifests, registers and approval records

Preserve all current artwork, stable IDs, immutable versions, stories, recipes, runtime behaviour and saved user data.

## Product objective

Create one shared Asset Catalogue with two sections:

1. Bubble pictures
2. Lighthouse room assets

It must let Frank, Claude and Codex inspect, audit and manage the artwork consistently throughout the project.

The existing Bubble Story Studio already has a categorised picture library, immutable versions, a large-image viewer and a coarse style verdict. Extend and reuse that foundation. Do not create a disconnected review page.

## Routes and navigation

Add permanent Studio routes such as:

- /studio/assets
- /studio/assets/bubbles
- /studio/assets/rooms

Add clear links from:

- /studio
- /studio/stories

The interface is a Grown-ups authoring tool, not a player-facing game screen.

## Bubble-asset catalogue

Show one cell for every Bubble picture in the current catalogue. Do not hardcode the catalogue count.

Group cells using the existing Bubble picture categories. Preserve the special distinction between object assets and mark/effect assets.

Every cell must show:

- thumbnail;
- human-readable label;
- stable asset ID;
- current immutable version;
- total number of versions;
- object or mark classification;
- category/family;
- every Bubble story using it;
- current audit percentage;
- current audit state;
- redraft state, if applicable.

Story names must be clickable and open the corresponding story in /studio/stories.

Calculate story usage from both repository drafts and Frank's currently saved Studio versions. Show the exact uses inside each story where practical:

- cast member;
- hero or support role;
- prop;
- ambient mark;
- appearance mark;
- step mark;
- relevant step numbers.

## Search and filtering

Support filtering by:

- text, label or ID;
- category;
- object versus mark;
- story;
- audit state;
- percentage range;
- current versus superseded version;
- needs redraft;
- unaudited;
- audit made stale by a newer version;
- Bubble assets that incorrectly contain detachable notation.

## Asset inspector

Clicking a cell must open a proper inspector containing:

- a large view of the asset;
- a literal 64 × 64 preview;
- checkerboard, light and dark backgrounds;
- current version and all immutable earlier versions;
- version dates and provenance notes;
- stories and exact roles using the asset;
- technical validation results;
- Claude and Codex audit results;
- Frank's editable canonical audit note;
- Frank's additional redraft direction;
- redraft controls and history.

Earlier versions must remain selectable and viewable. Never overwrite an existing version.

## Audit standard

The audit must use a versioned standard rather than a free-form impression.

Create a named and versioned Bubble asset standard based on the following binding brief:

### BUBBLE-STORY LIGNE-CLAIRE ASSET STANDARD

Translate the supplied Bubble-story asset into restrained, observational ligne claire while preserving exactly what the asset depicts.

Preserve:

- identity and purpose;
- object and component count;
- viewpoint and orientation;
- practical construction and topology;
- state and recognisable contents;
- relative arrangement and overlap order;
- broad silhouette.

Change the drawing language, not the subject. Do not add, remove, substitute or rearrange meaningful parts unless Frank explicitly directs it.

Drawing rules:

1. Use one even black outline weight throughout.
2. Draw a line only where there is a real edge, construction seam or indispensable identifying mark.
3. No hatching, stippling, texture strokes, sketch doubling, distress marks or decorative contour accents.
4. Every enclosed area has one uniform flat opaque colour.
5. No gradients, shine, gloss, specular highlights, reflection bands, luminous rims, glow, bloom, airbrushing, bevels or painterly modelling.
6. At most one additional flat shadow tone may be used, rarely and only when essential.
7. Show the object's own local colours under neutral, even daylight.
8. Black is used only for the even outlines and parts that are genuinely black or genuinely dark openings.
9. Objects must have credible adult proportions, mechanisms, materials, joins and weight, like accurately observed ligne-claire cars, tools and machines.
10. Simplify by leaving unnecessary detail out. Never simplify by making the object cute, inflated, toy-like, caricatured, mascot-like, emoji-like or sticker-like.
11. Small controlled hand-drawn irregularities are allowed only when they do not damage construction, contact logic, identity or readability.
12. The object must remain immediately identifiable at 64 × 64 pixels.

### Isolation of action and reaction notation

An ordinary object asset must contain only its static object or semantic subject.

It must not contain detachable:

- action or motion slashes;
- speed lines;
- impact ticks, bursts or stars;
- exertion marks;
- surprise, anger or alarm marks;
- exclamation or question symbols;
- sparkles or glints;
- droplets or splashes;
- dust or debris;
- steam, smoke or heat curls;
- aroma or odour lines;
- sparks, electrical arcs or welding effects;
- shaking, vibration or dizziness marks;
- any other free-standing comic punctuation.

These belong in separate transparent mark/effect assets so the story engine can position, animate, move and remove them independently.

If the catalogue entry is itself explicitly a mark/effect asset, it must contain only that isolated mark. It must not include the object, Keeper or scenery to which it may later be attached.

### Technical output contract

- 256 × 256 RGBA PNG unless an existing explicitly documented class requires otherwise;
- genuine transparent background;
- one semantic owner;
- at least 16 px transparent gutter, targeting 20 px;
- no scenery, room, floor, panel, tile or cast shadow;
- no text, lettering, number, logo or watermark;
- no pixels touching the canvas edge;
- independently usable by the Bubble-story compositor.

## Scoring model

Do not let an auditor type an arbitrary overall percentage.

Record each criterion as:

- pass;
- partial;
- fail;
- not applicable, only where genuinely justified.

Calculate the percentage from weighted criteria. Use this initial 100-point weighting:

- exact subject/identity/count preservation: 10
- topology, state, viewpoint and silhouette preservation: 8
- one consistent black line weight: 10
- lines only at real edges or indispensable marks: 8
- closed areas and uniform flat fills: 10
- no gradients, shine, glow, texture or painted modelling: 10
- correct local colour and correct use of black: 8
- accurate adult construction and proportions: 10
- simplification by omission rather than cuteness: 6
- clarity at 64 px: 8
- no embedded detachable action/reaction notation: 8
- transparency, gutter, ownership and technical contract: 4

Pass earns the full criterion weight, partial earns half and fail earns zero. Exclude a criterion from the denominator only when marked not applicable with a written reason.

The tool must display:

- calculated success percentage;
- pass/partial/fail result for every criterion;
- one concise overall explanation;
- a short explanation for every partial or failed criterion;
- auditor identity;
- asset ID and exact immutable version;
- audit-standard version;
- audit date;
- whether the audit is current or stale.

## Version-aware audits

Audits belong to:

- an asset ID;
- an exact immutable asset version;
- an exact audit-standard version;
- an auditor.

A new current asset version must not inherit a passing score automatically. It must show as unaudited while retaining all earlier audits as history.

If the audit standard changes, earlier audits remain visible but become stale against the new standard.

Claude and Codex must not overwrite one another's audits. If both inspect the same version, retain both audit records.

## Frank's editable notes

Frank must be able to edit the AI-generated audit explanation.

Provide:

- an editable canonical note;
- a separate optional "Frank's redraft direction" field;
- autosave or an explicit reliable Save action;
- visible saved/unsaved state;
- durable shared persistence.

Keep revision history behind the editable note so Frank's edit becomes authoritative without destroying the original Claude or Codex wording.

## Redraft workflow

Add a "Request redraft" action.

A redraft request must include:

- asset ID;
- exact current version;
- current image URL;
- failed and partial criteria;
- calculated score;
- canonical editable note;
- Frank's additional direction;
- stories affected;
- requested agent, if selected;
- creation and update timestamps.

Support these states:

- requested;
- claimed;
- drafting;
- ready for review;
- accepted;
- rejected;
- cancelled.

Claude and Codex must be able to list and claim redraft requests.

Accepting a redraft must register a new immutable asset version through the established picture workflow. Never replace, mutate or delete the prior image.

## Agent access

Claude and Codex need both web access and a machine-readable interface.

Provide documented API and CLI support along the lines of:

```
npm run asset-audits -- list bubbles --status unaudited
npm run asset-audits -- list bubbles --status needs-redraft
npm run asset-audits -- show <asset-id>
npm run asset-audits -- claim <asset-id> --version <n> --by claude
npm run asset-audits -- record <asset-id> --version <n> --by codex --file <audit.json>
npm run asset-audits -- redrafts
npm run asset-audits -- export
```

Exact command design may vary, but it must be straightforward for both agents to:

- enumerate assets;
- locate unaudited current versions;
- inspect the standard and existing notes;
- submit structured audit results;
- find requested redrafts;
- claim work without silently clobbering another agent;
- report a completed immutable replacement.

Validate all API and CLI writes on the server. Do not trust arbitrary client JSON.

## Persistence

Use durable shared server-side persistence. Browser-local storage is not sufficient when the production database is available.

Reuse the existing Studio persistence architecture where appropriate, or add dedicated validated tables/endpoints if that produces a safer model.

Preserve:

- authorship;
- timestamps;
- asset and standard versions;
- audit history;
- note revision history;
- redraft history.

The tool must fail safely if the database is unavailable and clearly report that changes are local or unsaved.

## Room-asset catalogue

Build a second section using the same reusable catalogue, inspector, audit, note and redraft framework:

/studio/assets/rooms

Organise assets by room. Begin with Kitchen.

The intended hierarchy is:

```
Kitchen
  Fitted cabinetry
  Sink and taps
  Oven
  Fridge
  Dishwasher
  Kettle
  Toaster
  Bin
  Table and chairs
  Mixing bowls and preparation objects
  Other props
  Separate effects and animated states
```

Each room-asset cell must show:

- room;
- family;
- stable asset/state ID;
- fixture, furniture, appliance, prop or effect classification;
- current version;
- thumbnail;
- production, approved, candidate, review-only or retired status;
- associated states;
- recipes/interactions using it;
- audit score and state;
- redraft state.

The room inspector should also show, where applicable:

- normal, open, active, broken and repaired states;
- interaction datum;
- floor/contact registration;
- scale;
- state-to-state continuity;
- separately owned effects;
- related review and approval provenance;
- whether it is actually wired into the room/runtime.

## Authoritative kitchen registry

The current kitchen assets are distributed across many immutable manifests, batch registers, approval records and review packs.

Create one authoritative repository-controlled kitchen catalogue that references those existing records without altering their bytes.

Do not assume the newest-looking draft is approved or canonical. Determine status from approval evidence, runtime references, manifests and documentation.

The registry must distinguish clearly between:

- production/current;
- explicitly approved but not yet promoted;
- candidate;
- superseded;
- rejected;
- review-only;
- effect-only.

Do not import every historical review composite as though it were a standalone game asset. Catalogue semantic assets and states, with provenance links to their supporting review records.

## Room audit profile

Reuse the visual ligne-claire rules where applicable, but add room-asset checks for:

- correct physical construction;
- correct room scale;
- correct floor/contact registration;
- interaction-datum accuracy;
- compatibility with neighbouring fitted assets;
- state continuity;
- no baked-in detachable effects;
- correct separation of fixture, movable object and effect layers;
- runtime wiring and status accurately reported.

Keep audit profiles versioned so Bubble assets and room assets can use related but distinct standards.

## Automated validation

Add deterministic checks where possible, including:

- referenced files exist;
- version IDs are unique and monotonic;
- every asset has exactly one category;
- every room asset has exactly one room and semantic family;
- PNG dimensions and RGBA mode;
- transparent background;
- no opaque pixels touching an edge;
- minimum transparent gutter;
- no missing story references;
- no missing room/recipe references;
- audit totals calculate correctly;
- new versions make prior current-version audits stale;
- redraft history cannot mutate immutable versions;
- note revisions preserve authorship and history;
- API rejects malformed audit submissions.

Automated image checks may flag possible gradients or excessive colour ramps, but must not pretend they can conclusively judge visual style. Keep visual verdicts explicit and attributable.

## Tests and acceptance

Add unit, integration and UI tests appropriate to the existing project.

At minimum verify:

- every current Bubble picture appears exactly once;
- story cross-references are correct;
- clicking an asset opens the inspector;
- 64 px preview is available;
- all immutable versions remain selectable;
- audit score calculation is deterministic;
- stale-audit behaviour works;
- Claude and Codex audit records do not overwrite one another;
- Frank can edit the canonical note and its history survives;
- redraft requests persist and transition safely;
- room filtering works;
- the kitchen registry is complete and internally valid;
- no existing story creation, editing, saving, playback or animation behaviour regresses.

Use existing project styling so the catalogue feels native to the Studio. It must remain usable with hundreds of assets and on an ordinary laptop screen.

## Build order

Implement in this order:

1. Shared catalogue/audit domain model.
2. Bubble asset catalogue and story cross-references.
3. Inspector, 64 px preview and immutable version browser.
4. Durable structured audits and calculated percentages.
5. Frank's editable canonical notes with revision history.
6. Redraft queue and agent-facing API/CLI.
7. Authoritative kitchen asset registry.
8. Room-assets UI using the shared catalogue framework.
9. Tests, documentation and final verification.

## Boundaries

- Do not redraw or modify artwork as part of this task.
- Do not promote candidate kitchen art.
- Do not alter existing image bytes.
- Do not remove immutable versions.
- Do not change existing Bubble story behaviour.
- Do not bake marks or effects into object assets.
- Do not create a disposable /keeper-review page instead of the Studio feature.
- Do not hardcode current catalogue counts.
- Preserve unrelated working-tree changes.

## Delivery

Before handoff:

- run focused tests during implementation;
- run the full relevant test suite;
- test the tool against the actual catalogue;
- verify the production build;
- update README.md, data/activity-stories/README.md, docs/RECIPES.md and any new architecture/operations documentation;
- document the audit standard, data schema, CLI commands, recovery behaviour and how Claude/Codex should use the queue;
- perform the mandatory documentation audit;
- commit the completed work;
- push the finished commit to remote main.

Deployment is manual in this repository. Do not run `npm run deploy` and do not create a commit whose subject ends in `[deploy]` unless Frank explicitly asks for production deployment. *(Frank's ac2 answer asks for a release at the end of each phase.)*

At handoff, report:

- routes added;
- number of Bubble assets and versions discovered dynamically;
- number of kitchen semantic assets/states registered;
- persistence model;
- tests run and results;
- documentation updated;
- final commit hash;
- whether production was deliberately left undeployed.
