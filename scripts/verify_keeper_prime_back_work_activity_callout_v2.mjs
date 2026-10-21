#!/usr/bin/env node
/** Verify the immutable V2 game-language activity-callout review candidate. */
import assert from 'node:assert/strict'
import crypto from 'node:crypto'
import fs from 'node:fs'
import path from 'node:path'
import { PNG } from 'pngjs'

const root = path.resolve(import.meta.dirname, '..')
const abs = name => path.join(root, name)
const json = name => JSON.parse(fs.readFileSync(abs(name), 'utf8'))
const sha = name => crypto.createHash('sha256').update(fs.readFileSync(abs(name))).digest('hex')
const png = name => PNG.sync.read(fs.readFileSync(abs(name)))
const px = (image, x, y) => image.data.subarray((y * image.width + x) * 4, (y * image.width + x) * 4 + 4)
const set = 'keeper-prime-back-work-activity-callout-v2'
const draft = 'art/drafts/keeper-prime-back-work-activity-callout-2026-10-19-v2'
const register = json(`${draft}/batch-register.json`)
const catalogue = json(`${draft}/catalogue.json`)
const publicCatalogue = json(`public/keeper-review/${set}/catalogue.json`)
const v1 = json('art/drafts/keeper-prime-back-work-activity-callout-2026-10-19-v1/catalogue.json')
const v1Public = json('public/keeper-review/keeper-prime-back-work-activity-callout-v1/catalogue.json')
const page = fs.readFileSync(abs(`public/keeper-review/${set}/index.html`), 'utf8')

function edgeAlphaCount(image) {
  let count = 0
  for (let x = 0; x < image.width; x += 1) {
    if (px(image, x, 0)[3]) count += 1
    if (px(image, x, image.height - 1)[3]) count += 1
  }
  for (let y = 1; y < image.height - 1; y += 1) {
    if (px(image, 0, y)[3]) count += 1
    if (px(image, image.width - 1, y)[3]) count += 1
  }
  return count
}

function alphaGutter(image) {
  let minX = image.width; let minY = image.height; let maxX = -1; let maxY = -1
  for (let y = 0; y < image.height; y += 1) for (let x = 0; x < image.width; x += 1) {
    if (!px(image, x, y)[3]) continue
    minX = Math.min(minX, x); minY = Math.min(minY, y); maxX = Math.max(maxX, x); maxY = Math.max(maxY, y)
  }
  assert.ok(maxX >= 0, 'empty callout component')
  return Math.min(minX, minY, image.width - 1 - maxX, image.height - 1 - maxY)
}

assert.equal(register.schema, 'lighthouse-keeper/reversible-review-batch@1')
assert.equal(register.set, set)
assert.equal(register.status, 'prime-back-work-callout-v2-awaiting-frank')
assert.equal(catalogue.schema, 'lighthouse-keeper/prime-back-work-activity-review@2')
assert.equal(catalogue.status, 'immutable-reversible-callout-v2-not-approved')
assert.equal(register.bodyInheritance.catalogueSha256, sha(register.bodyInheritance.catalogueFile))
assert.equal(register.bodyInheritance.registerSha256, sha(register.bodyInheritance.registerFile))
assert.equal(register.bodyInheritance.bodyAndRouteChanged, false)
assert.deepEqual(catalogue.body, v1.body, 'V2 must inherit every V1 body field and byte reference')
assert.deepEqual(catalogue.route, v1.route, 'V2 must inherit the complete V1 route')
assert.deepEqual(catalogue.registration, v1.registration)
assert.deepEqual(catalogue.reviewReferences, v1.reviewReferences)
assert.deepEqual(publicCatalogue.body, v1Public.body)
assert.deepEqual(publicCatalogue.route, v1Public.route)

for (const [name, authority] of Object.entries(register.authorities)) {
  if (name === 'runtimeManifest') {
    const entry = json(authority.file).keeper_cook_back
    assert.deepEqual(entry, { file: 'keeper_cook_back.png', w: 32, h: 40, frames: 8, fps: 4, density: 4, anchor: [16, 40], handUsePoint: [16, 21], startPose: 'standing-back', endPose: 'standing-back', assetRole: 'clip', loop: true, z: 50 })
  } else assert.equal(authority.sha256, sha(authority.file), `authority changed: ${authority.file}`)
}
for (const record of Object.values(register.protectedState)) assert.equal(record.sha256, sha(record.file), `protected state changed: ${record.file}`)
for (const [name, reference] of Object.entries(register.directionalReferences)) {
  assert.equal(reference.authority, false, `${name} was incorrectly promoted to authority`)
  if (reference.file) assert.equal(reference.sha256, sha(reference.file), `directional reference changed: ${reference.file}`)
}
assert.equal(register.directionalReferences.frankRadialInspiration.retained, false)

assert.equal(register.generation.selectedSources.length, 4)
for (const source of register.generation.selectedSources) {
  assert.equal(source.sha256, sha(source.file), `generated source changed: ${source.file}`)
  assert.deepEqual(source.pixels, [1536, 1024])
  assert.equal(source.splitX, 850)
  assert.equal(source.cells.length, 4)
  const [tl, tr, bl, br] = source.cells.map(cell => cell.crop)
  assert.deepEqual(tl, [0, 0, 850, source.splitY])
  assert.deepEqual(tr, [850, 0, 1536, source.splitY])
  assert.deepEqual(bl, [0, source.splitY, 850, 1024])
  assert.deepEqual(br, [850, source.splitY, 1536, 1024])
  assert.equal(new Set(source.cells.map(cell => cell.asset)).size, 4)
}

assert.equal(Object.keys(register.candidate.calloutComponents).length, 16)
for (const [name, record] of Object.entries(register.candidate.calloutComponents)) {
  assert.equal(record.sha256, sha(record.file), `${name} component changed`)
  const image = png(record.file)
  assert.deepEqual([image.width, image.height], [256, 256])
  assert.equal(edgeAlphaCount(image), 0, `${name} touches a cell edge`)
  assert.equal(record.edgeAlphaPixels, 0)
  assert.equal(record.transparentGutterPx, alphaGutter(image))
  assert.ok(record.transparentGutterPx >= 16, `${name} lacks a 16-pixel safety gutter`)
  assert.deepEqual(record.ownership, { ownerCount: 1, ambiguousPixels: 0, unownedVisiblePixels: 0 })
}

assert.deepEqual(Object.keys(catalogue.callouts.styles), ['orbit', 'bustle'])
assert.equal(catalogue.callouts.styles.orbit.status, 'equal review candidate')
assert.equal(catalogue.callouts.styles.bustle.status, 'equal review candidate')
assert.equal(catalogue.callouts.styleApproved, null)
assert.equal(catalogue.callouts.frames, 42)
assert.equal(catalogue.callouts.fps, 8)
assert.equal(catalogue.callouts.durationSeconds, 5.25)
assert.deepEqual(Object.keys(catalogue.callouts.phrases), ['cooking', 'mixing', 'washing', 'repair'])
for (const [activity, phrase] of Object.entries(catalogue.callouts.phrases)) {
  for (const treatment of ['orbit', 'bustle']) {
    const frames = phrase.treatments[treatment].frames
    assert.equal(frames.length, 42, `${activity}/${treatment} phrase length changed`)
    assert.deepEqual(frames.map(frame => frame.frame), Array.from({ length: 42 }, (_, i) => i))
    assert.ok(frames.slice(37).every(frame => frame.components.length === 0), `${activity}/${treatment} lacks a quiet tail`)
    assert.ok(frames.some(frame => frame.components.some(part => part.role === 'primary')))
    assert.ok(frames.some(frame => frame.components.some(part => part.role === 'helper')))
    for (const frame of frames) for (const part of frame.components) {
      assert.ok(catalogue.callouts.components[part.asset], `unknown component ${part.asset}`)
      assert.equal(catalogue.callouts.components[part.asset].activity, activity, `${part.asset} crossed activity ownership`)
      assert.ok(part.opacity >= 0 && part.opacity <= 1)
    }
  }
}
assert.equal(catalogue.callouts.phrases.mixing.family, 'mixing-washing')
assert.equal(catalogue.callouts.phrases.washing.family, 'mixing-washing')

for (const [treatment, record] of Object.entries(register.candidate.calloutContactSheets)) {
  assert.equal(record.sha256, sha(record.file), `${treatment} evidence changed`)
  assert.deepEqual(record.sampleFrames, [1, 4, 8, 15, 22, 29, 33, 38])
  assert.equal(record.includesPrimeBodyAtGameScale, true)
  const image = png(record.file)
  assert.deepEqual([image.width, image.height], [2560, 1024])
}

assert.equal(catalogue.sfx.bodySilent, true)
for (const activity of ['cooking', 'mixing', 'washing', 'repair']) {
  assert.ok(catalogue.sfx[activity].length > 0)
  assert.ok(catalogue.sfx[activity].every(cue => ['activity-beat', 'asset-state', 'completion'].includes(cue.kind)))
}
assert.deepEqual(publicCatalogue.callouts, catalogue.callouts)
assert.deepEqual(publicCatalogue.bodyInheritance, catalogue.bodyInheritance)
assert.equal(register.candidate.catalogue.sha256, sha(register.candidate.catalogue.file))
assert.equal(register.candidate.publicCatalogue.sha256, sha(register.candidate.publicCatalogue.file))
assert.equal(register.candidate.publicShell.sha256, sha(register.candidate.publicShell.file))

let archiveManifest = null
const archiveManifestFile = `review-archive/sets/${set}.json`
if (fs.existsSync(abs(archiveManifestFile))) archiveManifest = json(archiveManifestFile)
for (const asset of register.publishedAssets) {
  assert.equal(asset.sourceSha256, sha(asset.source), `published source changed: ${asset.source}`)
  if (fs.existsSync(abs(asset.public))) {
    assert.equal(asset.publicSha256, sha(asset.public), `public assembly changed: ${asset.public}`)
  } else {
    assert.ok(archiveManifest, `missing public assembly and archive manifest for ${asset.public}`)
    const legacy = `/${asset.publicAssemblyPath.replace(/^public\//, '')}`
    const archived = archiveManifest.entries[legacy]
    assert.ok(archived, `missing archived URL: ${legacy}`)
    assert.equal(archived.sha256, asset.sourceSha256)
    assert.equal(sha(archived.object), asset.sourceSha256)
  }
}

for (const [name, value] of Object.entries(register.checks)) assert.equal(value, name === 'kitchenWorkChanged' ? false : true, `${name} changed`)
for (const value of Object.values(register.approvalBoundary)) assert.equal(value, false, 'review candidate crossed its approval boundary')
for (const token of ['Critical seam gate', '24-frame action', 'Open radial orbit', 'Activity bustle', 'Cooking', 'Mixing', 'Washing', 'Generic repair', 'Keeper body', 'Activity cloud/marks', 'Supporting objects', 'Mute SFX', 'Reduced motion', 'img.decode', 'Promise.all']) assert.ok(page.includes(token), `review page missing ${token}`)

console.log('Prime rear-work callout V2 verified: V1 body/route immutable, 16 isolated game-language components, two 42-frame treatments, in-context evidence and no promotion.')
