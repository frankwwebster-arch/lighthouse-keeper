#!/usr/bin/env node
/** Deterministically verify the immutable Prime sweep-broom V6 review set. */
import assert from 'node:assert/strict'
import crypto from 'node:crypto'
import fs from 'node:fs'
import path from 'node:path'
import { PNG } from 'pngjs'

const root = path.resolve(import.meta.dirname, '..')
const pack = 'art/drafts/keeper-prime-sweep-broom-2026-10-18-v6'
const read = name => JSON.parse(fs.readFileSync(path.join(root, name), 'utf8'))
const bytes = name => fs.readFileSync(path.join(root, name))
const sha = name => crypto.createHash('sha256').update(bytes(name)).digest('hex')
const png = name => PNG.sync.read(bytes(name))
const register = read(`${pack}/batch-register.json`)
const route = read(`${pack}/keeper-prime-sweep-broom-v6.json`)
const page = fs.readFileSync(path.join(root, 'public/keeper-review/keeper-prime-sweep-broom-v6/index.html'), 'utf8')
const reviewer = fs.readFileSync(path.join(root, `${pack}/reviewer.html`), 'utf8')

const materialPredicates = {
  jumperBlue: ([r, g, b]) => b > 105 && b > r + 35 && b > g + 12,
  trouserNavy: ([r, g, b]) => b > 45 && b <= 185 && b > r * 1.04 && b > g * .82 && r < 145 && g < 150,
  skin: ([r, g, b]) => r > 175 && g > 72 && b > 38 && r > g + 34 && b < g * .88,
  cream: ([r, g, b]) => r > 150 && g > 135 && b > 105 && r - g < 72 && g - b < 82,
}
const pixelsFor = (image, predicate) => {
  const values = []
  for (let offset = 0; offset < image.data.length; offset += 4) {
    if (!image.data[offset + 3]) continue
    const rgb = [image.data[offset], image.data[offset + 1], image.data[offset + 2]]
    if (predicate(rgb)) values.push(rgb)
  }
  return values
}
const envelopeFor = (files, predicate) => {
  const values = files.flatMap(file => pixelsFor(png(file), predicate))
  assert.ok(values.length > 100, 'authority material sample must be substantial')
  const envelope = [[255, 0], [255, 0], [255, 0]]
  for (const rgb of values) for (let channel = 0; channel < 3; channel++) {
    envelope[channel][0] = Math.min(envelope[channel][0], rgb[channel])
    envelope[channel][1] = Math.max(envelope[channel][1], rgb[channel])
  }
  return envelope
}
const assertEveryPixelInEnvelope = (image, predicate, envelope, label, tolerance = 36) => {
  const values = pixelsFor(image, predicate)
  assert.ok(values.length > 25, `${label} material must be visibly present`)
  for (const rgb of values) for (let channel = 0; channel < 3; channel++) {
    assert.ok(rgb[channel] >= envelope[channel][0] - tolerance && rgb[channel] <= envelope[channel][1] + tolerance,
      `${label} pixel ${rgb.join(',')} outside exact-authority envelope`)
  }
}

assert.equal(register.set, 'keeper-prime-sweep-broom-v6')
assert.equal(register.status, 'prime-sweep-broom-v6-awaiting-frank')
assert.equal(register.supersedes.set, 'keeper-prime-sweep-broom-v5')
assert.equal(register.supersedes.status, 'rejected-provenance')
assert.equal(route.status, 'versioned-reversible-review-candidate-not-approved')
assert.equal(register.approvalBoundary.candidateApproved, false)
assert.equal(register.approvalBoundary.promotionAllowed, false)
assert.equal(register.approvalBoundary.productionChanged, false)
assert.equal(register.approvalBoundary.runtimeChanged, false)

for (const source of Object.values(register.sources)) assert.equal(sha(source.file), source.sha256)
for (const frame of register.candidate.frames) {
  const layers = {}
  for (const part of ['actor', 'prop', 'composite']) {
    assert.equal(sha(frame[part].file), frame[part].sha256, `${frame.id} ${part} hash`)
    layers[part] = png(frame[part].file)
    assert.deepEqual([layers[part].width, layers[part].height], [384, 320])
  }
  assert.equal(frame.composite.edgeAlphaPixels, 0, `${frame.id} shared-edge alpha`)
  assert.ok(frame.composite.transparentGutterPx >= 4, `${frame.id} transparent gutter`)
  assert.equal(frame.ownership.partitionExact, true)
  assert.equal(frame.ownership.multiplyOwnedPixels, 0)
  assert.equal(frame.ownership.unownedVisiblePixels, 0)
  for (let offset = 0; offset < layers.composite.data.length; offset += 4) {
    const actorAlpha = layers.actor.data[offset + 3]
    const propAlpha = layers.prop.data[offset + 3]
    assert.ok(!(actorAlpha && propAlpha), `${frame.id} multiply-owned pixel`)
    const owner = propAlpha ? layers.prop : layers.actor
    for (let channel = 0; channel < 4; channel++) {
      assert.equal(owner.data[offset + channel], layers.composite.data[offset + channel], `${frame.id} recomposition pixel`)
    }
  }
  if (/^(hold|sweep|turn)/.test(frame.id)) {
    if (['turn8', 'turn9'].includes(frame.id)) {
      assert.equal(frame.broomHandContact.status, 'occluded-carried')
      assert.equal(frame.broomHandContact.contactPixels, 0)
    } else {
      assert.equal(frame.broomHandContact.status, 'pass')
      assert.ok(frame.broomHandContact.contactPixels >= 8, `${frame.id} visible grip contact`)
    }
    assert.ok(frame.prop.bounds.minY >= 110, `${frame.id} prop must not claim cap/face pixels`)
  }
}

assert.equal(register.broomReplicationContract.type, 'traditional rigid-stock broom (not a mop or fan broom)')
assert.deepEqual(register.broomReplicationContract.registeredCellPx, [384, 320])
assert.deepEqual(register.broomReplicationContract.gameplayCellLp, [48, 40])
assert.equal(register.broomReplicationContract.pxPerLp, 8)
assert.equal(sha(register.broomReplicationContract.authority.file), register.broomReplicationContract.authority.sha256)
assert.equal(Object.keys(register.broomReplicationContract.perFramePropBoundsPx).length, 18)
const turns = Array.from({ length: 9 }, (_, index) => register.candidate.frames.find(frame => frame.id === `turn${index + 1}`))
for (const frame of turns) assert.ok(frame.prop.bounds, `${frame.id} must retain a separately owned visible broom`)
const rear = turns.at(-1)
const rearActorCentre = (rear.actor.bounds.minX + rear.actor.bounds.maxX) / 2
assert.ok(rear.prop.bounds.minX <= rearActorCentre && rear.prop.bounds.maxX >= rearActorCentre,
  'rear-view broom must remain on the hidden front axis and overlap the Keeper centre, never park at his side')
for (let index = 1; index < turns.length; index++) {
  const priorCentre = (turns[index - 1].prop.bounds.minX + turns[index - 1].prop.bounds.maxX) / 2
  const centre = (turns[index].prop.bounds.minX + turns[index].prop.bounds.maxX) / 2
  assert.ok(Math.abs(centre - priorCentre) <= 75, `${turns[index].id} broom continuity jump`)
}

assert.equal(route.route.length, 67)
assert.deepEqual(route.route.slice(0, 8).map(frame => frame.phase), Array(8).fill('approved standard walk into cupboard'))
assert.deepEqual(route.route.slice(-8).map(frame => frame.phase), Array(8).fill('approved standard walk out of cupboard'))
assert.equal(route.route.filter(frame => frame.phase === 'walking sweep outward').length, 16)
assert.equal(route.route.filter(frame => frame.phase === 'walking sweep return').length, 16)
assert.equal(new Set(route.route.filter(frame => frame.phase.startsWith('walking sweep')).map(frame => frame.recordId)).size, 8)
const turnRoute = route.route.filter(frame => frame.phase === 'held-broom core reversal')
assert.equal(turnRoute.length, 17)
assert.deepEqual(turnRoute.map(frame => frame.recordId), [
  'turn1', 'turn2', 'turn3', 'turn4', 'turn5', 'turn6', 'turn7', 'turn8', 'turn9',
  'turn8', 'turn7', 'turn6', 'turn5', 'turn4', 'turn3', 'turn2', 'turn1',
])
assert.deepEqual(turnRoute.map(frame => frame.mirror), [...Array(9).fill(true), ...Array(8).fill(false)])
for (const frame of route.route.filter(frame => frame.phase.startsWith('approved standard walk'))) assert.equal(frame.durationMs, 150)
for (const frame of route.route.filter(frame => frame.phase.startsWith('walking sweep'))) assert.equal(frame.durationMs, 220)
assert.deepEqual(turnRoute.map(frame => frame.durationMs), [270, ...Array(7).fill(180), 270, ...Array(7).fill(180), 270])
for (const frame of route.route.filter(frame => frame.phase === 'fully obscured state swap')) assert.equal(frame.durationMs, 300)
for (const frame of route.route.filter(frame => /sweep|reversal/.test(frame.phase))) {
  assert.equal(frame.actorRootXLp, frame.propRootXLp, `${frame.label} actor/prop root drift`)
}

const sweepFrames = Array.from({ length: 8 }, (_, index) => register.candidate.frames.find(frame => frame.id === `sweep${index + 1}`))
assert.equal(new Set(sweepFrames.map(frame => frame.composite.sha256)).size, 8, 'all eight sweep drawings must be distinct')
assert.equal(new Set(sweepFrames.map(frame => {
  const image = png(frame.composite.file)
  return crypto.createHash('sha256').update(image.data.subarray(220 * image.width * 4)).digest('hex')
})).size, 8, 'all eight lower-body/boot silhouettes must be distinct')
for (let index = 0; index < sweepFrames.length; index++) {
  assert.equal(sha(sweepFrames[index].legAuthority.file), sweepFrames[index].legAuthority.sha256)
  assert.equal(sweepFrames[index].gait.cycleFrame, index + 1)
}

// Per-pixel material verification: each visible material pixel in every new
// sweep and turn actor is checked against colour envelopes derived from the
// exact approved Walk V6 frame set, never against a whole-garment average.
const primeAuthorityFiles = register.authorities.approvedWalkV6.frameSha256.map((_, index) =>
  `art/drafts/keeper-prime-walk-2026-10-14-v6/drafts/frames/keeper_prime_walk-right_f${index + 1}.png`)
const primeEnvelopes = Object.fromEntries(Object.entries(materialPredicates).map(([name, predicate]) => [name, envelopeFor(primeAuthorityFiles, predicate)]))
for (const frame of [...sweepFrames, ...turns]) {
  const actor = png(frame.actor.file)
  for (const [name, predicate] of Object.entries(materialPredicates)) {
    assertEveryPixelInEnvelope(actor, predicate, primeEnvelopes[name], `${frame.id} ${name}`)
  }
}
const broomPredicate = ([r, g, b]) => r > 70 && g > 25 && r > g * 1.06 && b < g * .92
const broomEnvelope = envelopeFor([register.broomReplicationContract.authority.file], broomPredicate)
for (const frame of [register.candidate.frames.find(frame => frame.id === 'hold'), ...sweepFrames, ...turns]) {
  assertEveryPixelInEnvelope(png(frame.prop.file), broomPredicate, broomEnvelope, `${frame.id} broom material`, 44)
}
for (const handoff of route.route.filter(frame => frame.phase === 'fully obscured state swap')) {
  const { door, unit } = handoff.doorCoverage
  assert.ok(door[0] <= unit[0] && door[1] >= unit[1], 'door must physically cover full registered unit')
}

for (const asset of register.publishedAssets) assert.equal(sha(asset.source), asset.sourceSha256)
for (const token of ['Large inspection · 6 px/lp', 'Gameplay scale · 4 px/lp', 'Literal 1× · 1 px/lp', 'Previous-frame ghost', 'Loading and decoding every unique frame', 'img.decode', 'door fully covers Keeper and broom', 'walk 150 ms', 'sweeping step 220 ms', 'turn 180 ms']) assert.ok(reviewer.includes(token), token)
assert.doesNotMatch(reviewer, /keeper-prime-sweep-broom-v3\/assets/)
assert.match(page, /__V6_COMMIT__/)
console.log('Prime sweep-broom V6 verified: eight distinct walking-sweep cells, slower authored cadence, seventeen-frame front-held reversal with centred rear occlusion, rigid stock broom, exact actor/prop recomposition, physical cupboard occlusion, no promotion.')
