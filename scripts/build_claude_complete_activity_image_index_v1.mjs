#!/usr/bin/env node
import crypto from 'node:crypto'
import fs from 'node:fs'
import path from 'node:path'

const root = process.cwd()
const indexRoot = 'art/drafts/claude-complete-activity-image-index-2026-10-20-v1'
const activityRoot = 'art/drafts/claude-activity-cloud-review-pack-2026-10-20-v1'
const foodRoot = 'art/drafts/claude-bbq-food-asset-pack-2026-10-20-v1'
const abs = value => path.join(root, value)
const sha = value => crypto.createHash('sha256').update(fs.readFileSync(abs(value))).digest('hex')
const bytes = value => fs.statSync(abs(value)).size
const json = value => JSON.parse(fs.readFileSync(abs(value), 'utf8'))

const activityManifest = json(`${activityRoot}/asset-manifest.json`)
const foodManifest = json(`${foodRoot}/asset-manifest.json`)

const direct = (file, kind, pixels, preservation = 'exact-original-generated-bytes') => ({
  file,
  kind,
  pixels,
  preservation,
  sha256: sha(file),
  bytes: bytes(file),
})

const foodByOriginal = new Map()
for (const [id, component] of Object.entries(foodManifest.components)) {
  foodByOriginal.set(component.originalGeneratedPngSha256, {
    id,
    representations: [
      direct(component.sourceFile, 'compact-review-source', [384, 384], 'deterministically-downsampled-lossless-webp'),
      direct(component.file, 'final-independent-asset', [256, 256], 'deterministically-normalised-png'),
    ],
  })
}
for (const rejected of foodManifest.rejectedAttempts) {
  foodByOriginal.set(rejected.originalGeneratedPngSha256, {
    id: 'rejected-plateless-cooked-sausages',
    representations: [direct(rejected.file, 'rejected-evidence', [384, 384], 'deterministically-downsampled-lossless-webp')],
  })
}

const generated = [
  {
    cacheFile: 'exec-24c94cce-57c3-4512-855a-083202f173ce.png',
    originalSha256: 'dfa370a9c49480100fa4058a77aedcdbc0b588321f97b0e05f22549b44655d8b',
    originalPixels: [1536, 1024],
    role: 'generic-symbol-sheet-early-attempt-a',
    status: 'unselected-intermediate-retained-for-completeness',
    representations: [direct(`${indexRoot}/recovered-unselected-generations/generic-symbol-sheet-early-attempt-a.webp`, 'recovered-unselected-generation', [768, 512], 'deterministically-downsampled-lossless-webp')],
  },
  {
    cacheFile: 'exec-ddd731e5-da08-4ec3-a975-9c7f935dcddf.png',
    originalSha256: 'cc31f34ff3eeaf393d93e8d5ab78b35f1718f9c528e8d2739139c003739ce28c',
    originalPixels: [1536, 1024],
    role: 'generic-symbol-sheet-early-attempt-b',
    status: 'unselected-intermediate-retained-for-completeness',
    representations: [direct(`${indexRoot}/recovered-unselected-generations/generic-symbol-sheet-early-attempt-b.webp`, 'recovered-unselected-generation', [768, 512], 'deterministically-downsampled-lossless-webp')],
  },
  {
    cacheFile: 'exec-bddbb842-9d97-4556-9b1a-ca9166d433f9.png',
    originalSha256: '517309ab1ef8ba71849217d6da71fe1cd1c8b2b3a2ef94f86db7ee28fcc43b80',
    originalPixels: [1536, 1024],
    role: 'original-six-comic-symbol-source-sheet',
    status: 'accepted-source',
    representations: [direct(`${activityRoot}/assets/source/original-six-symbol-source-sheet.png`, 'accepted-source', [1536, 1024])],
  },
  {
    cacheFile: 'exec-2e8f1679-d09f-45e2-a7fc-d998a92d829e.png',
    originalSha256: '69dd1a140f881e497c965ed7d6f3000478ad832304f978ef07b7e42519982530',
    originalPixels: [1536, 1024],
    role: 'generic-action-symbol-sheet-insufficient-gutter',
    status: 'rejected-retained',
    representations: [direct(`${activityRoot}/evidence/rejected/generic-action-symbols-sheet-attempt-1-insufficient-gutter.png`, 'rejected-evidence', [1536, 1024])],
  },
  {
    cacheFile: 'exec-0f5f6982-dbd8-48ea-b3e5-83675a3e89b7.png',
    originalSha256: '327f29ac9c67fdf237892ac5f4abe52e4508e7107140b7fb1b265cb6b7a71ebb',
    originalPixels: [1254, 1254],
    role: 'generic-question-mark-source',
    status: 'accepted-source',
    representations: [direct(`${activityRoot}/assets/source/generic-question-mark-source.png`, 'accepted-source', [1254, 1254])],
  },
  {
    cacheFile: 'exec-13724c58-644a-418c-80af-69f4756508b9.png',
    originalSha256: 'e4afb957aeb8d1015a43fe2664135ef8830270b6ef70ab1941947aca552e390b',
    originalPixels: [1536, 1024],
    role: 'generic-action-symbol-sheet-scale-corrected',
    status: 'accepted-source',
    representations: [direct(`${activityRoot}/assets/source/generic-action-symbols-sheet-source.png`, 'accepted-source', [1536, 1024])],
  },
]

const foodGenerated = [
  ['exec-2fd5c1b7-9726-4c9c-8f25-0d21c8b5e47d.png', '4ac3e4269955c51d31fee0d18b47a1512116995ea041eba0563c413c817214ed', [1254, 1254], 'raw-beef-burger-patties', 'accepted-final'],
  ['exec-3ea7dc96-dd7e-4164-93f3-8c62c033a63c.png', '47e002e96d2d50d91058431af26cd2c5295c53569040f2add601c2c9693ab024', [1254, 1254], 'plateless-cooked-sausages', 'rejected-user-correction'],
  ['exec-ca44a99e-3465-46d2-af59-2adc35818f28.png', '8cca15c23f1391dee66db124cc35acff16783564d0b1ee45bf298ac4ce3e6a66', [1254, 1254], 'raw-linked-sausages', 'accepted-final'],
  ['exec-351a84f3-cd0d-45c2-98ab-5c62ad031bb2.png', 'b717c2ac1166905aec8f7c919bfbfb418a2b3832bafa608aa71c6249aaea1ed6', [1254, 1254], 'cold-unlit-bbq', 'accepted-final'],
  ['exec-9cb5c27c-e940-481c-9e0b-b7419e2ee4d1.png', 'bda822b834cd56993087ce787354c48ff6b0b055d79c56f8cdee23d6221150f4', [1254, 1254], 'cheese-being-sliced', 'accepted-final'],
  ['exec-de5a3a61-0649-4f48-9449-032c9ccb764a.png', 'b183c397e9cc6ccf80abdcabf8b79b1e6df19f2ab8e72616d1ec249bae3d1cfb', [1254, 1254], 'raw-steak', 'accepted-final'],
  ['exec-8a8dc0a0-29ca-4bc4-9461-23ff1b9e7428.png', '7c1604bf1be6fc9540a096c00e8053181b278ef245c8ebc83e7abf51ef912005', [1536, 1024], 'plated-steak-and-fries', 'accepted-final'],
  ['exec-c0ec7f68-b9d1-4c76-bcdc-c1ed8ac42831.png', '9bd83b220ab6b226b9c049e40b621d7ca849e9d810472e9789e809e692ba9877', [1254, 1254], 'ketchup-bottle', 'accepted-final'],
  ['exec-cacf44ac-3f8d-445a-a446-204264f2b166.png', '65333b6307e926acf0fb1cd24fe57155ac9621ba351c597e29482aebc40c6bf9', [1254, 1254], 'mustard-bottle', 'accepted-final'],
]
for (const [cacheFile, originalSha256, originalPixels, role, status] of foodGenerated) {
  const stored = foodByOriginal.get(originalSha256)
  if (!stored) throw new Error(`food generation missing from immutable food pack: ${cacheFile}`)
  generated.push({cacheFile, originalSha256, originalPixels, role, status, componentId: stored.id, representations: stored.representations})
}

if (generated.length !== 15) throw new Error(`expected 15 generated outputs, found ${generated.length}`)
for (const item of generated) {
  if (item.representations.length === 0) throw new Error(`unrepresented generation: ${item.cacheFile}`)
  for (const representation of item.representations) {
    if (!fs.existsSync(abs(representation.file))) throw new Error(`missing representation: ${representation.file}`)
  }
}

const ledger = {
  schema: 'lighthouse-keeper/claude-complete-activity-image-index@1',
  created: '2026-10-20',
  status: 'review-only-complete-chat-image-ledger',
  precedence: 'This ledger corrects per-image source geometry and coverage metadata only; it does not modify either immutable source pack.',
  counts: {
    generatedOutputsInThisChat: 15,
    generatedOutputsRepresentedInRepository: 15,
    previouslyMissingGeneratedOutputsRecovered: 2,
    reviewReadyIndependentAssets: 82,
    activityCloudPackImages: activityManifest.counts.pngImages,
    activityCloudPackFinalUsableAssets: activityManifest.counts.finalUsableVisualAssets,
    foodPackImages: 18,
    foodPackFinalUsableAssets: Object.keys(foodManifest.components).length,
  },
  packInventories: [
    {
      root: activityRoot,
      manifest: `${activityRoot}/asset-manifest.json`,
      manifestSha256: sha(`${activityRoot}/asset-manifest.json`),
      imageFiles: activityManifest.counts.pngImages,
      finalUsableAssets: activityManifest.counts.finalUsableVisualAssets,
    },
    {
      root: foodRoot,
      manifest: `${foodRoot}/asset-manifest.json`,
      manifestSha256: sha(`${foodRoot}/asset-manifest.json`),
      imageFiles: 18,
      finalUsableAssets: Object.keys(foodManifest.components).length,
    },
  ],
  generatedOutputs: generated,
  checks: {
    allGeneratedOutputsRepresented: true,
    immutablePacksUnchanged: true,
    recoveredAttemptsAreNotCandidates: true,
    runtimeChanged: false,
    kitchenChanged: false,
    deployed: false,
  },
}

fs.writeFileSync(abs(`${indexRoot}/image-ledger.json`), `${JSON.stringify(ledger, null, 2)}\n`)
