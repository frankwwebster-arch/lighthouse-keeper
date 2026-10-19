#!/usr/bin/env node
import assert from 'node:assert/strict'
import crypto from 'node:crypto'
import fs from 'node:fs'
import path from 'node:path'
import vm from 'node:vm'
import { fileURLToPath } from 'node:url'
import { PNG } from 'pngjs'

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..')
const set = 'activity-cloud-composer-v3'
const draft = 'art/drafts/activity-cloud-composer-2026-10-19-v3'
const abs = value => path.join(root, value)
const json = value => JSON.parse(fs.readFileSync(abs(value), 'utf8'))
const sha = value => crypto.createHash('sha256').update(fs.readFileSync(abs(value))).digest('hex')
const register = json(`${draft}/batch-register.json`)
const catalogue = json(`public/keeper-review/${set}/catalogue.json`)
const v2 = json('public/keeper-review/activity-cloud-composer-v2/catalogue.json')
const v2Register = json('art/drafts/activity-cloud-composer-2026-10-19-v2/batch-register.json')
const page = fs.readFileSync(abs(`public/keeper-review/${set}/index.html`), 'utf8')

const albumNames = [
  'music-album-sgt-pepper-homage',
  'music-album-morning-glory-homage',
  'music-album-screamadelica-homage',
  'music-album-velvet-banana-homage',
  'music-album-london-calling-homage',
  'music-album-dark-side-homage',
  'music-album-abbey-road-homage',
  'music-album-tapestry-homage',
  'music-album-sticky-fingers-homage',
  'music-album-never-mind-bollocks-homage',
  'music-album-born-usa-homage',
  'music-album-nevermind-homage',
]

assert.equal(register.schema, 'lighthouse-keeper/activity-cloud-composer-register@3')
assert.equal(catalogue.schema, 'lighthouse-keeper/activity-cloud-composer@1')
assert.equal(catalogue.set, set)
assert.equal(catalogue.status, 'immutable-reversible-review-tool-not-approved')
assert.equal(register.sourceVocabulary.catalogueSha256, sha(register.sourceVocabulary.catalogue))
assert.equal(register.sourceVocabulary.registerSha256, sha(register.sourceVocabulary.register))
assert.equal(register.sourceVocabulary.inheritedComponents, 74)
assert.equal(sha(v2Register.page.file), v2Register.page.sha256, 'immutable Composer V2 page changed')

assert.deepEqual(catalogue.body, v2.body, 'V3 changed inherited Prime body')
assert.deepEqual(catalogue.route, v2.route, 'V3 changed inherited Prime route')
assert.deepEqual(catalogue.reviewReferences, v2.reviewReferences)
assert.deepEqual(catalogue.defaultRecipe, v2.defaultRecipe)
assert.deepEqual({...catalogue.composer, localStorageKey: v2.composer.localStorageKey}, v2.composer)
for (const [name, component] of Object.entries(v2.components)) {
  assert.deepEqual(catalogue.components[name], component, `V3 changed inherited component: ${name}`)
}

assert.equal(Object.keys(v2.components).length, 74)
assert.equal(Object.keys(catalogue.components).length, 86)
assert.deepEqual(Object.keys(register.newComponents), albumNames)
assert.deepEqual(Object.keys(register.generatedSources), albumNames)

const edgeAlpha = png => {
  let count = 0
  for (let x = 0; x < png.width; x++) count += png.data[x * 4 + 3] > 8 || png.data[((png.height - 1) * png.width + x) * 4 + 3] > 8
  for (let y = 0; y < png.height; y++) count += png.data[(y * png.width) * 4 + 3] > 8 || png.data[(y * png.width + png.width - 1) * 4 + 3] > 8
  return count
}
const transparentGutter = png => {
  let minX = png.width, minY = png.height, maxX = -1, maxY = -1
  for (let y = 0; y < png.height; y++) for (let x = 0; x < png.width; x++) if (png.data[(y * png.width + x) * 4 + 3] > 8) {
    minX = Math.min(minX, x); minY = Math.min(minY, y); maxX = Math.max(maxX, x); maxY = Math.max(maxY, y)
  }
  return Math.min(minX, minY, png.width - 1 - maxX, png.height - 1 - maxY)
}

for (const name of albumNames) {
  const sourceRecord = register.generatedSources[name]
  assert.equal(sourceRecord.sha256, sha(sourceRecord.file))
  const source = PNG.sync.read(fs.readFileSync(abs(sourceRecord.file)))
  assert.equal(edgeAlpha(source), 0, `generated source touches outer edge: ${name}`)

  const record = register.newComponents[name]
  const component = catalogue.components[name]
  assert.equal(record.sha256, sha(record.file))
  assert.equal(record.family, 'music')
  assert.equal(record.ownership.ownerCount, 1)
  assert.equal(record.ownership.ambiguousPixels, 0)
  assert.equal(record.ownership.unownedVisiblePixels, 0)
  assert.equal(component.sha256, record.sha256)
  assert.equal(component.family, 'music')
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

for (const token of ['Activity Cloud Composer V3', '← Immutable Composer V2', 'V2 exact + 12 album homages', "const SET='activity-cloud-composer-v3'", "STORAGE='lighthouse-keeper.activity-cloud-composer-v3'", 'Promise.all', 'img.decode']) {
  assert.ok(page.includes(token), `V3 page missing ${token}`)
}
const scripts = [...page.matchAll(/<script>([\s\S]*?)<\/script>/g)].map(match => match[1])
assert.equal(scripts.length, 1)
new vm.Script(scripts[0])
for (const [name, value] of Object.entries(register.checks)) assert.equal(value, ['runtimeChanged', 'kitchenChanged', 'deployed'].includes(name) ? false : true, `${name} failed`)
for (const value of Object.values(register.approvalBoundary)) assert.equal(value, false)

console.log('Activity Cloud Composer V3 verified: Composer V2 and Prime authorities unchanged; 12 owned, gutter-safe album homages added; no promotion.')
