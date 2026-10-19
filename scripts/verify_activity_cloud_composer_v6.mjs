#!/usr/bin/env node
import assert from 'node:assert/strict'
import crypto from 'node:crypto'
import fs from 'node:fs'
import path from 'node:path'
import vm from 'node:vm'
import { fileURLToPath } from 'node:url'
import { PNG } from 'pngjs'

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..')
const set = 'activity-cloud-composer-v6'
const draft = 'art/drafts/activity-cloud-composer-2026-10-20-v6'
const abs = value => path.join(root, value)
const json = value => JSON.parse(fs.readFileSync(abs(value), 'utf8'))
const sha = value => crypto.createHash('sha256').update(fs.readFileSync(abs(value))).digest('hex')
const register = json(`${draft}/batch-register.json`)
const catalogue = json(`public/keeper-review/${set}/catalogue.json`)
const v5 = json('public/keeper-review/activity-cloud-composer-v5/catalogue.json')
const v5Register = json('art/drafts/activity-cloud-composer-2026-10-19-v5/batch-register.json')
const archive = json('review-archive/index.json')
const page = fs.readFileSync(abs(`public/keeper-review/${set}/index.html`), 'utf8')
const newNames = Object.keys(register.newComponents)

assert.equal(register.schema, 'lighthouse-keeper/activity-cloud-composer-register@6')
assert.equal(catalogue.schema, 'lighthouse-keeper/activity-cloud-composer@1')
assert.equal(catalogue.set, set)
assert.equal(catalogue.status, 'immutable-reversible-review-tool-not-approved')
assert.equal(sha(v5Register.page.file), v5Register.page.sha256, 'immutable Composer V5 page changed')
assert.equal(register.sourceVocabulary.catalogueSha256, sha(register.sourceVocabulary.catalogue))
assert.equal(register.sourceVocabulary.registerSha256, sha(register.sourceVocabulary.register))
assert.equal(register.sourceVocabulary.inheritedComponents, 146)

assert.deepEqual(catalogue.body, v5.body, 'V6 changed inherited Prime body')
assert.deepEqual(catalogue.route, v5.route, 'V6 changed inherited Prime route')
assert.deepEqual(catalogue.reviewReferences, v5.reviewReferences)
assert.deepEqual(catalogue.defaultRecipe, v5.defaultRecipe)
assert.deepEqual(catalogue.notationAccents, v5.notationAccents)
assert.deepEqual({...catalogue.composer, localStorageKey: v5.composer.localStorageKey}, v5.composer)
for (const [name, item] of Object.entries(v5.components)) assert.deepEqual(catalogue.components[name], item, `V6 changed inherited component ${name}`)
assert.equal(Object.keys(catalogue.components).length, 149)
assert.deepEqual(newNames, ['bathroom-flush-handle', 'bathroom-loo-brush', 'bathroom-bad-smell'])
assert.equal(register.generatedSources.length, 3)
assert.equal(Object.keys(catalogue.suggestedRecipes).length, 15)
for (const [key, recipe] of Object.entries(v5.suggestedRecipes)) {
  if (key === 'using-loo') continue
  assert.deepEqual(catalogue.suggestedRecipes[key], recipe, `V6 changed unrelated suggestion ${key}`)
}
assert.deepEqual(catalogue.suggestedRecipes['using-loo'].elements, [
  'bathroom-toilet', 'bathroom-toilet-roll', 'bathroom-flush-handle', 'bathroom-loo-brush', 'bathroom-bad-smell',
])

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

for (const source of register.generatedSources) {
  assert.equal(source.sha256, sha(source.file))
  const png = PNG.sync.read(fs.readFileSync(abs(source.file)))
  assert.equal(edgeAlpha(png), 0, `${source.file} touches outer edge`)
  assert.ok(source.visibleBounds.length === 4)
  assert.ok(newNames.includes(source.owner))
}

for (const name of newNames) {
  const record = register.newComponents[name]
  const component = catalogue.components[name]
  assert.equal(record.sha256, sha(record.file))
  assert.equal(component.sha256, record.sha256)
  assert.equal(component.sourceSet, set)
  assert.equal(component.family, 'bathroom')
  assert.equal(record.ownership.ownerCount, 1)
  assert.equal(record.ownership.ambiguousPixels, 0)
  assert.equal(record.ownership.unownedVisiblePixels, 0)
  assert.equal(record.edgeAlphaPixels, 0)
  assert.ok(record.transparentGutterPx >= 16)
  const png = PNG.sync.read(fs.readFileSync(abs(record.file)))
  assert.deepEqual([png.width, png.height], [256, 256])
  assert.equal(edgeAlpha(png), 0)
  assert.ok(transparentGutter(png) >= 16)
  const archived = archive.legacyPaths[component.src]
  if (archived) assert.equal(archived.sha256, component.sha256, `${name} archive hash mismatch`)
}

assert.equal(register.checks.primeBodyUnchanged, true)
assert.equal(register.checks.runtimeChanged, false)
assert.equal(register.checks.kitchenChanged, false)
assert.equal(register.checks.deployed, false)
assert.match(page, /Activity Cloud Composer V6/)
assert.match(page, /Immutable Composer V5/)
assert.match(page, /Start from a suggested package/)
assert.match(page, /showNotation/)
assert.match(page, /Promise\.all\(\[\.\.\.new Set/)
assert.match(page, /img\.decode/)
assert.match(page, /contextBakedIntoKeeper:false/)
const scripts = [...page.matchAll(/<script>([\s\S]*?)<\/script>/g)]
assert.equal(scripts.length, 1)
new vm.Script(scripts[0][1])

assert.equal(sha(register.catalogue.file), register.catalogue.sha256)
assert.equal(sha(register.page.file), register.page.sha256)
console.log(JSON.stringify({set, inheritedComponents: 146, newComponents: 3, components: 149, sources: 3, suggestedRecipes: 15, looPackageElements: 5, ownership: 'one-owner-zero-ambiguous', gutters: '>=16px', primeBody: 'unchanged', runtimeChanged: false, kitchenChanged: false, deployed: false}, null, 2))
