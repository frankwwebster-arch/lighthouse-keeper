/**
 * Where Frank's versions of bubble stories are kept. With the database (live
 * site) they are saved for everyone as `story-<id>` beside the recipe
 * studio's documents, with no PIN (Frank, 21 Oct). Without it (a local copy)
 * they stay in this browser. Either way they win over the drafts in
 * data/activity-stories/stories/.
 */

import { cleanStory, type Story } from './format'

export interface SavedStory extends Story {
  /** The draft it was edited from, so the studio can tell when the draft has changed since. */
  draftHash?: string
}

const LOCAL = 'lighthouse-keeper:activity-stories'
export const storyDocId = (id: string) => `story-${id}`

/** A short, stable fingerprint of a story's content. */
export function storyHash(s: Story): string {
  const text = JSON.stringify({ ...s, notes: undefined })
  let h = 2166136261
  for (let i = 0; i < text.length; i++) h = Math.imul(h ^ text.charCodeAt(i), 16777619)
  return (h >>> 0).toString(16)
}

function readLocal(): Record<string, SavedStory> {
  try {
    const raw = JSON.parse(localStorage.getItem(LOCAL) ?? '{}') as Record<string, unknown>
    return Object.fromEntries(Object.entries(raw).flatMap(([id, d]) => {
      const s = cleanStory(d)
      return s ? [[id, { ...s, draftHash: (d as SavedStory).draftHash }]] : []
    }))
  } catch {
    return {}
  }
}

export async function loadStories(): Promise<{ db: boolean; saved: Record<string, SavedStory> }> {
  try {
    const res = await fetch('/api/studio')
    const r = res.ok ? ((await res.json()) as { db: boolean; docs: { id: string; doc: unknown }[] }) : null
    if (r?.db) {
      const saved: Record<string, SavedStory> = {}
      for (const d of r.docs) {
        if (!d.id.startsWith('story-')) continue
        const s = cleanStory(d.doc)
        if (s) saved[s.id] = { ...s, draftHash: (d.doc as SavedStory).draftHash }
      }
      return { db: true, saved }
    }
  } catch {
    // no server: work locally
  }
  return { db: false, saved: readLocal() }
}

export async function saveStory(story: SavedStory, db: boolean): Promise<boolean> {
  if (!db) {
    try {
      localStorage.setItem(LOCAL, JSON.stringify({ ...readLocal(), [story.id]: story }))
      return true
    } catch {
      return false
    }
  }
  const res = await fetch(`/api/studio/doc/${storyDocId(story.id)}`, { method: 'PUT', headers: { 'content-type': 'application/json' }, body: JSON.stringify({ doc: story }) }).catch(() => null)
  return !!res?.ok
}

/** Forget Frank's version, so the draft shows again. */
export async function resetStory(id: string, db: boolean): Promise<boolean> {
  if (!db) {
    const all = readLocal()
    delete all[id]
    try {
      localStorage.setItem(LOCAL, JSON.stringify(all))
    } catch {
      return false
    }
    return true
  }
  const res = await fetch(`/api/studio/doc/${storyDocId(id)}`, { method: 'DELETE' }).catch(() => null)
  return !!res?.ok
}
