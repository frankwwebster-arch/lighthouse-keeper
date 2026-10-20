#!/usr/bin/env node
import assert from 'node:assert/strict'
import crypto from 'node:crypto'
import fs from 'node:fs'
import path from 'node:path'
import vm from 'node:vm'
import { fileURLToPath } from 'node:url'
import { PNG } from 'pngjs'

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..')
const set = 'keeper-prime-rear-action-choreography-v1'
const draft = 'art/drafts/keeper-prime-rear-action-choreography-2026-10-20-v1'
const abs = value => path.join(root, value)
const json = value => JSON.parse(fs.readFileSync(abs(value), 'utf8'))
const sha = value => crypto.createHash('sha256').update(fs.readFileSync(abs(value))).digest('hex')
const readPng = value => PNG.sync.read(fs.readFileSync(abs(value)))

const catalogue = json(`public/keeper-review/${set}/catalogue.json`)
const draftCatalogue = json(`${draft}/catalogue.json`)
const register = json(`${draft}/batch-register.json`)
const sourceSequence = json('public/keeper-review/keeper-prime-rear-action-sequence-v1/catalogue.json')
const vocabulary = json('public/keeper-review/activity-cloud-composer-v6/catalogue.json')
const page = fs.readFileSync(abs(`public/keeper-review/${set}/index.html`), 'utf8')

assert.equal(catalogue.schema, 'lighthouse-keeper/keeper-prime-rear-action-choreography@1')
assert.equal(catalogue.set, set)
assert.equal(catalogue.status, 'immutable-reversible-choreography-review-candidate-not-approved')
assert.deepEqual(catalogue, draftCatalogue, 'draft/public catalogue drift')
assert.equal(catalogue.sourceSequence.set, 'keeper-prime-rear-action-sequence-v1')
assert.equal(catalogue.sourceSequence.sha256, sha(catalogue.sourceSequence.file), 'approved sequence catalogue drift')
assert.equal(catalogue.sourceSequence.approvalSha256, sha(catalogue.sourceSequence.approvalRecord), 'approval record drift')
assert.equal(catalogue.sourceVocabulary.set, 'activity-cloud-composer-v6')
assert.equal(catalogue.sourceVocabulary.sha256, sha(catalogue.sourceVocabulary.file), 'Composer V6 catalogue drift')
assert.deepEqual(catalogue.sequence, sourceSequence.sequence, 'approved Prime sequence changed')
assert.equal(catalogue.actionStartIndex, sourceSequence.actionStartIndex)
assert.equal(catalogue.sequenceDurationMs, sourceSequence.sequenceDurationMs)
assert.deepEqual(catalogue.phaseCounts, sourceSequence.phaseCounts)
assert.equal(catalogue.sequence.length, 52)

const authorities = new Map(catalogue.authoritySnapshot.map(entry => [entry.src, entry.sha256]))
for (const frame of catalogue.sequence) {
  const expectedHash = frame.authoritySha256 ?? frame.candidateSha256
  assert.equal(authorities.get(frame.src), expectedHash, `authority snapshot mismatch: ${frame.src}`)
  const publicPath = `public${frame.src}`
  assert.equal(sha(publicPath), expectedHash, `Prime authority bytes changed: ${frame.src}`)
}
assert.equal(catalogue.sequence[27].src, vocabulary.reviewReferences.exactRear)
assert.equal(catalogue.sequence[28].src, vocabulary.reviewReferences.exactRear)
assert.equal(catalogue.sequence[50].src, vocabulary.reviewReferences.exactRear)
assert.equal(catalogue.sequence[51].src, vocabulary.reviewReferences.exactRear)

assert.deepEqual(catalogue.callout, {
  frames: 42,
  fps: 8,
  quietTailFrames: 5,
  quietTailRange: [37, 41],
  startsWithAction: true,
  placement: 'raised-above-cap',
  treatments: ['open', 'bubble'],
  motionModes: ['full', 'reduced'],
})
assert.deepEqual(Object.keys(catalogue.stories), ['garden-bbq', 'make-sandwich', 'washing-up', 'general-repair'])
assert.equal(catalogue.defaultStory, 'garden-bbq')
assert.equal(Object.keys(catalogue.symbols).length, 6)
assert.ok(!Object.keys(catalogue.symbols).some(key => key.startsWith('icon-')), 'rejected V1 flat icons leaked into symbol vocabulary')

for (const [id, component] of Object.entries(catalogue.inheritedComponents)) {
  assert.deepEqual(component, Object.fromEntries(['src', 'sha256', 'family', 'cellPixels', 'sourceSet'].map(key => [key, vocabulary.components[id][key] ?? null])), `inherited component drift: ${id}`)
  assert.equal(sha(`public${component.src}`), component.sha256, `inherited component bytes changed: ${id}`)
}

const requiredFields = ['instance', 'component', 'role', 'x', 'y', 'scale', 'rotation', 'opacity', 'z']
let timelineCount = 0
for (const [storyId, story] of Object.entries(catalogue.stories)) {
  assert.equal(story.bodyCompatibility, 'rear-work-with-context')
  assert.equal(story.elements.length, 5)
  assert.equal(story.sfx.length, 3)
  assert.deepEqual(story.sfx.map(cue => cue.kind), ['asset-state', 'activity-beat', 'completion'])
  assert.equal(story.storyBeats.length, 4)
  assert.deepEqual(Object.keys(story.timelines), ['open', 'bubble'])
  for (const element of story.elements) assert.ok(catalogue.inheritedComponents[element], `${storyId} unknown object: ${element}`)
  const openFull = story.timelines.open.full
  const bubbleFull = story.timelines.bubble.full
  assert.notDeepEqual(openFull, bubbleFull, `${storyId} bubble is only a container switch`)
  for (const [treatment, modes] of Object.entries(story.timelines)) {
    assert.deepEqual(Object.keys(modes), ['full', 'reduced'])
    for (const [motion, frames] of Object.entries(modes)) {
      timelineCount++
      assert.equal(frames.length, 42, `${storyId}/${treatment}/${motion} frame count`)
      assert.deepEqual(frames.map(frame => frame.frame), Array.from({ length: 42 }, (_, index) => index))
      assert.deepEqual(frames.slice(37).map(frame => frame.quietTail), [true, true, true, true, true])
      assert.deepEqual(frames.slice(0, 37).map(frame => frame.quietTail), Array(37).fill(false))
      assert.deepEqual([...new Set(frames.map(frame => frame.storyPhase))], ['beginning', 'working', 'resolution', 'quiet-tail'])
      const tailStates = frames.slice(37).map(frame => JSON.stringify({ objects: frame.objects, symbols: frame.symbols }))
      assert.equal(new Set(tailStates).size, 1, `${storyId}/${treatment}/${motion} quiet tail is not settled`)
      for (const frame of frames) {
        assert.equal(frame.objects.length, 5)
        assert.ok(frame.symbols.length >= 2)
        for (const item of [...frame.objects, ...frame.symbols]) {
          for (const field of requiredFields) assert.ok(Object.hasOwn(item, field), `${storyId}/${treatment}/${motion} missing ${field}`)
          assert.ok(Number.isFinite(item.x) && Number.isFinite(item.y) && Number.isFinite(item.scale) && Number.isFinite(item.rotation) && Number.isFinite(item.opacity) && Number.isInteger(item.z))
          assert.ok(item.opacity >= 0 && item.opacity <= 1)
        }
        for (const item of frame.objects) assert.ok(catalogue.inheritedComponents[item.component])
        for (const item of frame.symbols) assert.ok(catalogue.symbols[item.component])
        if (frame.quietTail) assert.ok(frame.symbols.every(item => item.opacity === 0), `${storyId}/${treatment}/${motion} symbol persists into quiet tail`)
        if (motion === 'reduced') {
          assert.ok(frame.objects.filter(item => item.opacity > 0).length <= 2, `${storyId}/${treatment} reduced motion has more than two objects`)
          assert.ok(frame.symbols.filter(item => item.opacity > 0).length <= 1, `${storyId}/${treatment} reduced motion has more than one symbol`)
          assert.ok(frame.objects.every(item => item.rotation === 0) && frame.symbols.every(item => item.rotation === 0), `${storyId}/${treatment} reduced motion rotates continuously`)
        }
      }
      if (motion === 'full') {
        for (const component of story.elements) {
          const positions = frames.flatMap(frame => frame.objects.filter(item => item.component === component && item.opacity > .2).map(item => `${item.x},${item.y}`))
          assert.ok(new Set(positions).size >= 2, `${storyId}/${treatment} object is not mobile: ${component}`)
        }
      }
    }
  }
}
assert.equal(timelineCount, 16)

assert.deepEqual(catalogue.controls, ['body', 'hero-result', 'supporting-objects', 'symbols', 'treatment-marks', 'treatment', 'sfx-declaration', 'speed', 'loop', 'reduced-motion', 'path-overlay', 'timeline'])
for (const value of Object.values(catalogue.separation)) assert.equal(value, value === false ? false : true)
assert.equal(catalogue.separation.contextBakedIntoKeeper, false)
assert.equal(catalogue.approvalBoundary.candidateApproved, false)
assert.equal(catalogue.approvalBoundary.runtimeChanged, false)
assert.equal(catalogue.approvalBoundary.finalChanged, false)
assert.equal(catalogue.approvalBoundary.kitchenChanged, false)
assert.equal(catalogue.approvalBoundary.primeAuthorityChanged, false)
assert.equal(catalogue.approvalBoundary.deployed, false)

const source = readPng(register.generatedSource.file)
assert.deepEqual([source.width, source.height], [1536, 1024])
const alphaAt = (image, x, y) => image.data[(y * image.width + x) * 4 + 3]
let boundaryPixels = 0
for (let y = 0; y < source.height; y++) for (const x of [0, 511, 512, 1023, 1024, 1535]) if (alphaAt(source, x, y) > 8) boundaryPixels++
for (let x = 0; x < source.width; x++) for (const y of [0, 511, 512, 1023]) if (alphaAt(source, x, y) > 8) boundaryPixels++
assert.equal(boundaryPixels, 0, 'source sheet crosses an ownership boundary')
assert.equal(register.generatedSource.sha256, sha(register.generatedSource.file))
assert.equal(register.generatedSource.cells.length, 6)
for (const cell of register.generatedSource.cells) {
  assert.ok(cell.gutterPx >= 80, `${cell.owner} source gutter below 80`)
  assert.equal(cell.ambiguousPixels, 0)
  assert.equal(cell.unownedVisiblePixels, 0)
}

for (const [id, record] of Object.entries(register.newSymbols)) {
  assert.equal(record.owner, id)
  assert.equal(record.sha256, sha(record.file))
  assert.equal(record.sourceSha256, sha(record.sourceFile))
  assert.equal(record.transparentGutterPx >= 20, true)
  assert.equal(record.edgeAlphaPixels, 0)
  assert.equal(record.ambiguousPixels, 0)
  assert.equal(record.unownedVisiblePixels, 0)
  const image = readPng(record.file)
  assert.deepEqual([image.width, image.height], [256, 256])
  let visibleEdge = 0
  for (let x = 0; x < image.width; x++) for (const y of [0, image.height - 1]) if (alphaAt(image, x, y) > 8) visibleEdge++
  for (let y = 0; y < image.height; y++) for (const x of [0, image.width - 1]) if (alphaAt(image, x, y) > 8) visibleEdge++
  assert.equal(visibleEdge, 0, `${id} touches cell edge`)
  assert.equal(catalogue.symbols[id].sha256, record.sha256)
}

assert.equal(register.schema, 'lighthouse-keeper/keeper-prime-rear-action-choreography-register@1')
assert.equal(register.candidate.storyCount, 4)
assert.equal(register.candidate.treatmentsPerStory, 2)
assert.equal(register.candidate.motionModesPerTreatment, 2)
assert.equal(register.candidate.timelineFrames, 42)
assert.equal(register.candidate.quietTailFrames, 5)
assert.equal(register.candidate.sequenceFrames, 52)
for (const entry of Object.values(register.files)) assert.equal(sha(entry.file), entry.sha256, `pinned file drift: ${entry.file}`)
assert.equal(register.files.page.sha256, register.files.template.sha256)

const manifest = json(`review-archive/sets/${set}.json`)
assert.equal(manifest.set, set)
assert.equal(Object.keys(manifest.entries).length, 6)
assert.equal(manifest.page.sha256, register.candidate.publicShell.sha256)
for (const asset of register.publishedAssets) {
  assert.equal(asset.sourceSha256, sha(asset.source))
  assert.equal(asset.publicSha256, asset.sourceSha256)
  const legacy = `/${asset.publicAssemblyPath.replace(/^public\//, '')}`
  assert.equal(manifest.entries[legacy].sha256, asset.sourceSha256)
  assert.equal(sha(manifest.entries[legacy].object), asset.sourceSha256)
}

for (const token of ['Promise.all', 'img.decode', 'requestAnimationFrame', 'reducedMotion', 'pathsVisible', 'heroVisible', 'supportVisible', 'symbolsVisible', 'treatmentVisible', 'muted', 'speed', 'loop', 'Open choreography · no bubble', 'Compact bustle · bubble', 'Path and frame diagnostic']) assert.match(page, new RegExp(token.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')))
assert.match(page, /preloadUrls\(\)\.map\(decode\)/)
assert.doesNotMatch(page, /<div[^>]+class="[^"]*counter/i)
assert.doesNotMatch(page, /kitchenChanged\s*:\s*true/)
const scripts = [...page.matchAll(/<script>([\s\S]*?)<\/script>/g)]
assert.equal(scripts.length, 1)
new vm.Script(scripts[0][1])

console.log(JSON.stringify({
  set,
  approvedSequenceFrames: catalogue.sequence.length,
  stories: Object.keys(catalogue.stories),
  authoredTreatments: 8,
  explicitTimelines: timelineCount,
  framesPerTimeline: 42,
  newOwnedSymbols: Object.keys(catalogue.symbols).length,
  sourceBoundaryAlphaPixels: boundaryPixels,
  quietTailFrames: 5,
  primeAuthorityChanged: false,
  runtimeChanged: false,
  kitchenChanged: false,
  deployed: false,
}, null, 2))
