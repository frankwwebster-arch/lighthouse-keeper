#!/usr/bin/env node
import assert from 'node:assert/strict'
import crypto from 'node:crypto'
import fs from 'node:fs'
import path from 'node:path'
import vm from 'node:vm'
import { fileURLToPath } from 'node:url'
import { PNG } from 'pngjs'

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..')
const sha256 = bytes => crypto.createHash('sha256').update(bytes).digest('hex')
const route = 'kitchen-cabinetry-room-layout-v1'
const draftRoot = 'art/drafts/kitchen-cabinetry-room-layout-2026-10-22-v1'
const sourcePath = 'art/source/kitchen-cabinetry-foundation-2026-10-22-v1/cabinetry-module-construction-sheet-approved.png'
const sourceHash = '898c212690c2db8a52a6c8ea7bd962afcf12c1df8e577dcc98c4508359cccee3'
const stateSourcePath = 'art/drafts/kitchen-cabinetry-state-derivatives-2026-10-22-v1/candidate-v4-red-fault-lights-fridge-leak.png'
const stateSourceHash = 'd53b7565558acf6dc5544dde8b415fe50ac9eec1683eb374d996114ad5a902e8'

assert.equal(sha256(fs.readFileSync(path.join(root, sourcePath))), sourceHash, 'approved cabinetry authority changed')
assert.equal(sha256(fs.readFileSync(path.join(root, stateSourcePath))), stateSourceHash, 'approved state visual authority changed')
const manifestBytes = fs.readFileSync(path.join(root, draftRoot, 'manifest.json'))
assert.deepEqual(manifestBytes, fs.readFileSync(path.join(root, `public/keeper-review/${route}/manifest.json`)), 'public and draft manifests differ')
const manifest = JSON.parse(manifestBytes)
assert.equal(manifest.status, 'unapproved-room-layout-review')
assert.deepEqual(manifest.room.logicalPixels, [772, 224])
assert.equal(manifest.room.bayWidth, 84)
assert.deepEqual(manifest.room.bodySize, [84, 74])
assert.deepEqual(manifest.room.originsX, [84, 168, 252, 336, 420, 504])
assert.equal(manifest.boundaries.productionChanged, false)
assert.equal(manifest.boundaries.runtimeChanged, false)
assert.equal(manifest.boundaries.approvedSourceOverwritten, false)
assert.equal(manifest.boundaries.healingApproved, false)
assert.equal(manifest.stateSource.sha256, stateSourceHash)
assert.deepEqual(manifest.states.sink, { off: 'sink', on: 'sink-on', broken: 'sink-broken' })
assert.equal(manifest.states.dishwasher.offUnavailable, 'dark-lamp production extraction is not yet authored')
const archive = JSON.parse(fs.readFileSync(path.join(root, `review-archive/sets/${route}.json`), 'utf8'))

for (const [name, record] of Object.entries(manifest.assets)) {
  const draft = fs.readFileSync(path.join(root, draftRoot, 'assets', record.file))
  assert.equal(sha256(draft), record.sha256, `${name} hash changed`)
  const url = `/keeper-review/${route}/assets/${record.file}`
  const archived = archive.entries[url]
  assert(archived, `${name} missing from content-addressed review set`)
  assert.equal(archived.sha256, record.sha256, `${name} archive hash differs`)
  assert.deepEqual(draft, fs.readFileSync(path.join(root, archived.object)), `${name} archive object differs from reversible draft`)
  const png = PNG.sync.read(draft)
  assert.deepEqual([png.width, png.height], record.pixels, `${name} dimensions changed`)
  assert.deepEqual(record.logicalBody, [84, 74], `${name} logical body changed`)
  let minX = png.width, minY = png.height, maxX = -1, maxY = -1
  for (let y = 0; y < png.height; y++) for (let x = 0; x < png.width; x++) {
    if (png.data[(y * png.width + x) * 4 + 3] === 0) continue
    minX = Math.min(minX, x); minY = Math.min(minY, y); maxX = Math.max(maxX, x); maxY = Math.max(maxY, y)
  }
  assert(maxX >= 0, `${name} crop is empty`)
  assert(Math.min(minX, minY, png.width - 1 - maxX, png.height - 1 - maxY) >= 4, `${name} lacks a four-pixel transparent safety gutter`)
}

const page = fs.readFileSync(path.join(root, `public/keeper-review/${route}/index.html`), 'utf8')
assert.match(page, /UNAPPROVED ROOM-LAYOUT REVIEW V1/)
assert.match(page, /Raw approved modules/)
assert.match(page, /Join-only diagnostic/)
assert.match(page, /localStorage/)
assert.match(page, /Promise\.all\(Object\.keys\(manifest\.assets\)\.map\(loadImage\)\)/, 'all unique crops must decode before movement unlocks')
assert.match(page, /84 × 74/)
assert.match(page, /Broken units retain the existing movement lock until repaired/)
const inlineScript = page.match(/<script>([\s\S]+)<\/script>/)?.[1]
assert(inlineScript, 'room workbench script missing')
new vm.Script(inlineScript, { filename: `${route}/inline.js` })

const config = fs.readFileSync(path.join(root, 'next.config.mjs'), 'utf8')
assert.match(config, /source: '\/keeper-review\/kitchen-cabinetry-room-layout-v1',[\s\S]*?destination: '\/keeper-review\/kitchen-cabinetry-room-layout-v1\/index\.html'/)

console.log('Kitchen Cabinetry Room Layout V1 verified: fourteen isolated approved-source crops, fixed 84x74 geometry, synchronized raw/healing comparison, persistent state-aware bay swapping and closed runtime gate.')
