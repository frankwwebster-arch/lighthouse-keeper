#!/usr/bin/env node
/** Verify the immutable, reversible Prime rear-work + activity-callout V1 review candidate. */
import assert from 'node:assert/strict'
import crypto from 'node:crypto'
import fs from 'node:fs'
import path from 'node:path'
import { PNG } from 'pngjs'

const root = path.resolve(import.meta.dirname, '..')
const abs = (name) => path.join(root, name)
const json = (name) => JSON.parse(fs.readFileSync(abs(name), 'utf8'))
const sha = (name) => crypto.createHash('sha256').update(fs.readFileSync(abs(name))).digest('hex')
const png = (name) => PNG.sync.read(fs.readFileSync(abs(name)))
const px = (image, x, y) => image.data.subarray((y * image.width + x) * 4, (y * image.width + x) * 4 + 4)
const set = 'keeper-prime-back-work-activity-callout-v1'
const draft = 'art/drafts/keeper-prime-back-work-activity-callout-2026-10-19-v1'
const register = json(`${draft}/batch-register.json`)
const catalogue = json(`${draft}/catalogue.json`)
const publicCatalogue = json(`public/keeper-review/${set}/catalogue.json`)
const page = fs.readFileSync(abs(`public/keeper-review/${set}/index.html`), 'utf8')
const components = ['capCrown', 'capBandBrim', 'jumperBlue', 'creamBand', 'trousers', 'boots', 'skin', 'hair', 'outline']

function edgeAlphaCount(image, x0 = 0, width = image.width) {
  let count = 0
  for (let x = x0; x < x0 + width; x += 1) {
    if (px(image, x, 0)[3]) count += 1
    if (px(image, x, image.height - 1)[3]) count += 1
  }
  for (let y = 1; y < image.height - 1; y += 1) {
    if (px(image, x0, y)[3]) count += 1
    if (px(image, x0 + width - 1, y)[3]) count += 1
  }
  return count
}

assert.equal(register.schema, 'lighthouse-keeper/reversible-review-batch@1')
assert.equal(register.set, set)
assert.equal(register.status, 'prime-back-work-and-callout-v1-awaiting-frank')
assert.equal(catalogue.schema, 'lighthouse-keeper/prime-back-work-activity-review@1')
assert.equal(catalogue.status, 'immutable-reversible-review-candidate-not-approved')
assert.deepEqual(catalogue.registration.cellPixels, [256, 320])
assert.equal(catalogue.registration.density, 8)
assert.equal(catalogue.registration.floorPixelY, 315)
assert.equal(catalogue.body.fps, 4)
assert.equal(catalogue.body.frames.length, 24)
assert.equal(catalogue.body.frames.length / catalogue.body.fps, 6)
assert.deepEqual(catalogue.body.sfxCues, [])
assert.equal(catalogue.sfx.bodySilent, true)
assert.equal(register.candidate.publicCatalogue.sha256, sha(register.candidate.publicCatalogue.file))
assert.equal(register.candidate.publicCatalogue.projection, 'playback-fields-only')
assert.deepEqual(publicCatalogue.callouts, catalogue.callouts)
assert.deepEqual(publicCatalogue.contextLayer, catalogue.contextLayer)
assert.deepEqual(publicCatalogue.sfx, catalogue.sfx)
assert.deepEqual(publicCatalogue.route, catalogue.route)
assert.deepEqual(publicCatalogue.reviewReferences, catalogue.reviewReferences)
assert.deepEqual(publicCatalogue.body.frames, catalogue.body.frames.map(({ frame, src }) => ({ frame, src })))

for (const [name, authority] of Object.entries(register.authorities)) {
  if (name === 'runtimeManifest') {
    const entry = json(authority.file).keeper_cook_back
    assert.deepEqual(entry, { file: 'keeper_cook_back.png', w: 32, h: 40, frames: 8, fps: 4, density: 4, anchor: [16, 40], handUsePoint: [16, 21], startPose: 'standing-back', endPose: 'standing-back', assetRole: 'clip', loop: true, z: 50 })
  } else assert.equal(authority.sha256, sha(authority.file), `authority changed: ${authority.file}`)
}
for (const reference of Object.values(register.directionalReferences)) {
  assert.equal(reference.sha256, sha(reference.file), `directional reference changed: ${reference.file}`)
  assert.equal(reference.authority, false, `${reference.file} must not become an authority`)
}
for (const source of register.generation.selectedSources) assert.equal(source.sha256, sha(source.file), `source changed: ${source.file}`)
assert.equal(register.generation.rejectedPromptProvenance.sha256, sha(register.generation.rejectedPromptProvenance.file))
assert.equal(register.historicalChoreographyOnly.clip, 'keeper_cook_back')
assert.equal(register.historicalChoreographyOnly.visibleHistoricalPixelsReused, 0)

const rearHash = register.authorities.exactRear.sha256
for (const frameNumber of [1, 23, 24]) assert.equal(catalogue.body.frames[frameNumber - 1].sha256, rearHash, `frame ${frameNumber} must be an exact rear-neutral byte copy`)
for (const frame of catalogue.body.frames) {
  assert.equal(frame.sha256, sha(frame.file), `body frame ${frame.frame} hash changed`)
  const image = png(frame.file)
  assert.deepEqual([image.width, image.height], [256, 320])
  assert.equal(edgeAlphaCount(image), 0, `body frame ${frame.frame} touches a cell edge`)
  assert.ok(frame.transparentGutterPx >= 4, `body frame ${frame.frame} lacks a four-pixel gutter`)
  assert.equal(frame.floorY, 315)
  const masks = components.map((name) => {
    const record = frame.componentMasks[name]
    assert.equal(record.sha256, sha(record.file), `body frame ${frame.frame} ${name} mask changed`)
    const mask = png(record.file)
    assert.deepEqual([mask.width, mask.height], [256, 320])
    return mask
  })
  let unowned = 0; let multiplyOwned = 0
  for (let y = 0; y < 320; y += 1) for (let x = 0; x < 256; x += 1) {
    const visible = px(image, x, y)[3] > 0
    // Ownership masks are grayscale PNGs: membership is the sample value, not their fully opaque PNG container alpha.
    const owners = masks.reduce((sum, mask) => sum + (px(mask, x, y)[0] > 0 ? 1 : 0), 0)
    if (visible && owners === 0) unowned += 1
    if (owners > 1) multiplyOwned += 1
    if (!visible) assert.equal(owners, 0, `frame ${frame.frame} has ownership outside visible pixels`)
  }
  assert.equal(unowned, 0, `body frame ${frame.frame} contains unowned pixels`)
  assert.equal(multiplyOwned, 0, `body frame ${frame.frame} contains multiply-owned pixels`)
  assert.deepEqual(frame.ownership, { unownedVisiblePixels: 0, multiplyOwnedVisiblePixels: 0 })
  for (const name of components) {
    const evidence = frame.colourEvidence[name]
    assert.equal(evidence.status, 'pass', `body frame ${frame.frame} ${name} colour registration failed`)
    assert.equal(evidence.authoritySha256, rearHash)
    assert.equal(evidence.visibleRgbFromExactAuthority, true)
    assert.ok(evidence.regionalLumaDelta.median <= 2)
    assert.ok(evidence.regionalLumaDelta.p25 <= 4)
    assert.ok(evidence.regionalLumaDelta.p75 <= 4)
  }
}

assert.equal(catalogue.body.strip.sha256, sha(catalogue.body.strip.file))
const strip = png(catalogue.body.strip.file)
assert.deepEqual([strip.width, strip.height], [24 * 256, 320])
catalogue.body.frames.forEach((frame, i) => {
  const source = png(frame.file)
  for (let y = 0; y < 320; y += 1) {
    const actual = strip.data.subarray((y * strip.width + i * 256) * 4, (y * strip.width + (i + 1) * 256) * 4)
    const expected = source.data.subarray(y * 256 * 4, (y + 1) * 256 * 4)
    assert.ok(actual.equals(expected), `strip cell ${i + 1} differs from its source frame`)
  }
})

assert.equal(catalogue.callouts.fps, 8)
assert.equal(catalogue.callouts.frames, 42)
assert.equal(catalogue.callouts.durationSeconds, 5.25)
assert.deepEqual(Object.keys(catalogue.callouts.styles), ['fan', 'cloud'])
assert.equal(catalogue.callouts.styles.fan.status, 'equal review candidate')
assert.equal(catalogue.callouts.styles.cloud.status, 'equal review candidate')
assert.equal(catalogue.callouts.styleApproved, null)
assert.deepEqual(Object.keys(catalogue.callouts.envelopeEffects), ['swirls', 'flicks'])
assert.deepEqual(Object.keys(catalogue.callouts.phrases), ['cooking', 'mixing', 'washing', 'repair'])
assert.equal(catalogue.callouts.phrases.mixing.family, 'mixing-washing')
assert.equal(catalogue.callouts.phrases.washing.family, 'mixing-washing')
for (const [name, phrase] of Object.entries(catalogue.callouts.phrases)) {
  assert.equal(phrase.frames.length, 42, `${name} must have a 42-frame independent callout phrase`)
  assert.ok(phrase.frames.slice(36).every((frame) => frame.components.length === 0), `${name} must settle to quiet final frames`)
  assert.ok(phrase.frames.some((frame) => frame.components.some((part) => part.role === 'primary')), `${name} lacks a main icon`)
  assert.ok(phrase.frames.some((frame) => frame.components.some((part) => part.role === 'helper')), `${name} lacks helper icons`)
}
for (const [name, record] of Object.entries(register.candidate.calloutComponents)) {
  assert.equal(record.sha256, sha(record.file), `${name} callout hash changed`)
  const image = png(record.file); const cellWidth = name === 'puff' ? 128 : 96
  assert.equal(image.width, cellWidth * record.frames.length)
  assert.equal(image.height, 96)
  record.frames.forEach((frame, index) => {
    assert.equal(edgeAlphaCount(image, index * cellWidth, cellWidth), 0, `${name} cell ${index + 1} touches a shared edge`)
    assert.equal(frame.edgeAlphaPixels, 0)
    assert.ok(frame.transparentGutterPx >= 4)
  })
}
for (const [style, record] of Object.entries(register.candidate.calloutContactSheets)) {
  assert.equal(record.sha256, sha(record.file), `${style} contact sheet changed`)
  assert.deepEqual(record.sampleFrames, [1, 4, 8, 15, 22, 29, 33, 38])
}
for (const phrase of ['cooking', 'mixing', 'washing', 'repair']) {
  assert.ok(catalogue.sfx[phrase].length > 0)
  assert.ok(catalogue.sfx[phrase].every((cue) => ['activity-beat', 'asset-state', 'completion'].includes(cue.kind)))
}

assert.equal(catalogue.route.length, 72)
assert.equal(catalogue.contextLayer.position, 'behind Keeper')
assert.equal(catalogue.contextLayer.separate, true)
assert.deepEqual(catalogue.route.reduce((result, frame) => ({ ...result, [frame.phase]: (result[frame.phase] || 0) + 1 }), {}), {
  'approved walk': 16, 'approved deceleration': 4, 'approved turn away': 8, 'Prime rear-work action': 24,
  'approved reverse turn': 8, 'approved acceleration': 4, 'approved walk away': 8,
})
assert.deepEqual(catalogue.route.map((frame) => frame.phase), [
  ...Array(16).fill('approved walk'), ...Array(4).fill('approved deceleration'), ...Array(8).fill('approved turn away'),
  ...Array(24).fill('Prime rear-work action'), ...Array(8).fill('approved reverse turn'),
  ...Array(4).fill('approved acceleration'), ...Array(8).fill('approved walk away'),
])
assert.equal(catalogue.route[27].authoritySha256, rearHash, 'approved turn must land on the exact rear endpoint')
assert.equal(catalogue.route[28].candidateSha256, rearHash, 'action F1 must receive the exact turn endpoint')
assert.equal(catalogue.route[27].src, catalogue.route[28].src, 'turn/action seam must use the same content-addressed bytes')
assert.deepEqual(catalogue.route.slice(28, 52).map((frame) => frame.actionFrame), Array.from({ length: 24 }, (_, i) => i + 1))
assert.ok(catalogue.route.slice(20, 60).every((frame) => frame.x === 374 && frame.dx === 0), 'turn/action/reverse-turn root must remain fixed')
assert.equal(catalogue.route[51].candidateSha256, rearHash, 'action F24 must return the exact rear endpoint')
assert.equal(catalogue.route[52].authoritySha256, catalogue.route[26].authoritySha256, 'departure must continue with the exact reverse turn F8')
for (const frame of catalogue.route) assert.ok(register.candidate.publishedAssets.some((asset) => asset.url === frame.src), `route URL not published: ${frame.src}`)
for (const asset of register.candidate.publishedAssets) {
  assert.equal(asset.sourceSha256, sha(asset.source), `published source changed: ${asset.source}`)
  assert.equal(asset.publicSha256, sha(asset.public), `published/archive object changed: ${asset.public}`)
  assert.equal(asset.sourceSha256, asset.publicSha256)
}

for (const [name, value] of Object.entries(register.checks)) assert.equal(value, name === 'kitchenWorkChanged' ? false : true, `${name} changed`)
for (const value of Object.values(register.approvalBoundary)) assert.equal(value, false, 'review candidate was promoted or approved')
for (const token of ['Critical seam gate', 'walk → stop → turn', '24 authored frames', '42 frames', 'Bubble-free fan', 'Cloud / puff', 'equal review candidates', 'Cooking', 'Mixing', 'Washing', 'Generic repair', 'Keeper', 'Envelope effects', 'Icons', 'Rear furniture', 'Mute SFX', 'Reduced motion', 'img.decode', 'Promise.all']) assert.ok(page.includes(token), `review page missing ${token}`)

// The normalisation contract requires the corrected rear palette behaviour, not the rejected V1 readings.
const backV1 = json('art/drafts/keeper-prime-sit-stand-back-2026-10-18-v1/batch-register.json')
const backV2 = json('art/drafts/keeper-prime-sit-stand-back-2026-10-18-v2/batch-register.json')
assert.ok(backV1.candidate.frames.slice(1, 6).every((frame) => frame.paletteRegistration.components.uniformBlue.outputMedianLuma <= 74))
assert.ok(backV2.candidate.frames.slice(1, 6).every((frame) => frame.paletteRegistration.prior.jumperCore.medianLuma <= 74))
assert.ok(backV2.candidate.frames.slice(1, 6).every((frame) => frame.paletteRegistration.corrected.jumperCore.medianLuma >= 94))
assert.ok(backV2.candidate.frames.slice(1, 6).every((frame) => frame.paletteRegistration.corrected.trouserCore.medianLuma >= 77))
assert.ok(catalogue.body.frames.every((frame) => frame.colourEvidence.jumperBlue.candidate.medianLuma >= 92))
assert.ok(catalogue.body.frames.every((frame) => frame.colourEvidence.trousers.candidate.medianLuma >= 75))

console.log('Keeper Prime rear-work/activity-callout V1 verified: 24 authored body frames, exact protected endpoints, disjoint ownership, safe gutters, V2 palette behaviour, four independent callout phrases and no promotion.')
