#!/usr/bin/env node
/**
 * Copies Frank's saved bubble stories (studio_docs rows `story-<id>`) from the
 * database into data/activity-stories/stories/, so Codex and Claude see them
 * in the repo. Read-only on the database. Run it when Frank says his stories
 * are ready, then review the diff and commit.
 *
 *   node --env-file=.env.local scripts/pull_activity_stories.mjs
 */

import fs from 'node:fs'
import path from 'node:path'
import { neon } from '@neondatabase/serverless'
import { STORIES_DIR } from './activity_story_pictures.mjs'

if (!process.env.DATABASE_URL) {
  console.error('✗ no DATABASE_URL: run with --env-file=.env.local')
  process.exit(1)
}
const rows = await neon(process.env.DATABASE_URL)`select id, doc, updated_at from studio_docs where id like 'story-%' order by id`
if (!rows.length) console.log('No saved stories yet: the drafts are current.')
for (const r of rows) {
  const { draftHash: _hash, ...story } = r.doc
  const file = path.join(STORIES_DIR, `${story.id}.json`)
  const was = fs.existsSync(file) ? fs.readFileSync(file, 'utf8') : null
  const next = JSON.stringify({ ...story, notes: `${story.notes ? `${story.notes} ` : ''}Frank's version, saved ${new Date(r.updated_at).toISOString().slice(0, 10)}.`.trim() }, null, 2) + '\n'
  if (was === next) continue
  fs.writeFileSync(file, next)
  console.log(`${was ? 'updated' : 'added'} ${path.relative(process.cwd(), file)}${was ? '' : ' (list it in src/activityStories/drafts.ts)'}`)
}
