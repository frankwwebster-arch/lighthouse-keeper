#!/usr/bin/env node
/** Verify the immutable Prime sweep-broom V8 exact-movement candidate. */
import assert from 'node:assert/strict'
import crypto from 'node:crypto'
import fs from 'node:fs'
import path from 'node:path'
import { PNG } from 'pngjs'

const root = path.resolve(import.meta.dirname, '..')
const pack = 'art/drafts/keeper-prime-sweep-broom-2026-10-19-v8'
const read = name => JSON.parse(fs.readFileSync(path.join(root, name), 'utf8'))
const bytes = name => fs.readFileSync(path.join(root, name))
const sha = name => crypto.createHash('sha256').update(bytes(name)).digest('hex')
const png = name => PNG.sync.read(bytes(name))
const register = read(`${pack}/batch-register.json`)
const data = read(`${pack}/keeper-prime-sweep-broom-v8.json`)
const reviewer = fs.readFileSync(path.join(root, pack, 'reviewer.html'), 'utf8')
const shell = fs.readFileSync(path.join(root, 'public/keeper-review/keeper-prime-sweep-broom-v8/index.html'), 'utf8')

assert.equal(register.set, 'keeper-prime-sweep-broom-v8')
assert.equal(register.status, 'prime-sweep-broom-v8-movement-awaiting-frank')
assert.equal(register.supersedes.set, 'keeper-prime-sweep-broom-v7')
assert.equal(register.supersedes.status, 'rejected-provenance')
assert.equal(data.status, 'versioned-reversible-movement-candidate-not-approved')
for (const value of Object.values(register.approvalBoundary)) assert.equal(value, false)

for (const group of ['approvedWalkV6', 'approvedTurnV9', 'approvedStopWalkV1']) {
  for (const authority of register.authorities[group]) assert.equal(sha(authority.file), authority.sha256)
}
assert.equal(sha(register.authorities.exactSideRightNeutral.file), register.authorities.exactSideRightNeutral.sha256)
assert.equal(sha(register.broom.authority.file), register.broom.authority.sha256)

const frames = register.candidate.frames
const walks = frames.filter(frame => frame.kind === 'approved-walk-v6-held-limb-edit')
const turns = frames.filter(frame => frame.kind === 'approved-turn-v9-held-limb-edit')
assert.deepEqual(walks.map(frame => frame.gaitFrame), [1,2,3,4,5,6,7,8])
assert.deepEqual(turns.map(frame => frame.turnFrame), [1,2,3,4,5,6,7,8,9])
assert.deepEqual(turns.map(frame => frame.angleDegrees), [90,98,105,120,135,150,165,172.5,180])

for (const frame of frames) {
  for (const part of ['actor', 'prop', 'composite']) {
    assert.equal(sha(frame[part].file), frame[part].sha256, `${frame.id} ${part} hash`)
    const image = png(frame[part].file)
    assert.deepEqual([image.width, image.height], [384, 320], `${frame.id} ${part} geometry`)
  }
  assert.equal(sha(frame.heldLimbMask.file), frame.heldLimbMask.sha256)
  assert.equal(frame.heldLimbMask.hardEdged, true)
  assert.equal(frame.heldLimbMask.audit.changedOutsideArmCorridor, 0)
  assert.equal(frame.composite.edgeAlphaPixels, 0)
  assert.ok(frame.composite.transparentGutterPx >= 4)
  assert.equal(frame.ownership.separateLayers, true)
  assert.deepEqual(frame.ownership.renderOrder, ['prop', 'actor'])

  const actor = png(frame.actor.file), base = png(frame.approvedBase.file), mask = png(frame.heldLimbMask.file)
  assert.deepEqual([actor.width, actor.height], [base.width, base.height])
  for (let p = 0; p < actor.width * actor.height; p++) {
    const offset = p * 4
    const owned = mask.data[offset + 3] || mask.data[offset]
    if (!owned) {
      for (let c = 0; c < 4; c++) assert.equal(actor.data[offset + c], base.data[offset + c], `${frame.id} outside-mask byte`)
    }
    const y = Math.floor(p / actor.width)
    if (y > frame.heldLimbMask.maxOwnedY) {
      assert.equal(owned, 0, `${frame.id} mask below held limbs`)
      for (let c = 0; c < 4; c++) assert.equal(actor.data[offset + c], base.data[offset + c], `${frame.id} lower-body authority byte`)
    }
  }
}

const phases = name => data.route.filter(frame => frame.phase === name)
const approach = phases('approved Walk V6 approach')
const depart = phases('approved Walk V6 departure')
const sweepLeft = phases('approved F1→F8 gait while sweeping left')
const sweepRight = phases('approved F1→F8 gait while sweeping right')
const turn = phases('approved Turn V9 reversal with held-limb-only edit')
assert.equal(approach.length, 49)
assert.equal(depart.length, 48)
assert.equal(sweepLeft.length, 32)
assert.equal(sweepRight.length, 32)
assert.equal(turn.length, 17)
assert.deepEqual(approach.slice(0, 48).map(frame => frame.gaitFrame), Array.from({length: 48}, (_, i) => i % 8 + 1))
assert.equal(approach.at(-1).gaitFrame, 1)
assert.deepEqual(depart.map(frame => frame.gaitFrame), Array.from({length: 48}, (_, i) => i % 8 + 1))
assert.deepEqual(sweepLeft.map(frame => frame.gaitFrame), Array.from({length: 32}, (_, i) => i % 8 + 1))
assert.deepEqual(sweepRight.map(frame => frame.gaitFrame), Array.from({length: 32}, (_, i) => i % 8 + 1))
assert.deepEqual(turn.map(frame => frame.turnFrame), [1,2,3,4,5,6,7,8,9,8,7,6,5,4,3,2,1])
assert.ok([...approach, ...depart, ...sweepLeft, ...sweepRight].every(frame => frame.durationMs === 125))
assert.ok(turn.every(frame => Math.abs(frame.durationMs - 1000/9) < 0.00001))

const deltas = sequence => sequence.slice(1).map((frame, i) => Math.abs(frame.actorRootXLp - sequence[i].actorRootXLp))
for (const delta of deltas(approach.slice(0, 49))) assert.ok(Math.abs(delta - 2.625) < 0.001)
for (const delta of deltas(depart)) assert.ok(Math.abs(delta - 2.625) < 0.001)
for (const delta of deltas(sweepLeft)) assert.ok(Math.abs(delta - 2.625) < 0.001)
for (const delta of deltas(sweepRight)) assert.ok(Math.abs(delta - 2.625) < 0.001)

const stop = phases('approved walk-to-stop bridge')
assert.equal(stop.length, 4)
assert.deepEqual(stop.map(frame => frame.label), ['exact reverse bridge F4','exact reverse bridge F3','exact reverse bridge F2','exact reverse bridge F1'])
assert.deepEqual(stop.map((frame, i) => Math.round((frame.actorRootXLp - (i ? stop[i-1].actorRootXLp : approach.at(-1).actorRootXLp)) * 8)), [18,12,6,2])
const start = phases('approved stop-to-walk bridge')
assert.equal(start.length, 5)
assert.deepEqual(start.map(frame => frame.label), ['exact mirrored stop F1','exact mirrored bridge F2','exact mirrored bridge F3','exact mirrored bridge F4','exact mirrored bridge F5'])
assert.deepEqual(start.slice(1).map((frame, i) => Math.round((start[i].actorRootXLp - frame.actorRootXLp) * 8)), [2,6,12,18])

const walkAuthorities = new Map(register.authorities.approvedWalkV6.map(item => [item.frame, item]))
for (const frame of [...approach, ...depart]) {
  const authority = walkAuthorities.get(frame.gaitFrame)
  assert.ok(frame.actorSrc.endsWith(`/review-archive/objects/${authority.sha256.slice(0,2)}/${authority.sha256}.png`))
  assert.equal(frame.actorSrc, frame.authoritySrc)
  assert.equal(frame.cellWidthLp, 32)
  assert.equal(frame.anchorXLp, 16)
}
for (const frame of [...phases('exact side-right neutral before hidden swap'), ...phases('exact side-right neutral after hidden swap')]) {
  assert.equal(frame.actorSrc, frame.authoritySrc)
  assert.equal(frame.mirror, false)
  assert.equal(frame.cupboard, 'closed')
}
assert.equal(phases('fully obscured standard-to-sweep swap').length, 1)
assert.equal(phases('fully obscured sweep-to-standard swap').length, 1)

for (const asset of register.publishedAssets) assert.equal(sha(asset.source), asset.sourceSha256)
for (const token of ['Exact movement correction', 'Judge movement only', 'F1→F8', '2.625 gameplay px/frame',
  'Large inspection · 6 px/lp', 'Gameplay scale · 4 px/lp', 'Literal 1× · 1 px/lp',
  'Previous-frame ghost', 'Loading and decoding every unique frame', 'img.decode', 'Owned limb pixels']) {
  assert.ok(reviewer.includes(token), `reviewer omits ${token}`)
}
assert.match(shell, /lighthouse-keeper\/[0-9a-f]{8}\/art\/drafts\/keeper-prime-sweep-broom-2026-10-19-v8\/reviewer\.html/)
assert.doesNotMatch(shell, /__V8_COMMIT__|\/main\/art\/drafts/)
console.log('Prime sweep-broom V8 verified: exact Walk V6 cadence/root motion, exact stop bridges, exact Turn V9 order, hard held-limb ownership, and byte-identical authority outside the declared mask.')
