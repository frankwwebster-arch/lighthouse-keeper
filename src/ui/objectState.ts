import type { ObjectId } from '../game/config'
import type { ObjectVisualState } from './art'

export function parseBrokenPreview(value: string | null, all: readonly ObjectId[]): ReadonlySet<ObjectId> {
  if (!value) return new Set()
  if (value === 'all') return new Set(all)
  const valid = new Set<ObjectId>(all)
  return new Set(value.split(',').map((id) => id.trim() as ObjectId).filter((id) => valid.has(id)))
}

export function visualStateFor(id: ObjectId, active: ObjectId | null, broken: ReadonlySet<ObjectId>): ObjectVisualState {
  if (broken.has(id)) return 'broken'
  return id === active ? 'on' : 'standard'
}
