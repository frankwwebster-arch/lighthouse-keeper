import { describe, expect, it } from 'vitest'
import { changedReviewNames } from './keeperReviewHandoff'

describe('changedReviewNames', () => {
  it('marks every record in the first handoff', () => {
    expect(changedReviewNames([
      { name: 'keeper_darts', happy: true },
      { name: 'keeper_walk', happy: false },
    ])).toEqual(['keeper_darts', 'keeper_walk'])
  })

  it('ignores save timestamps and object key order', () => {
    expect(changedReviewNames(
      [{ name: 'keeper_darts', notes: 'Keep hand shape', happy: true, updatedAt: '2026-10-11T08:00:00.000Z' }],
      [{ updatedAt: '2026-10-10T08:00:00.000Z', happy: true, name: 'keeper_darts', notes: 'Keep hand shape' }],
    )).toEqual([])
  })

  it('returns only decisions or notes that materially changed', () => {
    expect(changedReviewNames(
      [
        { name: 'keeper_darts', happy: false, redraftRequested: true, notes: 'Restore ragged side beard' },
        { name: 'keeper_walk', happy: true, notes: '' },
      ],
      [
        { name: 'keeper_darts', happy: true, redraftRequested: false, notes: '' },
        { name: 'keeper_walk', happy: true, notes: '' },
      ],
    )).toEqual(['keeper_darts'])
  })
})
