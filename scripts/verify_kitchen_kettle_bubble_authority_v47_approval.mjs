#!/usr/bin/env node
/** Pin Frank's exact Kitchen Kettle Bubble Authority V47 approval. */
import assert from 'node:assert/strict'
import crypto from 'node:crypto'
import fs from 'node:fs'
import path from 'node:path'

const root = process.cwd()
const pack = 'art/drafts/kitchen-kettle-bubble-authority-2026-10-22-v47'
const approval = JSON.parse(fs.readFileSync(path.join(root, 'docs/review/kitchen-kettle-bubble-authority-v47-approval-2026-10-22.json')))
const manifest = JSON.parse(fs.readFileSync(path.join(root, pack, 'manifest.json')))
const sha = file => crypto.createHash('sha256').update(fs.readFileSync(path.join(root, file))).digest('hex')

assert.equal(approval.schema, 'lighthouse-keeper/kitchen-review-approval@1')
assert.equal(approval.set, 'kitchen-kettle-bubble-authority-v47')
assert.equal(approval.approvedBy, 'Frank')
assert.equal(approval.approvalWords, 'Approve Kettle V47.')
assert.equal(approval.reviewCommit, 'd35a4837')
assert.equal(approval.visualAuthority, 'current-approved-kitchen-kettle-family')
assert.equal(approval.promotion, 'none')
assert.equal(approval.runtimeChanged, false)
assert.equal(approval.finalChanged, false)
assert.equal(approval.sourceOverwritten, false)

assert.equal(manifest.set, approval.set)
assert.equal(manifest.status, 'immutable-review-candidate-not-approved-not-promoted')
assert.deepEqual(manifest.registration, {
  register: false,
  promote: false,
  runtimeChanged: false,
  approvalRequired: true,
})
assert.equal(manifest.intactGuarantee.offAndOnByteIdentical, true)
assert.equal(manifest.intactGuarantee.bodyPixelsByteIdenticalToApprovedBubble, true)
assert.deepEqual(manifest.preservedV45Contract.brokenSteamAnchor, {
  dx: 27,
  dy: -78,
  reason: 'asset-local placement of the unchanged animated effect; V47 moves it to the fully open top',
})

const files = {
  manifest: `${pack}/manifest.json`,
  hashRegister: `${pack}/HASHES.sha256`,
  kettleOff: `${pack}/states/kettle-off.png`,
  kettleOn: `${pack}/states/kettle-on.png`,
  kettleBroken: `${pack}/states/kettle-broken.png`,
  approvedSteam: `${pack}/states/kettle-approved-steam-isolated.png`,
  stateFamilyEvidence: `${pack}/evidence/state-family-light-dark-64.png`,
  roomEvidence: `${pack}/evidence/exact-v45-room-retina-proof.png`,
  brokenSteamCompact: `${pack}/effects/fx-kettle-broken-steam--compact-f40.png`,
  brokenSteamRegular: `${pack}/effects/fx-kettle-broken-steam--regular-f40.png`,
  brokenSteamEmphatic: `${pack}/effects/fx-kettle-broken-steam--emphatic-f40.png`,
  onSteamCompact: `${pack}/effects/fx-kettle-on-steam--compact-f40.png`,
  onSteamRegular: `${pack}/effects/fx-kettle-on-steam--regular-f40.png`,
  onSteamEmphatic: `${pack}/effects/fx-kettle-on-steam--emphatic-f40.png`,
}
for (const [key, file] of Object.entries(files)) {
  assert.equal(sha(file), approval.hashes[key], `${key} approval hash drifted`)
}

assert.equal(approval.hashes.kettleOff, approval.hashes.kettleOn)
console.log('Kitchen Kettle Bubble Authority V47 approval verified: exact art and inherited V45 contract pinned; runtime promotion and future vibration/SFX remain separate.')
