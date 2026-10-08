/**
 * Where a player's game lives. With the database connected (Neon, through the
 * /api routes) it is kept there, so a player can carry on from any device. If
 * there is no database, or it cannot be reached, everything stays in this
 * browser and the game still works.
 */

import { DEFAULT_RULES, type Rules } from './config'
import type { State } from './engine'
import { clear, load, revive, save } from './storage'

export interface Player {
  id: string
  name: string
}

const PLAYERS = 'lighthouse-keeper:players'
const RULES = (id: string) => `lighthouse-keeper:rules:${id}`
const PIN = 'lighthouse-keeper:pin'

async function api<T>(url: string, init?: RequestInit): Promise<T | null> {
  try {
    const res = await fetch(url, init)
    return res.ok ? ((await res.json()) as T) : null
  } catch {
    return null
  }
}
const json = (method: string, body: unknown): RequestInit => ({ method, headers: { 'content-type': 'application/json' }, body: JSON.stringify(body) })

const localPlayers = (): Player[] => {
  try {
    return JSON.parse(localStorage.getItem(PLAYERS) ?? '[]') as Player[]
  } catch {
    return []
  }
}

export async function listPlayers(): Promise<{ db: boolean; players: Player[] }> {
  const r = await api<{ db: boolean; players: Player[] }>('/api/players')
  return r?.db ? r : { db: false, players: localPlayers() }
}

export async function addPlayer(name: string, db: boolean): Promise<Player | null> {
  if (db) return api<Player>('/api/players', json('POST', { name }))
  const p = { id: `${name.toLowerCase().replace(/[^a-z0-9]+/g, '-').slice(0, 20) || 'player'}-${Math.random().toString(36).slice(2, 7)}`, name }
  try {
    localStorage.setItem(PLAYERS, JSON.stringify([...localPlayers(), p]))
  } catch {
    // no storage: still playable this once
  }
  return p
}

export async function loadGame(id: string, db: boolean): Promise<State | null> {
  if (db) {
    const r = await api<{ state: State | null }>(`/api/save/${id}`)
    if (r) return revive(r.state) ?? load(id)
  }
  return load(id)
}

/** Always kept in the browser too, so a dropped connection loses nothing. */
export function saveGame(id: string, s: State, db: boolean): void {
  save(id, s)
  if (db) void api(`/api/save/${id}`, { method: 'PUT', headers: { 'content-type': 'application/json' }, body: JSON.stringify(s) })
}

export function deleteGame(id: string, db: boolean): void {
  clear(id)
  if (db) void api(`/api/save/${id}`, { method: 'DELETE' })
}

export async function loadRules(id: string, db: boolean): Promise<Rules> {
  if (db) {
    const r = await api<{ rules: Partial<Rules> | null }>(`/api/rules/${id}`)
    if (r?.rules) return { ...DEFAULT_RULES, ...r.rules }
  }
  try {
    return { ...DEFAULT_RULES, ...(JSON.parse(localStorage.getItem(RULES(id)) ?? '{}') as Partial<Rules>) }
  } catch {
    return { ...DEFAULT_RULES }
  }
}

const localPin = () => {
  try {
    return localStorage.getItem(PIN) ?? '1234'
  } catch {
    return '1234'
  }
}

export async function verifyPin(pin: string, db: boolean): Promise<boolean> {
  if (db) return !!(await api<{ ok: boolean }>('/api/pin', json('POST', { pin })))?.ok
  return pin === localPin()
}

export async function saveRules(id: string, pin: string, rules: Rules, db: boolean): Promise<void> {
  try {
    localStorage.setItem(RULES(id), JSON.stringify(rules))
  } catch {
    // fine
  }
  if (db) await api(`/api/rules/${id}`, json('PUT', { pin, rules }))
}

export async function changePin(pin: string, newPin: string, db: boolean): Promise<boolean> {
  if (db) return !!(await api('/api/pin', json('PUT', { pin, newPin })))
  try {
    localStorage.setItem(PIN, newPin)
  } catch {
    return false
  }
  return true
}
