# Prime Keeper back-work and activity-callout brief

**Status:** product direction captured and V1 review candidate built 19 October
2026; not approved, promoted or deployed. The implementation record is
`docs/KEEPER_PRIME_BACK_WORK_ACTIVITY_CALLOUT_V1_2026-10-19.md`.

**Review clarification, 19 October:** Claude's directional sketch is reference,
not an art or implementation authority. V1 therefore presents both a
bubble-free fan and a cloud/puff treatment as equal, separately switchable
review candidates. Neither is preferred or approved. The context proof places
its separate furniture layer behind the Keeper; no foreground occluder is
needed to conceal his hands.

## Why this is needed

The game needs one convincing back-to-camera work performance that can stand in
for many interactions at a counter, sink, appliance or work surface. The same
body motion should support turning on the kettle, preparing food, using a mixing
bowl, washing up and other lighthouse jobs without requiring a bespoke Keeper
animation for every object.

The repository already contains a production file named `keeper_work_back`, but
the Prime animation-bank audit classifies it as
`legacy-first-batch-non-prime-production` with motion salvage only. It is not an
approved Prime authority. A new candidate must therefore be derived from the
approved Prime rear identity and must not silently inherit the old sheet's body,
palette or endpoints.

The work performance alone cannot tell the player exactly what the Keeper is
doing while his hands are hidden. Every use of this generic performance should
therefore be paired with a separate, animated pictorial callout above him. This
is an **activity callout**, not dialogue and not the proposed wants/thought-
bubble system in `docs/EXPANSION_DESIGN.md`.

## Agreed design direction

### 1. One reusable rear-facing body performance

- The Keeper faces the work surface with both feet planted.
- Shoulders, elbows and upper torso provide the principal readable motion;
  small weight transfers and a slight head response stop the loop feeling
  mechanical.
- The hands work around one stable rear work-surface contact zone. They may be
  partly hidden by the foreground appliance, counter, sink or bowl.
- No kettle, bowl, pan, knife, tool, countertop, water or other contextual prop
  is baked into the Keeper strip.
- The loop should feel occupied and purposeful, but neutral enough that the
  callout and environmental asset determine whether it reads as cooking,
  washing, mixing, operating or repair.
- Entry and exit use the exact approved walk, phase-correct stop and turn
  authorities. The action receives and returns the exact approved direct-rear
  standing endpoint. It must not redraw, retime or replace those lower-body
  authorities.
- The first candidate is a versioned immutable draft. Existing raw, production
  and review files remain untouched, and rejection must require deleting only
  the new draft directory.

The legacy eight-frame, 4 fps `keeper_cook_back` is the choreography reference
for V1. `keeper_work_back` has identical historical pixels but is not the
semantic authority for this task. Neither clip is a pixel, anatomy, palette,
endpoint or timing authority.

### 2. A separate activity-callout layer

Review two original treatments above and slightly to one side of the Keeper's
head: a compact cartoon cloud/puff, and a bubble-free fan with a main icon,
outward helpers, swirls and flick marks. In both, small task icons appear
fleetingly and move with excited, legible energy: popping in, hopping, tilting,
crossing, orbiting briefly and vanishing. The result should suggest a flurry of
real activity hidden by the back-facing pose, rather than a static inventory
display. The directional Claude sketch is not a quality bar and contributes no
production art.

The visual grammar is:

1. A small puff or a few cloud marks establish the callout area.
2. One strong icon appears first and identifies the activity family.
3. One or two supporting icons enter in staggered beats; not every icon is
   shown at once.
4. Icons move through short arcs or bounces, with occasional emphasis marks,
   then disappear cleanly.
5. A brief quiet beat prevents a permanently busy halo before the phrase
   repeats or selects another authored phrase.

The animation should be lively rather than random noise. Its authored timing
must preserve silhouettes at normal iPad play size. It must not depend on text,
colour alone or very small detail to communicate meaning. A reduced-motion mode
can use the same puff with one stable primary icon and one secondary icon.

The callout is not baked into the Keeper or furniture. Each component remains
separately hashable, replaceable, layerable and rejectable:

- Prime rear-work Keeper strip;
- generic puff/emphasis effects;
- reusable icon sprites;
- an authored activity phrase that places and times those icons;
- contextual SFX cues;
- the appliance or work-surface art and its own state/effects.

All sprite-sheet icons, puffs and effects require transparent safety gutters in
every cell and deterministic checks for shared-edge alpha, ambiguous component
ownership and strip/metadata geometry.

### 3. Context recipes, not body variants

The actual recipe or asset state chooses the icon phrase and SFX. The callout is
presentation only; it must never decide whether an action succeeds, changes an
item's state or consumes an ingredient.

Initial vocabulary for review:

| Context | Primary read | Supporting icon ideas | Sound ownership |
|---|---|---|---|
| Turn on / prepare kettle | kettle | steam curl, cup, click mark | appliance click/boil belongs to the kettle recipe |
| Prepare or cook a meal | saucepan or frying pan | knife, spoon, ingredient shapes, heat marks | chopping/sizzle/clatter phrase selected by the meal recipe |
| Use mixing bowl | bowl and spoon/whisk | flour puff, egg or ingredient shapes | bowl/whisk/clink phrase selected by the recipe |
| Wash up | plate | sponge, bubbles, water drops, cutlery | water and crockery cues selected by the sink recipe |
| Generic repair | crossed hammer and spanner | screwdriver, nut/bolt, short dust puffs | tool taps/ratchet chosen by the repair recipe |

Knives and tools remain safely inside the callout; they never become implied
held props in the generic Keeper body strip. Icon sets may later become more
specific—for example, a fuse and screwdriver for electrical work—but the
generic repair phrase is the fallback whenever a repairable item's current
state is `broken` and no asset-specific repair phrase exists.

An asset-specific phrase takes priority over an activity-family phrase, which
takes priority over the generic repair fallback. A recipe may deliberately use
no callout only for an explicitly designed exception; ordinary uses of this
generic rear-work animation always provide one.

### 4. Audio contract

The Keeper body loop is silent. SFX are declared by the contextual activity
recipe so that a kettle can click and boil, washing can splash and clink, and a
repair can tap and ratchet without producing duplicate sounds from both the
actor and the asset.

Each cue should identify whether it is:

- an asset-state sound, such as boiling water;
- an authored activity beat, such as a knife chop or tool tap; or
- a completion/state-change sound.

Callout motion may share the timing of an activity beat, but should not add a
constant UI-like popping noise. The animation must also remain understandable
with audio muted.

### 5. Placement and layering

The recipe resolves the work surface's `usePoint` and an unclipped callout
anchor. Existing catalogue `bubbleOrigin` values may inform placement, but they
are not automatically authoritative for this larger animated cloud.

The V1 context proof uses room, rear-wall furniture, Keeper, local asset effects,
then activity callout. The Keeper's own back hides the hand-contact zone. No
review-only object is placed in front of him. The callout must remain inside the
room viewport and must move to the clearer side if a wall edge, ceiling or
nearby UI would clip it. Later asset-specific recipes may declare different
layering only when their real geometry requires it.

It starts only once the Keeper has reached the work pose, ends before he turns
away, and never follows him during the walk or turn. The environmental action
may continue afterward when appropriate—for example, the kettle may keep
boiling after the Keeper steps away.

## First review sequence

Build and approve this as separable gates rather than one irreversible batch:

1. **Prime body gate:** motion-only rear-work candidate in a complete approved
   walk/stop/turn/action/reverse-turn/walk context, plus isolated playback and
   Prime overlays. No activity icons or contextual prop can conceal body faults.
2. **Callout grammar gate:** the unchanged body candidate shown with three
   independently switchable phrases: cooking, mixing/washing, and generic
   repair. Review normal play size before enlargement.
3. **Context and audio gate:** demonstrate at least kettle, food preparation,
   washing up and broken-item repair with independent mute and layer controls.
4. **Contract gate:** add the validated data mapping, gutter/ownership checks,
   hashes and exact recovery/removal instructions. Promotion remains a separate
   explicit decision.

The first review must make it possible to hide the callout, hide the Keeper,
mute SFX and pause/step every layer independently. It must also show each icon
phrase on a plain contrasting background so transparent gutters and clipping
are visible.

## Acceptance criteria

- The Prime Keeper remains recognisably the approved direct-rear character at
  normal play size throughout the loop.
- Feet stay rooted; the trouser and jumper palette does not pulse; shoulder,
  elbow and hand motion has no sudden width or position snap.
- Entry and exit prove exact, measured seams to the approved rear neutral while
  preserving the approved walk and turn files byte-for-byte.
- The same Keeper bytes convincingly support all initial contexts.
- A player can identify each demonstrated activity from the callout alone in a
  muted review.
- Icons appear as a lively sequence, not a static cluster, but never become too
  small, frantic or numerous to read.
- Foreground object occlusion looks intentional and the callout never clips the
  room or UI.
- SFX ownership is singular and contextual; stopping or cancelling the action
  clears activity cues without cutting unrelated ambience.
- Every new frame is isolated inside its declared cell and every candidate and
  review artefact is content-addressed and immutable.

## Explicitly out of scope for the first candidate

- Runtime or production promotion.
- Replacing the approved walk, walk-stop or turn authorities.
- Building a unique body animation for each activity.
- Implementing wants, mood feedback, dialogue bubbles or the Numskulls panel.
- Completing the full lighthouse icon vocabulary.
- Changing gameplay duration, recipes, inventory, fault probability or repair
  success logic.

This brief is the durable starting point for a fresh, focused implementation
task. The art and motion should be reviewed before the wider recipe vocabulary
is expanded.
