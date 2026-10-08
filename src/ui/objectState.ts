import type { ObjectId } from '../game/config'
import type { ObjectVisualState } from './art'

export function parseBrokenPreview(value: string | null, all: readonly ObjectId[]): ReadonlySet<ObjectId> {
  if (!value) return new Set()
  if (value === 'all') return new Set(all)
  const valid = new Set<ObjectId>(all)
  return new Set(value.split(',').map((id) => id.trim() as ObjectId).filter((id) => valid.has(id)))
}

/** `?tiers=3` shows every object at its best tier up to 3; `?tiers=tv:3,bed:2` picks them. For checking art. */
export function parseTierPreview(value: string | null, maxOf: (id: ObjectId) => number, all: readonly ObjectId[]): Partial<Record<ObjectId, number>> {
  if (!value) return {}
  const out: Partial<Record<ObjectId, number>> = {}
  const valid = new Set<ObjectId>(all)
  const set = (id: ObjectId, n: number) => {
    if (valid.has(id) && Number.isFinite(n) && maxOf(id) > 1) out[id] = Math.max(1, Math.min(maxOf(id), Math.round(n)))
  }
  if (/^\d+$/.test(value.trim())) all.forEach((id) => set(id, Number(value)))
  else for (const part of value.split(',')) {
    const [id, n] = part.split(':').map((x) => x.trim())
    set(id as ObjectId, Number(n))
  }
  return out
}

export function visualStateFor(id: ObjectId, active: ObjectId | null, broken: ReadonlySet<ObjectId>): ObjectVisualState {
  if (broken.has(id)) return 'broken'
  return id === active ? 'on' : 'standard'
}
