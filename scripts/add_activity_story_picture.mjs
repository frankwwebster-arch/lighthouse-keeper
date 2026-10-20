#!/usr/bin/env node
/**
 * Add a picture, or a new version of one, to the bubble-story library.
 * Every story that uses the picture switches to the new version at once;
 * older versions are kept, so Frank can pin one back in the studio.
 *
 *   node scripts/add_activity_story_picture.mjs <id> <file.png> --note "why"
 *     [--kind object|mark] [--family bbq] [--label "Barbecue grill"] [--by codex]
 *   node scripts/add_activity_story_picture.mjs <id> --current <version>   (roll the library back)
 *
 * The PNG must be a 256 × 256 transparent cell with at least 16 px of clear
 * gutter on every side (docs/ACTIVITY_CALLOUT_AUTHORING_STANDARD.md). A file
 * inside an immutable art/drafts/ pack is referenced where it is (push the
 * pack to main so the live site can fetch it). Any other file is copied to
 * public/activity-stories/pictures/ under a name that includes its hash, so a
 * version can never be overwritten.
 */

import fs from 'node:fs'
import path from 'node:path'
import { CELL, ID, MIN_GUTTER, PUBLIC_DIR, REPO_PREFIX, ROOT, measure, readLibrary, sha256, writeLibrary } from './activity_story_pictures.mjs'

const args = process.argv.slice(2)
const flag = (name) => {
  const i = args.indexOf(`--${name}`)
  return i >= 0 ? args[i + 1] : undefined
}
const [id, file] = args
const fail = (msg) => {
  console.error(`✗ ${msg}`)
  process.exit(1)
}
if (!id || !ID.test(id)) fail('give a picture id in lower-case-kebab, e.g. bbq-grill or symbol-heat-shimmer')

const lib = readLibrary()
const existing = lib.pictures[id]

if (flag('current')) {
  const v = Number(flag('current'))
  if (!existing?.versions.some((x) => x.v === v)) fail(`${id} has no version ${v}`)
  existing.current = v
  writeLibrary(lib)
  console.log(`✓ ${id}: stories now use version ${v}`)
  process.exit(0)
}

if (!file || file.startsWith('--') || !fs.existsSync(file)) fail('give the PNG file to add')
const buf = fs.readFileSync(file)
const { cell, bounds, gutter } = measure(buf)
if (cell[0] !== CELL || cell[1] !== CELL) fail(`the cell must be ${CELL} × ${CELL}; this one is ${cell.join(' × ')}`)
if (!bounds) fail('the picture is empty')
if (gutter < MIN_GUTTER) fail(`only ${gutter} px of clear gutter; at least ${MIN_GUTTER} px is needed on every side`)
const note = flag('note')
if (!note) fail('say what changed with --note "…"')

const hash = sha256(buf)
if (existing?.versions.some((v) => v.sha256 === hash)) fail(`${id} already has this exact picture`)
const v = existing ? Math.max(...existing.versions.map((x) => x.v)) + 1 : 1
const inRepo = path.relative(ROOT, path.resolve(file))
let url
if (/^art\/drafts\//.test(inRepo) && !inRepo.includes('..')) url = REPO_PREFIX + inRepo
else {
  const name = `${id}-v${v}-${hash.slice(0, 12)}.png`
  fs.mkdirSync(PUBLIC_DIR, { recursive: true })
  fs.copyFileSync(file, path.join(PUBLIC_DIR, name))
  url = `/activity-stories/pictures/${name}`
}

const version = { v, url, sha256: hash, cell, bounds, added: new Date().toISOString().slice(0, 10), source: path.basename(file), by: flag('by') ?? 'codex', note }
if (existing) {
  existing.versions.push(version)
  existing.current = v
  if (existing.review?.status === 'rework-requested') existing.review = { status: 'approved', note: `Replaced by v${v}; awaiting Frank's look.` }
  if (existing.review?.status === 'approved' && existing.review.note.startsWith('Replaced')) existing.review.note = `Replaced by v${v}; awaiting Frank's look.`
} else {
  const kind = flag('kind')
  if (kind !== 'object' && kind !== 'mark') fail('a new picture needs --kind object or --kind mark')
  lib.pictures[id] = { kind, family: flag('family') ?? id.split('-')[0], label: flag('label') ?? id, current: v, versions: [version] }
  lib.pictures = Object.fromEntries(Object.entries(lib.pictures).sort(([a], [b]) => a.localeCompare(b)))
}
writeLibrary(lib)
console.log(`✓ ${id} v${v} added and now current (${bounds.join(', ')}; gutter ${gutter} px). Run npm run verify:activity-stories.`)
