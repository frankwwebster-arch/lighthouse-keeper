#!/usr/bin/env node
import assert from 'node:assert/strict'
import crypto from 'node:crypto'
import fs from 'node:fs'
import { PNG } from 'pngjs'

const json = file => JSON.parse(fs.readFileSync(file, 'utf8'))
const hashBytes = bytes => crypto.createHash('sha256').update(bytes).digest('hex')
const hash = file => hashBytes(fs.readFileSync(file))
const record = json('data/kitchen_room_layout_review_v7.json')
const register = json(record.nativeAssets.register)
const v6 = json('art/drafts/kitchen-room-layout-review-2026-10-24-v6/native-assets/extraction-register.json')
const page = fs.readFileSync('public/keeper-review/kitchen-room-layout-v7/index.html', 'utf8')
const route = fs.readFileSync('src/app/keeper-review/kitchen-room-layout-v7/route.ts', 'utf8')
const archiveRoute = fs.readFileSync('src/app/keeper-review/[set]/assets/[asset]/route.ts', 'utf8')

assert.equal(hash(record.nativeAssets.register), record.nativeAssets.registerSha256)
assert.equal(register.schema, 'lighthouse-keeper/kitchen-native-assets@7')
assert.equal(register.predecessor.sha256, record.nativeAssets.predecessorRegisterSha256)
assert.equal(hash(register.predecessor.register), register.predecessor.sha256)
assert.equal(hash('public/sprites/room_kitchen.png'), 'c1cb3c90b911ea09ae13d8fd09297787b990b0997dc589fb9e6a62c658099eff')
assert.equal(record.boundary.runtimeChanged, false)
assert.equal(record.boundary.gameplayChanged, false)
assert.equal(record.boundary.approvedFittedUnitsChanged, false)
assert.equal(record.boundary.roomGridChanged, false)
for (const key of ['scaleApplied', 'downscalingApplied', 'resamplingApplied', 'colourTransformApplied']) assert.equal(register[key], false)

const changed = new Set(['fitted-overlay-on', 'chair-standard'])
const pngs = {}
for (const [id, output] of Object.entries(register.outputs)) {
  const bytes = fs.readFileSync(output.file)
  assert.equal(hashBytes(bytes), output.sha256, `${id} hash changed`)
  const png = PNG.sync.read(bytes)
  pngs[id] = png
  assert.deepEqual([png.width, png.height], output.dimensions)
  if (!changed.has(id)) assert.equal(output.sha256, v6.outputs[id].sha256, `${id} differs from immutable V6`)
}
assert.equal(register.outputs['fitted-units-static'].sha256, 'ba84022371aea330e2fe50e5ad8fb37bf9d210aa1e09649d7f2fc69f460f49b1')
assert.equal(register.outputs['fitted-overlay-on'].predecessorSha256, v6.outputs['fitted-overlay-on'].sha256)
assert.equal(register.outputs['chair-standard'].predecessorSha256, v6.outputs['chair-standard'].sha256)

const on = pngs['fitted-overlay-on']
const onV6 = PNG.sync.read(fs.readFileSync(v6.outputs['fitted-overlay-on'].file))
for (let y = 0; y < on.height; y += 1) for (let x = 0; x < on.width; x += 1) {
  if (x >= 521 && x <= 624 && y >= 42 && y <= 128) continue
  const i = (y * on.width + x) * 4
  assert.deepEqual([...on.data.slice(i, i + 4)], [...onV6.data.slice(i, i + 4)], `ON overlay changed outside sink correction at ${x},${y}`)
}
for (let y = 42; y <= 96; y += 1) {
  let rowHasWater = false
  for (let x = 545; x <= 570; x += 1) if (on.data[(y * on.width + x) * 4 + 3]) rowHasWater = true
  assert.equal(rowHasWater, true, `water does not continuously reach tap outlet at row ${y}`)
}
for (let y = 99; y <= 128; y += 1) for (let x = 521; x <= 624; x += 1) assert.equal(on.data[(y * on.width + x) * 4 + 3], 0, `water intrudes on opaque basin front at ${x},${y}`)
let sinkAlpha = 0
for (let y = 42; y <= 98; y += 1) for (let x = 521; x <= 624; x += 1) if (on.data[(y * on.width + x) * 4 + 3]) sinkAlpha += 1
assert.ok(sinkAlpha > 350 && sinkAlpha < 1500, `unexpected corrected sink alpha area ${sinkAlpha}`)

const chair = pngs['chair-standard']
const chairV6 = PNG.sync.read(fs.readFileSync(v6.outputs['chair-standard'].file))
for (const [x, y] of [[43, 70], [63, 70], [83, 70], [103, 70], [72, 150]]) {
  assert.equal(chairV6.data[(y * chair.width + x) * 4 + 3], 255, `V6 evidence point ${x},${y} was not opaque`)
  assert.equal(chair.data[(y * chair.width + x) * 4 + 3], 0, `V7 chair gap ${x},${y} is not transparent`)
}
for (let p = 0; p < chair.width * chair.height; p += 1) {
  const i = p * 4
  if (!chair.data[i + 3]) continue
  assert.deepEqual([...chair.data.slice(i, i + 4)], [...chairV6.data.slice(i, i + 4)], `chair wood pixel changed at ${p % chair.width},${Math.floor(p / chair.width)}`)
}
assert.equal(register.outputs['chair-standard'].transparentPaperComponentsRemoved, 5)

for (const required of [
  "const ROOT='/keeper-review/kitchen-room-layout-v7/assets/',V='?v=7';",
  'V6 predecessor ↔ V7 draft',
  'V6 · rejected rectangular crop',
  'V7 · transparent between slats',
  'predecessorProofUrls',
  '.asset.table{z-index:3}',
  "for(const name of ['kettle','toaster','bowl','bin','table','chair'])",
]) assert.ok(page.includes(required), `V7 page missing ${required}`)
assert.ok(route.includes('/keeper-review/kitchen-room-layout-v7/index.html'))
assert.ok(archiveRoute.includes("'kitchen-room-layout-v7'"))

const archive = json('review-archive/index.json')
const expected = [
  ['prime-keeper-neutral-native-256x320.png', register.keeperPresentation.neutral.sha256],
  ['prime-keeper-seated-back-native-256x320.png', register.keeperPresentation.seated.sha256],
  ...Object.values(register.outputs).map(output => [output.publicReviewFile.split('/').pop(), output.sha256]),
]
for (const [asset, expectedHash] of expected) {
  const pathname = `/keeper-review/kitchen-room-layout-v7/assets/${asset}`
  const entry = archive.legacyPaths[pathname]
  assert.ok(entry, `${pathname} not archived`)
  assert.equal(entry.sha256, expectedHash)
  assert.equal(fs.existsSync(`review-archive/${entry.object.replace(/^review-archive\//, '')}`), true)
  assert.equal(fs.existsSync(`public${pathname}`), false)
}
console.log('Kitchen room layout review V7 verified: tap-outlet flow, opaque basin front, transparent chair gaps, locked fitted base and unchanged gameplay.')
