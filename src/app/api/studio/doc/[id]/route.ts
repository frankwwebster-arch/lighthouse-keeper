import { NextResponse } from 'next/server'
import { ensureSchema, hasDb, pinOk, sql } from '../../../../../lib/db'
import { cleanCategory, cleanRecipe } from '../../../../../studio/recipe'

export const dynamic = 'force-dynamic'

/** Save Frank's version of a recipe or macro (it wins over the draft). */
export async function PUT(req: Request, { params }: { params: { id: string } }) {
  if (!hasDb()) return NextResponse.json({ error: 'no database' }, { status: 503 })
  const body = (await req.json().catch(() => ({}))) as { pin?: unknown; doc?: unknown }
  await ensureSchema()
  if (!(await pinOk(body.pin))) return NextResponse.json({ error: 'wrong pin' }, { status: 403 })
  // Object types are kept as `cat-<id>`, so they never clash with a recipe of the same name.
  const isType = params.id.startsWith('cat-')
  const doc = isType ? cleanCategory(body.doc) : cleanRecipe(body.doc)
  if (!doc || (isType ? `cat-${doc.id}` : doc.id) !== params.id) return NextResponse.json({ error: isType ? 'not an object type' : 'not a recipe' }, { status: 400 })
  const meta = (body.doc as { draftHash?: unknown }).draftHash
  const saved = { ...doc, draftHash: typeof meta === 'string' ? meta : undefined }
  await sql()`insert into studio_docs (id, doc, updated_at) values (${params.id}, ${JSON.stringify(saved)}, now()) on conflict (id) do update set doc = excluded.doc, updated_at = now()`
  return NextResponse.json({ ok: true })
}

/** Forget Frank's version, so the draft shows again. */
export async function DELETE(req: Request, { params }: { params: { id: string } }) {
  if (!hasDb()) return NextResponse.json({ error: 'no database' }, { status: 503 })
  const body = (await req.json().catch(() => ({}))) as { pin?: unknown }
  await ensureSchema()
  if (!(await pinOk(body.pin))) return NextResponse.json({ error: 'wrong pin' }, { status: 403 })
  await sql()`delete from studio_docs where id = ${params.id}`
  return NextResponse.json({ ok: true })
}
