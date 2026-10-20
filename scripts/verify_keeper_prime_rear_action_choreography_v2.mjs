#!/usr/bin/env node
import assert from 'node:assert/strict'
import crypto from 'node:crypto'
import fs from 'node:fs'
import path from 'node:path'
import zlib from 'node:zlib'
import vm from 'node:vm'
import { fileURLToPath } from 'node:url'

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..')
const set = 'keeper-prime-rear-action-choreography-v2'
const v1Set = 'keeper-prime-rear-action-choreography-v1'
const draft = 'art/drafts/keeper-prime-rear-action-choreography-2026-10-20-v2'
const pack = `${draft}/claude-code-model-test-pack`
const abs = value => path.join(root, value)
const json = value => JSON.parse(fs.readFileSync(abs(value), 'utf8'))
const sha = value => crypto.createHash('sha256').update(fs.readFileSync(abs(value))).digest('hex')

const candidate = JSON.parse(zlib.gunzipSync(fs.readFileSync(abs(`public/keeper-review/${set}/catalogue.json.gz`))))
const v1 = json(`public/keeper-review/${v1Set}/catalogue.json`)
const register = json(`${draft}/batch-register.json`)
const assetManifest = json(`${pack}/asset-manifest.json`)
const page = fs.readFileSync(abs(`public/keeper-review/${set}/index.html`), 'utf8')

assert.equal(candidate.schema, 'lighthouse-keeper/keeper-prime-rear-action-choreography@2')
assert.equal(candidate.set, set)
assert.equal(candidate.defaultTreatment, 'bubble')
assert.equal(candidate.predecessor.catalogueSha256, sha(candidate.predecessor.catalogueFile))
assert.equal(candidate.predecessor.pageSha256, sha(candidate.predecessor.pageFile))
assert.equal(candidate.predecessor.manifestSha256, sha(candidate.predecessor.manifestFile))
assert.deepEqual(candidate.sequence, v1.sequence, 'approved Prime sequence changed')
assert.deepEqual(candidate.authoritySnapshot, v1.authoritySnapshot, 'Prime authority snapshot changed')
assert.deepEqual(candidate.inheritedComponents, v1.inheritedComponents, 'activity assets changed')
assert.deepEqual(candidate.symbols, v1.symbols, 'comic-symbol assets changed')
assert.equal(candidate.callout.bubbleRefinement.mainFill, 'rgba(246,239,211,.22)')
assert.equal(candidate.callout.bubbleRefinement.connectorLeftPx, 168)
assert.equal(candidate.callout.bubbleRefinement.additionalKineticSymbolsPerStory, 6)
assert.deepEqual(candidate.callout.bubbleRefinement.kineticSymbolGrammar, {
  directionalTrails: 3,
  contactImpacts: 3,
  marksFollowOwnedObjectMotion: true,
})
assert.equal(candidate.callout.bubbleRefinement.openTreatmentChanged, false)

const pathDistance = (frames, layer) => {
  const ids = [...new Set(frames.flatMap(frame => frame[layer].map(item => item.instance)))]
  let total = 0
  for (const id of ids) {
    const states = frames.map(frame => frame[layer].find(item => item.instance === id)).filter(Boolean)
    for (let index = 1; index < states.length; index++) {
      if (states[index - 1].opacity > .2 && states[index].opacity > .2) total += Math.hypot(states[index].x - states[index - 1].x, states[index].y - states[index - 1].y)
    }
  }
  return total
}

const meanPairDistance = frames => {
  let sum = 0
  let count = 0
  for (const frame of frames.slice(8, 34)) {
    const visible = frame.objects.filter(item => item.opacity > .35)
    for (let a = 0; a < visible.length; a++) for (let b = a + 1; b < visible.length; b++) {
      sum += Math.hypot(visible[a].x - visible[b].x, visible[a].y - visible[b].y)
      count++
    }
  }
  return sum / count
}

let v1Movement = 0
let v2Movement = 0
let v1Spacing = 0
let v2Spacing = 0
for (const storyId of Object.keys(v1.stories)) {
  const original = v1.stories[storyId]
  const refined = candidate.stories[storyId]
  assert.deepEqual(refined.timelines.open, original.timelines.open, `${storyId} V1 open treatment changed`)
  assert.notDeepEqual(refined.timelines.bubble.full, original.timelines.bubble.full, `${storyId} bubble did not change`)
  assert.equal(refined.timelines.bubble.full.length, 42)
  assert.equal(refined.timelines.bubble.reduced.length, 42)
  const oldIds = new Set(original.timelines.bubble.full.flatMap(frame => frame.symbols.map(item => item.instance)))
  const newIds = new Set(refined.timelines.bubble.full.flatMap(frame => frame.symbols.map(item => item.instance)))
  assert.equal(newIds.size, oldIds.size + 6)
  for (const support of refined.timelines.bubble.full[0].objects.filter(item => item.role === 'support')) {
    assert.ok(newIds.has(`momentum-${support.instance}`), `${storyId} missing momentum trail for ${support.instance}`)
    assert.ok(newIds.has(`contact-${support.instance}`), `${storyId} missing contact star for ${support.instance}`)
  }
  for (const frame of refined.timelines.bubble.full) {
    assert.equal(frame.objects.length, 5)
    assert.ok(frame.symbols.length >= 8)
    assert.ok(frame.objects.every(item => item.x >= -112 && item.x <= 112 && item.y >= -72 && item.y <= 68))
    for (const item of frame.symbols.filter(item => item.instance.startsWith('momentum-'))) {
      assert.equal(item.motionFunction, 'directional-trail')
      assert.ok(item.anchorInstance)
    }
    for (const item of frame.symbols.filter(item => item.instance.startsWith('contact-'))) {
      assert.equal(item.motionFunction, 'contact-impact')
      assert.ok(item.anchorInstance)
      assert.ok(item.interactionWith)
    }
    if (frame.quietTail) assert.ok(frame.symbols.every(item => item.opacity === 0), `${storyId} V2 symbol persists into quiet tail`)
  }
  for (const frame of refined.timelines.bubble.reduced) {
    assert.ok(frame.objects.filter(item => item.opacity > 0).length <= 2)
    assert.ok(frame.symbols.filter(item => item.opacity > 0).length <= 1)
    assert.ok([...frame.objects, ...frame.symbols].every(item => item.rotation === 0))
  }
  v1Movement += pathDistance(original.timelines.bubble.full, 'objects')
  v2Movement += pathDistance(refined.timelines.bubble.full, 'objects')
  v1Spacing += meanPairDistance(original.timelines.bubble.full)
  v2Spacing += meanPairDistance(refined.timelines.bubble.full)
}
assert.ok(v2Movement > v1Movement * 1.15, `bubble object movement did not rise enough: ${v1Movement} -> ${v2Movement}`)
assert.ok(v2Spacing > v1Spacing * 1.06, `bubble object spacing did not rise enough: ${v1Spacing} -> ${v2Spacing}`)

assert.match(page, /background:rgba\(246,239,211,\.22\)/)
assert.match(page, /left:168px;bottom:1px;background:rgba\(246,239,211,\.16\)/)
assert.match(page, /option value="bubble" selected/)
assert.match(page, /refined bubble bustle/)
assert.match(page, /Promise\.all/)
assert.match(page, /img\.decode/)
assert.match(page, /DecompressionStream\('gzip'\)/)
assert.match(page, /catalogue\.json\.gz/)
assert.ok(!fs.existsSync(abs(`public/keeper-review/${set}/catalogue.json`)), 'plain V2 public catalogue must stay out of deployment')
const scripts = [...page.matchAll(/<script>([\s\S]*?)<\/script>/g)]
assert.equal(scripts.length, 1)
new vm.Script(scripts[0][1])

assert.equal(register.schema, 'lighthouse-keeper/keeper-prime-rear-action-choreography-register@2')
assert.equal(register.publishedAssets.length, 0)
assert.equal(register.modelTestPack.assetCount, 68)
assert.equal(register.modelTestPack.manifestSha256, sha(register.modelTestPack.manifest))
assert.equal(register.checks.v1BytesUnchanged, true)
assert.equal(register.checks.runtimeChanged, false)
assert.equal(register.checks.kitchenChanged, false)
assert.equal(register.checks.deployed, false)
for (const entry of Object.values(register.files)) assert.equal(entry.sha256, sha(entry.file), `pinned file drift: ${entry.file}`)
assert.equal(register.candidate.publicShell.sha256, sha(register.candidate.publicShell.file))
assert.equal(register.candidate.catalogue.sha256, sha(register.candidate.catalogue.file))
assert.equal(register.candidate.publicCatalogueGzip.sha256, sha(register.candidate.publicCatalogueGzip.file))

assert.equal(assetManifest.schema, 'lighthouse-keeper/activity-cloud-model-test-pack@1')
assert.equal(assetManifest.assetCount, 68)
assert.equal(assetManifest.bodyAssetCount, 41)
assert.equal(assetManifest.activityAssetCount, 20)
assert.equal(assetManifest.symbolAssetCount, 6)
assert.equal(assetManifest.sourceAssetCount, 1)
assert.equal(assetManifest.assets.length, 68)
for (const asset of assetManifest.assets) {
  assert.ok(fs.existsSync(abs(asset.file)), `model-test asset missing: ${asset.file}`)
  assert.equal(asset.sha256, sha(asset.file), `model-test asset hash drift: ${asset.file}`)
  assert.equal(asset.sourceSha256, sha(asset.sourceFile), `model-test source hash drift: ${asset.sourceFile}`)
}
for (const file of ['README.md', 'CLAUDE_CODE_MODEL_TEST_PROMPT.md', 'metadata/v2-catalogue.json', 'metadata/v1-catalogue.json', 'metadata/approved-prime-sequence.json', 'metadata/activity-vocabulary.json']) assert.ok(fs.existsSync(abs(`${pack}/${file}`)), `model-test pack missing ${file}`)

assert.ok(!fs.existsSync(abs(`review-archive/sets/${set}.json`)), 'text-only V2 must not add an empty media archive set')

console.log(JSON.stringify({
  set,
  stories: Object.keys(candidate.stories),
  additionalKineticSymbolsPerStory: 6,
  bubbleObjectMovementIncreasePercent: Number(((v2Movement / v1Movement - 1) * 100).toFixed(1)),
  bubbleMeanPairSpacingIncreasePercent: Number(((v2Spacing / v1Spacing - 1) * 100).toFixed(1)),
  modelTestAssets: assetManifest.assetCount,
  v1Changed: false,
  primeAuthorityChanged: false,
  runtimeChanged: false,
  kitchenChanged: false,
  deployed: false,
}, null, 2))
