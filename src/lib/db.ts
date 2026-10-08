import { neon } from '@neondatabase/serverless'
import { createHash } from 'node:crypto'

/** The database is optional: with no DATABASE_URL the game keeps everything in the browser. */
export const hasDb = () => !!process.env.DATABASE_URL

let ready: Promise<void> | null = null

export function sql() {
  return neon(process.env.DATABASE_URL!)
}

/** Creates the tables the first time anything asks. Safe to run again. */
export function ensureSchema(): Promise<void> {
  if (!ready) {
    const q = sql()
    ready = (async () => {
      await q`create table if not exists players (id text primary key, name text not null, created_at timestamptz not null default now())`
      await q`create table if not exists saves (player_id text primary key references players(id) on delete cascade, state jsonb not null, updated_at timestamptz not null default now())`
      await q`create table if not exists player_rules (player_id text primary key references players(id) on delete cascade, rules jsonb not null)`
      await q`create table if not exists settings (key text primary key, value text not null)`
    })().catch((e) => {
      ready = null
      throw e
    })
  }
  return ready
}

export const hashPin = (pin: string) => createHash('sha256').update(`lighthouse-keeper:${pin}`).digest('hex')

export async function pinOk(pin: unknown): Promise<boolean> {
  if (typeof pin !== 'string' || !pin) return false
  const q = sql()
  const rows = (await q`select value from settings where key = 'pin'`) as { value: string }[]
  const stored = rows[0]?.value ?? hashPin('1234')
  return stored === hashPin(pin)
}

export const validId = (id: unknown): id is string => typeof id === 'string' && /^[a-z0-9-]{3,40}$/.test(id)
