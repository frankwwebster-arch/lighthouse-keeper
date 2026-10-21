#!/usr/bin/env node

import fs from 'node:fs'
import path from 'node:path'
import { fileURLToPath } from 'node:url'
import { PNG } from 'pngjs'
import { measure, readLibrary, sha256 } from './activity_story_pictures.mjs'

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..')
const pack = path.join(root, 'art/drafts/activity-story-ligne-claire-bbq-pilot-2026-10-21-v1')
const registerPath = path.join(pack, 'batch-register.json')

function filesUnder(directory) {
  return fs.readdirSync(directory, { withFileTypes: true }).flatMap((entry) => {
    const file = path.join(directory, entry.name)
    return entry.isDirectory() ? filesUnder(file) : [file]
  })
}

function visibleEdgePixels(buffer) {
  const png = PNG.sync.read(buffer)
  const points = new Set()
  for (let x = 0; x < png.width; x++) {
    points.add(`${x},0`)
    points.add(`${x},${png.height - 1}`)
  }
  for (let y = 0; y < png.height; y++) {
    points.add(`0,${y}`)
    points.add(`${png.width - 1},${y}`)
  }
  let count = 0
  for (const point of points) {
    const [x, y] = point.split(',').map(Number)
    if (png.data[(y * png.width + x) * 4 + 3] > 8) count++
  }
  return count
}

function visibleColours(buffer) {
  const png = PNG.sync.read(buffer)
  const colours = new Set()
  for (let i = 0; i < png.data.length; i += 4) {
    if (png.data[i + 3] <= 8) continue
    colours.add(`#${png.data[i].toString(16).padStart(2, '0')}${png.data[i + 1].toString(16).padStart(2, '0')}${png.data[i + 2].toString(16).padStart(2, '0')}`)
  }
  return colours
}

export function verifyActivityStoryLigneClaireBbqPilotV1() {
  const problems = []
  if (!fs.existsSync(registerPath)) return [`missing ligne-claire BBQ pilot register: ${registerPath}`]
  const register = JSON.parse(fs.readFileSync(registerPath, 'utf8'))
  const library = readLibrary()

  if (register.schema !== 'lighthouse-keeper/activity-story-ligne-claire-pilot@1') problems.push('ligne-claire BBQ pilot: wrong schema')
  if (register.status !== 'approved-and-registered') problems.push('ligne-claire BBQ pilot: status must be approved-and-registered')
  if (Object.keys(register.components ?? {}).length !== 6) problems.push('ligne-claire BBQ pilot: expected exactly six components')
  if (register.checks?.libraryVersionsAdded !== true) problems.push('ligne-claire BBQ pilot: libraryVersionsAdded must be true')
  if (register.approval?.words !== 'agreed, these are superb') problems.push('ligne-claire BBQ pilot: Frank approval wording is missing')

  for (const [id, component] of Object.entries(register.components ?? {})) {
    const sourcePath = path.join(root, component.sourceFile)
    const outputPath = path.join(root, component.file)
    const currentPath = path.join(root, component.currentReferenceFile)
    for (const [role, file] of [['source', sourcePath], ['output', outputPath], ['current reference', currentPath]]) {
      if (!fs.existsSync(file)) problems.push(`${id}: missing ${role} ${file}`)
    }
    if (!fs.existsSync(sourcePath) || !fs.existsSync(outputPath) || !fs.existsSync(currentPath)) continue
    const sourceBuffer = fs.readFileSync(sourcePath)
    const outputBuffer = fs.readFileSync(outputPath)
    if (sha256(sourceBuffer) !== component.sourceSha256) problems.push(`${id}: source hash drift`)
    if (sha256(outputBuffer) !== component.sha256) problems.push(`${id}: output hash drift`)
    if (sha256(fs.readFileSync(currentPath)) !== component.currentReferenceSha256) problems.push(`${id}: current reference hash drift`)
    if (visibleEdgePixels(sourceBuffer)) problems.push(`${id}: source has visible edge pixels`)
    if (visibleEdgePixels(outputBuffer)) problems.push(`${id}: output has visible edge pixels`)
    const geometry = measure(outputBuffer)
    if (geometry.cell.join() !== '256,256') problems.push(`${id}: output is not 256 × 256`)
    if (geometry.gutter < 20) problems.push(`${id}: output gutter is ${geometry.gutter}, expected at least 20`)
    if (!geometry.bounds || geometry.bounds.join() !== component.bounds.join()) problems.push(`${id}: measured bounds disagree with register`)
    if (component.ownership?.ownerCount !== 1 || component.ownership?.ambiguousPixels !== 0 || component.ownership?.unownedVisiblePixels !== 0)
      problems.push(`${id}: invalid ownership record`)
    const allowed = new Set(component.flatPalette)
    for (const colour of visibleColours(outputBuffer)) if (!allowed.has(colour)) problems.push(`${id}: output contains non-palette colour ${colour}`)
    const registered = library.pictures[id]?.versions.find((version) => version.v === component.libraryVersion)
    if (!registered) problems.push(`${id}: approved library version ${component.libraryVersion} is missing`)
    else if (registered.sha256 !== component.sha256) problems.push(`${id}: approved library version ${component.libraryVersion} has the wrong hash`)
    if (library.pictures[id]?.current !== component.libraryVersion) problems.push(`${id}: approved version ${component.libraryVersion} is not current`)
  }

  for (const item of register.rejected ?? []) {
    const file = path.join(pack, item.file)
    if (!fs.existsSync(file)) problems.push(`ligne-claire BBQ pilot: missing rejected provenance ${item.file}`)
    else if (sha256(fs.readFileSync(file)) !== item.sha256) problems.push(`ligne-claire BBQ pilot: rejected provenance hash drift ${item.file}`)
  }

  const evidencePath = path.join(root, register.evidence.file)
  if (!fs.existsSync(evidencePath)) problems.push('ligne-claire BBQ pilot: missing contact sheet')
  else if (sha256(fs.readFileSync(evidencePath)) !== register.evidence.sha256) problems.push('ligne-claire BBQ pilot: contact sheet hash drift')

  const listed = new Map(
    fs.readFileSync(path.join(pack, 'HASHES.sha256'), 'utf8').trim().split('\n').filter(Boolean).map((line) => {
      const match = line.match(/^([a-f0-9]{64})  (.+)$/)
      return match ? [match[2], match[1]] : [line, 'invalid']
    }),
  )
  const actual = filesUnder(pack).filter((file) => path.basename(file) !== 'HASHES.sha256')
  if (listed.size !== actual.length) problems.push(`ligne-claire BBQ pilot: HASHES lists ${listed.size} files, found ${actual.length}`)
  for (const file of actual) {
    const relative = path.relative(pack, file).split(path.sep).join('/')
    if (listed.get(relative) !== sha256(fs.readFileSync(file))) problems.push(`ligne-claire BBQ pilot: HASHES mismatch ${relative}`)
  }

  return problems
}

if (process.argv[1] === fileURLToPath(import.meta.url)) {
  const problems = verifyActivityStoryLigneClaireBbqPilotV1()
  if (problems.length) {
    console.error(`✗ ligne-claire BBQ pilot: ${problems.length} problem(s)\n  ${problems.join('\n  ')}`)
    process.exit(1)
  }
  console.log('✓ ligne-claire BBQ pilot: 6 approved current versions, flat palettes, provenance and contact sheet check out')
}
