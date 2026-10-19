#!/usr/bin/env node
/** Verify the immutable Prime sweep-broom V7 movement candidate. */
import assert from 'node:assert/strict'
import crypto from 'node:crypto'
import fs from 'node:fs'
import path from 'node:path'
import { PNG } from 'pngjs'

const root = path.resolve(import.meta.dirname, '..')
const pack = 'art/drafts/keeper-prime-sweep-broom-2026-10-18-v7'
const read = name => JSON.parse(fs.readFileSync(path.join(root, name), 'utf8'))
const bytes = name => fs.readFileSync(path.join(root, name))
const sha = name => crypto.createHash('sha256').update(bytes(name)).digest('hex')
const png = name => PNG.sync.read(bytes(name))
const register = read(`${pack}/batch-register.json`)
const route = read(`${pack}/keeper-prime-sweep-broom-v7.json`)
const reviewer = fs.readFileSync(path.join(root, pack, 'reviewer.html'), 'utf8')
const shell = fs.readFileSync(path.join(root, 'public/keeper-review/keeper-prime-sweep-broom-v7/index.html'), 'utf8')

assert.equal(register.set, 'keeper-prime-sweep-broom-v7')
assert.equal(register.status, 'prime-sweep-broom-v7-movement-awaiting-frank')
assert.equal(register.supersedes.set, 'keeper-prime-sweep-broom-v6')
assert.equal(register.supersedes.status, 'rejected-provenance')
assert.equal(route.status, 'versioned-reversible-movement-candidate-not-approved')
assert.equal(register.approvalBoundary.movementApproved, false)
assert.equal(register.approvalBoundary.broomArtApproved, false)
assert.equal(register.approvalBoundary.productionPromotionAllowed, false)
assert.equal(register.approvalBoundary.productionChanged, false)
assert.equal(register.approvalBoundary.runtimeChanged, false)
assert.equal(register.movementContract.walkCellsByteIdenticalOutsideArmCorridor, true)

for (const authority of register.authorities.approvedWalkV6) assert.equal(sha(authority.file), authority.sha256)
for (const authority of register.authorities.approvedTurnV9) assert.equal(sha(authority.file), authority.sha256)
assert.equal(sha(register.authorities.exactSideRightNeutral.file), register.authorities.exactSideRightNeutral.sha256)
assert.equal(sha(register.armSource.file), register.armSource.sha256)
for (const cutout of register.armSource.cutouts) assert.equal(sha(cutout.file), cutout.sha256)
assert.equal(sha(register.broom.authority.file), register.broom.authority.sha256)

const gaitNames = ['left-foot contact', 'left-foot down', 'left-foot passing', 'left-foot up',
  'right-foot contact', 'right-foot down', 'right-foot passing', 'right-foot up']
const sweeps = register.candidate.frames.filter(frame => frame.kind === 'approved-walk-with-sweep3-grip')
const turns = register.candidate.frames.filter(frame => frame.kind === 'approved-turn-v9-with-carrying-arms')
assert.deepEqual(sweeps.map(frame => frame.gaitFrame), [1, 2, 3, 4, 5, 6, 7, 8])
assert.deepEqual(sweeps.map(frame => frame.gaitPhase), gaitNames)
assert.equal(new Set(sweeps.map(frame => frame.actor.sha256)).size, 8, 'all eight gait cells must remain distinct')
assert.equal(new Set(sweeps.map(frame => frame.prop.sha256)).size, 1, 'walk broom layer must be byte-identical in all eight gait cells')
assert.deepEqual(turns.map(frame => frame.turnFrame), [1, 2, 3, 4, 5, 6, 7, 8, 9])
assert.deepEqual(turns.map(frame => frame.angleDegrees), [90, 98, 105, 120, 135, 150, 165, 172.5, 180])

for (const frame of [...sweeps, ...turns]) {
  for (const part of ['actor', 'prop', 'composite']) {
    assert.equal(sha(frame[part].file), frame[part].sha256, `${frame.id} ${part} hash`)
    const image = png(frame[part].file)
    assert.deepEqual([image.width, image.height], [384, 320], `${frame.id} ${part} geometry`)
  }
  assert.equal(frame.composite.edgeAlphaPixels, 0, `${frame.id} shared-edge alpha`)
  assert.ok(frame.composite.transparentGutterPx >= 4, `${frame.id} transparent gutter`)
  assert.equal(frame.ownership.separateLayers, true)
  assert.deepEqual(frame.ownership.renderOrder, ['prop', 'actor'])
  assert.equal(frame.ownership.recompositionExact, true)
  assert.equal(frame.armCorridor.audit.changedOutsideArmCorridor, 0, `${frame.id} may change only its arm corridor`)
  const actor = png(frame.actor.file), prop = png(frame.prop.file), composite = png(frame.composite.file)
  for (let offset = 0; offset < composite.data.length; offset += 4) {
    const aa = actor.data[offset + 3] / 255
    const pa = prop.data[offset + 3] / 255
    const outA = aa + pa * (1 - aa)
    const expected = [0, 0, 0, Math.round(outA * 255)]
    if (outA) for (let channel = 0; channel < 3; channel++) {
      expected[channel] = Math.round((actor.data[offset + channel] * aa + prop.data[offset + channel] * pa * (1 - aa)) / outA)
    }
    for (let channel = 0; channel < 4; channel++) {
      assert.ok(Math.abs(composite.data[offset + channel] - expected[channel]) <= 1, `${frame.id} recomposition pixel`)
    }
  }
  if (frame.turnFrame >= 8) assert.equal(frame.broomHandContactPixels, 0)
  else assert.ok(frame.broomHandContactPixels >= 100, `${frame.id} visible grip contact`)
}

assert.equal(route.route.length, 85)
const phases = name => route.route.filter(frame => frame.phase === name)
const walkIn = phases('approved standard walk into cupboard')
const sweepLeft = phases('approved walking gait while sweeping left')
const reversal = phases('exact approved V9 reversal while carrying broom')
const sweepRight = phases('approved walking gait while sweeping right')
const walkAway = phases('approved standard walk away from cupboard')
const expectedTwoCycles = [1,2,3,4,5,6,7,8,1,2,3,4,5,6,7,8]
assert.deepEqual(walkIn.map(frame => frame.gaitFrame), expectedTwoCycles)
assert.deepEqual(sweepLeft.map(frame => frame.gaitFrame), expectedTwoCycles)
assert.deepEqual(sweepRight.map(frame => frame.gaitFrame), expectedTwoCycles)
assert.deepEqual(walkAway.map(frame => frame.gaitFrame), expectedTwoCycles)
assert.ok(walkIn.every(frame => !frame.mirror && frame.durationMs === 125))
assert.ok(sweepLeft.every(frame => frame.mirror && frame.durationMs === 125))
assert.ok(sweepRight.every(frame => !frame.mirror && frame.durationMs === 125))
assert.ok(walkAway.every(frame => frame.mirror && frame.durationMs === 125))
assert.deepEqual(reversal.map(frame => frame.turnFrame), [1,2,3,4,5,6,7,8,9,8,7,6,5,4,3,2,1])
assert.ok(reversal.every(frame => Math.abs(frame.durationMs - 1000 / 9) < 0.00001))
assert.equal(phases('fully obscured standard-to-sweep swap').length, 1)
assert.equal(phases('fully obscured sweep-to-standard swap').length, 1)
assert.equal(phases('phase-correct stop at exact side-right neutral').length, 1)
assert.equal(phases('exact side-right neutral after action exit').length, 1)
for (const frame of [...phases('phase-correct stop at exact side-right neutral'), ...phases('exact side-right neutral after action exit')]) {
  assert.equal(frame.actorSrc, frame.authoritySrc)
  assert.equal(frame.mirror, false)
  assert.equal(frame.cupboard, 'closed')
}

const materialPredicates = {
  jumperBlue: ([r,g,b]) => b > 105 && b > r + 35 && b > g + 12,
  trouserNavy: ([r,g,b]) => b > 45 && b <= 190 && b > r * 1.02 && b > g * .78 && r < 150 && g < 155,
  skin: ([r,g,b]) => r > 170 && g > 68 && b > 35 && r > g + 30 && b < g * .95,
  cream: ([r,g,b]) => r > 145 && g > 125 && b > 95 && r - g < 80 && g - b < 90,
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
const envelopes = Object.fromEntries(Object.entries(materialPredicates).map(([name, predicate]) => {
  const values = register.authorities.approvedWalkV6.flatMap(authority => pixelsFor(png(authority.file), predicate))
  assert.ok(values.length > 100)
  return [name, [0,1,2].map(channel => [Math.min(...values.map(rgb => rgb[channel])), Math.max(...values.map(rgb => rgb[channel]))])]
}))
for (const frame of [...sweeps, ...turns]) for (const [name, predicate] of Object.entries(materialPredicates)) {
  const values = pixelsFor(png(frame.actor.file), predicate)
  assert.ok(values.length > 20, `${frame.id} ${name} visibility`)
  for (const rgb of values) for (let channel = 0; channel < 3; channel++) {
    assert.ok(rgb[channel] >= envelopes[name][channel][0] - 42 && rgb[channel] <= envelopes[name][channel][1] + 42,
      `${frame.id} ${name} pixel outside exact-authority envelope`)
  }
}

for (const asset of register.publishedAssets) assert.equal(sha(asset.source), asset.sourceSha256)
for (const token of ['Movement proof', 'Judge movement first', 'F1→F8', 'Large inspection · 6 px/lp',
  'Gameplay scale · 4 px/lp', 'Literal 1× · 1 px/lp', 'Previous-frame ghost',
  'Loading and decoding every unique frame', 'img.decode', 'data-layer=prop', 'data-layer=actor']) {
  assert.ok(reviewer.includes(token), `reviewer omits ${token}`)
}
assert.match(shell, /lighthouse-keeper\/[0-9a-f]{8}\/art\/drafts\/keeper-prime-sweep-broom-2026-10-18-v7\/reviewer\.html/)
assert.doesNotMatch(shell, /__V7_COMMIT__|\/main\/art\/drafts/)
assert.doesNotMatch(reviewer, /keeper-prime-sweep-broom-v6\/assets/)
console.log('Prime sweep-broom V7 verified: F1→F8 in both directions, exact 8 fps gait timing, exact V9 turn order/timing, stable separate walk prop, Sweep-3 grip, review-only delivery.')
