#!/usr/bin/env node
import assert from 'node:assert/strict'
import crypto from 'node:crypto'
import fs from 'node:fs'
import vm from 'node:vm'
import { PNG } from 'pngjs'

const json = file => JSON.parse(fs.readFileSync(file, 'utf8'))
const digest = bytes => crypto.createHash('sha256').update(bytes).digest('hex')
const hash = file => digest(fs.readFileSync(file))
const offset = (png, x, y) => (y * png.width + x) * 4
const alpha = (png, x, y) => png.data[offset(png, x, y) + 3]
const record = json('data/kitchen_room_layout_review_v12.json')
const register = json(record.nativeAssets.register)
const v11 = json(record.nativeAssets.predecessorRegister)
const page = fs.readFileSync('public/keeper-review/kitchen-room-layout-v12/index.html', 'utf8')
const route = fs.readFileSync('src/app/keeper-review/kitchen-room-layout-v12/route.ts', 'utf8')
const archiveRoute = fs.readFileSync('src/app/keeper-review/[set]/assets/[asset]/route.ts', 'utf8')

assert.equal(hash(record.nativeAssets.register), record.nativeAssets.registerSha256)
assert.equal(register.schema, 'lighthouse-keeper/kitchen-native-assets@12')
assert.equal(hash(register.predecessor.register), register.predecessor.sha256)
assert.equal(register.predecessor.sha256, 'ff79b7db93ae3ddceaaadc35b2a731656b2cb7f78f5bd8b2ccdca6550a93b26c')
assert.equal(hash('public/sprites/room_kitchen.png'), 'c1cb3c90b911ea09ae13d8fd09297787b990b0997dc589fb9e6a62c658099eff')
assert.equal(register.outputs['fitted-units-static'].sha256, 'ba84022371aea330e2fe50e5ad8fb37bf9d210aa1e09649d7f2fc69f460f49b1')
for (const key of ['runtimeChanged', 'gameplayChanged', 'approvedFittedUnitsChanged', 'roomGridChanged']) assert.equal(record.boundary[key], false)
for (const key of ['scaleApplied', 'downscalingApplied', 'resamplingApplied']) assert.equal(register[key], false)
assert.equal(record.nativeAssets.approvedBaseColourTransformApplied, false)
assert.equal(record.nativeAssets.separateLightEffectToneMapApplied, true)

const changed = new Set(['fitted-overlay-broken', 'oven-broken-cavity-light', 'dishwasher-warning-1', 'dishwasher-warning-2', 'dishwasher-warning-3'])
const pngs = {}
for (const [id, output] of Object.entries(register.outputs)) {
  const bytes = fs.readFileSync(output.file)
  const png = PNG.sync.read(bytes)
  assert.equal(digest(bytes), output.sha256, `${id} hash changed`)
  assert.deepEqual([png.width, png.height], output.dimensions)
  pngs[id] = png
  if (!changed.has(id)) assert.equal(output.sha256, v11.outputs[id].sha256, `${id} differs from immutable V11`)
}
assert.equal('oven-broken-fascia-pulse' in register.outputs, false)
assert.equal(register.outputs['bowl-broken'].sha256, v11.outputs['bowl-broken'].sha256)
assert.equal(register.outputs['broken-floor-water'].sha256, v11.outputs['broken-floor-water'].sha256)
for (let frame = 1; frame <= 3; frame += 1) assert.equal(register.outputs[`sink-broken-gush-${frame}`].sha256, v11.outputs[`sink-broken-gush-${frame}`].sha256)
assert.equal(register.reviewCalibration.sinkEffectOffsetY, -8)
assert.equal(register.reviewCalibration.brokenBowlInitialContactOffsetY, 0)

const broken = pngs['fitted-overlay-broken']
const v11Broken = PNG.sync.read(fs.readFileSync(v11.outputs['fitted-overlay-broken'].file))
const [moduleX, moduleY, moduleW, moduleH] = register.outputs['fitted-overlay-broken'].ovenModuleBounds
let moduleAlpha = 0
for (let y = 0; y < broken.height; y += 1) for (let x = 0; x < broken.width; x += 1) {
  const inside = x >= moduleX && x < moduleX + moduleW && y >= moduleY && y < moduleY + moduleH
  if (inside) moduleAlpha += alpha(broken, x, y) ? 1 : 0
  else {
    const i = offset(broken, x, y)
    assert.deepEqual([...broken.data.subarray(i, i + 4)], [...v11Broken.data.subarray(i, i + 4)], `broken overlay changed outside oven module at ${x},${y}`)
  }
}
assert.equal(moduleAlpha, 0, 'rejected open oven survived in Broken overlay')

const oven = pngs['oven-broken-cavity-light']
const [cavityX, cavityY, cavityW, cavityH] = register.outputs['oven-broken-cavity-light'].cavityBounds
let ovenInside = 0, ovenOutside = 0
for (let y = 0; y < oven.height; y += 1) for (let x = 0; x < oven.width; x += 1) {
  if (!alpha(oven, x, y)) continue
  if (x >= cavityX && x < cavityX + cavityW && y >= cavityY && y < cavityY + cavityH) ovenInside += 1
  else ovenOutside += 1
}
assert.ok(ovenInside > 13000, 'closed oven lit cavity is incomplete')
assert.equal(ovenOutside, 0, 'closed oven light escaped the existing glass/cavity bounds')

for (let number = 1; number <= 3; number += 1) {
  const id = `dishwasher-warning-${number}`
  const output = register.outputs[id], png = pngs[id]
  assert.deepEqual(output.dimensions, [22, 24])
  assert.equal(output.transparentSafetyGutter, 4)
  assert.deepEqual(output.basePosition, register.reviewCalibration.dishwasherWarningBasePositions[number - 1])
  for (let x = 0; x < png.width; x += 1) for (const y of [0, 1, 2, 3, png.height - 4, png.height - 3, png.height - 2, png.height - 1]) assert.equal(alpha(png, x, y), 0, `${id} lacks vertical safety gutter`)
  for (let y = 0; y < png.height; y += 1) for (const x of [0, 1, 2, 3, png.width - 4, png.width - 3, png.width - 2, png.width - 1]) assert.equal(alpha(png, x, y), 0, `${id} lacks horizontal safety gutter`)
}

for (const required of [
  "const ROOT='/keeper-review/kitchen-room-layout-v12/assets/',V='?v=12';",
  'Review-only V12',
  'V11 predecessor ↔ V12 positioning correction',
  '.run .sinkGush{top:-168px;height:444px}',
  '.run img{pointer-events:none}.run .warningLight{inset:auto;width:auto;height:auto;max-width:none;pointer-events:auto',
  'const WARNING_BASES=[[720,116],[742,116],[764,116]]',
  'startWarningDrag',
  'Dishwasher lens offsets',
  'Broken bowl contact',
  'closed oven cavity flicker',
  'Reject V12 by discarding only its page, route and V12 native correction directory. V1–V11',
  "'Ready: V12 closed-oven flicker and exact effect-position controls loaded.'",
]) assert.ok(page.includes(required), `V12 page missing ${required}`)
assert.equal(page.includes('ovenFascia'), false)
assert.equal(page.includes('oven-broken-fascia-pulse-native.png'), false)
assert.equal(page.includes('/keeper-review/kitchen-room-layout-v11/assets/'), false)
for (const script of [...page.matchAll(/<script>([\s\S]*?)<\/script>/g)].map(match => match[1])) new vm.Script(script)
assert.ok(route.includes('/keeper-review/kitchen-room-layout-v12/index.html'))
assert.ok(archiveRoute.includes("'kitchen-room-layout-v12'"))

const archive = json('review-archive/index.json')
const expected = [
  ['prime-keeper-neutral-native-256x320.png', register.keeperPresentation.neutral.sha256],
  ['prime-keeper-seated-back-native-256x320.png', register.keeperPresentation.seated.sha256],
  ...Object.values(register.outputs).map(output => [output.publicReviewFile.split('/').pop(), output.sha256]),
]
for (const [asset, expectedHash] of expected) {
  const pathname = `/keeper-review/kitchen-room-layout-v12/assets/${asset}`
  const entry = archive.legacyPaths[pathname]
  assert.ok(entry, `${pathname} not archived`)
  assert.equal(entry.sha256, expectedHash)
  assert.equal(fs.existsSync(`review-archive/${entry.object.replace(/^review-archive\//, '')}`), true)
  assert.equal(fs.existsSync(`public${pathname}`), false)
}

console.log('Kitchen room layout review V12 verified: rear-shifted unchanged geyser, isolated draggable warning lenses, closed oven with behind-glass cavity flicker, bowl contact calibration, unchanged fitted base/grid/runtime/gameplay.')
