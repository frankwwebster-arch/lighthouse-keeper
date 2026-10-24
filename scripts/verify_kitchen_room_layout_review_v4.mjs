#!/usr/bin/env node
import assert from 'node:assert/strict'
import crypto from 'node:crypto'
import fs from 'node:fs'
import { PNG } from 'pngjs'

const json = file => JSON.parse(fs.readFileSync(file, 'utf8'))
const hashBytes = bytes => crypto.createHash('sha256').update(bytes).digest('hex')
const hash = file => hashBytes(fs.readFileSync(file))
const record = json('data/kitchen_room_layout_review_v4.json')
const register = json(record.nativeAssets.register)
const fittedApproval = json('docs/review/kitchen-fitted-units-lock-approval-2026-10-24.json')
const page = fs.readFileSync('public/keeper-review/kitchen-room-layout-v4/index.html', 'utf8')
const route = fs.readFileSync('src/app/keeper-review/kitchen-room-layout-v4/route.ts', 'utf8')
const archiveRoute = fs.readFileSync('src/app/keeper-review/[set]/assets/[asset]/route.ts', 'utf8')

assert.equal(hash(record.authority.master), record.authority.masterSha256)
assert.equal(hash(record.nativeAssets.register), record.nativeAssets.registerSha256)
assert.equal(hash('public/sprites/room_kitchen.png'), 'c1cb3c90b911ea09ae13d8fd09297787b990b0997dc589fb9e6a62c658099eff', 'runtime room changed')
assert.equal(hash('public/keeper-review/kitchen-room-layout-v1/index.html'), '3638a275b375ce8731aa4b924522f8f37f44f453044ab9a7c4ca68644d3c25b6', 'immutable V1 shell changed')
assert.equal(hash('public/keeper-review/kitchen-room-layout-v2/index.html'), 'e9d9d5031961365dfb28ab89ca80ded68f30c34b1a389409d637353da69fddc2', 'immutable V2 shell changed')
assert.equal(hash('public/keeper-review/kitchen-room-layout-v3/index.html'), '2fb71a7db5f0a87da27ee4f3555e03688622ab90d14a0536215e0ca081e944e8', 'immutable V3 shell changed')
assert.deepEqual(register.authority.dimensions, [1536, 1024])
assert.equal(register.scaleApplied, false)
assert.equal(register.downscalingApplied, false)
assert.equal(register.resamplingApplied, false)
assert.equal(register.colourTransformApplied, false)
assert.equal(register.keeperPresentation.cssResize, false)
assert.deepEqual(register.keeperPresentation.dimensions, [256, 320])
assert.equal(register.keeperPresentation.sourcePixelsPerPace, 114)

const pngs = {}
for (const [id, output] of Object.entries(register.outputs)) {
  const bytes = fs.readFileSync(output.file)
  assert.equal(hashBytes(bytes), output.sha256, `${id} hash changed`)
  const png = PNG.sync.read(bytes)
  pngs[id] = png
  assert.deepEqual([png.width, png.height], output.dimensions, `${id} dimensions changed`)
}
assert.deepEqual(register.outputs['fitted-units-static'].dimensions, [1368, 284])
assert.equal(register.outputs['fitted-units-static'].sha256, record.nativeAssets.fittedBaseSha256)
assert.equal(register.outputs['fitted-units-static'].sha256, fittedApproval.lockedOutput.sha256)
assert.deepEqual(register.outputs['fitted-units-static'].dimensions, fittedApproval.lockedOutput.dimensions)
assert.equal(register.fittedUnits.bodyMovementBetweenStates, false)
const master = PNG.sync.read(fs.readFileSync(record.authority.master))
const fitted = pngs['fitted-units-static']
for (let y = 0; y < fitted.height; y += 1) for (let x = 0; x < fitted.width; x += 1) {
  const repairedTap = x >= 525 && x < 605 && y >= 6 && y < 68
  const sx = x + 65, sy = repairedTap ? y + 282 : y
  const actual = (y * fitted.width + x) * 4, expected = (sy * master.width + sx) * 4
  assert.deepEqual([...fitted.data.slice(actual, actual + 4)], [...master.data.slice(expected, expected + 4)], `unexpected fitted-body edit at ${x},${y}`)
}
for (const id of ['fitted-overlay-on', 'fitted-overlay-broken', 'dishwasher-warning-1', 'dishwasher-warning-2', 'dishwasher-warning-3', 'oven-broken-cavity-light']) {
  assert.deepEqual(register.outputs[id].dimensions, [1368, 284], `${id} registration changed`)
}
assert.deepEqual(register.outputs['broken-floor-water'].dimensions, [1376, 43])
assert.match(register.outputs['broken-floor-water'].role, /separate transparent floor-plane/)

const looseIds = ['toaster-off','toaster-on','toaster-broken','kettle-off','kettle-on','kettle-broken','bowl-standard','bowl-broken','bin-standard','bin-broken','table-standard','chair-standard']
for (const id of looseIds) {
  const png = pngs[id]
  for (let x = 0; x < png.width; x += 1) for (const y of [0, 1, 2, 3, png.height - 4, png.height - 3, png.height - 2, png.height - 1]) assert.equal(png.data[(y * png.width + x) * 4 + 3], 0, `${id} lost vertical safety gutter`)
  for (let y = 0; y < png.height; y += 1) for (const x of [0, 1, 2, 3, png.width - 4, png.width - 3, png.width - 2, png.width - 1]) assert.equal(png.data[(y * png.width + x) * 4 + 3], 0, `${id} lost horizontal safety gutter`)
  assert.ok(register.outputs[id].contactRow > 3 && register.outputs[id].contactRow < png.height - 4, `${id} needs a safe physical support row`)
}

assert.equal(register.outputs['kettle-off'].sha256, register.outputs['kettle-on'].sha256, 'Kettle ON must be byte-identical to OFF')
assert.equal(register.outputs['kettle-on'].steamLayer, 'separate-not-drawn-in-this-review')
assert.deepEqual(register.globalStateMap.on, { toaster: 'on', kettle: 'on', bin: 'standard', bowl: 'standard' })
assert.equal(register.outputs['toaster-on'].base, 'toaster-off')
assert.match(register.outputs['toaster-on'].method, /toast seated into its slots/)
assert.equal(register.outputs['bowl-standard'].neighbourComponentsRemoved, true)
assert.equal(register.outputs['bowl-broken'].expandedTopLeftSafety, true)
assert.equal(register.outputs['bin-standard'].sizeFactor, 1.5)
assert.equal(register.outputs['bin-standard'].nativePixelStraightRunExtension, true)
assert.equal(register.outputs['bin-broken'].coreSizeFactor, 1.5)
assert.equal(register.outputs['chair-standard'].facing, 'rear')
assert.equal(register.outputs['chair-standard'].targetSeatHeightPixels, 62)
assert.equal(register.outputs['table-standard'].targetSurfaceHeightPixels, 116)

for (const required of [
  "const ROOT='/keeper-review/kitchen-room-layout-v4/assets/'",
  'id="runBase"', 'id="runOn"', 'id="runBroken"', 'id="floorWater"',
  "base:'fitted-units-static-native.png'",
  "seated.style.left=`${FLOOR_CENTRES[2]-128}px`;seated.style.top=`${KEEPER_FLOOR_Y-320}px`",
  "GLOBAL={off:{toaster:'off',kettle:'off',bin:'standard',bowl:'standard'},on:{toaster:'on',kettle:'on',bin:'standard',bowl:'standard'}",
  'Promise.all(assetUrls.map(decodeImage))',
  'Animation and broken-SFX slots',
]) assert.ok(page.includes(required), `V4 page missing ${required}`)
for (const forbidden of ['RUN_TOPS', '84x74.png', 'mix-blend-mode', 'width:32*WORLD_SCALE', 'height:40*WORLD_SCALE']) assert.equal(page.includes(forbidden), false, `V4 page contains forbidden rendering ${forbidden}`)
assert.ok(route.includes('/keeper-review/kitchen-room-layout-v4/index.html'))
assert.ok(archiveRoute.includes("'kitchen-room-layout-v4'"))
assert.equal(record.boundary.runtimeChanged, false)
assert.equal(record.boundary.gameplayChanged, false)
assert.equal(record.boundary.approvedMasterChanged, false)

const archive = json('review-archive/index.json')
const expected = [
  ['prime-keeper-neutral-native-256x320.png', register.keeperPresentation.neutral.sha256],
  ['prime-keeper-seated-back-native-256x320.png', register.keeperPresentation.seated.sha256],
  ...Object.values(register.outputs).map(output => [output.publicReviewFile.split('/').pop(), output.sha256]),
]
for (const [asset, expectedHash] of expected) {
  const pathname = `/keeper-review/kitchen-room-layout-v4/assets/${asset}`
  const entry = archive.legacyPaths[pathname]
  assert.ok(entry, `${pathname} is not content-addressed`)
  assert.equal(entry.sha256, expectedHash, `${pathname} archive hash changed`)
  assert.equal(fs.existsSync(`review-archive/${entry.object.replace(/^review-archive\//, '')}`), true)
  assert.equal(fs.existsSync(`public${pathname}`), false, `${pathname} should be removed after archiving`)
}

console.log('Kitchen room layout review V4 verified: locked fitted base, native loose assets, fixed global states, isolated effects and reversible boundary.')
