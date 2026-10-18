#!/usr/bin/env node
/** Verify Frank's immutable approval of exact Keeper Prime back sit/stand V2. */
import assert from 'node:assert/strict'
import crypto from 'node:crypto'
import fs from 'node:fs'
import path from 'node:path'

const root = path.resolve(import.meta.dirname, '..')
const file = (name) => path.join(root, name)
const readJson = (name) => JSON.parse(fs.readFileSync(file(name), 'utf8'))
const sha = (name) => crypto.createHash('sha256').update(fs.readFileSync(file(name))).digest('hex')
const rel = {
  decision: 'docs/review/keeper-prime-sit-stand-back-v2-approval-2026-10-18.json',
  register: 'art/drafts/keeper-prime-sit-stand-back-2026-10-18-v2/batch-register.json',
  reviewRoute: 'src/app/keeper-review/keeper-prime-sit-stand-back-v2/route.ts',
  routeData: 'art/drafts/keeper-prime-sit-stand-back-2026-10-18-v2/keeper-prime-sit-stand-back-v2.json',
}
const frames = [1, 2, 3, 4, 5, 6].map((n) =>
  `art/drafts/keeper-prime-sit-stand-back-2026-10-18-v2/drafts/frames/keeper_prime_stand-to-sit-back_f${String(n).padStart(2, '0')}.png`,
)

for (const name of [...Object.values(rel), ...frames]) assert.ok(fs.existsSync(file(name)), `missing ${name}`)
const decision = readJson(rel.decision)
const register = readJson(rel.register)
const route = readJson(rel.routeData)

assert.equal(decision.schema, 'lighthouse-keeper/review-decision@1')
assert.equal(decision.reviewedOn, '2026-10-18')
assert.equal(decision.reviewedBy, 'Frank')
assert.equal(decision.candidate, 'keeper-prime-sit-stand-back-2026-10-18-v2')
assert.equal(decision.decision, 'approved-as-back-prime-sit-stand-authority')
assert.match(decision.wording, /Frank's explicit approval/)
assert.equal(decision.approvedHashes.batchRegister, sha(rel.register))
assert.equal(decision.approvedHashes.reviewRoute, sha(rel.reviewRoute))
assert.equal(decision.approvedHashes.routeData, sha(rel.routeData))
assert.deepEqual(decision.approvedHashes.keeperFrames, frames.map(sha))
assert.deepEqual(register.candidate.frames.map((frame) => frame.sha256), decision.approvedHashes.keeperFrames)
assert.equal(route.route.length, 61)

for (const flag of [
  'standEndpointExactApprovedTurnV9Rear', 'seatedEndpointAlphaExactRegisteredPrime',
  'sitToStandIsExactReverse', 'allVisibleKeeperPixelsDerivedFromPrimeAuthorities',
  'correctedFramesUseExactApprovedRearPrimeRgbSamples', 'jumperRegionalMedianMatchesExactPrimeEndpoint',
  'trouserRegionalMedianMatchesExactPrimeEndpoint', 'chairIsSeparateForegroundDepthLayer',
  'completeWalkStopTurnActionReturnContext', 'backV1RejectionRemainsImmutable',
  'sideRightV6SideLeftV1AndFrontV4ApprovalsRemainUnchanged',
]) assert.equal(decision.approvedContract[flag], true, `${flag} changed`)
assert.equal(decision.approvedContract.historicalKeeperPixelsVisible, 0)
assert.equal(decision.approvedContract.actionFrames, 6)
assert.equal(decision.approvedContract.contextFrames, 61)
for (const flag of ['sideRightSitStandApproved', 'sideLeftSitStandApproved', 'frontSitStandApproved', 'backSitStandApproved']) assert.equal(decision.approvalBoundary[flag], true)
for (const flag of ['rearAngleSitStandApproved', 'finalChanged', 'runtimeChanged', 'productionChanged', 'promotionPerformed', 'promotionAllowedWithoutSeparateInstruction']) assert.equal(decision.approvalBoundary[flag], false, `${flag} boundary changed`)

console.log('Keeper Prime back sit/stand V2 approval verified: exact six-pose action and 61-frame context are approved and hash-pinned; rear-angle and Final/runtime/production remain unchanged.')
