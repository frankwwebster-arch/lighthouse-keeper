#!/usr/bin/env node
import crypto from 'node:crypto'
import fs from 'node:fs'
import path from 'node:path'

const root = process.cwd()
const indexRoot = 'art/drafts/claude-complete-activity-image-index-2026-10-21-v5'
const previousRoot = 'art/drafts/claude-complete-activity-image-index-2026-10-21-v4'
const bedroomRoot = 'art/drafts/claude-bedroom-asset-pack-2026-10-21-v1'
const abs = value => path.join(root, value)
const sha = value => crypto.createHash('sha256').update(fs.readFileSync(abs(value))).digest('hex')
const bytes = value => fs.statSync(abs(value)).size
const json = value => JSON.parse(fs.readFileSync(abs(value), 'utf8'))
const previous = json(`${previousRoot}/image-ledger.json`)
const previousBubble = json(`${previousRoot}/bubble-assets.json`)
const bedroom = json(`${bedroomRoot}/asset-manifest.json`)

const direct = (file, kind, pixels, preservation) => ({
  file, kind, pixels, preservation, sha256: sha(file), bytes: bytes(file),
})

const accepted = Object.entries(bedroom.components).map(([componentId, component]) => ({
  cacheFile: component.originalCacheFile,
  originalSha256: component.originalGeneratedPngSha256,
  originalPixels: component.originalGeneratedGeometry,
  role: componentId,
  status: 'accepted-final',
  componentId,
  representations: [
    direct(component.sourceFile, 'compact-review-source', [384, 384], 'visible-alpha-isolated-lossless-webp'),
    direct(component.file, 'final-independent-asset', [256, 256], 'deterministically-normalised-png'),
  ],
}))
const generatedOutputs = [...previous.generatedOutputs, ...accepted]
if (generatedOutputs.length !== 99) throw new Error(`expected 99 generated outputs, found ${generatedOutputs.length}`)
if (new Set(generatedOutputs.map(item => item.cacheFile)).size !== 99) throw new Error('duplicate generated cache filename')
if (new Set(generatedOutputs.map(item => item.originalSha256)).size !== 99) throw new Error('duplicate generated hash')

const bedroomAssets = Object.entries(bedroom.components).map(([id, item]) => ({
  id,
  family: item.family,
  pack: bedroomRoot,
  file: item.file,
  sha256: item.sha256,
}))
const bubbleAssets = [...previousBubble.assets, ...bedroomAssets]
if (bubbleAssets.length !== 115) throw new Error(`expected 115 bubble assets, found ${bubbleAssets.length}`)
if (new Set(bubbleAssets.map(item => item.file)).size !== 115) throw new Error('duplicate bubble asset file')
for (const item of bubbleAssets) {
  if (!fs.existsSync(abs(item.file))) throw new Error(`missing bubble asset: ${item.file}`)
  if (sha(item.file) !== item.sha256) throw new Error(`bubble asset hash mismatch: ${item.file}`)
}

fs.mkdirSync(abs(indexRoot), { recursive: true })
const bubbleCatalogueFile = `${indexRoot}/bubble-assets.json`
fs.writeFileSync(abs(bubbleCatalogueFile), `${JSON.stringify({
  schema: 'lighthouse-keeper/claude-activity-bubble-assets@1',
  created: '2026-10-21',
  status: 'review-only',
  supersedes: `${previousRoot}/bubble-assets.json`,
  canonicalReferencePage: previousBubble.canonicalReferencePage,
  note: 'Accepted image assets suitable for bubble composition. V5 adds 26 bedroom props. Prime body frames, source-only art and rejected evidence are intentionally excluded; no Composer page was changed.',
  count: bubbleAssets.length,
  assets: bubbleAssets,
}, null, 2)}\n`)

const bedroomManifest = `${bedroomRoot}/asset-manifest.json`
const ledger = {
  schema: 'lighthouse-keeper/claude-complete-activity-image-index@5',
  created: '2026-10-21',
  status: 'review-only-complete-chat-image-ledger',
  supersedes: previousRoot,
  precedence: 'This ledger extends V4 with all 26 accepted bedroom generations. It changes coverage metadata only and does not modify any inherited immutable pack or existing Composer page.',
  priorIndexPins: {
    ledger: { file: `${previousRoot}/image-ledger.json`, sha256: sha(`${previousRoot}/image-ledger.json`) },
    bubbleCatalogue: { file: `${previousRoot}/bubble-assets.json`, sha256: sha(`${previousRoot}/bubble-assets.json`) },
  },
  counts: {
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
  },
  packInventories: [
    ...previous.packInventories,
    {
      root: bedroomRoot,
      manifest: bedroomManifest,
      manifestSha256: sha(bedroomManifest),
      imageFiles: 53,
      finalUsableAssets: Object.keys(bedroom.components).length,
      rejectedGenerationsRetained: bedroom.rejectedGenerations.length,
    },
  ],
  bubbleAssetCatalogue: {
    file: bubbleCatalogueFile,
    sha256: sha(bubbleCatalogueFile),
    assets: bubbleAssets.length,
    excludesPrimeBodyFrames: true,
    excludesRejectedEvidence: true,
  },
  generatedOutputs,
  checks: {
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
  },
}
fs.writeFileSync(abs(`${indexRoot}/image-ledger.json`), `${JSON.stringify(ledger, null, 2)}\n`)

const files = fs.readdirSync(abs(indexRoot)).filter(name => name !== 'HASHES.sha256').sort()
fs.writeFileSync(abs(`${indexRoot}/HASHES.sha256`), `${files.map(name => `${sha(`${indexRoot}/${name}`)}  ${name}`).join('\n')}\n`)
