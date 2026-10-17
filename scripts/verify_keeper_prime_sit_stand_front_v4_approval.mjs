#!/usr/bin/env node
/** Verify Frank's immutable approval of exact Keeper Prime front sit/stand V4. */
import assert from 'node:assert/strict'
import crypto from 'node:crypto'
import fs from 'node:fs'
import path from 'node:path'

const root = path.resolve(import.meta.dirname, '..')
const rel = {
  decision: 'docs/review/keeper-prime-sit-stand-front-v4-approval-2026-10-18.json',
  register: 'art/drafts/keeper-prime-sit-stand-front-2026-10-17-v4/batch-register.json',
  reviewRoute: 'src/app/keeper-review/keeper-prime-sit-stand-front-v4/route.ts',
  routeData: 'art/drafts/keeper-prime-sit-stand-front-2026-10-17-v4/keeper-prime-sit-stand-front-v4.json',
}
const frames = [1, 2, 3, 4, 5, 6].map((n) =>
  `art/drafts/keeper-prime-sit-stand-front-2026-10-17-v4/drafts/frames/keeper_prime_stand-to-sit-front_f${String(n).padStart(2, '0')}.png`,
)
const file = (name) => path.join(root, name)
const readJson = (name) => JSON.parse(fs.readFileSync(file(name), 'utf8'))
const sha = (name) => crypto.createHash('sha256').update(fs.readFileSync(file(name))).digest('hex')

for (const name of [...Object.values(rel), ...frames]) assert.ok(fs.existsSync(file(name)), `missing ${name}`)
const decision = readJson(rel.decision)
const register = readJson(rel.register)
const route = readJson(rel.routeData)

assert.equal(decision.schema, 'lighthouse-keeper/review-decision@1')
assert.equal(decision.reviewedOn, '2026-10-18')
assert.equal(decision.reviewedBy, 'Frank')
assert.equal(decision.candidate, 'keeper-prime-sit-stand-front-2026-10-17-v4')
assert.equal(decision.decision, 'approved-as-front-prime-sit-stand-authority')
assert.equal(decision.wording, 'Approved.')
assert.equal(decision.approvedHashes.batchRegister, sha(rel.register))
assert.equal(decision.approvedHashes.reviewRoute, sha(rel.reviewRoute))
assert.equal(decision.approvedHashes.routeData, sha(rel.routeData))
assert.deepEqual(decision.approvedHashes.keeperFrames, frames.map(sha))
assert.deepEqual(register.candidate.frames.map((frame) => frame.sha256), decision.approvedHashes.keeperFrames)
assert.deepEqual(register.candidate.frames.slice(1).map((frame) => frame.elbowSpanPx), [143, 143, 143, 143, 143])
assert.equal(route.route.length, 59)

for (const flag of ['standEndpointExactPrime', 'seatedEndpointExactRegisteredPrime', 'sitToStandIsExactReverse', 'allVisibleKeeperPixelsDerivedFromPrimeAuthorities', 'completeWalkStopTurnActionReturnContext', 'frontV1ThroughV3RejectionsRemainImmutable', 'sideRightV6AndSideLeftV1ApprovalsRemainUnchanged']) {
  assert.equal(decision.approvedContract[flag], true, `${flag} changed`)
}
assert.equal(decision.approvedContract.historicalKeeperPixelsVisible, 0)
assert.equal(decision.approvedContract.actionFrames, 6)
assert.equal(decision.approvedContract.contextFrames, 59)
assert.equal(decision.approvedContract.loweringFramesMatchSeatedElbowSpanPx, 143)
assert.equal(decision.approvedContract.seatHeightAboveFloorLp, 7.75)
for (const flag of ['sideRightSitStandApproved', 'sideLeftSitStandApproved', 'frontSitStandApproved']) assert.equal(decision.approvalBoundary[flag], true)
for (const flag of ['backSitStandApproved', 'rearAngleSitStandApproved', 'finalChanged', 'runtimeChanged', 'productionChanged', 'promotionPerformed']) assert.equal(decision.approvalBoundary[flag], false, `${flag} boundary changed`)

console.log('Keeper Prime front sit/stand V4 approval verified: exact six-pose action and 59-frame context pinned at a 143 px lowering elbow span; back/rear-angle and Final/runtime/production remain unchanged.')
