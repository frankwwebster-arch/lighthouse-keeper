/**
 * Exact frame and root tables for Codex's lattice proof (gate 4) and real-room proof (gate 5):
 * 1-, 2-, 3- and 4-step walks in both directions, and every route in one real room, for each root
 * profile side by side. The approved profile is compiled exactly as the game's default would be
 * (approved clips only); candidate profiles allow unapproved material and say so on every row.
 */
import { APPROVALS, DEFAULT_PROFILE, FAST_TIMING_V1, POSES, PROFILES, type RootProfile } from './locomotion'
import { anchorsAt, placementPoint, type Catalogue, type Placement, type Room } from './room'
import { DEFAULT_CONTEXT, buildFrameTable, compileDirect, compileRoute, type Endpoint, type FrameRow, type Leg, type Result, type Route, type RouteContext } from './routes'
import { CATALOGUE, LIVING_PLACEMENTS, LIVING_ROOM } from './rooms.data'
import { KU_PER_LP, KU_PER_SU, STEP_KU, TICKS_PER_SECOND } from './units'
import { validateWithGrowth } from './validator'

export const EXPORT_PATH = 'data/placement/route-tables-v1.json'

export const ROW_COLUMNS = ['i', 'leg', 'phase', 'clip', 'frame', 'pose', 'sha256', 'facing', 'mirrored', 'fps', 'ticks', 'startTick', 'dxKu', 'xKu', 'gaitFrame', 'boundsKu', 'visibleKu', 'approved', 'events'] as const

const rowArray = (r: FrameRow) => ROW_COLUMNS.map((c) => r[c])

export const contextFor = (profile: RootProfile): RouteContext =>
  profile.status === 'approved' ? { ...DEFAULT_CONTEXT, profile } : { ...DEFAULT_CONTEXT, profile, allowUnapproved: true }

const contextNote = (ctx: RouteContext) => (ctx.allowUnapproved ? 'for review only: may use unapproved root motion, poses or turns (see each row\'s approved flag)' : 'the default: approved root motion, timing and clips only')

function routeRecord(r: Result<Route>) {
  if (!r.ok) return { supported: false, code: r.code, reason: r.reason }
  const v = r.value
  return { supported: true, routeClass: v.routeClass, travelKu: v.travelKu, endKu: v.endKu, endFacing: v.endFacing, totalTicks: v.rows.reduce((a, x) => a + x.ticks, 0), legs: v.legs.map(legSummary), rows: v.rows.map(rowArray) }
}

function legSummary(l: Leg) {
  if (l.kind === 'turn' || l.kind === 'action') return { ...l, clips: undefined, clipNames: l.kind === 'turn' ? l.clips.map((c) => c.clip) : l.action.clips.map((c) => c.clip), action: l.kind === 'action' ? l.action.id : undefined }
  return l
}

export function latticeRoutes() {
  return PROFILES.map((profile) => {
    const ctx = contextFor(profile)
    const routes = [1, 2, 3, 4].flatMap((steps) =>
      (['right', 'left'] as const).map((direction) => {
        const to = (direction === 'right' ? 1 : -1) * steps * STEP_KU
        const r = compileDirect(ctx, 0, to)
        if (!r.ok) return { steps, direction, fromKu: 0, toKu: to, supported: false, code: r.code, reason: r.reason }
        const rows = buildFrameTable(ctx, [r.value], null)
        return { steps, direction, fromKu: 0, toKu: to, supported: true, stop: r.value.stop, walkFrames: r.value.walkFrames, distanceKu: Math.abs(to), totalTicks: rows.reduce((a, x) => a + x.ticks, 0), rows: rows.map(rowArray) }
      }),
    )
    return { profile: profile.id, note: contextNote(ctx), routes }
  })
}

export function realRoomRoutes(room: Room, placements: Placement[], catalogue: Catalogue) {
  const anchors = placements.flatMap((p) => anchorsAt(catalogue[p.object], placementPoint(catalogue[p.object], p)))
  const ends: { id: string; end: Endpoint }[] = [
    ...room.doors.map((d) => ({ id: `door:${d.id}`, end: { door: d.id } as Endpoint })),
    ...anchors.map((a) => ({ id: `${a.object}.${a.anchor.id}`, end: { anchor: a } as Endpoint })),
  ]
  return PROFILES.map((profile) => {
    const ctx = contextFor(profile)
    const routes = ends.flatMap((from) => ends.filter((to) => to !== from && !('door' in from.end && 'door' in to.end)).map((to) => ({ from: from.id, to: to.id, ...routeRecord(compileRoute(ctx, room, from.end, to.end)) })))
    return { profile: profile.id, note: contextNote(ctx), validation: validateWithGrowth({ room, placements, catalogue, profile }), routes }
  })
}

export function buildExport() {
  return {
    schema: 'lighthouse-keeper/placement-route-tables@1',
    generatedBy: 'src/placement/exportTables.ts (npm run export:placement)',
    plan: 'docs/architecture/FURNITURE_PLACEMENT_AND_LOCOMOTION.md, revision 3',
    units: { ku: 'one pixel of the 256 × 320 density-8 Keeper cell', kuPerLp: KU_PER_LP, kuPerSu: KU_PER_SU, stepKu: STEP_KU, ticksPerSecond: TICKS_PER_SECOND },
    approvals: APPROVALS,
    defaultProfile: DEFAULT_PROFILE.id,
    profiles: PROFILES,
    timing: { policy: 'data/keeper_timing_policy.json', ...FAST_TIMING_V1, rows: 'accelerate and walk rows play at walkFps, decelerate rows at decelerationFps, turns at turnFps' },
    poses: POSES,
    rowColumns: ROW_COLUMNS,
    rowNotes: {
      xKu: 'root after the row\'s delta; position changes only when the frame changes',
      boundsKu: 'room-local [from, to) of every pixel with alpha > 0; null for poses not drawn yet and for turn/action clips',
      visibleKu: 'width a door leaves visible; 0 = fully hidden; null without a room or bounds',
      mirrored: 'left travel mirrors the right-facing art about the root and negates every delta',
      approved: 'the drawing or clip on this row is approved; whether its root motion is approved is the profile\'s status',
    },
    lattice: { description: 'Anchor 0 to anchor ±84k ku. Distance must equal 84k exactly; odd k stops from F1, even k from F5.', profiles: latticeRoutes() },
    realRoom: {
      description: 'Every route among the living room\'s door and four anchors at Frank\'s 172 lp width: a seated action (armchair) and a back-facing action (bookshelf, approved Turn V9).',
      room: LIVING_ROOM,
      placements: LIVING_PLACEMENTS,
      catalogue: Object.fromEntries(LIVING_PLACEMENTS.map((p) => [p.object, CATALOGUE[p.object]])),
      profiles: realRoomRoutes(LIVING_ROOM, LIVING_PLACEMENTS, CATALOGUE),
    },
  }
}

/** JSON with each row (an array of primitives) on one line, so diffs stay readable. */
export function formatExport(value: unknown, indent = ''): string {
  const flat = (v: unknown): boolean => v === null || typeof v !== 'object' || (Array.isArray(v) && v.every((x) => x === null || typeof x !== 'object' || (Array.isArray(x) && x.every((y) => y === null || typeof y !== 'object'))))
  if (value === undefined) return 'null'
  if (flat(value)) return JSON.stringify(value)
  const next = indent + '  '
  if (Array.isArray(value)) return value.length ? `[\n${value.map((v) => next + formatExport(v, next)).join(',\n')}\n${indent}]` : '[]'
  const entries = Object.entries(value as Record<string, unknown>).filter(([, v]) => v !== undefined)
  return entries.length ? `{\n${entries.map(([k, v]) => `${next}${JSON.stringify(k)}: ${formatExport(v, next)}`).join(',\n')}\n${indent}}` : '{}'
}

export const exportText = () => formatExport(buildExport()) + '\n'
