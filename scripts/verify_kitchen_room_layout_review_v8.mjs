#!/usr/bin/env node
import assert from 'node:assert/strict'
import crypto from 'node:crypto'
import fs from 'node:fs'
import { PNG } from 'pngjs'

const json = file => JSON.parse(fs.readFileSync(file, 'utf8'))
const hashBytes = bytes => crypto.createHash('sha256').update(bytes).digest('hex')
const hash = file => hashBytes(fs.readFileSync(file))
const pixel = (png, x, y) => (y * png.width + x) * 4
const alpha = (png, x, y) => png.data[pixel(png, x, y) + 3]
const record = json('data/kitchen_room_layout_review_v8.json')
const register = json(record.nativeAssets.register)
const v7 = json('art/drafts/kitchen-room-layout-review-2026-10-25-v7/native-assets/extraction-register.json')
const page = fs.readFileSync('public/keeper-review/kitchen-room-layout-v8/index.html', 'utf8')
const route = fs.readFileSync('src/app/keeper-review/kitchen-room-layout-v8/route.ts', 'utf8')
const archiveRoute = fs.readFileSync('src/app/keeper-review/[set]/assets/[asset]/route.ts', 'utf8')

assert.equal(hash(record.nativeAssets.register), record.nativeAssets.registerSha256)
assert.equal(register.schema, 'lighthouse-keeper/kitchen-native-assets@8')
assert.equal(register.predecessor.sha256, record.nativeAssets.predecessorRegisterSha256)
assert.equal(hash(register.predecessor.register), register.predecessor.sha256)
assert.equal(hash('public/sprites/room_kitchen.png'), 'c1cb3c90b911ea09ae13d8fd09297787b990b0997dc589fb9e6a62c658099eff')
assert.equal(register.outputs['fitted-units-static'].sha256, 'ba84022371aea330e2fe50e5ad8fb37bf9d210aa1e09649d7f2fc69f460f49b1')
assert.equal(record.boundary.runtimeChanged, false)
assert.equal(record.boundary.gameplayChanged, false)
assert.equal(record.boundary.approvedFittedUnitsChanged, false)
assert.equal(record.boundary.roomGridChanged, false)
for (const key of ['scaleApplied', 'downscalingApplied', 'resamplingApplied', 'colourTransformApplied']) assert.equal(register[key], false)

const changed = new Set([
  'toaster-broken', 'bowl-broken', 'fitted-overlay-broken', 'broken-floor-water',
  'dishwasher-warning-1', 'dishwasher-warning-2', 'dishwasher-warning-3',
  'oven-broken-cavity-light', 'sink-broken-gush-1', 'sink-broken-gush-2', 'sink-broken-gush-3',
])
const pngs = {}
for (const [id, output] of Object.entries(register.outputs)) {
  const bytes = fs.readFileSync(output.file)
  assert.equal(hashBytes(bytes), output.sha256, `${id} hash changed`)
  const png = PNG.sync.read(bytes)
  pngs[id] = png
  assert.deepEqual([png.width, png.height], output.dimensions)
  if (!changed.has(id)) assert.equal(output.sha256, v7.outputs[id].sha256, `${id} differs from immutable V7`)
}

for (const id of ['toaster-broken', 'bowl-broken']) {
  const png = pngs[id]
  for (let x = 0; x < png.width; x += 1) {
    for (let y = 0; y < 8; y += 1) assert.equal(alpha(png, x, y), 0, `${id} lacks top safety gutter`)
    for (let y = png.height - 8; y < png.height; y += 1) assert.equal(alpha(png, x, y), 0, `${id} lacks bottom safety gutter`)
  }
  for (let y = 0; y < png.height; y += 1) {
    for (let x = 0; x < 8; x += 1) assert.equal(alpha(png, x, y), 0, `${id} lacks left safety gutter`)
    for (let x = png.width - 8; x < png.width; x += 1) assert.equal(alpha(png, x, y), 0, `${id} lacks right safety gutter`)
  }
}
assert.equal(register.outputs['toaster-broken'].detachedDebrisRemoved, 2)
assert.equal(register.outputs['bowl-broken'].detachedDebrisRemoved, 2)
assert.equal(register.outputs['bowl-broken'].hangingFrontPanelRemoved, true)
let bowlBreakAlpha = 0
for (let y = 32; y <= 72; y += 1) for (let x = 57; x <= 94; x += 1) bowlBreakAlpha += alpha(pngs['bowl-broken'], x, y) > 0 ? 1 : 0
assert.ok(bowlBreakAlpha < 460, `bowl front break closed unexpectedly (${bowlBreakAlpha} opaque pixels)`)

const floorWater = pngs['broken-floor-water']
for (let y = 0; y < floorWater.height; y += 1) for (let x = 0; x < floorWater.width; x += 1) {
  if (x < 360 || x > 760 || y < 10) assert.equal(alpha(floorWater, x, y), 0, `floor water escaped sink ownership at ${x},${y}`)
}
const broken = pngs['fitted-overlay-broken']
for (let y = 248; y < broken.height; y += 1) for (let x = 0; x < broken.width; x += 1) {
  const i = pixel(broken, x, y), r = broken.data[i], g = broken.data[i + 1], b = broken.data[i + 2]
  assert.ok(!(broken.data[i + 3] && g > 140 && b > 175 && b > r + 20), `water-like pixel remains in appliance overlay at ${x},${y}`)
}

for (const id of ['dishwasher-warning-1', 'dishwasher-warning-2', 'dishwasher-warning-3']) {
  const png = pngs[id]
  let count = 0, minx = png.width, miny = png.height, maxx = -1, maxy = -1
  for (let y = 0; y < png.height; y += 1) for (let x = 0; x < png.width; x += 1) if (alpha(png, x, y)) {
    count += 1; minx = Math.min(minx, x); miny = Math.min(miny, y); maxx = Math.max(maxx, x); maxy = Math.max(maxy, y)
  }
  assert.ok(count > 30 && count < 240, `${id} is not a compact fixed lens`)
  assert.ok(maxx - minx <= 20 && maxy - miny <= 20, `${id} retained a moving source rectangle`)
}

const oven = pngs['oven-broken-cavity-light']
let ovenPixels = 0
for (let y = 0; y < oven.height; y += 1) for (let x = 0; x < oven.width; x += 1) if (alpha(oven, x, y)) {
  ovenPixels += 1
  assert.ok(x >= 944 && x <= 1110 && y >= 174 && y <= 229, `oven light escaped cavity at ${x},${y}`)
}
assert.ok(ovenPixels > 1000, 'oven cavity light is unexpectedly empty')

for (const id of ['sink-broken-gush-1', 'sink-broken-gush-2', 'sink-broken-gush-3']) {
  const png = pngs[id]
  for (let y = 42; y <= 96; y += 1) {
    let rowHasWater = false
    for (let x = 535; x <= 582; x += 1) if (alpha(png, x, y)) rowHasWater = true
    assert.equal(rowHasWater, true, `${id} does not reach the tap outlet at row ${y}`)
  }
  for (let y = 99; y < png.height; y += 1) for (let x = 500; x <= 645; x += 1) assert.equal(alpha(png, x, y), 0, `${id} intrudes on the opaque basin front at ${x},${y}`)
}

for (const required of [
  "const ROOT='/keeper-review/kitchen-room-layout-v8/assets/',V='?v=8';",
  'V7 predecessor ↔ V8 broken-state draft',
  "sink:['sink-broken-gush-1-native.png','sink-broken-gush-2-native.png','sink-broken-gush-3-native.png']",
  '.camera.broken .g1{animation:gush1',
  '.camera.broken .ovenLight{animation:ovenBlink',
  'document.querySelectorAll(\'.warningLight,.sinkGush\')',
  '.asset.table{z-index:3}',
]) assert.ok(page.includes(required), `V8 page missing ${required}`)
assert.equal(page.includes('26%,59%{opacity:0}}.asset'), false, 'V8 page retained malformed V7 animation CSS')
assert.ok(route.includes('/keeper-review/kitchen-room-layout-v8/index.html'))
assert.ok(archiveRoute.includes("'kitchen-room-layout-v8'"))

const archive = json('review-archive/index.json')
const expected = [
  ['prime-keeper-neutral-native-256x320.png', register.keeperPresentation.neutral.sha256],
  ['prime-keeper-seated-back-native-256x320.png', register.keeperPresentation.seated.sha256],
  ...Object.values(register.outputs).map(output => [output.publicReviewFile.split('/').pop(), output.sha256]),
]
for (const [asset, expectedHash] of expected) {
  const pathname = `/keeper-review/kitchen-room-layout-v8/assets/${asset}`
  const entry = archive.legacyPaths[pathname]
  assert.ok(entry, `${pathname} not archived`)
  assert.equal(entry.sha256, expectedHash)
  assert.equal(fs.existsSync(`review-archive/${entry.object.replace(/^review-archive\//, '')}`), true)
  assert.equal(fs.existsSync(`public${pathname}`), false)
}
console.log('Kitchen room layout review V8 verified: debris-free supports, open bowl break, sink-owned water, fixed dishwasher lenses, cavity-only oven flicker, locked fitted base and unchanged gameplay.')
