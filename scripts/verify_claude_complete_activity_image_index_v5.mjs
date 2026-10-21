#!/usr/bin/env node
import assert from 'node:assert/strict'
import crypto from 'node:crypto'
import fs from 'node:fs'
import path from 'node:path'

const root = process.cwd()
const indexRoot = 'art/drafts/claude-complete-activity-image-index-2026-10-21-v5'
const bedroomRoot = 'art/drafts/claude-bedroom-asset-pack-2026-10-21-v1'
const abs = value => path.join(root, value)
const sha = value => crypto.createHash('sha256').update(fs.readFileSync(abs(value))).digest('hex')
const ledger = JSON.parse(fs.readFileSync(abs(`${indexRoot}/image-ledger.json`), 'utf8'))
const bubbleCatalogue = JSON.parse(fs.readFileSync(abs(`${indexRoot}/bubble-assets.json`), 'utf8'))
const bedroom = JSON.parse(fs.readFileSync(abs(`${bedroomRoot}/asset-manifest.json`), 'utf8'))

assert.equal(ledger.schema, 'lighthouse-keeper/claude-complete-activity-image-index@5')
assert.equal(ledger.status, 'review-only-complete-chat-image-ledger')
assert.deepEqual(ledger.counts, {
  generatedOutputsInThisChat: 99,
  generatedOutputsRepresentedInRepository: 99,
  previouslyMissingGeneratedOutputsRecovered: 2,
  reviewReadyIndependentAssets: 156,
  activityBubbleReadyAssets: 115,
  immutablePacks: 6,
  activityCloudPackFinalUsableAssets: 74,
  foodPackFinalUsableAssets: 8,
  toolsEphemeraPackFinalUsableAssets: 8,
  kitchenCondimentsPrepPackFinalUsableAssets: 14,
  householdCleaningCupboardPackFinalUsableAssets: 26,
  householdCleaningRejectedGenerationsRetained: 10,
  bedroomPackFinalUsableAssets: 26,
  bedroomRejectedGenerationsRetained: 0,
})
assert.equal(ledger.generatedOutputs.length, 99)
assert.equal(new Set(ledger.generatedOutputs.map(item => item.cacheFile)).size, 99)
assert.equal(new Set(ledger.generatedOutputs.map(item => item.originalSha256)).size, 99)
assert.equal(ledger.packInventories.length, 6)
assert.equal(ledger.priorIndexPins.ledger.sha256, sha(ledger.priorIndexPins.ledger.file))
assert.equal(ledger.priorIndexPins.bubbleCatalogue.sha256, sha(ledger.priorIndexPins.bubbleCatalogue.file))
assert.equal(ledger.bubbleAssetCatalogue.file, `${indexRoot}/bubble-assets.json`)
assert.equal(ledger.bubbleAssetCatalogue.sha256, sha(ledger.bubbleAssetCatalogue.file))
assert.equal(ledger.bubbleAssetCatalogue.assets, 115)
assert.equal(ledger.bubbleAssetCatalogue.excludesPrimeBodyFrames, true)
assert.equal(ledger.bubbleAssetCatalogue.excludesRejectedEvidence, true)
assert.equal(bubbleCatalogue.schema, 'lighthouse-keeper/claude-activity-bubble-assets@1')
assert.equal(bubbleCatalogue.count, 115)
assert.equal(bubbleCatalogue.assets.length, 115)
assert.equal(new Set(bubbleCatalogue.assets.map(item => item.file)).size, 115)
assert.ok(bubbleCatalogue.assets.every(item => !item.file.includes('/body/')))
assert.ok(bubbleCatalogue.assets.every(item => !item.file.includes('/rejected/')))
const bedroomCatalogueAssets = bubbleCatalogue.assets.filter(item => item.pack === bedroomRoot)
assert.equal(bedroomCatalogueAssets.length, 26)
assert.deepEqual(bedroomCatalogueAssets.map(item => item.id), Object.keys(bedroom.components))
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

const bedroomOutputs = ledger.generatedOutputs.filter(item => item.representations.some(value => value.file.startsWith(`${bedroomRoot}/`)))
assert.equal(bedroomOutputs.length, 26)
assert.ok(bedroomOutputs.every(item => item.status === 'accepted-final'))
assert.deepEqual(ledger.checks, {
  allGeneratedOutputsRepresented: true,
  inheritedPacksUnchanged: true,
  priorIndexHashPinned: true,
  recoveredAttemptsAreNotCandidates: true,
  cleaningRejectedAttemptsAreNotCandidates: true,
  bedroomRejectedAttemptCount: 0,
  allAcceptedAssetsIndependent: true,
  runtimeChanged: false,
  kitchenAuthorityChanged: false,
  primeChanged: false,
  animationAuthorityChanged: false,
  deploymentAuthorityChanged: false,
  composerPageChanged: false,
  deployed: false,
})

const hashLines = fs.readFileSync(abs(`${indexRoot}/HASHES.sha256`), 'utf8').trim().split('\n')
const hashed = new Set()
for (const line of hashLines) {
  const match = line.match(/^([0-9a-f]{64})  (.+)$/)
  assert.ok(match, `invalid hash line: ${line}`)
  assert.equal(sha(`${indexRoot}/${match[2]}`), match[1], `index hash mismatch: ${match[2]}`)
  hashed.add(match[2])
}
assert.deepEqual([...hashed].sort(), fs.readdirSync(abs(indexRoot)).filter(name => name !== 'HASHES.sha256').sort())

console.log(JSON.stringify({
  index: indexRoot,
  chatGenerations: 99,
  represented: 99,
  reviewReadyAssets: 156,
  activityBubbleReadyAssets: 115,
  immutablePacks: 6,
  bedroomAssets: 26,
  bedroomRejectedRetained: 0,
  runtimeChanged: false,
  deployed: false,
}, null, 2))
