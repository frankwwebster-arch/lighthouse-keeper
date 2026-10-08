import { describe, expect, it } from 'vitest'
import { CHATS, pickChat, replyToChat } from './chat'

describe('chat', () => {
  it('asks about school on a weekday afternoon', () => {
    const q = pickChat({ day: 3, hour: 16 }, [], 1)
    expect(q.when({ day: 3, hour: 16 })).toBe(true)
  })
  it('every time of the week has a question', () => {
    for (let day = 0; day < 7; day++) for (let h = 7; h < 21; h++) expect(CHATS.some((c) => c.when({ day, hour: h }))).toBe(true)
  })
  it('replies to good, bad and odd answers', () => {
    const q = CHATS[0]
    expect(replyToChat(q, 'great thanks').good).toBe(true)
    expect(replyToChat(q, 'terrible').good).toBe(false)
    expect(replyToChat(q, 'blah blah blah blah').line.length).toBeGreaterThan(0)
  })
})
