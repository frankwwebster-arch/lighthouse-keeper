#!/usr/bin/env node
import assert from 'node:assert/strict'
import crypto from 'node:crypto'
import fs from 'node:fs'
import { PNG } from 'pngjs'

const json = file => JSON.parse(fs.readFileSync(file, 'utf8'))
const digest = bytes => crypto.createHash('sha256').update(bytes).digest('hex')
const hash = file => digest(fs.readFileSync(file))
const offset = (png, x, y) => (y * png.width + x) * 4
const alpha = (png, x, y) => png.data[offset(png, x, y) + 3]
const record = json('data/kitchen_room_layout_review_v11.json')
const register = json(record.nativeAssets.register)
const v10 = json(record.nativeAssets.predecessorRegister)
const page = fs.readFileSync('public/keeper-review/kitchen-room-layout-v11/index.html', 'utf8')
const route = fs.readFileSync('src/app/keeper-review/kitchen-room-layout-v11/route.ts', 'utf8')
const archiveRoute = fs.readFileSync('src/app/keeper-review/[set]/assets/[asset]/route.ts', 'utf8')

assert.equal(hash(record.nativeAssets.register), record.nativeAssets.registerSha256)
assert.equal(register.schema, 'lighthouse-keeper/kitchen-native-assets@11')
assert.equal(hash(register.predecessor.register), register.predecessor.sha256)
assert.equal(hash('public/sprites/room_kitchen.png'), 'c1cb3c90b911ea09ae13d8fd09297787b990b0997dc589fb9e6a62c658099eff')
assert.equal(register.outputs['fitted-units-static'].sha256, 'ba84022371aea330e2fe50e5ad8fb37bf9d210aa1e09649d7f2fc69f460f49b1')
for (const key of ['runtimeChanged', 'gameplayChanged', 'approvedFittedUnitsChanged', 'roomGridChanged']) assert.equal(record.boundary[key], false)
for (const key of ['scaleApplied', 'downscalingApplied', 'resamplingApplied']) assert.equal(register[key], false)
assert.equal(record.nativeAssets.approvedBaseColourTransformApplied, false)
assert.equal(record.nativeAssets.separateLightEffectToneMapApplied, true)

const changed = new Set([
  'broken-floor-water',
  'oven-broken-cavity-light',
  'oven-broken-fascia-pulse',
  'sink-broken-gush-1',
  'sink-broken-gush-2',
  'sink-broken-gush-3',
])
const pngs = {}
for (const [id, output] of Object.entries(register.outputs)) {
  const bytes = fs.readFileSync(output.file), png = PNG.sync.read(bytes)
  assert.equal(digest(bytes), output.sha256, `${id} hash changed`)
  assert.deepEqual([png.width, png.height], output.dimensions)
  pngs[id] = png
  if (!changed.has(id)) assert.equal(output.sha256, v10.outputs[id].sha256, `${id} differs from immutable V10`)
}

assert.equal(register.outputs['bowl-broken'].sha256, v10.outputs['bowl-broken'].sha256)
assert.equal(register.outputs['bowl-broken'].contactSurfaceRow, 54)
assert.equal(register.outputs['bowl-broken'].deepestAlphaRow, 64)
assert.deepEqual(register.outputs['bowl-broken'].hangingShardRows, [55, 64])

const water = pngs['broken-floor-water']
const countAlpha = (minX, maxX, minY = 0, maxY = water.height - 1) => {
  let count = 0
  for (let y = minY; y <= maxY; y += 1) for (let x = minX; x <= maxX; x += 1) if (alpha(water, x, y)) count += 1
  return count
}
assert.ok(countAlpha(360, 640) > 1500, 'sink floor spill missing')
assert.ok(countAlpha(700, 910) > 400, 'dishwasher floor spill missing')
assert.equal(countAlpha(911, 1144), 0, 'water is incorrectly assigned to the oven interval')
assert.ok(countAlpha(1145, 1375) > 250, 'fridge floor spill missing')
assert.equal(register.outputs['broken-floor-water'].supportPlane, 'walking-floor')

for (let frame = 1; frame <= 3; frame += 1) {
  const id = `sink-broken-gush-${frame}`, png = pngs[id]
  assert.deepEqual([png.width, png.height], [1368, 444])
  assert.equal(register.outputs[id].runAlignmentOffsetY, 160)
  assert.ok(countImageAlpha(png, 410, 710, 0, 159) > 1500, `${id} has no upward geyser above the fitted run`)
}

function countImageAlpha(png, minX, maxX, minY, maxY) {
  let count = 0
  for (let y = minY; y <= maxY; y += 1) for (let x = minX; x <= maxX; x += 1) if (alpha(png, x, y)) count += 1
  return count
}

const oven = pngs['oven-broken-cavity-light']
const [cavityX, cavityY, cavityW, cavityH] = register.outputs['oven-broken-cavity-light'].cavityBounds
let ovenInside = 0, ovenOutside = 0
for (let y = 0; y < oven.height; y += 1) for (let x = 0; x < oven.width; x += 1) {
  if (!alpha(oven, x, y)) continue
  if (x >= cavityX && x < cavityX + cavityW && y >= cavityY && y < cavityY + cavityH) ovenInside += 1
  else ovenOutside += 1
}
assert.ok(ovenInside > 13000, 'opaque lit oven cavity state is incomplete')
assert.equal(ovenOutside, 0, 'oven lit state escaped its cavity replacement bounds')

const fascia = pngs['oven-broken-fascia-pulse']
const [fasciaX, fasciaY, fasciaW, fasciaH] = register.outputs['oven-broken-fascia-pulse'].fasciaBounds
let fasciaInside = 0, fasciaOutside = 0
for (let y = 0; y < fascia.height; y += 1) for (let x = 0; x < fascia.width; x += 1) {
  if (!alpha(fascia, x, y)) continue
  if (x >= fasciaX && x < fasciaX + fasciaW && y >= fasciaY && y < fasciaY + fasciaH) fasciaInside += 1
  else fasciaOutside += 1
}
assert.ok(fasciaInside > 250, 'oven fascia pulse is incomplete')
assert.equal(fasciaOutside, 0, 'oven fascia pulse moved outside its fixed lens bounds')

for (const required of [
  "const ROOT='/keeper-review/kitchen-room-layout-v11/assets/',V='?v=11';",
  'Review-only V11',
  'V10 predecessor ↔ V11 Broken-state correction',
  'broken:54},anchors:{standard:69,broken:65}',
  'oven-broken-fascia-pulse-native.png',
  '.run .sinkGush{top:-160px;height:444px}',
  'OTT sink geyser',
  'Reject V11 by discarding only its page, route and V11 native correction directory. V1–V10',
  "'Ready: V11 broken oven, bowl contact and appliance spills corrected.'",
]) assert.ok(page.includes(required), `V11 page missing ${required}`)
assert.equal(page.includes('broken:64},anchors:{standard:69,broken:65}'), false)
assert.equal(page.includes('Review-only V10'), false)
assert.ok(route.includes('/keeper-review/kitchen-room-layout-v11/index.html'))
assert.ok(archiveRoute.includes("'kitchen-room-layout-v11'"))

const archive = json('review-archive/index.json')
const expected = [
  ['prime-keeper-neutral-native-256x320.png', register.keeperPresentation.neutral.sha256],
  ['prime-keeper-seated-back-native-256x320.png', register.keeperPresentation.seated.sha256],
  ...Object.values(register.outputs).map(output => [output.publicReviewFile.split('/').pop(), output.sha256]),
]
for (const [asset, expectedHash] of expected) {
  const pathname = `/keeper-review/kitchen-room-layout-v11/assets/${asset}`, entry = archive.legacyPaths[pathname]
  assert.ok(entry, `${pathname} not archived`)
  assert.equal(entry.sha256, expectedHash)
  assert.equal(fs.existsSync(`review-archive/${entry.object.replace(/^review-archive\//, '')}`), true)
  assert.equal(fs.existsSync(`public${pathname}`), false)
}
console.log('Kitchen room layout review V11 verified: explicit bowl contact, opaque oven cavity flicker, fixed fascia pulse, OTT upward sink geyser, sink/dishwasher/fridge floor spills, no oven water, unchanged fitted base and gameplay.')
