#!/usr/bin/env node
/** Verify the immutable V3 activity vocabulary candidate. */
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
const set = 'keeper-prime-back-work-activity-callout-v3'
const draft = 'art/drafts/keeper-prime-back-work-activity-callout-2026-10-19-v3'
const register = json(`${draft}/batch-register.json`)
const catalogue = json(`${draft}/catalogue.json`)
const publicCatalogue = json(`public/keeper-review/${set}/catalogue.json`)
const v2 = json('art/drafts/keeper-prime-back-work-activity-callout-2026-10-19-v2/catalogue.json')
const v2Public = json('public/keeper-review/keeper-prime-back-work-activity-callout-v2/catalogue.json')
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
  assert.ok(maxX >= 0, 'empty component')
  return Math.min(minX, minY, image.width - 1 - maxX, image.height - 1 - maxY)
}

function cellEdgeAlphaCount(image, left, top, size) {
  let count = 0
  for (let x = left; x < left + size; x += 1) {
    if (px(image, x, top)[3]) count += 1
    if (px(image, x, top + size - 1)[3]) count += 1
  }
  for (let y = top + 1; y < top + size - 1; y += 1) {
    if (px(image, left, y)[3]) count += 1
    if (px(image, left + size - 1, y)[3]) count += 1
  }
  return count
}

assert.equal(register.schema, 'lighthouse-keeper/reversible-review-batch@1')
assert.equal(register.set, set)
assert.equal(register.status, 'prime-back-work-vocabulary-v3-awaiting-frank')
assert.equal(catalogue.schema, 'lighthouse-keeper/prime-back-work-activity-review@3')
assert.equal(catalogue.status, 'immutable-reversible-vocabulary-v3-not-approved')
assert.equal(register.bodyInheritance.catalogueSha256, sha(register.bodyInheritance.catalogueFile))
assert.equal(register.bodyInheritance.registerSha256, sha(register.bodyInheritance.registerFile))
assert.equal(register.bodyInheritance.bodyAndRouteChanged, false)
assert.deepEqual(catalogue.body, v2.body, 'V3 changed the V2/V1 body authority')
assert.deepEqual(catalogue.route, v2.route, 'V3 changed the approved walk-stop-turn route')
assert.deepEqual(catalogue.registration, v2.registration)
assert.deepEqual(catalogue.reviewReferences, v2.reviewReferences)
assert.deepEqual(publicCatalogue.body, v2Public.body)
assert.deepEqual(publicCatalogue.route, v2Public.route)

for (const [name, authority] of Object.entries(register.authorities)) {
  if (name === 'runtimeManifest') {
    const entry = json(authority.file).keeper_cook_back
    assert.deepEqual(entry, { file: 'keeper_cook_back.png', w: 32, h: 40, frames: 8, fps: 4, density: 4, anchor: [16, 40], handUsePoint: [16, 21], startPose: 'standing-back', endPose: 'standing-back', assetRole: 'clip', loop: true, z: 50 })
  } else assert.equal(authority.sha256, sha(authority.file), `authority changed: ${authority.file}`)
}
for (const record of Object.values(register.protectedState)) assert.equal(record.sha256, sha(record.file), `protected state changed: ${record.file}`)
for (const [name, reference] of Object.entries(register.directionalReferences)) {
  assert.equal(reference.authority, false, `${name} incorrectly promoted to authority`)
  if (reference.file) assert.equal(reference.sha256, sha(reference.file), `directional reference changed: ${reference.file}`)
}

assert.equal(register.generation.selectedSources.length, 13)
for (const source of register.generation.selectedSources) {
  assert.equal(source.sha256, sha(source.file), `generated source changed: ${source.file}`)
  assert.deepEqual(source.pixels, [1536, 1024])
  assert.equal(source.verticalSharedBoundaryAlphaPixels, 0, `${source.file} has alpha on vertical ownership boundary`)
  assert.equal(source.horizontalSharedBoundaryAlphaPixels, 0, `${source.file} has alpha on horizontal ownership boundary`)
  assert.equal(source.cells.length, 4)
  const [tl, tr, bl, br] = source.cells.map(cell => cell.crop)
  assert.deepEqual(tl, [0, 0, source.splitX, source.splitY])
  assert.deepEqual(tr, [source.splitX, 0, 1536, source.splitY])
  assert.deepEqual(bl, [0, source.splitY, source.splitX, 1024])
  assert.deepEqual(br, [source.splitX, source.splitY, 1536, 1024])
  assert.equal(new Set(source.cells.map(cell => cell.asset)).size, 4)
}

assert.equal(Object.keys(register.candidate.newCalloutComponents).length, 52)
for (const [name, record] of Object.entries(register.candidate.newCalloutComponents)) {
  assert.equal(record.sha256, sha(record.file), `${name} component changed`)
  const image = png(record.file)
  assert.deepEqual([image.width, image.height], [256, 256])
  assert.equal(edgeAlphaCount(image), 0, `${name} touches a cell edge`)
  assert.equal(record.edgeAlphaPixels, 0)
  assert.equal(record.transparentGutterPx, alphaGutter(image))
  assert.ok(record.transparentGutterPx >= 16, `${name} lacks a 16-pixel safety gutter`)
  assert.deepEqual(record.ownership, { ownerCount: 1, ambiguousPixels: 0, unownedVisiblePixels: 0 })
}
assert.equal(Object.keys(register.candidate.inheritedV2Components).length, 16)
for (const [name, record] of Object.entries(register.candidate.inheritedV2Components)) assert.equal(record.sha256, sha(record.file), `${name} inherited V2 component changed`)

const atlasRecord = register.candidate.componentAtlas
assert.equal(atlasRecord.sha256, sha(atlasRecord.file))
assert.equal(atlasRecord.componentOrder.length, 52)
const atlas = png(atlasRecord.file)
assert.deepEqual([atlas.width, atlas.height], [atlasRecord.columns * 256, atlasRecord.rows * 256])
atlasRecord.componentOrder.forEach((name, index) => {
  assert.ok(register.candidate.newCalloutComponents[name])
  assert.equal(cellEdgeAlphaCount(atlas, (index % atlasRecord.columns) * 256, Math.floor(index / atlasRecord.columns) * 256, 256), 0, `${name} touches an atlas cell edge`)
})

assert.deepEqual(Object.keys(catalogue.callouts.styles), ['orbit', 'bustle'])
assert.equal(catalogue.callouts.styleApproved, null)
assert.equal(catalogue.callouts.frames, 42)
assert.equal(catalogue.callouts.fps, 8)
assert.equal(Object.keys(catalogue.callouts.components).length, 68)
assert.equal(Object.keys(catalogue.callouts.phrases).length, 25)
assert.equal(catalogue.callouts.placement.counterPresent, false)
assert.equal(catalogue.callouts.placement.furniturePresent, false)

let worstLogicalBottom = -Infinity
for (const [activity, phrase] of Object.entries(catalogue.callouts.phrases)) {
  assert.ok(['rear-work', 'rear-work-with-context', 'dedicated-pose-required'].includes(phrase.bodyCompatibility), `${activity} lacks explicit body compatibility`)
  for (const treatment of ['orbit', 'bustle']) {
    const frames = phrase.treatments[treatment].frames
    assert.equal(frames.length, 42, `${activity}/${treatment} phrase length changed`)
    assert.deepEqual(frames.map(frame => frame.frame), Array.from({ length: 42 }, (_, i) => i))
    assert.ok(frames.slice(37).every(frame => frame.components.length === 0), `${activity}/${treatment} lacks a quiet tail`)
    assert.ok(frames.some(frame => frame.components.some(part => ['primary', 'resolved-primary'].includes(part.role))))
    for (const frame of frames) for (const part of frame.components) {
      assert.ok(catalogue.callouts.components[part.asset], `${activity} references unknown component ${part.asset}`)
      assert.ok(part.opacity >= 0 && part.opacity <= 1)
      const rotatedRadius = 52 * part.scale * Math.SQRT2
      worstLogicalBottom = Math.max(worstLogicalBottom, 95 + part.y + rotatedRadius)
    }
  }
}
const placement = catalogue.callouts.placement
assert.ok(placement.large.actorTopPx - (placement.large.calloutTopPx + worstLogicalBottom) >= placement.large.minimumCapClearancePx, 'large callout violates cap clearance')
assert.ok(placement.game.actorTopPx - (placement.game.calloutTopPx + worstLogicalBottom * placement.game.outerScale) >= placement.game.minimumCapClearancePx, 'game-scale callout violates cap clearance')

const sandwich = catalogue.callouts.phrases['snack-sandwich']
assert.deepEqual(sandwich.story, ['sandwich-bread', 'sandwich-ham', 'sandwich-lettuce', 'sandwich-tomato', 'cooking-sandwich'])
for (const treatment of ['orbit', 'bustle']) {
  const frames = sandwich.treatments[treatment].frames
  const ingredientFirst = Math.min(...frames.filter(frame => frame.components.some(part => part.role === 'ingredient')).map(frame => frame.frame))
  const resolvedFirst = Math.min(...frames.filter(frame => frame.components.some(part => part.role === 'resolved-primary')).map(frame => frame.frame))
  assert.ok(ingredientFirst < resolvedFirst, 'sandwich must assemble before resolving')
}
assert.deepEqual(catalogue.callouts.phrases.breakfast.lineage, { animal: 'cooking-pig', result: 'cooking-bacon' })
assert.deepEqual(catalogue.callouts.phrases['dinner-beef'].lineage, { animal: 'cooking-cow', result: 'bbq-steak' })
assert.deepEqual(catalogue.callouts.phrases['dinner-lamb'].lineage, { animal: 'cooking-sheep', results: ['bbq-lamb-chops', 'bbq-leg-lamb'] })

for (const token of ['rest-counting-sheep', 'music-guitarist', 'music-drummer', 'music-composer', 'aquarium-castle', 'aquarium-plants', 'aquarium-treasure', 'aquarium-aerator']) assert.ok(catalogue.callouts.components[token], `missing requested token ${token}`)
assert.ok(catalogue.callouts.phrases.sleeping.helpers.includes('rest-counting-sheep'))
assert.ok(catalogue.callouts.phrases['play-guitar'].helpers.includes('music-guitarist'))
assert.ok(catalogue.callouts.phrases['play-drums'].helpers.includes('music-drummer'))
assert.ok(catalogue.callouts.phrases['play-piano'].helpers.includes('music-composer'))
assert.ok(catalogue.callouts.phrases['feed-fish'].helpers.includes('aquarium-castle'))

assert.equal(catalogue.sfx.bodySilent, true)
for (const activity of Object.keys(catalogue.callouts.phrases)) {
  assert.ok(catalogue.sfx[activity].length > 0)
  assert.ok(catalogue.sfx[activity].every(cue => ['activity-beat', 'asset-state', 'completion'].includes(cue.kind)))
}
assert.deepEqual(publicCatalogue.callouts, catalogue.callouts)
assert.deepEqual(publicCatalogue.sfx, catalogue.sfx)
assert.deepEqual(publicCatalogue.bodyInheritance, catalogue.bodyInheritance)
assert.equal(register.candidate.catalogue.sha256, sha(register.candidate.catalogue.file))
assert.equal(register.candidate.publicCatalogue.sha256, sha(register.candidate.publicCatalogue.file))
assert.equal(register.candidate.publicShell.sha256, sha(register.candidate.publicShell.file))
assert.equal(register.candidate.raisedNoCounterContactSheet.sha256, sha(register.candidate.raisedNoCounterContactSheet.file))
assert.equal(register.candidate.raisedNoCounterContactSheet.counterPresent, false)
assert.equal(register.candidate.raisedNoCounterContactSheet.calloutRaised, true)

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

for (const [name, value] of Object.entries(register.checks)) assert.equal(value, ['kitchenWorkChanged', 'runtimeChanged'].includes(name) ? false : true, `${name} changed`)
for (const value of Object.values(register.approvalBoundary)) assert.equal(value, false, 'review candidate crossed its approval boundary')
assert.ok(!page.includes('class="furniture"'), 'review page reintroduced furniture/counter markup')
assert.ok(!page.includes('.furniture'), 'review page reintroduced furniture/counter CSS')
for (const token of ['Critical seam gate', 'Counter removed', 'Callouts raised', 'no counter', '42 frames', 'sandwich', 'Body', 'Activity envelope/marks', 'Primary/resolved object', 'Supporting/story objects', 'Mute SFX', 'Reduced motion', 'dedicated body poses', 'img.decode', 'Promise.all']) assert.ok(page.includes(token), `review page missing ${token}`)

console.log('Prime rear-work activity vocabulary V3 verified: V1/V2 body and route immutable, 52 new isolated components, 25 recipes, raised callouts, no counter, no promotion.')
