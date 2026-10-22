/**
 * “Tell Claude” notes (Frank, 21 Oct): under each bubble story Frank describes
 * a tweak in plain English; Claude reads every note at the start of a
 * session, makes the change and replies in the same thread. Kept apart from
 * the story itself (`notes-<story id>` beside `story-<id>`), so saving a story
 * never touches its notes and a note never needs a Save.
 */

export const NOTES_SCHEMA = 'lighthouse-keeper/story-notes@1'
export const NOTE_MAX = 4000

export interface StoryNote {
  id: string
  /** `frank` is whoever writes in the studio; `claude` is Claude's reply. */
  by: 'frank' | 'claude'
  text: string
  at: string
}

export interface StoryNotes {
  schema: typeof NOTES_SCHEMA
  story: string
  thread: StoryNote[]
}

export const notesDocId = (story: string) => `notes-${story}`
export const isStoryId = (id: string) => /^[a-z0-9][a-z0-9-]{0,59}$/.test(id)

export function newNote(by: StoryNote['by'], text: string, now = new Date()): StoryNote {
  return { id: `${now.getTime().toString(36)}-${Math.random().toString(36).slice(2, 6)}`, by, text: text.trim().slice(0, NOTE_MAX), at: now.toISOString() }
}

export function cleanNotes(raw: unknown): StoryNotes | null {
  const r = raw as Partial<StoryNotes> | null
  if (!r || typeof r !== 'object' || typeof r.story !== 'string' || !isStoryId(r.story)) return null
  const thread = (Array.isArray(r.thread) ? r.thread : []).flatMap((n): StoryNote[] => {
    const m = n as Partial<StoryNote>
    if (!m || typeof m.id !== 'string' || (m.by !== 'frank' && m.by !== 'claude') || typeof m.text !== 'string' || !m.text.trim() || typeof m.at !== 'string') return []
    return [{ id: m.id, by: m.by, text: m.text.slice(0, NOTE_MAX), at: m.at }]
  })
  return { schema: NOTES_SCHEMA, story: r.story, thread }
}

/** A thread is waiting for Claude when its newest note is Frank's. */
export const waitingForClaude = (n: StoryNotes | undefined) => n?.thread.at(-1)?.by === 'frank'

// ── In the browser ──

const LOCAL = 'lighthouse-keeper:story-notes'

function readLocal(): Record<string, StoryNotes> {
  try {
    const raw = JSON.parse(localStorage.getItem(LOCAL) ?? '{}') as Record<string, unknown>
    return Object.fromEntries(Object.entries(raw).flatMap(([id, d]) => {
      const n = cleanNotes(d)
      return n ? [[id, n]] : []
    }))
  } catch {
    return {}
  }
}

/** Every story's notes, from the docs `/api/studio` returned (or this browser's copy without a database). */
export function notesFrom(docs: { id: string; doc: unknown }[] | null): Record<string, StoryNotes> {
  if (!docs) return readLocal()
  const out: Record<string, StoryNotes> = {}
  for (const d of docs) {
    if (!d.id.startsWith('notes-')) continue
    const n = cleanNotes(d.doc)
    if (n) out[n.story] = n
  }
  return out
}

/** Adds Frank's note to a story's thread. Returns the thread as saved, or null if it couldn't be saved. */
export async function sendNote(story: string, text: string, db: boolean): Promise<StoryNotes | null> {
  if (!db) {
    const all = readLocal()
    const n = all[story] ?? { schema: NOTES_SCHEMA, story, thread: [] }
    const next = { ...n, thread: [...n.thread, newNote('frank', text)] }
    try {
      localStorage.setItem(LOCAL, JSON.stringify({ ...all, [story]: next }))
      return next
    } catch {
      return null
    }
  }
  const res = await fetch(`/api/studio/notes/${story}`, { method: 'POST', headers: { 'content-type': 'application/json' }, body: JSON.stringify({ text }) }).catch(() => null)
  return res?.ok ? cleanNotes(await res.json()) : null
}

/** Takes back one of Frank's own notes (Claude's replies stay). */
export async function removeNote(story: string, id: string, db: boolean): Promise<StoryNotes | null> {
  if (!db) {
    const all = readLocal()
    const n = all[story]
    if (!n) return null
    const next = { ...n, thread: n.thread.filter((m) => m.id !== id || m.by !== 'frank') }
    try {
      localStorage.setItem(LOCAL, JSON.stringify({ ...all, [story]: next }))
      return next
    } catch {
      return null
    }
  }
  const res = await fetch(`/api/studio/notes/${story}?note=${encodeURIComponent(id)}`, { method: 'DELETE' }).catch(() => null)
  return res?.ok ? cleanNotes(await res.json()) : null
}
