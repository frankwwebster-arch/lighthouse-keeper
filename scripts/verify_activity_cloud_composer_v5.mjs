#!/usr/bin/env node
import assert from 'node:assert/strict'
import crypto from 'node:crypto'
import fs from 'node:fs'
import path from 'node:path'
import vm from 'node:vm'
import { fileURLToPath } from 'node:url'
import { PNG } from 'pngjs'

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..')
const set = 'activity-cloud-composer-v5'
const draft = 'art/drafts/activity-cloud-composer-2026-10-19-v5'
const abs = value => path.join(root, value)
const json = value => JSON.parse(fs.readFileSync(abs(value), 'utf8'))
const sha = value => crypto.createHash('sha256').update(fs.readFileSync(abs(value))).digest('hex')
const register = json(`${draft}/batch-register.json`)
const catalogue = json(`public/keeper-review/${set}/catalogue.json`)
const v4 = json('public/keeper-review/activity-cloud-composer-v4/catalogue.json')
const v4Register = json('art/drafts/activity-cloud-composer-2026-10-19-v4/batch-register.json')
const archive = json('review-archive/index.json')
const page = fs.readFileSync(abs(`public/keeper-review/${set}/index.html`), 'utf8')

const newNames = Object.keys(register.newComponents)
assert.equal(register.schema, 'lighthouse-keeper/activity-cloud-composer-register@5')
assert.equal(catalogue.schema, 'lighthouse-keeper/activity-cloud-composer@1')
assert.equal(catalogue.set, set)
assert.equal(catalogue.status, 'immutable-reversible-review-tool-not-approved')
assert.equal(sha(v4Register.page.file), v4Register.page.sha256, 'immutable Composer V4 page changed')
assert.equal(register.sourceVocabulary.catalogueSha256, sha(register.sourceVocabulary.catalogue))
assert.equal(register.sourceVocabulary.registerSha256, sha(register.sourceVocabulary.register))
assert.equal(register.sourceVocabulary.inheritedComponents, 86)

assert.deepEqual(catalogue.body, v4.body, 'V5 changed inherited Prime body')
assert.deepEqual(catalogue.route, v4.route, 'V5 changed inherited Prime route')
assert.deepEqual(catalogue.reviewReferences, v4.reviewReferences)
assert.deepEqual(catalogue.defaultRecipe, v4.defaultRecipe)
assert.deepEqual(catalogue.notationAccents, v4.notationAccents, 'V5 changed deterministic notation')
assert.deepEqual({...catalogue.composer, localStorageKey: v4.composer.localStorageKey}, v4.composer)
for (const [name, item] of Object.entries(v4.components)) assert.deepEqual(catalogue.components[name], item, `V5 changed inherited component ${name}`)
assert.equal(Object.keys(catalogue.components).length, 146)
assert.equal(newNames.length, 60)
assert.equal(register.generatedSources.length, 10)
assert.equal(Object.keys(catalogue.suggestedRecipes).length, 15)

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

for (const sourceRecord of register.generatedSources) {
  assert.equal(sourceRecord.sha256, sha(sourceRecord.file))
  const png = PNG.sync.read(fs.readFileSync(abs(sourceRecord.file)))
  assert.deepEqual([png.width, png.height], [1536, 1024])
  assert.equal(edgeAlpha(png), 0, `${sourceRecord.file} touches outer edge`)
  assert.equal(lineAlpha(png, 'x', 512), 0, `${sourceRecord.file} crosses x=512`)
  assert.equal(lineAlpha(png, 'x', 1024), 0, `${sourceRecord.file} crosses x=1024`)
  assert.equal(lineAlpha(png, 'y', 512), 0, `${sourceRecord.file} crosses y=512`)
  assert.deepEqual(Object.values(sourceRecord.cellBoundaryAlphaPixels), [0, 0, 0])
}

for (const name of newNames) {
  const record = register.newComponents[name]
  const component = catalogue.components[name]
  assert.equal(record.sha256, sha(record.file))
  assert.equal(component.sha256, record.sha256)
  assert.equal(component.sourceSet, set)
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

for (const [key, recipe] of Object.entries(catalogue.suggestedRecipes)) {
  assert.equal(recipe.elements.length >= 4 && recipe.elements.length <= 5, true, `${key} must contain 4–5 elements`)
  assert.equal(new Set(recipe.elements).size, recipe.elements.length, `${key} repeats an element`)
  for (const name of recipe.elements) assert.ok(catalogue.components[name], `${key} references missing ${name}`)
  assert.ok(['rear-work-with-context', 'rear-work', 'dedicated-pose-required'].includes(recipe.bodyCompatibility))
  assert.ok(recipe.targetAssetId && recipe.targetAssetLabel && recipe.label && recipe.sfx)
}

assert.equal(register.checks.primeBodyUnchanged, true)
assert.equal(register.checks.runtimeChanged, false)
assert.equal(register.checks.kitchenChanged, false)
assert.equal(register.checks.deployed, false)
assert.match(page, /Activity Cloud Composer V5/)
assert.match(page, /Immutable Composer V4/)
assert.match(page, /Start from a suggested package/)
assert.match(page, /showNotation/)
assert.match(page, /notationAccents/)
assert.match(page, /Promise\.all\(\[\.\.\.new Set/)
assert.match(page, /img\.decode/)
assert.match(page, /contextBakedIntoKeeper:false/)
const scripts = [...page.matchAll(/<script>([\s\S]*?)<\/script>/g)]
assert.equal(scripts.length, 1)
new vm.Script(scripts[0][1])

assert.equal(sha(register.catalogue.file), register.catalogue.sha256)
assert.equal(sha(register.page.file), register.page.sha256)
console.log(JSON.stringify({set, inheritedComponents: 86, newComponents: 60, components: 146, sources: 10, suggestedRecipes: 15, ownership: 'one-owner-zero-ambiguous', gutters: '>=16px', primeBody: 'unchanged', runtimeChanged: false, kitchenChanged: false, deployed: false}, null, 2))
