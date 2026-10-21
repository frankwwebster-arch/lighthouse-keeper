#!/usr/bin/env node
import assert from 'node:assert/strict'
import crypto from 'node:crypto'
import { execFileSync } from 'node:child_process'
import fs from 'node:fs'
import path from 'node:path'
import { PNG } from 'pngjs'

const root = process.cwd()
const pack = 'art/drafts/claude-bedroom-asset-pack-2026-10-21-v1'
const abs = value => path.join(root, value)
const sha = value => crypto.createHash('sha256').update(fs.readFileSync(abs(value))).digest('hex')
const manifest = JSON.parse(fs.readFileSync(abs(`${pack}/asset-manifest.json`), 'utf8'))
const register = JSON.parse(fs.readFileSync(abs(`${pack}/source-register.json`), 'utf8'))
const protectedPins = JSON.parse(fs.readFileSync(abs(`${pack}/protected-authorities.json`), 'utf8'))
const expected = register.accepted.map(item => item.id)

const edgeAlpha = png => {
  let count = 0
  for (let x = 0; x < png.width; x++) count += Number(png.data[x * 4 + 3] > 8) + Number(png.data[((png.height - 1) * png.width + x) * 4 + 3] > 8)
  for (let y = 0; y < png.height; y++) count += Number(png.data[(y * png.width) * 4 + 3] > 8) + Number(png.data[(y * png.width + png.width - 1) * 4 + 3] > 8)
  return count
}

const visible = png => {
  let minX = png.width, minY = png.height, maxX = -1, maxY = -1
  for (let y = 0; y < png.height; y++) for (let x = 0; x < png.width; x++) if (png.data[(y * png.width + x) * 4 + 3] > 8) {
    minX = Math.min(minX, x); minY = Math.min(minY, y); maxX = Math.max(maxX, x); maxY = Math.max(maxY, y)
  }
  assert.ok(maxX >= 0, 'PNG has no visible alpha')
  return { width: maxX - minX + 1, height: maxY - minY + 1, gutter: Math.min(minX, minY, png.width - maxX - 1, png.height - maxY - 1) }
}

const tracked = execFileSync('git', ['ls-files', '-z'], { cwd: root, maxBuffer: 16 * 1024 * 1024 }).toString().split('\0').filter(Boolean).sort()
const patterns = {
  kitchen: /(^|\/)(kitchen|Kitchen)/,
  prime: /keeper[-_]prime|KEEPER_PRIME/,
  animation: /(^|\/)(animation|Animation)|keeper[-_]animation/,
  composerPages: /^public\/keeper-review\/activity-cloud-composer-v[0-9]+\//,
}
const deployment = new Set(['.github/workflows/deploy.yml', 'docs/DEPLOYMENT.md', 'scripts/deploy.mjs', 'scripts/vercel-ignore-build.mjs', 'scripts/vercel-ignore-build.test.ts', 'vercel.json'])
const aggregate = paths => {
  const hash = crypto.createHash('sha256')
  for (const relative of paths) {
    hash.update(relative); hash.update('\0'); hash.update(crypto.createHash('sha256').update(fs.readFileSync(abs(relative))).digest()); hash.update('\n')
  }
  return hash.digest('hex')
}
for (const [name, pattern] of Object.entries(patterns)) {
  const paths = tracked.filter(value => pattern.test(value))
  assert.equal(paths.length, protectedPins.groups[name].memberCount, `${name} authority membership`)
  assert.equal(aggregate(paths), protectedPins.groups[name].aggregateSha256, `${name} authority digest`)
}
const deploymentPaths = tracked.filter(value => deployment.has(value))
assert.equal(deploymentPaths.length, protectedPins.groups.deployment.memberCount)
assert.equal(aggregate(deploymentPaths), protectedPins.groups.deployment.aggregateSha256)

assert.equal(manifest.schema, 'lighthouse-keeper/claude-bedroom-asset-pack@1')
assert.equal(manifest.status, 'review-only')
assert.equal(register.accepted.length, 26)
assert.equal(register.rejected.length, 0)
assert.deepEqual(Object.keys(manifest.components), expected)
assert.deepEqual(manifest.sourceProcessing.reviewSourceGeometry, [384, 384])
for (const reference of manifest.styleReferences) assert.equal(reference.sha256, sha(reference.file))
assert.equal(manifest.sourceRegister.sha256, sha(manifest.sourceRegister.file))
assert.equal(manifest.protectedAuthorities.sha256, sha(manifest.protectedAuthorities.file))

for (const id of expected) {
  const component = manifest.components[id]
  assert.equal(component.sha256, sha(component.file), `${id} output hash`)
  assert.equal(component.sourceSha256, sha(component.sourceFile), `${id} source hash`)
  assert.match(component.originalCacheFile, /^exec-[0-9a-f-]+\.png$/)
  assert.match(component.originalGeneratedPngSha256, /^[0-9a-f]{64}$/)
  assert.equal(component.originalGeneratedGeometry.length, 2)
  assert.deepEqual(component.cellPixels, [256, 256])
  assert.equal(component.edgeAlphaPixels, 0)
  assert.ok(component.transparentGutterPx >= 20)
  assert.deepEqual(component.ownership, { ownerCount: 1, ambiguousPixels: 0, unownedVisiblePixels: 0 })
  const png = PNG.sync.read(fs.readFileSync(abs(component.file)))
  assert.deepEqual([png.width, png.height], [256, 256])
  assert.equal(edgeAlpha(png), 0)
  const geometry = visible(png)
  assert.ok(geometry.width <= 216 && geometry.height <= 216, `${id} visible area`)
  assert.ok(geometry.gutter >= 20, `${id} gutter`)
}

assert.equal(manifest.rejectedGenerations.length, 0)
assert.equal(manifest.evidence.sha256, sha(manifest.evidence.file))
assert.deepEqual(manifest.checks, {
  sourceEdgesClear: true,
  componentGuttersClear: true,
  componentOwnershipUnambiguous: true,
  styleReferencesUnchanged: true,
  allAcceptedAssetsIndependent: true,
  allTaskGenerationsRepresented: true,
  protectedAuthoritiesPinned: true,
  runtimeChanged: false,
  kitchenAuthorityChanged: false,
  primeChanged: false,
  animationAuthorityChanged: false,
  deploymentAuthorityChanged: false,
  composerPageChanged: false,
  deployed: false,
})

const hashLines = fs.readFileSync(abs(`${pack}/HASHES.sha256`), 'utf8').trim().split('\n')
const hashedFiles = new Set()
for (const line of hashLines) {
  const match = line.match(/^([0-9a-f]{64})  (.+)$/)
  assert.ok(match, `invalid hash line: ${line}`)
  assert.equal(sha(`${pack}/${match[2]}`), match[1], `pack hash mismatch: ${match[2]}`)
  hashedFiles.add(match[2])
}
const allPackFiles = fs.readdirSync(abs(pack), { recursive: true, withFileTypes: true })
  .filter(entry => entry.isFile() && entry.name !== 'HASHES.sha256')
  .map(entry => path.relative(abs(pack), path.join(entry.parentPath, entry.name)))
assert.deepEqual([...hashedFiles].sort(), allPackFiles.sort(), 'every pack file is hash-pinned')

const allowed = value => value.startsWith(`${pack}/`) || value.startsWith('art/drafts/claude-complete-activity-image-index-2026-10-21-v5/') || [
  'scripts/build_claude_bedroom_asset_pack_v1.py',
  'scripts/verify_claude_bedroom_asset_pack_v1.mjs',
  'scripts/build_claude_complete_activity_image_index_v5.mjs',
  'scripts/verify_claude_complete_activity_image_index_v5.mjs',
].includes(value)
const committedChanges = execFileSync('git', ['diff', '--name-only', protectedPins.capturedFrom, 'HEAD'], { cwd: root, maxBuffer: 16 * 1024 * 1024 }).toString().trim().split('\n').filter(Boolean)
assert.ok(committedChanges.every(allowed), `unexpected committed path: ${committedChanges.find(value => !allowed(value))}`)

console.log(JSON.stringify({
  pack,
  acceptedAssets: expected.length,
  rejectedGenerationsRetained: 0,
  taskGenerationsRepresented: 26,
  visibleArea: '<=216x216',
  gutters: '>=20px',
  hashes: 'verified',
  protectedAuthorities: 'verified',
  runtimeChanged: false,
  deployed: false,
}, null, 2))
