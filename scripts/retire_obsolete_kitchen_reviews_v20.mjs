#!/usr/bin/env node
/** Retire Kitchen V1–V4 and V6–V19 review routes without deleting evidence. */
import crypto from 'node:crypto'
import fs from 'node:fs'
import path from 'node:path'
import { fileURLToPath } from 'node:url'

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..')
const obsoleteSets = [
  'kitchen-basic-assets-v1',
  'kitchen-basic-assets-v2',
  'kitchen-basic-assets-v3',
  'kitchen-basic-assets-v4',
  'kitchen-basic-assets-v6-option-b',
  'kitchen-countertop-calibration-v6',
  'kitchen-room-flat-cutaway-v7',
  'kitchen-wall-anchored-v8',
  'kitchen-fridge-shelf-v9',
  'kitchen-porthole-backdrop-cutout-v10',
  'kitchen-kettle-recipe-shelf-v11',
  'kitchen-kettle-recipe-shelf-v12',
  'kitchen-countertop-continuity-v13',
  'kitchen-countertop-no-splashback-v14',
  'kitchen-option-b-clean-surface-v15',
  'kitchen-option-b-silhouette-clean-v16',
  'kitchen-v5-exact-rollback-v17',
  'kitchen-countertop-gate-v18',
  'kitchen-v5-v18-in-situ-comparison-v19',
]

const publicRoot = path.join(root, 'public/keeper-review')
const activeSetsRoot = path.join(root, 'review-archive/sets')
const retiredRoot = path.join(root, 'review-archive/retired/kitchen-v1-v4-v6-v19')
const retiredPages = path.join(retiredRoot, 'review-pages')
const retiredSets = path.join(retiredRoot, 'set-manifests')
fs.mkdirSync(retiredPages, { recursive: true })
fs.mkdirSync(retiredSets, { recursive: true })

for (const set of obsoleteSets) {
  const publicSource = path.join(publicRoot, set)
  const publicTarget = path.join(retiredPages, set)
  if (fs.existsSync(publicSource)) {
    if (fs.existsSync(publicTarget)) fs.rmSync(publicTarget, { recursive: true })
    fs.renameSync(publicSource, publicTarget)
  }
  const manifestSource = path.join(activeSetsRoot, `${set}.json`)
  const manifestTarget = path.join(retiredSets, `${set}.json`)
  if (fs.existsSync(manifestSource)) {
    if (fs.existsSync(manifestTarget)) fs.rmSync(manifestTarget)
    fs.renameSync(manifestSource, manifestTarget)
  }
}

const activeManifests = fs.readdirSync(activeSetsRoot).filter(name => name.endsWith('.json')).sort()
const legacyPaths = {}
for (const name of activeManifests) {
  const manifest = JSON.parse(fs.readFileSync(path.join(activeSetsRoot, name), 'utf8'))
  for (const [legacyPath, entry] of Object.entries(manifest.entries ?? {})) {
    if (legacyPaths[legacyPath]) throw new Error(`duplicate active archive path ${legacyPath}`)
    legacyPaths[legacyPath] = entry
  }
}

const hash = file => crypto.createHash('sha256').update(fs.readFileSync(file)).digest('hex')
const objectRoot = path.join(root, 'review-archive/objects')
const storedObjects = []
for (const prefix of fs.readdirSync(objectRoot).sort()) {
  const directory = path.join(objectRoot, prefix)
  for (const name of fs.readdirSync(directory).sort()) {
    const relative = `review-archive/objects/${prefix}/${name}`
    const file = path.join(root, relative)
    const digest = name.split('.')[0]
    if (hash(file) !== digest) throw new Error(`corrupt retained archive object ${relative}`)
    storedObjects.push([relative, fs.statSync(file).size])
  }
}

let logicalBytes = 0
for (const entry of Object.values(legacyPaths)) {
  if (!fs.existsSync(path.join(root, entry.object))) throw new Error(`missing active object ${entry.object}`)
  logicalBytes += entry.bytes
}
const uniqueBytes = storedObjects.reduce((sum, [, bytes]) => sum + bytes, 0)
const previous = JSON.parse(fs.readFileSync(path.join(root, 'review-archive/index.json'), 'utf8'))
const index = {
  version: 1,
  generatedOn: new Date().toISOString().slice(0, 10),
  objectsBaseUrl: previous.objectsBaseUrl,
  mediaExtensions: previous.mediaExtensions,
  stats: {
    setCount: activeManifests.length,
    referenceCount: Object.keys(legacyPaths).length,
    uniqueObjectCount: storedObjects.length,
    logicalBytes,
    uniqueBytes,
    deduplicatedBytes: logicalBytes - uniqueBytes,
  },
  legacyPaths: Object.fromEntries(Object.entries(legacyPaths).sort(([a], [b]) => a.localeCompare(b))),
}
fs.writeFileSync(path.join(root, 'review-archive/index.json'), `${JSON.stringify(index, null, 2)}\n`)

const record = {
  retiredOn: new Date().toISOString().slice(0, 10),
  reason: 'Frank retained exact V5 and replaced the disconnected furniture approach with V20; obsolete review routes must not remain published.',
  retainedOldFamily: 'kitchen-basic-assets-v5',
  activeReplacement: 'kitchen-fitted-galley-v20',
  retiredSets: obsoleteSets,
  evidence: {
    artTreesRemainInPlace: true,
    reviewPages: 'review-pages/',
    setManifests: 'set-manifests/',
    mediaObjects: '../../objects/',
    publiclyRouted: false,
  },
}
fs.writeFileSync(path.join(retiredRoot, 'RETIREMENT.json'), `${JSON.stringify(record, null, 2)}\n`)
fs.writeFileSync(path.join(retiredRoot, 'README.md'), `# Retired kitchen review evidence\n\nKitchen V1–V4 and V6–V19 were removed from the public review tooling on 17 October 2026 at Frank's direction. Their source/raw/draft art trees remain under \`art/\`; their immutable page files and set manifests are retained here; their content-addressed media bytes remain under \`review-archive/objects/\`.\n\nThese files are evidence only. Do not copy them back under \`public/keeper-review\` or \`review-archive/sets\`. Exact V5 is the only retained old-family public review; V20 is the active fitted-galley replacement gate.\n`)

console.log(JSON.stringify({ retiredSets: obsoleteSets.length, activeSets: activeManifests.length, activeReferences: index.stats.referenceCount, retainedObjects: storedObjects.length }, null, 2))
