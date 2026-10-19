#!/usr/bin/env node
/** Verify Frank's immutable approval of the held-implement motion POC V3. */
import assert from 'node:assert/strict'
import crypto from 'node:crypto'
import fs from 'node:fs'
import path from 'node:path'

const root = path.resolve(import.meta.dirname, '..')
const file = (name) => path.join(root, name)
const readJson = (name) => JSON.parse(fs.readFileSync(file(name), 'utf8'))
const sha = (name) => crypto.createHash('sha256').update(fs.readFileSync(file(name))).digest('hex')
const rel = {
  decision: 'docs/review/keeper-prime-upper-body-override-poc-v3-approval-2026-10-19.json',
  register: 'art/drafts/keeper-prime-upper-body-override-poc-2026-10-19-v3/batch-register.json',
  routeData: 'art/drafts/keeper-prime-upper-body-override-poc-2026-10-19-v3/keeper-prime-upper-body-override-poc-v3.json',
  reviewer: 'art/drafts/keeper-prime-upper-body-override-poc-2026-10-19-v3/reviewer.html',
  publicShell: 'public/keeper-review/keeper-prime-upper-body-override-poc-v3/index.html',
}

for (const name of Object.values(rel)) assert.ok(fs.existsSync(file(name)), `missing ${name}`)
const decision = readJson(rel.decision)
const register = readJson(rel.register)
const route = readJson(rel.routeData)
const frames = register.candidate.frames.map((frame) => frame.candidate.file)

assert.equal(decision.schema, 'lighthouse-keeper/review-decision@1')
assert.equal(decision.reviewedOn, '2026-10-19')
assert.equal(decision.reviewedBy, 'Frank')
assert.equal(decision.candidate, 'keeper-prime-upper-body-override-poc-v3')
assert.equal(decision.decision, 'approved-as-held-implement-motion-feasibility-poc')
assert.match(decision.wording, /explicitly approved/)
assert.equal(decision.approvedHashes.batchRegister, sha(rel.register))
assert.equal(decision.approvedHashes.routeData, sha(rel.routeData))
assert.equal(decision.approvedHashes.reviewer, sha(rel.reviewer))
assert.equal(decision.approvedHashes.publicShell, sha(rel.publicShell))
assert.deepEqual(decision.approvedHashes.keeperFrames, frames.map(sha))
assert.deepEqual(register.candidate.frames.map((frame) => frame.candidate.sha256), decision.approvedHashes.keeperFrames)

assert.equal(register.scope.gripProfile, decision.approvedContract.gripProfile)
assert.equal(register.scope.walkFrames, decision.approvedContract.walkPhases)
assert.equal(register.scope.turnFrames, decision.approvedContract.turnAngles)
assert.equal(route.route.length, decision.approvedContract.combinedPlaybackFrames)
assert.equal(register.construction.maximumVisibleHandComponents, decision.approvedContract.maximumVisibleHands)
assert.equal(register.construction.propPixels, decision.approvedContract.propPixels)
assert.equal(register.construction.standardWalkAdvanceLogicalPixelsPerFrame, decision.approvedContract.standardWalkAdvanceLogicalPixelsPerFrame)
assert.equal(register.construction.walkRootDeltaLogicalPixels * 8, decision.approvedContract.standardWalkCycleAdvanceLogicalPixels)
assert.equal(register.correction.playback.mode, 'one-shot')
assert.equal(register.correction.rearSeam.playbackFrame, decision.approvedContract.rearSeamPlaybackFrame)
assert.equal(register.correction.rearSeam.presentationOffsetXLp, decision.approvedContract.rearSeamPresentationOffsetLogicalPixels)
for (const flag of [
  'motionFeasibilityApproved', 'oneShotReviewPlayback', 'v1ArtworkReusedByteForByte',
  'v1AndV2RemainImmutable', 'productionSuccessorRequiresSeparablePrimeTorsoArmLayers',
]) assert.equal(decision.approvedContract[flag], true, `${flag} changed`)
for (const flag of ['heldImplementMotionFeasibilityApproved', 'holdShaftTwoHandConceptApproved']) assert.equal(decision.approvalBoundary[flag], true)
for (const flag of [
  'proxyArtworkApprovedForProduction', 'separablePrimeLayerArtworkApproved', 'broomApproved',
  'otherImplementVariantsApproved', 'finalChanged', 'runtimeChanged', 'productionChanged',
  'promotionPerformed', 'promotionAllowedWithoutSeparateInstruction',
]) assert.equal(decision.approvalBoundary[flag], false, `${flag} boundary changed`)

console.log('Prime held-implement POC V3 approval verified: the two-hand shaft-grip motion method is approved and hash-pinned; proxy art, implements, runtime, Final and production promotion remain unapproved.')
