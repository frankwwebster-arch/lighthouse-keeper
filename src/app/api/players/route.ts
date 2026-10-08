import { NextResponse } from 'next/server'
import { ensureSchema, hasDb, sql } from '../../../lib/db'

export const dynamic = 'force-dynamic'

/** Who can play. With no database, `db: false` tells the game to keep things in the browser. */
export async function GET() {
  if (!hasDb()) return NextResponse.json({ db: false, players: [] })
  try {
    await ensureSchema()
    const players = await sql()`select id, name from players order by created_at`
    return NextResponse.json({ db: true, players })
  } catch {
    return NextResponse.json({ db: false, players: [] })
  }
}

export async function POST(req: Request) {
  if (!hasDb()) return NextResponse.json({ error: 'no database' }, { status: 503 })
  const body = (await req.json().catch(() => ({}))) as { name?: unknown }
  const name = typeof body.name === 'string' ? body.name.trim().slice(0, 24) : ''
  if (!name) return NextResponse.json({ error: 'name needed' }, { status: 400 })
  await ensureSchema()
  const id = `${name.toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/^-|-$/g, '').slice(0, 20) || 'player'}-${Math.random().toString(36).slice(2, 7)}`
  await sql()`insert into players (id, name) values (${id}, ${name})`
  return NextResponse.json({ id, name })
}
