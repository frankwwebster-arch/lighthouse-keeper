#!/usr/bin/env node
/**
 * Frank's “Tell Claude” notes on bubble stories (studio_docs rows
 * `notes-<story id>`). Claude reads them at the start of every bubble-stories
 * session, makes each change, and replies in the same thread.
 *
 *   node --env-file=.env.local scripts/story_notes.mjs            every thread, waiting ones first
 *   node --env-file=.env.local scripts/story_notes.mjs waiting    only threads waiting for Claude
 *   node --env-file=.env.local scripts/story_notes.mjs reply <story-id> "Done: …"
 *
 * Listing is read-only. `reply` appends one Claude note to that story's thread.
 */

import { neon } from '@neondatabase/serverless'

if (!process.env.DATABASE_URL) {
  console.error('✗ no DATABASE_URL: run with --env-file=.env.local')
  process.exit(1)
}
const sql = neon(process.env.DATABASE_URL)
const [cmd = 'list', story, ...words] = process.argv.slice(2)

if (cmd === 'reply') {
  const text = words.join(' ').trim()
  if (!story || !/^[a-z0-9][a-z0-9-]{0,59}$/.test(story) || !text) {
    console.error('usage: story_notes.mjs reply <story-id> "text"')
    process.exit(1)
  }
  const now = new Date()
  const note = { id: `${now.getTime().toString(36)}-${Math.random().toString(36).slice(2, 6)}`, by: 'claude', text, at: now.toISOString() }
  const fresh = { schema: 'lighthouse-keeper/story-notes@1', story, thread: [note] }
  await sql`insert into studio_docs (id, doc, updated_at) values (${`notes-${story}`}, ${JSON.stringify(fresh)}, now())
    on conflict (id) do update set doc = jsonb_set(studio_docs.doc, '{thread}', coalesce(studio_docs.doc->'thread', '[]'::jsonb) || ${JSON.stringify([note])}::jsonb), updated_at = now()`
  console.log(`✓ replied on ${story}`)
  process.exit(0)
}

const rows = await sql`select id, doc, updated_at from studio_docs where id like 'notes-%' order by updated_at desc`
const threads = rows
  .map((r) => ({ story: r.doc?.story ?? r.id.slice(6), thread: Array.isArray(r.doc?.thread) ? r.doc.thread : [] }))
  .filter((t) => t.thread.length)
  .map((t) => ({ ...t, waiting: t.thread.at(-1).by === 'frank' }))
  .sort((a, b) => Number(b.waiting) - Number(a.waiting))
const shown = cmd === 'waiting' ? threads.filter((t) => t.waiting) : threads
if (!shown.length) console.log(cmd === 'waiting' ? 'No notes waiting for Claude.' : 'No notes yet.')
for (const t of shown) {
  console.log(`\n── ${t.story}${t.waiting ? '  ⟵ waiting for Claude' : ''}`)
  for (const n of t.thread) console.log(`  ${n.at.slice(0, 16).replace('T', ' ')}  ${n.by === 'frank' ? 'Frank ' : 'Claude'}  ${n.text.replace(/\n/g, '\n                            ')}`)
}
