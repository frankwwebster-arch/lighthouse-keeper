#!/usr/bin/env node
import assert from 'node:assert/strict'
import crypto from 'node:crypto'
import fs from 'node:fs'
import path from 'node:path'

const root = process.cwd()
const indexRoot = 'art/drafts/claude-complete-activity-image-index-2026-10-20-v2'
const abs = value => path.join(root, value)
const sha = value => crypto.createHash('sha256').update(fs.readFileSync(abs(value))).digest('hex')
const ledger = JSON.parse(fs.readFileSync(abs(`${indexRoot}/image-ledger.json`), 'utf8'))

assert.equal(ledger.schema, 'lighthouse-keeper/claude-complete-activity-image-index@2')
assert.equal(ledger.status, 'review-only-complete-chat-image-ledger')
assert.deepEqual(ledger.counts, {
  generatedOutputsInThisChat: 23,
  generatedOutputsRepresentedInRepository: 23,
  previouslyMissingGeneratedOutputsRecovered: 2,
  reviewReadyIndependentAssets: 90,
  immutablePacks: 3,
  activityCloudPackFinalUsableAssets: 74,
  foodPackFinalUsableAssets: 8,
  toolsEphemeraPackFinalUsableAssets: 8,
})
assert.equal(ledger.generatedOutputs.length, 23)
assert.equal(new Set(ledger.generatedOutputs.map(item => item.cacheFile)).size, 23)
assert.equal(new Set(ledger.generatedOutputs.map(item => item.originalSha256)).size, 23)
assert.equal(ledger.packInventories.length, 3)

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

const recovered = ledger.generatedOutputs.filter(item => item.status === 'unselected-intermediate-retained-for-completeness')
assert.equal(recovered.length, 2)
assert.ok(recovered.every(item => item.representations.every(value => value.kind === 'recovered-unselected-generation')))
assert.deepEqual(ledger.checks, {
  allGeneratedOutputsRepresented: true,
  immutablePacksUnchanged: true,
  recoveredAttemptsAreNotCandidates: true,
  allAssetsIndependent: true,
  runtimeChanged: false,
  kitchenChanged: false,
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
  chatGenerations: 23,
  represented: 23,
  reviewReadyAssets: 90,
  immutablePacks: 3,
  runtimeChanged: false,
  kitchenChanged: false,
  primeChanged: false,
  deployed: false,
}, null, 2))
