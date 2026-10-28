# Lighthouse Keeper — Unified Spec v2.1

Version 2.1 DRAFT · 26 Oct 2026 · Single source of truth for Claude Code (engine) and Codex (graphics) once approved.
Built from Codex's technical review of v1.3 (commit 42ec2552), with engine-side resolutions by Claude and Frank's decisions of 26 Oct. v2.1 folds every 26 Oct amendment into the body: the body now states one set of numbers, and the change log is history only.

> STATUS: WORKING SPEC (Frank, 26 Oct). Codex and Claude follow it for all new work. Items marked [Gate 0] still need Frank's formal sign-off. Existing runtime code and approved asset bytes stay unchanged until a migration is approved; no historical or hash-pinned asset or document is moved, renamed or overwritten.

## Shared channel — how Codex and Claude use this file
- This file lives at `docs/SPEC.md` in the repo (GitHub `frankwwebster-arch/lighthouse-keeper`, working copy `~/Documents/ChatGPT/Lighthouse Keeper`). It is the ONE shared source of truth and the channel between Codex and Claude. Frank should never need to attach or relay it.
- Before any task: `git pull`, then read this file. A task brief from Frank may override it for that task only.
- Either agent may edit it. Every edit: (1) change the body so it states one current answer (never append a contradiction); (2) add a dated line naming the author (Codex or Claude) and the reason at the end of `docs/SPEC_HISTORY.md`; (3) commit only this file with a message starting `SPEC:`; (4) push.
- Frank's decisions are recorded as "(Frank, date)" and may only be changed by Frank. Anything that would change one, or any open question, goes in section 18 as a proposal or question, signed and dated, for Frank.
- SCHEMATICS ARE GEOMETRY ONLY (Claude, 27 Oct): a schematic fixes sizes, positions and heights. It is NEVER a style or perspective reference; its flat boxes must not be copied as art. Every schematic image carries a 'GEOMETRY ONLY' label and shows top-reveal bands and the one-point perspective guides, so it cannot be read as a flat design.
- **CLEAR WALKING LANE — ABSOLUTE (Frank, 28 Oct):** the side doors' width must never overlap the depth of any furniture in a room. All furniture stands within 0.9 m of the back wall (front faces on y 485); each side door is 1.0 m wide and spans 1.0–2.0 m out from the back wall (floor y 488–516), straddling the walking line y 502. The keeper comes out of the stair door and walks a straight, unimpeded line to the other side of the room. Nothing ever stands in a doorway or the lane, and side doors open away from the room. Full method: `docs/SCHEMATIC_METHOD.md`.
- **IN THE GAME (Frank, 28 Oct):** nothing made is ever deleted. Each piece in the Room Planner has an In the game switch; a piece switched off keeps its drafts and notes but is left out of rooms and briefs. Codex ignores any piece with `inGame: false` in `docs/planner/pieces.json`.
- **ROOM PLANNER IS THE HUB (Frank, 28 Oct):** rooms, pieces, upgrades, reference images, every draft and Frank's feedback (verdicts, pinned likes and dislikes, next-round briefs) live in the Room Planner artifact. Codex reads the read-only mirror in `docs/planner/` (synced by Claude) and hands every draft back through a `DRAFTS.json` in its review folder (format in `docs/planner/README.md`). Codex never edits `docs/planner/`.
- **BAYS (Frank, 28 Oct):** floor pieces snap to approved 1 m bays: 9 as standard, x 286–1798 (windows fill bays 3 and 7); the strips either side are wall only. The bay count can grow per room (a wider room = a bulge or tower widening, rare).
- **CUPBOARD CLEARANCE (Frank, 28 Oct, revised):** when a room has the cupboard of myriads behind its right door, the narrow wall strip beside that door (x 1798–1888 on a 9-bay room) stays completely empty, wall pieces included. The last bay itself can be used (a whole empty bay left too big a gap).
- **LARDER DROPPED (Frank, 28 Oct):** there is no larder in the kitchen or anywhere else; it is not part of any brief. It stays in the Room Planner as a piece marked NOT IN THE GAME, drafts kept for reference. Its rectangle in `kitchen_v14_schematic.json` is void. The kitchen's run B gains a third cupboard (bay 8) and the dresser moves to bay 9, beside the cupboard of myriads.
- **FIXED SHELL + FINISHES (Frank, 28 Oct):** every floor uses ONE fixed shell drawing (ceiling edge, side walls, the two side doors, window frames, skirting, floor edge), painted once and never redrawn. Floor, wall and ceiling finishes (boards, lino, flagstones, carpet; paint, stone, panelling, wallpaper, tiles; beams, plain) are separate layers painted to the shell's fixed masks in its perspective, chosen per room and swapped without touching the shell, so rooms never drift.
- SCHEMATIC METHOD (Frank, 28 Oct): every room is laid out with the standard pieces in `docs/SCHEMATIC_METHOD.md`, using the Room Planner artifact (https://claude.ai/artifact/KAvqrmWsYootZJLmEz22kL). The right side door (cupboard of myriads or WC) is OPTIONAL per room.
- ROOM SCHEMATIC FIRST (Frank, 27 Oct): no room is ever briefed to Codex until Frank has approved its SCHEMATIC: a dimensioned layout drawn by Claude on the common room template (same module, shell, datums, stops and windows for every room), giving every element's exact box. The schematic is then the absolute brief; Codex fills the boxes. The kitchen schematic is APPROVED (Frank, 27 Oct): `docs/layout/kitchen_v14_schematic.json` (+ `kitchen_v14_schematic_1x.png`; every unit a 1.0 m module). Superseded: `docs/layout/kitchen_v13_schematic.json` + `kitchen_v13_upgrade_journey.png` (radio moved to the lobby; Grand Espresso climbs a 1.1 m column above the dishwasher slot; shows reserved upgrade slots and tier-3 wall climbs; earlier versions superseded).
- VERCEL AND REPO-SIZE GUARD — ABSOLUTE (Frank, 27 Oct: 'one day they'll block me'). (1) NO DEPLOYS for reviews: review work stays in the repo/working folder, where Frank and Claude look at it directly; never publish a review page just to show art. (2) A production deploy (`npm run deploy`, a `[deploy]` commit) happens ONLY when an issue labelled `go` explicitly says DEPLOY, at most ONCE PER DAY, and never several in a row (on 24–26 Oct there were 10 deploys in 3 days, three within 15 minutes). (3) Keep `public/` well under its 50 MiB guard; nothing from `review/` ever goes into `public/`. (4) Repo size: `.git` is already about 2 GB, so no animated GIFs or multi-megabyte review sheets are committed; review images are PNG, at most about 2 MB each and 20 MB per review folder; anything bigger stays local and uncommitted. Claude Code keeps the existing build-skip guard (`scripts/vercel-ignore-build.mjs`) in place.
- GO RULE (Frank, 26 Oct; moved to Issues 28 Oct): Codex starts work ONLY on GitHub issues labelled `codex` AND `go` (see `docs/ISSUES.md`). Anything else is for reading only, even if it looks complete. Claude adds `go` only after Frank agrees. When you finish a task, check for more; if there are none, stop and report.
- Messages for the other agent go on the relevant GitHub issue (Codex: via `docs/CODEX_REPLIES.md`). Keep them short.
- Never edit this file and other files in the same commit; never rewrite history; on a merge conflict, keep both changes and flag it in `docs/CODEX_REPLIES.md` (Codex) or on an issue (Claude).

## 0. Authority and provenance
- Precedence once approved: Frank's explicit decisions > this spec > `AGENTS.md` / `CLAUDE.md` > catalogue > historical briefs and handoffs. A task brief may override this spec for that task only, and says so.
- Superseded documents (v1.0–v1.4 `LIGHTHOUSE_SPEC.md`, `ENGINE_BRIEF.md`, `ART_BRIEF.md`, `KEEPER_ROOM_GRID_172_HANDOFF_2026-10-14.md`, the design-review catalogue's geometry, and v2.0 of this file) are RETAINED unchanged as history. They are marked superseded in an index, never deleted.
- Correction: v1.3/v1.4 wrongly ranked the 14 Oct 172 handoff above Frank's later 26 Oct grid decision. v2 follows the later decision.
- Note: an uncommitted draft `docs/LIGHTHOUSE_SPEC.md` (v1.4) was written to the working tree on 26 Oct. It is not authority. Frank decides whether to keep it as history or discard it; nothing else touches it.
- `AGENTS.md` and `CLAUDE.md` point here. Proposals from either tool go in section 18; only Frank promotes them. Superseded copies outside the repo (Frank's Downloads folder) are not authority.
- Active-version manifest: `/public/art/manifest/active.json` names the exact approved versions (by path and SHA-256) of keeper canon, palette, tower kit, item masters and runtime derivatives. Nothing resolves "latest" by directory order.

## 1. Units and scale
- **px** (delivered pixels): production assets are authored and delivered at the same resolution. The pixel-reboot "au" grid (1 au = 2 px) is retired with the pixel style (section 2).
- **World units (engine)**: 1 world unit = 1 delivered px. The engine stores integer world coordinates only. The old lp/ku system is retired from new code; any legacy geometry still in the engine gets a documented one-off migration (section 15). For the Prime Keeper, 1 ku = 1 px.
- **Scale (absolute):** 1 m = 168 px. Depth on screen (section 3h): object top reveals 1/6 of real depth (28 px per metre); the room floor band is a fixed 84 px.
- **The keeper sets the scale.** The approved Prime Keeper is used 1:1 and is never rescaled (298 px = 1.77 m). The world is drawn to fit him, not the reverse.
- **Widths are FREE; stops are on a lattice (Frank, 26 Oct; restores the 14 Oct contract):** the keeper's stopping points are a fixed lattice one step (84 px = 0.50 m) apart. Furniture keeps its real, chunky width and is NEVER squeezed into a step-wide slot. Each item the keeper uses is positioned so its MIDPOINT (or declared working point) sits exactly on a lattice point, so he stops dead centre. No weird narrow units.

## 2. Visual style — ligne claire [Gate 0]
- Working direction (Frank, 26 Oct): style B, smooth flat-colour illustration in a light ligne-claire manner. Target feel: "adult and yet also playful, suitably Hergé but also modern." Not pixel art; 8-bit and 16-bit were rejected as too blocky when zoomed.
- STYLE AUTHORITY: the approved Kitchen Oven V7 drawing, `art/source/kitchen-built-in-state-ligne-claire-2026-10-21-v7/oven-on-user-confirmed-visual-authority.png`, SHA-256 `0a8f0cbeb8fda75bc2da9948da8f2c7fc5a54f14d8202ef5bc2c89d8c0bb5538` (historical blob at commit `52e94f2a`; absent from the current working tree, read from git history). It is a STYLE reference only: it is never mapped into the game, and it stays hash-locked.
- What to carry from it: one uniform, confident near-black outline weight on every edge, matched to the keeper's outline at 1:1; flat, clean colour fills; at most one shadow tone per material; simple, readable shapes with hand-drawn charm; small details as plain line work (dial ticks, rack bars). Anti-aliased edges are fine. The only soft gradient permitted is light glow (oven cavity, lamps, screens), and that lives in light overlays, never in base art.
- Light from the upper left, shown only by shading inside objects. NO SHADOWS IN THE GAME (Frank, 26 Oct): no cast shadows on walls, no floor or contact shadows, under items or the keeper. Friendly, colourful, architectural; kid-appealing for ages 7–11, not babyish.
- Camera and depth: "front-on with a top reveal" (section 3h) everywhere: rooms, items, keeper, tower and island. Never isometric, never vanishing-point perspective.
- Kitchen palette (Frank, 27 Oct): DUCK-EGG painted wood (matt), cream enamel appliances, copper or brass handles and knobs, scrubbed pine and honey timber, a few blue-and-white plates; no chrome, no checkerboard, no red diner set. The earlier approved kitchen sheet (royal blue, cyan, cream, copper) remains a line-quality reference only; its drawn broken states are FX reference only (section 10f).
- Warmth and materials reference: `docs/lighthouse-island-orthographic-bare-shell-concept-v1.png` (warmth, materials, rock, outline weight). It is NOT authority for stairs, baked sky or sea, room count, geometry, windows, composition or the keeper.
- Retained catalogue decisions: original CRT box-telly character; later TV tiers stay a CRT-derived family; never stretched.

### 2a. Palette
- One shared named palette (`palette_env-v1`) is a REFERENCE for colour consistency, plus technical magenta #FF00FF. Do NOT snap or quantise ligne-claire art to it: snapping destroys the modelling (lesson of the 26 Oct kitchen rebuild). Validation only reports large drifts.
- **TWO VIEWING SCALES — ABSOLUTE (Frank, 27 Oct: 'really important to me').** Every asset must look good in (A) ROOM VIEW, the play view, where a 1 m unit is about 170 px wide, and (B) LIGHTHOUSE VIEW, the whole tower, where the same unit is only about 20 px wide. What this means for making them: (1) paint at 2× room size so room view (and any zoom) stays crisp; (2) design SILHOUETTE FIRST: each item must be recognisable at 20 px from its outline and one or two strong colour blocks (cream fridge, sage cabinets, copper accents), never from fine detail; (3) strong VALUE CONTRAST against the cream wall, so items don't dissolve when small; (4) fine detail (panels, plates, knobs) is a bonus for room view and is expected to vanish in lighthouse view; (5) lighthouse view uses a reviewed reduction of the assembled room (section 12), simplified by hand where it turns to mush; if reduction still fails, a small painted lighthouse-view version of the whole room is commissioned instead of shrinking; (6) EVERY review sheet shows the assembled room at both scales side by side, and an asset that does not read in lighthouse view fails.
- **NO ART DRAWN IN CODE — ABSOLUTE (Frank/Claude, 27 Oct, after the v14 build was drawn with PIL rectangles and came out as flat clip-art with no perspective).** Every visible game asset is painted by the image generator (or comes from an approved painted source). Code may ONLY crop, uniformly scale, pad, place, mask, recolour by mask, assemble and verify. It never draws shapes, panels, handles, shading or any part of an item. EXACT CANVASES ARE MET BY PAINTING TO THE RIGHT PROPORTIONS: generate each item at its rectangle's aspect ratio (at 2×), then scale uniformly and pad so its visible art fills the canvas within 4 px on each side; if the proportions are off, regenerate rather than distort or redraw in code.
- **PERSPECTIVE CHECKLIST for every room and item brief (the look Frank approved in the v8 pieces and the v8 room shell):** (1) every worktop and every cabinet, appliance or furniture top shows its shallow top reveal (about 17 px for 0.6 m depth) drawn straight up, with the front edge slab below it; (2) bevelled, layered fronts with one matt shadow tone and confident 3–4 px ink on main contours; (3) the shell is ONE-POINT PERSPECTIVE: side walls, ceiling beams and floor-board edges recede to the vanishing point at x 1024, y 250, with the side-wall doors drawn in that perspective (reference `reference/shell/room-shell-reference-01.png` and `review/kitchen-proof-v8-room-shell-v1/outputs/kitchen-v8-room-shell-empty-1x.png`); (4) floorboards in the floor band converge slightly towards the vanishing point; (5) side-by-side comparison with the approved v8 pieces (`review/kitchen-proof-v8-assets-v1/`) is part of every review sheet, and a result that looks flatter or more 'clip-art' than them fails.
- ART PRODUCTION METHOD (revised 26 Oct, after two rejected kitchens): for rooms of freestanding pieces, generate the room FREELY at high quality with the approved calibration as style reference and the keeper composited for scale, then cut each piece out and slide it so its midpoint sits on its stop (uniform scaling only). A rigid pixel layout guide during generation produced flat, toy-like art and is not used. Earlier wording: paint at final scale, then cut. Each room's furniture set is painted TOGETHER as one image at exactly 2× module size (3072 × 1152), using a layout guide (bay grid, every item's exact rectangle, floor, worktop and window lines) as the control input, so line weight, detail density and lighting stay consistent. The parts are then CUT from it along their declared rectangles and reduced uniformly to 1:1 with high-quality filtering. Never generate items one by one at large size and shrink them ~10×; never re-ink silhouettes or quantise colours in code. Outline weight at 1:1: about 3–4 px on main contours, matching the keeper. Later single-item replacements are painted at 2× into the same layout guide with the neighbouring parts visible, then cut the same way.
- The keeper palette is a named subset of the shared palette, measured from the Prime Keeper.
- No pink or near-magenta colour anywhere in any asset.

## 3. Room module and tower grid [Gate 0]
### 3a. Standard module (structure included in the dimensions)
| | Delivered px |
|---|---|
| Module | 2048 × 576 (Frank, 26 Oct: widened from 1536 for room to grow) |
| Left wall / right wall | 32 / 32 |
| Ceiling band / floor slab | 32 / 32 |
| Walk-in zone (always clear) | x 32–328 |
| Furniture field | x 328–2016 |
| Stopping lattice | x = 370 + 84n (one Prime Keeper step apart) |

- Vertical layout (y from the module top): ceiling band 0–32; back wall 32–460 (2.55 m); floor band 460–544 (84 px = 2.0 m room depth × 1/4); floor slab 544–576.
- Back-wall line (where the wall meets the floor): y = 460. Front edge of the floor: y = 544.
- Keeper walking line: per room (`walkY`, section 3g). Kitchen walkY = 502.
- Stopping lattice points ('stops') are numbered 1–20 from the door side: x = 370 + 84(n−1): 370, 454, 538, 622, 706, 790, 874, 958, 1042, 1126, 1210, 1294, 1378, 1462, 1546, 1630, 1714, 1798, 1882, 1966. They are NOT furniture slots. Layouts may still use 'bay' as shorthand for the 84 px interval around a stop when measuring, but no item width is tied to it.
- WHY 84: the stop spacing equals one Prime Keeper step (F1→F5 = 84 px), and the door clearance is set so the door point (x 118) is exactly three steps from stop 1. Every stop is therefore a whole number of steps from the door and from every other stop, so he can walk to and stop exactly on any item whose midpoint is placed on a stop.

### 3b. Windows
- Two per above-ground module, 168 × 168 px, each CENTRED ON A STOP so a sink or desk can sit centred beneath it: left window centred on stop 5 (x 622–790), right window centred on stop 13 (x 1294–1462), roughly symmetric about the module centre, at y 106–274. The sill (y 274) is 186 px ≈ 1.11 m above the back-wall line; the head is 74 px below the ceiling band.
- Frames and glazing bars are artwork; the whole glass region is exact #FF00FF with hard edges (no anti-aliasing against magenta). Window geometry is identical across all recoloured standard modules.
- **HARD RULE: no furniture or item may ever occlude a window.** No item may rise above y 274 inside x 622–790 or x 1294–1462, at any tier. No wall-mounted item, shelf, picture, curtain, pelmet or FX may overlap a window's frame or glass. Tall items (fridge-freezer, dresser, bookshelf, wardrobe, piano, four-poster canopy) stay clear of the window spans. Counter-top items (kettle, toaster) are not allowed under windows. The layout validator fails the build on any overlap, checked at every item's maximum-tier artwork bounds. The keeper is foreground and exempt.

### 3c. Hidden-circulation door
- One circulation entrance per floor, in the LEFT WALL of the leftmost module, at the FRONT of the room. No visible stairs, shaft, landing, lift car or recess.
- Because the camera looks straight at the back wall, only the door's jamb is visible: a vertical strip at x 0–32, y 208–544 (2.0 m from the floor front). No door panel is ever drawn on the back wall.
- Open, the door panel is a foreground occluder. Draw order: room shell → keeper → open door panel / jamb.
- Travel: the keeper walks left into the door, is occluded, the screen fades, and he emerges from the destination floor's door at the door standing point (x 118) on that room's walkY.
- The lift upgrade changes only the door jamb; the lift lives entirely in the hidden core. Costume and tool swaps may happen inside it.
- LOBBY HAT STAND AND BOOTS (Frank, 27 Oct): a hat-and-coat stand beside the lobby's LEFT door shows his outdoor gear (oilskin and sou'wester; winter coat, woolly hat and scarf); wellies and snow boots sit under the boot bench next to it. Each garment and pair of boots is a separate sprite, shown when he isn't wearing it and hidden while he's out in it, so the lobby shows at a glance what he's gone out in. The stand and bench are each one unchanging drawing.
- WET CLOTHES AND DRYING (Frank, 27 Oct; LATER, with the outdoor costumes): outdoor gear worn in rain or snow comes home WET and hangs on the lobby's ceiling airer (the same garment sprites, re-anchored to the airer, with drip FX) instead of the hat stand. While wet it can't be worn, so rain or snow jobs needing it must wait or are done without it (with a needs penalty). When dry it returns to the stand. Washed laundry dries the same way (washing line outside in fine weather; the airer when wet). Drying speed by tier: t1 ceiling airer = slow; t2 tumble dryer (replaces the airer; floor unit beside the washing machine, status lamp, faults stop drying until fixed) = fast; t3 = the Laundry Engine takes over drying too = near-instant. Exact times are tuning values, not art.
- LOBBY HAS NO WINDOWS (Frank, 27 Oct): the ground-floor lobby is the one floor without the standard two windows.
- FRONT DOOR (to the island) (Frank, 27 Oct; replaces the back-wall front door): there is NO door on any back wall anywhere in the game. In the lobby, the LEFT side-wall door leads to a hallway (never seen) holding both the stairs and the front door. On the lighthouse exterior the front door is on the LEFT of the tower base. Going out: he walks to the hat stand, does the rear-work entry/exit as he takes his gear (the matching garment and boot sprites vanish from the stand and bench), then exits through the left door in day clothes and appears outside in his gear. Coming home: he comes in through the left door in day clothes, does the rear-work entry/exit at the stand, and the gear reappears on it (wet gear goes on the airer to dry instead: see WET CLOTHES AND DRYING). The swap is hidden in the hallway, so no costumed clips are needed indoors and there is no depth-walking anywhere. Visitors: the doorbell on the wall beside the left door rings, and he goes out through the left door to answer it.

### 3d. Horizontal expansion
- Tiers: 1, 2 or 3 complete modules per floor. The 172/193/214 width tiers are retired.
- Extra modules attach through a 32 px divider with an open doorway, have no circulation door, and add 14 bays each.
- Never stretch a module; never move or rescale existing content. Existing world coordinates stay stable when a module is added (modules attach to the right).
- Joins preserve floor and ceiling heights, external band alignment and gallery alignment.

### 3e. Tower stack
Bottom to top:
1. Lair (optional, LATER): always the very bottom, below the waterline.
2. Boathouse (optional, LATER): at the waterline beneath the lobby; sea arch in its rightmost module; jetty runs from the arch.
3. Entrance lobby with utility (laundry): fixed ground floor; its floor-slab top (module y 544) is exactly on the island ground line. Left-wall door to the hallway with the stairs and the front door (section 3c); open-plan utility area; downstairs WC behind the right door.
4. Kitchen: fixed first floor, directly above the lobby.
5. Living room WITH THE DINING TABLE: ALWAYS the floor directly above the kitchen (Frank, 27 Oct). The keeper carries meals up one floor to eat; the kitchen has no table.
6. Other middle floors: saved random order (catalogue rule), above the living room.
7. Bedroom with en-suite: always directly beneath the lamp room.
8. Lantern cap: always on top.

Up to 20 above-ground floors. Day 1 = entrance lobby (with utility and downstairs WC), kitchen, living room, bedroom with en-suite, lantern cap.

### 3f. Lantern cap
- A full-width gallery and cornice across the active tower width (`gallery_left` + n × `gallery_mid` + `gallery_right`).
- One fixed-width lantern chamber, centred, with identical dimensions at every tower width. The shell is empty; lamp and telescope are separate sprites; glazing is exact magenta.
- Width: the lantern sits on its own lantern-floor grid. Proposed starting value 1072 × 576 px, centred on a one-module (2048 px) tower so a 488 px gallery walkway shows on each side; may grow with the wider module. Confirmed by the Gate 2 tower proof, then frozen (D11).

### 3g. Room depth and walking line
- Standard room depth 2.0 m (floor band 84 px). Furniture stands against the back wall; the floor in front of it is the keeper's walking space.
- **The keeper walks close to the furniture, never along the front edge of the floor.** In the top-reveal view anything further back is drawn higher, so a keeper far forward would see a worktop at chest height.
- Each room declares `walkY` = back-wall line + (deepest back-row item depth + 0.40 m) × 42, capped at y 536. Kitchen: 0.60 m units + 0.40 m = 1.00 m → walkY 502. With the keeper at walkY 502, the worktop edge reads at about 60% of his height.
- Floor items deliberately placed in front of the walking line (rare; e.g. a rug edge) are drawn after the keeper. Items behind it are drawn before him.
- Reference diagrams: `room_depth_rule.png` (layout) and `depth_projection_rule.png` (projection). Both predate the walkY rule; the text here wins.

### 3h. Projection — ABSOLUTE (applies to every room and every asset)
- ROOM SHELL SYMMETRY (Claude, 27 Oct, after shell v1's lopsided doors): the shell is SYMMETRIC about the module centre (x 1024). The vanishing point is at x 1024, at the keeper's eye height (about y 250). Both side walls have the same depth: the back wall spans x 160–1888. Each side wall carries ONE ordinary panelled door, 2.00 m tall at its front edge (336 px), seen in perspective, the same size and treatment on both sides, like the reference image; no oversized door slabs. Furniture stands only within the back-wall span.
- ROOM SHELL PERSPECTIVE (Frank, 27 Oct; applies from the v8 room stage, after the style test): the room SHELL uses gentle ONE-POINT perspective, the classic dolls'-house cutaway: the back wall stays flat and front-on; the side walls, ceiling edges and floor's side edges recede towards a single vanishing point at the room's centre, so the side walls and their doors are visible (left wall = stair door, right wall = magic-cupboard door, both drawn as real doors in perspective). Reference: Frank's favourite shell image, `reference/shell/room-shell-reference-01.png`. EVERYTHING PLACED IN THE ROOM (furniture, appliances, items, keeper) stays flat and front-on per the rules below, stands along the back wall, and never intrudes onto the angled side walls. Widened floors use three shell variants: left end, middle (no side walls), right end. Windows: raise sills above the reference's height and keep crisp glass edges.
- PROJECTION ("front-on with a top reveal"): every front face is drawn flat and true to size as a pure elevation. Depth is shown ONLY as a shallow top reveal drawn straight up, at 1/6 of the object's real depth (28 px per metre; a 0.60 m worktop = 17 px), matching the approved V7 oven and the approved kitchen proof draft. Round things on top surfaces (hotplates, bowls, sink basins, rims) are drawn as ellipses about 1/3 as tall as wide, so they read clearly. Recesses (oven cavity, fireplace, sink bowl) may show converging interior walls toward their own centre. No vanishing points, no sideways skew, no side faces, no visible ceilings, no angled walls. Sprites never change size with depth. This keeps assets mirrorable, stackable and consistent wherever they stand.
- FLOOR: a fixed 84 px band (y 460–544) in every room — a house rule, not derived from the reveal ratio — with floorboards or tiles as horizontal lines only. Its back edge meets the back wall at y 460. Placement on the floor uses the floor band's own scale (42 px per metre of floor depth).
- PLACEMENT: an object standing against the back wall has its front-face bottom at y = 460 + depth × 42 (a 0.60 m unit: y 485). A freestanding item standing d metres from the wall sits at y = 460 + (d + depth) × 42.
- KEEPER: drawn in the same convention: profile body, slight top reveal on cap and shoulders only; no contact shadow.
- LIGHT: upper left. Top reveals are the lightest tone, front faces mid. No cast or contact shadows anywhere.
- REAL MEASUREMENTS: every asset is sized from a real-world reference (chunky and generous rather than skinny, to suit the style) and drawn at its real width and height at 168 px/m. Record `realSizeM: [width, depth, height]`, `widthPx` and `midpointStop` (the stop its midpoint sits on) in `item.json`. Codex proposes measurements; Frank approves.
- Starting reference sizes (to be confirmed per item; real widths): base unit 0.50–1.00 × 0.60 × 0.90 m, worktop 0.90 m high; under-counter fridge 0.60 × 0.60 × 0.85 m; fridge-freezer 0.60 × 0.65 × 1.80 m; American-style fridge 0.90 × 0.70 × 1.80 m; basic oven 0.60 × 0.60 × 0.90 m (in a 1.0 m housing); two-oven range 1.00 × 0.60 × 0.90 m; Belfast sink 1.00 m; upright piano 1.45 × 0.60 × 1.20 m; armchair 0.85 × 0.85 × 0.95 m; bookshelf 0.80 × 0.30 × 1.80 m; bed side-on 1.95 long × 0.95 deep × 0.50 m, four-poster frame 2.10 m high; desk 1.20 × 0.60 × 0.75 m; basin 0.55 × 0.45 × 0.85 m; CRT television 0.60 × 0.50 × 0.50 m on a 0.50 m stand.

### 3i. Gait lattice (Prime Keeper)
- Walking uses the approved Prime Keeper gait (Walk V7, the approval record for the exact Walk V6 pixels), with 1 ku = 1 px: steady walk 21 px per frame; one step (F1 → F5) 84 px; one cycle 168 px; start bridge 2, 6, 12, 18 (38 px); stop bridge 18, 12, 6, 2 (38 px).
- Standing anchors are the STOPS: x = 370 + 84(n−1), n = 1…14. The door standing point is x = 118 (exactly three steps before stop 1).
- Every item he uses is placed with its midpoint on a stop, so he stops exactly at its centre, whatever its width.
- Where an item's working point is not its middle (e.g. one oven of a two-oven range), the item declares `workingPointPx`, and THAT is placed on a stop instead.
- Exact arrival needs every move to be a whole number of 84 px steps. That requires the pending gait decision (D15): re-time start and stop to 42 px each (3, 7, 13, 19 / 19, 13, 7, 3) and add the opposite-foot F5 stop. Until D15 is approved, reachable stops from the door are only 76 + 168n px.

### 3j. The RIGHT DOOR — the magic cupboard (Frank, 26 Oct)
- Every floor has TWO doorways, both in the side walls at the front and both seen only as a jamb: the LEFT door (x 0–32) leads to the hidden stair core; the RIGHT door (x 2016–2048, y 208–544, in the rightmost module) leads into a fictional space between the room and the tower's outer wall that holds whatever that room needs. Like the stairs, it is a deliberate fiction: it never takes up a bay and is never drawn.
- What lies behind the right door, by room: kitchen and most rooms = the cupboard of myriads (indoor tools: broom, hoover, super hoover, mop, duster, toolbox and so on); entrance lobby = the downstairs WC (a small "WC" sign on the jamb); bedroom = the WC, reached through the en-suite (section 3k), also signed.
- Use: the keeper walks along walkY to the right wall, passes behind the jamb and is hidden (draw order: shell → keeper → right jamb). Swaps happen while hidden: tool in or out, outfit change, toilet use, leaving or entering the tower. He reappears the same way, already holding the tool or in the new outfit.
- Costs: no bays, no item art beyond the jamb, no keeper animation beyond the walk. Bays 13–14 stay available for items; anything there stands behind walkY, so the keeper walks in front of it to the door.
- No camera-facing cupboards are needed anywhere. The toilet is never seen, anywhere in the game.
- DOORS OPEN BY THEMSELVES (Frank, 26 Oct): every door opens automatically as the keeper reaches it and closes behind him. There is no door-opening animation for the keeper, ever; a visible door is just a closed/open state swapped by the engine.
- GARDEN SHED (Frank, 26 Oct): the outdoor equivalent of the magic cupboard. Outdoor tools and kit (lawnmower, watering can, spade, fishing rod and tackle, crab pots, paint for the boat) come from the shed on its island plot, with the same walk-in, hidden-swap, walk-out mechanic.

### 3k. The en-suite (Frank, 26 Oct)
- The bedroom's EN-SUITE is an actual, visible bathroom at the right of the bedroom floor, about 3.0 m wide (x ≈ 1512–2016 on the 2048 module), proposed, confirmed in the bedroom proof.
- It is separated from the bedroom by a partition seen edge-on: a 16 px interior wall strip at about x 1504 (clear of the right window, which ends at x 1462), from the ceiling band to the floor, with an open doorway at the front where walkY crosses it. Same back wall, floor and ceiling lines; the en-suite may have its own wall colour or tiles.
- Contents, drawn as items: basin with mirror (bay 9), bath (bays 10–12, low enough to pass under the window sill), shower cubicle (bay 13, not a window bay), towel rail or laundry basket (bay 14). Teeth-brushing is rear-work at the basin.
- The WC is behind the floor's RIGHT DOOR, signed "WC", never seen. Pyjama changes happen there too.
- The lobby has NO end room and no internal doors: its right door is the downstairs WC (signed), with a small hand basin in the lobby beside it (bay 14).

## 4. Modular tower kit
Location `/public/art/tower/<version>/` with `tower_kit.json`:
`module_master.png`, `module_kitchen.png`, `module_living.png`, `module_bedroom.png`, `module_boathouse.png`, `module_lair.png`, `divider.png`, `wall_left.png`, `wall_right.png`, `wall_left_base.png`, `wall_right_base.png`, `gallery_left.png`, `gallery_mid.png`, `gallery_right.png`, `lantern.png`, `roof.png`. Every floor-height piece is 576 px tall.

- `module_master.png` is the geometry authority. Variants are produced only through declared wall-colour masks and declared permanent-feature overlays; no freehand structural redraws.
- Verification proves: identical window pixels; identical wall, floor, ceiling and skirting geometry; identical door geometry where required; differences only inside declared regions; dimensions and anchors match the manifest; no near-magenta pixels.
- Required code-assembled proofs before further furniture: (1) Day-1 tower, 4 floors × 1 module; (2) 3 floors × 2 modules; (3) a 3-module structural stress test; (4) ground-floor base and island join; (5) boathouse beneath the kitchen; (6) lair beneath the boathouse; (7) lantern and gallery alignment at all three widths. No hand-painted full-tower image is ever runtime authority.

## 5. Exact-magenta pipeline
- **Canonical key master:** an opaque environment PNG keeping exact #FF00FF (alpha 255). Never passed through tolerance removal; never the only copy.
- **Runtime derivative (built at BUILD time, not in the browser):** exact #FF00FF becomes alpha 0 with RGB zeroed; every other pixel is byte-identical. No tolerance, no defringe. This works because every key/non-key boundary is a hard edge (section 3b).
- **Reserved-colour validation:** exact key only; no visible art uses the key; near-magenta non-key colours fail validation; all key/non-key boundaries are hard edges.
- Validator record per asset: sourceSha256, runtimeSha256, width, height, magentaPixelCount, nearMagentaPixelCount (0), unexpectedMagentaPixelCount (0), nonKeyPixelChanges (0).
- Magenta is used only in opaque environment masters (sky and sea apertures, window glass, glazed doors, lantern glass, boathouse arch, lair portholes). Keeper, items, UI, bubble tokens and FX use true RGBA.
- Acceptance: the master keeps exact magenta through build and copy; the derivative keys exactly the same pixel count; non-key RGB is byte-identical; no legacy sprite command touches masters; rebuilds give identical hashes; both files are in the manifest; test fixtures cover enclosed windows, open sea and isolated portholes.

**Engine requirements (Claude):**
- Ship and load only the prebuilt RGBA derivatives; never chroma-key in the browser. The build strips gAMA, cHRM, iCCP and sRGB chunks from all PNGs, because decoded colours can shift with embedded colour profiles.
- Sampling: high-quality smooth filtering, using the supplied reviewed mips (section 12). The engine never builds its own mipmaps.
- Use non-premultiplied alpha handling on upload, or verify that anti-aliased edges don't darken.

## 6. Keeper canon — the Prime Keeper [Gate 3]
- The approved Prime Keeper animation bank is the only keeper authority. Identity contract: `data/keeper_prime_identity_contract.json` (Codex's working folder). `canon/active.json` records the contract and every approved clip by path and SHA-256.
- Registration: authoring cell 256 × 320 px; anchor [128, 320]; opaque sole datum y 316; standing height 298 px (= 1.77 m at 168 px/m). The engine places the sole datum on the room's walkY (the anchor therefore sits 4 px below walkY). The runtime cell recorded in the contract (128 × 160 at density 4) is a packaging detail; on screen the keeper is always 1:1 with the room art.
- NEVER rescale the keeper relative to the world. Scaling frames while keeping the 21 px/frame root motion makes planted feet slide, and a non-integer downscale softens his outline against the ligne-claire art. (An 83.89% display transform was proposed and rejected on 26 Oct.)
- Approved clips: neutral side, Walk V7 (= Walk V6 pixels), start and stop bridges, side↔back turn. New keeper art always starts from approved frames as the input reference and changes only the pose; candidates go to a review folder with a side-by-side against canon and enter the game only on Frank's approval.
- Retained design: navy peaked cap with small gold badge; full white beard and moustache; pink nose; bright blue knitted jumper, two white chest stripes, one per sleeve, ribbed cuffs and hem; navy trousers; chunky navy boots; stocky, about 3 heads tall.
- Forbidden drift: sailor collar, scarf, coat, apron, different hat, glasses, extra stripes, logos, weapons, changed face, beard or proportions, props painted into keeper frames.
- Every frame in a direction set shares the same cell, anchor and floor line. Root movement only where locomotion metadata records it; idles, turns and activities never wander.
- The approved Makko-era clips (walk loop, idles, turns) are retained unchanged as identity history. They are not production animation.

## 7. Animation strategy
- A small shared vocabulary. Most household activities reuse a rear-facing work loop, while bubble stories and separate effects explain the detail. Bespoke poses are exceptional and need a demonstrated readability or interaction need.
- Day-1 vocabulary (day clothes unless stated): neutral side, front and back; side walk loop; sweep-walk loop and hoover-push loop (cupboard tools, section 9a); front↔side turn; side↔back turn; rear-work entry, loop and exit; sit; stand; door-crossing compatibility. One get-into-bed clip (pyjamas only, section 9b); no sleep loop, get-out-of-bed or toilet animations: sleeping is shown by the bed's OCCUPIED state and toilet use is always hidden. No stair animations.
- FRONT-DOOR CLIPS: WITHDRAWN (Frank, 27 Oct). The front door is behind the lobby's left door, so there are no walk-away / walk-toward clips and no depth-walking anywhere in the game.
- Indicative budgets (not frozen until visual testing): walk 8 frames per cycle (168 px ÷ 21); turns 4–6 per direction or one exact reversible sequence; rear-work entry 2–3, loop 4, exit = reversed entry where valid; sit/stand 4–6; get into bed 4–6.
- Timing lives in clip metadata: locomotion about 8–10 fps, rear work about 6–8 fps, idle holds via per-frame durations, footfalls and bubble cues as named events.
- Mirroring is allowed only with no asymmetric prop, no text or directional symbol, valid costume, and declared mirrored facing. Mirrored walks negate root deltas. Props are separate sprites, positioned per facing.

**Engine requirements (Claude):**
- Locomotion: walk speed comes from the clip's recorded root motion. Every move between lattice points is a whole number of 84 px steps (start bridge → steady frames → stop bridge). A 1-step move goes start bridge straight into stop bridge. No stretching of artwork or root motion, no snapping, no shortened steps. Until D15 lands, a stop that can't hit its anchor exactly finishes on the nearest stop-capable frame and records the error in dev builds.
- Walk → idle and idle → walk join on frames flagged `stopCapable` / `startCapable` in clip metadata, not hard-coded frame numbers.
- Clip JSON is the only source of timing; the engine has no global frame-duration constant.

## 8. Sprite-sheet and asset safety

### 8-0. Asset isolation and change control (prevents redraw cascades)
- Every visual element is its own file: each unit front, worktop tile, end cap, plinth tile, insert, freestanding appliance, light overlay, counter-top item, wall item and FX sprite. Runs, rooms and towers are ASSEMBLED from these in code, never painted as one picture.
- THREE-SCALE REVIEW GATE (Frank, 27 Oct): no asset is approved until it has been shown on ONE sheet at all three scales the player sees, beside the Prime Keeper at the same scale: (1) CLOSE-UP 2× (zoomed in: detail and charm must hold, lines stay crisp); (2) ROOM 1:1 (the normal play view); (3) TOWER about 1/8 (the whole lighthouse: the piece must still read by silhouette and colour blocks alone, like a squint test; fine detail is expected to vanish). Design rule that follows: big, simple, characterful silhouettes and a few strong colour accents first; detail second. Sources are authored at 2× so the close-up stays sharp; smaller views come from reviewed reductions (section 12).
- PROPORTIONS AND SIZE (Claude, 26 Oct, from the first kitchen item batch): every asset is drawn at its exact in-game proportions (from its real size at 168 px/m and its bay width) and judged at 1:1 game size before approval. A larger working canvas is fine only if it has exactly the same aspect ratio and is reduced uniformly. Never stretch, squash or crop to fit. Detail that won't survive at game size (thin gloss streaks, tiny dial ticks) is simplified at the drawing stage.
- A fix to one asset touches ONLY that asset's file. A Codex task names the exact file(s) it may change, and must not modify any other asset.
- Regression gate: after any art change, the build re-assembles the affected rooms and verifies that every untouched asset file is byte-identical (hash check), and that the assembled room differs from the previous approved render only inside the changed asset's rectangle. Any other difference fails the change.
- Approved assets are locked by hash in the manifest. Changing a locked asset requires a new versioned draft (below) and Frank's approval.

### 8-1. Frames and sheets
- Canonical frames are stored individually (`clip/frames/frame_000.png` …) with `clip.json`; `sheet.png` / `sheet.json` are generated deterministically from them and are never the only source.
- Every frame has an explicit cell; everything belonging to it (body, prop, particle) stays inside; minimum 8 px transparent gutter on every edge; shared cell boundaries have alpha 0; ownership comes from geometry and metadata, never from connected-component order.
- Alpha: fully transparent pixels have RGB 0. Partial alpha is allowed only on anti-aliased outline edges and in light-overlay glows; no coloured fringes or halos.
- Every sheet verifies: dimensions, cell size, frame count, anchor and floor-line equality, palette (fills), alpha, gutters, zero shared-edge alpha, zero ambiguous or unowned pixels, metadata/image agreement, source and output hashes.
- Reversible amendments: corrections to approved art start in a new versioned draft directory, leave the approved asset untouched, record both hashes, include side-by-side and animated comparisons, are promoted only on explicit approval, and are rejected by deleting only the draft directory. Immutable review exports are never rewritten.

## 9. Activities and bubble stories [V1]
- Flow: walk to the interaction anchor → turn to rear → entry → shared rear-work loop (plus small separate hand, tool or effect sprites) → bubble story shows the specific activity → bubble resolves → exit to neutral.
- Every activity maps to: item, interaction anchor, keeper pose (rear-work or one of the few dedicated clips), bubble story, duration, need effects.
- The existing bubble-story library (339+ pictures, engine, `/studio/stories`, `data/activity-stories/`) is retained as an illustrated UI layer. Only the bubble frame, pointer and orchestration marks are redrawn in the ligne-claire style. Internal pictures stay unchanged; ids, recipes and timing are preserved. Individual pictures are redrawn later only on a demonstrated clash.
- Ownership: Claude owns the story engine and studio; Codex owns the pictures.

## 9a. Tools and cleaning [V1]
- Tools come from behind the room's RIGHT DOOR (section 3j). The pickup is never animated: the keeper walks into the right door and walks back out already holding and using the tool. Tools are separate prop sprites on the keeper's hand anchors, never painted into keeper frames.
- Every room can be cleaned. Tool tiers: broom (t1) → hoover (t2) → super hoover (t3). Each tier is a prop swap plus its matching loop, not a new room animation.
- Day-1 keeper clips this adds: SWEEP-WALK loop (side, moves along walkY) and HOOVER-PUSH loop (side). Super hoover reuses the hoover loop with its own prop.
- Later indoor tools use the same mechanic: mop, duster, toolbox (repairs), paintbrush. Outdoor tools come from the garden shed (section 3j).
- The engine owns which tool appears, its prop anchors per facing, and the cleaning effect (tidiness rising, dust puffs as FX).

## 9b. Occluding doors and costume changes
- Anything the keeper passes behind (the left stair door or the right door) can hide a swap: tool in or out, or outfit change. Outdoor gear (wellies, sou'wester, winter coat, woolly hat) goes on and off in the hallway behind the lobby's LEFT door, by weather, as he leaves or comes home; he takes it from and returns it to the hat stand and boot bench (section 3c).
- The en-suite is an actual bathroom (section 3k); the keeper goes behind the bedroom floor's RIGHT DOOR (the WC) and comes out changed (day clothes → pyjamas at night, and the reverse in the morning, by game time). The toilet is NEVER seen in use, anywhere in the game.
- Getting into bed IS animated (Frank, 26 Oct): a short get-into-bed clip in pyjamas (about 4–6 frames, side view, climbing in and pulling the covers up). On its last frame the keeper sprite hands over to the bed's OCCUPIED state (the bed art with his head on the pillow, covers up), drawn as a bed item state; sleeping is that still state, not a loop. In the morning the lights brighten and he steps out beside the bed in pyjamas (cut, or the clip reversed if it reads well).
- Brushing teeth happens at the basin, facing the mirror, so his back is to the camera: it uses the rear-work loop (in pyjamas) plus a bubble story.
- The costume list is fixed and short. No others without Frank's decision:
  | Costume | Used for | Changed via | Minimal clip set | Scope |
  |---|---|---|---|---|
  | Day clothes (default) | Everything | — | Full vocabulary | V1 |
  | Pyjamas | Night in the bedroom | En-suite WC door | Side walk; stop + turn (side↔back); brush-teeth rear loop at the basin; get into bed. Nothing else. | V1 — REQUIRED (Frank, 26 Oct) |
  | Swimming | Pool, lido, sea swim | Changing-room door | Walk to water, swim loop, exit | LATER |
  | Snow-sweeping (winter gear) | Clearing snow outside | Lobby left door (hallway), gear from the hat stand | Walk, snow-sweep loop | LATER |
  | Sou'wester / oilskins | Outdoor jobs in rain and storms | Lobby left door (hallway), gear from the hat stand | Walk, outdoor-work loop | LATER |
- Pyjamas are REQUIRED for V1. Every other costume is DROPPABLE: the game must play completely without them. If one proves troublesome, the engine falls back to day clothes for that context with no other change, and the costume can be removed from scope by Frank's decision alone.
- Cheaper option to try first for rain and snow: a separate hat sprite (sou'wester, woolly hat) on a per-frame head anchor over the day-clothes clips, instead of a whole new costume set.
- Costume sets follow the same canon, palette and approval rules as the day keeper (section 6), drawn from Prime Keeper frames.

## 10. Items
### 10a. Footprints
- Widths are real and free (no bay categories). Each item reserves the width of its LARGEST tier from the start, centred on its stop; lower tiers draw centred inside that reservation, and plain fillers or flexible cupboards take up any spare width.
- **No runtime reflow.** Each item reserves its MAXIMUM-tier footprint in the room layout from the start. Lower tiers draw inside that reservation; interaction anchors stay fixed across tiers; neighbours never move; purchased items reserve their place from the outset; validation uses maximum footprints.
- The player never moves items.
- Items are anchored bottom-left to their bay at their placement y (section 3h). Decorative wall art and rugs may declare visual bounds without taking exclusive floor bays, provided they don't obstruct interaction or windows.

### 10a-2. Fitted runs (kitchen units, and later bathroom, workshop and lab benches)
- Fitted furniture must read as one joined run. A fitted item is NEVER drawn with its own worktop, plinth or side panels. A run is assembled from four layers:
  1. PLINTH strip: one tileable 1-bay piece (84 × 17), plus left and right end caps, along the unit base line.
  2. UNIT FRONTS: each fitted item supplies only its front (doors, drawers, dishwasher front, sink cabinet), exactly its bay width, with no outer edges drawn.
  3. WORKTOP strip: one continuous worktop per run, made of a tileable 1-bay piece (84 × 32: 1/4-scale top reveal plus front edge), left and right end caps (16 px), and a 2 px joint line between tiles. Worktops are never part of an individual item.
  4. INSERTS: the sink and any built-in hob are NEVER cut into the worktop. The worktop tile underneath is always the same plain tile. Each insert is a separate sprite laid ON TOP of it, with its own rim wide enough to cover the join. No worktop art ever contains a hole or knows what sits on it.
- Appliances follow their tier in `data/upgrades.csv`: an under-counter or slot-in appliance (Day-1 fridge, basic oven) sits in the run under or between worktops; a tall or freestanding upgrade (fridge-freezer, American fridge) breaks the run, which ends with end caps either side. Styling keeps a light 1950s flavour (Frank, 26 Oct). No dishwasher.
- Anything tall or freestanding next to a run breaks the worktop, and the run puts end caps on either side.
- Freestanding items (table, chairs, bin, pet bowl) are separate sprites; counter-top items (toaster, kettle, mixing bowl) sit at mid-depth of the worktop at declared counter anchors.
- The engine (or build step) assembles runs automatically from contiguous bays tagged `fitted`, so neighbours always join perfectly, and an upgrade only swaps fronts, inserts or slot-ins while the run recomputes.
- One shared style for all runs in a room: matching door colour, handles, worktop material and plinth.

### 10a-3. Standard fitted vertical positions (0.60 m deep units against the back wall)
- Matched to the approved kitchen proof draft: unit base (front-face bottom) y 485. Plinth: y 468–485. Unit fronts: y 336–468. Worktop front edge (a chunky slab, as on V7): y 322–336. Worktop top reveal (0.60 m × 1/6 = 17 px): y 305–322. Counter items stand on y 314. With the keeper at walkY 502, the worktop edge is 180 px above his soles (60% of his height).
- Tall upgrades (fridge-freezer, American fridge, 1.80 m): feet on y 485, front y 183–485, top reveal y 166–183, kept clear of the window spans.
- Sink taps rise from the rear of the worktop reveal and stay below the window sill (y 274).

### 10b. Day-1 layouts and reserved footprint budget
**Kitchen (layout v8, UK COTTAGE, 2048 module, walkY 502) (Frank, 27 Oct; replaces the American 1950s v7, judged too shiny, too American, oven too tall, floor wrong).** A British cottage kitchen in a lighthouse: painted-wood furniture in one harmonious family (duck-egg, matt), each piece freestanding with its own wooden top, wall between pieces. Style: adult ligne claire per V7: matt flat colour, one shadow tone, uniform ink, NO gloss highlights, no shine streaks, no chrome sparkle; restraint over decoration. Floor: honey timber floorboards (horizontal boards in the floor band), not checkerboard. Wall: plain cream; a wooden plate shelf or small painted wall cupboards for the instant kitchen read, clear of windows.

**Kitchen standard-unit boundary (Frank, 27 Oct):** every ordinary one-unit cupboard/appliance master is exactly 126 px wide. The Day-1 cooker is one 126 px unit; its later range upgrade is exactly two units / 252 px, centred on the same stop and occupying the maximum reservation from day one. The range is deliberately deferred and is not part of the Day-1 asset set. Bespoke furniture (the Belfast sink cabinet, table and dresser) keeps its separately declared span.

| Item | Reserved span (x) | Midpoint stop | Surface for |
|---|---|---|---|
| Small cream larder fridge, counter height, matt: Day-1 one-unit art is x 391–517 (126 px), centred inside the unchanged 0.90 m maximum-tier reservation; t2/t3 may fill the reservation later | 378–530 | 454 (stop 2) | — |
| Belfast sink set in a painted cabinet with a wooden top, under the left window | 622–790 | 706 (stop 5) | washing-up |
| Painted cupboard with wooden top | 811–937 | 874 (stop 7) | KETTLE (stovetop or electric, enamel) |
| Cooker: t1 is one 126 px old-school cream gas cooker (x 1063–1189) with four burners/controls and an eye-level box hood/grill; t2/t3 future cottage range is exactly 252 px (two standard units), fills the reservation, and is NOT drawn yet | 1000–1252 | 1126 (stop 10) | — |
| Scrubbed pine table with two wooden chairs, under the right window (below the sill) | 1252–1504 | 1378 (stop 13) | eating, food prep; he can sit |
| Painted dresser: plate rack above with blue-and-white plates, counter shelf and cupboards below | 1555–1705 | 1630 (stop 16) | TOASTER |
| Painted cupboard with wooden top | 1735–1861 | 1798 (stop 18) | MIXER |
| Enamel pedal bin | 1945–1987 | 1966 (stop 20) | — |

- **KITCHEN v9 LAYOUT TEMPLATE — ABSOLUTE, SUPERSEDES the v8 table above where they differ (Claude, 27 Oct; DRAFT SCHEMATIC, under discussion with Frank).** `docs/layout/kitchen_v9_layout.json` + `docs/layout/kitchen_v9_layout_1x.png` give EVERY element's exact rectangle at 1:1 on the 2048 × 576 module: shell, windows, every base unit, the worktop strips and end caps, slot-in cooker (with its grill box), table, chairs, dresser, wall cupboards, counter items, keeper. Codex has NO size or position choices: each part is delivered on a canvas exactly its rectangle's size and fills it; any part that does not match fails. Choices left to Codex are surface detail only (panels, handles, grain, plates) in the approved v8 style.
- **SINGLE WORKTOP WITH HEALING (Frank, 27 Oct; restores the original fitted-run plan, section 10a-2):** base units have no tops of their own. Each run has ONE continuous worktop strip laid over its units (y 317–348: 17 px top reveal + 14 px front edge). Top reveals are drawn as plain rectangles with straight vertical ends, so where a worktop meets a slot-in (the cooker hob, also a rectangle at the same y) or another worktop, the tops butt together with NO V-shaped wedge. Only an EXPOSED run end (nothing beside it) gets a small tapered end-cap piece. The engine/build assembles runs; a sink bowl is an insert laid on the worktop.
- **CHUNKY RULE APPLIES TO EVERY TIER (Frank, 27 Oct).** Tier-2 and tier-3 versions, contraptions included, obey the same proportions: no piece taller than TWICE its width. A contraption in a 1.0 m slot tops out at about 2.0 m; only slots about 1.3 m or wider may reach the ceiling. Contraptions get their drama by SPRAWLING (gears, pipes, chutes and gadgets spreading across their slot and its wall) rather than by becoming tall and thin. The schematic's upgrade boxes carry `maxHeightPx` to enforce this.
- **CHUNKY RULE — ABSOLUTE (Frank, 27 Oct: 'I HATE the skinny units').** Every kitchen unit is the SAME chunky 1.0 m module (168 px wide; with the worktop it is slightly wider than tall, about 1.07:1, as in Frank's approved kitchen sheet `approved_kitchen_reference.png`): cupboards, sink, dishwasher slot, cooker and fridge alike. Nothing narrower than 1.0 m except small props. Every tall item is at least HALF as wide as it is tall. Every schematic is checked against this before Frank sees it, and Codex fails any part that breaks it.
- **SIZE TABLE — ABSOLUTE (Claude, 27 Oct, after the v8 room proof put the table at knee height, the oven too low, the dresser too high and the kettle and mixer in mid-air).** Heights are real at 168 px/m and are measured on the item's VISIBLE art (opaque bounding box) at 1:1. Each item is uniformly scaled so these heights are exact; its width follows from its own proportions (no stretching).

| Item | Key height (px above its feet) | Overall height (px) |
|---|---|---|
| Prime Keeper (never scaled) | — | 298 (1.77 m) |
| Base cupboard, sink cabinet, dresser base | WORKTOP / counter surface 151 (0.90 m) | 151 (+ taps on the sink) |
| Cooker | HOB 151 (0.90 m), level with the worktops; GRILL at head height, its box spanning about 270–336 (1.60–2.00 m) | 336 (2.00 m), the SAME overall height as the dresser (Frank, 27 Oct) |
| Small larder fridge | — | 143 (0.85 m) |
| Dresser | counter shelf 151 | 336 (2.00 m) |
| Kitchen table | TABLE TOP 128 (0.76 m) | 128 |
| Wooden chair | SEAT 76 (0.45 m) | 151 (0.90 m) back |
| Wall cupboard | bottom 244 above the floor line (1.45 m) | 101 (0.60 m) tall |
| Kettle / toaster / stand mixer | sits ON a surface | 42 / 34 / 59 (0.25 / 0.20 / 0.35 m) |
| Pedal bin | — | 101 (0.60 m) |
| Doors (side walls, front edge) | — | 336 (2.00 m) |

- Every back-row item stands with its feet on y 485, so ALL worktops, the sink top, the hob and the dresser's counter shelf form ONE straight line at y 334. Counter items stand ON that line (their feet at y 334) at their host's stop; they never float. Each host records `surfaceYPx`; the engine places counter items on it.
- The table and chairs stand slightly forward (feet y 492); the chair seat sits just below the table top.
- Separate doors with complete interiors, the oven layer stack, status lamps on electrical items and the one-drawing rule (section 10c) all still apply. Pet bowl out for now (D18).
- Broom → basic hoover → super hoover live behind the right door. The door tiers in `data/upgrades.csv` (old wooden door → knocker and peephole → smart door) now belong to the lobby's DOORBELL beside the left door (bell → intercom → Door-o-Matic).

**Other Day-1 rooms (proposed budgets for the fit check):**
| Room | Items (max bays) | Total |
|---|---|---|
| Entrance lobby + utility (ground floor) | Exact layout: `docs/layout/lobby_v6_schematic.json` (APPROVED, Frank 27 Oct). Left door = hallway (stairs + front door); doorbell; hat stand; boot bench; weather instrument; shoe station; ceiling clothes airer; washing machine with basket on top; hand basin and mirror; right door = downstairs WC (signed). No windows, no back-wall door, no internal doors | (D17) |
| Living | CRT TV unit 2, bookshelf 2, piano 3, armchair 2 (tools behind the right door) | 9 of 14 |
| Bedroom + en-suite | (old 1536 numbering; re-lay on the 2048 module at the bedroom proof) Bedroom bays 1–8: bed side-on 4 (four-poster in the same reservation, with OCCUPIED state), bedside table with phone 1, desk 2. En-suite bathroom bays 9–14: basin 1, bath 3, shower 1, towel rail 1; WC behind the right door | 14 of 14 |
| Lamp room (lantern grid) | Lamp mechanism 2, telescope 2 | 4 of 12 |
- Bedroom walkY: bed 0.95 m deep + 0.40 m → y 517.
- Lobby walkY: 0.60 m appliances + 0.40 m → y 502.
- The en-suite is a bathroom in bays 9–14 (section 3k) with basin, bath and shower; the WC is behind the right door. Bedroom proper: bays 1–8. Confirm in the Day-1 layout proof (D12).

### 10c. States
- **ABSOLUTE RULE — ONE IDENTICAL DRAWING, REPLACEABLE ELEMENTS ON TOP (Frank, 27 Oct).** Every item is ONE drawing, and that drawing is byte-identical in every state: off, on, in use, broken, being repaired. Nothing in the drawing ever changes for a state. No flapping or open doors for broken, no sagging, no scorch marks, no different knobs, no lit versions, no redrawn variants. Everything that changes is a separate, replaceable element positioned from points recorded in `item.json`, and almost all of it is drawn by the ENGINE, not by Codex:
  - light behind glass (oven window, screens): `lightRectPx`, engine-drawn glow (see below);
  - the STATUS LAMP on every electrical item: `statusLampPx`, engine-drawn dot (section 10d);
  - fault effects (smoke, steam, sparks, drips, puddles, shake): `effectOriginPx` and the shared FX kit (section 10f);
  - occupancy (keeper sitting, lying in bed): the keeper sprite placed at a recorded anchor.
- UPGRADE PRINCIPLES (Frank, 27 Oct; applies to every room): EVERY interactive item has three tiers. Tier 2 is a better version (faster, more reliable/fewer faults, more satisfying, bigger capacity). TIER 3 is always a wacky inventor's CONTRAPTION in the spirit of Professor Branestawm, W. Heath Robinson and Wallace-and-Gromit-style gadgets (mood: `reference/kitchen-mood/tier3-mood-*.png`, local only; vibe only, never copying any character or design): pulleys, string, brass, cogs, bellows, levers, little chutes, steam; it looks amazing, does something delightful automatically (e.g. a self-loading dishwasher so dishes never stack up, toast catapulted onto the plate) and almost never breaks. Rules still apply: it stays inside its item's reserved slot width, may climb the wall ABOVE its own slot (never over windows; wall decor is placed outside those columns), is ONE drawing, and its moving bits (wheels, pulleys, pistons) are separate small sprites the engine animates. All three tiers of a slot are drawn to fit the same reserved slot, which the schematic fixes from Day 1.
- UPGRADES GROW UP, NOT OUT (Frank, 27 Oct): every room keeps ONE fixed width for its whole life. Each item's slot is reserved on the room's schematic for its largest tier; tier-3 contraptions get their drama by climbing the wall and ceiling above their own slot. No ordinary upgrade widens a room or the tower, so no floor is ever left sparse. Whole-tower widening that pulls the island apart (docs/EXPANSION_DESIGN.md) is kept only for rare spectacle unlocks (boathouse, lido and the like), and sideways bulges only for balconies (diving board, hot tub).
- KITCHEN BULGE (Frank, 27 Oct; future option): rooms can always be made bigger; the kitchen, which naturally holds the most kit, is a good candidate for a sideways BULGE out through the tower wall (like the balcony extensions) if its contents ever outgrow the module.
- TIER 3 OPENS A ROOM (Frank, 27 Oct): fully upgrading certain items unlocks a whole themed floor via the dawn reveal, and the contraption MOVES UP into its new room as the centrepiece; its old slot reverts to the tier-2 item. Pairings (draft): weather instrument (thermometer → barometer → satellite Weather Engine) → Weather Station; Pianola Engine → Music Room; Observatory telescope → Observatory; Library Engine → Library; Televisor → Cinema; Inventor's Desk → Workshop; Reef Engine → Aquarium; Greenhouse Engine → Greenhouse. Growth is mostly UPWARD (new floors); whole-tower widening that pushes the island apart happens only a few times as milestone spectacles, and whenever it does every room's schematic must have a filled-in wider version so no floor looks sparse.
- DISHWASHER (Frank, 27 Oct): a brand-new purchasable item, not on Day 1: it takes a reserved 1-unit slot beside the sink (the Day-1 cupboard there is replaced when bought) and then has its own tiers (t3 = self-loading contraption).
- KITCHEN UPGRADE LIST (Frank, 27 Oct; replaces the kitchen rows of data/upgrades.csv). Tier-3 contraptions are BUILT OUT OF the original item, massively upgraded (steampunk-leaning British inventor: visible gears and pulleys, brass, gauges, flashing bulbs, steam), each with a brass maker's NAME PLATE (e.g. 'TOASTOMATIC Mk III').
  | Item | Tier 1 (Day 1) | Tier 2 | Tier 3 contraption |
  |---|---|---|---|
  | Cooker (double slot) | old-school cooker, eye-level grill | cottage range | BAKE-O-MATIC: bellows, copper pipes up the wall, pressure gauges, steam whistle when done, pies out on a little conveyor |
  | Fridge (double slot) | tall single fridge-freezer (1 unit, left end of the kitchen, worktop ends square against it) | American-style double-door | FROST ENGINE: brass cooling coils up the wall, frosty vapour, crank drops an ice cube down a chute into a glass |
  | Hot drinks | Brown Betty teapot | simple coffee machine (keeps a teapot on its warming plate: tea is never lost) | GRAND ESPRESSO CONTRAPTION: tall glass cylinders of beans feeding a cog-driven grinder and copper boiler, dials, steam, whistle; the cup rides a tiny conveyor; teapot still on its warmer |
    | Toaster | two-slice | four-slice | TOAST CATAPULT: spring arm flips toast into a toast rack |
  | Mixer (on the dresser counter) | stand mixer | food processor | ROBOCHEF: a robot chef that cooks meals on demand; replaces the whole dresser when built (Frank, 27 Oct) |
  | Dishwasher (new purchase, 1-unit slot beside the sink) | basic | quiet and fast | SELF-LOADER: an arm collects plates, brushes scrub, plates stack themselves |
  | Bin | pedal bin | recycling bins | COMPOST ENGINE: crank grinder, pipe into the wall marked 'TO GARDEN' |
  | Cleaning (behind right door) | broom | hoover | super hoover |
- WALL CUPBOARDS BELONG TO THE BASE CABINET BELOW (Frank, 27 Oct): each wall cupboard is part of the same item as the base cabinet beneath it. When an upgrade (e.g. a double-slot range or fridge, or a climbing tier-3 contraption) takes over that cabinet's slot or wall column, the wall cupboard goes with it. Other wall decor (clock, calendar, spice rack) is placed only above slots that never get a climbing contraption.
- PRODUCTION ORDER: tier 1 first (V1); tiers 2 and 3 as a later dedicated batch in the same style, every slot and wall column reserved on the schematic from Day 1.
- KITCHEN PROPS (Frank, 27 Oct): TEA is a Brown Betty TEAPOT with cups (he pours himself a cup; it replaces the kettle as the tea item). The RADIO is a fully interactive item: switch on to hear the weather forecast (tied to the weather system) or music; electrical, so it has a status lamp. Decorative/ambient: wall clock showing game time, calendar showing the game day, spice rack, bread bin (draining rack dropped, Frank 27 Oct). No props on windowsills or in front of glass.
- OPENING DOORS IN THE KITCHEN (Frank, 27 Oct; larder removed 28 Oct): the FRIDGE and the OVEN are the kitchen's doors that open, each a separate door sprite over a complete interior.
- APPLIANCE DOORS ARE SEPARATE PARTS FROM DAY ONE (Frank, 27 Oct): the cooker's oven door and the fridge door are drawn as their own sprites, and the body is drawn with its INTERIOR complete underneath (oven cavity with shelf and back wall; fridge shelves with a few items), so nothing is ever hidden that would need redrawing. Each door records its `hingePx` (pivot point) and closed position in `item.json`. The engine (or Frank in the studio) can then show it closed, open, or hanging off its hinge at any angle, purely by positioning or rotating the same door sprite. The body drawing never changes. A broken cooker MAY use the hanging-door pose as part of its fault recipe.
- OVEN LAYER STACK (Frank, 27 Oct), back to front, all registered to points in `item.json`:
  1. ENGINE LIGHT: a warm glow rectangle filling `lightRectPx` (the cavity). Off = none; On = steady; Broken = random flicker.
  2. COOKER BODY: one unchanging drawing. The oven cavity (back wall, side walls, shelf runners, shelf) is drawn as line work over partly see-through dark tint, so the engine light glows through it.
  3. OVEN CONTENTS on the shelf at `contentsPx`: none (empty, Off), a dish cooking (On), or the SAME dish burnt and charred (Broken). Two small sprites (cooking, burnt) with identical outline and position; only the colouring differs.
  4. OVEN DOOR: its own sprite at `hingePx`; its window is see-through tinted glass (partial alpha), so the light and contents show through it at ANY pose: closed, open, or hanging off askew. A hanging door may also reveal the cavity directly.
  5. FX: smoke from `effectOriginPx` (more when the door hangs off), status lamp at `statusLampPx`.
- The only drawn extras ever allowed are genuine moving parts needed for normal use (for example a fridge door opening when he takes food out). Each is a separate small sprite over the unchanged drawing, never a whole redraw, and it is never used to show a fault.
- Verification: the item's drawing has ONE hash across all states; any state that changes the drawing's pixels fails the build.
- One drawing per item per tier, in its neutral (off) appearance. It is the ONLY full drawing the item ever has.
- LIGHT OVERLAYS replace drawn ON and FLASHING states. Any part of an item that lights up (oven window, fridge interior, lamp bulb, TV screen glow, radio dial, indicator LED) is a separate small overlay sprite with a declared rectangle in `item.json` (`lightOverlays[{id, file, rectPx}]`). The engine controls each overlay: `off`, `on` (steady), `pulse`, or `flicker` (random intervals and brightness). Example: the cooker is one OFF drawing plus one "oven window lit" overlay. No flicker frames are ever drawn.
- PREFERRED LIGHT METHOD — ENGINE LIGHT BEHIND GLASS (Claude, 27 Oct; the overlay-registration problem behind the long-running broken-oven flicker): wherever a light sits behind glass (oven window, fridge interior seen through a door, TV screen, lamp glass), the item drawing leaves the glass as a see-through region (dark tinted glass at partial alpha, with the interior shelf/loaf drawn as line work on it) and records `lightRectPx` (the exact glass rectangle, or a mask file). The ENGINE draws the light itself BEHIND the drawing: a warm glow rectangle filling `lightRectPx`, steady for On, randomly flickering for Broken. Small indicator lamps are a recorded `indicatorPointPx`; the engine draws the dot. No separately drawn glow sprite has to line up with anything, so a redraw cannot break it.
- Moving parts that can't be done with a light overlay (fridge door opening, cupboard door swinging, TV picture) are the only drawn extra frames, and each is a separate small overlay over the OFF master, not a redraw of the whole item.
- Every overlay or derived frame differs from the master only inside its declared rectangle (pixel-diff verified).
- Never drawn: broken, dirty, open-for-broken or alert variants. Faults are section 10f.

### 10d. Fault indicators
- FAULTS HAVE CONSEQUENCES (Frank, 27 Oct): a broken item's fault should matter in play, e.g. a broken radio alarm means he oversleeps.
- STATUS LAMP (Frank, 27 Oct): EVERY electrical item (cooker, fridge, washing machine, dryer, kettle, toaster, mixer, TV, radio, lamp, computer and so on) has a small lamp bezel drawn into its art, unlit, at `statusLampPx`. The ENGINE lights it: steady GREEN when the item is working normally; an angry, intermittently FLASHING RED when it is broken. Flashing versus steady (not just colour) carries the meaning, for colour-blind players. Non-electrical items (sink, table, bin) have no lamp; their faults show through FX only (drips, puddle, wobble). Tapping the item or its lamp sends the keeper.
- TOWER and ISLAND views: a room-level badge on the affected room and, off-screen, edge indicators (section 13).

### 10e. Item metadata (minimum)
`id, tier, widthPx, reservedWidthPx, midpointStop, workingPointPx, fitted | freestanding | counter, realSizeM, canvasPx, anchorPx, standPointX, lightOverlays[], movingPartOverlays[], interactionAnchors[{id, offsetPx, facing}], bubbleOriginPx, effectOriginPx, statusLightPointPx, faultRecipes[], palette, styleReference, sourceSha256, files{}`.

### 10f. Fault effects kit (no broken art, ever)
- Every fault is an engine RECIPE layered on unchanged item art, combining:
  1. SHAKE: whole-sprite jiggle, now and then (no art).
  2. LIGHT FAULT: the item's own light overlay driven to flicker, stutter or die.
  3. PARTICLES: shared small animated sprites: smoke puff, sparks, steam, drips.
  4. FLOOR DECALS: placed in front of the item, never on it: a spreading puddle, a scorch smudge.
  5. STATUS LAMP flips from steady green to flashing red (section 10d).
  6. SFX: clunk, fizz, drip, alarm beep, plus an onset chime.
  7. FIXED: sparkle burst and a "ding" when the keeper sorts it.
- Example recipes: cooker = stuttering window glow + smoke + occasional bang with shake; dishwasher = spreading puddle + drips + beeping LED; fridge = flashing red lamp + cold mist and a drip puddle; lamp = flicker → sparks → dark.
- **ONE FAULT AT A TIME (Frank, 27 Oct): game rule.** Only one item in the whole lighthouse can be broken at any moment. No new fault starts until the current one is repaired. This replaces the grown-up 'maximum concurrent faults' setting (fixed at 1; the frequency setting stays). Because there is only one, its sound is the player's guide: the fault's SFX loops from the broken item, panned left/right by its position on screen and quieter the further away its floor is, so the player can find it by ear even if they miss the game director's pop-up.
- The kit is about 8–10 small sprites, made once (Codex task after the kitchen proof). A new fault never needs new art.
- The approved kitchen sheet's drawn broken states (flooding sink, falling doors, burnt toaster, cracked kettle, spilt bin) are reference for these effects only, not production art.

## 11. Island and outdoor art
- Same units as the tower: 1 module width (FW) = 2048 px; 1 bay = 84 px. Major plots use module-width units; facilities may use whole-bay increments. The "12 lp outdoor grid" is withdrawn.
- Ground line level with the entrance lobby's floor-slab top. Same front-on top-reveal projection and 168 px/m scale as the rooms.
- Day 1: full island rock including below a level waterline; short grass; rough grass and rocks on uncleared ground; play lawn; vegetable bed; barbecue terrace; cliff steps; wooden jetty; moored rowing boat with outboard; empty future plots; separate surface and edge pieces where expansion needs them.
- Never in the foreground master: sky, sea, clouds, birds, waves, horizon, distant islands, ships.
- Later plots (catalogue list plus play lawn, beehives, shed, spare plot) are listed with sizes for approval before drawing.

## 12. Rendering, mips and zoom
**Layers, back to front:** sky (time of day, weather; clouds and birds as engine sprites) → sea → island and tower foreground → items, keeper, FX → waterline wave band (y from the art manifest) → weather overlay, UI, edge indicators.

**Scaling:**
- World geometry is always 1:1: no asset is ever scaled relative to another. Display scaling applies uniformly to the whole composed view, so relative line weights stay consistent.
- Review and approval happen at 1:1 delivered px.
- ROOM view: the module (2048 × 576) fits the viewport width, or on narrow screens the camera frames the keeper and pans with him; leftover margin shows tower exterior and sky, never stretching.
- TOWER and ISLAND views use pre-generated, reviewed mip levels (1/2, 1/4, 1/8 where needed). Thin critical features (window bars, railings, the keeper's face, status lights, item legs, structural seams) get declared minimum-feature preservation or a hand-corrected mip. The runtime picks the nearest larger mip and downsamples smoothly from it (never more than 2×).
- Transitions: a jump cut, or a glide that pans at the outgoing view's scale, then crossfades (about 0.25 s) to the incoming view. Camera position snaps to whole display pixels.
- Engine work this needs: mip-set selector per view, viewport fitting, pixel-snapped camera, two-layer crossfade. A planned task, not a blocker.

**Ghosting:** a runtime tint (about 25% saturation, 55% brightness) on non-active floors. It keeps edges and alpha, never needs separate art, and never applies to event overlays or alerts.

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
- Decided: hidden circulation over visible stairs, lift or slide art; boathouse under the lobby over shore placement; engine fault recipes over broken frames; bay indices over free-x; CRT family retained.
- Snooker: approved in principle as a LATER dedicated room unlocked by buying the table (CENTREPIECE). It stays in the games hall's catalogue entry until that room is specified and approved. No V1 impact.

## 15. Engine migration (Claude)
- New geometry module using world units = delivered px, with the module, bay, window, door, floor and per-room walkY constants from section 3, generated from `tower_kit.json` and room layout files rather than hard-coded.
- One-off converters for any stored legacy ku/lp coordinates (saves, layouts) into world px, with tests. Old geometry code is kept until the converter is verified, then marked deprecated, not deleted, until Frank approves removal.
- The 172-handoff drag-and-drop contract is retired (the player never moves items). Its route and clearance checks are re-expressed on the 14-bay grid: walk-in zone clear, reserved footprints non-overlapping, windows unoccluded, every interaction anchor reachable on the step lattice, keeper action envelopes unobstructed.
- Draw order by placement y: back-row items → items behind walkY → keeper → items in front of walkY → occluding doors and jamb.
- Asset loading reads only manifest-listed runtime derivatives and verifies hashes in dev builds.

## 16. Christmas version (V1) — target 20 Dec 2026
- Players: Ralph (7) and Eddie (11), separate saves and difficulty.
- In V1: Day-1 tower (entrance lobby with laundry, kitchen, living room, bedroom with en-suite, lamp room), island scenery with the boat at the jetty; needs bars; daily credits based on each need ending the day green (rules per D9); everyday activities (eat/cook, sleep, wash, toilet, clean, laundry → washing line, relax, lamp duty) via rear-work and bubble stories; pyjamas; faults and repair per section 10f; day/night and basic weather backdrop; camera per section 13 (simplified); base-tier items only; upgrade spending only if it fits. Existing features (typed commands, phone, day report, quizzes): keep if solid, hide if flaky.
- Not in V1: full catalogue conversion, tier-2/3 furniture art, bespoke per-activity animation, new bubble vocabulary, other costumes, lair, boathouse unlock, multi-module widening, advanced weather, island facilities, snooker room, non-essential mini-games, maths and admin dials, gifting.
- Production order: Gate 0 → kitchen proof v3 → magenta pipeline → ROOM/TOWER/ISLAND style proof → lock palette and grid → keeper canon manifest → master module and kit → Day-1 tower and island → base-tier items → fault effects kit → minimal keeper clips → bubble integration → UI, needs and credits art → sky, sea and weather layers → verify all activity flows → multi-zoom, palette, gutter and magenta verification → stabilise and release.
- Indicative schedule: 26 Oct–2 Nov spec, kitchen proof, pipeline · 3–9 Nov kit and canon manifest · 10–23 Nov rooms, island, base items · 24 Nov–6 Dec keeper clips, bubbles, UI, backgrounds · 7–13 Dec integration · 14–19 Dec bug fixing and polish · 20 Dec release.
- Art freeze: once Gates 0–2 pass, style, palette and grid are frozen until 20 Dec; changes need Frank's explicit decision.

## 17. Gates
- **Gate 0 (Frank):** approve the ligne-claire style with V7 as style authority; the 2048 × 576 module with 20 stops 84 px apart; scale 1 m = 168 px with the Prime Keeper 1:1 at 298 px; 2.0 m room depth with per-room walkY; the minimal animation strategy; bubble-story retention; no-reflow reserved footprints; 1–3 module widening.
- **Gate 1:** the exact-magenta master survives the build unchanged and produces a verified exact-match RGBA derivative.
- **Gate 2:** one representative room (the kitchen) is approved at ROOM, TOWER and ISLAND scale (including mips and the lantern width).
- **Gate 3:** the Prime Keeper contract and approved clips are recorded in `active.json` with hashes.
- **Gate 4:** one- and multi-module assemblies pass geometry and pixel-diff checks.
- **Gate 5:** maximum reserved footprints fit all four Day-1 rooms, with no window occlusion.
- **Gate 6:** one complete activity runs: walk → stop on the bay centre → turn → rear work → bubble → completion → neutral.
- **Gate 7:** all sheets pass gutter, ownership, alpha, palette, anchor and metadata checks.
- **Gate 8:** the complete Day-1 loop works in all three views with no missing art, stale legacy geometry or unverified assets.

## 18. Open decisions and proposals
- D7 (style): ligne claire, V7 as style authority (Frank, 26 Oct). Formal confirmation at Gate 0.
- D8 (grid): 2048 × 576, 20 stops 84 px apart, free widths, 168 px/m, 2.0 m depth, per-room walkY. Formal confirmation at Gate 0 after the kitchen proof.
- D9 (V1 gameplay rules): needs bars, decay rates, activity restores, day end, credit rules. To be settled at the Claude Code kickoff and recorded in section 16.
- D11: lantern width (proposed 1072 × 576 px, 12 bays). Confirm at Gate 2.
- D12 RESOLVED (Frank, 26 Oct): every floor's right door hides the cupboard of myriads or the WC (signed) in the lobby and the bedroom floor; the en-suite is a visible bathroom in bays 9–14 (section 3k).
- D14 RESOLVED (Frank, 26 Oct): no utility cupboards in rooms; the right door replaces them.
- D15 OPEN, BLOCKING exact stops: approve the Prime gait re-time (start/stop 42 px each, max +4 px cumulative change) and the F5 opposite-foot stop, so every lattice point is reachable. The kitchen proof renders both versions.
- D17 RESOLVED (Frank, 26 Oct): ground-floor entrance lobby with boot room (the lobby's cupboard), laundry and a downstairs WC; kitchen on the first floor; laundry → washing line on the lawn is a V1 activity. Exact bay layout to be confirmed in the lobby proof.
- D16 NEW: bed footprint. In a 2.0 m-deep room the bed must be shown side-on, so it needs 4 bays (2.0 m), with the four-poster in the same reservation. This replaces Frank's earlier "bed 2 bays → four-poster 3 bays" decision, which predates the new scale. Frank to confirm.
- D13 RESOLVED (Frank, 26 Oct): toilet use is always hidden behind the WC door; no bathroom pose.
- Catalogue register items (marine lab, radio room, greenhouse, transport, power, bank, bowling/gaming/hot-tub/roof, solar tracker) remain open as listed there.
- D18 IN PROGRESS (27 Oct): the full upgrade design now lives in `docs/UPGRADE_MATRIX.md` (DRAFT for Frank). The live game's `data/upgrades.csv` is updated by Claude Code only after approval, room by room. Earlier note:  review of `data/upgrades.csv`, room by room, as each room is built (kitchen first, once its proof is approved). Known issues to resolve then: fridge t3 'pet cannot steal' (no pet in V1; the pet bowl itself is provisional); door tiers move to the lobby front door; bedroom basin tiers vs the en-suite's basin, bath and shower; toilet tiers now invisible (sound/behaviour only, or drop); TV t2 flat-screen vs the CRT-family decision; new upgrades for lobby laundry and garden shed; largest-tier widths in the living room (grand piano, cinema wall, library wall); jetty t3 vs boathouse; garden t3 vs greenhouse facility; modern vs retro tone. Until then the table stands, except that the fridge t3 pet clause is ignored.
- D19 RESOLVED, BUILT, NOT YET LIVE (Frank, 15 Oct; built 27 Oct in `31030e67` on origin/main, `src/game/bills.ts`): BILLS AND OVERDRAFT. Each night power and heating bills are paid from what is left in his purse first, then from the day's allowance; the 40-credit carry cap applies after the bill. Starting-kit bill 7 credits (power 4, heating 3: 2 standing heating charge + per-object running costs by tier); efficient upgrades save, comfort upgrades cost more; a stormy day multiplies heating by 1.5. Overdrawn is gentle: red balance, upgrades/shop/pizza refuse, grown-ups' gifts still arrive, keeper loses a little spirits each overdrawn morning, nothing switched off; floor at −20 (anything beyond is let off). Grown-ups' dials: billsOn, billScale %, overdraftLimit. Day report itemises bills; upgrade button shows the change to the nightly bill. Reverses the 8 Oct bank-room 'no overdrafts' line (EXPANSION_DESIGN.md updated). OPEN: whether it is on in the V1 Christmas build (section 16).
- Proposed changes: (none yet)

## 19. Work items: GitHub Issues (Frank, 28 Oct)
- All work, tasks and agent-to-agent messages live in GitHub Issues: https://github.com/frankwwebster-arch/lighthouse-keeper/issues. Read-only mirror for Codex: `docs/ISSUES.md` (Claude regenerates it).
- Labels: `needs-frank` (waiting on Frank) · `go` (Frank has said go) · `codex` / `claude` (whose job) · `agent` (an agent can do it alone, no input from Frank) · area labels (`kitchen`, `lobby`, `rooms`, `shell`, `planner`).
- Codex starts ONLY issues labelled both `codex` and `go`, closes them with `Fixes #n` in the finishing commit, and writes questions or blockers to `docs/CODEX_REPLIES.md` (Claude moves them onto the issue).
- History (former agent notes and the change log): `docs/SPEC_HISTORY.md`.

## Change log
Moved to `docs/SPEC_HISTORY.md` (28 Oct 2026). Append new dated lines there.
