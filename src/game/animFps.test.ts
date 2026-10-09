import { describe, expect, it } from 'vitest'
import { FPS, clampFps, cleanFps, fpsExport, fpsFor, isTweaked, pruneFps, withFps } from './animFps'

describe('animation speeds', () => {
  it('keeps speeds in range and on the half-step, like the review page', () => {
    expect(clampFps(0)).toBe(FPS.min)
    expect(clampFps(99)).toBe(FPS.max)
    expect(clampFps(4.3)).toBe(4.5)
    expect(clampFps(4.2)).toBe(4)
  })

  it('drops anything that is not a sensible name, speed and sheet speed', () => {
    expect(cleanFps(null)).toEqual({})
    expect(cleanFps([4])).toEqual({})
    expect(
      cleanFps({
        keeper_walk: { fps: 6, drawn: 4 },
        keeper_dance: { fps: '7.5', drawn: '4' },
        keeper_cross: { fps: 50, drawn: 4 },
        'bad name': { fps: 4, drawn: 4 },
        keeper_sad: { fps: 'fast', drawn: 4 },
        keeper_yawn: { fps: 5 },
        keeper_bored: 6,
      }),
    ).toEqual({ keeper_walk: { fps: 6, drawn: 4 }, keeper_dance: { fps: 7.5, drawn: 4 }, keeper_cross: { fps: 20, drawn: 4 } })
  })

  it('plays at the grown-ups’ speed while the sheet still has the speed it was set against', () => {
    const o = withFps({}, 'keeper_walk', 6, 4)
    expect(fpsFor(o, 'keeper_walk', 4)).toBe(6)
    expect(isTweaked(o, 'keeper_walk', 4)).toBe(true)
    expect(fpsFor(o, 'keeper_dance', 4)).toBe(4)
  })

  it('lets the sheet win once its metadata speed changes', () => {
    const o = withFps({}, 'keeper_walk', 6, 4)
    expect(fpsFor(o, 'keeper_walk', 5)).toBe(5)
    expect(isTweaked(o, 'keeper_walk', 5)).toBe(false)
    const sheets: Record<string, number> = { keeper_walk: 5, keeper_dance: 4 }
    const both = withFps(o, 'keeper_dance', 8, 4)
    expect(pruneFps(both, (n) => sheets[n])).toEqual({ keeper_dance: { fps: 8, drawn: 4 } })
    expect(pruneFps(both, () => undefined)).toEqual({})
  })

  it('setting a speed back to the sheet’s (or clearing it) removes the tweak', () => {
    const a = withFps({}, 'keeper_walk', 6, 4)
    expect(withFps(a, 'keeper_walk', 4, 4)).toEqual({})
    expect(withFps(a, 'keeper_walk', undefined, 4)).toEqual({})
    expect(withFps(a, 'keeper_dance', 25, 4)).toEqual({ keeper_walk: { fps: 6, drawn: 4 }, keeper_dance: { fps: 20, drawn: 4 } })
  })

  it('copies out as animationFps for the metadata, sorted', () => {
    const o = withFps(withFps({}, 'keeper_walk', 6, 4), 'keeper_dance', 5, 4)
    expect(JSON.parse(fpsExport(o))).toEqual({ animationFps: { keeper_dance: 5, keeper_walk: 6 } })
    expect(Object.keys(JSON.parse(fpsExport(o)).animationFps)).toEqual(['keeper_dance', 'keeper_walk'])
  })
})
