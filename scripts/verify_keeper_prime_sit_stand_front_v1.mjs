#!/usr/bin/env node

import assert from 'node:assert/strict'
import crypto from 'node:crypto'
import fs from 'node:fs'
import path from 'node:path'
import { PNG } from 'pngjs'

const root = path.resolve(import.meta.dirname, '..')
const rel = (file) => path.join(root, file)
const json = (file) => JSON.parse(fs.readFileSync(rel(file), 'utf8'))
const sha = (file) => crypto.createHash('sha256').update(fs.readFileSync(rel(file))).digest('hex')
const register = json('art/drafts/keeper-prime-sit-stand-front-2026-10-17-v1/batch-register.json')
const data = json('art/drafts/keeper-prime-sit-stand-front-2026-10-17-v1/keeper-prime-sit-stand-front-v1.json')
const turn = json('art/drafts/keeper-prime-turn-front-side-2026-10-13-v1/batch-register.json')
const approval = json('docs/review/keeper-prime-sit-stand-side-left-v1-approval-2026-10-17.json')
const page = fs.readFileSync(rel('src/app/keeper-review/keeper-prime-sit-stand-front-v1/route.ts'), 'utf8')

assert.equal(register.status, 'front-prime-redraw-candidate-awaiting-frank')
assert.equal(register.classification.inheritedFamily, 'keeper_sit_front')
assert.equal(register.classification.auditTreatment, 'partial-motion-salvage-assessment')
assert.equal(register.classification.visibleHistoricalKeeperPixelsInCandidate, 0)
assert.equal(register.authorities.pinnedSideLeftApproval.sha256, sha(register.authorities.pinnedSideLeftApproval.file))
assert.equal(register.authorities.pinnedSideLeftApproval.decision, approval.decision)
assert.equal(approval.approvalBoundary.sideLeftSitStandApproved, true)
assert.equal(data.route.length, 59)
assert.deepEqual(data.coreRange, [27, 40])
assert.equal(data.action.frames.length, 6)
assert.equal(data.derivation.visibleHistoricalKeeperPixelsInCandidate, 0)

const expectedHeights = [298, 286, 276, 268, 264, 264]
for (const [index, frame] of register.candidate.frames.entries()) {
  assert.equal(frame.sha256, sha(frame.file))
  assert.equal(frame.sourceSha256, sha(frame.source))
  const png = PNG.sync.read(fs.readFileSync(rel(frame.file)))
  assert.deepEqual([png.width, png.height], [256, 320])
  assert.equal(frame.edgeAlphaPixels, 0)
  assert.ok(frame.transparentGutterPx >= 4)
  assert.equal(frame.bounds.height, expectedHeights[index])
  assert.equal(frame.bounds.maxY, 315)
  const centre = (frame.bounds.minX + frame.bounds.maxX) / 2
  assert.ok(Math.abs(centre - 127.5) <= 1, `frame ${index + 1} lost front-axis registration`)
  if (index > 0 && index < 5) {
    assert.equal(frame.registration.filter, 'Lanczos')
    assert.equal(frame.registration.creativePixelWarp, false)
    assert.deepEqual(frame.registration.registeredSize, [frame.bounds.width, frame.bounds.height])
  }
}
assert.equal(register.candidate.frames[0].sha256, register.authorities.standingFront.sha256)
assert.equal(register.candidate.frames[5].sha256, register.authorities.seatedFront.sha256)

for (const generated of register.generation.generatedSources) assert.equal(generated.sha256, sha(generated.file))
assert.equal(register.generation.endpointPixelsGenerated, false)
for (const [direction, strip] of [['forward', register.candidate.forwardStrip], ['reverse', register.candidate.reverseStrip]]) {
  assert.equal(strip.sha256, sha(strip.file))
  assert.deepEqual(strip.pixels, [1536, 320])
  const png = PNG.sync.read(fs.readFileSync(rel(strip.file)))
  assert.deepEqual([png.width, png.height], strip.pixels)
  const frames = direction === 'forward' ? register.candidate.frames : [...register.candidate.frames].reverse()
  for (let index = 0; index < 6; index += 1) {
    const expected = PNG.sync.read(fs.readFileSync(rel(frames[index].file)))
    for (let y = 0; y < 320; y += 1) {
      const actualStart = ((y * png.width) + index * 256) * 4
      const expectedStart = y * 256 * 4
      assert.ok(png.data.subarray(actualStart, actualStart + 1024).equals(expected.data.subarray(expectedStart, expectedStart + 1024)), `${direction} strip frame ${index + 1} mismatch`)
    }
  }
}

assert.deepEqual(data.turn.frames.map((frame) => frame.sha256), turn.frames.map((frame) => frame.sha256))
for (const frame of turn.frames) assert.equal(frame.sha256, sha(frame.file))
assert.equal(data.route.filter((frame) => frame.phase === 'turn side-right → front').length, 7)
assert.equal(data.route.filter((frame) => frame.phase === 'turn front → side-right').length, 7)
assert.equal(data.route.filter((frame) => frame.phase === 'stand → sit front').length, 5)
assert.equal(data.route.filter((frame) => frame.phase === 'seated-front hold').length, 4)
assert.equal(data.route.filter((frame) => frame.phase === 'sit → stand front').length, 5)
assert.equal(data.room.chair.seatHeightAboveFloorLp, 7.75)
assert.equal(data.room.chair.renderLayer, 'behind-keeper')
for (const frame of data.route.slice(20, 48)) assert.equal(frame.rootXLp, 86)
for (const frame of data.route) assert.ok(register.publishedAssets.some((asset) => asset.url === frame.src), `unpublished route image ${frame.src}`)

for (const [name, value] of Object.entries(register.checks)) {
  if (name === 'historicalKeeperPixelsReusedInCandidate') assert.equal(value, false)
  else assert.equal(value, true, `${name} changed`)
}
for (const flag of ['frontSitStandApproved', 'backSitStandApproved', 'rearAngleSitStandApproved', 'promotionAllowed', 'finalChanged', 'runtimeChanged', 'productionChanged']) assert.equal(register.approvalBoundary[flag], false)
for (const token of ['Promise.all(unique.map(preload))', 'Standing Prime ghost', 'Previous-frame ghost', 'Large inspection · 8×', 'Proposed game presentation · 4×', 'Literal logical raster · 1×', 'Action loop only', 'Turn + action + return', 'Six-pose Prime derivation proof', 'Historical <code>keeper_sit_front</code>']) assert.ok(page.includes(token), `review page missing ${token}`)
assert.ok(page.includes('/keeper-review/keeper-prime-sit-stand-front-v1/route.json'))

console.log('Keeper Prime front sit/stand V1 verified: exact Prime endpoints, four isolated Prime-derived intermediates, approved turns and complete 59-frame context pass; back/rear-angle and Final/runtime/production remain unchanged.')
