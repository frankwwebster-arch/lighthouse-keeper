#!/usr/bin/env node
/** Deterministically verify the immutable Prime sweep-broom V4 review set. */
import assert from 'node:assert/strict'
import crypto from 'node:crypto'
import fs from 'node:fs'
import path from 'node:path'
import { PNG } from 'pngjs'

const root = path.resolve(import.meta.dirname, '..')
const pack = 'art/drafts/keeper-prime-sweep-broom-2026-10-18-v4'
const read = name => JSON.parse(fs.readFileSync(path.join(root, name), 'utf8'))
const bytes = name => fs.readFileSync(path.join(root, name))
const sha = name => crypto.createHash('sha256').update(bytes(name)).digest('hex')
const png = name => PNG.sync.read(bytes(name))
const register = read(`${pack}/batch-register.json`)
const route = read(`${pack}/keeper-prime-sweep-broom-v4.json`)
const page = fs.readFileSync(path.join(root, 'public/keeper-review/keeper-prime-sweep-broom-v4/index.html'), 'utf8')
const reviewer = fs.readFileSync(path.join(root, `${pack}/reviewer.html`), 'utf8')

assert.equal(register.set, 'keeper-prime-sweep-broom-v4')
assert.equal(register.status, 'prime-sweep-broom-v4-awaiting-frank')
assert.equal(register.supersedes.set, 'keeper-prime-sweep-broom-v3')
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
    assert.equal(frame.broomHandContact.status, 'pass')
    assert.ok(frame.broomHandContact.contactPixels >= 8)
    assert.ok(frame.prop.bounds.minY >= 118, `${frame.id} prop must not claim cap/face pixels`)
  }
}

assert.equal(register.broomReplicationContract.type, 'traditional rigid-stock broom (not a mop or fan broom)')
assert.deepEqual(register.broomReplicationContract.registeredCellPx, [384, 320])
assert.deepEqual(register.broomReplicationContract.gameplayCellLp, [48, 40])
assert.equal(register.broomReplicationContract.pxPerLp, 8)
assert.equal(sha(register.broomReplicationContract.authority.file), register.broomReplicationContract.authority.sha256)
assert.equal(Object.keys(register.broomReplicationContract.perFramePropBoundsPx).length, 9)

assert.equal(route.route.length, 51)
assert.deepEqual(route.route.slice(0, 8).map(frame => frame.phase), Array(8).fill('approved standard walk into cupboard'))
assert.deepEqual(route.route.slice(-8).map(frame => frame.phase), Array(8).fill('approved standard walk out of cupboard'))
assert.equal(route.route.filter(frame => frame.phase === 'walking sweep outward').length, 12)
assert.equal(route.route.filter(frame => frame.phase === 'walking sweep return').length, 12)
assert.equal(new Set(route.route.filter(frame => frame.phase.startsWith('walking sweep')).map(frame => frame.recordId)).size, 3)
assert.equal(route.route.filter(frame => frame.phase === 'held-broom core reversal').length, 9)
for (const handoff of route.route.filter(frame => frame.phase === 'fully obscured state swap')) {
  const { door, unit } = handoff.doorCoverage
  assert.ok(door[0] <= unit[0] && door[1] >= unit[1], 'door must physically cover full registered unit')
}

for (const asset of register.publishedAssets) assert.equal(sha(asset.source), asset.sourceSha256)
for (const token of ['Large inspection · 6 px/lp', 'Gameplay scale · 4 px/lp', 'Literal 1× · 1 px/lp', 'Previous-frame ghost', 'Loading and decoding every unique frame', 'img.decode', 'door fully covers Keeper and broom']) assert.ok(reviewer.includes(token), token)
assert.doesNotMatch(reviewer, /keeper-prime-sweep-broom-v3\/assets/)
assert.match(page, /__V4_COMMIT__/)
console.log('Prime sweep-broom V4 verified: stock broom, isolated cells, moving-leg sweep, held-broom reversal, physical cupboard occlusion, exact actor/prop recomposition, no promotion.')
