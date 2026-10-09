import { describe, expect, it } from 'vitest'
import { FPS, clampFps, cleanFps, fpsExport, fpsFor, withFps } from './animFps'

describe('animation speeds', () => {
  it('keeps speeds in range and on the half-step, like the review page', () => {
    expect(clampFps(0)).toBe(FPS.min)
    expect(clampFps(99)).toBe(FPS.max)
    expect(clampFps(4.3)).toBe(4.5)
    expect(clampFps(4.2)).toBe(4)
  })

  it('drops anything that is not a sensible name and number', () => {
    expect(cleanFps(null)).toEqual({})
    expect(cleanFps([4])).toEqual({})
    expect(cleanFps({ keeper_walk: 6, keeper_dance: '7.5', 'bad name': 4, keeper_sad: 'fast', keeper_yawn: NaN, keeper_cross: 50 })).toEqual({ keeper_walk: 6, keeper_dance: 7.5, keeper_cross: 20 })
  })

  it('plays at the grown-ups’ speed, or the drawn one', () => {
    expect(fpsFor({ keeper_walk: 6 }, 'keeper_walk', 4)).toBe(6)
    expect(fpsFor({ keeper_walk: 6 }, 'keeper_dance', 4)).toBe(4)
  })

  it('setting a speed back to the drawn one (or clearing it) removes the override', () => {
    const a = withFps({}, 'keeper_walk', 6, 4)
    expect(a).toEqual({ keeper_walk: 6 })
    expect(withFps(a, 'keeper_walk', 4, 4)).toEqual({})
    expect(withFps(a, 'keeper_walk', undefined, 4)).toEqual({})
    expect(withFps(a, 'keeper_dance', 25, 4)).toEqual({ keeper_walk: 6, keeper_dance: 20 })
  })

  it('copies out for Codex as animationFps, sorted', () => {
    expect(JSON.parse(fpsExport({ keeper_walk: 6, keeper_dance: 5 }))).toEqual({ animationFps: { keeper_dance: 5, keeper_walk: 6 } })
    expect(Object.keys(JSON.parse(fpsExport({ b: 1, a: 2 })).animationFps)).toEqual(['a', 'b'])
  })
})
