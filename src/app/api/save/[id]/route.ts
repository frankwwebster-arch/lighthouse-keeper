import { NextResponse } from 'next/server'
import { ensureSchema, hasDb, sql, validId } from '../../../../lib/db'

export const dynamic = 'force-dynamic'

export async function GET(_req: Request, { params }: { params: { id: string } }) {
  if (!hasDb() || !validId(params.id)) return NextResponse.json({ state: null })
  await ensureSchema()
  const rows = (await sql()`select state from saves where player_id = ${params.id}`) as { state: unknown }[]
  return NextResponse.json({ state: rows[0]?.state ?? null })
}

export async function PUT(req: Request, { params }: { params: { id: string } }) {
  if (!hasDb() || !validId(params.id)) return NextResponse.json({ error: 'no' }, { status: 400 })
  const text = await req.text()
  if (text.length > 400_000) return NextResponse.json({ error: 'too big' }, { status: 413 })
  let state: { v?: number }
  try {
    state = JSON.parse(text)
  } catch {
    return NextResponse.json({ error: 'bad json' }, { status: 400 })
  }
  if (state.v !== 1) return NextResponse.json({ error: 'not a game' }, { status: 400 })
  await ensureSchema()
  const known = (await sql()`select 1 from players where id = ${params.id}`) as unknown[]
  if (!known.length) return NextResponse.json({ error: 'unknown player' }, { status: 404 })
  await sql()`insert into saves (player_id, state, updated_at) values (${params.id}, ${text}::jsonb, now()) on conflict (player_id) do update set state = excluded.state, updated_at = now()`
  return NextResponse.json({ ok: true })
}

export async function DELETE(_req: Request, { params }: { params: { id: string } }) {
  if (!hasDb() || !validId(params.id)) return NextResponse.json({ error: 'no' }, { status: 400 })
  await ensureSchema()
  await sql()`delete from saves where player_id = ${params.id}`
  return NextResponse.json({ ok: true })
}
