/**
 * Route compiler (plan section 4) and frame-table builder (section 5). One frame table drives both
 * frame and position: position changes only when the frame changes, every walking row carries its
 * authored non-zero delta, and a stop's last row is the exact neutral at the exact anchor. Left is
 * the mirror: negated deltas, mirror-safe art only. The compiler never stretches a stride, snaps an
 * endpoint or improvises a stop: a route it cannot build exactly is reported as unsupported.
 */
import { CELL, FAST_TIMING_V1, DEFAULT_PROFILE, POSES, WALK_CYCLE, sum, type PoseId, type RootProfile, type StopPhase, type TransitionTiming } from './locomotion'
import { dirOf, doorOf, inwardFacing, onLattice, opposite, type ActionSpec, type ClipRef, type Facing, type PlacedAnchor, type Room } from './room'
import { STEP_KU, ticksForFps, type Ku } from './units'

export type Heading = Facing | 'back' | 'front'

export interface TurnLibrary {
  /** Zero-root clips that turn him from one heading to another, or null if none exist. */
  clips(from: Heading, to: Heading): ClipRef[] | null
}

const SIDE_BACK_V9 = 'art/drafts/keeper-prime-turn-side-back-2026-10-13-v10/batch-register.json'
const FRONT_SIDE_V1 = 'art/drafts/keeper-prime-turn-front-side-2026-10-13-v1/batch-register.json'

/**
 * Keeper Prime turns as registered on 14 October 2026. Side-right ↔ back is Frank's approved nine-frame
 * Turn V9 (and its exact reverse). Front ↔ side-right is still a draft. Mirrored turns for side-left
 * have not been confirmed mirror-safe, so they count as unapproved.
 */
export const PRIME_TURNS: TurnLibrary = {
  clips(from, to) {
    if (from === to) return []
    const rightBack: ClipRef = { clip: 'keeper_prime_turn_side-right_to_back', frames: 9, approved: true, source: SIDE_BACK_V9 }
    const backRight: ClipRef = { clip: 'keeper_prime_turn_back_to_side-right', frames: 9, approved: true, source: `${SIDE_BACK_V9} (exact reverse strip)` }
    const leftBack: ClipRef = { clip: 'keeper_prime_turn_side-left_to_back (mirror)', frames: 9, approved: false, source: `${SIDE_BACK_V9}, mirrored; mirror safety unconfirmed` }
    const backLeft: ClipRef = { clip: 'keeper_prime_turn_back_to_side-left (mirror)', frames: 9, approved: false, source: `${SIDE_BACK_V9}, mirrored reverse; mirror safety unconfirmed` }
    const frontRight: ClipRef = { clip: 'keeper_prime_turn_front_to_side-right', frames: 8, approved: false, source: `${FRONT_SIDE_V1} (draft)` }
    const rightFront: ClipRef = { clip: 'keeper_prime_turn_side-right_to_front', frames: 8, approved: false, source: `${FRONT_SIDE_V1} (draft, reversed)` }
    const table: Record<string, ClipRef[]> = {
      'right>back': [rightBack], 'back>right': [backRight], 'left>back': [leftBack], 'back>left': [backLeft],
      'right>front': [rightFront], 'front>right': [frontRight],
      // About-turns go through the back, the only approved turn family.
      'right>left': [rightBack, backLeft], 'left>right': [leftBack, backRight],
    }
    return table[`${from}>${to}`] ?? null
  },
}

export interface RouteContext {
  profile: RootProfile
  timing: TransitionTiming
  turns: TurnLibrary
  /** false: any clip Frank has not approved makes the route unsupported. */
  allowUnapproved: boolean
}

/** What may be presented as the default: approved root motion, approved timing, approved clips only. */
export const DEFAULT_CONTEXT: RouteContext = { profile: DEFAULT_PROFILE, timing: FAST_TIMING_V1, turns: PRIME_TURNS, allowUnapproved: false }

export type Unsupported = {
  ok: false
  code: 'zero-distance' | 'needs-f5-stop' | 'off-step' | 'no-turn' | 'unapproved-clip' | 'no-hidden-start' | 'never-hidden' | 'bad-action'
  reason: string
}
export type Result<T> = { ok: true; value: T } | Unsupported

const fail = (code: Unsupported['code'], reason: string): Unsupported => ({ ok: false, code, reason })

/** A candidate profile may only be used where unapproved material is explicitly allowed and labelled. */
const unapprovedProfile = (ctx: RouteContext): Unsupported | null =>
  !ctx.allowUnapproved && ctx.profile.status !== 'approved' ? fail('unapproved-clip', `${ctx.profile.label} is not approved.`) : null

// ── walks ──

export interface WalkSolution { distance: Ku; walkFrames: number; stop: StopPhase }

const stopFrameFor = (phase: StopPhase) => (phase === 'F1' ? 0 : 4)

/**
 * Splits a distance into start + whole steady frames + stop. After the start he is on Walk F1, so
 * n steady frames later he is on gait frame 1 + n mod 8: a stop from F1 needs n ≡ 0 and from F5 n ≡ 4 (mod 8).
 */
export function solveWalk(profile: RootProfile, distance: Ku): Result<WalkSolution> {
  if (distance <= 0) return fail('zero-distance', 'He is already there.')
  const s = sum(profile.start.dx)
  for (const phase of ['F1', 'F5'] as const) {
    const stop = profile.stops[phase]
    if (!stop) continue
    const rem = distance - s - sum(stop.dx)
    if (rem >= 0 && rem % profile.walkDx === 0 && (rem / profile.walkDx) % 8 === stopFrameFor(phase)) return { ok: true, value: { distance, walkFrames: rem / profile.walkDx, stop: phase } }
  }
  const f1 = profile.stops.F1!
  const rem = distance - s - sum(f1.dx)
  if (!profile.stops.F5 && rem >= 0 && rem % profile.walkDx === 0 && (rem / profile.walkDx) % 8 === 4)
    return fail('needs-f5-stop', `${distance} ku arrives on Walk F5, and the Walk F5 stop is not ${profile.status === 'approved' ? 'approved' : 'in this profile'} yet.`)
  return fail('off-step', `${distance} ku is not ${s} ku of start + whole ${profile.walkDx} ku walk frames + a ${sum(f1.dx)} ku stop.`)
}

// ── frame rows ──

export type RowPhase = 'accelerate' | 'walk' | 'decelerate' | 'turn' | 'action'

export interface FrameRow {
  i: number
  leg: number
  phase: RowPhase
  clip: string
  frame: number
  pose: PoseId | null
  sha256: string | null
  facing: Heading
  mirrored: boolean
  fps: number
  /** Duration in 1/240 s ticks; startTick is the row's start from the table's start. */
  ticks: number
  startTick: number
  dxKu: Ku
  xKu: Ku
  gaitFrame: number | null
  /** Room-local horizontal extent of every non-transparent pixel, or null when the pose is not drawn. */
  boundsKu: [Ku, Ku] | null
  /** Width of the composite a door does not hide: 0 is fully hidden; null without a room or a drawn pose. */
  visibleKu: Ku | null
  approved: boolean
  events: string[]
}

type RowSpec = Omit<FrameRow, 'i' | 'leg' | 'startTick'>

/** Mirroring about the root line x = 128 keeps the anchor exact. */
export function poseBounds(pose: PoseId, facing: Facing, xKu: Ku, kind: 'alpha' | 'opaque' = 'alpha'): [Ku, Ku] | null {
  const b = kind === 'alpha' ? POSES[pose].alphaBounds : POSES[pose].opaqueBounds
  if (!b) return null
  return facing === 'right' ? [xKu + b[0] - CELL.anchorX, xKu + b[2] - CELL.anchorX] : [xKu + CELL.anchorX - b[2], xKu + CELL.anchorX - b[0]]
}

const poseTopKu = (pose: PoseId) => (POSES[pose].alphaBounds ? CELL.anchorY - POSES[pose].alphaBounds![1] : null)

/** The part of [from, to) a door leaves visible: inside the walls and outside every door's mask. */
export function visibleWidth(room: Room, bounds: [Ku, Ku], topKu: Ku): Ku {
  let lo = Math.max(bounds[0], 0)
  let hi = Math.min(bounds[1], room.widthKu)
  for (const d of room.doors) {
    const fits = topKu <= d.occlusion.topKu
    if (d.wall === 'left') lo = Math.max(lo, fits ? d.occlusion.to : d.occlusion.from)
    else hi = Math.min(hi, fits ? d.occlusion.from : d.occlusion.to)
  }
  return Math.max(0, hi - lo)
}

function poseRow(pose: PoseId, dx: Ku, phase: RowPhase, fps: number, facing: Facing, xBefore: Ku, room: Room | null): RowSpec {
  const p = POSES[pose]
  const xKu = xBefore + dirOf(facing) * dx
  const boundsKu = poseBounds(pose, facing, xKu)
  const top = poseTopKu(pose)
  return {
    phase, clip: p.clip, frame: p.frame, pose, sha256: p.sha256, facing, mirrored: facing === 'left', fps, ticks: ticksForFps(fps),
    dxKu: dirOf(facing) * dx, xKu, gaitFrame: p.gaitFrame ?? null, boundsKu,
    visibleKu: room && boundsKu && top !== null ? visibleWidth(room, boundsKu, top) : null,
    approved: p.sha256 !== null, events: [],
  }
}

function walkRowSpecs(ctx: RouteContext, x0: Ku, facing: Facing, walkFrames: number, stop: StopPhase | null, room: Room | null): RowSpec[] {
  const { profile, timing } = ctx
  const rows: RowSpec[] = []
  let x = x0
  const push = (r: RowSpec) => { rows.push(r); x = r.xKu }
  profile.start.poses.forEach((pose, k) => push(poseRow(pose, profile.start.dx[k], 'accelerate', timing.walkFps, facing, x, room)))
  for (let j = 1; j <= walkFrames; j++) push(poseRow(WALK_CYCLE[j % 8], profile.walkDx, 'walk', timing.walkFps, facing, x, room))
  if (stop) {
    const bridge = profile.stops[stop]!
    bridge.poses.forEach((pose, k) => push(poseRow(pose, bridge.dx[k], 'decelerate', timing.decelerationFps, facing, x, room)))
    rows[rows.length - 1].events.push('arrive')
  }
  rows[0].events.push('start')
  return rows
}

function clipRows(clips: ClipRef[], phase: RowPhase, fps: (c: ClipRef) => number, facing: Heading, x0: Ku): RowSpec[] {
  const out: RowSpec[] = []
  let x = x0
  const dir = facing === 'left' ? -1 : 1
  for (const c of clips)
    for (let f = 1; f <= c.frames; f++) {
      const dx = dir * (c.dx?.[f - 1] ?? 0)
      x += dx
      out.push({ phase, clip: c.clip, frame: f, pose: null, sha256: null, facing, mirrored: facing === 'left', fps: fps(c), ticks: ticksForFps(fps(c)), dxKu: dx, xKu: x, gaitFrame: null, boundsKu: null, visibleKu: null, approved: c.approved, events: [] })
    }
  return out
}

// ── legs ──

export type Leg =
  | { kind: 'direct'; from: Ku; to: Ku; facing: Facing; steps: number | null; walkFrames: number; stop: StopPhase }
  | { kind: 'ingress'; door: string; S: Ku; T: Ku; facing: Facing; walkFrames: number; stop: StopPhase; firstVisibleRow: number }
  | { kind: 'egress'; door: string; from: Ku; facing: Facing; walkFrames: number; hiddenAtRow: number; hiddenAtKu: Ku }
  | { kind: 'turn'; at: Ku; from: Heading; to: Heading; clips: ClipRef[] }
  | { kind: 'action'; at: Ku; facing: Facing; action: ActionSpec }
  | { kind: 'hidden'; door: string; swapTo?: string; aboutTurn?: boolean; toRoom?: string; toDoor?: string }

export interface CompiledLegs { legs: Leg[]; rows: FrameRow[] }

function legRows(ctx: RouteContext, leg: Leg, room: Room | null): RowSpec[] {
  switch (leg.kind) {
    case 'direct': return walkRowSpecs(ctx, leg.from, leg.facing, leg.walkFrames, leg.stop, room)
    case 'ingress': return walkRowSpecs(ctx, leg.S, leg.facing, leg.walkFrames, leg.stop, room)
    case 'egress': return walkRowSpecs(ctx, leg.from, leg.facing, leg.walkFrames, null, room)
    case 'turn': return clipRows(leg.clips, 'turn', () => ctx.timing.turnFps, leg.from, leg.at)
    case 'action': {
      const a = leg.action
      const face = a.face ? (ctx.turns.clips(leg.facing, a.face) ?? []) : []
      const back = a.face ? (ctx.turns.clips(a.face, leg.facing) ?? []) : []
      const before = clipRows(face, 'turn', () => ctx.timing.turnFps, leg.facing, leg.at)
      const body = clipRows(a.clips, 'action', (c) => c.fps ?? ctx.timing.walkFps, a.face ?? leg.facing, leg.at)
      const after = clipRows(back, 'turn', () => ctx.timing.turnFps, a.face ?? leg.facing, body.length ? body[body.length - 1].xKu : leg.at)
      return [...before, ...body, ...after]
    }
    case 'hidden': return []
  }
}

/** Expands legs into one frame table with running ticks. */
export function buildFrameTable(ctx: RouteContext, legs: Leg[], room: Room | null): FrameRow[] {
  const rows: FrameRow[] = []
  let tick = 0
  legs.forEach((leg, li) => {
    for (const r of legRows(ctx, leg, room)) {
      rows.push({ ...r, i: rows.length, leg: li, startTick: tick })
      tick += r.ticks
    }
  })
  return rows
}

// ── route classes ──

/** Class 5: direct same-room walk between two anchors, k steps apart → 42 + 84(k − 1) + 42 = 84k ku. */
export function compileDirect(ctx: RouteContext, from: Ku, to: Ku): Result<Leg & { kind: 'direct' }> {
  const facing: Facing = to > from ? 'right' : 'left'
  const d = Math.abs(to - from)
  const guard = unapprovedProfile(ctx)
  if (guard) return guard
  const sol = solveWalk(ctx.profile, d)
  if (!sol.ok) return sol
  return { ok: true, value: { kind: 'direct', from, to, facing, steps: d % STEP_KU === 0 ? d / STEP_KU : null, walkFrames: sol.value.walkFrames, stop: sol.value.stop } }
}

const MAX_WALK_FRAMES = 256

/**
 * Class 1: planned backwards from the anchor T to a hidden origin S = T − dir × distance, choosing the
 * shortest walk whose neutral, start bridge and Walk F1 are all fully hidden and whose first visible
 * row is mid-stride.
 */
export function compileIngress(ctx: RouteContext, room: Room, doorId: string, T: Ku): Result<Leg & { kind: 'ingress' }> {
  const guard = unapprovedProfile(ctx)
  if (guard) return guard
  const door = doorOf(room, doorId)
  const facing = inwardFacing(door)
  const dir = dirOf(facing)
  const s = sum(ctx.profile.start.dx)
  const neutralTop = poseTopKu('neutral')!
  for (let n = 0; n <= MAX_WALK_FRAMES; n++)
    for (const phase of ['F1', 'F5'] as const) {
      const stop = ctx.profile.stops[phase]
      if (!stop || n % 8 !== stopFrameFor(phase)) continue
      const S = T - dir * (s + n * ctx.profile.walkDx + sum(stop.dx))
      if (dir === 1 ? S > door.hiddenPocketEdgeKu : S < door.hiddenPocketEdgeKu) continue
      if (visibleWidth(room, poseBounds('neutral', facing, S)!, neutralTop) !== 0) continue
      const rows = walkRowSpecs(ctx, S, facing, n, phase, room)
      const startLen = ctx.profile.start.poses.length
      if (rows.slice(0, startLen).some((r) => r.visibleKu !== 0)) continue
      const first = rows.findIndex((r) => r.visibleKu !== 0)
      if (first < startLen || rows[first].phase !== 'walk') continue
      return { ok: true, value: { kind: 'ingress', door: door.id, S, T, facing, walkFrames: n, stop: phase, firstVisibleRow: first } }
    }
  return fail('no-hidden-start', `No hidden start behind ${doorId} reaches ${T} ku exactly.`)
}

/** Class 2: start bridge, then whole walk frames until the whole composite is hidden. No stop. */
export function compileEgress(ctx: RouteContext, room: Room, doorId: string, from: Ku): Result<Leg & { kind: 'egress' }> {
  const guard = unapprovedProfile(ctx)
  if (guard) return guard
  const door = doorOf(room, doorId)
  const facing = opposite(inwardFacing(door))
  const rows = walkRowSpecs(ctx, from, facing, MAX_WALK_FRAMES, null, room)
  const onF1 = ctx.profile.start.poses.length - 1
  const at = rows.findIndex((r, i) => i >= onF1 && r.visibleKu === 0)
  if (at < 0) return fail('never-hidden', `Walking out from ${from} ku never hides him behind ${doorId}.`)
  return { ok: true, value: { kind: 'egress', door: door.id, from, facing, walkFrames: at - onF1, hiddenAtRow: at, hiddenAtKu: rows[at].xKu } }
}

function turnLeg(ctx: RouteContext, at: Ku, from: Heading, to: Heading): Result<Leg[]> {
  if (from === to) return { ok: true, value: [] }
  const clips = ctx.turns.clips(from, to)
  if (!clips) return fail('no-turn', `There is no turn from ${from} to ${to}.`)
  if (!ctx.allowUnapproved && clips.some((c) => !c.approved)) return fail('unapproved-clip', `The turn from ${from} to ${to} uses a clip Frank has not approved (${clips.filter((c) => !c.approved).map((c) => c.clip).join(', ')}).`)
  return { ok: true, value: [{ kind: 'turn', at, from, to, clips }] }
}

/** Every action recipe returns to its declared anchor, or declares a reviewed held-prop or environment endpoint. */
export function checkAction(ctx: RouteContext, facing: Facing, a: ActionSpec): Result<true> {
  if (a.endpoint === 'anchor') {
    const net = sum(a.clips.flatMap((c) => c.dx ?? []))
    if (net !== 0) return fail('bad-action', `${a.id} ends ${net} ku from its anchor without declaring a reviewed endpoint.`)
  }
  if (a.face) {
    for (const [f, t] of [[facing, a.face], [a.face, facing]] as const) {
      const r = turnLeg(ctx, 0, f, t)
      if (!r.ok) return r
    }
  }
  if (!ctx.allowUnapproved && a.clips.some((c) => !c.approved)) return fail('unapproved-clip', `${a.id} uses an action clip Frank has not approved.`)
  return { ok: true, value: true }
}

export type Endpoint = { door: string } | { anchor: PlacedAnchor }

export interface Route extends CompiledLegs {
  routeClass: 1 | 2 | 3 | 4 | 5
  endKu: Ku | null
  endFacing: Facing | null
  /** Total distance walked, signed by direction. */
  travelKu: Ku
}

function finish(ctx: RouteContext, room: Room, routeClass: Route['routeClass'], legs: Leg[], endKu: Ku | null, endFacing: Facing | null): Result<Route> {
  const rows = buildFrameTable(ctx, legs, room)
  return { ok: true, value: { routeClass, legs, rows, endKu, endFacing, travelKu: sum(rows.map((r) => r.dxKu)) } }
}

/**
 * Compiles a route between two endpoints in one room. He stands at an anchor facing its declared
 * facing (after any action he returns to that neutral). Classes: 1 door → anchor, 2 anchor → door,
 * 4 door → door (hidden transfer), 5 anchor → anchor. Class 3 is compileDoorControl.
 */
export function compileRoute(ctx: RouteContext, room: Room, from: Endpoint, to: Endpoint): Result<Route> {
  if ('door' in from && 'door' in to) return finish(ctx, room, 4, [{ kind: 'hidden', door: from.door, toDoor: to.door }], null, null)
  if ('door' in from && 'anchor' in to) {
    const ing = compileIngress(ctx, room, from.door, to.anchor.xKu)
    if (!ing.ok) return ing
    const turn = turnLeg(ctx, to.anchor.xKu, ing.value.facing, to.anchor.anchor.facing)
    if (!turn.ok) return turn
    return finish(ctx, room, 1, [ing.value, ...turn.value], to.anchor.xKu, to.anchor.anchor.facing)
  }
  if ('anchor' in from && 'door' in to) {
    const out = opposite(inwardFacing(doorOf(room, to.door)))
    const turn = turnLeg(ctx, from.anchor.xKu, from.anchor.anchor.facing, out)
    if (!turn.ok) return turn
    const eg = compileEgress(ctx, room, to.door, from.anchor.xKu)
    if (!eg.ok) return eg
    return finish(ctx, room, 2, [...turn.value, eg.value], null, null)
  }
  const a = (from as { anchor: PlacedAnchor }).anchor
  const b = (to as { anchor: PlacedAnchor }).anchor
  if (a.xKu === b.xKu) {
    const turn = turnLeg(ctx, a.xKu, a.anchor.facing, b.anchor.facing)
    if (!turn.ok) return turn
    return finish(ctx, room, 5, turn.value, b.xKu, b.anchor.facing)
  }
  const walkFacing: Facing = b.xKu > a.xKu ? 'right' : 'left'
  const pre = turnLeg(ctx, a.xKu, a.anchor.facing, walkFacing)
  if (!pre.ok) return pre
  const walk = compileDirect(ctx, a.xKu, b.xKu)
  if (!walk.ok) return walk
  const post = turnLeg(ctx, b.xKu, walkFacing, b.anchor.facing)
  if (!post.ok) return post
  return finish(ctx, room, 5, [...pre.value, walk.value, ...post.value], b.xKu, b.anchor.facing)
}

/** Class 3: hidden door → a door-control anchor → act → back out of the same door. */
export function compileDoorControl(ctx: RouteContext, room: Room, doorId: string, control: PlacedAnchor): Result<Route> {
  const inRoute = compileRoute(ctx, room, { door: doorId }, { anchor: control })
  if (!inRoute.ok) return inRoute
  const act = control.anchor.action
  const actLegs: Leg[] = []
  if (act) {
    const ok = checkAction(ctx, control.anchor.facing, act)
    if (!ok.ok) return ok
    actLegs.push({ kind: 'action', at: control.xKu, facing: control.anchor.facing, action: act })
  }
  const outRoute = compileRoute(ctx, room, { anchor: control }, { door: doorId })
  if (!outRoute.ok) return outRoute
  return finish(ctx, room, 3, [...inRoute.value.legs, ...actLegs, ...outRoute.value.legs], null, null)
}

// ── interruptions ──

export interface Interruption {
  rows: FrameRow[]
  endKu: Ku
  stop: StopPhase
  /** Frames played after the order arrived, before the stop bridge. */
  carriedFrames: number
  onLattice: boolean | null
}

/**
 * A new order mid-walk: he carries on to the next legal stop phase (Walk F1, or F5 once that stop
 * exists), stops there and replans. He never teleports. Rows must be one walking leg's table.
 */
export function interruptAt(ctx: RouteContext, rows: FrameRow[], atRow: number, room: Room | null = null): Result<Interruption> {
  const cur = rows[atRow]
  if (!cur) return fail('off-step', `There is no row ${atRow}.`)
  const last = rows[rows.length - 1]
  if (cur.phase === 'decelerate') {
    const from = rows.slice(0, atRow).reverse().find((r) => r.phase !== 'decelerate')
    return { ok: true, value: { rows, endKu: last.xKu, stop: from?.gaitFrame === 5 ? 'F5' : 'F1', carriedFrames: 0, onLattice: room ? onLattice(room, last.xKu) : null } }
  }
  const legal = (r: FrameRow) => (r.phase === 'walk' || r.phase === 'accelerate') && (r.gaitFrame === 1 || (r.gaitFrame === 5 && !!ctx.profile.stops.F5))
  let j = atRow
  while (j < rows.length && !legal(rows[j])) j++
  // A leg without a decelerating tail (egress) may run out: extend it with whole walk frames.
  const kept = rows.slice(0, Math.min(j, rows.length - 1) + 1).map((r) => ({ ...r, events: r.events.filter((e) => e !== 'arrive') }))
  let extra = 0
  while (!legal(kept[kept.length - 1])) {
    const prev = kept[kept.length - 1]
    if (prev.facing !== 'left' && prev.facing !== 'right') return fail('off-step', 'Not a walking row.')
    const next = WALK_CYCLE[(prev.gaitFrame ?? 1) % 8]
    const spec = poseRow(next, ctx.profile.walkDx, 'walk', ctx.timing.walkFps, prev.facing, prev.xKu, room)
    kept.push({ ...spec, i: kept.length, leg: prev.leg, startTick: prev.startTick + prev.ticks })
    if (++extra > 8) return fail('off-step', 'No legal stop phase.')
  }
  const at = kept[kept.length - 1]
  const stop: StopPhase = at.gaitFrame === 5 ? 'F5' : 'F1'
  const bridge = ctx.profile.stops[stop]!
  let x = at.xKu
  let tick = at.startTick + at.ticks
  bridge.poses.forEach((pose, k) => {
    const spec = poseRow(pose, bridge.dx[k], 'decelerate', ctx.timing.decelerationFps, at.facing as Facing, x, room)
    kept.push({ ...spec, i: kept.length, leg: at.leg, startTick: tick })
    x = spec.xKu
    tick += spec.ticks
  })
  kept[kept.length - 1].events.push('arrive')
  return { ok: true, value: { rows: kept, endKu: x, stop, carriedFrames: kept.length - bridge.poses.length - 1 - atRow, onLattice: room ? onLattice(room, x) : null } }
}

