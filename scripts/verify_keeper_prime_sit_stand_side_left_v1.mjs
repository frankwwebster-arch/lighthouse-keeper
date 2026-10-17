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
const register = json('art/drafts/keeper-prime-sit-stand-side-left-2026-10-17-v1/batch-register.json')
const data = json('art/drafts/keeper-prime-sit-stand-side-left-2026-10-17-v1/keeper-prime-sit-stand-side-left-v1.json')
const right = json('art/drafts/keeper-prime-sit-stand-side-2026-10-17-v2/keeper-prime-sit-stand-side-v2.json')
const approval = json('docs/review/keeper-prime-sit-stand-side-v6-approval-2026-10-17.json')
const page = fs.readFileSync(rel('src/app/keeper-review/keeper-prime-sit-stand-side-left-v1/route.ts'), 'utf8')

assert.equal(register.status, 'side-left-exact-reflection-candidate-awaiting-frank')
assert.equal(register.classification.inheritedFamily, 'keeper_sit_side')
assert.equal(register.classification.auditTreatment, 'partial-motion-salvage-assessment')
assert.equal(register.classification.visibleHistoricalKeeperPixels, 0)
assert.equal(register.authorities.sideRightApproval.sha256, sha(register.authorities.sideRightApproval.file))
assert.equal(register.authorities.sideRightApproval.decision, approval.decision)
assert.equal(data.route.length, 45)
assert.equal(data.action.frames.length, 6)
assert.equal(data.derivation.method, 'exact-horizontal-reflection')
assert.equal(data.derivation.visibleHistoricalKeeperPixels, 0)

for (const [index, frame] of register.candidate.frames.entries()) {
  assert.equal(frame.sha256, sha(frame.file))
  assert.equal(frame.sourceSha256, sha(frame.source))
  assert.equal(frame.sourceSha256, approval.approvedHashes.keeperFrames[index])
  const source = PNG.sync.read(fs.readFileSync(rel(frame.source)))
  const candidate = PNG.sync.read(fs.readFileSync(rel(frame.file)))
  assert.deepEqual([candidate.width, candidate.height], [256, 320])
  assert.deepEqual([source.width, source.height], [candidate.width, candidate.height])
  for (let y = 0; y < source.height; y += 1) for (let x = 0; x < source.width; x += 1) for (let channel = 0; channel < 4; channel += 1) {
    assert.equal(candidate.data[(y * candidate.width + x) * 4 + channel], source.data[(y * source.width + (source.width - 1 - x)) * 4 + channel], `mirror mismatch in frame ${index + 1} at ${x},${y},${channel}`)
  }
  assert.equal(frame.edgeAlphaPixels, 0)
  assert.ok(frame.transparentGutterPx >= 4)
}
for (const frame of register.candidate.reflectedContextCells) {
  assert.equal(frame.sha256, sha(frame.file))
  assert.equal(frame.sourceSha256, sha(frame.source))
  assert.equal(frame.edgeAlphaPixels, 0)
  assert.ok(frame.transparentGutterPx >= 1)
}

assert.equal(register.candidate.frames[5].sha256, sha(register.authorities.registeredSideLeftSeatedEndpoint.file))
assert.equal(register.candidate.forwardStrip.sha256, sha(register.candidate.forwardStrip.file))
assert.equal(register.candidate.reverseStrip.sha256, sha(register.candidate.reverseStrip.file))
for (const strip of [register.candidate.forwardStrip, register.candidate.reverseStrip]) {
  const png = PNG.sync.read(fs.readFileSync(rel(strip.file)))
  assert.deepEqual([png.width, png.height], strip.pixels)
  assert.deepEqual(strip.pixels, [1536, 320])
}

for (const [index, frame] of data.route.entries()) {
  const source = right.route[index]
  assert.equal(frame.rootXLp, Number((172 - source.rootXLp).toFixed(3)))
  assert.equal(frame.durationMs, source.durationMs)
  assert.equal(frame.phase, source.phase)
  assert.equal(frame.actionFrame, source.actionFrame)
  assert.equal(frame.sourceRightSrc, source.src)
}
assert.equal(data.room.chair.seatHeightAboveFloorLp, 7.75)
assert.equal(data.room.chair.seatTopWorldYLp, 44.25)
assert.equal(data.room.chair.shinRearWorldXLp + data.room.chair.shinClearanceLp, data.room.chair.seatFrontRimWorldXLp)
assert.ok(data.room.chair.seatFrontRimWorldXLp < data.room.chair.backrestFrontWorldXLp)
assert.ok(Object.values(register.checks).every(Boolean))
assert.equal(register.approvalBoundary.sideLeftSitStandApproved, false)
assert.equal(register.approvalBoundary.promotionAllowed, false)

for (const token of ['Promise.all(unique.map(preload))', 'Standing Prime ghost', 'Previous-frame ghost', 'Large inspection · 8×', 'Proposed game presentation · 4×', 'Literal logical raster · 1×', 'Action loop only', 'Source-right authority', 'Candidate side-left reflection']) {
  assert.ok(page.includes(token), `review page missing ${token}`)
}
assert.ok(page.includes('/keeper-review/keeper-prime-sit-stand-side-left-v1/route.json'))

console.log('Keeper Prime side-left sit/stand V1 verified: all action/context pixels are exact isolated reflections of pinned Prime authorities; 45-frame context, ghosts, comparison and no-promotion boundary pass.')
