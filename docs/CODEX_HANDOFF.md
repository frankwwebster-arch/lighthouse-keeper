# Lighthouse Keeper — handoff decisions

> **Current cross-agent handoff:** this 8 October decision record remains useful
> history. For current Keeper Prime authorities, Timing Lab state, next gates
> and Claude's furniture/locomotion architecture task, read
> [`CODEX_TO_CLAUDE_HANDOFF_2026-10-14.md`](CODEX_TO_CLAUDE_HANDOFF_2026-10-14.md)
> first.

Date: 2026-10-08

This note records the decisions made in the visual-design conversation so implementation can continue without relying on chat history.

> **26 October supersession for whole-island establishing art:** the Day 1
> four-floor statement below is historical. The current establishing-shot
> brief uses two enclosed Day 1 floors (kitchen and bedroom/en-suite) plus the
> lamp room, and a 20-floor, three-module expanded tower. Door, geometry and
> draft-status details are in
> [`LIGHTHOUSE_ESTABLISHING_SHOTS_2026-10-26.md`](LIGHTHOUSE_ESTABLISHING_SHOTS_2026-10-26.md).

## Visual direction

- Use the Pixel direction as the primary style.
- The game is flat, front-on 2D cutaway art, not isometric and not full 3D.
- Use a consistent 4 px logical pixel grid, crisp nearest-neighbour scaling, saturated colours, dark pixel outlines, and simple faces.
- The lighthouse is the visual anchor: classic alternating red-and-white exterior stripes.
- The keeper is the main animation challenge. The old modular layered parts are rejected as final review art; production uses full animation strips measured against the approved walk's skull, shoulder, hip, core-width and sole landmarks. Cooking, brushing teeth, and similar actions can often show his back with small arm/body movements rather than requiring bespoke front-facing animation.

## Interior item states

Every clickable interior object uses one shared state contract:

- `standard`: static idle appearance.
- `on`: active/use state, animated.
- `broken`: faulty state, animated.

Broken objects share a visual grammar: gentle casing wobble, looping smoke, and occasional sparks. Add only a small object-specific cue when helpful. The Pixel TV test is in `style_b_pixel/obj_tv_states_sheet.png` with separate AI-generated state crops beside it.

## Lighthouse expansion

- Day 1 begins with four floors, bottom to top: kitchen, living room, bedroom with en suite, and lamp room.
- The lighthouse can expand upward and downward. It does not need to be realistic.
- The lamp room must always remain at the top.
- The main gameplay shaft uses one active standard-room width per floor and never tapers. The delivered first-generation assets are 110 × 35; the agreed replacement initial target is 172 × 56, with later whole-lighthouse tiers of 193 and 214. Any apparent taper is decorative exterior shading only. The lamp room is inset/fixed-width, with a wraparound rail and outdoor walkway. See `KEEPER_ROOM_GRID_172_HANDOFF_2026-10-14.md`.
- Future standard-floor progression is deliberately non-linear. Keep kitchen at the base, lamp room topmost and bedroom directly below it; give every other eligible floor a one-time random middle-stack position and persist the resulting order. Do not pre-assign future room types to heights or let concept-art taper dictate their order. Derive stripe phase from world Y.
- New floors can slide into place or materialise in a large puff of smoke. Reuse one arrival animation for all new floors.
- New floors must continue the alternating exterior stripe pattern. Calculate stripe phase from world/floor position so inserted floors align automatically.
- Underground expansion should be a surprise. Day 1 must show ordinary grass, soil, and rock only—not an obvious empty basement, shaft, cave, or reserved development space. When the Batcave-style lair unlocks, reveal it by extending the underground surface downward.
- Once the lighthouse exceeds roughly six floors, unlock a lift so inter-floor travel does not become tedious.
- At maximum height, a possible late-game gag is the keeper parachuting from the lamp-room roof.

## Night / day transition

- At the end of the day, the lighthouse closes up completely.
- The camera zooms out to show the whole lighthouse while the keeper sleeps.
- Night lasts approximately 30 seconds and presents a carefully readable daily recap/statistics sequence. It is intentionally not skippable because it is part of the learning experience.
- Energy restoration depends on bed quality: basic 80%, upgraded 90%, master 100%.
- The background should support a reusable day/night treatment rather than requiring a wholly separate world layout.

## New mechanic

The telescope in the lamp room is a dedicated spotting mini-game. It should be treated as a future feature, not decorative furniture: telescope use can zoom the camera, present a scanning/search interaction, and reward spotting ships, visitors, weather events, wildlife, or other distant targets.

## Background asset

The current master concept is:

- `art/background/lighthouse_master_day_pixel.png`

It is designed as a crop-safe master plate: calm expandable sky above, a clean grass/soil/rock boundary below, and no visible underground promise. It contains the four starting floors, the inset fixed-width lamp room, outdoor walkway rail, garden, shop hut, jetty, and sea. The shop hut is now historical concept material only: the canonical shop will be off-island and reached by boat.

## Next implementation priorities

Completed in the first implementation slice:

- Fixed-width modular kitchen, living-room, and bedroom/en-suite runtime bands.
- Shared `standard` / `on` / `broken` object renderer, broken-effect grammar, and horizontal strip playback.
- Rear-facing fallback pose for cooker and basin work.
- Reserved hidden changing-room geometry currently sits on Floor 3 as an interim implementation; the later extension must move with the bedroom beneath the lamp room.
- Browser verification at desktop and 1024 × 768 iPad sizes.
- First production Pixel batch: red/white shell bands and kitchen, living-room, and bedroom/en-suite plates, integrated through `npm run sprites`.
- Seeded keeper-owned breakdown and repair gameplay; the off-island shop remains excluded from faults.

Next priorities:

1. Review delivery-order item 2 in `docs/floor-asset-catalogue/review.html`, then use `docs/keeper-scale-audit/review.html` for the 173 accepted keeper animations and their walk/action seams. Frank's immutable second review recorded 96 Happy, 68 Awaiting new draft review, 3 Review later and 6 Unreviewed; the current reviewer has 97 Happy and 67 Awaiting after the retained Darts draft was selected as preferred. Use the compact animation-first gallery and its `Open close review` action; independently filter status, pose and active/reserve list, and Previous/Next stays inside the full selected filter set. Close review retains Codex response, canonical/draft comparison, compressible retained drafts, an exportable preferred-promotion selector, pose override and reversible reserve control. Obsolete modular/reference art remains hidden.
2. Use `data/keeper_asset_contract.json` and `data/keeper_object_dimensions.json` as the authority for all new object scale, keeper pivots and interaction heights. The current 1,479-frame original-comparison record and fixed-scale transition viewer are in `docs/keeper-scale-audit/`; the 191-sheet audit must be rerun for every keeper delivery and must report zero failures.
   Multi-frame keeper clips use 4fps by default. Accepted per-clip overrides
   from 1fps to 10.5fps live in `KEEPER_FPS_OVERRIDES`, each source sidecar and
   the runtime manifest.
3. For any keeper-animation continuation, read `docs/KEEPER_ANIMATION_HANDOFF.md` and `docs/KEEPER_COSTUME_ROUTE_AUDIT.md` first. They record the exact 173-clip transition classification, the immutable dated review/resolution records, scuba jetty/dive/swim and parachute jump/drift/landing routes, seated nap, mower shed-occlusion route, three-tier cleaning cupboard route, artist-smock route, guitar prop handoffs and remaining outfit bridge backlog. Read the latest **Hand back to Codex** queue entry before proposing any changes. Its `changedAnimationNames` is the authoritative semantic delta (save timestamps are ignored): the first server batch compares with the shipped review baseline and later ones with the preceding handoff. Inspect and act only on those exact records unless Frank separately asks for a full re-audit. The complete snapshot remains available for recovery. Beard length and its ragged side silhouette are identity-locked and must be checked frame by frame.
   Before opening any mutable art or metadata file, claim the exact queued handoff with `PATCH /api/keeper-review-handoffs` and `{ "id": "<handoff id>", "action": "claim", "note": "<short task description>" }`. This locks the online reviewer’s feedback-changing controls. After the amended delivery is committed, pushed and deployed, call the same endpoint with `action: "complete"`; only use `action: "release"` if no amendments were started and the note explains why. Never work from an unclaimed handoff.
4. The next distinct reviewer build is specified in `docs/prompts/KEEPER_REVIEW_WORKBENCH_BUILD.md`. It extends this project’s reviewer to rooms, furniture, annotations, crop/anchor proposals, new-animation requests, routine/trigger relationships and scene context preview. It must remain draft-first and defer generic multi-project productisation until the Keeper workbench is proven.
   Width and height each have precise −0.5%/+0.5% buttons beside their slider;
   both inputs update the same saved and exported values.
   Rotation, horizontal/vertical position and opacity likewise have precise
   −0.5/+0.5 buttons in degrees, logical pixels and percentage points.
   The frame controls can play only the reviewed card once or in a loop; that
   playback mode is inspection state and is not exported as production feedback.
4. Add a day/night palette or overlay system and the proper roughly 30-second recap.
5. Design future floor missions so eligible standard floors can unlock in different orders; do not hard-code a linear room sequence.
6. Leave aquarium, weather station, lair, lift, pets, visitors, ship and weather art until the later batch is authorised.
