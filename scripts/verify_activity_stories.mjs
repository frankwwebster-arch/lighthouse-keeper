#!/usr/bin/env node
/**
 * Checks the bubble-story library and drafts (data/activity-stories/):
 * every picture version exists, matches its SHA-256 and measured bounds,
 * is a clean 256 × 256 cell, and every story names only known pictures.
 * Motion rules are checked by src/activityStories/compile.test.ts.
 *
 *   npm run verify:activity-stories
 */

import fs from 'node:fs'
import path from 'node:path'
import { CELL, ID, MIN_GUTTER, ROOT, STORIES_DIR, fileFor, measure, readLibrary, sha256 } from './activity_story_pictures.mjs'
import { completePictureCatalogue } from './import_activity_story_picture_catalogue.mjs'
import { verifyCodexBubbleStoryFamiliesV1 } from './verify_codex_bubble_story_families_v1.mjs'
import { verifyActivityStoryLigneClaireBbqPilotV1 } from './verify_activity_story_ligne_claire_bbq_pilot_v1.mjs'
import { verifyActivityStorySymbolColourSemanticsV1 } from './verify_activity_story_symbol_colour_semantics_v1.mjs'

const problems = []
problems.push(...verifyCodexBubbleStoryFamiliesV1())
problems.push(...verifyActivityStoryLigneClaireBbqPilotV1())
problems.push(...verifyActivityStorySymbolColourSemanticsV1())
const lib = readLibrary()
if (lib.schema !== 'lighthouse-keeper/activity-picture-library@1') problems.push('pictures.json: wrong schema')

for (const f of lib.keeper.rearWork) {
  const file = fileFor(f.url)
  if (!file || !fs.existsSync(file)) problems.push(`keeper frame missing: ${f.url}`)
  else if (sha256(fs.readFileSync(file)) !== f.sha256) problems.push(`keeper frame changed: ${f.url}`)
}
if (lib.keeper.rearWork.length !== 24) problems.push(`the keeper's rear-work loop should be 24 frames, not ${lib.keeper.rearWork.length}`)

let versions = 0
for (const [id, p] of Object.entries(lib.pictures)) {
  if (!ID.test(id)) problems.push(`${id}: ids are lower-case-kebab`)
  if (p.kind !== 'object' && p.kind !== 'mark') problems.push(`${id}: kind must be object or mark`)
  if (!p.versions?.some((v) => v.v === p.current)) problems.push(`${id}: current version ${p.current} isn't listed`)
  const seen = new Set()
  for (const v of p.versions ?? []) {
    versions++
    if (seen.has(v.v)) problems.push(`${id}: version ${v.v} is listed twice`)
    seen.add(v.v)
    const file = fileFor(v.url)
    if (!file || !fs.existsSync(file)) {
      problems.push(`${id} v${v.v}: no file for ${v.url}`)
      continue
    }
    const buf = fs.readFileSync(file)
    if (sha256(buf) !== v.sha256) problems.push(`${id} v${v.v}: the file doesn't match its SHA-256 (files are never edited in place; add a new version)`)
    const m = measure(buf)
    if (m.cell[0] !== CELL || m.cell[1] !== CELL) problems.push(`${id} v${v.v}: cell is ${m.cell.join(' × ')}, not ${CELL} × ${CELL}`)
    if (!m.bounds || m.bounds.join() !== v.bounds.join()) problems.push(`${id} v${v.v}: bounds are ${m.bounds?.join(', ')}, the library says ${v.bounds.join(', ')}`)
    if (m.gutter < MIN_GUTTER) problems.push(`${id} v${v.v}: only ${m.gutter} px of clear gutter`)
  }
}

// Claude and Frank need the complete review-ready activity vocabulary, not
// only the small choreography subset that originally seeded this library.
// The closure record supplies the few historical versions that predate a
// machine-readable registered pack, so all 452 versions present when Frank
// paused the programme remain protected as a minimum, while later additions
// can still extend the catalogue.
const closure = JSON.parse(fs.readFileSync(path.join(ROOT, 'data/activity-stories/catalogue-closure-2026-10-22.json'), 'utf8'))
const expected = new Map()
for (const source of completePictureCatalogue()) expected.set(`${source.id}@${source.sha256}`, source)
for (const source of closure.unmanifestedLegacyVersions ?? []) expected.set(`${source.id}@${source.sha256}`, source)
for (const source of expected.values()) {
  const picture = lib.pictures[source.id]
  const provenance = source.set ?? 'catalogue closure'
  if (!picture) problems.push(`${source.id}: missing from the complete activity picture catalogue (${provenance})`)
  else if (!picture.versions.some((version) => version.sha256 === source.sha256 && (source.v === undefined || version.v === source.v) && (source.url === undefined || version.url === source.url)))
    problems.push(`${source.id}: ${provenance} source version is missing from the library`)
}
if (expected.size !== closure.minimumVersions)
  problems.push(`catalogue closure describes ${expected.size} unique versions, expected ${closure.minimumVersions}`)
if (new Set([...expected.values()].map((source) => source.id)).size !== closure.minimumPictures)
  problems.push(`catalogue closure does not cover all ${closure.minimumPictures} picture ids`)
if (Object.keys(lib.pictures).length < closure.minimumPictures)
  problems.push(`picture library has fallen below the ${closure.minimumPictures}-picture closure`)
if (versions < closure.minimumVersions)
  problems.push(`picture library has fallen below the ${closure.minimumVersions}-version closure`)

const stories = fs.readdirSync(STORIES_DIR).filter((f) => f.endsWith('.json'))
for (const f of stories) {
  const s = JSON.parse(fs.readFileSync(path.join(STORIES_DIR, f), 'utf8'))
  if (s.schema !== 'lighthouse-keeper/activity-story@1') problems.push(`${f}: wrong schema`)
  if (`${s.id}.json` !== f) problems.push(`${f}: id ${s.id} should match the file name`)
  for (const [as, m] of Object.entries(s.cast ?? {})) if (!lib.pictures[m.picture]) problems.push(`${f}: ${as} uses ${m.picture}, which isn't in the library`)
  for (const [as, m] of Object.entries(s.cast ?? {})) if (m.appear && lib.pictures[m.appear]?.kind !== 'mark') problems.push(`${f}: ${as} bursts ${m.appear} as it appears, which isn't a mark in the library`)
  for (const st of s.steps ?? []) if (st.mark && lib.pictures[st.mark]?.kind !== 'mark') problems.push(`${f}: mark ${st.mark} isn't a mark in the library`)
  for (const a of s.ambient ?? []) if (lib.pictures[a.picture]?.kind !== 'mark') problems.push(`${f}: extra mark ${a.picture} isn't a mark in the library`)
  for (const pr of s.props ?? []) if (lib.pictures[pr.picture]?.kind !== 'object') problems.push(`${f}: prop ${pr.picture} isn't a picture in the library`)
}

if (problems.length) {
  console.error(`✗ bubble stories: ${problems.length} problem(s)\n  ${problems.join('\n  ')}`)
  process.exit(1)
}
console.log(`✓ bubble stories: ${Object.keys(lib.pictures).length} pictures (${versions} versions), 24 keeper frames and ${stories.length} stories check out`)
