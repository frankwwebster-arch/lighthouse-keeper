/**
 * Test-only compatibility for immutable registers that name former public files.
 * Production requests use the review-archive redirect route instead.
 */
import fs from 'node:fs'
import { syncBuiltinESMExports } from 'node:module'
import path from 'node:path'
import { fileURLToPath } from 'node:url'

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..')
const INDEX = path.join(ROOT, 'review-archive/index.json')
const originalReadFileSync = fs.readFileSync.bind(fs)
const originalExistsSync = fs.existsSync.bind(fs)
const originalReaddirSync = fs.readdirSync.bind(fs)
const originalStatSync = fs.statSync.bind(fs)
const originalAccessSync = fs.accessSync.bind(fs)
const originalPromisesReadFile = fs.promises.readFile.bind(fs.promises)
const originalPromisesAccess = fs.promises.access.bind(fs.promises)
const originalPromisesStat = fs.promises.stat.bind(fs.promises)
const archive = originalExistsSync(INDEX) ? JSON.parse(originalReadFileSync(INDEX, 'utf8')) : { legacyPaths: {} }
const virtual = new Map()
for (const [legacyPath, entry] of Object.entries(archive.legacyPaths ?? {})) {
  virtual.set(path.resolve(ROOT, 'public', legacyPath.replace(/^\//, '')), path.resolve(ROOT, entry.object))
}

const normalize = (value) => {
  if (typeof value === 'string') return path.resolve(value)
  if (value instanceof URL && value.protocol === 'file:') return path.resolve(fileURLToPath(value))
  return null
}
const resolveVirtual = (value) => {
  const normalized = normalize(value)
  return normalized ? virtual.get(normalized) : undefined
}
const virtualChildren = (directory) => {
  const normalized = normalize(directory)
  if (!normalized) return []
  const prefix = `${normalized}${path.sep}`
  const children = new Set()
  for (const file of virtual.keys()) {
    if (!file.startsWith(prefix)) continue
    const remainder = file.slice(prefix.length)
    children.add(remainder.split(path.sep)[0])
  }
  return [...children]
}

fs.readFileSync = function patchedReadFileSync(file, ...args) {
  return originalReadFileSync(resolveVirtual(file) ?? file, ...args)
}
fs.existsSync = function patchedExistsSync(file) {
  return originalExistsSync(file) || Boolean(resolveVirtual(file)) || virtualChildren(file).length > 0
}
fs.statSync = function patchedStatSync(file, ...args) {
  return originalStatSync(resolveVirtual(file) ?? file, ...args)
}
fs.accessSync = function patchedAccessSync(file, ...args) {
  return originalAccessSync(resolveVirtual(file) ?? file, ...args)
}
fs.readdirSync = function patchedReaddirSync(directory, options) {
  const virtualNames = virtualChildren(directory)
  if (virtualNames.length === 0) return originalReaddirSync(directory, options)
  if (options && typeof options === 'object' && options.withFileTypes) return originalReaddirSync(directory, options)
  let physical = []
  if (originalExistsSync(directory)) physical = originalReaddirSync(directory, options)
  const names = new Set([...physical.map(String), ...virtualNames])
  return [...names].sort()
}
fs.promises.readFile = function patchedPromisesReadFile(file, ...args) {
  return originalPromisesReadFile(resolveVirtual(file) ?? file, ...args)
}
fs.promises.access = function patchedPromisesAccess(file, ...args) {
  return originalPromisesAccess(resolveVirtual(file) ?? file, ...args)
}
fs.promises.stat = function patchedPromisesStat(file, ...args) {
  return originalPromisesStat(resolveVirtual(file) ?? file, ...args)
}
syncBuiltinESMExports()
