#!/usr/bin/env node
import assert from 'node:assert/strict'
import crypto from 'node:crypto'
import fs from 'node:fs'
import vm from 'node:vm'
import { PNG } from 'pngjs'

const json = file => JSON.parse(fs.readFileSync(file, 'utf8'))
const digest = bytes => crypto.createHash('sha256').update(bytes).digest('hex')
const hash = file => digest(fs.readFileSync(file))
const pixelOffset = (png, x, y) => (y * png.width + x) * 4
const alpha = (png, x, y) => png.data[pixelOffset(png, x, y) + 3]
const record = json('data/kitchen_room_layout_review_v13.json')
const register = json(record.nativeAssets.register)
const v12 = json(record.nativeAssets.predecessorRegister)
const page = fs.readFileSync('public/keeper-review/kitchen-room-layout-v13/index.html', 'utf8')
const route = fs.readFileSync('src/app/keeper-review/kitchen-room-layout-v13/route.ts', 'utf8')
const archiveRoute = fs.readFileSync('src/app/keeper-review/[set]/assets/[asset]/route.ts', 'utf8')

assert.equal(hash(record.nativeAssets.register), record.nativeAssets.registerSha256)
assert.equal(register.schema, 'lighthouse-keeper/kitchen-native-assets@13')
assert.equal(hash(register.predecessor.register), register.predecessor.sha256)
assert.equal(register.predecessor.sha256, 'fa7eb77f5d9b68db2e104e369401bc1e8e410d15ef78ad9a4ab8c9d7fcbdacfd')
assert.equal(hash('public/sprites/room_kitchen.png'), 'c1cb3c90b911ea09ae13d8fd09297787b990b0997dc589fb9e6a62c658099eff')
assert.equal(register.outputs['fitted-units-static'].sha256, 'ba84022371aea330e2fe50e5ad8fb37bf9d210aa1e09649d7f2fc69f460f49b1')
for (const key of ['runtimeChanged', 'gameplayChanged', 'approvedFittedUnitsChanged', 'roomGridChanged']) assert.equal(record.boundary[key], false)
for (const key of ['scaleApplied', 'downscalingApplied', 'resamplingApplied']) assert.equal(register[key], false)
assert.equal(record.nativeAssets.approvedBaseColourTransformApplied, false)
assert.equal(record.nativeAssets.separateEffectColourTransformsApplied, true)
assert.deepEqual(register.reviewCalibration.dishwasherWarningAcceptedOffsets, [[-5, -2], [-5, -2], [-5, -2]])
assert.deepEqual(register.reviewCalibration.dishwasherWarningColours, ['amber', 'cyan', 'violet'])

const changed = new Set([
  'bowl-broken', 'fitted-overlay-broken', 'broken-floor-water',
  'dishwasher-warning-1', 'dishwasher-warning-2', 'dishwasher-warning-3',
  'dishwasher-warning-1-cyan', 'dishwasher-warning-1-violet',
  'dishwasher-warning-2-cyan', 'dishwasher-warning-2-violet',
  'dishwasher-warning-3-cyan', 'dishwasher-warning-3-violet',
])
const pngs = {}
for (const [id, output] of Object.entries(register.outputs)) {
  const bytes = fs.readFileSync(output.file)
  const png = PNG.sync.read(bytes)
  assert.equal(digest(bytes), output.sha256, `${id} hash changed`)
  assert.deepEqual([png.width, png.height], output.dimensions)
  pngs[id] = png
  if (!changed.has(id)) assert.equal(output.sha256, v12.outputs[id].sha256, `${id} differs from immutable V12`)
}

const bowl = pngs['bowl-broken']
assert.deepEqual([bowl.width, bowl.height], [137, 125])
assert.equal(register.outputs['bowl-broken'].contactRow, 116)
assert.equal(register.outputs['bowl-broken'].anchorX, 69)
assert.equal(register.outputs['bowl-broken'].fullBaseRetained, true)
assert.equal(alpha(bowl, 40, 60), 0, 'broken front-left section was not removed')
assert.ok([...Array(bowl.width).keys()].filter(x => alpha(bowl, x, 116)).length >= 18, 'bowl foot/base does not reach its declared contact row')
assert.ok([...Array(17).keys()].flatMap(dy => [...Array(bowl.width).keys()].map(x => alpha(bowl, x, 100 + dy))).filter(Boolean).length > 650, 'bowl base is incomplete')

const broken = pngs['fitted-overlay-broken']
const v12Broken = PNG.sync.read(fs.readFileSync(v12.outputs['fitted-overlay-broken'].file))
const warningRects = register.outputs['fitted-overlay-broken'].neutralisedWarningLensRects
let changedInside = 0
for (let y = 0; y < broken.height; y += 1) for (let x = 0; x < broken.width; x += 1) {
  const inside = warningRects.some(([rx, ry, rw, rh]) => x >= rx && x < rx + rw && y >= ry && y < ry + rh)
  const i = pixelOffset(broken, x, y)
  const same = broken.data.subarray(i, i + 4).every((value, channel) => value === v12Broken.data[i + channel])
  if (inside) changedInside += same ? 0 : 1
  else assert.equal(same, true, `broken overlay changed outside old warning-lens bounds at ${x},${y}`)
}
assert.ok(changedInside > 500, 'old fixed warning lamps were not neutralised')

for (let number = 1; number <= 3; number += 1) for (const colour of ['amber', 'cyan', 'violet']) {
  const id = colour === 'amber' ? `dishwasher-warning-${number}` : `dishwasher-warning-${number}-${colour}`
  const png = pngs[id], output = register.outputs[id]
  assert.deepEqual(output.dimensions, [22, 24])
  assert.equal(output.transparentSafetyGutter, 4)
  assert.equal(output.lightColour, colour)
  for (let x = 0; x < png.width; x += 1) for (const y of [0, 1, 2, 3, 20, 21, 22, 23]) assert.equal(alpha(png, x, y), 0, `${id} lacks vertical safety gutter`)
  for (let y = 0; y < png.height; y += 1) for (const x of [0, 1, 2, 3, 18, 19, 20, 21]) assert.equal(alpha(png, x, y), 0, `${id} lacks horizontal safety gutter`)
}

const water = pngs['broken-floor-water']
for (let y = 0; y < water.height; y += 1) for (let x = 911; x <= 1144; x += 1) assert.equal(alpha(water, x, y), 0, `water entered oven interval at ${x},${y}`)
let dishwasherPixels = 0, dishwasherFoam = 0
const dishwasherEdges = new Set()
for (let y = 0; y < water.height; y += 1) {
  const row = []
  for (let x = 650; x <= 910; x += 1) if (alpha(water, x, y)) {
    row.push(x)
    dishwasherPixels += 1
    const i = pixelOffset(water, x, y)
    if (water.data[i] > 220 && water.data[i + 1] > 220 && water.data[i + 2] > 220) dishwasherFoam += 1
  }
  if (row.length) dishwasherEdges.add(`${row[0]}:${row.at(-1)}`)
}
assert.ok(dishwasherPixels > 5500, 'dishwasher spill is not substantial enough')
assert.ok(dishwasherFoam > 100, 'dishwasher spill lacks fine froth')
assert.ok(dishwasherEdges.size > 15, 'dishwasher spill silhouette is too rectilinear')
const sinkEdges = new Set()
for (let y = 10; y <= 22; y += 1) {
  const row = []
  for (let x = 360; x <= 640; x += 1) if (alpha(water, x, y)) row.push(x)
  sinkEdges.add(`${row[0]}:${row.at(-1)}`)
}
assert.ok(sinkEdges.size >= 10, 'sink spill still has straight clipped sides')

for (const required of [
  "const ROOT='/keeper-review/kitchen-room-layout-v13/assets/',V='?v=13';",
  'Review-only V13',
  'V12 predecessor ↔ V13 asset corrections',
  'contacts:{standard:116,broken:116},anchors:{standard:69,broken:69}',
  'ACCEPTED_WARNING_OFFSETS=[[-5,-2],[-5,-2],[-5,-2]]',
  'scheduleWarning',
  'node.style.opacity=Math.random()<.24?0:1',
  'document.addEventListener(\'pointerup\',endDrag,{once:true})',
  "model.counter={...active.counterBefore}",
  "model.floor={...active.floorBefore}",
  'Table and chair anchors unchanged.',
  '.flat(Infinity)',
  'L1 -5,-2 · L2 -5,-2 · L3 -5,-2',
  'closed oven cavity flicker',
  'Reject V13 by discarding only its page, route and V13 native correction directory. V1–V12',
]) assert.ok(page.includes(required), `V13 page missing ${required}`)
assert.equal(page.includes('ovenFascia'), false)
assert.equal(page.includes('/keeper-review/kitchen-room-layout-v12/assets/'), false)
for (const script of [...page.matchAll(/<script>([\s\S]*?)<\/script>/g)].map(match => match[1])) new vm.Script(script)
assert.ok(route.includes('/keeper-review/kitchen-room-layout-v13/index.html'))
assert.ok(archiveRoute.includes("'kitchen-room-layout-v13'"))

const archive = json('review-archive/index.json')
const expected = [
  ['prime-keeper-neutral-native-256x320.png', register.keeperPresentation.neutral.sha256],
  ['prime-keeper-seated-back-native-256x320.png', register.keeperPresentation.seated.sha256],
  ...Object.values(register.outputs).map(output => [output.publicReviewFile.split('/').pop(), output.sha256]),
]
for (const [asset, expectedHash] of expected) {
  const pathname = `/keeper-review/kitchen-room-layout-v13/assets/${asset}`
  const entry = archive.legacyPaths[pathname]
  assert.ok(entry, `${pathname} not archived`)
  assert.equal(entry.sha256, expectedHash)
  assert.equal(fs.existsSync(`review-archive/${entry.object.replace(/^review-archive\//, '')}`), true)
  assert.equal(fs.existsSync(`public${pathname}`), false)
}

console.log('Kitchen room layout review V13 verified: complete-base bowl, drag-scope isolation, accepted clean multicolour warning lights, tapered sink spill, organic frothy dishwasher water, dry oven, and unchanged fitted base/grid/runtime/gameplay.')
