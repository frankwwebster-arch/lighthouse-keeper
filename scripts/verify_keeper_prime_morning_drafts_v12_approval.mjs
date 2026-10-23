import assert from 'node:assert/strict'
import crypto from 'node:crypto'
import fs from 'node:fs'
import path from 'node:path'
import { fileURLToPath } from 'node:url'

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..')
const approvalFile = path.join(root, 'docs/review/keeper-prime-morning-drafts-v12-approval-2026-10-23.json')
const approval = JSON.parse(fs.readFileSync(approvalFile))
const manifest = JSON.parse(fs.readFileSync(path.join(root, approval.approvedBatch.manifest.path)))
const sha256 = file => crypto.createHash('sha256').update(fs.readFileSync(path.join(root, file))).digest('hex')

assert.equal(approval.schema, 'lighthouse-keeper/review-decision@1')
assert.equal(approval.reviewedOn, '2026-10-23')
assert.equal(approval.reviewedBy, 'Frank')
assert.equal(approval.candidate, 'keeper-prime-morning-drafts-v12')
assert.equal(approval.decision, 'approved-all-ten-sequences-as-prime-animation-review-authorities')
assert.equal(manifest.version, 12)
assert.equal(manifest.sequences.length, 10)
assert.equal(manifest.sequences.reduce((sum, sequence) => sum + sequence.frames.length, 0), 162)
assert.equal(approval.scope.sequenceCount, 10)
assert.equal(approval.scope.frameOccurrences, 162)
assert.equal(approval.approvalBoundary.allTenSequencesApproved, true)
assert.equal(approval.approvalBoundary.all162FrameOccurrencesApproved, true)
assert.equal(approval.approvalBoundary.runtimeChanged, false)
assert.equal(approval.approvalBoundary.promotionPerformed, false)
assert.equal(approval.approvalBoundary.promotionAllowedWithoutSeparateInstruction, false)

for (const item of Object.values(approval.approvedBatch)) {
  assert.equal(sha256(item.path), item.sha256, `${item.path}: approval pin changed`)
}

const approvedById = new Map(approval.approvedSequences.map(sequence => [sequence.id, sequence]))
assert.equal(approvedById.size, 10)
for (const sequence of manifest.sequences) {
  const approved = approvedById.get(sequence.id)
  assert.ok(approved, `${sequence.id}: absent from approval`)
  assert.equal(approved.title, sequence.title)
  assert.equal(approved.frames, sequence.frames.length)
  assert.equal(approved.fps, sequence.fps)
  assert.equal(approved.startPose, sequence.startPose)
  assert.equal(approved.endPose, sequence.endPose)
  assert.equal(approved.stripSha256, sequence.draftStrip.sha256)
}

assert.deepEqual(approval.approvedIdentityContract.logicalCell, manifest.dimensions.logicalCell)
assert.deepEqual(approval.approvedIdentityContract.authoringCell, manifest.dimensions.authoringCell)
assert.equal(approval.approvedIdentityContract.authoringScale, manifest.dimensions.scale)
assert.deepEqual(approval.approvedIdentityContract.anchor, manifest.dimensions.anchor)
assert.equal(approval.approvedIdentityContract.capTopY, manifest.dimensions.capTop)
assert.equal(approval.approvedIdentityContract.floorOpaqueY, manifest.dimensions.floorOpaqueY)
assert.deepEqual(approval.approvedIdentityContract.jumperBlueRgb, manifest.colourLock.jumperBlue)
assert.deepEqual(approval.approvedIdentityContract.jumperCreamRgb, manifest.colourLock.jumperCream)
assert.deepEqual(approval.approvedIdentityContract.trousersRgb, manifest.colourLock.trousers)
assert.deepEqual(approval.approvedIdentityContract.bootsRgb, manifest.colourLock.boots)
assert.equal(approval.approvedIdentityContract.frontReviewAuthoritySha256, manifest.reviewAuthorities.front.sha256)
assert.equal(approval.approvedIdentityContract.backReviewAuthoritySha256, manifest.reviewAuthorities.back.sha256)
assert.equal(approval.approvedIdentityContract.sideRightAuthoritySha256, manifest.reviewAuthorities.sideRight.sha256)

const v12Doc = fs.readFileSync(path.join(root, 'docs/PRIME_KEEPER_EXPANDED_ANIMATION_REVIEW_V12_2026-10-23.md'), 'utf8')
const handoff = fs.readFileSync(path.join(root, 'docs/PRIME_KEEPER_NEXT_ANIMATION_RUN_HANDOFF_2026-10-23.md'), 'utf8')
const gaps = JSON.parse(fs.readFileSync(path.join(root, 'data/keeper_prime_animation_gaps.json')))
assert.ok(v12Doc.includes('keeper-prime-morning-drafts-v12-approval-2026-10-23.json'))
assert.ok(handoff.includes('keeper-prime-morning-drafts-v12-approval-2026-10-23.json'))
assert.equal(gaps.reviewDrafts.versionedReviewUrl, '/prime-keeper-animation-drafts-v12')
assert.equal(gaps.reviewDrafts.status, 'approved-review-authorities-awaiting-runtime-integration')
assert.equal(gaps.reviewDrafts.frameOccurrences, 162)
assert.equal(gaps.reviewDrafts.approvedSequences, 10)
assert.equal(gaps.reviewDrafts.approvalRecord, 'docs/review/keeper-prime-morning-drafts-v12-approval-2026-10-23.json')
assert.equal(gaps.nextRunDeferrals.instruction, 'Skip pets and visitors in the next animation run.')
assert.deepEqual(gaps.nextRunDeferrals.interactionIds, ['door_greet', 'with_chat', 'with_cards', 'with_tv', 'pet_feed', 'pet_play'])

console.log('Verified Prime morning drafts V12 approval: 10 sequences, 162 frame occurrences, exact identity contract and immutable hash pins.')
