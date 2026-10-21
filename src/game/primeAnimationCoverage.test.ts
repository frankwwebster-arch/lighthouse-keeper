import { describe, expect, it } from 'vitest'
import gaps from '../../data/keeper_prime_animation_gaps.json'
import { INTERACTIONS } from './config'

describe('Prime Keeper animation gap inventory', () => {
  it('classifies every current interaction exactly once', () => {
    const classified = gaps.priorities.flatMap((group) => group.interactionIds)
    const current = INTERACTIONS.map((interaction) => interaction.id)
    expect([...classified].sort()).toEqual([...current].sort())
    expect(new Set(classified).size).toBe(classified.length)
  })

  it('keeps runtime totals aligned with the promoted bank', () => {
    expect(gaps.installedNow.runtimeSprites).toBe(27)
    expect(gaps.installedNow.registeredFrames).toBe(217)
  })
})
