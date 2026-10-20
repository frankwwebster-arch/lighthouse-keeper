#!/usr/bin/env node
import assert from 'node:assert/strict'
import crypto from 'node:crypto'
import fs from 'node:fs'
import path from 'node:path'
import { PNG } from 'pngjs'

const root = process.cwd()
const pack = 'art/drafts/claude-bbq-food-asset-pack-2026-10-20-v1'
const abs = value => path.join(root, value)
const sha = value => crypto.createHash('sha256').update(fs.readFileSync(abs(value))).digest('hex')
const manifest = JSON.parse(fs.readFileSync(abs(`${pack}/asset-manifest.json`), 'utf8'))
const expected = [
  'bbq-raw-burger-patties',
  'bbq-sausages',
  'bbq-grill',
  'cooking-cheese-slicing',
  'bbq-raw-steak',
  'meal-steak-fries',
  'condiment-ketchup-bottle',
  'condiment-mustard-bottle',
]

const edgeAlpha = png => {
  let count = 0
  for (let x = 0; x < png.width; x++) count += Number(png.data[x * 4 + 3] > 8) + Number(png.data[((png.height - 1) * png.width + x) * 4 + 3] > 8)
  for (let y = 0; y < png.height; y++) count += Number(png.data[(y * png.width) * 4 + 3] > 8) + Number(png.data[(y * png.width + png.width - 1) * 4 + 3] > 8)
  return count
}
const gutter = png => {
  let minX = png.width, minY = png.height, maxX = -1, maxY = -1
  for (let y = 0; y < png.height; y++) for (let x = 0; x < png.width; x++) if (png.data[(y * png.width + x) * 4 + 3] > 8) {
    minX = Math.min(minX, x); minY = Math.min(minY, y); maxX = Math.max(maxX, x); maxY = Math.max(maxY, y)
  }
  assert.ok(maxX >= 0, 'PNG has no visible alpha')
  return Math.min(minX, minY, png.width - maxX - 1, png.height - maxY - 1)
}

assert.equal(manifest.schema, 'lighthouse-keeper/claude-bbq-food-asset-pack@1')
assert.equal(manifest.status, 'review-only')
assert.match(manifest.foodPresentationRule, /plates are reserved for finished meals/i)
assert.deepEqual(Object.keys(manifest.components), expected)
assert.deepEqual(manifest.sourceProcessing.reviewSourceGeometry, [384, 384])

for (const id of expected) {
  const component = manifest.components[id]
  assert.equal(component.sha256, sha(component.file), `${id} output hash`)
  assert.equal(component.sourceSha256, sha(component.sourceFile), `${id} source hash`)
  assert.match(component.originalGeneratedPngSha256, /^[0-9a-f]{64}$/)
  assert.deepEqual(component.cellPixels, [256, 256])
  assert.equal(component.edgeAlphaPixels, 0)
  assert.ok(component.transparentGutterPx >= 20)
  assert.deepEqual(component.ownership, {ownerCount: 1, ambiguousPixels: 0, unownedVisiblePixels: 0})
  const png = PNG.sync.read(fs.readFileSync(abs(component.file)))
  assert.deepEqual([png.width, png.height], [256, 256])
  assert.equal(edgeAlpha(png), 0)
  assert.ok(gutter(png) >= 20)
}

assert.equal(manifest.rejectedAttempts.length, 1)
assert.equal(manifest.rejectedAttempts[0].sha256, sha(manifest.rejectedAttempts[0].file))
assert.match(manifest.rejectedAttempts[0].reason, /raw linked sausage string/i)
for (const [id, proposal] of Object.entries(manifest.supersessionProposals)) {
  assert.equal(proposal.oldSha256, sha(proposal.oldFile), `${id} old authority hash`)
  assert.equal(proposal.proposedSha256, manifest.components[id].sha256, `${id} proposed hash`)
  assert.equal(proposal.oldBytesUnchanged, true)
}
assert.equal(manifest.evidence.sha256, sha(manifest.evidence.file))
assert.deepEqual(manifest.checks, {
  sourceEdgesClear: true,
  componentGuttersClear: true,
  componentOwnershipUnambiguous: true,
  priorAssetsUnchanged: true,
  rejectedAttemptRetained: true,
  allAssetsIndependent: true,
  runtimeChanged: false,
  kitchenChanged: false,
  deployed: false,
})

const hashLines = fs.readFileSync(abs(`${pack}/HASHES.sha256`), 'utf8').trim().split('\n')
for (const line of hashLines) {
  const match = line.match(/^([0-9a-f]{64})  (.+)$/)
  assert.ok(match, `invalid hash line: ${line}`)
  assert.equal(sha(`${pack}/${match[2]}`), match[1], `pack hash mismatch: ${match[2]}`)
}

console.log(JSON.stringify({
  pack,
  assets: expected.length,
  rejectedAttempts: 1,
  gutters: '>=20px',
  hashes: 'verified',
  priorAssetsUnchanged: true,
  runtimeChanged: false,
  kitchenChanged: false,
  deployed: false,
}, null, 2))
