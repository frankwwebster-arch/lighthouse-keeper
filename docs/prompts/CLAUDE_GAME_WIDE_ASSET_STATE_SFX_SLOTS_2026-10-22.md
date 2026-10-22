# Prompt for Claude — game-wide asset-state SFX slots

Continue Lighthouse Keeper from the newest `main` commit after Codex's Kitchen
Complete Review V46 delivery. Read `AGENTS.md`, `CLAUDE.md`, `README.md`,
`docs/RECIPES.md`, `src/game/config.ts`, `src/game/engine.ts`,
`src/ui/objectState.ts`, `src/ui/art.tsx`, `src/studio/SoundLibrary.tsx`,
`src/studio/store.ts` and `src/studio/audio.ts` before editing.

Frank wants an editable SFX slot for every real asset in the game, not only the
kitchen kettle. Claude owns this runtime/studio work. Build a typed,
data-driven asset-state sound contract and a simple grown-ups' editing surface
that reuses the existing sound library rather than inventing a second upload or
storage system.

## Product outcome

Every `OBJECTS` entry in `src/game/config.ts` must have named sound slots for
each supported visual/runtime state:

- `standard` (the normal/off/idle state);
- `on` (working/active state);
- `broken`;
- state transitions where they exist: `turn-on`, `turn-off`, `breakdown` and
  `repair`.

Do not manufacture meaningless continuous sounds. A slot may deliberately be
silent, but it must still exist in the contract and editor so Frank can fill it
later. `here` is not a real asset and must not receive slots. Keep `shop` and
`armchair` non-breakable unless an existing product decision changes that;
they still receive their supported Standard/On slots.

Use stable IDs derived from the object and state, for example:

```text
asset.fridge.standard
asset.fridge.on
asset.fridge.broken
asset.fridge.transition.breakdown
asset.fridge.transition.repair
```

Choose one canonical naming convention, document it, and provide a migration
map for current generic names such as `electronic-fizzle`,
`mechanical-clunk`, `plumbing-sputter` and `structure-crack`. Preserve current
behaviour while migrating; do not silently discard existing story/recipe cue
names.

## Reuse the existing sound library

The repository already has the right core interaction:

- `studio_sounds` persists named files;
- a named cue without a file is a placeholder blip;
- `SoundLibrary` accepts drag-and-drop or the file picker onto a placeholder;
- replacing a placeholder updates every consumer of that stable sound ID.

Extend that system. Do not create a parallel binary store, kitchen-only sound
library or hard-coded browser audio list. All new state slots should appear as
placeholders in the existing studio sound library even before any recipe uses
them. Frank must be able to unlock the studio, drag one audio file directly
onto a slot, preview it, replace it, or remove it back to a placeholder.

Add an “Asset state sounds” view/filter grouped by room, asset and state. It
should show every slot, its current file/placeholder status, a play button, and
the same drop/file-picker affordance already used by `SoundLibrary`. Keep the
ordinary recipe-sound workflow unchanged.

## Runtime contract

Implement one central resolver, not per-component special cases. It should
accept at least object ID, tier, visual state and transition/event, and return
the stable sound slot plus playback policy. The contract must support:

- one-shot and loop policies;
- volume and optional trim defaults without baking edits into audio files;
- state entry and state exit;
- immediate cancellation of the previous state's loop when an asset changes
  state, disappears, changes tier, is repaired, or the scene unmounts;
- no duplicate loop when React rerenders;
- multiple assets sounding independently;
- global audio/mute/accessibility preferences already present in the app;
- deterministic game state: audio failure must never affect simulation state,
  RNG, saves or activity timing.

`standard` should normally be silent unless Frank supplies a file and enables
its policy. `on` may loop while the object is active. `broken` may loop while
broken. `breakdown` and `repair` are one-shots. Repair must stop a Broken loop
and any queued Broken sound immediately before starting the repair cue.

The Codex V46 review establishes the intended presentation contract for broken
appliances: Off/Subtle/Emphatic motion is independent of SFX, environmental
effects keep their own anchors, and repair synchronously stops motion and
sound. Do not copy V46's review-only Web Audio implementation into runtime;
use the shared sound library and runtime audio service.

## Coverage and compatibility

Generate default slot declarations from `OBJECTS`, then allow explicit
per-object overrides. Cover all current real assets:

`door`, `fridge`, `cooker`, `broom`, `petbowl`, `tv`, `bookshelf`, `piano`,
`armchair`, `bed`, `phone`, `desk`, `basin`, `toilet`, `telescope`, `lamp`,
`garden`, `shop`, `jetty`, `tank`, `fishfood`, `barometer`, `radio`, `console`
and `gadgets`.

Do not conflate story SFX ownership (`data/activity-stories/**`) with ambient
asset-state sound. A story may trigger the same stable slot, but the asset
state system owns state-loop start/stop semantics. Keep recipe cue behaviour
and `sfxCues` backward compatible.

## Tests and acceptance

Add focused unit/component tests proving:

1. every real `OBJECTS` entry has all required supported slots and `here` does
   not;
2. every slot ID is unique and stable;
3. unresolved slots use the existing placeholder path;
4. dropping a file on a named slot stores it under that exact ID and all
   consumers resolve it;
5. Standard → On starts the On sound once; rerender does not duplicate it;
6. On → Broken stops On before starting Breakdown/Broken;
7. Broken → Standard/On repair stops Broken synchronously, then plays Repair;
8. unmount, tier replacement and object removal stop active loops;
9. two active assets do not stop each other's sound;
10. audio load/decode/play failure leaves game state and saves unchanged;
11. existing recipe and Bubble-story sound tests remain green.

Run `npm test`, `npm run typecheck` and `npm run build`. Update README,
`docs/RECIPES.md`, current status/decision documents and any schema reference.
Perform the mandatory documentation audit. Commit, push to remote `main`, and
release once with `npm run deploy -- "game-wide asset-state SFX slots"` only
after all checks pass. Verify the deployed Studio flow with Frank's personal
Chrome profile: placeholder visible, drag/drop replacement persists, preview
works, and repair stops a Broken loop immediately.

Do not alter or promote visual art. Kitchen Kettle Bubble Authority V47 is the
approved, hash-pinned visual authority but remains unpromoted and unwired; its
new configurable vibration/SFX presentation in Kitchen Complete Review V46 is
still review-only. Do not rewrite Codex's immutable review packs. The task is
runtime/studio sound infrastructure and its documented contract.
