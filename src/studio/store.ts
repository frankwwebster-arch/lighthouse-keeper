/**
 * Where the recipe studio keeps Frank's work: his versions of recipes and
 * macros, and the sound library. With the database (live site) they are
 * saved for everyone, behind the grown-ups' PIN. Without it (a local copy)
 * recipes stay in this browser and sounds only last until the page closes.
 */

import { cleanRecipe, type Recipe } from './recipe'

export interface SavedDoc extends Recipe {
  /** The draft it was edited from, so the studio can tell when the draft has changed since. */
  draftHash?: string
}

export interface SoundInfo {
  id: string
  label: string
  mime: string
  bytes: number
  updatedAt: string
  /** Where to fetch the audio from. */
  url: string
}

const LOCAL_DOCS = 'lighthouse-keeper:studio-docs'
const localSounds = new Map<string, SoundInfo>()

const soundUrl = (id: string, updatedAt: string) => `/api/studio/sound/${id}?v=${encodeURIComponent(updatedAt)}`

function readLocalDocs(): Record<string, SavedDoc> {
  try {
    const raw = JSON.parse(localStorage.getItem(LOCAL_DOCS) ?? '{}') as Record<string, unknown>
    return Object.fromEntries(Object.entries(raw).flatMap(([id, d]) => {
      const doc = cleanRecipe(d)
      return doc ? [[id, { ...doc, draftHash: (d as SavedDoc).draftHash }]] : []
    }))
  } catch {
    return {}
  }
}

export async function loadStudio(): Promise<{ db: boolean; saved: Record<string, SavedDoc>; sounds: SoundInfo[] }> {
  try {
    const res = await fetch('/api/studio')
    const r = res.ok ? ((await res.json()) as { db: boolean; docs: { id: string; doc: unknown; updatedAt: string }[]; sounds: Omit<SoundInfo, 'url'>[] }) : null
    if (r?.db) {
      const saved: Record<string, SavedDoc> = {}
      for (const d of r.docs) {
        const doc = cleanRecipe(d.doc)
        if (doc) saved[doc.id] = { ...doc, draftHash: (d.doc as SavedDoc).draftHash }
      }
      return { db: true, saved, sounds: r.sounds.map((s) => ({ ...s, url: soundUrl(s.id, s.updatedAt) })) }
    }
  } catch {
    // no server: work locally
  }
  return { db: false, saved: readLocalDocs(), sounds: [...localSounds.values()] }
}

export async function saveDoc(pin: string, doc: SavedDoc, db: boolean): Promise<boolean> {
  if (!db) {
    try {
      localStorage.setItem(LOCAL_DOCS, JSON.stringify({ ...readLocalDocs(), [doc.id]: doc }))
      return true
    } catch {
      return false
    }
  }
  const res = await fetch(`/api/studio/doc/${doc.id}`, { method: 'PUT', headers: { 'content-type': 'application/json' }, body: JSON.stringify({ pin, doc }) }).catch(() => null)
  return !!res?.ok
}

/** Forget Frank's version (the draft shows again). */
export async function resetDoc(pin: string, id: string, db: boolean): Promise<boolean> {
  if (!db) {
    const all = readLocalDocs()
    delete all[id]
    try {
      localStorage.setItem(LOCAL_DOCS, JSON.stringify(all))
    } catch {
      return false
    }
    return true
  }
  const res = await fetch(`/api/studio/doc/${id}`, { method: 'DELETE', headers: { 'content-type': 'application/json' }, body: JSON.stringify({ pin }) }).catch(() => null)
  return !!res?.ok
}

/** A sound name from a file name: "Door Creak 02.wav" → "door_creak_02". */
export const soundIdFrom = (fileName: string) =>
  fileName
    .replace(/\.[a-z0-9]+$/i, '')
    .toLowerCase()
    .replace(/[^a-z0-9]+/g, '_')
    .replace(/^_+|_+$/g, '')
    .slice(0, 60) || 'sound'

export async function uploadSound(pin: string, id: string, file: File, db: boolean): Promise<SoundInfo | { error: string }> {
  if (!file.type.startsWith('audio/')) return { error: `${file.name} is not an audio file` }
  const now = new Date().toISOString()
  if (!db) {
    const info = { id, label: file.name, mime: file.type, bytes: file.size, updatedAt: now, url: URL.createObjectURL(file) }
    localSounds.set(id, info)
    return info
  }
  const res = await fetch(`/api/studio/sound/${id}`, { method: 'PUT', headers: { 'content-type': file.type, 'x-pin': pin, 'x-label': file.name }, body: file }).catch(() => null)
  if (!res?.ok) return { error: res ? (((await res.json().catch(() => ({}))) as { error?: string }).error ?? 'upload failed') : 'could not reach the server' }
  return { id, label: file.name, mime: file.type, bytes: file.size, updatedAt: now, url: soundUrl(id, now) }
}

export async function deleteSound(pin: string, id: string, db: boolean): Promise<boolean> {
  if (!db) return localSounds.delete(id)
  const res = await fetch(`/api/studio/sound/${id}`, { method: 'DELETE', headers: { 'x-pin': pin } }).catch(() => null)
  return !!res?.ok
}
