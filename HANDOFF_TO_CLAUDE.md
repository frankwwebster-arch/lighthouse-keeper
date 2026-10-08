# Lighthouse Keeper — implementation handoff report

Date: 2026-10-08
Status: the first three runtime floor modules and three-state rendering contract are implemented. The first production Pixel batch now supplies two shell bands and three room plates; all previously supplied PNGs remain **prototype/concept art**, not production sprites.

This report answers the implementation questions raised for the Next.js 14 / React build. Facts about delivered files are separated from recommendations so the game is not accidentally built around a placeholder.

## Implementation update

- `src/ui/floors.tsx` now renders fixed-width modular kitchen, living-room, and bedroom/en-suite bands. `src/game/config.ts` uses integer 4× coordinates and places the toilet on Floor 3.
- `src/ui/art.tsx` implements `standard`, `on`, and `broken`; broken uses a shared integer-step casing wobble, smoke, and sparks. `?broken=<ids>` is the internal browser preview.
- `src/ui/Sprite.tsx` supports horizontal strips through `{ "file", "frames", "fps" }` manifest entries while retaining compatibility with old string paths.
- Cooker and basin activities use the named production rear-work aliases. The wider keeper set is exported and reviewable; most newer clips remain unwired until their matching world mechanics exist.
- The seeded breakdown/repair loop is playable. Grown-ups can set average game-minutes between faults and the maximum concurrent faults; both zero values disable faults. Broken objects reject normal actions and expose a 25-game-minute repair action. The event stream carries placeholder SFX categories, but no audio engine/files are delivered.
- The shop is explicitly excluded from keeper-owned faults. Its current on-island placement is a temporary gameplay fallback; the agreed later route is keeper jetty → upgradeable rowing boat/tug/speedboat → off-island shop. The keeper's jetty, garden/greenhouse, and future boat may break. A future workshop floor reduces fault pressure.
- The exact current asset contract is [docs/CODEX_BRIEF.md](docs/CODEX_BRIEF.md), with production details in [docs/PRODUCTION_ASSET_KIT.md](docs/PRODUCTION_ASSET_KIT.md).
- Delivery-order item 1 is integrated: two 110 × 8 shell stripe tiles and three 105 × 35 room plates. Untouched generated sources and prompts live in `art/source/first-production-batch/`; the existing concept pack remains reference-only.

## 1. Files, format, naming and scale

1. The selected visual direction is Pixel. `style_a_blocky/` is an archived rejected direction; do not ship or extend it.
2. The machine-readable file inventory is [art/asset_inventory.json](art/asset_inventory.json). It lists every PNG currently delivered, with exact path, pixel dimensions, colour mode, alpha-channel presence, and broad type. It is the source of truth for current file facts.
3. The small runtime-facing mapping is [art/manifest.json](art/manifest.json). It lists the current concept/placeholder asset keys and explicitly records what is not delivered. It is JSON-valid, but it is intentionally not yet a final production manifest.
4. Important existing files are:

   | Purpose | Path | Exact pixels / alpha | Status |
   |---|---|---:|---|
   | First production batch | `public/sprites/tower_stripe_{red,white}.png`, `room_{kitchen,living,bedroom}.png` | 110 × 8 and 105 × 35, RGBA | Production, integrated |
   | Day 1 master plate | `art/background/lighthouse_master_day_pixel.png` | 1576 x 998, opaque RGB | Concept plate |
   | 10-floor tower study | `art/background/lighthouse_10_floors_pixel.png` | 1254 x 1254, opaque RGB | Concept plate |
   | Wide 10-floor/lift study | `art/background/lighthouse_10_floors_wide_pixel.png` | 1254 x 1254, opaque RGB | Concept plate |
   | Island wall-push study | `art/background/lighthouse_expansion_island_split_pixel.png` | 1774 x 887, opaque RGB | Concept plate |
   | TV three-state sheet | `style_b_pixel/obj_tv_states_sheet.png` | 2172 x 724, RGBA | Visual reference; not a sprite strip |
   | TV crops | `style_b_pixel/obj_tv_{standard,on,broken}_ai.png` | 724 x 724 each, RGBA | Visual reference; not animation-ready |
   | Keeper/cat/object PNGs | `style_b_pixel/**` | See inventory | Mixed placeholders/concepts |

5. There are no layered source files (PSD, Aseprite, ORA) and no authoritative animation strips. Existing “parts” are placeholder PNGs and cannot be assumed to share pivots, scale, silhouette, palette, or z-order.
6. Recommended production coordinate system: a **300 x 190 logical-pixel stage**, rendered at exactly **4 CSS pixels per logical pixel** (1200 x 760 at normal scale) with `image-rendering: pixelated`. Produce final sprite sources at one logical pixel per source pixel. Existing concept PNGs are not consistently authored to that rule and must not define production dimensions.
7. Production naming contract:

   ```text
   keeper_front_<part>_<variant>.png
   keeper_back_<part>.png
   keeper_reference.png
   obj_<id>_<state>_f<frames>.png
   obj_<id>_t<tier>_<state>_f<frames>.png
   room_<type>.png
   fx_<name>_f<frames>.png
   bubble_<emotion>_f<frames>.png
   ```

   Frames sit left-to-right in one strip. Tier 1 has no suffix; later tiers use `_t2` and onward. Keep the manifest mapping gameplay IDs to file, frame count, fps, anchor, use point, effect origin, bubble origin, and z-order.
8. Current art total is roughly 14.7 MiB of file payload (around 32 MiB allocated on disk). Do not atlas the opaque full-scene concept plates. For production, use separate 2048 x 2048-or-smaller atlases by category: keeper, objects, effects/UI, NPCs, and floor/world modules.

## 2. Lighthouse keeper: rig and animation bible

1. **Delivered fact:** a 48-export production keeper set now exists under `art/raw/keeper-first-batch/` and `public/sprites/`, with aligned parts, front/rear/side action strips, manifest metadata and review GIFs. `data/keeper_asset_contract.json` is the scale and interaction authority.
2. **Locked production contract:** every keeper part uses the same 32 x 40 canvas; the measured standing reference is 24.75 x 38.25 logical pixels and the floor anchor is `(16, 40)`. Airborne actions may use 48 x 56 for the vertical dive or 48 x 84 for parachute deployment, but never rescale the character.
3. Required production parts:

   | Part | Pivot recommendation | Notes |
   |---|---|---|
   | `keeper_{front,back}_torso` | hips `(16,25)` | same 32 x 40 canvas |
   | `keeper_front_head_{happy,neutral,grumpy,asleep,open}` | neck `(16,11)` | face variants; cap/beard included |
   | `keeper_back_head` | neck `(16,11)` | no face variants |
   | `keeper_{front,back}_arm_l` / `_arm_r` | shoulders `(10,15)` / `(22,15)` | same aligned canvas |
   | `keeper_{front,back}_leg_l` / `_leg_r` | hips `(13,25)` / `(19,25)` | same aligned canvas |
   | `prop_*` | per prop | pan, toothbrush, phone, book, fishing rod, cup |
   | `keeper_outfit_dive_*` | same pivots | full-length red-and-white striped bathing suit; no cap/helmet; bare feet |

4. Default draw order, back to front: rear prop, rear arm, rear leg, body, front leg, head, beard, cap, front arm, held prop, foreground effect. A rear-view work pose may use a simpler fixed composition, but needs its own silhouette rather than mirroring the face.
5. Pixel rotation policy: do not rotate raster limbs with CSS transforms. Either animate with translated parts, or provide hand-drawn angles at 15-degree steps for any visible swing. This avoids blur, uneven outlines, and sub-pixel jitter on iPad.
6. Lighting/mirroring policy: keep the keeper’s lighting mostly centred/non-directional so a runtime horizontal flip remains valid. Draw manual left-facing versions for one-sided props, readable lettering, and asymmetrical costume details.
7. The back-facing work pose is an intentional asset-saving device: cooking, brushing teeth, washing, and similar close-up tasks can show his back and small shoulder/arm movement. This is a design decision, not a temporary compromise.
8. Animation bible (recommended first-pass strips; `loop` means repeat while the activity remains active):

   | Clip | View | Frames / fps | Loop | Notes |
   |---|---|---:|---|---|
   | `idle` | front/side | 4 / 6 | yes | breathing, blink |
   | `walk` | side | 8 / 10 | yes | shared movement clip |
   | `reach_use` | side | 5 / 10 | no | shared interaction start |
   | `eat` | side/front | 6 / 8 | yes | bowl/plate prop |
   | `cook_back` | rear | 6 / 8 | yes | pan/shoulder motion |
   | `brush_teeth_back` | rear | 6 / 8 | yes | small elbow motion |
   | `wash_back` | rear | 6 / 8 | yes | shower/sink use |
   | `read` | side | 4 / 5 | yes | page flick optional |
   | `piano` | side/front | 8 / 10 | yes | alternating hands |
   | `watch_tv` | rear ¾ | 8 / 6 | yes | delivered offset sightline; mirror left/right |
   | `sleep` | side | 4 / 4 | yes | blanket rise; ZZZ effect separate |
   | `fish` | side | 8 / 8 | yes | rod bend / occasional catch event |
   | `dig` / `tidy` | side | 6 / 8 | yes | shared tool rhythm |
   | `phone` | side | 4 / 6 | yes | hand/head movement |
   | `greet` | front | 5 / 8 | no | wave |
   | `dance` | front | 8 / 10 | yes | celebratory loop |
   | `jump` | side | 6 / 12 | no | land returns to idle |
   | `spin` | front | 6 / 12 | no | reaction/reward |
   | `shake` | front | 4 / 12 | no | error/rejection |
   | `shrug` | front | 4 / 8 | no | confused state |
   | `robot_walk` | side | 8 / 8 | yes | later upgrade gag |
   | `chicken_care` | side | 6 / 8 | yes | feed/collect eggs |
   | `headstand` / `flex` | front | 6 / 10, 5 / 8 | no/yes | gym reward clips |
   | `cry` / `laugh` | front | 4 / 6, 4 / 8 | yes | short reaction loops |
   | `hide` / `loo` | side | 5 / 8, 6 / 6 | no/yes | use privacy silhouette where appropriate |
   | `bodily_gag` | side | 3 / 12 | no | burp/fart/sneeze; effect separate |
   | `change_to_dive` | hidden | 0 visible | n/a | never show the keeper between the doors |

9. **Delivered fact:** 48 production exports now cover the master parts and initial movement/action set, including gardening, shopping bags, rowing, speedboat/outboard operation and offset TV watching. See `docs/KEEPER_ANIMATIONS.md` for exact delivered and pending clips.

## 3. Clickable objects, states, tiers and anchors

1. The shared contract for every clickable interior item is fixed:

   - `standard`: static idle appearance.
   - `on`: animated active/use appearance.
   - `broken`: animated fault appearance.

2. Broken-state grammar is fixed across the game: gentle casing wobble, looping smoke, and occasional sparks. Add only a small object-specific cue when useful. The user specifically approved this for the TV and wants it reused rather than reinvented per object.
3. **Delivered fact:** TV is the sole visual three-state test. It is a concept reference, with no separated wobble/smoke/spark frames. All other delivered object files are basic placeholder PNGs, not complete state sets.
4. Recommended first production object table:

   | Object | Tiers | Standard / on / broken | Recommended footprint / anchor | Notes |
   |---|---:|---|---|---|
   | TV | 3 | still screen / scanline-flicker / wobble-smoke-sparks | 28 x 20; bottom-centre | TV reference approved |
   | cooker | 3 | cold / flame-steam / wobble-smoke | 28 x 22; bottom-centre | cooking uses rear pose |
   | shower | 2 | dry / water drops-steam / sputter-smoke | 18 x 30; bottom-centre | bathroom |
   | bed | 3 | made / sleep + ZZZ / broken spring wobble | 42 x 22; bottom-centre | restores 80/90/100% |
   | fridge | 3 | closed / open glow / rattle-smoke | 20 x 32; bottom-centre | kitchen |
   | phone | 3 | still / ring bounce / dead spark | 10 x 14; bottom-centre | desk/table prop |
   | telescope | 3 | folded / scan sweep / jammed rattle | 30 x 26; bottom-centre | future spotting mini-game |
   | lift | 3 | closed / doors + indicator / jammed doors | 22 x 34; bottom-centre | unlock around floor 7 |
   | hoover / robot butler | 3 | parked / moving / runaway wobble | 20 x 16; bottom-centre | labour-saving escalation |
   | chicken coop | 2 | tidy / chickens pecking / broken latch | 44 x 28; bottom-centre | feed, eggs, tidy loop |
   | piano | 2 | still / keys-hands | 38 x 28; bottom-centre | optional early living-room activity |
   | toilet / sink | 2 | still / water/flush / leak | 20 x 18; bottom-centre | keep humour gentle |

5. Tiers are not final art decisions except where stated. Recommendation: reserve 3 tiers for objects that materially change player choice (bed, cooker, TV, fridge, phone, telescope, lift, cleaners); use 2 tiers for simple props. Every tier uses the same footprint/anchor unless the gameplay deliberately adds a bay.
6. All interaction anchors should be stored explicitly in the final manifest: `objectAnchor` (floor contact), `keeperUsePoint`, `effectOrigin`, and `bubbleOrigin`. Do not infer them from transparent bounds.

## 4. Lighthouse, floors, expansion and backgrounds

1. Day 1 floor order, bottom to top, is fixed: kitchen; living room; bedroom with en suite; lamp room. The lamp room is always the topmost room.
2. The game is a flat, front-on 2D cutaway — not isometric and not full 3D. The lighthouse is the visual anchor: classic alternating red-and-white stripes, dark pixel outlines, funny but not babyish.
3. The main shaft must retain a constant gameplay width. Do not taper ordinary floors. Any apparent taper is a tiny decorative outer-wall treatment only. The lamp room may be inset/fixed width and has a wraparound rail/outdoor walkway.
4. Production floor-band size is locked at **110 x 35 logical pixels**; room plates are **105 x 35**. The runtime modules are implemented at 4× (440 x 140), and the first three room PNGs plus red/white shell stripes are delivered. Future room plates remain missing.
5. Stripe continuity must be world-coordinate-based, never based on the insertion order of floor assets. Recommended rule, evaluated against global vertical coordinate:

   ```ts
   const stripeIndex = Math.floor((worldY + localY) / 8);
   const stripeColour = stripeIndex % 2 === 0 ? '#C8463C' : '#F3E7CC';
   ```

   Use outline `#14243A`. Set the final band height once and preserve it for old saves. Do not rescale existing floors when adding a new one.

### Locked rule: future floor progression is non-linear

The tapered concept paintings do **not** impose a construction order. Future standard floors are interchangeable 110 x 35 bands, and the player may unlock eligible floor types in different orders. Do not assign Workshop, Weather Station, Radio Room, Marine Lab, Map Room, or other future standard floors to permanent height numbers merely to reproduce the concept silhouette. The full idea backlog and system relationships are in `docs/EXPANSION_DESIGN.md`.

When a standard floor is unlocked:

1. Keep the kitchen/entrance as the ground anchor.
2. Keep the lamp room topmost and the bedroom immediately below it.
3. Choose a random available position for the newly unlocked standard floor in the middle stack; existing middle floors may shift.
4. Persist the resulting order in the save and never reshuffle it nightly.
5. Recalculate shell stripes from absolute world Y; never store stripe colour on the floor type.

Day 1 remains fixed—kitchen, living room, bedroom/en-suite, lamp room—but the identity and eventual middle-stack position of later standard floors are not predetermined. A gameplay dependency may restrict eligibility (for example, the lift becomes necessary after more than six complete floors), but it must be an explicit systems rule rather than an art/geometry restriction.

Side/rear extensions, the lift service core and the underground lair do not consume standard stack slots and must not be used to force a linear ordinary-floor sequence. The diving changing-room/board extension follows the bedroom as it moves upward; the keeper may eventually dive the full lighthouse height. The current fixed Floor 3 reservation is implementation debt.
6. New floors may slide into position or arrive in a large reusable puff of smoke. Recommendation: `fx_floor_arrival_smoke`, 64 x 64 logical pixels, 8 frames at 12 fps. This effect is not yet delivered.
7. Expansion architecture is deliberately magical:

   - Local needs (diving room, upgraded kitchen, gaming room, gym) use a left/right/rear **parent-floor extension bay**, joined at a visible structural seam. The keeper reaches the parent floor normally, then walks horizontally through a new door.
   - A ubiquitous upgrade, such as a lift or a global room-width upgrade, can push the whole lighthouse walls apart. Do not deform or rescale existing furniture.
   - During a global wall push, the island splits into safe earth plates carrying exterior unlocks. Water gaps, dust, wobbling fences, and surprised chickens create the comic beat. The final beat grows fresh soil, grass, rocks, and plants in the new gap so the island is larger, not permanently broken.
   - Garden, boat/jetty and chicken coop are mission unlocks and are intentionally absent from Day 1. The shop is an off-island destination rather than an island building; its current island depiction is non-canonical concept/fallback material.

8. Underground development is a surprise. Day 1 shows normal grass, soil, and rock only — no obvious empty basement, shaft, cave, or reserved area. When a Batcave-like lair unlocks, extend terrain downward then reveal the interior. The first `ground_strip.png` is specified at 300 x 30 logical pixels.
9. The lift becomes necessary at roughly seven floors (more than six complete floors). Keep it in a rear or side aligned service core/bay so it does not consume every front-facing room. Each floor still needs one aligned landing door.
10. **Superseded implementation note:** the current code fixes the diving changing room to Floor 3, but the approved design attaches it to the bedroom wherever that room moves. Its beam/floor plane must align with the current bedroom band, allowing a full-height dive as the tower grows. Sequence: normal travel to the bedroom; keeper walks through the inner door in ordinary clothes; closes and disappears; comic zip/change SFX plays; outfit swaps off-screen; exterior door opens; he emerges in Victorian red-and-white bathing suit and walks to the board. Never show the keeper in the narrow space between the two doors.
11. At maximum height, parachuting from the lamp-room roof is a possible late-game comic unlock, not a Day 1 requirement.
12. Existing background plates are opaque single images. They cannot support parallax, camera crops, night tinting, or expansion cleanly. Required production layers are: `bg_sky`, `bg_clouds`, `bg_distant_village`, `bg_sea`, `bg_island_back`, `bg_lighthouse_shell`, `bg_terrain`, and `bg_foreground`. The village should remain in the distance as a telescope target; it is visible in the early concept direction.
13. Recommended day/night palette treatment: preserve the world art and tint via layers, rather than creating a separate night layout. Dawn: `#F2A65A` at 18% overlay; day: none; dusk: `#6C4A7D` at 28% multiply; night: `#10264E` at 52% multiply; lamp core `#FFE9A6`, glow `#FFC854`. Render the lamp beam separately (4 frames at 6 fps) above the night overlay.
14. End-of-day behaviour is fixed: the lighthouse closes up, camera zooms out to the whole tower, keeper sleeps, and the non-skippable roughly 30-second recap/stat panel is displayed. Bed quality restores 80% (basic), 90% (upgraded), or 100% (master) energy.

## 5. Effects, bubbles, other characters and audio hooks

1. Recommended effects sheet requirements:

   | Effect | Logical size | Frames / fps | Status |
   |---|---:|---:|---|
   | smoke / steam / stink | 16 x 16 | 6 / 8 | Not delivered as strips |
   | sparks / lightning | 16 x 16 | 4 / 12 | Not delivered as strips |
   | music / heart / ZZZ / coin | 12 x 12 | 4 / 8 | Prototype bubble icons only |
   | rain | 8 x 16 | 4 / 10 | Not delivered |
   | splash | 48 x 32 | 8 / 12 | Not delivered |
   | floor-arrival smoke | 64 x 64 | 8 / 12 | Not delivered |

2. Current `style_b_pixel/bubble_*.png` icons are visual placeholders rather than tested animation strips. Bubble placement must use the stored `bubbleOrigin`, with clamping to the camera frame.
3. No production visitors, seagulls, ships, cat rigs, or telescope targets are delivered. The current cat PNGs are concept material only. Recommended priority: keeper and core-object effects first; then cat idle/walk; then simple seagull/ship silhouettes for telescope use; then visitors.
4. Telescope is a future dedicated spotting mini-game, not decoration. It can reward spotting ships, visitors, weather, wildlife, and distant targets through a scan/search interaction.
5. The sound language should be faintly comic and cohesive. The diving sequence specifically needs: inner door open/close, zip/change while hidden, exterior door open/close, board creak, jump whoosh, and a huge splash. Object hooks should similarly separate start, loop, success, failure, and repair sounds. No audio files are delivered.
6. Future labour-saving progression: simple Wallace-and-Gromit-like contraptions, then an automated hoover, then a robot butler. They save time but can create comic faults, rather than removing interaction.

## 6. Runtime, browser, licensing and packing constraints

1. Use integer logical coordinates throughout. Character and object `y = 0` should mean floor contact in art/export coordinates; document any engine-axis conversion once at the renderer boundary.
2. Use nearest-neighbour scaling only. Do not use browser image smoothing, sub-pixel positions, CSS rotation of pixel art, fractional camera zoom, or untested canvas filtering.
3. Prefer a sprite renderer/canvas layer for active animation and CSS/DOM only for static UI. Test on target iPad Safari early: texture memory, context-loss recovery, touch hit targets, and 30-second recap readability are practical browser risks.
4. Reduce active layered sprites by compositing static room furniture into floor layers where interaction does not require separation. Keep dynamic effects short-lived and pooled. Pause off-screen animation.
5. Recommended atlas grouping: keeper/outfits; interactive objects; effects + bubbles; cats/NPCs; floor modules/world props. Keep backgrounds separate and streamed by layer, not packed into sprite atlases.
6. Asset provenance: current images were made for this project during the design process. Do not incorporate unverified marketplace art, copied game art, or external sprite packs without recording their licence in the repository. Preserve prompts/source notes and regenerated final sprite sources in a `art/source/` directory when production art begins.
7. The file inventory identifies alpha presence but does not prove that an alpha asset has clean edge pixels, consistent transparency, correct pivot placement, or a production licence. Validate those in the final asset build step.

## 7. Gaps, risks, prioritised work and estimate

1. The current concepts should **not** be sliced into gameplay sprites as a shortcut. The major risk is inconsistent scale/style and no reusable pivots, not lack of PNG files.
2. Required first production deliverables, in order:

   1. Extend the approved keeper set in the priority order in `docs/KEEPER_ANIMATIONS.md`, preserving `data/keeper_asset_contract.json`.
   2. Build object art against the keeper's fixed switch, handle, seat, worktop, bowl and ground-use heights.
   3. Production 110 x 35 lighthouse shell bands and 105 x 35 room PNGs matching the implemented runtime modules.
   4. TV production assets for all three states, including separate wobble/smoke/spark effects; then cooker, shower and bed.
   5. Separated day/night world layers and the reusable floor-arrival smoke effect.
   6. Lift/expansion bay specification, then the Floor-3 diving changing-room sequence.
   7. Telescope, chicken coop, labour-saving systems, underground lair, visitors, ships and other unlockable content.

3. Estimated final asset volume: approximately **650–900 individual frame/source PNGs**, excluding audio and full-scene promotional art. A reasonable split is 150–220 keeper/outfit frames, 220–320 object-state frames, 80–120 effects/bubbles, 80–120 floor/world modules, and 120–180 cats/visitors/telescope targets. Expect 8–12 runtime atlases after padding and packing.
4. Key technical risks and mitigation:

   | Risk | Mitigation |
   |---|---|
   | Pixel blur/jitter | integer coordinates, nearest-neighbour, no runtime raster rotation |
   | Lighthouse becoming too narrow | fixed core width; use extension bays/global wall push |
   | Stripe mismatch after insertion | calculate colour from global world Y |
   | iPad performance | atlas dynamic sprites, pool effects, pause off-screen animation |
   | Night recap unreadable | prototype its typography/timing on target iPad before content expands |
   | Costume-change complexity | hide the sprite between two aligned Floor-3 changing-room doors |
   | Underground telegraphed too early | keep Day 1 terrain solid; reveal only on unlock |

5. Undecided items with recommendations:

   | Item | Decision status | Recommendation |
   |---|---|---|
   | Exact final floor width | Decided | 110 logical pixels; do not taper or rescale existing floors |
   | Final day/night implementation | Undecided | Tint layered art; do not maintain two geometry sets |
   | Whether global lift uses rear or side core | Undecided | Prefer rear core where visible cutaway readability permits; otherwise side bay |
   | Object tier visual language | Undecided | Keep silhouette/anchor stable and add clearer utility/detail at higher tiers |
   | Exact animation implementation | Undecided | Begin with frame strips; move only proven reusable limbs to a part rig |
   | SFX files/engine | Undecided | Define event hooks now; commission/source audio after interactions are playable |

6. This handoff deliberately distinguishes the implemented runtime from the remaining production asset set. Delivery-order item 1 is complete; delivery-order item 2 and the 48-export keeper review set exist for review at 4× logical scale. Continue remaining keeper work from the prioritized backlog in `docs/KEEPER_ANIMATIONS.md`, and build every prop from `data/keeper_asset_contract.json` rather than estimating scale from concept art.
