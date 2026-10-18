#!/usr/bin/env node
/** Verify Frank's immutable approval of exact Kitchen Bin Effects V31. */
import assert from 'node:assert/strict'
import crypto from 'node:crypto'
import fs from 'node:fs'
import path from 'node:path'

const root = path.resolve(import.meta.dirname, '..')
const file = (name) => path.join(root, name)
const readJson = (name) => JSON.parse(fs.readFileSync(file(name), 'utf8'))
const sha = (name) => crypto.createHash('sha256').update(fs.readFileSync(file(name))).digest('hex')
const rel = {
  decision: 'docs/review/kitchen-bin-effects-v31-approval-2026-10-18.json',
  catalogue: 'art/drafts/kitchen-bin-effects-2026-10-18-v31/candidate-catalogue.json',
  register: 'art/drafts/kitchen-bin-effects-2026-10-18-v31/batch-register.json',
  page: 'public/keeper-review/kitchen-bin-effects-v31/index.html',
  archive: 'review-archive/sets/kitchen-bin-effects-v31.json',
}
for (const name of Object.values(rel)) assert.ok(fs.existsSync(file(name)), `missing ${name}`)

const decision = readJson(rel.decision)
const catalogue = readJson(rel.catalogue)
const register = readJson(rel.register)
const archive = readJson(rel.archive)
assert.equal(decision.schema, 'lighthouse-keeper/review-decision@1')
assert.equal(decision.reviewedOn, '2026-10-18')
assert.equal(decision.reviewedBy, 'Frank')
assert.equal(decision.candidate, 'kitchen-bin-effects-2026-10-18-v31')
assert.equal(decision.decision, 'approved-as-kitchen-bin-fault-review-authority')
assert.equal(decision.wording, 'excellent, approved')
assert.equal(decision.approvedHashes.candidateCatalogue, sha(rel.catalogue))
assert.equal(decision.approvedHashes.batchRegister, sha(rel.register))
assert.equal(decision.approvedHashes.reviewPage, sha(rel.page))
assert.equal(decision.approvedHashes.archiveManifest, sha(rel.archive))

assert.equal(catalogue.status, 'approved-comic-readable-stench-review-authority')
assert.equal(register.status, 'approved-review-authority')
assert.equal(register.approvedOn, '2026-10-18')
assert.equal(catalogue.boundaries.approved, true)
for (const [name, approvedHash] of Object.entries(decision.approvedHashes.outputs)) {
  const raw = `art/raw/kitchen-bin-effects-2026-10-18-v31/${name}`
  assert.equal(sha(raw), approvedHash, `${name} changed after approval`)
  assert.equal(catalogue.outputs[name].sha256, approvedHash)
  assert.equal(archive.entries[`/keeper-review/kitchen-bin-effects-v31/assets/${name}`].sha256, approvedHash)
}
assert.equal(Object.keys(archive.entries).length, 6)
for (const effect of Object.values(catalogue.effects)) {
  assert.equal(effect.reusable, true)
  assert.equal(effect.frames, 40)
  assert.equal(effect.fps, 4)
  assert.equal(effect.durationSeconds, 10)
  assert.deepEqual(effect.cellPixels, [80, 80])
  assert.equal(effect.objectPixelsChanged, false)
}
assert.equal(catalogue.effects.slow_flies.sfxCue, 'kitchen_bin_flies_slow_loop')
for (const flag of [
  'standardAndOverflowingObjectFamilyApproved', 'objectPixelsUnchangedFromV28',
  'environmentalFxAreSeparateReusableLayers', 'stenchUsesThreeCurlingGreenTrailsAndLooseHaze',
  'transparentFrameGutters', 'placeholderSfxCuePresent',
]) assert.equal(decision.approvedContract[flag], true, `${flag} changed`)
assert.equal(decision.approvedContract.objectAnimated, false)
assert.equal(decision.approvedContract.flyCount, 3)
assert.equal(decision.approvedContract.durationSeconds, 10)
for (const flag of ['kitchenBinFaultReviewAuthorityApproved', 'v20ThroughV30RemainImmutable']) assert.equal(decision.approvalBoundary[flag], true)
for (const flag of ['finalChanged', 'runtimeChanged', 'productionAssetsChanged', 'promotionPerformed', 'promotionAllowedWithoutSeparateInstruction']) assert.equal(decision.approvalBoundary[flag], false, `${flag} boundary changed`)

const page = fs.readFileSync(file(rel.page), 'utf8')
assert.match(page, /three curling green smell trails, loose translucent haze, and three clearly legible slow flies/)
assert.match(page, /loaded and decoded\. Playback unlocked/)
console.log('Kitchen Bin Effects V31 approval verified: exact V28 object family plus ten-second comic stench and fly overlays are approved and hash-pinned; Final/runtime remain unchanged.')
