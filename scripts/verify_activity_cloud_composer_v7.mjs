#!/usr/bin/env node
import assert from 'node:assert/strict'
import crypto from 'node:crypto'
import fs from 'node:fs'
import path from 'node:path'
import vm from 'node:vm'
import { fileURLToPath } from 'node:url'
import { PNG } from 'pngjs'

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..')
const set = 'activity-cloud-composer-v7'
const draft = 'art/drafts/activity-cloud-composer-2026-10-20-v7'
const abs = value => path.join(root, value)
const json = value => JSON.parse(fs.readFileSync(abs(value), 'utf8'))
const sha = value => crypto.createHash('sha256').update(fs.readFileSync(abs(value))).digest('hex')
const register = json(`${draft}/batch-register.json`)
const catalogue = json(`public/keeper-review/${set}/catalogue.json`)
const v6 = json('public/keeper-review/activity-cloud-composer-v6/catalogue.json')
const v6Register = json('art/drafts/activity-cloud-composer-2026-10-20-v6/batch-register.json')
const archive = json('review-archive/index.json')
const page = fs.readFileSync(abs(`public/keeper-review/${set}/index.html`), 'utf8')
const expectedNames = [
  'symbol-heat-shimmer',
  'symbol-pleasant-aroma',
  'symbol-foul-odour',
  'symbol-electrical-arc',
  'symbol-welding-sparks',
  'symbol-exclamation-mark',
  'symbol-question-mark',
]
const expectedFamilies = {
  'symbol-heat-shimmer': 'heat',
  'symbol-pleasant-aroma': 'scent',
  'symbol-foul-odour': 'scent',
  'symbol-electrical-arc': 'electrical',
  'symbol-welding-sparks': 'welding',
  'symbol-exclamation-mark': 'notation',
  'symbol-question-mark': 'notation',
}

const edgeAlpha = png => {
  let count = 0
  for (let x = 0; x < png.width; x++) count += Number(png.data[x * 4 + 3] > 8) + Number(png.data[((png.height - 1) * png.width + x) * 4 + 3] > 8)
  for (let y = 0; y < png.height; y++) count += Number(png.data[(y * png.width) * 4 + 3] > 8) + Number(png.data[(y * png.width + png.width - 1) * 4 + 3] > 8)
  return count
}
const bounds = png => {
  let minX = png.width, minY = png.height, maxX = -1, maxY = -1
  for (let y = 0; y < png.height; y++) for (let x = 0; x < png.width; x++) if (png.data[(y * png.width + x) * 4 + 3] > 8) {
    minX = Math.min(minX, x); minY = Math.min(minY, y); maxX = Math.max(maxX, x); maxY = Math.max(maxY, y)
  }
  assert.ok(maxX >= 0, 'PNG has no visible alpha')
  return [minX, minY, maxX + 1, maxY + 1]
}
const transparentGutter = png => {
  const [minX, minY, maxX, maxY] = bounds(png)
  return Math.min(minX, minY, png.width - maxX, png.height - maxY)
}

assert.equal(register.schema, 'lighthouse-keeper/activity-cloud-composer-register@7')
assert.equal(catalogue.schema, 'lighthouse-keeper/activity-cloud-composer@1')
assert.equal(catalogue.set, set)
assert.equal(catalogue.status, 'immutable-reversible-review-tool-not-approved')
assert.equal(sha(v6Register.page.file), v6Register.page.sha256, 'immutable Composer V6 page changed')
assert.equal(register.sourceVocabulary.catalogueSha256, sha(register.sourceVocabulary.catalogue))
assert.equal(register.sourceVocabulary.registerSha256, sha(register.sourceVocabulary.register))
assert.equal(register.sourceVocabulary.inheritedComponents, 149)

assert.deepEqual(catalogue.body, v6.body, 'V7 changed inherited Prime body')
assert.deepEqual(catalogue.route, v6.route, 'V7 changed inherited Prime route')
assert.deepEqual(catalogue.reviewReferences, v6.reviewReferences)
assert.deepEqual(catalogue.defaultRecipe, v6.defaultRecipe)
assert.deepEqual(catalogue.notationAccents, v6.notationAccents)
assert.deepEqual(catalogue.suggestedRecipes, v6.suggestedRecipes)
assert.deepEqual({...catalogue.composer, localStorageKey: v6.composer.localStorageKey}, v6.composer)
for (const [name, item] of Object.entries(v6.components)) assert.deepEqual(catalogue.components[name], item, `V7 changed inherited component ${name}`)
assert.equal(Object.keys(catalogue.components).length, 156)
assert.deepEqual(Object.keys(register.newComponents), expectedNames)

const sheetSource = register.generatedSources[0]
assert.deepEqual(sheetSource.layout, [3, 2])
assert.deepEqual(sheetSource.cellPixels, [512, 512])
assert.equal(sheetSource.sha256, sha(sheetSource.file))
assert.equal(sheetSource.boundaryAlphaPixels, 0)
assert.equal(sheetSource.cells.length, 6)
const sheet = PNG.sync.read(fs.readFileSync(abs(sheetSource.file)))
assert.deepEqual([sheet.width, sheet.height], [1536, 1024])
for (const x of [0, 511, 512, 1023, 1024, 1535]) for (let y = 0; y < sheet.height; y++) assert.ok(sheet.data[(y * sheet.width + x) * 4 + 3] <= 8, `source sheet alpha at x=${x}`)
for (const y of [0, 511, 512, 1023]) for (let x = 0; x < sheet.width; x++) assert.ok(sheet.data[(y * sheet.width + x) * 4 + 3] <= 8, `source sheet alpha at y=${y}`)
for (const cell of sheetSource.cells) {
  assert.ok(expectedNames.includes(cell.owner))
  assert.ok(cell.gutterPx >= 80)
  assert.equal(cell.ambiguousPixels, 0)
  assert.equal(cell.unownedVisiblePixels, 0)
}

const questionSource = register.generatedSources[1]
assert.equal(questionSource.sha256, sha(questionSource.file))
const question = PNG.sync.read(fs.readFileSync(abs(questionSource.file)))
assert.equal(edgeAlpha(question), 0)
assert.equal(questionSource.owner, 'symbol-question-mark')

for (const name of expectedNames) {
  const record = register.newComponents[name]
  const component = catalogue.components[name]
  assert.equal(record.sha256, sha(record.file))
  assert.equal(component.sha256, record.sha256)
  assert.equal(component.sourceSet, set)
  assert.equal(component.family, expectedFamilies[name])
  assert.equal(record.ownership.ownerCount, 1)
  assert.equal(record.ownership.ambiguousPixels, 0)
  assert.equal(record.ownership.unownedVisiblePixels, 0)
  assert.equal(record.edgeAlphaPixels, 0)
  assert.ok(record.transparentGutterPx >= 20)
  const png = PNG.sync.read(fs.readFileSync(abs(record.file)))
  assert.deepEqual([png.width, png.height], [256, 256])
  assert.equal(edgeAlpha(png), 0)
  assert.ok(transparentGutter(png) >= 20)
  const archived = archive.legacyPaths[component.src]
  assert.ok(archived, `${name} missing review-archive mapping`)
  assert.equal(archived.sha256, component.sha256, `${name} archive hash mismatch`)
}

assert.equal(register.checks.sourceEdgesClear, true)
assert.equal(register.checks.sourceCellGuttersAtLeast80, true)
assert.equal(register.checks.componentGuttersAtLeast20, true)
assert.equal(register.checks.componentOwnershipUnambiguous, true)
assert.equal(register.checks.primeBodyUnchanged, true)
assert.equal(register.checks.runtimeChanged, false)
assert.equal(register.checks.kitchenChanged, false)
assert.equal(register.checks.deployed, false)
assert.match(page, /Activity Cloud Composer V7/)
assert.match(page, /Immutable Composer V6/)
assert.match(page, /V6 exact \+ seven generic action symbols/)
assert.match(page, /Start from a suggested package/)
assert.match(page, /Promise\.all\(\[\.\.\.new Set/)
assert.match(page, /img\.decode/)
assert.match(page, /contextBakedIntoKeeper:false/)
const scripts = [...page.matchAll(/<script>([\s\S]*?)<\/script>/g)]
assert.equal(scripts.length, 1)
new vm.Script(scripts[0][1])

assert.equal(sha(register.catalogue.file), register.catalogue.sha256)
assert.equal(sha(register.page.file), register.page.sha256)
console.log(JSON.stringify({set, inheritedComponents: 149, newComponents: 7, components: 156, sourceSheetGutters: '>=80px', componentGutters: '>=20px', ownership: 'one-owner-zero-ambiguous', primeBody: 'unchanged', runtimeChanged: false, kitchenChanged: false, deployed: false}, null, 2))
