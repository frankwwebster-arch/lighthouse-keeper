#!/usr/bin/env node
/** Verify the immutable, reversible Prime Keeper sweep-broom V1 review candidate. */
import assert from 'node:assert/strict'
import crypto from 'node:crypto'
import fs from 'node:fs'
import path from 'node:path'
import { PNG } from 'pngjs'

const root = path.resolve(import.meta.dirname, '..')
const abs = (name) => path.join(root, name)
const readJson = (name) => JSON.parse(fs.readFileSync(abs(name), 'utf8'))
const sha = (name) => crypto.createHash('sha256').update(fs.readFileSync(abs(name))).digest('hex')
const readPng = (name) => PNG.sync.read(fs.readFileSync(abs(name)))
const registerFile = 'art/drafts/keeper-prime-sweep-broom-2026-10-18-v1/batch-register.json'
const routeFile = 'art/drafts/keeper-prime-sweep-broom-2026-10-18-v1/keeper-prime-sweep-broom-v1.json'
const pageFile = 'public/keeper-review/keeper-prime-sweep-broom-v1/index.html'
const register = readJson(registerFile)
const route = readJson(routeFile)
const page = fs.readFileSync(abs(pageFile), 'utf8')
const expectedComponents = ['capCrown', 'capBandBrim', 'badge', 'jumperBlue', 'creamBand', 'trousers', 'boots', 'skin', 'hair', 'beard', 'outline']
const expectedActionPath = ['neutral', 'acquire', 'phase1', 'phase2', 'phase3', 'phase4', 'phase3', 'phase2', 'phase1', 'acquire', 'neutral']
const expectedLoop = ['phase1', 'phase2', 'phase3', 'phase4', 'phase3', 'phase2']

function pixel(png, x, y) {
  const offset = (y * png.width + x) * 4
  return png.data.subarray(offset, offset + 4)
}

function bounds(png) {
  let minX = png.width; let minY = png.height; let maxX = -1; let maxY = -1; let count = 0
  for (let y = 0; y < png.height; y += 1) for (let x = 0; x < png.width; x += 1) {
    if (!pixel(png, x, y)[3]) continue
    minX = Math.min(minX, x); minY = Math.min(minY, y); maxX = Math.max(maxX, x); maxY = Math.max(maxY, y); count += 1
  }
  assert.ok(count, 'empty PNG')
  return { minX, minY, maxX, maxY, width: maxX - minX + 1, height: maxY - minY + 1, opaquePixels: count }
}

function verifyStrip(stripRecord, ids) {
  assert.equal(stripRecord.sha256, sha(stripRecord.file))
  const strip = readPng(stripRecord.file)
  assert.deepEqual([strip.width, strip.height], [384 * ids.length, 320])
  ids.forEach((id, index) => {
    const source = readPng(register.candidate.frames.find((frame) => frame.id === id).composite.file)
    for (let y = 0; y < 320; y += 1) for (let x = 0; x < 384; x += 1) {
      const actual = pixel(strip, index * 384 + x, y); const expected = pixel(source, x, y)
      assert.equal(actual[3], expected[3], `${stripRecord.file} frame ${index + 1} alpha changed`)
      if (expected[3]) assert.ok(actual.equals(expected), `${stripRecord.file} frame ${index + 1} visible pixel changed`)
    }
  })
}

assert.equal(register.schema, 'lighthouse-keeper/reversible-review-batch@1')
assert.equal(register.set, 'keeper-prime-sweep-broom-v1')
assert.equal(register.status, 'prime-sweep-broom-v1-awaiting-frank')
assert.equal(register.auditTreatment, 'partial-motion-salvage-assessment')
assert.equal(route.schema, 'lighthouse-keeper/prime-action-review@1')
assert.equal(route.status, 'versioned-reversible-review-candidate-not-approved')
assert.deepEqual(route.components, expectedComponents)
assert.deepEqual(register.candidate.actionPath, expectedActionPath)
assert.deepEqual(register.candidate.actionLoop, expectedLoop)
assert.deepEqual(route.actionPath, expectedActionPath)
assert.deepEqual(route.actionLoop, expectedLoop)
assert.deepEqual(register.registration.logicalCell, [48, 40])
assert.deepEqual(register.registration.cellPixels, [384, 320])
assert.equal(register.registration.density, 8)
assert.equal(register.registration.floorPixelY, 315)
assert.equal(register.registration.creativePixelWarp, false)

for (const authority of [register.authorities.exactSideRightNeutral, register.authorities.smoothPrimeSource]) assert.equal(authority.sha256, sha(authority.file))
assert.equal(register.authorities.backSitStandV2Approval.sha256, sha(register.authorities.backSitStandV2Approval.file))
assert.equal(register.authorities.backSitStandV2Approval.promotionPerformed, false)
assert.equal(register.historicalChoreographyOnly.raw.sha256, sha(register.historicalChoreographyOnly.raw.file))
assert.equal(register.historicalChoreographyOnly.runtime.sha256, sha(register.historicalChoreographyOnly.runtime.file))
assert.equal(register.historicalChoreographyOnly.visibleKeeperPixelsReused, 0)
assert.deepEqual(register.historicalChoreographyOnly.allowedEvidence, ['joint paths', 'weight transfer', 'broom movement', 'hand contact', 'timing'])
for (const source of Object.values(register.generation.sources)) assert.equal(source.sha256, sha(source.file))

const neutral = register.candidate.frames.find((frame) => frame.id === 'neutral')
const neutralActor = readPng(neutral.actor.file)
const authority = readPng(neutral.actor.authorityFile)
assert.deepEqual([neutralActor.width, neutralActor.height], [384, 320])
assert.deepEqual([authority.width, authority.height], [256, 320])
for (let y = 0; y < 320; y += 1) assert.ok(neutralActor.data.subarray(y * 384 * 4, y * 384 * 4 + 256 * 4).equals(authority.data.subarray(y * 256 * 4, (y + 1) * 256 * 4)), `neutral authority crop changed at row ${y}`)

for (const frame of register.candidate.frames) {
  for (const part of ['actor', 'prop', 'composite']) assert.equal(frame[part].sha256, sha(frame[part].file), `${frame.id} ${part} hash changed`)
  const actor = readPng(frame.actor.file); const prop = readPng(frame.prop.file); const composite = readPng(frame.composite.file)
  assert.deepEqual([actor.width, actor.height], [384, 320]); assert.deepEqual([prop.width, prop.height], [384, 320]); assert.deepEqual([composite.width, composite.height], [384, 320])
  assert.deepEqual(frame.actor.bounds, bounds(actor)); assert.deepEqual(frame.prop.bounds, bounds(prop)); assert.deepEqual(frame.composite.bounds, bounds(composite))
  assert.equal(frame.actor.bounds.maxY, 315, `${frame.id} actor floor changed`)
  assert.equal(frame.prop.bounds.maxY, 315, `${frame.id} broom floor changed`)
  assert.equal(frame.composite.edgeAlphaPixels, 0)
  assert.ok(frame.composite.transparentGutterPx >= 4)
  for (let offset = 0; offset < actor.data.length; offset += 4) {
    const actorAlpha = actor.data[offset + 3]; const propAlpha = prop.data[offset + 3]; const compositeAlpha = composite.data[offset + 3]
    assert.ok(!(actorAlpha && propAlpha), `${frame.id} actor/prop ownership overlaps`)
    if (actorAlpha) assert.ok(composite.data.subarray(offset, offset + 4).equals(actor.data.subarray(offset, offset + 4)), `${frame.id} actor not topmost`)
    else if (propAlpha) assert.ok(composite.data.subarray(offset, offset + 4).equals(prop.data.subarray(offset, offset + 4)), `${frame.id} visible prop differs from composite`)
    else assert.equal(compositeAlpha, 0, `${frame.id} contains an unowned composite pixel`)
  }
  assert.equal(frame.ownership.unownedVisiblePixels, 0)
  assert.equal(frame.ownership.multiplyOwnedVisiblePixels, 0)
  for (const component of expectedComponents) {
    const evidence = frame.colourEvidence[component]
    assert.equal(evidence.status, 'pass', `${frame.id} ${component} colour gate failed`)
    assert.equal(evidence.authoritySha256, register.authorities.exactSideRightNeutral.sha256)
    assert.ok(evidence.candidate.pixels >= evidence.minimum)
    assert.ok(Math.abs(evidence.candidate.medianLuma - evidence.authority.medianLuma) <= 2)
    assert.ok(Math.abs(evidence.candidate.p25Luma - evidence.authority.p25Luma) <= 4)
    assert.ok(Math.abs(evidence.candidate.p75Luma - evidence.authority.p75Luma) <= 4)
    assert.ok(evidence.medianOklabDelta <= 0.02)
    assert.ok(evidence.p95NearestAuthoritySwatchDelta <= 0.05)
    assert.equal(frame.componentMasks[component].sha256, sha(frame.componentMasks[component].file))
  }
  if (frame.id === 'neutral') assert.equal(frame.broomHandContact.status, 'staged-room-prop-no-contact')
  else {
    assert.equal(frame.broomHandContact.status, 'pass')
    assert.ok(frame.broomHandContact.occludedHandlePixelsBehindEachHand.every((count) => count >= 8))
    assert.equal(frame.broomHandContact.propGeometry.bristleFloorY, 315)
    assert.equal(frame.prop.rawBehindActorSha256, sha(frame.prop.rawBehindActorFile))
  }
}

verifyStrip(register.candidate.forwardStrip, expectedActionPath)
verifyStrip(register.candidate.loopStrip, expectedLoop)
for (const record of [register.candidate.contactSheet, register.candidate.route]) assert.equal(record.sha256, sha(record.file))
assert.equal(route.route.length, 47)
assert.deepEqual(route.route.map((frame) => frame.phase), [
  ...Array(16).fill('approved walk'), ...Array(3).fill('phase-correct stop'), 'exact neutral', 'action entry',
  ...Array(12).fill('sweeping loop'), ...Array(3).fill('action exit'), ...Array(4).fill('phase-correct walk start'), ...Array(7).fill('approved walk away'),
])
assert.deepEqual(route.route.slice(21, 33).map((frame) => frame.actionId), [...expectedLoop, ...expectedLoop])
assert.equal(route.route[19].actionId, 'neutral'); assert.equal(route.route[35].actionId, 'neutral')
assert.deepEqual(route.route.slice(36, 40).map((frame) => frame.label), ['approved acceleration bridge 1', 'approved acceleration bridge 2', 'approved acceleration bridge 3', 'approved Walk V6 F1'])
for (const frame of route.route) for (const key of ['actorSrc', 'propSrc']) assert.ok(register.publishedAssets.some((asset) => asset.url === frame[key]), `route URL not published: ${frame[key]}`)
for (const asset of register.publishedAssets) assert.equal(asset.sourceSha256, sha(asset.source), `published source changed: ${asset.source}`)
for (const [name, value] of Object.entries(register.checks)) assert.equal(value, name === 'historicalKeeperPixelsReused' ? false : true, `${name} changed`)
for (const flag of ['candidateApproved', 'promotionAllowed', 'finalChanged', 'runtimeChanged', 'productionChanged']) assert.equal(register.approvalBoundary[flag], false)
for (const token of ['Complete route', 'Action path', 'Action loop', 'Large inspection · 6 px/lp', 'Gameplay scale · 4 px/lp', 'Literal 1× · 1 px/lp', 'Previous-frame ghost', 'Exact Prime ghost', 'Frame-by-frame Prime comparison', 'Loading and decoding every unique frame', 'img.decode', 'Promise.all']) assert.ok(page.includes(token), `review page missing ${token}`)

console.log('Keeper Prime sweep broom V1 verified: six owned actor/prop composites, exact Prime endpoint, per-material all-frame colour gates, two-hand contact, four-pixel gutters and complete 47-frame route; nothing promoted.')
