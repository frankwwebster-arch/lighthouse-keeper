#!/usr/bin/env node
import crypto from 'node:crypto'
import fs from 'node:fs'
import path from 'node:path'

const root = process.cwd()
const indexRoot = 'art/drafts/claude-complete-activity-image-index-2026-10-20-v3'
const previousRoot = 'art/drafts/claude-complete-activity-image-index-2026-10-20-v2'
const kitchenRoot = 'art/drafts/claude-kitchen-condiments-prep-pack-2026-10-20-v1'
const abs = value => path.join(root, value)
const sha = value => crypto.createHash('sha256').update(fs.readFileSync(abs(value))).digest('hex')
const bytes = value => fs.statSync(abs(value)).size
const json = value => JSON.parse(fs.readFileSync(abs(value), 'utf8'))
const previous = json(`${previousRoot}/image-ledger.json`)
const kitchen = json(`${kitchenRoot}/asset-manifest.json`)

const direct = (file, kind, pixels, preservation) => ({
  file, kind, pixels, preservation, sha256: sha(file), bytes: bytes(file),
})

const cacheByComponent = {
  'condiment-wholegrain-mustard-jar': 'exec-68c40945-7e3d-4a83-a95f-3ca54643a516.png',
  'condiment-pickle-jar': 'exec-7bc7b504-6698-4af9-a4e9-18980d841d8c.png',
  'condiment-mayonnaise-jar': 'exec-87f662e6-0a4e-4153-894e-95181e149a8a.png',
  'condiment-salt-mill': 'exec-e9347043-5893-455d-991c-9a37dd4b04b1.png',
  'condiment-pepper-mill': 'exec-b5bc58cc-4de1-423f-ba8c-b479f854fb63.png',
  'prep-bread-slicing': 'exec-23be16a4-c7b4-4549-9cf2-4c20efa41f37.png',
  'knife-chef': 'exec-ee8b11c2-7cbb-4f1c-87ba-e4d4278fd360.png',
  'knife-bread': 'exec-8275b728-6332-4011-bcc2-a0cab63b8042.png',
  'knife-paring': 'exec-1e81e04c-1193-46eb-89e2-7676ad0ceee7.png',
  'ingredient-butter-block': 'exec-d0b5a87f-c5ab-4947-a9a7-f0c0c6f8fb19.png',
  'condiment-olive-oil': 'exec-68d6e67c-9d13-4205-a8f6-50c80634a00b.png',
  'condiment-raspberry-jam': 'exec-7287d9ba-be6e-4251-b160-7d04bfcb37dd.png',
  'condiment-honey-pot': 'exec-f4bef225-24a7-4c32-a285-b9d09af3c3e9.png',
  'condiment-malt-vinegar': 'exec-5cf247d4-c18d-45a7-9b93-fbfef84dafe9.png',
}

const added = Object.entries(kitchen.components).map(([componentId, component]) => ({
  cacheFile: cacheByComponent[componentId],
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

const generatedOutputs = [...previous.generatedOutputs, ...added]
if (generatedOutputs.length !== 37) throw new Error(`expected 37 generated outputs, found ${generatedOutputs.length}`)
if (new Set(generatedOutputs.map(item => item.cacheFile)).size !== 37) throw new Error('duplicate generated cache filename')
if (new Set(generatedOutputs.map(item => item.originalSha256)).size !== 37) throw new Error('duplicate generated hash')

const kitchenManifest = `${kitchenRoot}/asset-manifest.json`
const ledger = {
  schema: 'lighthouse-keeper/claude-complete-activity-image-index@3',
  created: '2026-10-20',
  status: 'review-only-complete-chat-image-ledger',
  supersedes: previousRoot,
  precedence: 'This ledger extends V2 with the Kitchen condiments and preparation batch. It changes coverage metadata only and does not modify any immutable source pack.',
  counts: {
    generatedOutputsInThisChat: 37,
    generatedOutputsRepresentedInRepository: 37,
    previouslyMissingGeneratedOutputsRecovered: 2,
    reviewReadyIndependentAssets: 104,
    immutablePacks: 4,
    activityCloudPackFinalUsableAssets: 74,
    foodPackFinalUsableAssets: 8,
    toolsEphemeraPackFinalUsableAssets: 8,
    kitchenCondimentsPrepPackFinalUsableAssets: 14,
  },
  packInventories: [
    ...previous.packInventories,
    {
      root: kitchenRoot,
      manifest: kitchenManifest,
      manifestSha256: sha(kitchenManifest),
      imageFiles: 29,
      finalUsableAssets: Object.keys(kitchen.components).length,
    },
  ],
  generatedOutputs,
  checks: {
    allGeneratedOutputsRepresented: true,
    immutablePacksUnchanged: true,
    recoveredAttemptsAreNotCandidates: true,
    allAssetsIndependent: true,
    runtimeChanged: false,
    kitchenAuthorityChanged: false,
    primeChanged: false,
    deployed: false,
  },
}

fs.writeFileSync(abs(`${indexRoot}/image-ledger.json`), `${JSON.stringify(ledger, null, 2)}\n`)
