import { NextResponse } from 'next/server'
import { ensureSchema, hasDb, sql } from '../../../lib/db'

export const dynamic = 'force-dynamic'

/** Everything the recipe studio has saved: edited recipes and macros, and the sound library (without the audio itself). */
export async function GET() {
  if (!hasDb()) return NextResponse.json({ db: false, docs: [], sounds: [] })
  await ensureSchema()
  const q = sql()
  const docs = (await q`select id, doc, updated_at from studio_docs order by id`) as { id: string; doc: unknown; updated_at: string }[]
  const sounds = (await q`select id, label, mime, bytes, updated_at from studio_sounds order by id`) as { id: string; label: string; mime: string; bytes: number; updated_at: string }[]
  return NextResponse.json({
    db: true,
    docs: docs.map((d) => ({ id: d.id, doc: d.doc, updatedAt: d.updated_at })),
    sounds: sounds.map((s) => ({ id: s.id, label: s.label, mime: s.mime, bytes: s.bytes, updatedAt: s.updated_at })),
  })
}
