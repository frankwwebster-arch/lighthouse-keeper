/**
 * Placement validator (plan section 3.2). Hard rules:
 *  1. every anchor is on the lattice;
 *  2. the footprint lies inside the walls;
 *  3. the footprint stays out of every door clear area;
 *  4. within a lane, footprints don't overlap;
 *  5. every anchor is reachable from the door and from every other anchor: nothing solid, other than
 *     the two endpoints' own items, lies in the space his body sweeps between them;
 *  6. no front-lane item covers him while he walks between, or stands at, reachable anchors;
 *  7. the whole Keeper stays inside the room at and around every anchor.
 * Soft rule: "room to grow" (the next tier wouldn't fit as things stand).
 *
 * The space his body sweeps near an anchor is measured from the exact bridge poses (the registers'
 * opaque bounds), not from a nominal width: stopping, his front boot reaches 89 ku past the anchor.
 * Codex's room-grid contract: a drag is accepted only when every variant (tier) of the object fits.
 */
import { sum, DEFAULT_PROFILE, type PoseId, type RootProfile } from './locomotion'
import { poseBounds } from './routes'
import {
  anchorsAt, dirOf, doorClear, doorWallX, footprintAt, inside, onLattice, overlaps, placementPoint, solidsAt,
  type Catalogue, type Facing, type Interval, type ObjectType, type PlacedAnchor, type Placement, type Room, type TierGeometry,
} from './room'

export type Rule = 1 | 2 | 3 | 4 | 5 | 6 | 7

export interface Issue {
  rule: Rule | 'grow' | 'catalogue'
  severity: 'error' | 'warning'
  object: string
  other?: string
  /** A short reason a child can read. */
  text: string
}

export interface LayoutInput {
  room: Room
  placements: readonly Placement[]
  catalogue: Catalogue
  /** Which bridges define the body's sweep; the default is what Frank has approved. */
  profile?: RootProfile
  /** 'all': every tier of every item must fit where it stands (the room-grid drag contract). Default 'current'. */
  variants?: 'current' | 'all'
}

export interface PlacedItem {
  placement: Placement
  type: ObjectType
  geometry: TierGeometry
  xKu: number
  footprint: Interval
  solids: Interval[]
  anchors: PlacedAnchor[]
}

export function placeItems(input: LayoutInput): { items: PlacedItem[]; issues: Issue[] } {
  const issues: Issue[] = []
  const items: PlacedItem[] = []
  const seen = new Set<string>()
  for (const p of input.placements) {
    if (p.room !== input.room.id) continue
    const type = input.catalogue[p.object]
    if (!type) { issues.push({ rule: 'catalogue', severity: 'error', object: p.object, text: `There is no ${p.object} in the catalogue.` }); continue }
    if (seen.has(p.object)) issues.push({ rule: 'catalogue', severity: 'error', object: p.object, text: `There are two ${type.label}s in this room.` })
    seen.add(p.object)
    const geometry = type.tiers.find((g) => g.tier === p.tier)
    if (!geometry) { issues.push({ rule: 'catalogue', severity: 'error', object: p.object, text: `${type.label} has no tier ${p.tier}.` }); continue }
    if (!type.anchors.some((a) => a.id === p.anchor)) { issues.push({ rule: 'catalogue', severity: 'error', object: p.object, text: `${type.label} has no ${p.anchor} spot.` }); continue }
    if (!Number.isInteger(p.xKu)) { issues.push({ rule: 1, severity: 'error', object: p.object, text: `${type.label} isn't on a square.` }); continue }
    const xKu = placementPoint(type, p)
    items.push({ placement: p, type, geometry, xKu, footprint: footprintAt(geometry, xKu), solids: solidsAt(geometry, xKu), anchors: anchorsAt(type, xKu) })
  }
  return { items, issues }
}

/**
 * Everything his body can cover at an anchor when traffic comes from or goes to one side: the neutral,
 * the stop bridges arriving from that side (with the gait frame before each) and the start bridge
 * leaving towards it. provisional: a stop pose in the profile is not drawn yet, so its pixels are unknown.
 */
export function keeperEnvelope(profile: RootProfile, x: number, side: 'left' | 'right'): { extent: Interval; provisional: boolean } {
  const arrive: Facing = side === 'left' ? 'right' : 'left'
  const depart: Facing = side
  let from = Infinity
  let to = -Infinity
  let provisional = false
  const add = (pose: PoseId, facing: Facing, at: number) => {
    const b = poseBounds(pose, facing, at, 'opaque')
    if (!b) { provisional = true; return }
    from = Math.min(from, b[0])
    to = Math.max(to, b[1])
  }
  add('neutral', 'right', x)
  add('neutral', 'left', x)
  for (const phase of ['F1', 'F5'] as const) {
    const stop = profile.stops[phase]
    if (!stop) continue
    let at = x - dirOf(arrive) * sum(stop.dx)
    add(phase === 'F1' ? 'walkF1' : 'walkF5', arrive, at)
    stop.poses.forEach((p, k) => { at += dirOf(arrive) * stop.dx[k]; add(p, arrive, at) })
  }
  let at = x
  profile.start.poses.forEach((p, k) => { at += dirOf(depart) * profile.start.dx[k]; add(p, depart, at) })
  return { extent: { from, to }, provisional }
}

const hull = (xs: Interval[]): Interval => ({ from: Math.min(...xs.map((i) => i.from)), to: Math.max(...xs.map((i) => i.to)) })

type Endpoint = { kind: 'anchor'; x: number; owner: string; label: string; concealed: Interval | null } | { kind: 'door'; x: number; label: string }

export function validateRoom(input: LayoutInput): Issue[] {
  const issues = validateTiers(input)
  if (input.variants !== 'all') return issues
  // Every other variant of each item, with its neighbours as they stand.
  for (const p of input.placements) {
    if (p.room !== input.room.id) continue
    for (const g of input.catalogue[p.object]?.tiers ?? []) {
      if (g.tier === p.tier) continue
      const as = input.placements.map((q) => (q === p ? { ...q, tier: g.tier } : q))
      for (const i of errorsOf(validateTiers({ ...input, placements: as })))
        if ((i.object === p.object || i.other === p.object) && !issues.some((j) => j.object === i.object && j.rule === i.rule && j.other === i.other))
          issues.push({ ...i, text: `${i.text} (as the ${g.label})` })
    }
  }
  return issues
}

function validateTiers(input: LayoutInput): Issue[] {
  const { room } = input
  const profile = input.profile ?? DEFAULT_PROFILE
  const { items, issues } = placeItems(input)
  const label = (id: string) => input.catalogue[id]?.label ?? id
  const walls: Interval = { from: 0, to: room.widthKu }

  for (const it of items) {
    const name = it.type.label
    // 1
    for (const a of it.anchors)
      if (!Number.isInteger(a.anchor.offsetSteps) || !onLattice(room, a.xKu)) issues.push({ rule: 1, severity: 'error', object: it.type.id, text: `${name} isn't on a square.` })
    // 2
    if (!inside(it.footprint, walls)) issues.push({ rule: 2, severity: 'error', object: it.type.id, text: `${name} would poke through the wall.` })
    // 3
    for (const d of room.doors)
      if (overlaps(it.footprint, doorClear(room, d))) issues.push({ rule: 3, severity: 'error', object: it.type.id, text: `${name} is too close to the door.` })
  }
  // 4
  for (let i = 0; i < items.length; i++)
    for (let j = i + 1; j < items.length; j++) {
      const a = items[i], b = items[j]
      if (a.type.lane === b.type.lane && overlaps(a.footprint, b.footprint))
        issues.push({ rule: 4, severity: 'error', object: a.type.id, other: b.type.id, text: `${a.type.label} and ${b.type.label} are in each other's way.` })
    }

  // 5, 6, 7: sweep between every pair of endpoints.
  const ends: Endpoint[] = [
    ...items.flatMap((it) => it.anchors.map((a): Endpoint => {
      const c = a.anchor.concealedBy
      return { kind: 'anchor', x: a.xKu, owner: it.type.id, label: it.type.label, concealed: c ? { from: it.xKu + c.span[0], to: it.xKu + c.span[1] } : null }
    })),
    ...room.doors.map((d): Endpoint => ({ kind: 'door', x: doorWallX(room, d), label: 'the door' })),
  ]
  const envelope = (e: Endpoint, towards: number) => keeperEnvelope(profile, e.x, towards < e.x ? 'left' : 'right').extent
  const reported = new Set<string>()
  const once = (key: string, issue: Issue) => { if (!reported.has(key)) { reported.add(key); issues.push(issue) } }

  for (let i = 0; i < ends.length; i++)
    for (let j = i + 1; j < ends.length; j++) {
      const p = ends[i], q = ends[j]
      if (p.kind === 'door' && q.kind === 'door') continue
      if (p.x === q.x) continue
      const parts: Interval[] = [{ from: Math.min(p.x, q.x), to: Math.max(p.x, q.x) }]
      for (const [e, o] of [[p, q], [q, p]] as const) if (e.kind === 'anchor') parts.push(envelope(e, o.x))
      const sweep = hull(parts)
      const owners = new Set([p, q].flatMap((e) => (e.kind === 'anchor' ? [e.owner] : [])))
      const anchorEnd = (p.kind === 'anchor' ? p : q) as Endpoint & { kind: 'anchor' }
      const otherEnd = anchorEnd === p ? q : p
      for (const it of items) {
        if (owners.has(it.type.id)) continue
        if (it.solids.some((s) => overlaps(s, sweep)))
          once(`5:${anchorEnd.owner}:${otherEnd.label}:${it.type.id}`, { rule: 5, severity: 'error', object: anchorEnd.owner, other: it.type.id, text: `He can't get from ${otherEnd.kind === 'door' ? 'the door' : label((otherEnd as { owner: string }).owner)} to ${anchorEnd.label} past ${it.type.label}.` })
        else if (it.type.lane === 'front' && overlaps(it.footprint, sweep))
          once(`6:${anchorEnd.owner}:${it.type.id}`, { rule: 6, severity: 'error', object: anchorEnd.owner, other: it.type.id, text: `${it.type.label} would hide him on the way to ${anchorEnd.label}.` })
      }
      // 7: walls without a door; a door's own clear area covers its side. Past a wall is allowed
      // only behind the anchor's own concealing door (the far-wall cupboard).
      for (const [e, o] of [[p, q], [q, p]] as const) {
        if (e.kind !== 'anchor') continue
        const env = envelope(e, o.x)
        const doorLeft = room.doors.some((d) => d.wall === 'left')
        const doorRight = room.doors.some((d) => d.wall === 'right')
        const hidden = (from: number, to: number) => !!e.concealed && e.concealed.from <= from && e.concealed.to >= to
        if ((!doorLeft && env.from < 0 && !hidden(env.from, 0)) || (!doorRight && env.to > room.widthKu && !hidden(room.widthKu, env.to)))
          once(`7:${e.owner}`, { rule: 7, severity: 'error', object: e.owner, text: `He wouldn't fit between ${e.label} and the wall.` })
      }
    }

  // 6 and 7 at the standing anchor itself.
  for (const it of items)
    for (const a of it.anchors) {
      const stand = poseBounds('neutral', a.anchor.facing, a.xKu, 'opaque')!
      const body: Interval = { from: stand[0], to: stand[1] }
      if (!inside(body, walls)) issues.push({ rule: 7, severity: 'error', object: it.type.id, text: `He wouldn't fit beside ${it.type.label}.` })
      for (const f of items)
        if (f !== it && f.type.lane === 'front' && overlaps(f.footprint, body))
          once(`6:${it.type.id}:${f.type.id}`, { rule: 6, severity: 'error', object: it.type.id, other: f.type.id, text: `${f.type.label} would hide him at ${it.type.label}.` })
    }
  return issues
}

export const errorsOf = (issues: Issue[]) => issues.filter((i) => i.severity === 'error')

/** Hard rules plus the soft "room to grow" rule for each item's next tier. */
export function validateWithGrowth(input: LayoutInput): Issue[] {
  const issues = validateRoom(input)
  for (const p of input.placements) {
    if (p.room !== input.room.id) continue
    const type = input.catalogue[p.object]
    const next = type?.tiers.find((g) => g.tier === p.tier + 1)
    if (!type || !next) continue
    const grown = input.placements.map((q) => (q === p ? { ...q, tier: next.tier } : q))
    if (errorsOf(validateRoom({ ...input, variants: 'current', placements: grown })).some((i) => i.object === p.object || i.other === p.object))
      issues.push({ rule: 'grow', severity: 'warning', object: p.object, text: `${next.label} wouldn't fit here as things stand.` })
  }
  return issues
}

/** Catalogue invariants: tiers keep the same anchors (by construction) and the same contact datums. */
export function validateType(type: ObjectType): Issue[] {
  const issues: Issue[] = []
  const first = type.tiers[0]
  if (!first) return [{ rule: 'catalogue', severity: 'error', object: type.id, text: `${type.label} has no tiers.` }]
  const key = (c: Record<string, number>) => JSON.stringify(Object.keys(c).sort().map((k) => [k, c[k]]))
  for (const t of type.tiers) {
    if (key(t.contacts) !== key(first.contacts)) issues.push({ rule: 'catalogue', severity: 'error', object: type.id, text: `${t.label} moves a contact datum.` })
    if (t.footprint[0] > t.footprint[1]) issues.push({ rule: 'catalogue', severity: 'error', object: type.id, text: `${t.label} has a backwards footprint.` })
  }
  if (new Set(type.tiers.map((t) => t.tier)).size !== type.tiers.length) issues.push({ rule: 'catalogue', severity: 'error', object: type.id, text: `${type.label} repeats a tier.` })
  for (const a of type.anchors)
    if (!Number.isInteger(a.offsetSteps)) issues.push({ rule: 1, severity: 'error', object: type.id, text: `${type.label}'s ${a.id} anchor is a split step from its centre.` })
  return issues
}

