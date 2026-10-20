# Kitchen Modular Asset and Join Standard

Date: 20 October 2026

Status: governing authoring method for later kitchen assets and upgrades. It
records the approved V38 split-cabinet result without promoting review art into
Final or runtime.

## Why this exists

Kitchen assets must be movable and upgradeable without breaking the continuous
fitted-galley appearance or changing the Prime Keeper's stride registration.
Earlier attempts embedded pieces of neighbouring cabinets or countertop in an
appliance sprite. Those composites looked correct in one arrangement but
created gaps, doubled furniture and stale fragments after a state or position
changed.

The durable solution has three independent concerns:

1. an immutable standalone object body;
2. exact grid placement and interaction geometry;
3. compositor-owned edge repair selected from current adjacency.

No one layer is allowed to compensate permanently for another.

## Canonical geometry

- The room proof is `772 × 224 px`.
- A normal fitted unit owns one `84 × 74 px` logical body.
- Canonical body origins are `x = 84, 168, 252, 336, 420, 504`.
- The worktop plane begins at room `y = 134`; the fitted-unit foot line is
  `y = 208`.
- Prime's stop/turn interaction point is always the midpoint of the committed
  logical footprint, at `body x + 42, y = 218` for a one-bay object.
- Transparent source cells may be wider or taller to contain a door, tap,
  effect or four-pixel safety gutter. Their declared offset maps the logical
  body back to its exact origin; cell dimensions never redefine gameplay
  geometry.

A later two-bay upgrade, such as an `84 px` oven becoming a `168 px` range,
must reserve two adjacent grid bays, expose only its two outer edges and derive
its Prime anchor from the midpoint of the complete `168 px` footprint. It must
not scale or drift the grid.

## Independent bodies

Every fridge, oven, sink, dishwasher, cabinet bay and later white good is a
complete standalone object. It contains no wall pixels and no pixels belonging
to its neighbour. Countertop repair is not baked into appliance artwork.

Interactive state families are constructed together from one model:

- Off/Standard;
- On, where applicable;
- Broken.

Unchanged casing geometry must remain identical across states. Mechanical
changes must remain physically credible: hinges stay on the same side, doors
retain their dimensions, and a bottom-hinged door opens toward the camera.

## Cabinet edge states

Approved Cabinet V11 supplies two distinct one-bay centres. Each bay has four
deterministic variants:

| Left side | Right side | Result |
| --- | --- | --- |
| exposed | exposed | both exact rounded V11 outer ends |
| exposed | joined | rounded left; exact V11 internal right edge |
| joined | exposed | exact V11 internal left edge; rounded right |
| joined | joined | both exact V11 internal edges |

These are literal source-region substitutions, not redraws. V38 verifies every
output pixel against its declared V11 coordinate.

## Snap, swap and occupancy

Pointer movement may be loose, but committed state is exact:

- an imprecise drag previews the nearest legal origin;
- release stores only an exact 84-pixel origin;
- an empty-bay layout moves into the empty bay;
- a full layout swaps the selected object with the current occupant;
- overlap, fractional positions and persisted free-drag coordinates are
  forbidden;
- each object remains independently movable; a redundant pair/group mode is
  not supplied.

The compositor recalculates every left and right neighbour after each commit.
Prime's anchor is then derived from the snapped logical body, never from the
transparent sprite cell or visible overflow.

## Broken-state movement lock and effect ownership

A movable kitchen asset becomes position-locked when its state becomes
`broken`. This is a general gameplay rule for appliances, cabinets and later
upgrades, not a dishwasher-specific exception.

- The asset retains its exact snapped grid origin and Prime interaction
  midpoint until repaired.
- Direct drag, bay-button movement and any group/layout operation which would
  move the broken asset are rejected.
- A different asset cannot swap into the occupied bay if that swap would
  displace the broken asset.
- A repair transition to Off, On or another non-broken state unlocks movement.
- Upgrading or replacing a broken asset therefore requires repair first.

Environmental effects remain separate sprite strips but are owned by their
appliance instance. Each placed layer stores `anchorAssetId`, applicable state,
asset-local `dx`/`dy`, size, crop, speed and model. Save/load must persist the
asset state, exact origin and owned layer transforms together. This makes suds,
smoke, leaking water and similar effects permanently follow their source while
the source is movable, and guarantees they cannot become detached once the
Broken lock engages. Removing an effect layer remains independently allowed.

The renderer resolves joins from the locked position exactly as it does for an
unlocked snapped position. The lock changes interaction state only; it never
bakes effects, neighbours or healing pixels into the appliance sprite.

## Join resolver and draw order

Exact adjacency means `left.x + left.width === right.x`. Only then may a repair
be drawn.

- A pair containing the oven uses the approved V32 triangular countertop
  underlay, blue body backfill and narrow neighbour-side cleanup.
- Every other compatible fitted pair uses the approved V22 blue body backfill
  and row-matched flat countertop cap.
- An exposed sink left side uses the approved V25 cutout and exact rounded V11
  end.
- An exposed cabinet side uses its corresponding V11 edge-state pixels.
- An exposed standalone appliance uses its own finished end.

The mandatory order is: room background; active backfills/underlays; immutable
object bodies; front caps/cleanup masks; independent environmental effects.
Removing or moving either neighbour must remove its former repair immediately.

## Environmental animation library

Steam, smoke, heat, water, smell, flies, suds and similar effects are separate
transparent strips. The canonical loop is forty isolated frames at 4 fps,
lasting ten seconds. Each frame must retain transparent safety gutters and one
unambiguous owner.

Reusable effects support:

- application to an explicitly selected asset/state;
- multiple simultaneous layers;
- drag placement relative to that asset;
- model/intensity choice;
- resize and crop;
- speed `0.1×–4×` while preserving the ten-second source loop;
- individual removal;
- named SFX placeholders.

The review may provide a good drafted placement, but that placement is data,
not pixels baked into the object. Appliance-specific illumination that changes
the cavity itself may remain a registered state animation when relocation
would be incorrect.

## Required review and verification

Every new or upgraded object must show all states isolated at inspection scale
and in the complete kitchen at exact game size. A movable workbench must test
both exposed sides, every relevant neighbour class and every legal occupancy
or swap permutation.

Deterministic checks must reject:

- geometry or anchor drift;
- changes to inherited approved bytes;
- Off/On casing silhouette drift;
- missing or misclassified joins;
- opaque pixels in shared sprite-cell gutters;
- empty/duplicate animation frames or strip/metadata mismatch;
- missing preload/decode gating;
- review media outside the content-addressed archive;
- accidental promotion into Final or runtime.

All work begins as a new versioned, reversible review set. Visual approval pins
that exact set; promotion remains a later explicit instruction.
