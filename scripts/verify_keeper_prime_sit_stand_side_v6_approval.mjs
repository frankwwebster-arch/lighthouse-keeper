#!/usr/bin/env node
/** Verify Frank's immutable approval of exact Keeper Prime side-right sit/stand V6. */
import assert from 'node:assert/strict'
import crypto from 'node:crypto'
import fs from 'node:fs'
import path from 'node:path'

const root = path.resolve(import.meta.dirname, '..')
const rel = {
  decision: 'docs/review/keeper-prime-sit-stand-side-v6-approval-2026-10-17.json',
  register: 'art/drafts/keeper-prime-sit-stand-side-2026-10-17-v6/batch-register.json',
  reviewRoute: 'src/app/keeper-review/keeper-prime-sit-stand-side-v6/route.ts',
  workbenchRoute: 'src/app/keeper-review/keeper-prime-context-workbench-v15/route.ts',
  geometry: 'data/keeper_prime_seat_geometry_v3.json',
  routeData: 'art/drafts/keeper-prime-sit-stand-side-2026-10-17-v2/keeper-prime-sit-stand-side-v2.json',
}
const frames = [1, 2, 3, 4, 5, 6].map((n) =>
  `art/drafts/keeper-prime-sit-stand-side-2026-10-17-v2/drafts/frames/keeper_prime_stand-to-sit-side-right_f${String(n).padStart(2, '0')}.png`,
)
const file = (name) => path.join(root, name)
const readJson = (name) => JSON.parse(fs.readFileSync(file(name), 'utf8'))
const sha = (name) => crypto.createHash('sha256').update(fs.readFileSync(file(name))).digest('hex')

for (const name of [...Object.values(rel), ...frames]) assert.ok(fs.existsSync(file(name)), `missing ${name}`)
const decision = readJson(rel.decision)
const register = readJson(rel.register)
const geometry = readJson(rel.geometry)
const route = readJson(rel.routeData)

assert.equal(decision.schema, 'lighthouse-keeper/review-decision@1')
assert.equal(decision.reviewedOn, '2026-10-17')
assert.equal(decision.reviewedBy, 'Frank')
assert.equal(decision.candidate, 'keeper-prime-sit-stand-side-2026-10-17-v6')
assert.equal(decision.decision, 'approved-as-side-right-prime-sit-stand-and-seat-geometry-authority')
assert.equal(decision.wording, 'approved')

assert.equal(decision.approvedHashes.batchRegister, sha(rel.register))
assert.equal(decision.approvedHashes.reviewRoute, sha(rel.reviewRoute))
assert.equal(decision.approvedHashes.workbenchRoute, sha(rel.workbenchRoute))
assert.equal(decision.approvedHashes.seatGeometry, sha(rel.geometry))
assert.equal(decision.approvedHashes.routeData, sha(rel.routeData))
assert.deepEqual(decision.approvedHashes.keeperFrames, frames.map(sha))
assert.deepEqual(register.immutableContent.keeperFrameHashes, decision.approvedHashes.keeperFrames)
assert.equal(register.immutableContent.route.sha256, decision.approvedHashes.routeData)

assert.equal(route.route.length, 45)
assert.equal(decision.approvedContract.actionFrames, 6)
assert.equal(decision.approvedContract.contextFrames, 45)
assert.equal(decision.approvedContract.seatHeightAboveFloorLp, geometry.vertical.seatHeightAboveFloorLp)
assert.equal(decision.approvedContract.seatTopWorldYLp, geometry.vertical.seatTopWorldYLp)
assert.equal(decision.approvedContract.backrestFrontWorldXLp, geometry.chair.backrestFrontWorldXLp)
assert.equal(decision.approvedContract.seatFrontRimWorldXLp, geometry.chair.seatFrontRimWorldXLp)
assert.equal(decision.approvedContract.shinRearWorldXLp, geometry.anatomy.shinRearWorldXLp)
assert.equal(decision.approvedContract.shinClearanceLp, geometry.chair.shinClearanceLp)
for (const flag of ['standEndpointExactPrime', 'seatedEndpointExactRegisteredPrime', 'sitToStandIsExactReverse', 'keeperFramesRootsTimingAndEndpointsUnchangedFromV2']) {
  assert.equal(decision.approvedContract[flag], true, `${flag} changed`)
}
for (const flag of ['sideRightSitStandApproved', 'measuredSideRightSeatGeometryApproved', 'workbenchV15RemainsReviewInfrastructure']) {
  assert.equal(decision.approvalBoundary[flag], true, `${flag} changed`)
}
for (const flag of ['otherSittingDirectionsApproved', 'finalChanged', 'runtimeChanged', 'productionChanged', 'promotionPerformed']) {
  assert.equal(decision.approvalBoundary[flag], false, `${flag} boundary changed`)
}

console.log('Keeper Prime side-right sit/stand V6 approval verified: exact six-pose action, 45-frame context and measured 7.75-lp support geometry pinned; other views and Final/runtime/production remain unchanged.')
