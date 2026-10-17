#!/usr/bin/env node
/** Verify Frank's immutable approval of exact Keeper Prime side-left sit/stand V1. */
import assert from 'node:assert/strict'
import crypto from 'node:crypto'
import fs from 'node:fs'
import path from 'node:path'

const root = path.resolve(import.meta.dirname, '..')
const rel = {
  decision: 'docs/review/keeper-prime-sit-stand-side-left-v1-approval-2026-10-17.json',
  register: 'art/drafts/keeper-prime-sit-stand-side-left-2026-10-17-v1/batch-register.json',
  reviewRoute: 'src/app/keeper-review/keeper-prime-sit-stand-side-left-v1/route.ts',
  routeData: 'art/drafts/keeper-prime-sit-stand-side-left-2026-10-17-v1/keeper-prime-sit-stand-side-left-v1.json',
}
const frames = [1, 2, 3, 4, 5, 6].map((n) =>
  `art/drafts/keeper-prime-sit-stand-side-left-2026-10-17-v1/drafts/frames/keeper_prime_stand-to-sit-side-left_f${String(n).padStart(2, '0')}.png`,
)
const file = (name) => path.join(root, name)
const readJson = (name) => JSON.parse(fs.readFileSync(file(name), 'utf8'))
const sha = (name) => crypto.createHash('sha256').update(fs.readFileSync(file(name))).digest('hex')

for (const name of [...Object.values(rel), ...frames]) assert.ok(fs.existsSync(file(name)), `missing ${name}`)
const decision = readJson(rel.decision)
const register = readJson(rel.register)
const route = readJson(rel.routeData)

assert.equal(decision.schema, 'lighthouse-keeper/review-decision@1')
assert.equal(decision.reviewedOn, '2026-10-17')
assert.equal(decision.reviewedBy, 'Frank')
assert.equal(decision.candidate, 'keeper-prime-sit-stand-side-left-2026-10-17-v1')
assert.equal(decision.decision, 'approved-as-side-left-prime-sit-stand-authority')
assert.equal(decision.wording, 'approved')

assert.equal(decision.approvedHashes.batchRegister, sha(rel.register))
assert.equal(decision.approvedHashes.reviewRoute, sha(rel.reviewRoute))
assert.equal(decision.approvedHashes.routeData, sha(rel.routeData))
assert.deepEqual(decision.approvedHashes.keeperFrames, frames.map(sha))
assert.deepEqual(register.candidate.frames.map((frame) => frame.sha256), decision.approvedHashes.keeperFrames)
assert.equal(route.route.length, 45)

for (const flag of ['standEndpointExactPrime', 'seatedEndpointExactRegisteredPrime', 'sitToStandIsExactReverse', 'allKeeperPixelsExactHorizontalReflectionsOfPinnedPrimeAuthorities', 'sideRightV6RemainsUnchanged']) {
  assert.equal(decision.approvedContract[flag], true, `${flag} changed`)
}
assert.equal(decision.approvedContract.historicalKeeperPixelsVisible, 0)
assert.equal(decision.approvedContract.actionFrames, 6)
assert.equal(decision.approvedContract.contextFrames, 45)
assert.equal(decision.approvedContract.seatHeightAboveFloorLp, 7.75)
assert.equal(decision.approvalBoundary.sideLeftSitStandApproved, true)
for (const flag of ['frontSitStandApproved', 'backSitStandApproved', 'rearAngleSitStandApproved', 'finalChanged', 'runtimeChanged', 'productionChanged', 'promotionPerformed']) {
  assert.equal(decision.approvalBoundary[flag], false, `${flag} boundary changed`)
}

console.log('Keeper Prime side-left sit/stand V1 approval verified: exact reflected six-pose action and 45-frame context pinned; front/back/rear-angle and Final/runtime/production remain unchanged.')
