#!/usr/bin/env node

import assert from 'node:assert/strict'
import crypto from 'node:crypto'
import fs from 'node:fs'
import path from 'node:path'
import { PNG } from 'pngjs'

const root = path.resolve(import.meta.dirname, '..')
const read = (file) => fs.readFileSync(path.join(root, file), 'utf8')
const json = (file) => JSON.parse(read(file))
const sha = (file) => crypto.createHash('sha256').update(fs.readFileSync(path.join(root, file))).digest('hex')
const geometry = json('data/keeper_prime_seat_geometry_v3.json')
const register = json('art/drafts/keeper-prime-sit-stand-side-2026-10-17-v6/batch-register.json')
const v2 = json('art/drafts/keeper-prime-sit-stand-side-2026-10-17-v2/batch-register.json')
const route = json('art/drafts/keeper-prime-sit-stand-side-2026-10-17-v2/keeper-prime-sit-stand-side-v2.json')
const app = read('src/app/keeper-review/keeper-prime-sit-stand-side-v6/route.ts')
const workbench = read('src/app/keeper-review/keeper-prime-context-workbench-v15/route.ts')
const wbRegister = json('art/drafts/keeper-prime-context-workbench-2026-10-17-v15/batch-register.json')

assert.equal(geometry.schema, 'lighthouse-keeper/prime-seat-geometry@3')
assert.equal(geometry.status, 'review-candidate-not-runtime')
assert.equal(geometry.vertical.rejectedNominalSeatHeightAboveFloorLp, 11)
assert.equal(geometry.vertical.pelvisLastOpaqueSourceY, 257)
assert.equal(geometry.vertical.supportPlaneSourceY, 258)
assert.equal(geometry.vertical.supportPlaneSourceY, geometry.vertical.pelvisLastOpaqueSourceY + 1)
assert.equal(geometry.vertical.seatHeightAboveFloorLp, 7.75)
assert.equal(geometry.routeRegistration.floorWorldYLp - geometry.vertical.seatTopWorldYLp, 7.75)
assert.equal(geometry.vertical.seatTopWorldYLp, geometry.routeRegistration.actorCellTopWorldYLp + geometry.vertical.supportPlaneSourceY / geometry.density)
assert.equal(geometry.chair.backrestFrontWorldXLp, geometry.anatomy.spineBackContactWorldXLp)
assert.equal(geometry.chair.backrestRearWorldXLp + geometry.chair.backrestThicknessLp, geometry.chair.backrestFrontWorldXLp)
assert.equal(geometry.chair.backrestRearWorldXLp + geometry.chair.totalSeatDepthLp, geometry.chair.seatFrontRimWorldXLp)
assert.ok(geometry.chair.seatFrontRimWorldXLp < geometry.anatomy.shinRearWorldXLp)
assert.equal(geometry.anatomy.shinRearWorldXLp - geometry.chair.seatFrontRimWorldXLp, 0.5)

const frameFile = v2.candidate.frames[5].file
assert.equal(sha(frameFile), geometry.authoritySha256)
const png = PNG.sync.read(fs.readFileSync(path.join(root, frameFile)))
const { xRange, yRange, alphaThreshold } = geometry.vertical.pelvisEvidence
let measuredPelvisLastOpaqueY = -1
for (let y = yRange[0]; y <= yRange[1]; y += 1) for (let x = xRange[0]; x <= xRange[1]; x += 1) {
  if (png.data[(y * png.width + x) * 4 + 3] > alphaThreshold) measuredPelvisLastOpaqueY = Math.max(measuredPelvisLastOpaqueY, y)
}
assert.equal(measuredPelvisLastOpaqueY, geometry.vertical.pelvisLastOpaqueSourceY)
for (let x = xRange[0]; x <= xRange[1]; x += 1) {
  assert.ok(png.data[(geometry.vertical.supportPlaneSourceY * png.width + x) * 4 + 3] <= alphaThreshold, `support plane intersects seated pelvis at x=${x}`)
}

let measuredShinRear = Infinity
for (let y = geometry.anatomy.shinEvidenceSource.yRange[0]; y <= geometry.anatomy.shinEvidenceSource.yRange[1]; y += 1) for (let x = 0; x < png.width; x += 1) {
  if (png.data[(y * png.width + x) * 4 + 3] > 16) measuredShinRear = Math.min(measuredShinRear, x)
}
assert.equal(measuredShinRear, geometry.anatomy.shinEvidenceSource.x)

assert.equal(route.route.length, 45)
assert.deepEqual(register.immutableContent.keeperFrameHashes, v2.candidate.frames.map((frame) => frame.sha256))
assert.equal(register.immutableContent.route.sha256, sha(register.immutableContent.route.file))
assert.ok(Object.values(register.checks).every(Boolean))
assert.equal(register.approvalBoundary.promotionAllowed, false)
for (const token of ['seatTop:44.25', 'seatHeight:7.75', 'supportSourceY:258', 'rejectedSeatTop:41', 'backrestFront:76.625', 'seatFront:83.75', 'shinRear:84.25', 'Promise.all', 'Large inspection · 8×', 'Proposed game presentation · 4×', 'Literal logical raster · 1×']) {
  assert.ok(app.includes(token), `missing V6 page token ${token}`)
}
assert.ok(app.includes('/keeper-review/keeper-prime-sit-stand-side-v2/route.json'))
assert.ok(workbench.includes('/keeper-review/keeper-prime-sit-stand-side-v6/'))
assert.ok(workbench.includes('V15'))
assert.ok(workbench.includes('7.75 lp above floor'))
assert.ok(workbench.includes('measured seated underside'))
assert.equal(wbRegister.candidate.sittingCandidate, '/keeper-review/keeper-prime-sit-stand-side-v6/')
assert.ok(Object.values(wbRegister.checks).every(Boolean))

console.log('Keeper Prime sit/stand side V6 verified: support plane begins immediately below the measured seated pelvis; exact Keeper pixels and 45-frame route remain unchanged.')
