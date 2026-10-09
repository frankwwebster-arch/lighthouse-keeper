import { describe, expect, it } from 'vitest'
import { cleaningClipForTier } from './Actors'

describe('cleaningClipForTier', () => {
  it('selects the broom, basic hoover and super hoover progression', () => {
    expect(cleaningClipForTier(1)).toBe('sweep_broom')
    expect(cleaningClipForTier(2)).toBe('hoover_basic')
    expect(cleaningClipForTier(3)).toBe('hoover_super')
    expect(cleaningClipForTier(4)).toBe('hoover_super')
  })
})
