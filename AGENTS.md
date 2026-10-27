# Lighthouse Keeper: notes for coding agents (Codex and others)

> **Vercel guard (Frank, 27 Oct):** never deploy to show review art; deploy only when `docs/SPEC.md` section 19 has a GO'd DEPLOY note, at most once per day. No GIFs or review images over ~2 MB committed. See the guard in `docs/SPEC.md`.

> **Shared spec (Frank, 26 Oct 2026):** `docs/SPEC.md` is the single working spec and the shared channel between Codex and Claude. `git pull` and read it before every task; where it conflicts with older rules below or with `docs/CODEX_BRIEF.md`, the spec wins. Follow its "Shared channel" rules to update it and leave notes for Claude in its section 19.

**Deployment is manual.** Pushing to `main` does not deploy. Vercel builds only
when the newest commit on `main` has a subject line ending in `[deploy]`; branch
pushes never build.

- Commit and push freely, but never end an ordinary commit subject with `[deploy]`.
- Release once per review batch: `npm run deploy -- "short note"` (it pulls,
  adds an empty `[deploy]` commit and pushes). Frank can also use GitHub →
  Actions → "Deploy to production".
- Branch previews no longer exist. To show Frank a review page, deploy, then
  send the production link.
- Full workflow, retention policy and rollback: `docs/DEPLOYMENT.md`.

**Review media is content-addressed.** Review HTML and small JSON files remain
under `public/keeper-review`, but PNG/GIF/JPEG/WebP/AVIF evidence belongs in
`review-archive/objects`, never as a committed public binary. Oversized review
JSON (24 KiB or more) uses the same archive; small JSON remains public. After
any review builder writes evidence, run `npm run maintain:keeper-review`; it
deduplicates the bytes, updates the per-set manifests, removes only verified
public copies and checks the deployment payload. `npm test` fails if an
archiveable review payload returns or an archive hash/manifest is wrong.
Every new moving review page must preload and decode all unique frame URLs
before enabling controls or starting playback. Use a fresh versioned page and
asset prefix when correcting delivery; never rewrite an immutable old page.

## Graphics authority and absolute rules

For all new graphics work, `docs/CODEX_BRIEF.md` is the current authority.
The four blocks below are copied from its 26 October 2026 absolute rules. They
supersede conflicting historical art-direction, room-grid, Keeper-generation
and item-art guidance. Historical assets and documents remain provenance only;
this brief does not itself authorise changing approved canonical bytes. If a
required canon reference is missing, do not reconstruct it from prose.

### Magenta key colour (ABSOLUTE)

- Everything see-through is flat pure magenta `#FF00FF`: sky, sea, all window
  glass, glazed doors, lamp-room glass, boathouse sea arch, lair portholes.
  Frames and glazing bars are drawn; nothing is painted inside the glass.
- No clouds, birds, sun, waves, horizon, islands or ships in foreground art.
  The game draws sky, sea and weather as animated layers.
- Island rock is drawn in full, including below a perfectly level waterline.
- Magenta is used nowhere else. No pink or magenta room colours.

**Magenta pipeline gate:** the legacy `art/raw/` → `npm run sprites` route
removes `#FF00FF`; it is not valid for authoring or preserving new tower,
island or environment masters. Establish a reviewed, exact-magenta-preserving
delivery route before production art is created. Never pass the only master
copy through the legacy cleanup step.

### Room module grid (ABSOLUTE)

- Module: exactly 1536 × 512 px. Floor slab bottom 32 px, ceiling top 32 px,
  side walls 32 px.
- NO STAIRS are ever drawn; the stairway is hidden inside the tower wall. The
  leftmost module of each floor has one plain wooden door in its LEFT wall.
- Walk-in zone: x = 32–256, in front of the door, always empty floor.
- Bay zone: x = 256–1504, 13 bays of 96 px (numbered 1–13 from the left).
- Windows: two per above-ground module, 192 × 192 px, over bays 4–5 and 10–11,
  sills 160 px above the floor surface. Identical on every floor.
- Extra modules on a floor: joined by a 32 px interior wall with an open
  doorway; no door or walk-in zone.
- Keeper standing height about 250 px.
- Room shells are bare: walls, floor, ceiling, skirting, panelling, doors,
  window frames and listed permanent features only. No furniture, appliances,
  rugs, curtains, pictures, lamps, plants, props, stairs or characters.
- All room modules are made from ONE master module (`module_master.png`) by
  recolouring walls and adding the room's permanent features in code. Every
  other pixel stays identical; verify with a pixel diff.

### Keeper character (ABSOLUTE)

- Canon files live in `/public/art/keeper/canon/` (approved side idle, front
  idle, walk loop, turns). Never modify or regenerate them.
- Never draw the keeper from a text description. Every new pose starts from a
  canon image as the input reference and changes only the pose.
- Locked design: navy peaked cap with small gold badge; full white beard and
  moustache; pink nose; bright blue knitted jumper with two white chest stripes
  and one on each sleeve, ribbed cuffs and hem; plain navy trousers; chunky navy
  boots; stocky, about 3 heads tall.
- Forbidden: sailor collar (a recurring drift on back and shoulder views),
  scarf, coat, apron, hat changes, glasses, extra stripes, logos, weapons, any
  unrequested object, any change of face, beard or build.
- Palette: extract it from the canon side idle in code into `palette.json`
  (main colours measured: blues `#0560C4`, `#0A57B5`; navies `#263E6B`,
  `#041535`; skin `#ECD1B5`; beard `#FCF1DE`). Snap every new keeper pixel to
  it; report if more than 2% were far off.
- Size: frames 256 px tall, keeper 244–256 px, anchored bottom-centre at the
  feet. Fix size by scaling and padding in code, never by redrawing.
- Animation: 2–4 key poses per action, with motion added by the engine.
  Locomotion loops may use more frames. Every animation starts and ends on the
  neutral standing pose. Props are always separate sprites.
- Not needed: stair animations (stairs are hidden).
- Approval gate: new keeper art goes to `/public/art/keeper/candidates/` with a
  side-by-side comparison against canon. It enters the game only after Frank
  approves.

**Keeper migration gate:** the brief requires canon files at
`/public/art/keeper/canon/`, but the current repository does not yet satisfy
that requirement. Because the rule above forbids constructing the Keeper from
prose, do not create new Keeper art until Frank-approved canon references have
been installed there. Existing approved Keeper assets remain immutable during
that migration.

Hash-pinned Prime contracts and historical room/circulation handoffs must stay
byte-identical for their verifiers. They remain evidence for the installed
runtime only and do not substitute for the missing target canon or override
this brief's new-art rules.

### Items (ABSOLUTE)

- Every floor item is exactly 1 bay (96 px) or 2 bays (192 px) wide. Upgraded
  versions (e.g. range oven, 2 bays) are drawn now at final size.
- Minimal states only. Example oven: OFF, ON, INTERIOR LIGHT FLASHING (2
  frames).
- Never draw broken, dirty or alert states into an item. The engine adds overlay
  animations (smoke, exclamation marks, sparkles, drips) on top.
- Batch rule: draw one master per item, then produce every state from it in ONE
  go, changing only the element that differs (e.g. the oven's light). Every
  other pixel identical, verified by pixel diff.
- Output per item: a folder with `master.png`, one PNG per state, and
  `item.json` (states, bay width, anchor bottom-left).
- Before drawing any room's items, list them with base and upgraded bay sizes
  and confirm the fully upgraded layout fits 13 bays per module.

Roles and other project rules: `CLAUDE.md` and `docs/CODEX_TO_CLAUDE_HANDOFF_2026-10-14.md`.
