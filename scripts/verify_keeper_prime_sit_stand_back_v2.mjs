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
const register = json('art/drafts/keeper-prime-sit-stand-back-2026-10-18-v2/batch-register.json')
const data = json('art/drafts/keeper-prime-sit-stand-back-2026-10-18-v2/keeper-prime-sit-stand-back-v2.json')
const v1 = json('art/drafts/keeper-prime-sit-stand-back-2026-10-18-v1/batch-register.json')
const page = fs.readFileSync(abs('src/app/keeper-review/keeper-prime-sit-stand-back-v2/route.ts'), 'utf8')

function alphaSha(file) {
  const png = PNG.sync.read(fs.readFileSync(abs(file))); const alpha = Buffer.alloc(png.width * png.height)
  for (let source = 3, target = 0; source < png.data.length; source += 4, target += 1) alpha[target] = png.data[source]
  return crypto.createHash('sha256').update(alpha).digest('hex')
}

assert.equal(register.set, 'keeper-prime-sit-stand-back-v2')
assert.equal(register.status, 'back-foreground-chair-v2-palette-corrected-awaiting-frank')
assert.equal(data.status, 'reversible-back-review-candidate-v2-not-approved')
assert.equal(data.route.length, 61)
assert.equal(register.predecessor.sha256, sha(register.predecessor.register))
assert.match(register.predecessor.disposition, /darker than Prime/)
assert.equal(register.authorities.standingBackPalette.sha256, sha(register.authorities.standingBackPalette.file))
assert.deepEqual(register.authorities.standingBackPalette.regionalReadings, { jumperCore: { pixels: 5131, medianLuma: 95, p25Luma: 92, p75Luma: 97 }, trouserCore: { pixels: 3433, medianLuma: 77, p25Luma: 73, p75Luma: 78 } })

for (const [index, frame] of register.candidate.frames.entries()) {
  assert.equal(frame.sha256, sha(frame.file))
  assert.equal(frame.alphaSha256, alphaSha(frame.file))
  assert.equal(frame.alphaSha256, v1.candidate.frames[index].alphaSha256)
  assert.equal(frame.bounds.width, v1.candidate.frames[index].bounds.width)
  assert.equal(frame.bounds.height, v1.candidate.frames[index].bounds.height)
  assert.equal(frame.priorV1Sha256, v1.candidate.frames[index].sha256)
  if (index === 0) assert.equal(frame.sha256, v1.candidate.frames[index].sha256)
  else {
    assert.notEqual(frame.sha256, v1.candidate.frames[index].sha256)
    assert.equal(frame.paletteRegistration.offAuthorityPixels, 0)
    assert.equal(frame.paletteRegistration.allVisibleRgbFromApprovedPrimeAuthorities, true)
    assert.ok(Math.abs(frame.paletteRegistration.corrected.jumperCore.medianLuma - 95) <= 1)
    assert.ok(Math.abs(frame.paletteRegistration.corrected.trouserCore.medianLuma - 77) <= 1)
    assert.ok(frame.paletteRegistration.prior.jumperCore.medianLuma <= 74)
    assert.ok(frame.paletteRegistration.prior.trouserCore.medianLuma <= 53)
  }
}

assert.deepEqual(register.candidate.frames.map((frame) => frame.bounds.width), [155, 150, 150, 150, 150, 150])
assert.deepEqual(register.candidate.frames.map((frame) => frame.bounds.height), [298, 286, 276, 270, 266, 264])
assert.deepEqual(data.route.slice(28, 33).map((frame) => frame.actionFrame), [2, 3, 4, 5, 6])
assert.deepEqual(data.route.slice(37, 42).map((frame) => frame.actionFrame), [5, 4, 3, 2, 1])
for (const frame of data.action.frames) {
  for (const key of ['src', 'sourcePreviewSrc', 'priorV1Src', 'paletteAuthoritySrc']) assert.ok(register.publishedAssets.some((asset) => asset.url === frame[key]), `missing published ${key}`)
}
for (const frame of data.route) assert.ok(register.publishedAssets.some((asset) => asset.url === frame.src))
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
for (const [name, value] of Object.entries(register.checks)) assert.equal(value, name === 'historicalKeeperPixelsReusedInCandidate' ? false : true, `${name} failed`)
for (const flag of ['backV1Approved', 'backV2Approved', 'rearAngleSitStandApproved', 'promotionAllowed', 'finalChanged', 'runtimeChanged', 'productionChanged']) assert.equal(register.approvalBoundary[flag], false)
for (const token of ['getBackV1', 'keeper-prime-sit-stand-back-v2', 'Prime regional match', 'Immutable V1 · rejected colour match', 'paletteAuthoritySrc', 'priorV1Src']) assert.ok(page.includes(token), `page missing ${token}`)

console.log('Keeper Prime back sit/stand V2 verified: exact V1 geometry and alpha, direct regional jumper/trouser match to exact approved rear endpoint, complete 61-frame context, ghost overlays, foreground rear chair and zero promotion.')
