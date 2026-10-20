#!/usr/bin/env node
import crypto from 'node:crypto'
import fs from 'node:fs'
import path from 'node:path'

const root = process.cwd()
const indexRoot = 'art/drafts/claude-complete-activity-image-index-2026-10-21-v4'
const previousRoot = 'art/drafts/claude-complete-activity-image-index-2026-10-20-v3'
const cleaningRoot = 'art/drafts/claude-household-cleaning-cupboard-pack-2026-10-21-v1'
const activityRoot = 'art/drafts/claude-activity-cloud-review-pack-2026-10-20-v1'
const foodRoot = 'art/drafts/claude-bbq-food-asset-pack-2026-10-20-v1'
const toolsRoot = 'art/drafts/claude-bbq-tools-ephemera-pack-2026-10-20-v1'
const kitchenRoot = 'art/drafts/claude-kitchen-condiments-prep-pack-2026-10-20-v1'
const abs = value => path.join(root, value)
const sha = value => crypto.createHash('sha256').update(fs.readFileSync(abs(value))).digest('hex')
const bytes = value => fs.statSync(abs(value)).size
const json = value => JSON.parse(fs.readFileSync(abs(value), 'utf8'))
const previous = json(`${previousRoot}/image-ledger.json`)
const cleaning = json(`${cleaningRoot}/asset-manifest.json`)
const activity = json(`${activityRoot}/asset-manifest.json`)
const food = json(`${foodRoot}/asset-manifest.json`)
const tools = json(`${toolsRoot}/asset-manifest.json`)
const kitchen = json(`${kitchenRoot}/asset-manifest.json`)

const direct = (file, kind, pixels, preservation) => ({
  file, kind, pixels, preservation, sha256: sha(file), bytes: bytes(file),
})

const accepted = Object.entries(cleaning.components).map(([componentId, component]) => ({
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

const rejected = cleaning.rejectedGenerations.map(item => ({
  cacheFile: item.cacheFile,
  originalSha256: item.originalGeneratedPngSha256,
  originalPixels: item.originalGeneratedGeometry,
  role: item.role,
  status: 'rejected-retained',
  rejectionReason: item.reason,
  representations: [direct(item.file, 'rejected-evidence', item.pixels, item.preservation)],
}))

const generatedOutputs = [...previous.generatedOutputs, ...accepted, ...rejected]
if (generatedOutputs.length !== 73) throw new Error(`expected 73 generated outputs, found ${generatedOutputs.length}`)
if (new Set(generatedOutputs.map(item => item.cacheFile)).size !== 73) throw new Error('duplicate generated cache filename')
if (new Set(generatedOutputs.map(item => item.originalSha256)).size !== 73) throw new Error('duplicate generated hash')

const activityRoles = new Set(['activity-object', 'original-comic-symbol', 'generic-action-symbol-v7'])
const inheritedBubbleAssets = activity.files
  .filter(item => activityRoles.has(item.role))
  .map(item => ({
    id: path.basename(item.path, path.extname(item.path)),
    family: item.role,
    pack: activityRoot,
    file: `${activityRoot}/${item.path}`,
    sha256: item.sha256,
  }))
const componentAssets = (manifest, pack, family) => Object.entries(manifest.components).map(([id, item]) => ({
  id,
  family: item.family || family,
  pack,
  file: item.file,
  sha256: item.sha256,
}))
const bubbleAssets = [
  ...inheritedBubbleAssets,
  ...componentAssets(food, foodRoot, 'bbq-food'),
  ...componentAssets(tools, toolsRoot, 'bbq-tool'),
  ...componentAssets(kitchen, kitchenRoot, 'kitchen-prop'),
  ...componentAssets(cleaning, cleaningRoot, 'cleaning-prop'),
]
if (bubbleAssets.length !== 89) throw new Error(`expected 89 bubble assets, found ${bubbleAssets.length}`)
if (new Set(bubbleAssets.map(item => item.file)).size !== 89) throw new Error('duplicate bubble asset file')
for (const item of bubbleAssets) {
  if (!fs.existsSync(abs(item.file))) throw new Error(`missing bubble asset: ${item.file}`)
  if (sha(item.file) !== item.sha256) throw new Error(`bubble asset hash mismatch: ${item.file}`)
}
const bubbleCatalogueFile = `${indexRoot}/bubble-assets.json`
fs.mkdirSync(abs(indexRoot), { recursive: true })
fs.writeFileSync(abs(bubbleCatalogueFile), `${JSON.stringify({
  schema: 'lighthouse-keeper/claude-activity-bubble-assets@1',
  created: '2026-10-21',
  status: 'review-only',
  canonicalReferencePage: 'public/keeper-review/activity-cloud-composer-v5/index.html',
  note: 'Accepted image assets suitable for bubble composition. Prime body frames, source-only art and rejected evidence are intentionally excluded.',
  count: bubbleAssets.length,
  assets: bubbleAssets,
}, null, 2)}\n`)

const cleaningManifest = `${cleaningRoot}/asset-manifest.json`
const ledger = {
  schema: 'lighthouse-keeper/claude-complete-activity-image-index@4',
  created: '2026-10-21',
  status: 'review-only-complete-chat-image-ledger',
  supersedes: previousRoot,
  precedence: 'This ledger extends V3 with every accepted and rejected household cleaning-cupboard generation. It changes coverage metadata only and does not modify any inherited immutable pack.',
  counts: {
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
  },
  packInventories: [
    ...previous.packInventories,
    {
      root: cleaningRoot,
      manifest: cleaningManifest,
      manifestSha256: sha(cleaningManifest),
      imageFiles: 63,
      finalUsableAssets: Object.keys(cleaning.components).length,
      rejectedGenerationsRetained: cleaning.rejectedGenerations.length,
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
    recoveredAttemptsAreNotCandidates: true,
    cleaningRejectedAttemptsAreNotCandidates: true,
    allAcceptedAssetsIndependent: true,
    runtimeChanged: false,
    kitchenAuthorityChanged: false,
    primeChanged: false,
    deployed: false,
  },
}

fs.writeFileSync(abs(`${indexRoot}/image-ledger.json`), `${JSON.stringify(ledger, null, 2)}\n`)
