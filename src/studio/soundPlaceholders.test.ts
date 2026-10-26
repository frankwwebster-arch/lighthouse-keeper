import { describe, expect, it } from 'vitest'
import { SOUND_PLACEHOLDER_IDS, SOUND_PLACEHOLDERS } from './soundPlaceholders'

describe('studio sound placeholders', () => {
  it('have unique stable ids that the sound library can replace by name', () => {
    expect(new Set(SOUND_PLACEHOLDER_IDS).size).toBe(SOUND_PLACEHOLDER_IDS.length)
    expect(SOUND_PLACEHOLDER_IDS.every((id) => /^[a-z0-9_-]+$/.test(id))).toBe(true)
  })

  it('includes the hidden stone-stairwell travel cue with an explicit scope', () => {
    expect(SOUND_PLACEHOLDERS).toContainEqual(expect.objectContaining({
      id: 'footsteps_stone_stairwell',
      scope: 'hidden-stair-travel',
    }))
  })
})
