#!/usr/bin/env node
/** Move Keeper review media into the content-addressed archive. */
import crypto from 'node:crypto'
import fs from 'node:fs'
import path from 'node:path'
import { execFileSync } from 'node:child_process'
import { fileURLToPath } from 'node:url'

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..')
const PUBLIC_ROOT = path.join(ROOT, 'public/keeper-review')
const ARCHIVE_ROOT = path.join(ROOT, 'review-archive')
const SET_ROOT = path.join(ARCHIVE_ROOT, 'sets')
const INDEX = path.join(ARCHIVE_ROOT, 'index.json')
const BASE_URL = 'https://raw.githubusercontent.com/frankwwebster-arch/lighthouse-keeper/main/review-archive/objects'
const MEDIA_EXTENSIONS = new Set(['.png', '.gif', '.jpg', '.jpeg', '.webp', '.avif'])
const LARGE_DATA_EXTENSIONS = new Set(['.json', '.json.gz'])
const LARGE_DATA_THRESHOLD_BYTES = 24 * 1024
const PUBLIC_DATA_EXCEPTIONS = {
  '/keeper-review/activity-cloud-composer-v6/catalogue.json': 'eb5060a665694137ce63a45dcb8f914d1086570393399b1537d37ade660fe2aa',
}
const UNPUBLISHED_HISTORICAL_LINKS = new Set([
  '/keeper-review/keeper-prime-context-workbench-v8/inventory.json',
  '/keeper-review/keeper-prime-context-workbench-v9/inventory.json',
  '/keeper-review/keeper-prime-context-workbench-v10/inventory.json',
])

const sha256 = (buffer) => crypto.createHash('sha256').update(buffer).digest('hex')
const posix = (value) => value.split(path.sep).join('/')
const writeJson = (file, value) => {
  fs.mkdirSync(path.dirname(file), { recursive: true })
  fs.writeFileSync(file, `${JSON.stringify(value, null, 2)}\n`)
}

function walk(directory) {
  if (!fs.existsSync(directory)) return []
  const files = []
  for (const entry of fs.readdirSync(directory, { withFileTypes: true }).sort((a, b) => a.name.localeCompare(b.name))) {
    const absolute = path.join(directory, entry.name)
    if (entry.isDirectory()) files.push(...walk(absolute))
    else if (entry.isFile()) files.push(absolute)
  }
  return files
}

const archiveExtension = file => file.toLowerCase().endsWith('.json.gz') ? '.json.gz' : path.extname(file).toLowerCase()
const legacyPathFor = file => `/${posix(path.relative(path.join(ROOT, 'public'), file))}`
const shouldArchive = file => {
  const extension = archiveExtension(file)
  if (PUBLIC_DATA_EXCEPTIONS[legacyPathFor(file)]) return false
  return MEDIA_EXTENSIONS.has(extension) ||
    (LARGE_DATA_EXTENSIONS.has(extension) && fs.statSync(file).size >= LARGE_DATA_THRESHOLD_BYTES)
}
const trackedObjectFiles = () => execFileSync(
  'git', ['ls-files', '-z', '--', 'review-archive/objects'],
  { cwd: ROOT, encoding: 'utf8', maxBuffer: 32 * 1024 * 1024 },
).split('\0').filter(Boolean).map(file => path.join(ROOT, file))

function pageForSet(setName) {
  const candidate = setName === 'drafts'
    ? path.join(PUBLIC_ROOT, 'index.html')
    : path.join(PUBLIC_ROOT, setName, 'index.html')
  if (!fs.existsSync(candidate)) return null
  const bytes = fs.readFileSync(candidate)
  return {
    path: posix(path.relative(ROOT, candidate)),
    sha256: sha256(bytes),
    bytes: bytes.length,
  }
}

const previous = fs.existsSync(INDEX) ? JSON.parse(fs.readFileSync(INDEX, 'utf8')) : null
const legacyPaths = {}
function retainArchivedEntry(legacyPath, entry, source) {
  const normalized = {
    ...entry,
    url: `${BASE_URL}/${entry.sha256.slice(0, 2)}/${entry.sha256}${entry.extension}`,
  }
  const existing = legacyPaths[legacyPath]
  if (existing && existing.sha256 !== normalized.sha256) {
    throw new Error(`archive manifest conflict for ${legacyPath}: ${existing.sha256} versus ${normalized.sha256} from ${source}`)
  }
  legacyPaths[legacyPath] = normalized
}
for (const [legacyPath, entry] of Object.entries(previous?.legacyPaths ?? {})) {
  retainArchivedEntry(legacyPath, entry, 'previous index')
}
for (const manifestFile of walk(SET_ROOT).filter((file) => path.extname(file) === '.json')) {
  const manifest = JSON.parse(fs.readFileSync(manifestFile, 'utf8'))
  for (const [legacyPath, entry] of Object.entries(manifest.entries ?? {})) {
    retainArchivedEntry(legacyPath, entry, posix(path.relative(ROOT, manifestFile)))
  }
}
for (const [legacyPath, expectedHash] of Object.entries(PUBLIC_DATA_EXCEPTIONS)) {
  const publicFile = path.join(ROOT, 'public', legacyPath.replace(/^\//, ''))
  if (!fs.existsSync(publicFile) || sha256(fs.readFileSync(publicFile)) !== expectedHash) {
    throw new Error(`pinned public review-data exception is missing or changed: ${legacyPath}`)
  }
  delete legacyPaths[legacyPath]
}
const physicalPayloads = walk(PUBLIC_ROOT).filter(shouldArchive)

for (const file of physicalPayloads) {
  const bytes = fs.readFileSync(file)
  const hash = sha256(bytes)
  const extension = archiveExtension(file)
  const objectRelative = `review-archive/objects/${hash.slice(0, 2)}/${hash}${extension}`
  const objectPath = path.join(ROOT, objectRelative)
  if (fs.existsSync(objectPath)) {
    if (sha256(fs.readFileSync(objectPath)) !== hash) throw new Error(`archive object collision: ${objectRelative}`)
  } else {
    fs.mkdirSync(path.dirname(objectPath), { recursive: true })
    fs.copyFileSync(file, objectPath)
  }
  const legacyPath = legacyPathFor(file)
  legacyPaths[legacyPath] = {
    sha256: hash,
    extension,
    bytes: bytes.length,
    object: objectRelative,
    url: `${BASE_URL}/${hash.slice(0, 2)}/${hash}${extension}`,
  }
}

// These optional inventory hyperlinks were intentionally never published;
// their version verifiers require the duplicate files to remain absent.
for (const legacyPath of UNPUBLISHED_HISTORICAL_LINKS) delete legacyPaths[legacyPath]

const orderedPaths = Object.fromEntries(Object.entries(legacyPaths).sort(([a], [b]) => a.localeCompare(b)))
const sets = new Map()
for (const [legacyPath, entry] of Object.entries(orderedPaths)) {
  const relative = legacyPath.replace(/^\/keeper-review\//, '')
  const setName = relative.split('/')[0]
  if (!sets.has(setName)) sets.set(setName, {})
  sets.get(setName)[legacyPath] = entry
}

fs.mkdirSync(SET_ROOT, { recursive: true })
for (const [setName, entries] of [...sets.entries()].sort(([a], [b]) => a.localeCompare(b))) {
  writeJson(path.join(SET_ROOT, `${setName}.json`), {
    version: 1,
    set: setName,
    page: pageForSet(setName),
    objectsBaseUrl: BASE_URL,
    entries,
  })
}

let logicalBytes = 0
for (const entry of Object.values(orderedPaths)) {
  logicalBytes += entry.bytes
}
// Only count committed objects plus objects referenced by the rebuilt index.
// Untracked, unrelated draft objects may coexist in a working tree and must
// not make an archive refresh non-deterministic or absorb another task's work.
const retainedObjectFiles = [...new Set([
  ...trackedObjectFiles(),
  ...Object.values(orderedPaths).map(entry => path.join(ROOT, entry.object)),
])].sort((a, b) => a.localeCompare(b))
for (const file of retainedObjectFiles) {
  if (!fs.existsSync(file)) throw new Error(`retained archive object is missing: ${posix(path.relative(ROOT, file))}`)
}
const uniqueBytes = retainedObjectFiles.reduce((sum, file) => sum + fs.statSync(file).size, 0)
writeJson(INDEX, {
  version: 1,
  objectsBaseUrl: BASE_URL,
  mediaExtensions: [...MEDIA_EXTENSIONS].sort(),
  largeDataExtensions: [...LARGE_DATA_EXTENSIONS].sort(),
  largeDataThresholdBytes: LARGE_DATA_THRESHOLD_BYTES,
  stats: {
    setCount: sets.size,
    referenceCount: Object.keys(orderedPaths).length,
    uniqueObjectCount: retainedObjectFiles.length,
    logicalBytes,
    uniqueBytes,
    deduplicatedBytes: logicalBytes - uniqueBytes,
  },
  legacyPaths: orderedPaths,
})

// Removal is last: re-read the generated global and per-set manifests and
// prove that both declarations and the stored object match the public bytes.
const writtenIndex = JSON.parse(fs.readFileSync(INDEX, 'utf8'))
for (const file of physicalPayloads) {
  const bytes = fs.readFileSync(file)
  const expectedHash = sha256(bytes)
  const legacyPath = legacyPathFor(file)
  const setName = legacyPath.replace(/^\/keeper-review\//, '').split('/')[0]
  const setManifest = JSON.parse(fs.readFileSync(path.join(SET_ROOT, `${setName}.json`), 'utf8'))
  const globalEntry = writtenIndex.legacyPaths[legacyPath]
  const setEntry = setManifest.entries[legacyPath]
  if (!globalEntry || !setEntry || JSON.stringify(globalEntry) !== JSON.stringify(setEntry)) {
    throw new Error(`refusing to remove ${legacyPath}: generated manifests do not agree`)
  }
  const objectFile = path.join(ROOT, globalEntry.object)
  if (globalEntry.sha256 !== expectedHash || !fs.existsSync(objectFile) || sha256(fs.readFileSync(objectFile)) !== expectedHash) {
    throw new Error(`refusing to remove ${legacyPath}: archived object/hash verification failed`)
  }
  fs.unlinkSync(file)
}
for (const directory of walkDirectories(PUBLIC_ROOT).sort((a, b) => b.length - a.length)) {
  if (directory !== PUBLIC_ROOT && fs.readdirSync(directory).length === 0) fs.rmdirSync(directory)
}

function walkDirectories(directory) {
  if (!fs.existsSync(directory)) return []
  const result = [directory]
  for (const entry of fs.readdirSync(directory, { withFileTypes: true })) {
    if (entry.isDirectory()) result.push(...walkDirectories(path.join(directory, entry.name)))
  }
  return result
}

console.log(JSON.stringify({
  archivedReferences: Object.keys(orderedPaths).length,
  archivedThisRun: physicalPayloads.length,
  uniqueObjects: retainedObjectFiles.length,
  logicalMiB: Number((logicalBytes / 1024 / 1024).toFixed(2)),
  uniqueMiB: Number((uniqueBytes / 1024 / 1024).toFixed(2)),
  savedPerDeploymentMiB: Number((logicalBytes / 1024 / 1024).toFixed(2)),
}, null, 2))
