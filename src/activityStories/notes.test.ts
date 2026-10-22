import { describe, expect, it } from 'vitest'
import { cleanNotes, newNote, notesFrom, waitingForClaude } from './notes'

describe('Tell Claude notes', () => {
  it('keeps only well-formed notes, in order', () => {
    const n = cleanNotes({ story: 'lunch', thread: [newNote('frank', '  use the clean plate  '), { id: 'x', by: 'someone', text: 'hi', at: 'now' }, { id: 'y', by: 'claude', text: '', at: 'now' }, newNote('claude', 'Done.')] })
    expect(n?.thread.map((m) => [m.by, m.text])).toEqual([['frank', 'use the clean plate'], ['claude', 'Done.']])
  })

  it('refuses a thread for something that is not a story id', () => {
    expect(cleanNotes({ story: '../etc', thread: [] })).toBeNull()
    expect(cleanNotes(null)).toBeNull()
  })

  it('is waiting for Claude while Frank has the last word', () => {
    const asked = cleanNotes({ story: 'lunch', thread: [newNote('frank', 'a')] })!
    expect(waitingForClaude(asked)).toBe(true)
    expect(waitingForClaude({ ...asked, thread: [...asked.thread, newNote('claude', 'done')] })).toBe(false)
    expect(waitingForClaude(undefined)).toBe(false)
  })

  it('reads notes from the studio docs and ignores stories and recipes', () => {
    const docs = [
      { id: 'notes-lunch', doc: { story: 'lunch', thread: [newNote('frank', 'a')] } },
      { id: 'story-lunch', doc: { id: 'lunch' } },
      { id: 'make-tea', doc: {} },
    ]
    expect(Object.keys(notesFrom(docs))).toEqual(['lunch'])
  })
})
