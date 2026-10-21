#!/usr/bin/env node
/** Verify the content-addressed Keeper review archive and deployment boundary. */
import crypto from 'node:crypto'
import fs from 'node:fs'
import path from 'node:path'
import { execFileSync } from 'node:child_process'
import { fileURLToPath } from 'node:url'
import { verifyRootAbsoluteReviewUrls } from './review_page_url_policy.mjs'

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..')
const ARCHIVE = path.join(ROOT, 'review-archive')
const INDEX = path.join(ARCHIVE, 'index.json')
const PUBLIC = path.join(ROOT, 'public')
const PUBLIC_REVIEW = path.join(PUBLIC, 'keeper-review')
const MEDIA_EXTENSIONS = new Set(['.png', '.gif', '.jpg', '.jpeg', '.webp', '.avif'])
const LARGE_DATA_EXTENSIONS = new Set(['.json', '.json.gz'])
const LARGE_DATA_THRESHOLD_BYTES = 24 * 1024
const PUBLIC_DATA_EXCEPTIONS = {
  '/keeper-review/activity-cloud-composer-v6/catalogue.json': 'eb5060a665694137ce63a45dcb8f914d1086570393399b1537d37ade660fe2aa',
}
const PUBLIC_LIMIT_BYTES = 50 * 1024 * 1024
const UNPUBLISHED_HISTORICAL_LINKS = new Set([
  '/keeper-review/keeper-prime-context-workbench-v8/inventory.json',
  '/keeper-review/keeper-prime-context-workbench-v9/inventory.json',
  '/keeper-review/keeper-prime-context-workbench-v10/inventory.json',
])
const fail = (message) => { throw new Error(`Review archive: ${message}`) }
const hash = (file) => crypto.createHash('sha256').update(fs.readFileSync(file)).digest('hex')
const posix = value => value.split(path.sep).join('/')
const archiveExtension = file => file.toLowerCase().endsWith('.json.gz') ? '.json.gz' : path.extname(file).toLowerCase()
const legacyPathFor = file => `/${posix(path.relative(PUBLIC, file))}`
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
verifyRootAbsoluteReviewUrls(ROOT)
if (!fs.existsSync(INDEX)) fail('index.json is missing')
const index = JSON.parse(fs.readFileSync(INDEX, 'utf8'))
if (index.version !== 1 || index.objectsBaseUrl !== 'https://raw.githubusercontent.com/frankwwebster-arch/lighthouse-keeper/main/review-archive/objects') fail('index identity/base URL invalid')
if (JSON.stringify(index.mediaExtensions) !== JSON.stringify([...MEDIA_EXTENSIONS].sort()) ||
    JSON.stringify(index.largeDataExtensions) !== JSON.stringify([...LARGE_DATA_EXTENSIONS].sort()) ||
    index.largeDataThresholdBytes !== LARGE_DATA_THRESHOLD_BYTES) fail('archive payload policy is missing or stale')
for (const [legacyPath, expectedHash] of Object.entries(PUBLIC_DATA_EXCEPTIONS)) {
  const publicFile = path.join(PUBLIC, legacyPath.replace(/^\//, ''))
  if (!fs.existsSync(publicFile) || hash(publicFile) !== expectedHash || index.legacyPaths[legacyPath]) {
    fail(`pinned public review-data exception is missing, changed, or archived: ${legacyPath}`)
  }
}

const referencedObjects = new Set()
let logicalBytes = 0
for (const [legacyPath, entry] of Object.entries(index.legacyPaths)) {
  if (!legacyPath.startsWith('/keeper-review/')) fail(`legacy path outside review root: ${legacyPath}`)
  if (!/^[a-f0-9]{64}$/.test(entry.sha256)) fail(`invalid hash for ${legacyPath}`)
  const expectedObject = `review-archive/objects/${entry.sha256.slice(0, 2)}/${entry.sha256}${entry.extension}`
  if (entry.object !== expectedObject) fail(`non-canonical object path for ${legacyPath}`)
  if (entry.url !== `${index.objectsBaseUrl}/${entry.sha256.slice(0, 2)}/${entry.sha256}${entry.extension}`) fail(`URL mismatch for ${legacyPath}`)
  const object = path.join(ROOT, entry.object)
  if (!fs.existsSync(object) || hash(object) !== entry.sha256) fail(`missing or corrupt object for ${legacyPath}`)
  if (fs.statSync(object).size !== entry.bytes) fail(`size mismatch for ${legacyPath}`)
  const oldPublic = path.join(ROOT, 'public', legacyPath.replace(/^\//, ''))
  try { fs.lstatSync(oldPublic); fail(`archived payload still physically present in public: ${legacyPath}`) } catch (error) { if (error.code !== 'ENOENT') throw error }
  referencedObjects.add(entry.object)
  logicalBytes += entry.bytes
}

const trackedObjects = execFileSync('git', ['ls-files', '-z', '--', 'review-archive/objects'], {
  cwd: ROOT, encoding: 'utf8', maxBuffer: 32 * 1024 * 1024,
}).split('\0').filter(Boolean)
const storedObjects = [...new Set([...trackedObjects, ...referencedObjects])].sort()
for (const object of storedObjects) {
  const relative = object.replace(/^review-archive\/objects\//, '')
  const match = relative.match(/^([a-f0-9]{2})\/([a-f0-9]{64})(\.[a-z0-9]+(?:\.[a-z0-9]+)*)$/)
  if (!match || match[2].slice(0, 2) !== match[1]) fail(`invalid object path ${object}`)
  const file = path.join(ROOT, object)
  if (!fs.existsSync(file) || hash(file) !== match[2]) fail(`object filename/hash mismatch ${object}`)
}
if (new Set(storedObjects).size !== storedObjects.length) fail('duplicate object path')
for (const object of referencedObjects) if (!storedObjects.includes(object)) fail(`referenced object missing from store: ${object}`)

const setFiles = fs.readdirSync(path.join(ARCHIVE, 'sets')).filter((name) => name.endsWith('.json')).sort()
const setEntries = new Map()
for (const name of setFiles) {
  const manifest = JSON.parse(fs.readFileSync(path.join(ARCHIVE, 'sets', name), 'utf8'))
  if (manifest.version !== 1 || `${manifest.set}.json` !== name || manifest.objectsBaseUrl !== index.objectsBaseUrl) fail(`invalid set manifest ${name}`)
  if (manifest.page) {
    const page = path.join(ROOT, manifest.page.path)
    if (!fs.existsSync(page) || hash(page) !== manifest.page.sha256 || fs.statSync(page).size !== manifest.page.bytes) fail(`immutable page changed for ${name}`)
  }
  for (const [legacyPath, entry] of Object.entries(manifest.entries)) {
    if (setEntries.has(legacyPath)) fail(`legacy path appears in multiple sets: ${legacyPath}`)
    setEntries.set(legacyPath, entry)
  }
}
if (setEntries.size !== Object.keys(index.legacyPaths).length) fail('set/global reference counts differ')
for (const [legacyPath, entry] of Object.entries(index.legacyPaths)) if (JSON.stringify(setEntries.get(legacyPath)) !== JSON.stringify(entry)) fail(`set/global entry differs: ${legacyPath}`)
for (const legacyPath of UNPUBLISHED_HISTORICAL_LINKS) if (index.legacyPaths[legacyPath]) fail(`intentionally unpublished duplicate was archived: ${legacyPath}`)

const routeFiles = [
  'src/app/keeper-review/[set]/assets/[asset]/route.ts',
  'src/app/keeper-review/drafts/[asset]/route.ts',
  'src/app/keeper-review/[set]/[asset]/route.ts',
]
for (const routeFile of routeFiles) {
  const source = path.join(ROOT, routeFile)
  if (!fs.existsSync(source) || !fs.readFileSync(source, 'utf8').includes('reviewArchiveEntry')) fail(`archive resolver route missing or invalid: ${routeFile}`)
}
for (const legacyPath of Object.keys(index.legacyPaths)) {
  const routable = /^\/keeper-review\/drafts\/[^/]+$/.test(legacyPath) ||
    /^\/keeper-review\/[^/]+\/assets\/[^/]+$/.test(legacyPath) ||
    /^\/keeper-review\/[^/]+\/[^/]+$/.test(legacyPath)
  if (!routable) fail(`archived legacy path has no resolver route: ${legacyPath}`)
}

let resolvedPageReferences = 0
const literalReviewPath = /\/keeper-review\/[A-Za-z0-9._/-]+\.(?:png|gif|jpe?g|webp|avif|json(?:\.gz)?)/gi
for (const page of walk(PUBLIC_REVIEW).filter(file => file.endsWith('.html'))) {
  for (const legacyPath of fs.readFileSync(page, 'utf8').match(literalReviewPath) ?? []) {
    const physical = path.join(PUBLIC, legacyPath.replace(/^\//, ''))
    if (!fs.existsSync(physical) && !index.legacyPaths[legacyPath] && !UNPUBLISHED_HISTORICAL_LINKS.has(legacyPath)) {
      fail(`review page ${posix(path.relative(ROOT, page))} references unresolved payload ${legacyPath}`)
    }
    if (!UNPUBLISHED_HISTORICAL_LINKS.has(legacyPath)) resolvedPageReferences += 1
  }
}

const uniqueBytes = storedObjects.reduce((sum, object) => sum + fs.statSync(path.join(ROOT, object)).size, 0)
if (index.stats.setCount !== setFiles.length || index.stats.referenceCount !== setEntries.size || index.stats.uniqueObjectCount !== storedObjects.length || index.stats.logicalBytes !== logicalBytes || index.stats.uniqueBytes !== uniqueBytes || index.stats.deduplicatedBytes !== logicalBytes - uniqueBytes) fail('index statistics changed')
if (index.stats.referenceCount < 500 || index.stats.uniqueObjectCount >= index.stats.referenceCount || index.stats.deduplicatedBytes < 20 * 1024 * 1024) fail('archive does not meet deduplication floor')

const publicReviewPayloads = walk(PUBLIC_REVIEW).filter(file => {
  const extension = archiveExtension(file)
  if (PUBLIC_DATA_EXCEPTIONS[legacyPathFor(file)]) return false
  return MEDIA_EXTENSIONS.has(extension) ||
    (LARGE_DATA_EXTENSIONS.has(extension) && fs.statSync(file).size >= LARGE_DATA_THRESHOLD_BYTES)
})
if (publicReviewPayloads.length) {
  const offenders = publicReviewPayloads
    .sort((a, b) => fs.statSync(b).size - fs.statSync(a).size)
    .slice(0, 10)
    .map(file => `${(fs.statSync(file).size / 1024).toFixed(1)} KiB  ${posix(path.relative(ROOT, file))}`)
    .join('\n  ')
  fail(`archiveable review payload remains under public/keeper-review:\n  ${offenders}\nRun npm run maintain:keeper-review. Review HTML and JSON below 24 KiB stay public.`)
}

const publicFiles = walk(PUBLIC)
const publicBytes = publicFiles.reduce((sum, file) => sum + fs.lstatSync(file).size, 0)
if (publicBytes >= PUBLIC_LIMIT_BYTES) {
  const largest = publicFiles.sort((a, b) => fs.statSync(b).size - fs.statSync(a).size).slice(0, 10)
    .map(file => `${(fs.statSync(file).size / 1024 / 1024).toFixed(2)} MiB  ${posix(path.relative(ROOT, file))}`)
    .join('\n  ')
  fail(`public/ deployment payload is ${(publicBytes / 1024 / 1024).toFixed(2)} MiB; the unchanged limit is 50.00 MiB. This measures only public/ (not repository size, review-archive/, or art/drafts/).\nLargest public/ files:\n  ${largest}\nRun npm run maintain:keeper-review to archive review evidence; do not remove runtime assets or art/drafts.`)
}
console.log(`Review archive verified: ${setFiles.length} sets, ${setEntries.size} references → ${storedObjects.length} immutable objects; ${resolvedPageReferences} literal page references resolve; public payload ${(publicBytes / 1024 / 1024).toFixed(2)} MiB.`)
