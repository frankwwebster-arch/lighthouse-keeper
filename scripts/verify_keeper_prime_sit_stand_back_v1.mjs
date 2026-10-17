#!/usr/bin/env node

import assert from 'node:assert/strict'
import crypto from 'node:crypto'
import fs from 'node:fs'
import path from 'node:path'
import { PNG } from 'pngjs'

const root = path.resolve(import.meta.dirname, '..')
const abs = (file) => path.join(root, file)
const json = (file) => JSON.parse(fs.readFileSync(abs(file), 'utf8'))
const sha = (file) => crypto.createHash('sha256').update(fs.readFileSync(abs(file))).digest('hex')
const register = json('art/drafts/keeper-prime-sit-stand-back-2026-10-18-v1/batch-register.json')
const data = json('art/drafts/keeper-prime-sit-stand-back-2026-10-18-v1/keeper-prime-sit-stand-back-v1.json')
const page = fs.readFileSync(abs('src/app/keeper-review/keeper-prime-sit-stand-back-v1/route.ts'), 'utf8')

function alphaSha(file) {
  const png = PNG.sync.read(fs.readFileSync(abs(file)))
  const alpha = Buffer.alloc(png.width * png.height)
  for (let source = 3, target = 0; source < png.data.length; source += 4, target += 1) alpha[target] = png.data[source]
  return crypto.createHash('sha256').update(alpha).digest('hex')
}

assert.equal(register.set, 'keeper-prime-sit-stand-back-v1')
assert.equal(register.status, 'back-foreground-chair-v1-awaiting-frank')
assert.equal(data.status, 'reversible-back-review-candidate-not-approved')
assert.equal(data.route.length, 61)
assert.deepEqual(register.candidate.frames.map((frame) => frame.bounds.width), [155, 150, 150, 150, 150, 150])
assert.deepEqual(register.candidate.frames.map((frame) => frame.bounds.height), [298, 286, 276, 270, 266, 264])
assert.deepEqual(register.candidate.frames.slice(1).map((frame) => frame.elbowSpanPx), [150, 150, 150, 150, 150])

for (const approval of Object.values(register.authorities.pinnedApprovals)) {
  assert.equal(approval.sha256, sha(approval.file))
  assert.match(approval.decision, /^approved-/)
}
assert.equal(register.authorities.approvedSideBackTurn.sha256, sha(register.authorities.approvedSideBackTurn.file))
assert.equal(register.authorities.walkStopReturn.sha256, sha(register.authorities.walkStopReturn.register))
assert.equal(register.authorities.walkStopReturn.routeSha256, sha(register.authorities.walkStopReturn.route))
assert.equal(register.authorities.standardUniformPalette.sha256, sha(register.authorities.standardUniformPalette.file))
assert.equal(register.authorities.seatedBackGeometry.sha256, sha(register.authorities.seatedBackGeometry.file))
assert.equal(register.historicalChoreographyOnly.sha256, sha(register.historicalChoreographyOnly.file))
assert.equal(register.historicalChoreographyOnly.pixelsReusedInCandidate, false)

const palettePng = PNG.sync.read(fs.readFileSync(abs(register.authorities.standardUniformPalette.file)))
const paletteRgb = new Set()
for (let offset = 0; offset < palettePng.data.length; offset += 4) if (palettePng.data[offset + 3]) paletteRgb.add(`${palettePng.data[offset]},${palettePng.data[offset + 1]},${palettePng.data[offset + 2]}`)

for (const frame of register.candidate.frames) {
  assert.equal(frame.sha256, sha(frame.file))
  assert.equal(frame.sourceSha256, sha(frame.source))
  assert.equal(frame.alphaSha256, alphaSha(frame.file))
  const png = PNG.sync.read(fs.readFileSync(abs(frame.file)))
  assert.deepEqual([png.width, png.height], [256, 320])
  assert.equal(frame.edgeAlphaPixels, 0)
  assert.ok(frame.transparentGutterPx >= 4)
  assert.equal(frame.bounds.maxY, 315)
  if (frame.frame > 1) {
    assert.equal(frame.paletteRegistration.authoritySha256, register.authorities.standardUniformPalette.sha256)
    assert.equal(frame.paletteRegistration.offPalettePixels, 0)
    assert.equal(frame.paletteRegistration.allVisibleRgbFromAuthority, true)
    for (const component of ['uniformBlue', 'trousers', 'boots']) assert.equal(frame.paletteRegistration.components[component].outputMedianMatchesAuthority, true)
    for (let offset = 0; offset < png.data.length; offset += 4) {
      if (!png.data[offset + 3]) continue
      assert.ok(paletteRgb.has(`${png.data[offset]},${png.data[offset + 1]},${png.data[offset + 2]}`), `F${frame.frame} has off-authority RGB at pixel ${offset / 4}`)
    }
  }
}

assert.equal(register.candidate.frames[0].sha256, register.authorities.standingBack.sha256)
assert.equal(register.candidate.frames[5].alphaSha256, register.authorities.seatedBackGeometry.alphaSha256)
assert.notEqual(register.candidate.frames[5].sha256, register.authorities.seatedBackGeometry.sha256)

for (const [direction, strip] of [['forward', register.candidate.forwardStrip], ['reverse', register.candidate.reverseStrip]]) {
  assert.equal(strip.sha256, sha(strip.file))
  const png = PNG.sync.read(fs.readFileSync(abs(strip.file)))
  assert.deepEqual([png.width, png.height], [1536, 320])
  const frames = direction === 'forward' ? register.candidate.frames : [...register.candidate.frames].reverse()
  for (let i = 0; i < 6; i += 1) {
    const expected = PNG.sync.read(fs.readFileSync(abs(frames[i].file)))
    for (let y = 0; y < 320; y += 1) assert.ok(png.data.subarray(((y * 1536) + i * 256) * 4, ((y * 1536) + i * 256) * 4 + 1024).equals(expected.data.subarray(y * 1024, y * 1024 + 1024)))
  }
}

assert.equal(data.room.chair.renderLayer, 'foreground-over-keeper')
assert.equal(data.room.chair.visibleSurface, 'rear of chair')
assert.equal(data.room.chair.actorDepth, 'behind-chair-during-turn-action-and-return')
assert.deepEqual(data.route.slice(28, 33).map((frame) => frame.actionFrame), [2, 3, 4, 5, 6])
assert.deepEqual(data.route.slice(37, 42).map((frame) => frame.actionFrame), [5, 4, 3, 2, 1])
for (const frame of data.route) assert.ok(register.publishedAssets.some((asset) => asset.url === frame.src))
for (const [name, value] of Object.entries(register.checks)) assert.equal(value, name === 'historicalKeeperPixelsReusedInCandidate' ? false : true, `${name} failed`)
for (const flag of ['backV1Approved', 'rearAngleSitStandApproved', 'promotionAllowed', 'finalChanged', 'runtimeChanged', 'productionChanged']) assert.equal(register.approvalBoundary[flag], false)
for (const token of ['getFrontV4', 'keeper-prime-sit-stand-back-v1', 'Prime palette locked', 'darker colour rejected', 'foreground chair']) assert.ok(page.includes(token), `page missing ${token}`)

console.log('Keeper Prime back sit/stand V1 verified: exact approved rear entry, exact seated alpha geometry, component-wise approved Prime V5 palette for F2-F6, 150 px lowering width, foreground rear chair, 61-frame complete context and zero promotion.')
