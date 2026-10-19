#!/usr/bin/env node
import assert from 'node:assert/strict'
import crypto from 'node:crypto'
import fs from 'node:fs'
import path from 'node:path'
import vm from 'node:vm'
import { fileURLToPath } from 'node:url'
import { PNG } from 'pngjs'

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..')
const set = 'activity-cloud-composer-v1'
const draft = 'art/drafts/activity-cloud-composer-2026-10-19-v1'
const abs = value => path.join(root, value)
const json = value => JSON.parse(fs.readFileSync(abs(value), 'utf8'))
const sha = value => crypto.createHash('sha256').update(fs.readFileSync(abs(value))).digest('hex')
const register = json(`${draft}/batch-register.json`)
const catalogue = json(`public/keeper-review/${set}/catalogue.json`)
const v3 = json('public/keeper-review/keeper-prime-back-work-activity-callout-v3/catalogue.json')
const page = fs.readFileSync(abs(`public/keeper-review/${set}/index.html`), 'utf8')

assert.equal(register.schema, 'lighthouse-keeper/activity-cloud-composer-register@1')
assert.equal(catalogue.schema, 'lighthouse-keeper/activity-cloud-composer@1')
assert.equal(catalogue.status, 'immutable-reversible-review-tool-not-approved')
assert.equal(register.sourceVocabulary.catalogueSha256, sha(register.sourceVocabulary.catalogue))
assert.equal(register.sourceVocabulary.registerSha256, sha(register.sourceVocabulary.register))
assert.deepEqual(catalogue.body, v3.body, 'composer changed inherited Prime rear-work body')
assert.deepEqual(catalogue.route, v3.route, 'composer changed inherited route')
assert.deepEqual(catalogue.reviewReferences, v3.reviewReferences)

const inheritedNames = Object.keys(v3.callouts.components).sort()
assert.equal(inheritedNames.length, 68)
assert.equal(catalogue.sourceVocabulary.inheritedComponents, 68)
for (const name of inheritedNames) {
  const { sha256, ...inherited } = catalogue.components[name]
  assert.deepEqual(inherited, v3.callouts.components[name], `inherited component changed: ${name}`)
  assert.match(sha256, /^[a-f0-9]{64}$/)
}

const expectedNew = ['bbq-sausages', 'bbq-hotdogs', 'bbq-burgers', 'bbq-ketchup', 'bbq-charcoal']
assert.equal(Object.keys(catalogue.components).length, 73)
assert.deepEqual(Object.keys(register.newComponents), expectedNew)
assert.deepEqual(catalogue.defaultRecipe.elements, expectedNew)
assert.equal(catalogue.defaultRecipe.targetAssetId, 'outdoor.bbq')
assert.equal(catalogue.defaultRecipe.bodyCompatibility, 'rear-work-with-context')
assert.deepEqual(catalogue.composer, {
  minimumElements: 4, maximumElements: 5, frames: 42, fps: 8, quietTailFrames: 5,
  treatments: ['orbit', 'bustle'], localStorageKey: 'lighthouse-keeper.activity-cloud-composer-v1',
  exportSchema: 'lighthouse-keeper/activity-cloud-recipe@1'
})

const source = PNG.sync.read(fs.readFileSync(abs(register.generatedSource.file)))
assert.deepEqual([source.width, source.height], [1536, 1024])
const alphaAt = (x, y) => source.data[(y * source.width + x) * 4 + 3] > 8
for (const x of register.generatedSource.selectedSplitX) {
  let count = 0
  for (let y = 0; y < source.height; y++) count += alphaAt(x, y)
  assert.equal(count, 0, `alpha touches source split x=${x}`)
}
let horizontal = 0
for (let x = 0; x < source.width; x++) horizontal += alphaAt(x, register.generatedSource.selectedSplitY)
assert.equal(horizontal, 0, 'alpha touches source horizontal split')
let empty = 0
for (let y = 512; y < 1024; y++) for (let x = 1028; x < 1536; x++) empty += alphaAt(x, y)
assert.equal(empty, 0, 'declared empty sixth cell contains alpha')

const transparentGutter = png => {
  let minX = png.width, minY = png.height, maxX = -1, maxY = -1
  for (let y = 0; y < png.height; y++) for (let x = 0; x < png.width; x++) if (png.data[(y * png.width + x) * 4 + 3] > 8) {
    minX = Math.min(minX, x); minY = Math.min(minY, y); maxX = Math.max(maxX, x); maxY = Math.max(maxY, y)
  }
  return Math.min(minX, minY, png.width - 1 - maxX, png.height - 1 - maxY)
}
const edgeAlpha = png => {
  let count = 0
  for (let x = 0; x < png.width; x++) count += png.data[x * 4 + 3] > 8 || png.data[((png.height - 1) * png.width + x) * 4 + 3] > 8
  for (let y = 0; y < png.height; y++) count += png.data[(y * png.width) * 4 + 3] > 8 || png.data[(y * png.width + png.width - 1) * 4 + 3] > 8
  return count
}
for (const name of expectedNew) {
  const record = register.newComponents[name]
  assert.equal(record.sha256, sha(record.file))
  assert.equal(record.ownership.ownerCount, 1)
  assert.equal(record.ownership.ambiguousPixels, 0)
  assert.equal(record.ownership.unownedVisiblePixels, 0)
  const png = PNG.sync.read(fs.readFileSync(abs(record.file)))
  assert.deepEqual([png.width, png.height], [256, 256])
  assert.equal(edgeAlpha(png), 0, `${name} touches component edge`)
  assert.ok(transparentGutter(png) >= 16, `${name} lacks transparent gutter`)
  assert.equal(catalogue.components[name].sha256, record.sha256)
  assert.equal(catalogue.components[name].sourceSet, set)
}

assert.equal(register.catalogue.sha256, sha(register.catalogue.file))
assert.equal(register.page.sha256, sha(register.page.file))
assert.equal(register.candidate.publicShell.file, register.page.file)
assert.equal(register.candidate.publicShell.sha256, register.page.sha256)
assert.equal(register.atlas.sha256, sha(register.atlas.file))
const atlas = PNG.sync.read(fs.readFileSync(abs(register.atlas.file)))
assert.deepEqual([atlas.width, atlas.height], [1280, 256])
for (let cell = 0; cell < 5; cell++) {
  const crop = new PNG({ width: 256, height: 256 })
  PNG.bitblt(atlas, crop, cell * 256, 0, 256, 256, 0, 0)
  assert.equal(edgeAlpha(crop), 0, `atlas cell ${cell} touches edge`)
}

let archiveManifest = null
const archiveManifestFile = `review-archive/sets/${set}.json`
if (fs.existsSync(abs(archiveManifestFile))) archiveManifest = json(archiveManifestFile)
for (const asset of register.publishedAssets) {
  assert.equal(asset.sourceSha256, sha(asset.source))
  if (fs.existsSync(abs(asset.public))) assert.equal(asset.publicSha256, sha(asset.public))
  else {
    assert.ok(archiveManifest, `missing public file and archive manifest: ${asset.public}`)
    const legacy = `/${asset.publicAssemblyPath.replace(/^public\//, '')}`
    assert.equal(archiveManifest.entries[legacy].sha256, asset.sourceSha256)
    assert.equal(sha(archiveManifest.entries[legacy].object), asset.sourceSha256)
  }
}

for (const token of ['Activity Cloud Composer V1', 'Household asset label', 'Household asset ID', '4–5', 'localStorage', 'Export JSON', 'Import JSON', 'crypto.subtle', "minimumElements", "maximumElements", "dedicated-pose-required", 'generic rear-work Keeper is intentionally withheld', 'Promise.all', 'img.decode']) assert.ok(page.includes(token), `page missing ${token}`)
assert.ok(page.includes('selection=[],frame=18'), 'composer must open on the populated review frame')
assert.ok(!page.includes('contenteditable'), 'composer must not mutate source component markup')
const scripts = [...page.matchAll(/<script>([\s\S]*?)<\/script>/g)].map(match => match[1])
assert.equal(scripts.length, 1)
new vm.Script(scripts[0])
for (const [name, value] of Object.entries(register.checks)) assert.equal(value, ['runtimeChanged', 'kitchenChanged', 'deployed'].includes(name) ? false : true, `${name} failed`)
for (const value of Object.values(register.approvalBoundary)) assert.equal(value, false)

console.log('Activity Cloud Composer V1 verified: 68 inherited + 5 new isolated components, 4–5 element recipes, household-asset labels, local drafts/export, unchanged Prime and no promotion.')
