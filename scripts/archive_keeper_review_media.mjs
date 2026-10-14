#!/usr/bin/env node
/** Move Keeper review media into the content-addressed archive. */
import crypto from 'node:crypto'
import fs from 'node:fs'
import path from 'node:path'
import { fileURLToPath } from 'node:url'

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..')
const PUBLIC_ROOT = path.join(ROOT, 'public/keeper-review')
const ARCHIVE_ROOT = path.join(ROOT, 'review-archive')
const OBJECT_ROOT = path.join(ARCHIVE_ROOT, 'objects')
const SET_ROOT = path.join(ARCHIVE_ROOT, 'sets')
const INDEX = path.join(ARCHIVE_ROOT, 'index.json')
const BASE_URL = 'https://raw.githubusercontent.com/frankwwebster-arch/lighthouse-keeper/main/review-archive/objects'
const MEDIA_EXTENSIONS = new Set(['.png', '.gif', '.jpg', '.jpeg', '.webp', '.avif'])

const sha256 = (buffer) => crypto.createHash('sha256').update(buffer).digest('hex')
const posix = (value) => value.split(path.sep).join('/')
const writeJson = (file, value) => {
  fs.mkdirSync(path.dirname(file), { recursive: true })
  fs.writeFileSync(file, `${JSON.stringify(value, null, 2)}\n`)
}

function walk(directory) {
  if (!fs.existsSync(directory)) return []
  const files = []
  for (const entry of fs.readdirSync(directory, { withFileTypes: true })) {
    const absolute = path.join(directory, entry.name)
    if (entry.isDirectory()) files.push(...walk(absolute))
    else if (entry.isFile()) files.push(absolute)
  }
  return files
}

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
const legacyPaths = Object.fromEntries(Object.entries(previous?.legacyPaths ?? {}).map(([legacyPath, entry]) => [
  legacyPath,
  {
    ...entry,
    url: `${BASE_URL}/${entry.sha256.slice(0, 2)}/${entry.sha256}${entry.extension}`,
  },
]))
const physicalMedia = walk(PUBLIC_ROOT).filter((file) => MEDIA_EXTENSIONS.has(path.extname(file).toLowerCase()))

for (const file of physicalMedia) {
  const bytes = fs.readFileSync(file)
  const hash = sha256(bytes)
  const extension = path.extname(file).toLowerCase()
  const objectRelative = `review-archive/objects/${hash.slice(0, 2)}/${hash}${extension}`
  const objectPath = path.join(ROOT, objectRelative)
  if (fs.existsSync(objectPath)) {
    if (sha256(fs.readFileSync(objectPath)) !== hash) throw new Error(`archive object collision: ${objectRelative}`)
  } else {
    fs.mkdirSync(path.dirname(objectPath), { recursive: true })
    fs.copyFileSync(file, objectPath)
  }
  const legacyPath = `/${posix(path.relative(path.join(ROOT, 'public'), file))}`
  legacyPaths[legacyPath] = {
    sha256: hash,
    extension,
    bytes: bytes.length,
    object: objectRelative,
    url: `${BASE_URL}/${hash.slice(0, 2)}/${hash}${extension}`,
  }
}

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

const uniqueObjects = new Map()
let logicalBytes = 0
for (const entry of Object.values(orderedPaths)) {
  logicalBytes += entry.bytes
  uniqueObjects.set(entry.object, entry.bytes)
}
const uniqueBytes = [...uniqueObjects.values()].reduce((sum, bytes) => sum + bytes, 0)
writeJson(INDEX, {
  version: 1,
  generatedOn: new Date().toISOString().slice(0, 10),
  objectsBaseUrl: BASE_URL,
  mediaExtensions: [...MEDIA_EXTENSIONS].sort(),
  stats: {
    setCount: sets.size,
    referenceCount: Object.keys(orderedPaths).length,
    uniqueObjectCount: uniqueObjects.size,
    logicalBytes,
    uniqueBytes,
    deduplicatedBytes: logicalBytes - uniqueBytes,
  },
  legacyPaths: orderedPaths,
})

for (const file of physicalMedia) fs.unlinkSync(file)
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
  uniqueObjects: uniqueObjects.size,
  logicalMiB: Number((logicalBytes / 1024 / 1024).toFixed(2)),
  uniqueMiB: Number((uniqueBytes / 1024 / 1024).toFixed(2)),
  savedPerDeploymentMiB: Number((logicalBytes / 1024 / 1024).toFixed(2)),
}, null, 2))
