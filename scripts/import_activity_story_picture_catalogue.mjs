#!/usr/bin/env node
/**
 * Import every review-ready, isolated activity-callout component into the
 * shared Bubble stories picture library. The source PNGs stay in their
 * immutable art/drafts packs; add_activity_story_picture.mjs registers them
 * by URL and hash, validates their 256px cell/gutter contract, and preserves
 * any existing versions.
 *
 * Sources covered:
 * - Activity Cloud Composer V1-V7
 * - Prime rear-work activity callout V2 and V3
 * - every Claude picture pack with a component asset manifest
 *
 * Safe to rerun: exact id/hash pairs already in the library are skipped.
 */

import crypto from 'node:crypto'
import fs from 'node:fs'
import path from 'node:path'
import { spawnSync } from 'node:child_process'
import { fileURLToPath } from 'node:url'
import { ROOT, readLibrary } from './activity_story_pictures.mjs'

const DRAFTS = path.join(ROOT, 'art/drafts')
const ADD = path.join(ROOT, 'scripts/add_activity_story_picture.mjs')

const sha256 = (file) => crypto.createHash('sha256').update(fs.readFileSync(file)).digest('hex')
const title = (id) => id
  .split('-')
  .map((word, i) => {
    if (word === 'bbq') return 'BBQ'
    if (word === 'loo') return 'loo'
    if (word === 'sgt') return 'Sgt.'
    if (word === 'usa') return 'USA'
    return i === 0 ? word[0].toUpperCase() + word.slice(1) : word
  })
  .join(' ')

function addRecord(records, id, component, set, kind = 'object', family = component.family) {
  if (!component.file || !component.sha256) throw new Error(`${set}/${id}: incomplete component record`)
  records.push({ id, file: component.file, sha256: component.sha256, family: family ?? id.split('-')[0], kind, set })
}

export function sourceCatalogue() {
  const records = []
  const composerRegisters = fs.readdirSync(DRAFTS)
    .filter((name) => /^activity-cloud-composer-.+-v\d+$/.test(name))
    .map((name) => path.join(DRAFTS, name, 'batch-register.json'))
    .filter(fs.existsSync)
    .sort()

  for (const register of composerRegisters) {
    const batch = JSON.parse(fs.readFileSync(register, 'utf8'))
    for (const [id, component] of Object.entries(batch.newComponents ?? {}))
      addRecord(records, id, component, batch.set, id.startsWith('symbol-') ? 'mark' : 'object')
    for (const [id, component] of Object.entries(batch.newAccentComponents ?? {}))
      addRecord(records, id, component, batch.set, 'mark', component.family ?? 'music-notation')
  }

  const v2 = JSON.parse(fs.readFileSync(path.join(DRAFTS, 'keeper-prime-back-work-activity-callout-2026-10-19-v2/batch-register.json'), 'utf8'))
  for (const [id, component] of Object.entries(v2.candidate.calloutComponents))
    addRecord(records, id, component, v2.set, 'object', component.activity)

  const v3 = JSON.parse(fs.readFileSync(path.join(DRAFTS, 'keeper-prime-back-work-activity-callout-2026-10-19-v3/batch-register.json'), 'utf8'))
  for (const [id, component] of Object.entries(v3.candidate.newCalloutComponents))
    addRecord(records, id, component, v3.set)

  const claudePackManifests = fs.readdirSync(DRAFTS)
    .filter((name) => name.startsWith('claude-'))
    .map((name) => path.join(DRAFTS, name, 'asset-manifest.json'))
    .filter(fs.existsSync)
    .sort()
  for (const manifest of claudePackManifests) {
    const pack = JSON.parse(fs.readFileSync(manifest, 'utf8'))
    for (const [id, component] of Object.entries(pack.components ?? {})) {
      const family = pack.set === 'claude-bedroom-asset-pack-v1' && component.family === 'leisure'
        ? 'bedroom-leisure'
        : component.family
      addRecord(records, id, component, pack.set ?? path.basename(path.dirname(manifest)), 'object', family)
    }
  }

  const unique = new Map()
  for (const record of records) {
    const key = `${record.id}@${record.sha256}`
    if (unique.has(key)) continue
    unique.set(key, record)
    const absolute = path.join(ROOT, record.file)
    if (!fs.existsSync(absolute)) throw new Error(`${record.id}: missing ${record.file}`)
    const actual = sha256(absolute)
    if (actual !== record.sha256) throw new Error(`${record.id}: source hash changed (${actual})`)
  }
  return [...unique.values()].sort((a, b) => a.id.localeCompare(b.id) || a.sha256.localeCompare(b.sha256))
}

if (path.resolve(process.argv[1] ?? '') === fileURLToPath(import.meta.url)) {
  const records = sourceCatalogue()
  let added = 0
  let skipped = 0

  for (const record of records) {
    const library = readLibrary()
    const existing = library.pictures[record.id]
    if (existing?.versions.some((version) => version.sha256 === record.sha256)) {
      skipped++
      continue
    }
    const previousCurrent = existing?.current
    const args = [
      ADD,
      record.id,
      path.join(ROOT, record.file),
      '--kind', record.kind,
      '--family', record.family,
      '--label', title(record.id),
      '--note', `Imported from complete review-ready ${record.set} picture catalogue`,
    ]
    const result = spawnSync(process.execPath, args, { cwd: ROOT, encoding: 'utf8' })
    if (result.status !== 0) throw new Error(`${record.id}: ${result.stderr || result.stdout}`)
    process.stdout.write(result.stdout)
    // Importing a historical alternate must not replace an already-current image.
    if (previousCurrent) {
      const restore = spawnSync(process.execPath, [ADD, record.id, '--current', String(previousCurrent)], { cwd: ROOT, encoding: 'utf8' })
      if (restore.status !== 0) throw new Error(`${record.id}: could not restore version ${previousCurrent}: ${restore.stderr || restore.stdout}`)
    }
    added++
  }

  console.log(`Activity picture catalogue complete: ${records.length} source components; ${added} added, ${skipped} already present.`)
}
