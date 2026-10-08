import { CHATS } from './chat'
import { DEFAULT_RULES, NEEDS } from './config'
import type { State } from './engine'

const KEY = 'lighthouse-keeper:v1'

/** Keep the game in the browser. */
export function save(s: State): void {
  try {
    localStorage.setItem(KEY, JSON.stringify(s))
  } catch {
    // Private mode or full storage: he just will not remember.
  }
}

/** Bring a saved game back (or null if there is none, or it is no good). */
export function load(): State | null {
  try {
    const raw = localStorage.getItem(KEY)
    if (!raw) return null
    const s = JSON.parse(raw) as State
    if (s.v !== 1 || typeof s.clock !== 'number' || !s.needs) return null
    // JSON turns Infinity into null; and a saved chat question has lost its test for the time.
    s.thunderAt = s.thunderAt ?? Infinity
    s.rules = { ...DEFAULT_RULES, ...(s.rules ?? {}) }
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

export function clear(): void {
  try {
    localStorage.removeItem(KEY)
  } catch {
    // nothing to do
  }
}

// ─── The grown-ups' dials, kept apart so a new game keeps them ──────────────

import type { Rules } from './config'
const ADMIN = 'lighthouse-keeper:admin:v1'

export interface Admin {
  pin: string
  rules: Rules
}

export function loadAdmin(): Admin {
  try {
    const raw = localStorage.getItem(ADMIN)
    if (raw) {
      const a = JSON.parse(raw) as Partial<Admin>
      return { pin: typeof a.pin === 'string' && a.pin ? a.pin : '1234', rules: { ...DEFAULT_RULES, ...(a.rules ?? {}) } }
    }
  } catch {
    // fall through to the defaults
  }
  return { pin: '1234', rules: { ...DEFAULT_RULES } }
}

export function saveAdmin(a: Admin): void {
  try {
    localStorage.setItem(ADMIN, JSON.stringify(a))
  } catch {
    // nothing to do
  }
}
