import { describe, expect, it } from 'vitest'
import { APPROVED_PROFILE, CANDIDATE_F5_PROFILE, CANDIDATE_PROFILE, POSES, type RootProfile } from './locomotion'
import { anchorsAt, placementPoint, spotX, type PlacedAnchor } from './room'
import { CATALOGUE, LIVING_PLACEMENTS, LIVING_ROOM } from './rooms.data'
import {
  DEFAULT_CONTEXT, buildFrameTable, checkAction, compileDirect, compileDoorControl, compileEgress, compileIngress, compileRoute, interruptAt, solveWalk,
  type FrameRow, type RouteContext,
} from './routes'
import { STEP_KU, kuToStageSu } from './units'

const ctxFor = (profile: RootProfile): RouteContext => ({ ...DEFAULT_CONTEXT, profile, allowUnapproved: profile.status !== 'approved' })
const FULL = ctxFor(CANDIDATE_F5_PROFILE)
const GATE1 = ctxFor(CANDIDATE_PROFILE)
const total = (rows: FrameRow[]) => rows.reduce((a, r) => a + r.dxKu, 0)

function directRows(ctx: RouteContext, from: number, to: number) {
  const leg = compileDirect(ctx, from, to)
  if (!leg.ok) throw new Error(leg.reason)
  return { leg: leg.value, rows: buildFrameTable(ctx, [leg.value], null) }
}

const living = () => LIVING_PLACEMENTS.map((p) => anchorsAt(CATALOGUE[p.object], placementPoint(CATALOGUE[p.object], p))[0])

describe('direct walks (tests 5, 6, 7)', () => {
  it('emits exactly 84k ku; odd k stops from F1 and even k from F5', () => {
    for (let k = 1; k <= 12; k++) {
      const { leg, rows } = directRows(FULL, 0, k * STEP_KU)
      expect(total(rows)).toBe(84 * k)
      expect(rows[rows.length - 1].xKu).toBe(84 * k)
      expect(leg.stop).toBe(k % 2 ? 'F1' : 'F5')
      expect(leg.steps).toBe(k)
      expect(leg.walkFrames).toBe(4 * (k - 1))
    }
  })

  it('until the F5 stop is approved, even-step routes report unsupported and are never improvised', () => {
    for (let k = 1; k <= 8; k++) {
      const r = compileDirect(GATE1, 0, k * STEP_KU)
      if (k % 2) expect(r.ok).toBe(true)
      else expect(r).toMatchObject({ ok: false, code: 'needs-f5-stop' })
    }
  })

  it('the approved default supports no direct walk on the lattice: every one is 8 ku out', () => {
    for (let k = 1; k <= 12; k++) expect(compileDirect(DEFAULT_CONTEXT, 0, k * STEP_KU)).toMatchObject({ ok: false, code: 'off-step' })
    // It does walk its own distances exactly, e.g. 76 ku.
    expect(solveWalk(APPROVED_PROFILE, 76)).toEqual({ ok: true, value: { distance: 76, walkFrames: 0, stop: 'F1' } })
  })

  it('candidate profiles are refused where unapproved material is not allowed', () => {
    expect(compileDirect({ ...DEFAULT_CONTEXT, profile: CANDIDATE_F5_PROFILE }, 0, 84)).toMatchObject({ ok: false, code: 'unapproved-clip' })
  })

  it('left travel negates the same deltas on the mirrored, mirror-safe poses', () => {
    for (let k = 1; k <= 4; k++) {
      const right = directRows(FULL, 0, k * STEP_KU).rows
      const left = directRows(FULL, 0, -k * STEP_KU).rows
      expect(left.map((r) => r.dxKu)).toEqual(right.map((r) => -r.dxKu))
      expect(left.map((r) => r.pose)).toEqual(right.map((r) => r.pose))
      expect(left.every((r) => r.mirrored && r.facing === 'left')).toBe(true)
      expect(left.every((r) => r.pose === null || POSES[r.pose].mirrorSafe)).toBe(true)
    }
  })

  it('no locomotion row stands still, position changes only per frame, and the endpoint is the exact neutral', () => {
    const { rows } = directRows(FULL, 100, 100 + 5 * STEP_KU)
    expect(rows.every((r) => r.dxKu !== 0)).toBe(true)
    rows.forEach((r, i) => expect(r.xKu).toBe((i ? rows[i - 1].xKu : 100) + r.dxKu))
    expect(rows[rows.length - 1].pose).toBe('neutral')
    expect(rows[rows.length - 1].events).toContain('arrive')
    expect(rows.every((r) => Number.isInteger(r.xKu))).toBe(true)
  })

  it('times rows by Fast Timing V1 in whole ticks', () => {
    const { rows } = directRows(FULL, 0, 84)
    expect(rows.map((r) => [r.phase, r.fps])).toEqual([
      ['accelerate', 10], ['accelerate', 10], ['accelerate', 10], ['accelerate', 10],
      ['decelerate', 12], ['decelerate', 12], ['decelerate', 12], ['decelerate', 12],
    ])
    expect(rows.map((r) => r.startTick)).toEqual([0, 24, 48, 72, 96, 116, 136, 156])
  })
})

describe('the density-8 Keeper is never re-snapped to whole lp (test 11)', () => {
  it('keeps half stage units at the render boundary', () => {
    const { rows } = directRows(FULL, 0, 84)
    expect(rows.map((r) => r.xKu)).toEqual([3, 10, 23, 42, 61, 74, 81, 84])
    expect(rows.map((r) => kuToStageSu(0, r.xKu))).toEqual([1.5, 5, 11.5, 21, 30.5, 37, 40.5, 42])
  })
})

describe('turns and actions (tests 8, 9)', () => {
  const at = (facing: 'left' | 'right', x = 704): PlacedAnchor => ({ object: 'x', xKu: x, anchor: { id: 'use', offsetSteps: 0, facing, entryPose: 'standing-side-' + facing, exitPose: 'standing-side-' + facing } })

  it('turns have zero root motion and keep the anchor', () => {
    const r = compileRoute(FULL, LIVING_ROOM, { anchor: at('right') }, { anchor: at('left') })
    if (!r.ok) throw new Error(r.reason)
    expect(r.value.rows.length).toBe(18)
    expect(r.value.rows.every((x) => x.phase === 'turn' && x.dxKu === 0 && x.xKu === 704 && x.fps === 16)).toBe(true)
  })

  it('the approved default refuses turns Frank has not approved (the mirrored rear turn)', () => {
    expect(compileRoute(DEFAULT_CONTEXT, LIVING_ROOM, { anchor: at('right') }, { anchor: at('left') })).toMatchObject({ ok: false, code: 'unapproved-clip' })
  })

  it('an action must return to its anchor or declare a reviewed endpoint', () => {
    const clip = (dx: number[]) => ({ clip: 'test', frames: dx.length, dx, approved: true })
    expect(checkAction(DEFAULT_CONTEXT, 'right', { id: 'sit', clips: [clip([0, 8, 4, -12])], endpoint: 'anchor' }).ok).toBe(true)
    expect(checkAction(DEFAULT_CONTEXT, 'right', { id: 'drift', clips: [clip([0, 8])], endpoint: 'anchor' })).toMatchObject({ ok: false, code: 'bad-action' })
    expect(checkAction(DEFAULT_CONTEXT, 'right', { id: 'carry', clips: [clip([0, 8])], endpoint: { reviewed: 'carry-ready+cake', pose: 'carry-ready+prop' } }).ok).toBe(true)
    // The bookshelf's back-facing action uses the approved side → back turn and its exact reverse.
    expect(checkAction(DEFAULT_CONTEXT, 'right', CATALOGUE.bookshelf.anchors[0].action!).ok).toBe(true)
    expect(checkAction(DEFAULT_CONTEXT, 'left', CATALOGUE.bookshelf.anchors[0].action!)).toMatchObject({ ok: false, code: 'unapproved-clip' })
  })
})

describe('door routes (test 10)', () => {
  it('ingress is planned backwards with an exact sum, hidden until mid-stride', () => {
    for (const ctx of [DEFAULT_CONTEXT, GATE1, FULL])
      for (const a of living()) {
        const ing = compileIngress(ctx, LIVING_ROOM, 'door', a.xKu)
        if (!ing.ok) throw new Error(ing.reason)
        const rows = buildFrameTable(ctx, [ing.value], LIVING_ROOM)
        expect(ing.value.S + total(rows)).toBe(a.xKu)
        expect(ing.value.S).toBeLessThanOrEqual(LIVING_ROOM.doors[0].hiddenPocketEdgeKu)
        const first = ing.value.firstVisibleRow
        expect(rows[first].phase).toBe('walk')
        expect(rows.slice(0, first).every((r) => r.visibleKu === 0)).toBe(true)
        expect(rows[first].visibleKu).toBeGreaterThan(0)
        expect(rows[rows.length - 1].xKu).toBe(a.xKu)
      }
  })

  it('egress transfers only once the whole composite is hidden', () => {
    const ctx = FULL
    for (const a of living()) {
      const eg = compileEgress(ctx, LIVING_ROOM, 'door', a.xKu)
      if (!eg.ok) throw new Error(eg.reason)
      const rows = buildFrameTable(ctx, [eg.value], LIVING_ROOM)
      expect(rows.length - 1).toBe(eg.value.hiddenAtRow)
      expect(rows[rows.length - 1].visibleKu).toBe(0)
      expect(rows.slice(0, -1).some((r) => r.visibleKu === 0)).toBe(false)
    }
  })

  it('every walk phase has a fully hidden frame behind the placeholder leaf (narrowest to widest Walk V6 frames)', () => {
    // Leaving from 168 consecutive positions covers every phase of the 168 ku cycle.
    for (const ctx of [DEFAULT_CONTEXT, FULL])
      for (let x = 600; x < 600 + 168; x++) expect(compileEgress(ctx, LIVING_ROOM, 'door', x).ok).toBe(true)
  })

  it('class 3 goes in, acts and leaves through the same door', () => {
    const control = living()[0]
    const r = compileDoorControl(FULL, LIVING_ROOM, 'door', control)
    if (!r.ok) throw new Error(r.reason)
    expect(r.value.routeClass).toBe(3)
    expect(r.value.legs.map((l) => l.kind)).toEqual(['ingress', 'action', 'turn', 'egress'])
  })

  it('route classes 1, 2, 4 and 5 compile from endpoints', () => {
    const [a, b] = living()
    const cls = (from: Parameters<typeof compileRoute>[2], to: Parameters<typeof compileRoute>[3]) => {
      const r = compileRoute(FULL, LIVING_ROOM, from, to)
      return r.ok ? r.value.routeClass : r.code
    }
    expect(cls({ door: 'door' }, { anchor: a })).toBe(1)
    expect(cls({ anchor: a }, { door: 'door' })).toBe(2)
    expect(cls({ door: 'door' }, { door: 'door' })).toBe(4)
    expect(cls({ anchor: a }, { anchor: b })).toBe(5)
  })
})

describe('interruptions (test 16)', () => {
  it('candidate: he carries on at most 3 frames to the next F1 or F5, stops exactly and lands on the lattice', () => {
    const { rows } = directRows(FULL, spotX(LIVING_ROOM, 1), spotX(LIVING_ROOM, 9))
    rows.forEach((r, i) => {
      if (r.phase === 'decelerate') return
      const s = interruptAt(FULL, rows, i, LIVING_ROOM)
      if (!s.ok) throw new Error(s.reason)
      expect(s.value.carriedFrames).toBeLessThanOrEqual(3)
      expect(s.value.onLattice).toBe(true)
      const out = s.value.rows
      expect(out[out.length - 1].pose).toBe('neutral')
      expect(out[out.length - 1].xKu).toBe(s.value.endKu)
      expect(out.slice(0, i + 1)).toEqual(rows.slice(0, i + 1).map((x) => ({ ...x, events: x.events.filter((e) => e !== 'arrive') })))
    })
  })

  it('gate-1 candidate: at most 7 frames to the next F1, still on the lattice', () => {
    const { rows } = directRows(GATE1, spotX(LIVING_ROOM, 1), spotX(LIVING_ROOM, 10))
    rows.forEach((r, i) => {
      if (r.phase === 'decelerate') return
      const s = interruptAt(GATE1, rows, i, LIVING_ROOM)
      if (!s.ok) throw new Error(s.reason)
      expect(s.value.carriedFrames).toBeLessThanOrEqual(7)
      expect(s.value.stop).toBe('F1')
      expect(s.value.onLattice).toBe(true)
    })
  })

  it('an order during the stop bridge lets the stop finish', () => {
    const { rows } = directRows(FULL, 452, 452 + 2 * STEP_KU)
    const s = interruptAt(FULL, rows, rows.length - 2, LIVING_ROOM)
    expect(s).toMatchObject({ ok: true, value: { endKu: 452 + 168, stop: 'F5', carriedFrames: 0 } })
  })
})

describe('determinism (test 15)', () => {
  it('identical inputs give identical routes', () => {
    const anchors = living()
    const run = () => JSON.stringify(anchors.flatMap((a) => anchors.map((b) => compileRoute(FULL, LIVING_ROOM, { anchor: a }, { anchor: b }))))
    expect(run()).toBe(run())
  })

  it('every pair of living-room anchors is reachable in whole steps with the full candidate', () => {
    const anchors = living()
    for (const a of anchors)
      for (const b of anchors) {
        if (a === b) continue
        const r = compileRoute(FULL, LIVING_ROOM, { anchor: a }, { anchor: b })
        if (!r.ok) throw new Error(r.reason)
        expect(r.value.travelKu).toBe(b.xKu - a.xKu)
        expect(Math.abs(r.value.travelKu) % STEP_KU).toBe(0)
      }
  })
})

