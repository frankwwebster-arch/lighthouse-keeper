#!/usr/bin/env node
import assert from 'node:assert/strict'
import crypto from 'node:crypto'
import fs from 'node:fs'
import path from 'node:path'

const root = process.cwd()
const indexRoot = 'art/drafts/claude-complete-activity-image-index-2026-10-21-v4'
const abs = value => path.join(root, value)
const sha = value => crypto.createHash('sha256').update(fs.readFileSync(abs(value))).digest('hex')
const ledger = JSON.parse(fs.readFileSync(abs(`${indexRoot}/image-ledger.json`), 'utf8'))
const bubbleCatalogue = JSON.parse(fs.readFileSync(abs(`${indexRoot}/bubble-assets.json`), 'utf8'))

assert.equal(ledger.schema, 'lighthouse-keeper/claude-complete-activity-image-index@4')
assert.equal(ledger.status, 'review-only-complete-chat-image-ledger')
assert.deepEqual(ledger.counts, {
  generatedOutputsInThisChat: 73,
  generatedOutputsRepresentedInRepository: 73,
  previouslyMissingGeneratedOutputsRecovered: 2,
  reviewReadyIndependentAssets: 130,
  activityBubbleReadyAssets: 89,
  immutablePacks: 5,
  activityCloudPackFinalUsableAssets: 74,
  foodPackFinalUsableAssets: 8,
  toolsEphemeraPackFinalUsableAssets: 8,
  kitchenCondimentsPrepPackFinalUsableAssets: 14,
  householdCleaningCupboardPackFinalUsableAssets: 26,
  householdCleaningRejectedGenerationsRetained: 10,
})
assert.equal(ledger.generatedOutputs.length, 73)
assert.equal(new Set(ledger.generatedOutputs.map(item => item.cacheFile)).size, 73)
assert.equal(new Set(ledger.generatedOutputs.map(item => item.originalSha256)).size, 73)
assert.equal(ledger.packInventories.length, 5)
assert.equal(ledger.bubbleAssetCatalogue.file, `${indexRoot}/bubble-assets.json`)
assert.equal(ledger.bubbleAssetCatalogue.sha256, sha(ledger.bubbleAssetCatalogue.file))
assert.equal(ledger.bubbleAssetCatalogue.assets, 89)
assert.equal(ledger.bubbleAssetCatalogue.excludesPrimeBodyFrames, true)
assert.equal(ledger.bubbleAssetCatalogue.excludesRejectedEvidence, true)
assert.equal(bubbleCatalogue.schema, 'lighthouse-keeper/claude-activity-bubble-assets@1')
assert.equal(bubbleCatalogue.count, 89)
assert.equal(bubbleCatalogue.assets.length, 89)
assert.equal(new Set(bubbleCatalogue.assets.map(item => item.file)).size, 89)
assert.ok(bubbleCatalogue.assets.every(item => !item.file.includes('/body/')))
assert.ok(bubbleCatalogue.assets.every(item => !item.file.includes('/rejected/')))
for (const item of bubbleCatalogue.assets) {
  assert.ok(fs.existsSync(abs(item.file)), `missing bubble asset: ${item.file}`)
  assert.equal(item.sha256, sha(item.file), `bubble asset hash mismatch: ${item.file}`)
}

for (const pack of ledger.packInventories) {
  assert.equal(pack.manifestSha256, sha(pack.manifest), `immutable pack manifest drift: ${pack.manifest}`)
  assert.ok(fs.existsSync(abs(`${pack.root}/README.md`)))
  assert.ok(fs.existsSync(abs(`${pack.root}/CLAUDE_REVIEW_PROMPT.md`)))
}
for (const item of ledger.generatedOutputs) {
  assert.match(item.cacheFile, /^exec-[0-9a-f-]+\.png$/)
  assert.match(item.originalSha256, /^[0-9a-f]{64}$/)
  assert.ok(item.representations.length >= 1, `unrepresented output: ${item.cacheFile}`)
  for (const representation of item.representations) {
    assert.ok(fs.existsSync(abs(representation.file)), `missing representation: ${representation.file}`)
    assert.equal(representation.sha256, sha(representation.file), `representation hash mismatch: ${representation.file}`)
    assert.equal(representation.bytes, fs.statSync(abs(representation.file)).size)
  }
}

const cleaningRejected = ledger.generatedOutputs.filter(item => item.status === 'rejected-retained' && item.rejectionReason?.includes('glow'))
assert.equal(cleaningRejected.length, 10)
assert.ok(cleaningRejected.every(item => item.representations.every(value => value.kind === 'rejected-evidence')))
const recovered = ledger.generatedOutputs.filter(item => item.status === 'unselected-intermediate-retained-for-completeness')
assert.equal(recovered.length, 2)
assert.ok(recovered.every(item => item.representations.every(value => value.kind === 'recovered-unselected-generation')))
assert.deepEqual(ledger.checks, {
  allGeneratedOutputsRepresented: true,
  inheritedPacksUnchanged: true,
  recoveredAttemptsAreNotCandidates: true,
  cleaningRejectedAttemptsAreNotCandidates: true,
  allAcceptedAssetsIndependent: true,
  runtimeChanged: false,
  kitchenAuthorityChanged: false,
  primeChanged: false,
  deployed: false,
})

const hashLines = fs.readFileSync(abs(`${indexRoot}/HASHES.sha256`), 'utf8').trim().split('\n')
for (const line of hashLines) {
  const match = line.match(/^([0-9a-f]{64})  (.+)$/)
  assert.ok(match, `invalid hash line: ${line}`)
  assert.equal(sha(`${indexRoot}/${match[2]}`), match[1], `index hash mismatch: ${match[2]}`)
}

console.log(JSON.stringify({
  index: indexRoot,
  chatGenerations: 73,
  represented: 73,
  reviewReadyAssets: 130,
  activityBubbleReadyAssets: 89,
  immutablePacks: 5,
  householdCleaningAssets: 26,
  householdCleaningRejectedRetained: 10,
  runtimeChanged: false,
  kitchenAuthorityChanged: false,
  primeChanged: false,
  deployed: false,
}, null, 2))
