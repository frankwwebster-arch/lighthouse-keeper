#!/usr/bin/env node
/** Verify Frank's immutable approval boundary for Prime Rear Action Sequence V1. */
import assert from 'node:assert/strict'
import crypto from 'node:crypto'
import fs from 'node:fs'
import path from 'node:path'

const root = path.resolve(import.meta.dirname, '..')
const file = (name) => path.join(root, name)
const readJson = (name) => JSON.parse(fs.readFileSync(file(name), 'utf8'))
const sha = (name) => crypto.createHash('sha256').update(fs.readFileSync(file(name))).digest('hex')

const rel = {
  decision: 'docs/review/keeper-prime-rear-action-sequence-v1-approval-2026-10-20.json',
  register: 'art/drafts/keeper-prime-rear-action-sequence-2026-10-20-v1/batch-register.json',
  draftCatalogue: 'art/drafts/keeper-prime-rear-action-sequence-2026-10-20-v1/catalogue.json',
  reviewCatalogue: 'public/keeper-review/keeper-prime-rear-action-sequence-v1/catalogue.json',
  pageTemplate: 'art/drafts/keeper-prime-rear-action-sequence-2026-10-20-v1/page-template.html',
  reviewPage: 'public/keeper-review/keeper-prime-rear-action-sequence-v1/index.html',
  builder: 'scripts/build_keeper_prime_rear_action_sequence_v1.py',
  candidateVerifier: 'scripts/verify_keeper_prime_rear_action_sequence_v1.mjs',
  followUp: 'docs/ACTIVITY_CALLOUT_DYNAMIC_CHOREOGRAPHY_NEXT.md',
}

for (const name of Object.values(rel)) assert.ok(fs.existsSync(file(name)), `missing ${name}`)
const decision = readJson(rel.decision)
const register = readJson(rel.register)
const catalogue = readJson(rel.reviewCatalogue)

assert.equal(decision.schema, 'lighthouse-keeper/review-decision@1')
assert.equal(decision.reviewedOn, '2026-10-20')
assert.equal(decision.reviewedBy, 'Frank')
assert.equal(decision.candidate, 'keeper-prime-rear-action-sequence-v1')
assert.equal(decision.decision, 'approved-as-prime-rear-action-sequence-continuity-authority')
assert.match(decision.wording, /richer future activity-cloud choreography/)

for (const [key, name] of [
  ['batchRegister', rel.register],
  ['draftCatalogue', rel.draftCatalogue],
  ['reviewCatalogue', rel.reviewCatalogue],
  ['pageTemplate', rel.pageTemplate],
  ['reviewPage', rel.reviewPage],
  ['builder', rel.builder],
  ['candidateVerifier', rel.candidateVerifier],
]) assert.equal(decision.approvedHashes[key], sha(name), `${key} hash changed`)

assert.equal(decision.approvedHashes.draftCatalogue, decision.approvedHashes.reviewCatalogue)
assert.equal(decision.approvedHashes.pageTemplate, decision.approvedHashes.reviewPage)
assert.equal(register.set, decision.candidate)
assert.equal(catalogue.set, decision.candidate)
assert.equal(catalogue.sequence.length, 52)
assert.equal(catalogue.actionStartIndex, 28)
assert.equal(catalogue.phaseCounts['approved walk'], 16)
assert.equal(catalogue.phaseCounts['approved deceleration'], 4)
assert.equal(catalogue.phaseCounts['approved turn away'], 8)
assert.equal(catalogue.phaseCounts['Prime rear-work action'], 24)
assert.equal(catalogue.callout.startsWithAction, true)
assert.equal(catalogue.callout.placement, 'raised-above-cap')

for (const flag of [
  'walkStopTurnRearActionContinuityApproved', 'rearNeutralSeamExact',
  'allKeeperAndRouteBytesInherited', 'activityLayerBeginsOnlyWithAction',
  'activityLayerRemainsAboveCap', 'bodyCalloutTreatmentAndSfxIndependent',
]) assert.equal(decision.approvedContract[flag], true, `${flag} changed`)
assert.equal(decision.approvedContract.contextPropOrCounterBakedIntoKeeper, false)

for (const flag of [
  'richerAuthoredChoreographyRequired', 'mobileAssetsRequired',
  'associatedComicSymbolsRequired', 'bubbleAndNonBubbleExamplesRequired',
]) assert.equal(decision.followUpDirection[flag], true, `${flag} changed`)
assert.equal(decision.followUpDirection.currentSimpleCloudChoreographyIsFinal, false)
assert.equal(decision.followUpDirection.brief, rel.followUp)

assert.equal(decision.approvalBoundary.sequenceContinuityApproved, true)
for (const flag of [
  'currentSimpleCloudMotionApprovedAsFinal', 'newDynamicCalloutArtApproved',
  'runtimeChanged', 'finalChanged', 'kitchenChanged', 'promotionPerformed',
  'deploymentPerformed', 'promotionAllowedWithoutSeparateInstruction',
  'deploymentAllowedWithoutSeparateInstruction',
]) assert.equal(decision.approvalBoundary[flag], false, `${flag} boundary changed`)
assert.equal(decision.delivery.deployed, false)
assert.equal(decision.delivery.externalBrowserAvailabilityExpected, false)

console.log('Prime Rear Action Sequence V1 approval verified: exact continuity is approved and hash-pinned; simple cloud motion, runtime promotion and deployment remain outside approval.')
