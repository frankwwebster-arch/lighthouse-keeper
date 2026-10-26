# Lighthouse Keeper — Unified Spec v2 (DRAFT for Frank's approval)

Version 2.0 DRAFT · 26 Oct 2026 · Single source of truth for Claude Code (engine) and Codex (graphics) once approved.
Built from Codex's technical review of v1.3 (commit 42ec2552), with engine-side objections and resolutions added by Claude.

> STATUS: PROPOSAL. Until Frank approves Gate 0 (section 17), `AGENTS.md` and `docs/CODEX_BRIEF.md` remain the repository authority. No repository file is edited or deleted, and no historical or hash-pinned asset or document is moved, renamed or overwritten, by adopting this draft.

## 0. Authority and provenance
- Precedence once approved: Frank's explicit decisions > this spec > `AGENTS.md` / `CLAUDE.md` > catalogue > historical briefs and handoffs.
- Superseded documents (v1.0–v1.4 `LIGHTHOUSE_SPEC.md`, `ENGINE_BRIEF.md`, `ART_BRIEF.md`, `KEEPER_ROOM_GRID_172_HANDOFF_2026-10-14.md`, the design-review catalogue's geometry) are RETAINED unchanged as history. They are marked superseded in an index, never deleted.
- Correction: v1.3/v1.4 wrongly ranked the 14 Oct 172 handoff above Frank's later 26 Oct grid decision. v2 follows the later decision.
- Note: an uncommitted draft `docs/LIGHTHOUSE_SPEC.md` (v1.4) was written to the working tree on 26 Oct. It is not authority. Frank decides whether to keep it as history or discard it; nothing else touches it.
- On approval, this file becomes `SPEC.md` at the repo root, and `CLAUDE.md` / `AGENTS.md` point to it instead of restating rules. Proposals from either tool go in section 18; only Frank promotes them.
- Active-version manifest: `/public/art/manifest/active.json` names the exact approved versions (by path and SHA-256) of keeper canon, palette, tower kit, item masters and runtime derivatives. Nothing resolves "latest" by directory order.

## 1. Units
- **au** (authoring pixels): the grid Codex draws on.
- **px** (delivered pixels): production assets. 1 au = 2 px exactly (nearest-neighbour).
- **World units (engine)**: 1 world unit = 1 delivered px. The engine stores integer world coordinates only. The old lp/ku system is retired from new code; any legacy geometry still in the engine gets a documented one-off migration (section 15).

## 2. Visual style — high-resolution pixel illustration [Gate 0]
- Not 8-bit or 16-bit. Crisp hard-edged pixels at 768 × 256 au per room, delivered at 2×.
- No anti-aliasing, gradients, airbrushing, high-frequency dithering or stray single-pixel noise. Strong clustered shapes; intentional diagonals.
- Outlines in a deep-navy ink (not black): important silhouettes selectively 2 au, interior construction lines 1 au, secondary seams in a darker local colour.
- Each material: flat base + one shadow tone + one restrained highlight. Light from the upper left, short shadows falling right.
- Friendly, colourful, architectural; kid-appealing for ages 7–11, not babyish, not deliberately retro.
- Camera: flat orthographic side elevation everywhere. Floors and ceilings are bands, rooms are flat (not boxes), the tower is straight-sided, the island is side-on. Never isometric.
- Best current reference: `docs/lighthouse-island-orthographic-bare-shell-concept-v1.png` for warmth, materials, rock, outline weight and character only. It is NOT authority for stairs, baked sky or sea, room count, geometry, windows, composition or the keeper.
- Retained catalogue decisions: original CRT box-telly character; later TV tiers stay a CRT-derived family; never stretched.

### 2a. Palette
- One shared visible palette of up to 64 colours (`palette_env-v1`), plus technical magenta #FF00FF, which is not counted.
- The keeper palette is a named subset of the shared palette.
- Generated images may start off-palette, but candidates are snapped deterministically before review. Production exports have zero off-palette opaque pixels.
- Seed colours from the current keeper (jumper blues, deep navies, warm skin, cream beard, white stripes, gold badge); final values are approved from a full ROOM-view proof.
- No pink or near-magenta colour anywhere in the palette.

## 3. Room module and tower grid [Gate 0]
### 3a. Standard module (structure included in the dimensions)
| | Delivered px | Authoring au |
|---|---|---|
| Module | 1536 × 512 | 768 × 256 |
| Left wall / right wall | 32 / 32 | 16 / 16 |
| Ceiling band / floor slab | 32 / 32 | 16 / 16 |
| Walk-in zone (always clear) | x 32–256 | x 16–128 |
| Bay field | x 256–1504 | x 128–752 |
| Bays | 13 × 96 | 13 × 48 |

- Floor surface (walking line): y = 480 px from the module top.
- Bays are numbered 1–13 from the door side.

### 3b. Windows
- Two per above-ground module, 192 × 192 px (96 × 96 au), over bays 4–5 and 10–11, sills 160 px above the floor surface.
- Frames and glazing bars are artwork; the whole glass region is exact #FF00FF. Window geometry is identical across all recoloured standard modules.

### 3c. Hidden-circulation door
- One circulation entrance per floor, in the LEFT WALL of the leftmost module. No visible stairs, shaft, landing, lift car or recess.
- Closed, the door is flat and minimal. Open, its panel is a foreground occluder. Draw order: room shell → keeper → open door panel.
- Travel: the keeper walks left into the door, is occluded, the screen fades, and he emerges from the destination floor's door into its walk-in zone.
- The lift upgrade changes only the door jamb; the lift lives entirely in the hidden core. Costume changes may happen inside it.
- The kitchen's separate exterior front door, on its back wall, is not the circulation door.

### 3d. Horizontal expansion
- Tiers: 1, 2 or 3 complete modules per floor. The 172/193/214 width tiers are retired.
- Extra modules attach through a 32 px divider with an open doorway, have no circulation door, and add 13 bays each.
- Never stretch a module; never move or rescale existing content. Existing world coordinates stay stable when a module is added (modules attach to the right).
- Joins preserve floor and ceiling heights, external band alignment and gallery alignment.

### 3e. Tower stack
Bottom to top:
1. Lair (optional, LATER): always the very bottom, below the waterline.
2. Boathouse (optional, LATER): at the waterline beneath the kitchen; sea arch in its rightmost module; jetty runs from the arch.
3. Kitchen and entrance: fixed ground floor; floor surface exactly on the island ground line.
4. Middle floors: saved random order (catalogue rule).
5. Bedroom with en-suite: always directly beneath the lamp room.
6. Lantern cap: always on top.

Up to 20 above-ground floors. Day 1 = kitchen, living room, bedroom with en-suite, lantern cap.

### 3f. Lantern cap
- A full-width gallery and cornice across the active tower width (`gallery_left` + n × `gallery_mid` + `gallery_right`).
- One fixed-width lantern chamber, centred, with identical dimensions at every tower width. The shell is empty; lamp and telescope are separate sprites; glazing is exact magenta.
- Width (resolves review [UNSURE]): the lantern sits on its own lantern-floor grid, not the room grid. Proposed starting value 1152 × 512 px (576 × 256 au, 12 bays wide), centred on a one-module tower so a 192 px gallery walkway shows on each side. The final value is confirmed by the Gate 2 tower proof, then frozen. The 148 lp value is withdrawn.

## 4. Modular tower kit
Location `/public/art/tower/<version>/` with `tower_kit.json`:
`module_master.png`, `module_kitchen.png`, `module_living.png`, `module_bedroom.png`, `module_boathouse.png`, `module_lair.png`, `divider.png`, `wall_left.png`, `wall_right.png`, `wall_left_base.png`, `wall_right_base.png`, `gallery_left.png`, `gallery_mid.png`, `gallery_right.png`, `lantern.png`, `roof.png`.

- `module_master.png` is the geometry authority. Variants are produced only through declared wall-colour masks and declared permanent-feature overlays; no freehand structural redraws.
- Verification proves: identical window pixels; identical wall, floor, ceiling and skirting geometry; identical door geometry where required; differences only inside declared regions; dimensions and anchors match the manifest; no near-magenta pixels.
- Required code-assembled proofs before any furniture: (1) Day-1 tower, 4 floors × 1 module; (2) 3 floors × 2 modules; (3) a 3-module structural stress test; (4) ground-floor base and island join; (5) boathouse beneath the kitchen; (6) lair beneath the boathouse; (7) lantern and gallery alignment at all three widths. No hand-painted full-tower image is ever runtime authority.

## 5. Exact-magenta pipeline
- **Canonical key master:** an opaque environment PNG keeping exact #FF00FF (alpha 255). Never passed through tolerance removal; never the only copy.
- **Runtime derivative (built at BUILD time, not in the browser):** exact #FF00FF becomes alpha 0 with RGB zeroed; every other pixel is byte-identical. No tolerance, no defringe.
- **Reserved-colour validation:** exact key only; no visible art uses the key; near-magenta non-key colours fail validation; all key/non-key boundaries are hard edges.
- Validator record per asset: sourceSha256, runtimeSha256, width, height, magentaPixelCount, nearMagentaPixelCount (0), unexpectedMagentaPixelCount (0), nonKeyPixelChanges (0).
- Magenta is used only in opaque environment masters (sky and sea apertures, window glass, glazed doors, lantern glass, boathouse arch, lair portholes). Keeper, items, UI, bubble tokens and FX use true RGBA.
- Acceptance: the master keeps exact magenta through build and copy; the derivative keys exactly the same pixel count; non-key RGB is byte-identical; no legacy sprite command touches masters; rebuilds give identical hashes; both files are in the manifest; test fixtures cover enclosed windows, open sea and isolated portholes.

**Engine requirements (Claude):**
- Ship and load only the prebuilt RGBA derivatives; never chroma-key in the browser. Decoded colours can shift with embedded colour profiles, so the build strips gAMA, cHRM, iCCP and sRGB chunks from all PNGs, and runtime keying would be unreliable anyway.
- All sprite drawing uses nearest-neighbour sampling: `imageSmoothingEnabled = false` on Canvas 2D, `NEAREST` filtering with no mipmap generation if WebGL. The engine never asks the GPU or browser to build mipmaps; it uses the supplied ones (section 12).
- Use non-premultiplied alpha handling on upload, or verify that keyed edges don't darken.

## 6. Keeper reboot and canon migration [Gate 3]
- Blocker: `/public/art/keeper/canon/` does not exist. No new keeper art until Frank approves identity references.
- Process: (1) select exact historical images that carry the approved identity (e.g. the approved Makko side idle, front idle and walk, and the approved turn frames); (2) record SHA-256 values; (3) Frank approves them as identity references; (4) install them byte-identically under `canon/identity-reference-v1/`; (5) produce pixel-reboot candidates from them; (6) review front, side and back together at ROOM scale; (7) approve; (8) promote to `canon/pixel-reboot-v1/`; (9) point `canon/active.json` at it, with hashes; (10) never overwrite any source bytes.
- Retained design: navy peaked cap with small gold badge; full white beard and moustache; pink nose; bright blue knitted jumper, two white chest stripes, one per sleeve, ribbed cuffs and hem; navy trousers; chunky navy boots; stocky, about 3 heads tall.
- Forbidden drift: sailor collar, scarf, coat, apron, different hat, glasses, extra stripes, logos, weapons, changed face, beard or proportions, props painted into keeper frames.
- Frame geometry: delivered cell 256 × 320 px (128 × 160 au); anchor [128, 312] px ([64, 156] au) at the feet; keeper 244–250 px tall; 8 px bottom gutter. Every frame in a direction set shares the same cell, anchor and floor line. Root movement only where locomotion metadata records it; idles, turns and activities never wander.
- The approved Makko-era clips (walk loop, idles, turns) are retained unchanged as identity references and history. They are not production animation in the pixel reboot, so their frame counts and 42 ms timing are removed from this spec.

## 7. Animation strategy
- A small shared vocabulary. Most household activities reuse a rear-facing work loop, while bubble stories and separate effects explain the detail. Bespoke poses are exceptional and need a demonstrated readability or interaction need.
- Day-1 vocabulary: neutral side, front and back; side walk loop; front↔side turn; side↔back turn; rear-work entry, loop and exit; sit; stand; bed entry; sleep loop; bed exit; door-crossing compatibility; a discreet bathroom pose only if rear-work can't cover it. No stair animations.
- Indicative budgets (not frozen until visual testing): walk 8; turns 4–6 per direction or one exact reversible sequence; rear-work entry 2–3, loop 4, exit = reversed entry where valid; sit/stand 4–6; bed entry/exit 4–6; sleep 2–4.
- Timing lives in clip metadata: locomotion about 8–10 fps, rear work about 6–8 fps, idle holds via per-frame durations, footfalls and bubble cues as named events.
- Mirroring is allowed only with no asymmetric prop, no text or directional symbol, valid costume, and declared mirrored facing. Props are separate sprites, positioned per facing.

**Engine requirements (Claude):**
- Locomotion (replaces the handoff's "whole gait cycles only" rule, which can't land on 96 px bay anchors): walk speed is derived from the clip's recorded root motion per cycle. Distances that aren't a whole number of cycles are handled by finishing on the nearest declared stop-capable frame within half a stride, then a short ease (≤ 1 frame duration) to the exact anchor. No stretching of artwork or root motion.
- Walk → idle and idle → walk join on frames flagged `stopCapable` / `startCapable` in clip metadata, not hard-coded frame numbers.
- Clip JSON is the only source of timing; the engine has no global frame-duration constant.

## 8. Sprite-sheet and asset safety
- Canonical frames are stored individually (`clip/frames/frame_000.png` …) with `clip.json`; `sheet.png` / `sheet.json` are generated deterministically from them and are never the only source.
- Every frame has an explicit cell; everything belonging to it (body, prop, shadow, particle) stays inside; minimum 8 px transparent gutter on every edge; shared cell boundaries have alpha 0; ownership comes from geometry and metadata, never from connected-component order.
- Canonical pixel art alpha is 0 or 255 only; fully transparent pixels have RGB 0; no fringes. Runtime opacity is allowed for UI transitions.
- Every sheet verifies: dimensions, cell size, frame count, anchor and floor-line equality, palette, alpha, gutters, zero shared-edge alpha, zero ambiguous or unowned pixels, metadata/image agreement, source and output hashes.
- Reversible amendments: corrections to approved art start in a new versioned draft directory, leave the approved asset untouched, record both hashes, include side-by-side and animated comparisons, are promoted only on explicit approval, and are rejected by deleting only the draft directory. Immutable review exports are never rewritten.

## 9. Activities and bubble stories [V1]
- Flow: walk to the interaction anchor → turn to rear → entry → shared rear-work loop (plus small separate hand, tool or effect sprites) → bubble story shows the specific activity → bubble resolves → exit to neutral.
- Every activity maps to: item, interaction anchor, keeper pose (rear-work or one of the few dedicated clips), bubble story, duration, need effects.
- The existing bubble-story library (339+ pictures, engine, `/studio/stories`, `data/activity-stories/`) is retained as a deliberately higher-resolution illustrated UI layer. Only the bubble frame, pointer and orchestration marks are redrawn in the new pixel style. Internal pictures stay unchanged and are not auto-pixelated; ids, recipes and timing are preserved. Individual pictures are redrawn later only on a demonstrated clash.
- Ownership: Claude owns the story engine and studio; Codex owns the pictures.

## 10. Items
### 10a. Footprints
- SMALL 1 bay (96 px), DOUBLE 2 (192 px), LARGE 3 (288 px), CENTREPIECE up to 4 (384 px).
- **No runtime reflow** (replaces v1.x). Each item reserves its MAXIMUM-tier footprint in the room layout from the start. Lower tiers draw inside that reservation; interaction anchors stay fixed across tiers; neighbours never move; purchased items reserve their place from the outset; validation uses maximum footprints. (This is Frank's alternative "draw maximum scope for every element now".)
- The player never moves items.
- Items are anchored bottom-left to their bay on the floor surface. Decorative wall art and rugs may declare visual bounds without taking exclusive floor bays, provided they don't obstruct interaction or windows.

### 10b. Day-1 reserved footprint budget (proposed, for the fit check)
| Room | Item | Max bays |
|---|---|---|
| Kitchen | Worktop 3, fridge 2, cooker/range 2, broom storage 1, pet bowl 1 | 9 of 13 |
| Living | CRT TV unit 2, bookshelf 2, piano 3, armchair 2 | 9 of 13 |
| Bedroom + en-suite | Bed/four-poster 3, phone/bedside 1, desk 2, basin 2, toilet 1 | 9 of 13, plus the permanent partition |
| Lamp room (lantern grid) | Lamp mechanism 2, telescope 2 | 4 of 12 |

- The en-suite partition is permanent geometry. Proposed position: the partition stands at the left edge of bay 11, so bays 11–13 form the en-suite (basin 2 + toilet 1) and bays 1–10 the bedroom. Confirm in the Day-1 layout proof.

### 10c. States
- One master per item per tier. Derived states only: OFF, ON (up to 4 frames), optional FLASHING (2 frames). Each derived state differs only inside its declared changing region (pixel-diff verified).
- Never drawn: broken, dirty or alert variants.
- The engine owns faults: status light, FX (smoke, sparks, water drips/spray, steam, loose spring, wobble), alert icons and SFX (per-fault sound plus an onset chime).

### 10d. Fault indicators
- ROOM view: the item's own indicator lamp with an engine-drawn, hard-edged stepped pulse (no soft glow). Colour plus shape or icon redundancy for accessibility: red ✕ broken, amber ! needs attention, green ✓ ready, blue i information.
- TOWER and ISLAND views: a room-level badge on the affected room and, off-screen, edge indicators (section 13). Don't rely on the tiny lamp at these scales.

### 10e. Item metadata (minimum)
`id, tier, bayWidth, reservedBayWidth, canvasPx, anchorPx, states{off, on[], flashing[]}, interactionAnchors[{id, offsetPx, facing}], bubbleOriginPx, effectOriginPx, statusLightPointPx, faultType, palette, sourceSha256, files{}`.

## 11. Island and outdoor art
- Same units as the tower: 1 module width = 768 au = 1536 px; 1 bay = 48 au = 96 px. Major plots use module-width units; facilities may use whole-bay increments. The "12 lp outdoor grid" is withdrawn.
- Day 1: full island rock including below a level waterline; ground line level with the kitchen floor; short grass; rough grass and rocks on uncleared ground; play lawn; vegetable bed; barbecue terrace; cliff steps; wooden jetty; moored rowing boat with outboard; empty future plots; separate surface and edge pieces where expansion needs them.
- Never in the foreground master: sky, sea, clouds, birds, waves, horizon, distant islands, ships.
- Later plots (catalogue list plus play lawn, beehives, shed, spare plot) are listed with sizes for approval before drawing.

## 12. Rendering, mips and zoom
**Layers, back to front:** sky (time of day, weather; clouds and birds as engine sprites) → sea → island and tower foreground → items, keeper, FX → waterline wave band (y from the art manifest) → weather overlay, UI, edge indicators.

**Pixel-exact scaling (engine resolution of the review's [UNSURE]):**
- Art is only ever displayed at integer multiples of its authoring grid, so pixels stay uniform.
- ROOM view: largest integer scale of the 768 au module that fits the viewport width with its walls: ×2 (1536 px) on a 1920-wide screen, with the leftover margin showing tower exterior and sky, not stretching. On narrower viewports, ×1 (768 px).
- TOWER and ISLAND views use pre-generated mip levels of the delivered art: 1/2 (= 1 au per px), 1/4 and 1/8 where needed. Each mip is palette-preserving and visually reviewed; thin critical features (window bars, railings, the keeper's face, status lights, item legs, structural seams) get declared minimum-feature preservation or a hand-corrected mip.
- Transitions: no continuous resampling. A transition is (a) a jump cut, or (b) a glide that pans at the outgoing view's fixed scale, then crossfades (about 0.25 s) to the incoming view's mip at its fixed scale. Camera position always snaps to whole display pixels.
- Engine work this needs: a mip-set selector per view, integer-scale viewport fitting, pixel-snapped camera, and a two-layer crossfade. Contained and feasible for V1. The current camera doesn't do this, so it's a planned task, not a blocker.

**Ghosting:** a runtime tint (about 25% saturation, 55% brightness) on non-active floors. It keeps hard edges and alpha, never needs separate art, and never applies to event overlays or alerts.

## 13. Camera behaviour
- Fixed views: ROOM, TOWER, ISLAND (section 12 for scaling).
- ROOM framing: the active room's module, centred vertically. On multi-module floors, ROOM view frames the module the keeper is in, and walking into a neighbouring module pans horizontally at the same scale. Neighbouring floors are ghosted and not tappable in Director mode; event overlays in ghosted rooms draw at full brightness and are tappable.
- DIRECTOR MODE (default): cut to the room the keeper enters; on floor travel, glide out to TOWER and cut to ROOM on arrival; when the player sends him to an item elsewhere, glide out as he starts moving; outdoors uses ISLAND; events needing attention cut to them.
- EXPLORE MODE: starts on drag, swipe or scroll; pans TOWER and ISLAND; tapping a room or plot cuts to ROOM; tapping an item sends the keeper and returns to Director mode. Events never move the camera in Explore; they show edge indicators. 8 s idle returns to Director mode. A permanent "find the keeper" button.
- Priority: one event owns the camera at a time; the rest queue as indicators; never cut during a mini-game or mid-tap.
- V1 simplification: Director mode plus basic vertical and island scrolling; full Explore mode if time allows.

## 14. Catalogue reconciliation
- The catalogue remains authority for: room and activity inventory, unlock challenges, need effects, timings, breakdown rules, bathroom-access rules, and tier names where wanted.
- It is NOT authority for: room dimensions, free-x placement, visible stairs or lift shafts, pixel density, broken-item frames, historical plates and item frame sizes, or style.
- Decided: hidden circulation over visible stairs, lift or slide art; boathouse under the kitchen over shore placement; engine fault overlays over broken frames; bay indices over free-x; CRT family retained.
- Snooker (resolves the v1.3 contradiction): Frank said the snooker table is a bought asset that "likely deserves its own room, with a mini game". So: approved in principle as a LATER dedicated room unlocked by buying the table (CENTREPIECE, 4 bays). It stays in the games hall's catalogue entry until that room is specified and approved. No V1 impact.

## 15. Engine migration (Claude)
- New geometry module using world units = delivered px, with the module, bay, window, door and floor-surface constants from section 3, generated from `tower_kit.json` rather than hard-coded.
- One-off converters for any stored legacy ku/lp coordinates (saves, layouts) into world px, with tests. Old geometry code is kept until the converter is verified, then marked deprecated, not deleted, until Frank approves removal.
- The 172-handoff drag-and-drop contract is retired (the player never moves items). Its route and clearance checks are re-expressed on the 13-bay grid: walk-in zone clear, reserved footprints non-overlapping, every interaction anchor reachable, keeper action envelopes unobstructed.
- Asset loading reads only manifest-listed runtime derivatives and verifies hashes in dev builds.

## 16. Christmas version (V1) — target 20 Dec 2026
- Players: Ralph (7) and Eddie (11), separate saves and difficulty.
- In V1: Day-1 tower (kitchen/entrance, living room, bedroom with en-suite, lamp room), island scenery with the boat at the jetty; needs bars; daily credits based on each need ending the day green (rules per D9); everyday activities (eat/cook, sleep, wash, toilet, clean, relax, lamp duty) via rear-work and bubble stories; faults and repair per section 10; day/night and basic weather backdrop; camera per section 13 (simplified); base-tier items only; upgrade spending only if it fits. Existing features (typed commands, phone, day report, quizzes): keep if solid, hide if flaky.
- Not in V1: full catalogue conversion, tier-2/3 furniture art, bespoke per-activity animation, new bubble vocabulary, lair, boathouse unlock, multi-module widening, advanced weather, island facilities, snooker room, non-essential mini-games, maths and admin dials, gifting.
- Production order: Gate 0 → magenta pipeline → one ROOM/TOWER/ISLAND style proof → lock palette and grid → keeper canon migration → front/side/back reboot approval → master module and kit → Day-1 tower and island → base-tier items → minimal keeper clips → bubble integration → UI, needs and credits art → sky, sea and weather layers → verify all activity flows → multi-zoom, palette, gutter and magenta verification → stabilise and release.
- Indicative schedule: 26 Oct–2 Nov spec, grid, style proof, pipeline · 3–9 Nov canon migration and kit · 10–23 Nov rooms, island, base items · 24 Nov–6 Dec keeper clips, bubbles, UI, backgrounds · 7–13 Dec integration · 14–19 Dec bug fixing and polish · 20 Dec release.
- Art freeze: once Gates 0–2 pass, style, palette and grid are frozen until 20 Dec; changes need Frank's explicit decision.

## 17. Gates
- **Gate 0 (Frank):** approve the pixel reboot, the 1536 × 512 / 13-bay grid, the 244–250 px keeper, the minimal animation strategy, bubble-story retention, no-reflow reserved footprints, and 1–3 module widening.
- **Gate 1:** the exact-magenta master survives the build unchanged and produces a verified exact-match RGBA derivative.
- **Gate 2:** one representative room is approved at ROOM, TOWER and ISLAND scale (including mips and the lantern width).
- **Gate 3:** identity references are installed, reboot candidates reviewed, `active.json` populated.
- **Gate 4:** one- and multi-module assemblies pass geometry and pixel-diff checks.
- **Gate 5:** maximum reserved footprints fit all four Day-1 rooms.
- **Gate 6:** one complete activity runs: walk → turn → rear work → bubble → completion → neutral.
- **Gate 7:** all sheets pass gutter, ownership, alpha, palette, anchor and metadata checks.
- **Gate 8:** the complete Day-1 loop works in all three views with no missing art, stale legacy geometry or unverified assets.

## 18. Open decisions and proposals
- D7 (style): pixel reboot per section 2. Awaiting Gate 0.
- D8 (grid): 1536 × 512 / 13 bays per section 3. Awaiting Gate 0.
- D9 (V1 gameplay rules): needs bars, decay rates, activity restores, day end, credit rules. To be settled at the Claude Code kickoff and recorded in section 16.
- D11: lantern width (proposed 1152 px). Confirm at Gate 2.
- D12: en-suite partition at bay 11. Confirm at Gate 5.
- D13: whether Day 1 includes a toilet or bathroom pose beyond rear-work (only if rear-work can't read discreetly).
- Catalogue register items (marine lab, radio room, greenhouse, transport, power, bank, bowling/gaming/hot-tub/roof, solar tracker) remain open as listed there.
- Proposed changes: (none yet)

## Change log
- 26 Oct 2026: v2.0 DRAFT. Rebuilt from Codex's technical review of v1.3 plus engine-side resolutions: pixel reboot at 768 × 256 au ×2; 1536 × 512 / 13-bay grid; au/px units; 244–250 px keeper in a 256 × 320 cell; left-wall circulation door; 1–3 module widening; reserved maximum footprints with no reflow; exact-match magenta with build-time derivatives; integer-scale rendering with reviewed mips; clip-metadata timing; sprite safety and provenance rules; bubble stories as a separate illustrated layer; snooker approved in principle as LATER; lantern width deferred to proof. v1.x and the 172 handoff retained as history.
