#!/usr/bin/env node
/** Verify the immutable Prime held-implement motion-feasibility POC V1. */
import assert from 'node:assert/strict'
import crypto from 'node:crypto'
import fs from 'node:fs'
import path from 'node:path'
import { PNG } from 'pngjs'

const root = path.resolve(import.meta.dirname, '..')
const pack = 'art/drafts/keeper-prime-upper-body-override-poc-2026-10-19-v1'
const set = 'keeper-prime-upper-body-override-poc-v1'
const read = file => JSON.parse(fs.readFileSync(path.join(root, file), 'utf8'))
const bytes = file => fs.readFileSync(path.join(root, file))
const sha = file => crypto.createHash('sha256').update(bytes(file)).digest('hex')
const png = file => PNG.sync.read(bytes(file))

const register = read(`${pack}/batch-register.json`)
const data = read(`${pack}/${set}.json`)
const reviewer = fs.readFileSync(path.join(root, pack, 'reviewer.html'), 'utf8')
const shell = fs.readFileSync(path.join(root, `public/keeper-review/${set}/index.html`), 'utf8')

assert.equal(register.set, set)
assert.equal(register.status, 'prime-upper-body-override-poc-awaiting-frank')
assert.equal(register.supersedes.set, 'keeper-prime-sweep-broom-v8')
assert.equal(register.supersedes.status, 'rejected-provenance')
assert.equal(data.set, set)
assert.equal(data.status, 'versioned-reversible-proof-of-concept-not-approved')
for (const value of Object.values(register.approvalBoundary)) assert.equal(value, false)
assert.equal(register.construction.method, 'phase-matched full-character proxy; never overlay held limbs on the complete authority')
assert.equal(register.construction.headLockedToExactAuthority, false)
assert.equal(register.construction.lowerBodyLockedToExactAuthority, false)
assert.equal(register.construction.propPixels, 0)

for (const authority of register.authorities.approvedWalkV6) assert.equal(sha(authority.file), authority.sha256)
for (const authority of register.authorities.approvedTurnV9) assert.equal(sha(authority.file), authority.sha256)
for (const key of ['primeRig', 'requestedGripReference', 'generatedTurnSource']) {
  assert.equal(sha(register.authorities[key].file), register.authorities[key].sha256)
}

const frames = register.candidate.frames
assert.equal(frames.length, 17)
const walks = frames.filter(frame => frame.kind === 'approved-walk-v6-upper-body-override')
const turns = frames.filter(frame => frame.kind === 'approved-turn-v9-upper-body-override')
assert.deepEqual(walks.map(frame => frame.gaitFrame), [1,2,3,4,5,6,7,8])
assert.deepEqual(turns.map(frame => frame.turnFrame), [1,2,3,4,5,6,7,8,9])
assert.deepEqual(turns.map(frame => frame.angleDegrees), [90,98,105,120,135,150,165,172.5,180])
assert.ok(walks.every(frame => frame.durationMs === 125))
assert.ok(turns.every(frame => Math.abs(frame.durationMs - 1000 / 9) < 0.00001))
assert.deepEqual(walks.map(frame => frame.hands.visibleComponentCount), [2,2,2,2,2,2,2,2])
assert.deepEqual(turns.map(frame => frame.hands.visibleComponentCount), [2,2,2,2,2,2,2,0,0])

for (const frame of frames) {
  for (const key of ['candidate', 'registeredSource', 'upperBodyOverride', 'headLock', 'gripGuide']) {
    assert.equal(sha(frame[key].file), frame[key].sha256, `${frame.id} ${key} hash`)
  }
  const image = png(frame.candidate.file)
  assert.deepEqual([image.width, image.height], [384, 320], `${frame.id} geometry`)
  assert.equal(frame.candidate.edgeAlphaPixels, 0, `${frame.id} edge alpha`)
  assert.ok(frame.candidate.transparentGutterPx >= 4, `${frame.id} gutter`)
  assert.ok(frame.hands.visibleComponentCount <= 2, `${frame.id} hand ceiling`)
  assert.equal(frame.colourEvidence.nonAuthorityRgbPixels, 0, `${frame.id} palette provenance`)
  assert.equal(frame.ownership.propPixels, 0, `${frame.id} prop isolation`)
  assert.equal(frame.ownership.separatePropExpectedLater, true)
  assert.equal(frame.upperBodyOverride.pocConstraint, 'phase-matched full-character proxy; not pixel-identical authority')
  assert.equal(frame.upperBodyOverride.audit.changedOutsideOverride, 0)
}

assert.equal(data.route.length, 33)
assert.deepEqual(data.route.slice(0, 8).map(frame => frame.recordId), [1,2,3,4,5,6,7,8].map(i => `walk${i}`))
assert.deepEqual(data.route.slice(8, 25).map(frame => frame.recordId), [1,2,3,4,5,6,7,8,9,8,7,6,5,4,3,2,1].map(i => `turn${i}`))
assert.deepEqual(data.route.slice(25).map(frame => frame.recordId), [1,2,3,4,5,6,7,8].map(i => `walk${i}`))
assert.ok(data.route.slice(0, 8).every(frame => frame.mirror === false && frame.durationMs === 125))
assert.ok(data.route.slice(8, 17).every(frame => frame.mirror === false))
assert.ok(data.route.slice(17, 25).every(frame => frame.mirror === true))
assert.ok(data.route.slice(25).every(frame => frame.mirror === true && frame.durationMs === 125))
const rightRoots = data.route.slice(0, 8).map(frame => frame.rootXLp)
const leftRoots = data.route.slice(25).map(frame => frame.rootXLp)
for (let i = 1; i < rightRoots.length; i++) assert.ok(Math.abs(rightRoots[i] - rightRoots[i - 1] - 2.625) < 0.001)
for (let i = 1; i < leftRoots.length; i++) assert.ok(Math.abs(leftRoots[i - 1] - leftRoots[i] - 2.625) < 0.001)

for (const asset of register.publishedAssets) assert.equal(sha(asset.source), asset.sourceSha256)
for (const token of [
  'motion feasibility, not production art', 'No broom', 'Two-hand shaft grip',
  'Large inspection · 6 px/lp', 'Gameplay scale · 4 px/lp', 'Literal 1× · 1 px/lp',
  'Previous-frame ghost', 'Grip-axis overlay', 'Loading and decoding every unique frame', 'img.decode',
  'phase-matched proxies', 'separable Prime torso/arm layers'
]) assert.ok(reviewer.includes(token), `reviewer omits ${token}`)

assert.match(shell, /lighthouse-keeper\/[0-9a-f]{8,40}\/art\/drafts\/keeper-prime-upper-body-override-poc-2026-10-19-v1\/reviewer\.html/)
assert.doesNotMatch(shell, /__POC_COMMIT__|\/main\/art\/drafts/)

console.log('Prime held-implement POC V1 verified: 8 alternating gait phases, 9 approved turn angles, two-hand ceiling, no prop pixels, authority-derived palette, transparent gutters, and an explicit non-production approval boundary.')
