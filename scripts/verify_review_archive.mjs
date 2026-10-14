#!/usr/bin/env node
/** Verify the content-addressed Keeper review archive and deployment boundary. */
import crypto from 'node:crypto'
import fs from 'node:fs'
import path from 'node:path'
import { fileURLToPath } from 'node:url'

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..')
const ARCHIVE = path.join(ROOT, 'review-archive')
const INDEX = path.join(ARCHIVE, 'index.json')
const fail = (message) => { throw new Error(`Review archive: ${message}`) }
const hash = (file) => crypto.createHash('sha256').update(fs.readFileSync(file)).digest('hex')
if (!fs.existsSync(INDEX)) fail('index.json is missing')
const index = JSON.parse(fs.readFileSync(INDEX, 'utf8'))
if (index.version !== 1 || !index.objectsBaseUrl.startsWith('https://')) fail('index identity/base URL invalid')

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
  try { fs.lstatSync(oldPublic); fail(`archived media still physically present in public: ${legacyPath}`) } catch (error) { if (error.code !== 'ENOENT') throw error }
  referencedObjects.add(entry.object)
  logicalBytes += entry.bytes
}

const storedObjects = []
for (const prefix of fs.readdirSync(path.join(ARCHIVE, 'objects'))) {
  const directory = path.join(ARCHIVE, 'objects', prefix)
  if (!fs.statSync(directory).isDirectory() || !/^[a-f0-9]{2}$/.test(prefix)) fail(`invalid object prefix ${prefix}`)
  for (const name of fs.readdirSync(directory)) {
    const match = name.match(/^([a-f0-9]{64})(\.[a-z0-9]+)$/)
    if (!match) fail(`invalid object filename ${prefix}/${name}`)
    const file = path.join(directory, name)
    if (match[1].slice(0, 2) !== prefix || hash(file) !== match[1]) fail(`object filename/hash mismatch ${prefix}/${name}`)
    storedObjects.push(`review-archive/objects/${prefix}/${name}`)
  }
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

const uniqueBytes = storedObjects.reduce((sum, object) => sum + fs.statSync(path.join(ROOT, object)).size, 0)
if (index.stats.setCount !== setFiles.length || index.stats.referenceCount !== setEntries.size || index.stats.uniqueObjectCount !== storedObjects.length || index.stats.logicalBytes !== logicalBytes || index.stats.uniqueBytes !== uniqueBytes || index.stats.deduplicatedBytes !== logicalBytes - uniqueBytes) fail('index statistics changed')
if (index.stats.referenceCount < 500 || index.stats.uniqueObjectCount >= index.stats.referenceCount || index.stats.deduplicatedBytes < 20 * 1024 * 1024) fail('archive does not meet deduplication floor')

const realSize = (directory) => {
  let total = 0
  for (const entry of fs.readdirSync(directory, { withFileTypes: true })) {
    const file = path.join(directory, entry.name)
    if (entry.isDirectory()) total += realSize(file)
    else if (entry.isFile()) total += fs.lstatSync(file).size
  }
  return total
}
const publicBytes = realSize(path.join(ROOT, 'public'))
if (publicBytes >= 50 * 1024 * 1024) fail(`public deployment payload is ${(publicBytes / 1024 / 1024).toFixed(2)} MiB, expected below 50 MiB`)
console.log(`Review archive verified: ${setFiles.length} sets, ${setEntries.size} references → ${storedObjects.length} immutable objects; public payload ${(publicBytes / 1024 / 1024).toFixed(2)} MiB.`)
