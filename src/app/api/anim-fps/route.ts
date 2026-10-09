import { NextResponse } from 'next/server'
import { cleanFps } from '../../../game/animFps'
import { ensureSchema, hasDb, pinOk, sql } from '../../../lib/db'

export const dynamic = 'force-dynamic'

/** The grown-ups' animation speeds: one set for the whole game (src/game/animFps.ts). */
export async function GET() {
  if (!hasDb()) return NextResponse.json({ db: false, fps: {} })
  await ensureSchema()
  const rows = (await sql()`select value from settings where key = 'animFps'`) as { value: string }[]
  let fps = {}
  try {
    fps = cleanFps(JSON.parse(rows[0]?.value ?? '{}'))
  } catch {
    // a damaged value is treated as no changes
  }
  return NextResponse.json({ db: true, fps })
}

export async function PUT(req: Request) {
  if (!hasDb()) return NextResponse.json({ error: 'no database' }, { status: 503 })
  const body = (await req.json().catch(() => ({}))) as { pin?: unknown; fps?: unknown }
  await ensureSchema()
  if (!(await pinOk(body.pin))) return NextResponse.json({ error: 'wrong pin' }, { status: 403 })
  const fps = cleanFps(body.fps)
  await sql()`insert into settings (key, value) values ('animFps', ${JSON.stringify(fps)}) on conflict (key) do update set value = excluded.value`
  return NextResponse.json({ ok: true, fps })
}
