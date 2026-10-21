#!/usr/bin/env node
/** Verify the immutable 54-picture Codex Bubble-story family expansion. */

import fs from 'node:fs'
import path from 'node:path'
import { fileURLToPath } from 'node:url'
import { ROOT, measure, sha256 } from './activity_story_pictures.mjs'

const PACK = path.join(ROOT, 'art/drafts/codex-bubble-story-families-2026-10-21-v1')
const MANIFEST = path.join(PACK, 'asset-manifest.json')
const REGISTER = path.join(PACK, 'source-register.json')
const HASHES = path.join(PACK, 'HASHES.sha256')
const EXPECTED_FAMILIES = new Map([
  ['fishing', 6],
  ['garden', 6],
  ['pet-care', 6],
  ['repair', 12],
  ['pub', 8],
  ['art', 8],
  ['inventing', 8],
])

const relativeToRoot = (file) => path.relative(ROOT, file).split(path.sep).join('/')

function allFiles(dir) {
  return fs.readdirSync(dir, { withFileTypes: true }).flatMap((entry) => {
    const file = path.join(dir, entry.name)
    return entry.isDirectory() ? allFiles(file) : [file]
  })
}

export function verifyCodexBubbleStoryFamiliesV1() {
  const problems = []
  const fail = (message) => problems.push(`codex family pack: ${message}`)
  for (const file of [MANIFEST, REGISTER, HASHES]) if (!fs.existsSync(file)) fail(`missing ${relativeToRoot(file)}`)
  if (problems.length) return problems

  const manifest = JSON.parse(fs.readFileSync(MANIFEST, 'utf8'))
  const register = JSON.parse(fs.readFileSync(REGISTER, 'utf8'))
  if (manifest.schema !== 'lighthouse-keeper/codex-bubble-story-families-pack@1') fail('wrong manifest schema')
  if (manifest.set !== 'codex-bubble-story-families-v1') fail(`wrong set ${manifest.set}`)
  if (register.schema !== 'lighthouse-keeper/codex-bubble-story-family-source-register@1') fail('wrong source-register schema')

  const components = Object.entries(manifest.components ?? {})
  if (components.length !== 54) fail(`expected 54 components, found ${components.length}`)
  const familyCounts = new Map()
  const acceptedById = new Map((register.accepted ?? []).map((entry) => [entry.id, entry]))
  if (acceptedById.size !== 54 || register.accepted?.length !== 54) fail(`expected 54 distinct accepted sources, found ${register.accepted?.length ?? 0}`)
  if (register.rejected?.length !== 1 || register.rejected?.[0]?.id !== 'art-easel-and-canvas') fail('the recorded rejected easel candidate is missing or changed')

  const outputHashes = new Set()
  const sourceHashes = new Set()
  for (const [id, component] of components) {
    familyCounts.set(component.family, (familyCounts.get(component.family) ?? 0) + 1)
    if (!id.startsWith(`${component.family === 'pet-care' ? 'pet' : component.family}-`)) fail(`${id}: id does not match family ${component.family}`)
    if (!component.label) fail(`${id}: missing human-readable label`)
    if (component.cellPixels?.join() !== '256,256') fail(`${id}: manifest cell is not 256 × 256`)
    if (component.transparentGutterPx < 20) fail(`${id}: manifest gutter is below 20 px`)
    if (component.edgeAlphaPixels !== 0) fail(`${id}: edge alpha is not clear`)
    if (component.ownership?.ownerCount !== 1 || component.ownership?.ambiguousPixels !== 0 || component.ownership?.unownedVisiblePixels !== 0)
      fail(`${id}: ownership is not isolated`)

    const output = path.join(ROOT, component.file ?? '')
    if (!fs.existsSync(output)) fail(`${id}: missing output ${component.file}`)
    else {
      const buffer = fs.readFileSync(output)
      const actualHash = sha256(buffer)
      if (actualHash !== component.sha256) fail(`${id}: output SHA-256 changed`)
      if (outputHashes.has(actualHash)) fail(`${id}: duplicates another final picture byte-for-byte`)
      outputHashes.add(actualHash)
      const measured = measure(buffer)
      const expectedBounds = [component.normalisedOffset[0], component.normalisedOffset[1], component.normalisedOffset[0] + component.normalisedVisibleSize[0], component.normalisedOffset[1] + component.normalisedVisibleSize[1]]
      if (measured.cell.join() !== '256,256') fail(`${id}: output cell is ${measured.cell.join(' × ')}`)
      if (measured.gutter < 20) fail(`${id}: measured gutter is ${measured.gutter} px`)
      if (measured.bounds?.join() !== expectedBounds.join()) fail(`${id}: measured bounds ${measured.bounds?.join(',')} disagree with the manifest`)
    }

    const source = path.join(ROOT, component.sourceFile ?? '')
    if (!fs.existsSync(source)) fail(`${id}: missing prepared source ${component.sourceFile}`)
    else {
      const sourceHash = sha256(fs.readFileSync(source))
      if (sourceHash !== component.sourceSha256) fail(`${id}: prepared source SHA-256 changed`)
      if (sourceHashes.has(sourceHash)) fail(`${id}: duplicates another prepared source byte-for-byte`)
      sourceHashes.add(sourceHash)
    }
    const accepted = acceptedById.get(id)
    if (!accepted || accepted.sourceFile !== component.sourceFile || accepted.originalGeneratedPngSha256 !== component.originalGeneratedPngSha256)
      fail(`${id}: manifest and source register disagree`)
  }

  for (const [family, expected] of EXPECTED_FAMILIES) {
    const actual = familyCounts.get(family) ?? 0
    if (actual !== expected) fail(`${family}: expected ${expected} pictures, found ${actual}`)
    familyCounts.delete(family)
  }
  for (const family of familyCounts.keys()) fail(`unexpected family ${family}`)

  const registerHash = sha256(fs.readFileSync(REGISTER))
  if (manifest.sourceRegister?.file !== relativeToRoot(REGISTER) || manifest.sourceRegister?.sha256 !== registerHash)
    fail('manifest source-register reference is stale')

  const listed = new Map()
  for (const line of fs.readFileSync(HASHES, 'utf8').trim().split('\n')) {
    const match = line.match(/^([a-f0-9]{64})  (.+)$/)
    if (!match) fail(`malformed HASHES.sha256 line: ${line}`)
    else if (listed.has(match[2])) fail(`HASHES.sha256 lists ${match[2]} twice`)
    else listed.set(match[2], match[1])
  }
  const trackedFiles = allFiles(PACK).filter((file) => file !== HASHES && !file.endsWith('.raw.png'))
  for (const file of trackedFiles) {
    const relative = path.relative(PACK, file).split(path.sep).join('/')
    if (!listed.has(relative)) fail(`HASHES.sha256 omits ${relative}`)
    else if (listed.get(relative) !== sha256(fs.readFileSync(file))) fail(`${relative}: HASHES.sha256 is stale`)
    listed.delete(relative)
  }
  for (const leftover of listed.keys()) fail(`HASHES.sha256 names missing file ${leftover}`)
  const rawSources = allFiles(path.join(PACK, 'source')).filter((file) => file.endsWith('.png'))
  if (rawSources.length) fail(`source contains ${rawSources.length} uncompressed PNG file(s)`)
  return problems
}

if (path.resolve(process.argv[1] ?? '') === fileURLToPath(import.meta.url)) {
  const problems = verifyCodexBubbleStoryFamiliesV1()
  if (problems.length) {
    console.error(`✗ Codex Bubble-story family pack: ${problems.length} problem(s)\n  ${problems.join('\n  ')}`)
    process.exit(1)
  }
  console.log('✓ Codex Bubble-story family pack: 54 isolated pictures across 7 families check out')
}
