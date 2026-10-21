#!/usr/bin/env node
/** Verify the reversible Keeper full-face canon pack and its read-only inventory. */
import crypto from 'node:crypto'
import fs from 'node:fs'
import path from 'node:path'
import { PNG } from 'pngjs'

const ROOT = path.resolve(import.meta.dirname, '..')
const PACK = path.join(ROOT, 'art/drafts/keeper-full-face-canon-pack-2026-10-12-v1')
const REGISTER = path.join(PACK, 'canon-pack-register.json')
const INVENTORY = path.join(ROOT, 'data/keeper_full_face_inventory.json')
const MANIFEST = path.join(ROOT, 'public/sprites/manifest.json')
const PUBLIC_PAGE = path.join(ROOT, 'public/keeper-review/full-face-canon-v1/index.html')
const REVIEW_PAGE = path.join(ROOT, 'public/keeper-review/index.html')
const EXPECTED_PRIMARY_SHA = '6d3b5057f7dad4410230c5c2a1959a2db468aca6f2d28486ec6db9e07827056a'
const EXPECTED_QUALITY_SHA = '14c70ab69c9cb558d1a7b9b092425718a43269ea8fb2a20ad3d64638d30ea17a'
const fail = (message: string): never => { throw new Error(`keeper full-face canon: ${message}`) }
const readJson = (file: string) => JSON.parse(fs.readFileSync(file, 'utf8')) as Record<string, any>
const absolute = (relative: string) => path.join(ROOT, relative)
const sha256 = (file: string) => crypto.createHash('sha256').update(fs.readFileSync(file)).digest('hex')

for (const file of [REGISTER, INVENTORY, PUBLIC_PAGE, REVIEW_PAGE]) if (!fs.existsSync(file)) fail(`missing ${path.relative(ROOT, file)}`)
const register = readJson(REGISTER)
const inventory = readJson(INVENTORY)
const manifest = readJson(MANIFEST)
if (register.packId !== 'keeper-full-face-canon-pack-2026-10-12-v1') fail('unexpected pack id')
if (register.status !== 'approved-for-batch-authoring') fail('pack approval state is not recorded')
if (register.approval?.approvedBy !== 'Frank' || register.approval?.approvedOn !== '2026-10-12') fail('explicit approval evidence is missing')
if (register.scopeGate?.productionPromoted !== false) fail('pack incorrectly claims or permits production promotion')
if (register.candidate?.promotionAllowed !== false) fail('candidate is not explicitly non-promotable')
if (register.primaryGeometryAuthority.sha256 !== EXPECTED_PRIMARY_SHA || sha256(absolute(register.primaryGeometryAuthority.file)) !== EXPECTED_PRIMARY_SHA) fail('primary authority hash changed')
if (register.renderingQualityReference.sha256 !== EXPECTED_QUALITY_SHA || sha256(absolute(register.renderingQualityReference.file)) !== EXPECTED_QUALITY_SHA) fail('V11 quality reference hash changed')

const candidatePath = absolute(register.candidate.file)
const primaryPath = absolute(register.primaryGeometryAuthority.file)
if (sha256(candidatePath) !== register.candidate.sha256) fail('candidate hash is stale')
if (!fs.readFileSync(candidatePath).equals(fs.readFileSync(primaryPath))) fail('V1 candidate is not byte-identical to the selected primary')
const candidate = PNG.sync.read(fs.readFileSync(candidatePath))
const sidecar = readJson(absolute(register.candidate.sidecar))
if (candidate.width !== sidecar.w * sidecar.density || candidate.height !== sidecar.h * sidecar.density || sidecar.frames !== 1) fail('candidate geometry disagrees with its sidecar')
if (sidecar.startPose !== 'standing-front' || sidecar.endPose !== 'standing-front' || sidecar.pose !== 'standing-front') fail('candidate neutral endpoint contract changed')
const alphaValues = new Set<number>()
let border = 0
for (let y = 0; y < candidate.height; y += 1) for (let x = 0; x < candidate.width; x += 1) {
  const alpha = candidate.data[((y * candidate.width) + x) * 4 + 3]
  alphaValues.add(alpha)
  if (alpha > 0 && (x === 0 || x === candidate.width - 1 || y === 0 || y === candidate.height - 1)) border += 1
}
if ([...alphaValues].sort((a, b) => a - b).join(',') !== '0,255') fail('candidate alpha is not binary')
if (border !== 0) fail(`candidate lost its transparent safety gutter (${border} edge pixels)`)

for (const [name, record] of Object.entries(register.masksAndGuides as Record<string, any>)) {
  const file = absolute(record.file)
  if (!fs.existsSync(file) || sha256(file) !== record.sha256) fail(`${name} mask/guide is missing or stale`)
  const image = PNG.sync.read(fs.readFileSync(file))
  if (image.width !== candidate.width || image.height !== candidate.height) fail(`${name} mask/guide geometry changed`)
  let pixels = 0
  for (let i = 3; i < image.data.length; i += 4) if (image.data[i]) pixels += 1
  if (pixels !== record.pixelCount || pixels === 0) fail(`${name} mask/guide pixel count changed`)
}
for (const [name, record] of Object.entries(register.evidence as Record<string, any>)) {
  if (!record.file) continue
  const file = absolute(record.file)
  if (!fs.existsSync(file) || (record.sha256 && sha256(file) !== record.sha256)) fail(`${name} evidence is missing or stale`)
}
for (const sectionName of ['primaryGeometryAuthority', 'renderingQualityReference'] as const) {
  const section = register[sectionName]
  if (!fs.existsSync(absolute(section.storedCopy)) || sha256(absolute(section.storedCopy)) !== section.storedCopySha256) fail(`${sectionName} stored copy is missing or stale`)
}

const manualScope = new Set([
  'keeper_reference', 'keeper_idle', 'keeper_sit_front', 'keeper_neutral_standing-front', 'keeper_neutral_sitting-front',
  'keeper_turn_front', 'keeper_turn_left_front', 'keeper_artist_smock_turn_front', 'keeper_pyjamas_turn_back',
  'keeper_party_turn_back', 'keeper_walk_into_lift', 'keeper_artist-smock_neutral_standing-front',
  'keeper_light-blue-pyjamas_neutral_standing-front',
])
const expectedNames = Object.entries(manifest)
  .filter(([name, spec]: [string, any]) => name.startsWith('keeper_') && !name.startsWith('keeper_prime_') && spec.assetRole !== 'component' && (spec.facing === 'front' || spec.facing === 'down' || manualScope.has(name)))
  .map(([name]) => name).sort()
const entries = inventory.entries as Record<string, any>[]
const actualNames = entries.map(entry => entry.name).sort()
if (inventory.count !== 62 || entries.length !== 62) fail(`expected 62 inventory entries, found ${entries.length}`)
if (actualNames.join('\n') !== expectedNames.join('\n')) fail('inventory no longer covers the complete manifest-derived direct-front scope')
if (new Set(actualNames).size !== actualNames.length) fail('inventory contains duplicate exact names')
if (inventory.visualMetadataExclusions?.keeper_bath_enter == null || inventory.visualMetadataExclusions?.keeper_bath_exit == null) fail('visual metadata exclusions are incomplete')

const withdrawn = new Set(inventory.withdrawnProvenance.withdrawn.map((entry: Record<string, any>) => entry.animation))
if (withdrawn.size !== 12) fail('withdrawn face-camera provenance no longer contains exactly 12 retained rejected drafts')
const deleted = inventory.withdrawnProvenance.deleted
if (deleted.length !== 1 || deleted[0].animation !== 'keeper_count_money') fail('deleted keeper_count_money provenance is missing')

for (const entry of entries) {
  const spec = manifest[entry.name]
  if (!spec) fail(`${entry.name} is absent from the runtime manifest`)
  for (const key of ['sourceStrip', 'sidecar', 'runtimeStrip']) {
    const file = absolute(entry[key])
    if (!fs.existsSync(file) || sha256(file) !== entry[`${key}Sha256`]) fail(`${entry.name} ${key} hash is stale`)
  }
  const strip = PNG.sync.read(fs.readFileSync(absolute(entry.sourceStrip)))
  const metadata = readJson(absolute(entry.sidecar))
  const frameWidth = metadata.w * metadata.density
  if (strip.width !== frameWidth * metadata.frames || strip.height !== metadata.h * metadata.density) fail(`${entry.name} strip/sidecar geometry mismatch`)
  if (metadata.frames !== entry.frames || spec.frames !== entry.frames) fail(`${entry.name} frame count is stale`)
  for (const range of entry.fullFaceFrameRanges) if (range.length !== 2 || range[0] < 1 || range[1] < range[0] || range[1] > entry.frames) fail(`${entry.name} has an invalid full-face frame range`)
  const edgeCounts: number[] = []
  for (let frame = 0; frame < metadata.frames; frame += 1) {
    let count = 0
    const left = frame * frameWidth
    for (let y = 0; y < strip.height; y += 1) for (let x = 0; x < frameWidth; x += 1) {
      if (x !== 0 && x !== frameWidth - 1 && y !== 0 && y !== strip.height - 1) continue
      if (strip.data[((y * strip.width) + left + x) * 4 + 3] > 0) count += 1
    }
    edgeCounts.push(count)
  }
  if (edgeCounts.join(',') !== entry.opaqueCellEdgePixelsByFrame.join(',')) fail(`${entry.name} edge evidence is stale`)
  if (edgeCounts.reduce((sum, value) => sum + value, 0) !== entry.opaqueCellEdgePixels) fail(`${entry.name} edge total is stale`)
  if (withdrawn.has(entry.name) && entry.withdrawnAmendmentPolicy !== 'withdrawn-rejected-provenance-only') fail(`${entry.name} could reactivate a withdrawn candidate`)
}
const countMoney = entries.find(entry => entry.name === 'keeper_count_money')
if (countMoney?.withdrawnAmendmentPolicy !== 'deleted-do-not-regenerate') fail('keeper_count_money deletion gate is missing')

const publicPage = fs.readFileSync(PUBLIC_PAGE, 'utf8')
for (const value of [EXPECTED_PRIMARY_SHA, EXPECTED_QUALITY_SHA, register.candidate.sha256, 'Approved for small-batch authoring', 'Approve full-face canon pack V1. These are excellent', 'keeper_count_money']) if (!publicPage.includes(value)) fail(`public page omits ${value}`)
for (const match of publicPage.matchAll(/src="assets\/([^"]+\.png)"/g)) {
  const file = path.join(path.dirname(PUBLIC_PAGE), 'assets', match[1])
  if (!fs.existsSync(file)) fail(`published comparison asset is missing: ${match[1]}`)
  const hashPrefix = match[1].match(/-([0-9a-f]{16})\.png$/)?.[1]
  if (!hashPrefix || !sha256(file).startsWith(hashPrefix)) fail(`published comparison asset hash is stale: ${match[1]}`)
}
if (!fs.readFileSync(REVIEW_PAGE, 'utf8').includes('/keeper-review/full-face-canon-v1/')) fail('main reviewer does not link to the canon pack')

console.log(`Verified ${entries.length} full-face inventory assets and ${Object.keys(register.masksAndGuides).length} canon masks/guides; V1 remains byte-identical, gutter-safe and approved for batch authoring`)
