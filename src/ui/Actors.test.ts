import { describe, expect, it } from 'vitest'
import { cleaningClipForTier, primeTravelClipFor } from './Actors'
import { primeActionClipFor, primeActionPlanFor, primeVerticalClipFor } from './primeChoreography'

describe('cleaningClipForTier', () => {
  it('selects the broom, basic hoover and super hoover progression', () => {
    expect(cleaningClipForTier(1)).toBe('sweep_broom')
    expect(cleaningClipForTier(2)).toBe('hoover_basic')
    expect(cleaningClipForTier(3)).toBe('hoover_super')
    expect(cleaningClipForTier(4)).toBe('hoover_super')
  })
})

describe('Prime action choreography', () => {
  it('uses installed sit, seated neutral and stand clips for ordinary seated leisure', () => {
    expect(primeActionClipFor('tv_watch', 0, 20)).toBe('keeper_prime_sit_side-right')
    expect(primeActionClipFor('tv_watch', 1, 20)).toBe('keeper_prime_neutral_sitting-side-right')
    expect(primeActionClipFor('tv_watch', 20, 0.5)).toBe('keeper_prime_stand_side-right')
  })

  it('turns to the rear, sits, holds, stands and returns to side for diary work', () => {
    expect(primeActionClipFor('desk_diary', 0, 20)).toBe('keeper_prime_turn_side-right_to_back')
    expect(primeActionClipFor('desk_diary', 0.7, 20)).toBe('keeper_prime_sit_back')
    expect(primeActionClipFor('desk_diary', 2, 20)).toBe('keeper_prime_neutral_sitting-back')
    expect(primeActionClipFor('desk_diary', 20, 1)).toBe('keeper_prime_stand_back')
    expect(primeActionClipFor('desk_diary', 20, 0.2)).toBe('keeper_prime_turn_back_to_side-right')
  })

  it('uses approved rear turns around the rear-work loop', () => {
    expect(primeActionClipFor('cooker_cook', 0, 20)).toBe('keeper_prime_turn_side-right_to_back')
    expect(primeActionClipFor('cooker_cook', 1, 20)).toBe('keeper_prime_rear_work')
    expect(primeActionClipFor('cooker_cook', 20, 0.2)).toBe('keeper_prime_turn_back_to_side-right')
  })

  it('prepares the installed ladder and darts clips without inventing consumers', () => {
    expect(primeVerticalClipFor('ladder-up')).toBe('keeper_prime_ladder_climb')
    expect(primeActionPlanFor('play_darts')?.hold).toBe('keeper_prime_darts_throw')
    expect(primeActionPlanFor('pet_play')).toBeNull()
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
