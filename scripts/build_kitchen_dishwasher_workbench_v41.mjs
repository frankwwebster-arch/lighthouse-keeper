#!/usr/bin/env node
/** Build V41: byte-identical V40 art with the canonical Broken-state movement lock. */
import crypto from 'node:crypto'
import fs from 'node:fs'
import path from 'node:path'

const root = process.cwd()
const set = 'kitchen-dishwasher-workbench-v41'
const batch = 'kitchen-dishwasher-workbench-2026-10-20-v41'
const raw = path.join(root, 'art/raw', batch)
const draft = path.join(root, 'art/drafts', batch)
const review = path.join(root, 'public/keeper-review', set)
const template = path.join(root, 'scripts/templates/kitchen_dishwasher_workbench_v41.html')
const v40Raw = path.join(root, 'art/raw/kitchen-dishwasher-workbench-2026-10-20-v40')
const v40Catalogue = path.join(root, 'art/drafts/kitchen-dishwasher-workbench-2026-10-20-v40/candidate-catalogue.json')
const sha = file => crypto.createHash('sha256').update(fs.readFileSync(file)).digest('hex')

for (const file of [template, v40Catalogue]) if (!fs.existsSync(file)) throw new Error(`Missing authority: ${file}`)
for (const dir of [raw, draft, review]) {
  fs.mkdirSync(dir, { recursive: true })
  for (const item of fs.readdirSync(dir)) fs.rmSync(path.join(dir, item), { recursive: true, force: true })
}

const v40 = JSON.parse(fs.readFileSync(v40Catalogue, 'utf8'))
const outputs = []
for (const name of Object.keys(v40.publishedAssets)) {
  const source = path.join(v40Raw, name)
  if (!fs.existsSync(source)) throw new Error(`Missing V40 asset: ${source}`)
  const output = path.join(raw, name)
  fs.copyFileSync(source, output)
  outputs.push(output)
}

const brokenAssetLock = {
  scope: 'every movable kitchen asset',
  lockState: 'broken',
  lockedAssetPosition: 'retain exact snapped grid origin until repaired',
  directMove: 'reject',
  displacementBySwap: 'reject',
  groupMoveIncludingLockedAsset: 'reject',
  unlockTransition: 'repair to any non-broken state',
  effectOwnership: 'every applied environmental layer stores anchorAssetId and asset-local dx/dy',
  persistence: 'save asset state, exact grid origin, effect owner and local transform together',
}
const snapContract = {
  ...v40.snapContract,
  brokenAssetsMovable: false,
  moveIntoBrokenOccupiedBay: 'reject',
  groupMoveIncludingBrokenAsset: 'reject',
  repairUnlocksMovement: true,
}
const effects = Object.fromEntries(Object.entries(v40.effects).map(([id, effect]) => [id, {
  ...effect,
  anchorAssetId: effect.asset,
  transformSpace: 'asset-local',
  remainsAttachedWhileBroken: true,
}]))
const publishedAssets = Object.fromEntries(outputs.map(file => [path.basename(file), sha(file)]))
const catalogue = {
  ...v40,
  set,
  version: 41,
  status: 'reversible-unapproved-unpromoted',
  authorities: {
    v40Catalogue: { file: path.relative(root, v40Catalogue), sha256: sha(v40Catalogue) },
  },
  sourceProvenance: {
    mode: 'behaviour-only successor; all review art copied byte-identically from V40',
    v40RawDirectory: path.relative(root, v40Raw),
  },
  effects,
  snapContract,
  brokenAssetLock,
  boundaries: { ...v40.boundaries, v40Changed: false, runtimeControllerImplemented: false },
  publishedAssets,
}

const catalogueFile = path.join(draft, 'candidate-catalogue.json')
fs.writeFileSync(catalogueFile, `${JSON.stringify(catalogue, null, 2)}\n`)
const shell = path.join(review, 'index.html')
fs.writeFileSync(shell, fs.readFileSync(template, 'utf8').replace('__DATA__', JSON.stringify(catalogue)))
const register = {
  schema: 'lighthouse-keeper/reversible-review-batch@1',
  set,
  status: catalogue.status,
  candidate: {
    catalogue: { file: path.relative(root, catalogueFile), sha256: sha(catalogueFile) },
    publicShell: { file: path.relative(root, shell), sha256: sha(shell) },
  },
  sources: [{ file: path.relative(root, v40Catalogue), sha256: sha(v40Catalogue) }],
  publishedAssets: outputs.map(file => ({
    source: path.relative(root, file),
    sourceSha256: sha(file),
    publicAssemblyPath: path.posix.join('public/keeper-review', set, 'assets', path.basename(file)),
  })),
}
fs.writeFileSync(path.join(draft, 'batch-register.json'), `${JSON.stringify(register, null, 2)}\n`)
console.log('Built Kitchen Dishwasher Workbench V41: V40 art unchanged; Broken locks position and owns local effects')
