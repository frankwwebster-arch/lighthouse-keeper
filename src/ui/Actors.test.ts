import { describe, expect, it } from 'vitest'
import { cleaningClipForTier, primeTravelClipFor } from './Actors'

describe('cleaningClipForTier', () => {
  it('selects the broom, basic hoover and super hoover progression', () => {
    expect(cleaningClipForTier(1)).toBe('sweep_broom')
    expect(cleaningClipForTier(2)).toBe('hoover_basic')
    expect(cleaningClipForTier(3)).toBe('hoover_super')
    expect(cleaningClipForTier(4)).toBe('hoover_super')
  })
})

describe('primeTravelClipFor', () => {
  it('binds every supported travel phase to the promoted Prime bank', () => {
    expect(primeTravelClipFor('idle')).toBe('keeper_prime_neutral_standing-side-right')
    expect(primeTravelClipFor('walk-start')).toBe('keeper_prime_walk_side_start')
    expect(primeTravelClipFor('walk')).toBe('keeper_prime_walk_side_cycle')
    expect(primeTravelClipFor('walk-stop')).toBe('keeper_prime_walk_side_stop')
    expect(primeTravelClipFor('stairs-up')).toBe('keeper_prime_stairs_up')
    expect(primeTravelClipFor('stairs-down')).toBe('keeper_prime_stairs_down')
  })

  it('keeps the lift visibly neutral until a lift-specific clip exists', () => {
    expect(primeTravelClipFor('lift')).toBeNull()
  })
})
