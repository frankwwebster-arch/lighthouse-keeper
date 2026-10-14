import crypto from 'node:crypto'
import fs from 'node:fs'
import { PNG } from 'pngjs'
import { describe, expect, it } from 'vitest'
import {
  APPROVALS, APPROVED_PROFILE, APPROVED_STOP_WALK_STOP_REGISTER, APPROVED_STOP_WALK_STOP_REGISTER_SHA256, APPROVED_WALK_REGISTER, APPROVED_WALK_REGISTER_SHA256,
  CANDIDATE_F5_PROFILE, CANDIDATE_PROFILE, DEFAULT_PROFILE, FAST_TIMING_V1, POSES, PROFILES, profileFor, rootTableFromRegister, sum, type RootProfile,
} from './locomotion'
import { solveWalk } from './routes'
import { STEP_KU } from './units'

const sha = (p: string) => crypto.createHash('sha256').update(fs.readFileSync(p)).digest('hex')
const json = (p: string) => JSON.parse(fs.readFileSync(p, 'utf8'))

describe('approved authorities (tests 1, 2, 17)', () => {
  it('every reused PNG is byte-identical to its approved authority', () => {
    const swsRegister = fs.readFileSync(APPROVED_STOP_WALK_STOP_REGISTER, 'utf8')
    const walkRegister = fs.readFileSync(APPROVED_WALK_REGISTER, 'utf8')
    for (const pose of Object.values(POSES)) {
      if (!pose.file) continue
      expect(sha(pose.file), pose.id).toBe(pose.sha256)
      expect(swsRegister.includes(pose.sha256!) || walkRegister.includes(pose.sha256!), `${pose.id} is named by an approval record`).toBe(true)
    }
  })

  it('pose bounds are the PNGs\' own alpha > 0 bounds', () => {
    for (const pose of Object.values(POSES)) {
      if (!pose.file) continue
      const png = PNG.sync.read(fs.readFileSync(pose.file))
      let x0 = Infinity, y0 = Infinity, x1 = -1, y1 = -1
      for (let y = 0; y < png.height; y++)
        for (let x = 0; x < png.width; x++)
          if (png.data[(y * png.width + x) * 4 + 3] > 0) { x0 = Math.min(x0, x); y0 = Math.min(y0, y); x1 = Math.max(x1, x + 1); y1 = Math.max(y1, y + 1) }
      expect([png.width, png.height]).toEqual([256, 320])
      expect([x0, y0, x1, y1], pose.id).toEqual(pose.alphaBounds)
    }
  })

  it('approval registers are unchanged', () => {
    expect(sha(APPROVED_STOP_WALK_STOP_REGISTER)).toBe(APPROVED_STOP_WALK_STOP_REGISTER_SHA256)
    expect(sha(APPROVED_WALK_REGISTER)).toBe(APPROVED_WALK_REGISTER_SHA256)
    expect(json(APPROVED_STOP_WALK_STOP_REGISTER).approval.approvedBy).toBe('Frank')
  })

  it('the approved table is read from the approval register, and the candidate is kept beside it', () => {
    const t = rootTableFromRegister(json(APPROVED_STOP_WALK_STOP_REGISTER))
    expect(t).toEqual({ start: [...APPROVED_PROFILE.start.dx], walk: APPROVED_PROFILE.walkDx, stop: [...APPROVED_PROFILE.stops.F1!.dx] })
    expect(PROFILES.map((p) => [p.id, p.status])).toEqual([['approved-v1', 'approved'], ['candidate-42', 'candidate'], ['candidate-42-f5', 'candidate']])
    for (const p of PROFILES) expect(p.label.length).toBeGreaterThan(10)
    expect(CANDIDATE_PROFILE.awaiting.length).toBeGreaterThan(0)
    expect(CANDIDATE_F5_PROFILE.awaiting.length).toBeGreaterThan(CANDIDATE_PROFILE.awaiting.length)
  })

  it('the default is only what Frank has approved', () => {
    expect(APPROVALS.rootCandidate).toBe(false)
    expect(APPROVALS.f5Stop).toBe(false)
    expect(DEFAULT_PROFILE).toBe(APPROVED_PROFILE)
    expect(DEFAULT_PROFILE.stops.F5).toBeNull()
    expect(profileFor({ rootCandidate: true, f5Stop: false })).toBe(CANDIDATE_PROFILE)
    expect(profileFor({ rootCandidate: true, f5Stop: true })).toBe(CANDIDATE_F5_PROFILE)
    expect(profileFor({ rootCandidate: false, f5Stop: true })).toBe(APPROVED_PROFILE)
  })

  it('timing is Fast Timing V1 as approved', () => {
    const policy = json('data/keeper_timing_policy.json')
    expect(policy.status).toBe('approved-project-timing-policy')
    expect(policy.transitionProfile).toEqual(FAST_TIMING_V1)
  })
})

describe('root-motion arithmetic (tests 3, 4)', () => {
  it('candidate bridges total 42 ku both ways; steady frames stay 21; approved bridges are 38', () => {
    for (const p of [CANDIDATE_PROFILE, CANDIDATE_F5_PROFILE]) {
      expect(sum(p.start.dx)).toBe(42)
      expect(sum(p.stops.F1!.dx)).toBe(42)
      expect(p.walkDx).toBe(21)
    }
    expect(sum(CANDIDATE_F5_PROFILE.stops.F5!.dx)).toBe(42)
    expect(sum(APPROVED_PROFILE.start.dx)).toBe(38)
    expect(sum(APPROVED_PROFILE.stops.F1!.dx)).toBe(38)
    // The candidate adds exactly 1 ku to each moving row and keeps the +4, +6, +6 acceleration shape.
    expect(CANDIDATE_PROFILE.start.dx.map((d, i) => d - APPROVED_PROFILE.start.dx[i])).toEqual([1, 1, 1, 1])
    const diffs = (xs: readonly number[]) => xs.slice(1).map((x, i) => x - xs[i])
    expect(diffs(CANDIDATE_PROFILE.start.dx)).toEqual(diffs(APPROVED_PROFILE.start.dx))
  })

  it('F1 and F5 stops end on the same exact neutral', () => {
    const f1 = CANDIDATE_F5_PROFILE.stops.F1!, f5 = CANDIDATE_F5_PROFILE.stops.F5!
    expect(f1.poses[f1.poses.length - 1]).toBe('neutral')
    expect(f5.poses[f5.poses.length - 1]).toBe('neutral')
    expect(sum(f1.dx)).toBe(sum(f5.dx))
    // The F5 bridge is its own drawing, never a leg-swapped copy of the F1 bridge.
    expect(f5.poses.slice(0, 3).some((p) => f1.poses.includes(p))).toBe(false)
    expect(f5.poses.slice(0, 3).every((p) => POSES[p].sha256 === null)).toBe(true)
  })
})

/** Every distance up to `max` that a profile can walk exactly from neutral to neutral. */
const reachable = (p: RootProfile, max: number) => Array.from({ length: max }, (_, i) => i + 1).filter((d) => solveWalk(p, d).ok)

describe('the three-anchor proof (plan 6.2)', () => {
  const MAX = 3000

  it('approved numbers reach only 76 + 168n ku, so no three anchors can all be joined', () => {
    const r = reachable(APPROVED_PROFILE, MAX)
    expect(r).toEqual(r.map((_, n) => 76 + 168 * n))
    const set = new Set(r)
    // Anchors a < b < c: d(a,c) = d(a,b) + d(b,c). No two reachable distances sum to a reachable one.
    for (const d1 of r) for (const d2 of r) if (d1 + d2 <= MAX) expect(set.has(d1 + d2)).toBe(false)
    // In particular none of them is a whole number of 84 ku steps.
    expect(r.some((d) => d % STEP_KU === 0)).toBe(false)
  })

  it('an F5 stop alone does not rescue the approved bridges (76 + 84n leaves 68 for a pair)', () => {
    const hypothetical: RootProfile = { ...APPROVED_PROFILE, stops: { F1: APPROVED_PROFILE.stops.F1, F5: { poses: CANDIDATE_F5_PROFILE.stops.F5!.poses, dx: APPROVED_PROFILE.stops.F1!.dx } } }
    const r = reachable(hypothetical, MAX)
    expect(r).toEqual(r.map((_, n) => 76 + 84 * n))
    const set = new Set(r)
    for (const d1 of r) for (const d2 of r) if (d1 + d2 <= MAX) expect(set.has(d1 + d2)).toBe(false)
  })

  it('candidate numbers reach exactly every whole step, so every set of anchors can be joined', () => {
    const r = reachable(CANDIDATE_F5_PROFILE, MAX)
    expect(r).toEqual(r.map((_, n) => STEP_KU * (n + 1)))
    const set = new Set(r)
    for (const d1 of r) for (const d2 of r) if (d1 + d2 <= MAX) expect(set.has(d1 + d2)).toBe(true)
  })

  it('the gate-1 candidate alone reaches only odd steps', () => {
    const r = reachable(CANDIDATE_PROFILE, MAX)
    expect(r).toEqual(r.map((_, n) => STEP_KU * (2 * n + 1)))
  })
})
