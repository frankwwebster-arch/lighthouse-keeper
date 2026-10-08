import { NextResponse } from 'next/server'
import { ensureSchema, hasDb, hashPin, pinOk, sql } from '../../../lib/db'

export const dynamic = 'force-dynamic'

/** Is this the grown-ups' PIN? (It starts as 1234.) */
export async function POST(req: Request) {
  if (!hasDb()) return NextResponse.json({ ok: false, db: false })
  const body = (await req.json().catch(() => ({}))) as { pin?: unknown }
  await ensureSchema()
  return NextResponse.json({ ok: await pinOk(body.pin), db: true })
}

export async function PUT(req: Request) {
  if (!hasDb()) return NextResponse.json({ error: 'no database' }, { status: 503 })
  const body = (await req.json().catch(() => ({}))) as { pin?: unknown; newPin?: unknown }
  await ensureSchema()
  if (!(await pinOk(body.pin))) return NextResponse.json({ error: 'wrong pin' }, { status: 403 })
  if (typeof body.newPin !== 'string' || !/^\d{3,8}$/.test(body.newPin)) return NextResponse.json({ error: 'pin must be 3-8 digits' }, { status: 400 })
  await sql()`insert into settings (key, value) values ('pin', ${hashPin(body.newPin)}) on conflict (key) do update set value = excluded.value`
  return NextResponse.json({ ok: true })
}
