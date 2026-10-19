#!/usr/bin/env node
import assert from 'node:assert/strict'
import crypto from 'node:crypto'
import fs from 'node:fs'
import path from 'node:path'
import vm from 'node:vm'
import { fileURLToPath } from 'node:url'
import { PNG } from 'pngjs'

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..')
const set = 'activity-cloud-composer-v2'
const draft = 'art/drafts/activity-cloud-composer-2026-10-19-v2'
const abs = value => path.join(root, value)
const json = value => JSON.parse(fs.readFileSync(abs(value), 'utf8'))
const sha = value => crypto.createHash('sha256').update(fs.readFileSync(abs(value))).digest('hex')
const register = json(`${draft}/batch-register.json`)
const catalogue = json(`public/keeper-review/${set}/catalogue.json`)
const v1 = json('public/keeper-review/activity-cloud-composer-v1/catalogue.json')
const v1Register = json('art/drafts/activity-cloud-composer-2026-10-19-v1/batch-register.json')
const page = fs.readFileSync(abs(`public/keeper-review/${set}/index.html`), 'utf8')

assert.equal(register.schema, 'lighthouse-keeper/activity-cloud-composer-register@2')
assert.equal(catalogue.schema, 'lighthouse-keeper/activity-cloud-composer@1')
assert.equal(catalogue.set, set)
assert.equal(catalogue.status, 'immutable-reversible-review-tool-not-approved')
assert.equal(register.sourceVocabulary.catalogueSha256, sha(register.sourceVocabulary.catalogue))
assert.equal(register.sourceVocabulary.registerSha256, sha(register.sourceVocabulary.register))
assert.equal(register.sourceVocabulary.inheritedComponents, 73)
assert.equal(sha(v1Register.page.file), v1Register.page.sha256, 'immutable Composer V1 page changed')

assert.deepEqual(catalogue.body, v1.body, 'V2 changed inherited Prime body')
assert.deepEqual(catalogue.route, v1.route, 'V2 changed inherited Prime route')
assert.deepEqual(catalogue.reviewReferences, v1.reviewReferences)
assert.deepEqual(catalogue.defaultRecipe, v1.defaultRecipe)
assert.deepEqual({...catalogue.composer, localStorageKey: v1.composer.localStorageKey}, v1.composer)
for (const [name, component] of Object.entries(v1.components)) {
  assert.deepEqual(catalogue.components[name], component, `V2 changed inherited component: ${name}`)
}

assert.equal(Object.keys(v1.components).length, 73)
assert.equal(Object.keys(catalogue.components).length, 74)
assert.deepEqual(Object.keys(register.newComponents), ['hygiene-shampoo'])
const shampoo = catalogue.components['hygiene-shampoo']
assert.equal(shampoo.family, 'hygiene')
assert.equal(shampoo.sourceSet, set)
assert.deepEqual(shampoo.cellPixels, [256, 256])

const source = PNG.sync.read(fs.readFileSync(abs(register.generatedSource.file)))
assert.equal(register.generatedSource.sha256, sha(register.generatedSource.file))
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
assert.equal(edgeAlpha(source), 0, 'generated shampoo source touches outer edge')
const record = register.newComponents['hygiene-shampoo']
assert.equal(record.sha256, sha(record.file))
assert.equal(record.ownership.ownerCount, 1)
assert.equal(record.ownership.ambiguousPixels, 0)
assert.equal(record.ownership.unownedVisiblePixels, 0)
const component = PNG.sync.read(fs.readFileSync(abs(record.file)))
assert.deepEqual([component.width, component.height], [256, 256])
assert.equal(edgeAlpha(component), 0)
assert.ok(transparentGutter(component) >= 16)
assert.equal(shampoo.sha256, record.sha256)

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

for (const token of ['Activity Cloud Composer V2', '← Immutable Composer V1', 'V1 exact + shampoo', "const SET='activity-cloud-composer-v2'", "STORAGE='lighthouse-keeper.activity-cloud-composer-v2'", 'Promise.all', 'img.decode']) {
  assert.ok(page.includes(token), `V2 page missing ${token}`)
}
const scripts = [...page.matchAll(/<script>([\s\S]*?)<\/script>/g)].map(match => match[1])
assert.equal(scripts.length, 1)
new vm.Script(scripts[0])
for (const [name, value] of Object.entries(register.checks)) assert.equal(value, ['runtimeChanged', 'kitchenChanged', 'deployed'].includes(name) ? false : true, `${name} failed`)
for (const value of Object.values(register.approvalBoundary)) assert.equal(value, false)

console.log('Activity Cloud Composer V2 verified: Composer V1 and Prime authorities unchanged; one owned, gutter-safe shampoo token added; no promotion.')
