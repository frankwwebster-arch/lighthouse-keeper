import { CHATS } from './chat'
import { DEFAULT_RULES, NEEDS } from './config'
import type { State } from './engine'
import { freshMissions } from './missions'

const KEY = (id: string) => `lighthouse-keeper:save:${id}`

/** Keep the game in the browser. */
export function save(id: string, s: State): void {
  try {
    localStorage.setItem(KEY(id), JSON.stringify(s))
  } catch {
    // Private mode or full storage: he just will not remember.
  }
}

/** Tidy a saved game that came from the browser or the database (older saves may lack newer fields). */
export function revive(s: State | null): State | null {
  try {
    if (!s || s.v !== 1 || typeof s.clock !== 'number' || !s.needs) return null
    // JSON turns Infinity into null; and a saved chat question has lost its test for the time.
    s.thunderAt = s.thunderAt ?? Infinity
    s.rules = { ...DEFAULT_RULES, ...(s.rules ?? {}) }
    s.broken = Array.isArray(s.broken) ? s.broken : []
    s.unlocked = Array.isArray(s.unlocked) ? s.unlocked : []
    s.missions = s.missions && Array.isArray(s.missions.done) ? { done: s.missions.done, progress: s.missions.progress ?? {} } : freshMissions()
    s.tally.needSums = { ...Object.fromEntries(NEEDS.map((n) => [n, 0])), ...(s.tally.needSums ?? {}) } as typeof s.tally.needSums
    if (s.prompt?.kind === 'chat') {
      const saved = s.prompt.chat
      const found = CHATS.find((c) => c.id === saved.id)
      s.prompt = found ? { kind: 'chat', chat: found } : null
    }
    return s
  } catch {
    return null
  }
}

/** The copy kept in this browser for a player. */
export function load(id: string): State | null {
  try {
    const raw = localStorage.getItem(KEY(id))
    return raw ? revive(JSON.parse(raw) as State) : null
  } catch {
    return null
  }
}

export function clear(id: string): void {
  try {
    localStorage.removeItem(KEY(id))
  } catch {
    // nothing to do
  }
}
