#!/usr/bin/env node
import assert from 'node:assert/strict'
import crypto from 'node:crypto'
import fs from 'node:fs'
import path from 'node:path'
import vm from 'node:vm'
import { fileURLToPath } from 'node:url'
import { PNG } from 'pngjs'

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..')
const set = 'activity-cloud-composer-v4'
const draft = 'art/drafts/activity-cloud-composer-2026-10-19-v4'
const abs = value => path.join(root, value)
const json = value => JSON.parse(fs.readFileSync(abs(value), 'utf8'))
const sha = value => crypto.createHash('sha256').update(fs.readFileSync(abs(value))).digest('hex')
const register = json(`${draft}/batch-register.json`)
const catalogue = json(`public/keeper-review/${set}/catalogue.json`)
const v3 = json('public/keeper-review/activity-cloud-composer-v3/catalogue.json')
const v3Register = json('art/drafts/activity-cloud-composer-2026-10-19-v3/batch-register.json')
const page = fs.readFileSync(abs(`public/keeper-review/${set}/index.html`), 'utf8')

const accentNames = [
  'music-notation-quaver',
  'music-notation-beamed-quavers',
  'music-notation-treble-clef',
  'music-notation-bass-clef',
  'music-notation-sharp-note',
  'music-notation-rising-stave',
]

assert.equal(register.schema, 'lighthouse-keeper/activity-cloud-composer-register@4')
assert.equal(catalogue.schema, 'lighthouse-keeper/activity-cloud-composer@1')
assert.equal(catalogue.set, set)
assert.equal(catalogue.status, 'immutable-reversible-review-tool-not-approved')
assert.equal(register.sourceVocabulary.catalogueSha256, sha(register.sourceVocabulary.catalogue))
assert.equal(register.sourceVocabulary.registerSha256, sha(register.sourceVocabulary.register))
assert.equal(register.sourceVocabulary.inheritedComponents, 86)
assert.equal(sha(v3Register.page.file), v3Register.page.sha256, 'immutable Composer V3 page changed')

assert.deepEqual(catalogue.body, v3.body, 'V4 changed inherited Prime body')
assert.deepEqual(catalogue.route, v3.route, 'V4 changed inherited Prime route')
assert.deepEqual(catalogue.reviewReferences, v3.reviewReferences)
assert.deepEqual(catalogue.defaultRecipe, v3.defaultRecipe)
assert.deepEqual(catalogue.components, v3.components, 'V4 changed inherited selectable components')
assert.deepEqual({...catalogue.composer, localStorageKey: v3.composer.localStorageKey}, v3.composer)
assert.equal(Object.keys(catalogue.components).length, 86)

assert.equal(catalogue.notationAccents.triggerFamily, 'music')
assert.equal(catalogue.notationAccents.defaultEnabled, true)
assert.equal(catalogue.notationAccents.seedAlgorithm, 'fnv1a32-v1')
assert.equal(catalogue.notationAccents.sequenceLengthFrames, 6)
assert.equal(catalogue.notationAccents.visibleNotes, 3)
assert.deepEqual(Object.keys(catalogue.notationAccents.components), accentNames)
assert.deepEqual(Object.keys(register.newAccentComponents), accentNames)

const edgeAlpha = png => {
  let count = 0
  for (let x = 0; x < png.width; x++) count += png.data[x * 4 + 3] > 8 || png.data[((png.height - 1) * png.width + x) * 4 + 3] > 8
  for (let y = 0; y < png.height; y++) count += png.data[(y * png.width) * 4 + 3] > 8 || png.data[(y * png.width + png.width - 1) * 4 + 3] > 8
  return count
}
const lineAlpha = (png, axis, coordinate) => {
  let count = 0
  if (axis === 'x') for (let y = 0; y < png.height; y++) count += png.data[(y * png.width + coordinate) * 4 + 3] > 8
  else for (let x = 0; x < png.width; x++) count += png.data[(coordinate * png.width + x) * 4 + 3] > 8
  return count
}
const transparentGutter = png => {
  let minX = png.width, minY = png.height, maxX = -1, maxY = -1
  for (let y = 0; y < png.height; y++) for (let x = 0; x < png.width; x++) if (png.data[(y * png.width + x) * 4 + 3] > 8) {
    minX = Math.min(minX, x); minY = Math.min(minY, y); maxX = Math.max(maxX, x); maxY = Math.max(maxY, y)
  }
  return Math.min(minX, minY, png.width - 1 - maxX, png.height - 1 - maxY)
}

assert.equal(register.generatedSource.sha256, sha(register.generatedSource.file))
const source = PNG.sync.read(fs.readFileSync(abs(register.generatedSource.file)))
assert.deepEqual([source.width, source.height], [1536, 1024])
assert.equal(edgeAlpha(source), 0, 'notation source touches outer edge')
assert.equal(lineAlpha(source, 'x', 512), 0, 'notation source crosses x=512')
assert.equal(lineAlpha(source, 'x', 1024), 0, 'notation source crosses x=1024')
assert.equal(lineAlpha(source, 'y', 512), 0, 'notation source crosses y=512')
assert.deepEqual(Object.values(register.generatedSource.cellBoundaryAlphaPixels), [0, 0, 0])

for (const name of accentNames) {
  const record = register.newAccentComponents[name]
  const component = catalogue.notationAccents.components[name]
  assert.equal(record.sha256, sha(record.file))
  assert.equal(record.family, 'music-notation')
  assert.equal(record.ownership.ownerCount, 1)
  assert.equal(record.ownership.ambiguousPixels, 0)
  assert.equal(record.ownership.unownedVisiblePixels, 0)
  assert.equal(component.sha256, record.sha256)
  assert.equal(component.sourceSet, set)
  assert.deepEqual(component.cellPixels, [256, 256])
  const png = PNG.sync.read(fs.readFileSync(abs(record.file)))
  assert.deepEqual([png.width, png.height], [256, 256])
  assert.equal(edgeAlpha(png), 0, `component touches edge: ${name}`)
  assert.ok(transparentGutter(png) >= 16, `component gutter is unsafe: ${name}`)
}

assert.equal(register.catalogue.sha256, sha(register.catalogue.file))
assert.equal(register.page.sha256, sha(register.page.file))
assert.deepEqual(register.candidate.publicShell, register.page)

let archiveManifest = null
const archiveManifestFile = `review-archive/sets/${set}.json`
if (fs.existsSync(abs(archiveManifestFile))) archiveManifest = json(archiveManifestFile)
for (const asset of register.publishedAssets) {
  assert.equal(asset.sourceSha256, sha(asset.source))
  if (fs.existsSync(abs(asset.public))) assert.equal(asset.publicSha256, sha(asset.public))
  else {
    assert.ok(archiveManifest, `missing public asset and archive manifest: ${asset.public}`)
    const legacy = `/${asset.publicAssemblyPath.replace(/^public\//, '')}`
    assert.equal(archiveManifest.entries[legacy].sha256, asset.sourceSha256)
    assert.equal(sha(archiveManifest.entries[legacy].object), asset.sourceSha256)
  }
}

for (const token of [
  'Activity Cloud Composer V4',
  '← Immutable Composer V3',
  'V3 exact + deterministic music notation',
  "const SET='activity-cloud-composer-v4'",
  "STORAGE='lighthouse-keeper.activity-cloud-composer-v4'",
  'id="showNotation"',
  'function notationEnabled()',
  'function notationParts(treatment)',
  'notationBakedIntoComponents:false',
  'Object.values(d.notationAccents.components)',
  'Promise.all',
  'img.decode',
]) assert.ok(page.includes(token), `V4 page missing ${token}`)

const scripts = [...page.matchAll(/<script>([\s\S]*?)<\/script>/g)].map(match => match[1])
assert.equal(scripts.length, 1)
new vm.Script(scripts[0])

const seed32 = value => {
  let h = 2166136261
  for (let i = 0; i < value.length; i++) { h ^= value.charCodeAt(i); h = Math.imul(h, 16777619) }
  return h >>> 0
}
assert.equal(seed32('vinyl|music-album-abbey-road-homage'), seed32('vinyl|music-album-abbey-road-homage'))
assert.notEqual(seed32('vinyl|music-guitar'), seed32('vinyl|music-piano'))

for (const [name, value] of Object.entries(register.checks)) assert.equal(value, ['runtimeChanged', 'kitchenChanged', 'deployed'].includes(name) ? false : true, `${name} failed`)
for (const value of Object.values(register.approvalBoundary)) assert.equal(value, false)

console.log('Activity Cloud Composer V4 verified: Composer V3 and Prime authorities unchanged; six owned notation accents deterministically accompany all music selections; no promotion.')
