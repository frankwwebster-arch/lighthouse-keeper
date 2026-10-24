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
const record = json('data/kitchen_room_layout_review_v10.json')
const register = json(record.nativeAssets.register)
const v9 = json(record.nativeAssets.predecessorRegister)
const page = fs.readFileSync('public/keeper-review/kitchen-room-layout-v10/index.html', 'utf8')
const route = fs.readFileSync('src/app/keeper-review/kitchen-room-layout-v10/route.ts', 'utf8')
const archiveRoute = fs.readFileSync('src/app/keeper-review/[set]/assets/[asset]/route.ts', 'utf8')

assert.equal(hash(record.nativeAssets.register), record.nativeAssets.registerSha256)
assert.equal(register.schema, 'lighthouse-keeper/kitchen-native-assets@10')
assert.equal(hash(register.predecessor.register), register.predecessor.sha256)
assert.equal(hash('public/sprites/room_kitchen.png'), 'c1cb3c90b911ea09ae13d8fd09297787b990b0997dc589fb9e6a62c658099eff')
assert.equal(register.outputs['fitted-units-static'].sha256, 'ba84022371aea330e2fe50e5ad8fb37bf9d210aa1e09649d7f2fc69f460f49b1')
for (const key of ['runtimeChanged', 'gameplayChanged', 'approvedFittedUnitsChanged', 'roomGridChanged']) assert.equal(record.boundary[key], false)
for (const key of ['scaleApplied', 'downscalingApplied', 'resamplingApplied', 'colourTransformApplied']) assert.equal(register[key], false)

const pngs = {}
for (const [id, output] of Object.entries(register.outputs)) {
  const bytes = fs.readFileSync(output.file), png = PNG.sync.read(bytes)
  assert.equal(digest(bytes), output.sha256, `${id} hash changed`)
  assert.deepEqual([png.width, png.height], output.dimensions)
  pngs[id] = png
  if (id !== 'fitted-overlay-on') assert.equal(output.sha256, v9.outputs[id].sha256, `${id} differs from immutable V9`)
}

const on = pngs['fitted-overlay-on']
const oldOn = PNG.sync.read(fs.readFileSync(v9.outputs['fitted-overlay-on'].file))
let streamPixels = 0
for (let y = 0; y < on.height; y += 1) for (let x = 0; x < on.width; x += 1) {
  const i = offset(on, x, y)
  if (!(x >= 500 && x <= 650 && y >= 42 && y <= 98)) {
    assert.deepEqual([...on.data.slice(i, i + 4)], [...oldOn.data.slice(i, i + 4)], `ON overlay changed outside sink water at ${x},${y}`)
  }
  if (x >= 500 && x <= 650 && y >= 42 && y <= 98 && alpha(on, x, y)) {
    streamPixels += 1
    assert.ok(x >= 552 && x <= 561, `ON water escaped the straight stream at ${x},${y}`)
  }
}
for (let y = 42; y <= 98; y += 1) {
  let rowHasWater = false
  for (let x = 552; x <= 561; x += 1) if (alpha(on, x, y)) rowHasWater = true
  assert.equal(rowHasWater, true, `straight ON stream is interrupted at row ${y}`)
}
assert.ok(streamPixels > 400 && streamPixels < 550, `unexpected straight-stream alpha area ${streamPixels}`)
assert.equal(register.outputs['fitted-overlay-on'].splashPixelsRemoved, true)
assert.deepEqual(register.outputs['fitted-overlay-on'].straightStreamBounds, [552, 42, 561, 98])

for (const required of [
  "const ROOT='/keeper-review/kitchen-room-layout-v10/assets/',V='?v=10';",
  'Review-only V10',
  'V9 predecessor ↔ V10 ON sink correction',
  'V10 · straight stream only',
  'Reject V10 by discarding only its page, route and V10 native correction directory. V1–V9',
  "'Ready: V10 ON tap stream is straight with no pooling.'",
]) assert.ok(page.includes(required), `V10 page missing ${required}`)
assert.equal(page.includes('Review-only V9'), false)
assert.ok(route.includes('/keeper-review/kitchen-room-layout-v10/index.html'))
assert.ok(archiveRoute.includes("'kitchen-room-layout-v10'"))

const archive = json('review-archive/index.json')
const expected = [
  ['prime-keeper-neutral-native-256x320.png', register.keeperPresentation.neutral.sha256],
  ['prime-keeper-seated-back-native-256x320.png', register.keeperPresentation.seated.sha256],
  ...Object.values(register.outputs).map(output => [output.publicReviewFile.split('/').pop(), output.sha256]),
]
for (const [asset, expectedHash] of expected) {
  const pathname = `/keeper-review/kitchen-room-layout-v10/assets/${asset}`, entry = archive.legacyPaths[pathname]
  assert.ok(entry, `${pathname} not archived`)
  assert.equal(entry.sha256, expectedHash)
  assert.equal(fs.existsSync(`review-archive/${entry.object.replace(/^review-archive\//, '')}`), true)
  assert.equal(fs.existsSync(`public${pathname}`), false)
}
console.log('Kitchen room layout review V10 verified: straight ON tap stream, zero splash/pooling, immutable V9 inheritance, no scaling and unchanged gameplay.')
