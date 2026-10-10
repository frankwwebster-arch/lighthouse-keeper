import { NextResponse } from 'next/server'
import { ensureSchema, hasDb, pinOk, sql } from '../../../../../lib/db'

export const dynamic = 'force-dynamic'

/** Sound effects are short: anything bigger is probably the wrong file. */
const MAX_BYTES = 3 * 1024 * 1024
const validId = (id: string) => /^[a-z0-9_-]{1,60}$/.test(id)

export async function GET(_req: Request, { params }: { params: { id: string } }) {
  if (!hasDb() || !validId(params.id)) return new NextResponse(null, { status: 404 })
  await ensureSchema()
  const rows = (await sql()`select mime, data from studio_sounds where id = ${params.id}`) as { mime: string; data: string }[]
  if (!rows[0]) return new NextResponse(null, { status: 404 })
  return new NextResponse(Buffer.from(rows[0].data, 'base64'), { headers: { 'content-type': rows[0].mime, 'cache-control': 'private, max-age=0, must-revalidate' } })
}

/** Upload (or replace) a sound: the audio is the request body; the PIN and a label travel in headers. */
export async function PUT(req: Request, { params }: { params: { id: string } }) {
  if (!hasDb()) return NextResponse.json({ error: 'no database' }, { status: 503 })
  if (!validId(params.id)) return NextResponse.json({ error: 'sound names are lower-case letters, digits, - and _' }, { status: 400 })
  await ensureSchema()
  if (!(await pinOk(req.headers.get('x-pin')))) return NextResponse.json({ error: 'wrong pin' }, { status: 403 })
  const mime = (req.headers.get('content-type') ?? '').split(';')[0].trim()
  if (!mime.startsWith('audio/')) return NextResponse.json({ error: 'not an audio file' }, { status: 415 })
  const bytes = new Uint8Array(await req.arrayBuffer())
  if (!bytes.length) return NextResponse.json({ error: 'empty file' }, { status: 400 })
  if (bytes.length > MAX_BYTES) return NextResponse.json({ error: 'too big: keep sound effects under 3 MB' }, { status: 413 })
  const label = (req.headers.get('x-label') ?? params.id).slice(0, 120)
  const data = Buffer.from(bytes).toString('base64')
  await sql()`insert into studio_sounds (id, label, mime, data, bytes, updated_at) values (${params.id}, ${label}, ${mime}, ${data}, ${bytes.length}, now()) on conflict (id) do update set label = excluded.label, mime = excluded.mime, data = excluded.data, bytes = excluded.bytes, updated_at = now()`
  return NextResponse.json({ ok: true, bytes: bytes.length })
}

export async function DELETE(req: Request, { params }: { params: { id: string } }) {
  if (!hasDb()) return NextResponse.json({ error: 'no database' }, { status: 503 })
  await ensureSchema()
  if (!(await pinOk(req.headers.get('x-pin')))) return NextResponse.json({ error: 'wrong pin' }, { status: 403 })
  await sql()`delete from studio_sounds where id = ${params.id}`
  return NextResponse.json({ ok: true })
}
