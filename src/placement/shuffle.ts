/**
 * The shuffle (plan section 3.4) and the child's drop guidance. Frank's answers: neighbours slide
 * aside and keep their order, with one Undo (D4); a bigger upgrade offers a shuffle, otherwise says
 * what to move (D3). The shuffle moves neighbours outward by the fewest lattice steps; walls and the
 * doorway exclusion are fixed; the smallest total move wins, ties going away from the door; nothing
 * changes room. Everything is deterministic. Invalid positions are never returned as a layout.
 */
import { canonicalPlacements, spotOf, spotX, spots, type Placement, type Room } from './room'
import { STEP_KU, type Ku } from './units'
import { errorsOf, validateRoom, type Issue, type LayoutInput } from './validator'

export interface Move { object: string; fromKu: Ku; toKu: Ku }

export interface DropPlan {
  /** Green: drop to place. Amber: fits if neighbours shuffle. Grey: can't go here (cannot be saved). */
  verdict: 'fits' | 'shuffle' | 'cannot'
  /** The layout to apply (for 'cannot', the layout unchanged). */
  placements: Placement[]
  moved: Move[]
  /** Why it can't go here, child-readable; empty unless 'cannot'. */
  reasons: Issue[]
  /** The nearest snap position where it would fit, and whether that needs a shuffle. */
  nearest?: { xKu: Ku; verdict: 'fits' | 'shuffle' }
  /** For an upgrade that can't fit: items whose moving elsewhere would make room. */
  whatToMove?: string[]
}

const awayFromDoorSign = (room: Room) => (room.doors.some((d) => d.wall === 'right') && !room.doors.some((d) => d.wall === 'left') ? -1 : 1)

const valid = (input: Omit<LayoutInput, 'placements'>, placements: Placement[]) => errorsOf(validateRoom({ ...input, placements })).length === 0

/**
 * Keeps `fixed` where it is and slides the other items in its room outward, preserving their order.
 * Returns the best valid layout, or null.
 */
export function shuffleAround(input: LayoutInput, fixed: Placement): { placements: Placement[]; moved: Move[] } | null {
  const { room } = input
  const elsewhere = input.placements.filter((p) => p.room !== room.id)
  const others = canonicalPlacements(input.placements.filter((p) => p.room === room.id && p.object !== fixed.object))
  const all = spots(room)
  const lo = all[0]
  const hi = all[all.length - 1]
  const sign = awayFromDoorSign(room)
  const at = (p: Placement, s: number): Placement => ({ ...p, xKu: spotX(room, s) })
  const blocks = (layout: Placement[], object: string) =>
    errorsOf(validateRoom({ ...input, placements: layout })).some((i) => i.object === object || i.other === object)

  let best: { placements: Placement[]; moved: Move[]; cost: number; away: number } | null = null
  for (let b = 0; b <= others.length; b++) {
    const placed: Placement[] = [fixed]
    let failed = false
    // Left of the fixed item, nearest first, each moving left only as far as it must; then the right.
    let bound = spotOf(room, fixed.xKu)
    for (let i = b - 1; i >= 0 && !failed; i--) {
      let s = Math.min(spotOf(room, others[i].xKu), bound - 1)
      while (s >= lo && blocks([...placed, at(others[i], s)], others[i].object)) s--
      if (s < lo) failed = true
      else { placed.push(at(others[i], s)); bound = s }
    }
    bound = spotOf(room, fixed.xKu)
    for (let i = b; i < others.length && !failed; i++) {
      let s = Math.max(spotOf(room, others[i].xKu), bound + 1)
      while (s <= hi && blocks([...placed, at(others[i], s)], others[i].object)) s++
      if (s > hi) failed = true
      else { placed.push(at(others[i], s)); bound = s }
    }
    if (failed || !valid(input, placed)) continue
    const moved = others.flatMap((o) => {
      const n = placed.find((p) => p.object === o.object)!
      return n.xKu === o.xKu ? [] : [{ object: o.object, fromKu: o.xKu, toKu: n.xKu }]
    })
    const cost = moved.reduce((a, m) => a + Math.abs(m.toKu - m.fromKu), 0) / STEP_KU
    const away = moved.reduce((a, m) => a + sign * (m.toKu - m.fromKu), 0)
    if (!best || cost < best.cost || (cost === best.cost && away > best.away)) best = { placements: placed, moved, cost, away }
  }
  return best ? { placements: canonicalPlacements([...elsewhere, ...best.placements]), moved: best.moved } : null
}

function tryAt(input: LayoutInput, target: Placement): Omit<DropPlan, 'nearest' | 'whatToMove'> {
  const rest = input.placements.filter((p) => !(p.room === input.room.id && p.object === target.object))
  const direct = canonicalPlacements([...rest, target])
  const issues = errorsOf(validateRoom({ ...input, placements: direct }))
  if (issues.length === 0) return { verdict: 'fits', placements: direct, moved: [], reasons: [] }
  const shuffled = shuffleAround({ ...input, placements: rest }, target)
  if (shuffled) return { verdict: 'shuffle', placements: shuffled.placements, moved: shuffled.moved, reasons: [] }
  const mine = issues.filter((i) => i.object === target.object || i.other === target.object)
  return { verdict: 'cannot', placements: canonicalPlacements([...input.placements]), moved: [], reasons: mine.length ? mine : issues }
}

/** Snap positions ordered by distance from xKu, ties going away from the door. */
function byNearness(room: Room, xKu: Ku): Ku[] {
  const sign = awayFromDoorSign(room)
  return spots(room).map((s) => spotX(room, s)).filter((x) => x !== xKu).sort((a, b) => Math.abs(a - xKu) - Math.abs(b - xKu) || sign * (b - a))
}

/** Snaps a dragged anchor x to the nearest lattice line inside the walls (ties away from the door). */
export function snapX(room: Room, xKu: number): Ku {
  const all = spots(room).map((s) => spotX(room, s))
  const sign = awayFromDoorSign(room)
  return all.reduce((best, x) => (Math.abs(x - xKu) < Math.abs(best - xKu) || (Math.abs(x - xKu) === Math.abs(best - xKu) && sign * (x - best) > 0) ? x : best), all[0])
}

/**
 * Frank (project page, 14 October, question 1): a drop checks only the tier he has now; a bigger
 * upgrade later shuffles its neighbours (D3). Every room must still hold every item fully upgraded:
 * see roomHoldsFullyUpgraded. 'all' is Codex's stricter contract, kept as an option.
 */
export const DROP_VARIANTS: 'all' | 'current' = 'current'

/** A child drags an item so its selected anchor snaps to xKu (or the shop places a new one there). */
export function planDrop(base: LayoutInput, object: string, xKu: Ku, opts: { tier?: number; anchor?: string } = {}): DropPlan {
  const input = { ...base, variants: base.variants ?? DROP_VARIANTS }
  const current = input.placements.find((p) => p.room === input.room.id && p.object === object)
  const anchor = opts.anchor ?? current?.anchor ?? input.catalogue[object]?.anchors[0]?.id ?? 'use'
  const target: Placement = { object, room: input.room.id, xKu: snapX(input.room, xKu), anchor, tier: opts.tier ?? current?.tier ?? 1 }
  const plan: DropPlan = tryAt(input, target)
  if (plan.verdict !== 'cannot') return plan
  for (const x of byNearness(input.room, target.xKu)) {
    const alt = tryAt(input, { ...target, xKu: x })
    if (alt.verdict !== 'cannot') return { ...plan, nearest: { xKu: x, verdict: alt.verdict } }
  }
  return plan
}

/** The shop offers a bigger tier of an item already in the room. */
export function planUpgrade(input: LayoutInput, object: string, tier: number): DropPlan {
  const current = input.placements.find((p) => p.room === input.room.id && p.object === object)
  if (!current) throw new Error(`${object} is not in ${input.room.id}`)
  const target = { ...current, tier }
  const plan: DropPlan = tryAt(input, target)
  if (plan.verdict !== 'cannot') return plan
  const whatToMove = input.placements
    .filter((p) => p.room === input.room.id && p.object !== object)
    .filter((p) => tryAt({ ...input, placements: input.placements.filter((q) => q !== p) }, target).verdict !== 'cannot')
    .map((p) => p.object)
  return { ...plan, whatToMove }
}

/**
 * Room design helper: packs items in the given order as close to the door as the rules allow and
 * reports usedKu, the furthest footprint edge from the stair-side wall.
 */
export function packRoom(base: Omit<LayoutInput, 'placements'>, order: { object: string; anchor: string; tier: number }[]): { placements: Placement[]; usedKu: Ku } | null {
  const { room } = base
  const all = spots(room)
  const placed: Placement[] = []
  let next = all[0]
  for (const o of order) {
    let s = next
    const place = (n: number): Placement => ({ object: o.object, room: room.id, xKu: spotX(room, n), anchor: o.anchor, tier: o.tier })
    while (s <= all[all.length - 1] && !valid(base, [...placed, place(s)])) s++
    if (s > all[all.length - 1]) return null
    placed.push(place(s))
    next = s + 1
  }
  const usedKu = Math.max(...placed.map((p) => p.xKu + base.catalogue[p.object].tiers.find((t) => t.tier === p.tier)!.footprint[1]))
  return { placements: canonicalPlacements(placed), usedKu }
}

const permutations = <T,>(xs: T[]): T[][] => (xs.length <= 1 ? [xs] : xs.flatMap((x, i) => permutations([...xs.slice(0, i), ...xs.slice(i + 1)]).map((r) => [x, ...r])))

/**
 * Frank: every room must fit every fully upgraded asset. Tries every order of the room's items, each at
 * its largest tier, and returns the tightest arrangement found, or null if none fits.
 */
export function roomHoldsFullyUpgraded(base: Omit<LayoutInput, 'placements'>, objects: { object: string; anchor: string }[]): { placements: Placement[]; usedKu: Ku } | null {
  let best: { placements: Placement[]; usedKu: Ku } | null = null
  const maxed = objects.map((o) => ({ ...o, tier: Math.max(...base.catalogue[o.object].tiers.map((t) => t.tier)) }))
  for (const order of permutations(maxed)) {
    const r = packRoom({ ...base, variants: 'current' }, order)
    if (r && (!best || r.usedKu < best.usedKu)) best = r
  }
  return best
}
