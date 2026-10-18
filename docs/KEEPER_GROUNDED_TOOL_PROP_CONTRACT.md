# Grounded tool prop contract

_Recorded 18 October 2026. Source of truth for the dimensionally registered
traditional broom in Prime `keeper_sweep_broom` V2, and for the reusable
movement/occlusion rules for compatible grounded-tool actions._

## Reuse boundary

The **cupboard handoff and root-motion route** are reusable for a Hoover and
other compatible grounded-tool tasks: normal walk into the cupboard, change
only while the Keeper is fully occluded, then emerge in the tool-action gait;
repeat the same fully occluded swap on return. The action artwork itself is not
generic. A Hoover needs its own head, hose/body, handle and contact evidence;
a lawnmower needs its own wheeled deck, handle, wheel/floor contacts and a
turning radius. Neither may reuse visible broom pixels or be presented as an
approved broom variant.

Every future grounded-tool candidate must remain versioned and reversible,
keep the prop as a separately owned layer, derive visible Keeper pixels from
its applicable Prime authorities, and verify all prop/hand/floor contact and
cell gutters independently.

## Common runtime handoff

The reusable route is a **state-machine contract**, not a mandate to reuse the
broom drawing or sweep timing:

1. approved standard walk right into the cupboard;
2. one fully hidden closed-door frame, at which the normal-walk state may swap
   to the tool-action state;
3. outward tool gait with root motion and leg phase appropriate to the tool;
4. an explicitly authored turnaround (or a separately documented proxy);
5. return tool gait with root motion and leg phase;
6. one fully hidden closed-door frame, at which the tool state may swap back to
   normal walk;
7. approved standard walk left out of the cupboard.

The duration of steps 3–5 remains gameplay-owned (for example, hygiene state),
not baked into the art. Any prop whose real-world staging cannot enter the
cupboard must use a different handoff, rather than silently applying this one.

## Prime broom V2: fixed rendering dimensions

All dimensions below are **source pixels in the 384 × 320 action cell**. The
cell floor is `y=315`; the broom is drawn at 4× supersample then binary-alpha
reduced. Use the named axes per pose: `v` is the normalized handle direction
from upper hand to lower hand, and `p=(-v_y, v_x)` is the cross-handle axis.

| Element | Registered dimension / anchor | Required appearance |
| --- | --- | --- |
| Handle | 13 px dark outer stroke; 9 px timber body; 2 px warm highlight. Its top is 14 px opposite `v` from the upper-hand centre. | Straight wooden shaft, not a tubular vacuum handle. |
| Collar / ferrule | Centre pinned to `y=254`; clamped to `x=190…340`. 18 px across `p`; 13 px along `v` (`-6…+7`). | Dark-edged iron ferrule with a 1 px light edge. |
| Timber stock | Centre is 8 px below the ferrule on `v`; 44 px across `p`; 12 px along `v`. | Solid timber cross-stock with dark outline and a 1 px timber highlight. |
| Bristle envelope | Starts at the stock's lower edge; 38 px across `p` at root, widening to a 58 px floor footprint (`floor centre ±29 px`). The floor ends land at `y=315`. | Straw, tapering from stock to floor; never a rectangular mop pad. |
| Bristles | 13 individually visible 2 px strands. Roots span 34 px across `p`; endpoints span the full 58 px footprint and alternate `y=315/314`. | Two straw tones: light `#F6C261`, dark `#A16625`; envelope base `#CF9139`. |
| Bindings | Two 2 px dark bands at 7 px and 14 px from bristle start along `v`; each spans 42 px across `p`. | Visible bound-straw construction. |
| Stock / shaft colours | Shaft body `#7E461C`, highlight `#E19D4C`; timber stock `#8B4D1F`, highlight `#E09541`; ferrule `#534840`, edge `#B29F84`; outline `#0A0F14`. | Preserve these component roles, not just an averaged brown. |

### Pose anchoring and ownership

- Measure two actual hand centres per authored pose. Derive `v` from those
  centres; if an unreliable pose falls below a downward component of `0.72`,
  use the bounded fallback `(±0.18, 0.984)` only and record it.
- The collar stays on `y=254`, the bristle tips stay on floor row `315`, and the
  stock/bristle geometry follows the computed handle axis. Clamp only the
  collar x-position to `190…340`; do not scale components to hide overlap.
- Render raw prop first, then mask its pixels behind the opaque actor. The
  actor remains wholly Prime-derived; the prop has its own layer, source hash,
  bounds and contact measurements.
- Keep at least a four-pixel transparent gutter to every action-cell edge. The
  prop may meet the floor datum but must never leak alpha onto a shared cell
  edge.

### Evidence and acceptance gates

The V2 visual-reference image is
`art/drafts/keeper-prime-sweep-broom-2026-10-18-v2/sources/generated/traditional-broom-detail-reference-generated.png`
(`cfb638200c1eff8d078798561fab4ee06896e8f23d567bd6047734a02c296214`). It
informs construction only; the deterministic registered layer is authoritative
for V2.

For each future broom reproduction, record: both hand centres, handle top,
collar centre, bristle-floor row, component dimensions, raw-prop and visible-
prop hashes, layer ownership, bounds, gutter result, and per-frame hand/prop
contact. Review at large, gameplay and literal 1× scales. The exact V2 records
already live in `keeper-prime-sweep-broom-v2.json` and `batch-register.json`;
they must never be overwritten.
