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
const record = json('data/kitchen_room_layout_review_v9.json')
const register = json(record.nativeAssets.register)
const v8 = json(record.nativeAssets.predecessorRegister)
const page = fs.readFileSync('public/keeper-review/kitchen-room-layout-v9/index.html', 'utf8')
const route = fs.readFileSync('src/app/keeper-review/kitchen-room-layout-v9/route.ts', 'utf8')
const archiveRoute = fs.readFileSync('src/app/keeper-review/[set]/assets/[asset]/route.ts', 'utf8')

assert.equal(hash(record.nativeAssets.register), record.nativeAssets.registerSha256)
assert.equal(register.schema, 'lighthouse-keeper/kitchen-native-assets@9')
assert.equal(hash(register.predecessor.register), register.predecessor.sha256)
assert.equal(hash('public/sprites/room_kitchen.png'), 'c1cb3c90b911ea09ae13d8fd09297787b990b0997dc589fb9e6a62c658099eff')
assert.equal(register.outputs['fitted-units-static'].sha256, 'ba84022371aea330e2fe50e5ad8fb37bf9d210aa1e09649d7f2fc69f460f49b1')
for (const key of ['runtimeChanged', 'gameplayChanged', 'approvedFittedUnitsChanged', 'roomGridChanged']) assert.equal(record.boundary[key], false)
for (const key of ['scaleApplied', 'downscalingApplied', 'resamplingApplied', 'colourTransformApplied']) assert.equal(register[key], false)

const changed = new Set(['bowl-broken', 'broken-floor-water'])
const pngs = {}
for (const [id, output] of Object.entries(register.outputs)) {
  const bytes = fs.readFileSync(output.file), png = PNG.sync.read(bytes)
  assert.equal(digest(bytes), output.sha256, `${id} hash changed`)
  assert.deepEqual([png.width, png.height], output.dimensions)
  pngs[id] = png
  if (!changed.has(id)) assert.equal(output.sha256, v8.outputs[id].sha256, `${id} differs from immutable V8`)
}

const bowl = pngs['bowl-broken']
for (let x = 0; x < bowl.width; x += 1) for (const y of [...Array(8).keys(), ...Array.from({ length: 8 }, (_, i) => bowl.height - 8 + i)]) assert.equal(alpha(bowl, x, y), 0, 'bowl lacks vertical safety gutter')
for (let y = 0; y < bowl.height; y += 1) for (const x of [...Array(8).keys(), ...Array.from({ length: 8 }, (_, i) => bowl.width - 8 + i)]) assert.equal(alpha(bowl, x, y), 0, 'bowl lacks horizontal safety gutter')
let removedPanelPixels = 0
for (let y = 49; y < bowl.height - 8; y += 1) for (let x = 8; x <= 76; x += 1) if (alpha(bowl, x, y)) removedPanelPixels += 1
assert.ok(removedPanelPixels < 160, `front-left bowl panel remains (${removedPanelPixels} opaque pixels)`)
assert.equal(register.outputs['bowl-broken'].frontLeftPanelRemoved, true)

const water = pngs['broken-floor-water']
let waterPixels = 0
for (let y = 0; y < water.height; y += 1) for (let x = 0; x < water.width; x += 1) if (alpha(water, x, y)) {
  waterPixels += 1
  assert.ok(x >= 360 && x <= 640 && y >= 10, `floor water escaped sink footprint at ${x},${y}`)
}
assert.ok(waterPixels > 1000, 'sink puddle is unexpectedly empty')

for (const required of [
  "const ROOT='/keeper-review/kitchen-room-layout-v9/assets/',V='?v=9';",
  'Review-only V9',
  'V8 predecessor ↔ V9 final correction',
  'Reject V9 by discarding only its page, route and V9 native correction directory. V1–V8',
  "'Ready: V9 broken bowl and sink-owned water corrected.'",
  "sink:['sink-broken-gush-1-native.png','sink-broken-gush-2-native.png','sink-broken-gush-3-native.png']",
]) assert.ok(page.includes(required), `V9 page missing ${required}`)
assert.equal(page.includes('Review-only V6'), false)
assert.ok(route.includes('/keeper-review/kitchen-room-layout-v9/index.html'))
assert.ok(archiveRoute.includes("'kitchen-room-layout-v9'"))

const archive = json('review-archive/index.json')
const expected = [
  ['prime-keeper-neutral-native-256x320.png', register.keeperPresentation.neutral.sha256],
  ['prime-keeper-seated-back-native-256x320.png', register.keeperPresentation.seated.sha256],
  ...Object.values(register.outputs).map(output => [output.publicReviewFile.split('/').pop(), output.sha256]),
]
for (const [asset, expectedHash] of expected) {
  const pathname = `/keeper-review/kitchen-room-layout-v9/assets/${asset}`, entry = archive.legacyPaths[pathname]
  assert.ok(entry, `${pathname} not archived`)
  assert.equal(entry.sha256, expectedHash)
  assert.equal(fs.existsSync(`review-archive/${entry.object.replace(/^review-archive\//, '')}`), true)
  assert.equal(fs.existsSync(`public${pathname}`), false)
}
console.log('Kitchen room layout review V9 verified: open debris-free bowl, sink-footprint puddle, immutable V8 inheritance, no scaling and unchanged gameplay.')
