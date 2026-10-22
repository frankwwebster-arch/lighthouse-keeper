import assert from 'node:assert/strict'
import crypto from 'node:crypto'
import fs from 'node:fs'
import path from 'node:path'

const root = process.cwd()
const approvalPath = path.join(root, 'docs/review/kitchen-broken-motion-workbench-v46-kettle-approval-2026-10-22.json')
const v46 = path.join(root, 'art/drafts/kitchen-ligne-claire-complete-review-2026-10-22-v46')
const v50 = path.join(root, 'art/drafts/kitchen-ligne-claire-complete-review-2026-10-22-v50')
const public46 = path.join(root, 'public/keeper-review/kitchen-ligne-claire-complete-review-v46/index.html')
const public50 = path.join(root, 'public/keeper-review/kitchen-ligne-claire-complete-review-v50/index.html')

const sha = file => crypto.createHash('sha256').update(fs.readFileSync(file)).digest('hex')
const approval = JSON.parse(fs.readFileSync(approvalPath, 'utf8'))

assert.equal(approval.approvedBy, 'Frank')
assert.equal(approval.approvalWords, 'kettle is approved')
assert.equal(approval.promotion, 'none')
assert.equal(approval.runtimeChanged, false)
assert.equal(approval.dishwasherDecision.status, 'rejected')
assert.equal(approval.successorInheritance.dishwasherApproval, false)

const expected = {
  manifest: path.join(v46, 'manifest.json'),
  batchRegister: path.join(v46, 'batch-register.json'),
  reviewShell: public46,
  v50SuccessorManifest: path.join(v50, 'manifest.json'),
  v50SuccessorReviewShell: public50,
  kettleOff: path.join(v50, 'candidates/kettle--kettle-off.png'),
  kettleOn: path.join(v50, 'candidates/kettle--kettle-on.png'),
  kettleBroken: path.join(v50, 'candidates/kettle--kettle-broken.png'),
  brokenBodyLayer: path.join(v50, 'components/kettle-broken-body.png'),
  brokenLidLayer: path.join(v50, 'components/kettle-broken-lid.png'),
  replaceablePlaceholderSfx: path.join(v50, 'audio/broken-appliance-metal-rattle-placeholder.wav'),
}
for (const [key, file] of Object.entries(expected)) {
  assert.equal(sha(file), approval.hashes[key], `${key} approval hash drift`)
}

const manifest46 = JSON.parse(fs.readFileSync(path.join(v46, 'manifest.json'), 'utf8'))
const manifest50 = JSON.parse(fs.readFileSync(path.join(v50, 'manifest.json'), 'utf8'))
for (const manifest of [manifest46, manifest50]) {
  assert.deepEqual(manifest.brokenApplianceMotion.modes, ['off', 'subtle', 'emphatic'])
  assert.equal(manifest.brokenApplianceMotion.sfx.independentToggle, true)
  assert.equal(manifest.brokenApplianceMotion.sfx.defaultEnabled, false)
  assert.equal(manifest.brokenApplianceMotion.environmentalEffects.inheritObjectTransform, false)
  for (const key of ['synchronous', 'zeroTransforms', 'cancelPendingSfx', 'stopActiveSoundNodes', 'releaseMovementLock']) {
    assert.equal(manifest.brokenApplianceMotion.repair[key], true, `repair.${key} drift`)
  }
  assert.equal(manifest.registration.register, false)
  assert.equal(manifest.registration.promote, false)
}

assert.equal(sha(path.join(v46, 'components/kettle-broken-body.png')), approval.hashes.brokenBodyLayer)
assert.equal(sha(path.join(v46, 'components/kettle-broken-lid.png')), approval.hashes.brokenLidLayer)
assert.equal(sha(path.join(v46, 'audio/broken-appliance-metal-rattle-placeholder.wav')), approval.hashes.replaceablePlaceholderSfx)

console.log('Verified kettle motion/SFX approval: exact V46/V50 inheritance, three modes, anchored steam, replaceable SFX and closed dishwasher gate.')
