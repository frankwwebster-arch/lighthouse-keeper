import { describe, expect, it } from 'vitest'
import { reviewArchiveEntry, reviewArchiveStats } from './reviewArchive'

describe('review archive lookup', () => {
  it('resolves a historical review path to its immutable external object', () => {
    const entry = reviewArchiveEntry('/keeper-review/keeper-prime-turn-side-back-v9/assets/frame9-31dbac4efc00089f.png')
    expect(entry?.sha256).toBe('31dbac4efc00089fe6f831dc23f8397b4e3a8faf4d4aaa09a92b2ff407eebc35')
    expect(entry?.url).toContain(`/31/${entry?.sha256}.png`)
    expect(entry?.url).toMatch(/^https:\/\/raw\.githubusercontent\.com\//)
  })

  it('fails closed for unknown and out-of-scope paths', () => {
    expect(reviewArchiveEntry('/keeper-review/not-real/assets/missing.png')).toBeNull()
    expect(reviewArchiveEntry('/sprites/keeper_walk.png')).toBeNull()
  })

  it('resolves oversized review data without changing its historical URL', () => {
    const entry = reviewArchiveEntry('/keeper-review/activity-cloud-composer-v7/catalogue.json')
    expect(entry?.sha256).toBe('8657470a3103bd8c65771b8ea4f21c75d1b95cd057e8c2a8736f8c4c8b1132a0')
    expect(entry?.url).toContain(`/86/${entry?.sha256}.json`)
  })

  it('records material deduplication', () => {
    expect(reviewArchiveStats.referenceCount).toBeGreaterThan(500)
    expect(reviewArchiveStats.uniqueObjectCount).toBeLessThan(reviewArchiveStats.referenceCount)
    expect(reviewArchiveStats.deduplicatedBytes).toBeGreaterThan(20 * 1024 * 1024)
  })
})
