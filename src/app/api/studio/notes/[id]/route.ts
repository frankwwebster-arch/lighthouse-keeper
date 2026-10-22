import { NextResponse } from 'next/server'
import { ensureSchema, hasDb, sql } from '../../../../../lib/db'
import { NOTES_SCHEMA, cleanNotes, isStoryId, newNote, notesDocId } from '../../../../../activityStories/notes'

export const dynamic = 'force-dynamic'

/** Adds a “Tell Claude” note to a bubble story's thread. No PIN, like the stories themselves (Frank, 21 Oct). */
export async function POST(req: Request, { params }: { params: { id: string } }) {
  if (!hasDb()) return NextResponse.json({ error: 'no database' }, { status: 503 })
  if (!isStoryId(params.id)) return NextResponse.json({ error: 'not a story' }, { status: 400 })
  const body = (await req.json().catch(() => ({}))) as { text?: unknown }
  if (typeof body.text !== 'string' || !body.text.trim()) return NextResponse.json({ error: 'empty note' }, { status: 400 })
  await ensureSchema()
  const note = newNote('frank', body.text)
  const fresh = { schema: NOTES_SCHEMA, story: params.id, thread: [note] }
  // Appended in the database, so two notes sent at once both survive.
  const rows = (await sql()`insert into studio_docs (id, doc, updated_at) values (${notesDocId(params.id)}, ${JSON.stringify(fresh)}, now())
    on conflict (id) do update set doc = jsonb_set(studio_docs.doc, '{thread}', coalesce(studio_docs.doc->'thread', '[]'::jsonb) || ${JSON.stringify([note])}::jsonb), updated_at = now()
    returning doc`) as { doc: unknown }[]
  return NextResponse.json(cleanNotes(rows[0]?.doc))
}

/** Takes back one of Frank's own notes (`?note=<id>`); Claude's replies stay. */
export async function DELETE(req: Request, { params }: { params: { id: string } }) {
  if (!hasDb()) return NextResponse.json({ error: 'no database' }, { status: 503 })
  const id = new URL(req.url).searchParams.get('note')
  if (!isStoryId(params.id) || !id) return NextResponse.json({ error: 'which note?' }, { status: 400 })
  await ensureSchema()
  const rows = (await sql()`update studio_docs set doc = jsonb_set(doc, '{thread}', coalesce((select jsonb_agg(e order by i) from jsonb_array_elements(doc->'thread') with ordinality t(e, i) where e->>'id' <> ${id} or e->>'by' <> 'frank'), '[]'::jsonb)), updated_at = now()
    where id = ${notesDocId(params.id)} returning doc`) as { doc: unknown }[]
  if (!rows.length) return NextResponse.json({ error: 'no notes' }, { status: 404 })
  return NextResponse.json(cleanNotes(rows[0].doc))
}
