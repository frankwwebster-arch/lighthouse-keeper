#!/usr/bin/env node
/** Verify Frank's immutable approval of exact Kitchen Sink V18. */
import assert from 'node:assert/strict'
import crypto from 'node:crypto'
import fs from 'node:fs'
import path from 'node:path'

const root = path.resolve(import.meta.dirname, '..')
const file = name => path.join(root, name)
const readJson = name => JSON.parse(fs.readFileSync(file(name), 'utf8'))
const sha = name => crypto.createHash('sha256').update(fs.readFileSync(file(name))).digest('hex')
const rel = {
  decision: 'docs/review/kitchen-sink-angled-join-v18-approval-2026-10-19.json',
  catalogue: 'art/drafts/kitchen-sink-angled-join-2026-10-19-v18/candidate-catalogue.json',
  register: 'art/drafts/kitchen-sink-angled-join-2026-10-19-v18/batch-register.json',
  page: 'public/keeper-review/kitchen-sink-angled-join-v18/index.html',
  archive: 'review-archive/sets/kitchen-sink-angled-join-v18.json',
}
for (const name of Object.values(rel)) assert.ok(fs.existsSync(file(name)), `missing ${name}`)

const decision = readJson(rel.decision)
const catalogue = readJson(rel.catalogue)
const register = readJson(rel.register)
const archive = readJson(rel.archive)
assert.equal(decision.schema, 'lighthouse-keeper/review-decision@1')
assert.equal(decision.reviewedOn, '2026-10-19')
assert.equal(decision.reviewedBy, 'Frank')
assert.equal(decision.candidate, 'kitchen-sink-angled-join-2026-10-19-v18')
assert.equal(decision.decision, 'approved-as-kitchen-sink-review-authority')
assert.equal(decision.wording, 'approved')
assert.equal(decision.approvedHashes.candidateCatalogue, sha(rel.catalogue))
assert.equal(decision.approvedHashes.batchRegister, sha(rel.register))
assert.equal(decision.approvedHashes.reviewPage, sha(rel.page))
assert.equal(decision.approvedHashes.archiveManifest, sha(rel.archive))

assert.equal(catalogue.status, 'approved-kitchen-sink-review-authority')
assert.equal(catalogue.boundaries.approvedReviewAuthority, true)
assert.equal(register.status, 'approved-review-authority-unpromoted')
assert.equal(register.approvedOn, '2026-10-19')
assert.equal(catalogue.construction.frontElevationExactV11, true)
assert.equal(catalogue.construction.worktopJoinDirection, 'down-right')
assert.deepEqual(catalogue.construction.worktopJoinOuterStartsByRow, [1, 1, 1, 2, 2, 2, 3, 3, 3])
assert.deepEqual(catalogue.construction.basinPerspective.rearRow.span, [20, 70])
assert.deepEqual(catalogue.construction.basinPerspective.frontRow.span, [18, 73])
assert.equal(catalogue.construction.basinPerspective.widensTowardFront, true)

for (const [name, expected] of Object.entries(decision.approvedHashes.outputs)) {
  const raw = `art/raw/kitchen-sink-angled-join-2026-10-19-v18/${name}`
  assert.equal(sha(raw), expected, `${name} changed after approval`)
  assert.equal(catalogue.outputs[name], expected)
  assert.equal(archive.entries[`/keeper-review/kitchen-sink-angled-join-v18/assets/${name}`].sha256, expected)
}
assert.equal(Object.keys(archive.entries).length, 13)
for (const effect of Object.values(catalogue.effects)) {
  assert.equal(effect.frames, decision.approvedContract.framesPerEffect)
  assert.equal(effect.fps, decision.approvedContract.fps)
  assert.equal(effect.durationSeconds, decision.approvedContract.durationSeconds)
  assert.equal(effect.byteIdenticalToV17, true)
}
for (const flag of [
  'standaloneSinkFamilyApproved', 'standardOnBrokenFamilyApproved',
  'exactV11CabinetFrontApproved', 'downRightWorktopJoinApproved',
  'opposingBasinSplayApproved', 'staticBasesByteIdentical',
  'environmentalEffectsRemainSeparate', 'onWaterLoopApproved',
  'brokenBasinJetsLoopApproved', 'namedSfxPlaceholdersPresent',
]) assert.equal(decision.approvedContract[flag], true, `${flag} changed`)
assert.deepEqual(decision.approvedContract.cellPixels, [92, 108])
assert.deepEqual(decision.approvedContract.bodyPixels, [84, 74])
for (const flag of ['kitchenSinkReviewAuthorityApproved', 'v11AndV17RemainImmutable']) assert.equal(decision.approvalBoundary[flag], true)
for (const flag of [
  'finalChanged', 'runtimeChanged', 'productionAssetsChanged',
  'promotionPerformed', 'promotionAllowedWithoutSeparateInstruction',
]) assert.equal(decision.approvalBoundary[flag], false, `${flag} boundary changed`)

const page = fs.readFileSync(file(rel.page), 'utf8')
assert.match(page, /V18 approved review authority/)
assert.match(page, /small down-right diagonal/)
assert.match(page, /widening slightly/)
assert.match(page, /loaded and decoded\. Playback unlocked/)
console.log('Kitchen Sink V18 approval verified: exact V11-front family, angled join, splayed basin and two ten-second water loops are approved and hash-pinned; Final/runtime remain unchanged.')
