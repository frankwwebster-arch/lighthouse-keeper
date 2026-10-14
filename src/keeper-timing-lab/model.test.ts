import { describe, expect, it } from 'vitest'
import { changedProfileFields, clampProfile, frameDurationMs, phaseFrameCounts, profileDurationMs, sectionFrames, type LoopSection, type TimingFrame, type TimingProfile } from './model'

const frames: TimingFrame[] = [
  { id: 'w1', src: '/w1.png', phase: 'walk', phaseLabel: 'walk', pose: 'F1', dx: 21, x: 21 },
  { id: 'w2', src: '/w2.png', phase: 'walk', phaseLabel: 'walk', pose: 'F2', dx: 21, x: 42 },
  { id: 'd1', src: '/d1.png', phase: 'deceleration', phaseLabel: 'deceleration', pose: '75%', dx: 18, x: 60 },
  { id: 's1', src: '/s1.png', phase: 'settle', phaseLabel: 'settle', pose: 'stop', dx: 0, x: 60 },
  { id: 't1', src: '/t1.png', phase: 'turn', phaseLabel: 'turn', pose: '75°', dx: 0, x: 60 },
  { id: 't2', src: '/t2.png', phase: 'turn', phaseLabel: 'turn', pose: 'front', dx: 0, x: 60 },
  { id: 'h1', src: '/h1.png', phase: 'frontHold', phaseLabel: 'hold', pose: 'front', dx: 0, x: 60 },
  { id: 'h2', src: '/h2.png', phase: 'frontHold', phaseLabel: 'hold', pose: 'front', dx: 0, x: 60 },
]
const profile: TimingProfile = { walkFps: 8, decelerationFps: 8, settleMs: 125, turnFps: 10, frontHoldMs: 500 }
const fastTimingV1: TimingProfile = { walkFps: 10, decelerationFps: 12, settleMs: 0, turnFps: 16, frontHoldMs: 625 }

describe('Keeper Timing Lab model', () => {
  it('assigns independent durations to each phase', () => {
    const counts = phaseFrameCounts(frames)
    expect(frameDurationMs(frames[0], profile, counts)).toBe(125)
    expect(frameDurationMs(frames[3], profile, counts)).toBe(125)
    expect(frameDurationMs(frames[4], profile, counts)).toBe(100)
    expect(frameDurationMs(frames[6], profile, counts)).toBe(250)
    expect(profileDurationMs(frames, profile)).toBe(1200)
  })

  it('filters playback to named sections without altering source frames', () => {
    const turn: LoopSection = { id: 'turn', label: 'Turn only', phases: ['turn'] }
    expect(sectionFrames(frames, turn).map((frame) => frame.id)).toEqual(['t1', 't2'])
    expect(frames).toHaveLength(8)
  })

  it('reports the recommended proposal as turn-only', () => {
    const baseline = { ...profile, turnFps: 8 }
    expect(changedProfileFields(baseline, profile)).toEqual(['turnFps'])
  })

  it('clamps imported values to the supported tuning range', () => {
    expect(clampProfile({ walkFps: 1, decelerationFps: 20, settleMs: -4, turnFps: 99, frontHoldMs: 20 })).toEqual({ walkFps: 4, decelerationFps: 16, settleMs: 0, turnFps: 16, frontHoldMs: 125 })
  })

  it('reproduces the approved Fast Timing V1 route duration', () => {
    const route = [
      ...Array.from({ length: 16 }, (_, index) => ({ ...frames[0], id: `walk-${index}` })),
      ...Array.from({ length: 4 }, (_, index) => ({ ...frames[2], id: `deceleration-${index}` })),
      { ...frames[3], id: 'settle' },
      ...Array.from({ length: 7 }, (_, index) => ({ ...frames[4], id: `turn-${index}` })),
      ...Array.from({ length: 4 }, (_, index) => ({ ...frames[6], id: `hold-${index}` })),
    ]
    expect(profileDurationMs(route, fastTimingV1)).toBeCloseTo(2995.833333333333, 8)
    expect(changedProfileFields({ walkFps: 8, decelerationFps: 8, settleMs: 125, turnFps: 8, frontHoldMs: 500 }, fastTimingV1)).toEqual(['walkFps', 'decelerationFps', 'settleMs', 'turnFps', 'frontHoldMs'])
  })
})
