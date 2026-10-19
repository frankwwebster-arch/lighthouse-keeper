#!/usr/bin/env node
/**
 * Replace one immutable review set without absorbing unrelated untracked media.
 *
 * Usage:
 *   node scripts/replace_keeper_review_set.mjs <batch-register.json> [base-ref]
 *
 * The batch register must expose `set`, `publishedAssets`, and
 * `candidate.publicShell.file`. The global resolver is rebuilt from the chosen
 * Git base plus this one set; object-store statistics describe the files that
 * would exist in that committed tree, not every unrelated file in the working
 * directory.
 */
import crypto from 'node:crypto'
import fs from 'node:fs'
import path from 'node:path'
import { execFileSync } from 'node:child_process'
import { fileURLToPath } from 'node:url'

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..')
const REGISTER_FILE = process.argv[2]
const BASE_REF = process.argv[3] ?? 'HEAD'
const BASE_URL = 'https://raw.githubusercontent.com/frankwwebster-arch/lighthouse-keeper/main/review-archive/objects'
const INDEX_FILE = path.join(ROOT, 'review-archive/index.json')
const SET_ROOT = path.join(ROOT, 'review-archive/sets')

if (!REGISTER_FILE) throw new Error('batch-register.json path is required')

const sha256 = buffer => crypto.createHash('sha256').update(buffer).digest('hex')
const posix = value => value.split(path.sep).join('/')
const readJson = file => JSON.parse(fs.readFileSync(file, 'utf8'))
const writeJson = (file, value) => {
  fs.mkdirSync(path.dirname(file), { recursive: true })
  fs.writeFileSync(file, `${JSON.stringify(value, null, 2)}\n`)
}
const git = args => execFileSync('git', args, { cwd: ROOT, encoding: 'utf8', maxBuffer: 32 * 1024 * 1024 })

const registerPath = path.resolve(ROOT, REGISTER_FILE)
const register = readJson(registerPath)
const set = register.set
if (!set || !Array.isArray(register.publishedAssets)) throw new Error('invalid reversible review batch register')

const baseIndex = JSON.parse(git(['show', `${BASE_REF}:review-archive/index.json`]))
const prefix = `/keeper-review/${set}/`
const entries = {}

for (const asset of register.publishedAssets) {
  const source = path.resolve(ROOT, asset.source)
  const bytes = fs.readFileSync(source)
  const hash = sha256(bytes)
  if (hash !== asset.sourceSha256) throw new Error(`source hash changed: ${asset.source}`)
  const extension = path.extname(asset.publicAssemblyPath).toLowerCase()
  const object = `review-archive/objects/${hash.slice(0, 2)}/${hash}${extension}`
  const objectFile = path.join(ROOT, object)
  if (!fs.existsSync(objectFile)) throw new Error(`archive object missing: ${object}`)
  if (sha256(fs.readFileSync(objectFile)) !== hash) throw new Error(`archive object hash changed: ${object}`)
  const legacyPath = `/${posix(asset.publicAssemblyPath).replace(/^public\//, '')}`
  if (!legacyPath.startsWith(prefix)) throw new Error(`asset escaped set prefix: ${legacyPath}`)
  entries[legacyPath] = {
    sha256: hash,
    extension,
    bytes: bytes.length,
    object,
    url: `${BASE_URL}/${hash.slice(0, 2)}/${hash}${extension}`,
  }
}

const shellRelative = posix(register.candidate.publicShell.file)
const shellFile = path.join(ROOT, shellRelative)
const shellBytes = fs.readFileSync(shellFile)
const page = { path: shellRelative, sha256: sha256(shellBytes), bytes: shellBytes.length }
const orderedEntries = Object.fromEntries(Object.entries(entries).sort(([a], [b]) => a.localeCompare(b)))
writeJson(path.join(SET_ROOT, `${set}.json`), {
  version: 1,
  set,
  page,
  objectsBaseUrl: BASE_URL,
  entries: orderedEntries,
})

const legacyPaths = {}
for (const [legacyPath, entry] of Object.entries(baseIndex.legacyPaths)) {
  if (!legacyPath.startsWith(prefix)) legacyPaths[legacyPath] = entry
}
Object.assign(legacyPaths, orderedEntries)
const orderedPaths = Object.fromEntries(Object.entries(legacyPaths).sort(([a], [b]) => a.localeCompare(b)))

const baseObjects = git(['ls-tree', '-r', '--name-only', BASE_REF, 'review-archive/objects'])
  .trim().split('\n').filter(Boolean)
const objectFiles = new Set([...baseObjects, ...Object.values(orderedEntries).map(entry => entry.object)])
let uniqueBytes = 0
for (const object of objectFiles) {
  const file = path.join(ROOT, object)
  if (!fs.existsSync(file)) throw new Error(`committed-base object missing from working tree: ${object}`)
  uniqueBytes += fs.statSync(file).size
}
const logicalBytes = Object.values(orderedPaths).reduce((sum, entry) => sum + entry.bytes, 0)
const setNames = new Set(Object.keys(orderedPaths).map(legacyPath => legacyPath.replace(/^\/keeper-review\//, '').split('/')[0]))

writeJson(INDEX_FILE, {
  version: 1,
  generatedOn: new Date().toISOString().slice(0, 10),
  objectsBaseUrl: BASE_URL,
  mediaExtensions: baseIndex.mediaExtensions,
  stats: {
    setCount: setNames.size,
    referenceCount: Object.keys(orderedPaths).length,
    uniqueObjectCount: objectFiles.size,
    logicalBytes,
    uniqueBytes,
    deduplicatedBytes: logicalBytes - uniqueBytes,
  },
  legacyPaths: orderedPaths,
})

console.log(JSON.stringify({
  set,
  baseRef: BASE_REF,
  references: Object.keys(orderedEntries).length,
  committedTreeObjects: objectFiles.size,
  globalReferences: Object.keys(orderedPaths).length,
}, null, 2))
