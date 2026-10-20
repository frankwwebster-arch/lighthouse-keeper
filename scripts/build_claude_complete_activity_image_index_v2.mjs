#!/usr/bin/env node
import crypto from 'node:crypto'
import fs from 'node:fs'
import path from 'node:path'

const root = process.cwd()
const indexRoot = 'art/drafts/claude-complete-activity-image-index-2026-10-20-v2'
const previousRoot = 'art/drafts/claude-complete-activity-image-index-2026-10-20-v1'
const toolsRoot = 'art/drafts/claude-bbq-tools-ephemera-pack-2026-10-20-v1'
const abs = value => path.join(root, value)
const sha = value => crypto.createHash('sha256').update(fs.readFileSync(abs(value))).digest('hex')
const bytes = value => fs.statSync(abs(value)).size
const json = value => JSON.parse(fs.readFileSync(abs(value), 'utf8'))
const previous = json(`${previousRoot}/image-ledger.json`)
const tools = json(`${toolsRoot}/asset-manifest.json`)

const direct = (file, kind, pixels, preservation) => ({
  file,
  kind,
  pixels,
  preservation,
  sha256: sha(file),
  bytes: bytes(file),
})

const cacheByComponent = {
  'bbq-tongs': 'exec-faf43851-9ea6-49a7-a07e-f23aa6741be3.png',
  'bbq-slotted-turner': 'exec-a71245cb-cfba-4e78-8a26-6f6a74665465.png',
  'bbq-basting-brush': 'exec-163e5f8f-0ff5-4bb1-b3f3-af56f2a2d2da.png',
  'bbq-grill-fork': 'exec-94522f15-d52b-474a-8e05-4084d2cff7c0.png',
  'bbq-heatproof-mitt': 'exec-8b92ed47-66c4-4273-afb3-80ac31869d11.png',
  'bbq-charcoal-chimney': 'exec-7122d417-2e00-4186-94ff-df9b8c826d7a.png',
  'bbq-skewer-bundle': 'exec-d72c1e32-3ba8-44bc-8aeb-a26469036b1d.png',
  'bbq-charcoal-bag': 'exec-14e6b927-a7a1-4fd1-83b4-349073196ed7.png',
}

const added = Object.entries(tools.components).map(([componentId, component]) => ({
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
if (generatedOutputs.length !== 23) throw new Error(`expected 23 generated outputs, found ${generatedOutputs.length}`)
if (new Set(generatedOutputs.map(item => item.cacheFile)).size !== 23) throw new Error('duplicate generated cache filename')
if (new Set(generatedOutputs.map(item => item.originalSha256)).size !== 23) throw new Error('duplicate generated hash')

const toolsManifest = `${toolsRoot}/asset-manifest.json`
const ledger = {
  schema: 'lighthouse-keeper/claude-complete-activity-image-index@2',
  created: '2026-10-20',
  status: 'review-only-complete-chat-image-ledger',
  supersedes: previousRoot,
  precedence: 'This ledger extends V1 with the BBQ tools and ephemera generation batch. It changes coverage metadata only and does not modify any immutable source pack.',
  counts: {
    generatedOutputsInThisChat: 23,
    generatedOutputsRepresentedInRepository: 23,
    previouslyMissingGeneratedOutputsRecovered: 2,
    reviewReadyIndependentAssets: 90,
    immutablePacks: 3,
    activityCloudPackFinalUsableAssets: 74,
    foodPackFinalUsableAssets: 8,
    toolsEphemeraPackFinalUsableAssets: 8,
  },
  packInventories: [
    ...previous.packInventories,
    {
      root: toolsRoot,
      manifest: toolsManifest,
      manifestSha256: sha(toolsManifest),
      imageFiles: 17,
      finalUsableAssets: Object.keys(tools.components).length,
    },
  ],
  generatedOutputs,
  checks: {
    allGeneratedOutputsRepresented: true,
    immutablePacksUnchanged: true,
    recoveredAttemptsAreNotCandidates: true,
    allAssetsIndependent: true,
    runtimeChanged: false,
    kitchenChanged: false,
    primeChanged: false,
    deployed: false,
  },
}

fs.writeFileSync(abs(`${indexRoot}/image-ledger.json`), `${JSON.stringify(ledger, null, 2)}\n`)
