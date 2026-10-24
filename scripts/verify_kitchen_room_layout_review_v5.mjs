#!/usr/bin/env node
import assert from 'node:assert/strict'
import crypto from 'node:crypto'
import fs from 'node:fs'
import { PNG } from 'pngjs'

const json = file => JSON.parse(fs.readFileSync(file, 'utf8'))
const hashBytes = bytes => crypto.createHash('sha256').update(bytes).digest('hex')
const hash = file => hashBytes(fs.readFileSync(file))
const record = json('data/kitchen_room_layout_review_v5.json')
const register = json(record.nativeAssets.register)
const v4 = json('art/drafts/kitchen-room-layout-review-2026-10-24-v4/native-assets/extraction-register.json')
const page = fs.readFileSync('public/keeper-review/kitchen-room-layout-v5/index.html', 'utf8')
const route = fs.readFileSync('src/app/keeper-review/kitchen-room-layout-v5/route.ts', 'utf8')
const archiveRoute = fs.readFileSync('src/app/keeper-review/[set]/assets/[asset]/route.ts', 'utf8')

assert.equal(hash(record.nativeAssets.register), record.nativeAssets.registerSha256)
assert.equal(hash(register.sources.loose.file), register.sources.loose.sha256)
assert.equal(hash(register.sources.furniture.file), register.sources.furniture.sha256)
assert.equal(hash(register.sources.loose.file), record.nativeAssets.looseSourceSha256)
assert.equal(hash(register.sources.furniture.file), record.nativeAssets.furnitureSourceSha256)
assert.equal(hash('public/sprites/room_kitchen.png'), 'c1cb3c90b911ea09ae13d8fd09297787b990b0997dc589fb9e6a62c658099eff', '84 x 74 runtime room changed')
for (const [version, expected] of Object.entries({
  v1: '3638a275b375ce8731aa4b924522f8f37f44f453044ab9a7c4ca68644d3c25b6',
  v2: 'e9d9d5031961365dfb28ab89ca80ded68f30c34b1a389409d637353da69fddc2',
  v3: '2fb71a7db5f0a87da27ee4f3555e03688622ab90d14a0536215e0ca081e944e8',
  v4: '09041a86287b8d34cf4a1938a0c5a571f9540e318a22c2bd68540e35b42399a5',
})) assert.equal(hash(`public/keeper-review/kitchen-room-layout-${version}/index.html`), expected, `immutable ${version.toUpperCase()} shell changed`)

assert.equal(register.schema, 'lighthouse-keeper/kitchen-native-assets@5')
assert.equal(register.scaleApplied, false)
assert.equal(register.downscalingApplied, false)
assert.equal(register.resamplingApplied, false)
assert.equal(register.colourTransformApplied, false)
assert.equal(record.nativeAssets.scaleAppliedToKitchenArt, false)
assert.equal(record.boundary.runtimeChanged, false)
assert.equal(record.boundary.gameplayChanged, false)
assert.equal(record.boundary.approvedFittedUnitsChanged, false)
assert.equal(register.placement.counterSupportLocalY, 84)
assert.equal(register.placement.previousCounterSupportLocalY, 71)
assert.equal(register.placement.counterSupportLocalY - register.placement.previousCounterSupportLocalY, 13)
assert.ok(Math.abs(register.worldDensity.keeperDisplayScale - 228 / 168) < 1e-12)
assert.deepEqual(register.keeperPresentation.sourceDimensions, [256, 320])
assert.deepEqual(register.keeperPresentation.displayDimensions, [347.428571, 434.285714])
assert.ok(register.worldDensity.cabinetWorktopHeightPixels / register.keeperPresentation.displayDimensions[1] > 0.48)
assert.ok(register.worldDensity.cabinetWorktopHeightPixels / register.keeperPresentation.displayDimensions[1] < 0.50)

const pngs = {}
for (const [id, output] of Object.entries(register.outputs)) {
  const bytes = fs.readFileSync(output.file)
  assert.equal(hashBytes(bytes), output.sha256, `${id} hash changed`)
  const png = PNG.sync.read(bytes)
  pngs[id] = png
  assert.deepEqual([png.width, png.height], output.dimensions, `${id} dimensions changed`)
}
for (const id of ['fitted-units-static','fitted-overlay-on','fitted-overlay-broken','dishwasher-warning-1','dishwasher-warning-2','dishwasher-warning-3','oven-broken-cavity-light','broken-floor-water']) {
  assert.equal(register.outputs[id].sha256, v4.outputs[id].sha256, `${id} differs from locked V4`)
  assert.equal(register.outputs[id].inheritedByteIdenticalFromV4, true)
}
assert.equal(register.outputs['fitted-units-static'].sha256, 'ba84022371aea330e2fe50e5ad8fb37bf9d210aa1e09649d7f2fc69f460f49b1')

const looseIds = ['toaster-off','toaster-on','toaster-broken','kettle-off','kettle-on','kettle-broken','bin-standard','bin-broken','bowl-standard','bowl-broken','table-standard','chair-standard']
function opaqueComponents(png) {
  const seen = new Uint8Array(png.width * png.height)
  const sizes = []
  for (let y = 0; y < png.height; y += 1) for (let x = 0; x < png.width; x += 1) {
    const start = y * png.width + x
    if (seen[start] || png.data[start * 4 + 3] < 40) continue
    const queue = [start]
    seen[start] = 1
    let size = 0
    while (queue.length) {
      const at = queue.pop(), ax = at % png.width, ay = Math.floor(at / png.width)
      size += 1
      for (const [nx, ny] of [[ax - 1, ay], [ax + 1, ay], [ax, ay - 1], [ax, ay + 1]]) {
        if (nx < 0 || ny < 0 || nx >= png.width || ny >= png.height) continue
        const next = ny * png.width + nx
        if (!seen[next] && png.data[next * 4 + 3] >= 40) { seen[next] = 1; queue.push(next) }
      }
    }
    sizes.push(size)
  }
  return sizes.sort((a, b) => b - a)
}
function bottomProfileVariation(png) {
  const bottoms = []
  for (let x = 8; x < png.width - 8; x += 1) {
    let bottom = -1
    for (let y = 8; y < png.height - 8; y += 1) if (png.data[(y * png.width + x) * 4 + 3] >= 40) bottom = y
    if (bottom >= 0) bottoms.push(bottom)
  }
  return new Set(bottoms).size
}
for (const id of looseIds) {
  const png = pngs[id]
  for (let inset = 0; inset < 8; inset += 1) {
    for (let x = 0; x < png.width; x += 1) {
      assert.equal(png.data[(inset * png.width + x) * 4 + 3], 0, `${id} lost top safety gutter`)
      assert.equal(png.data[((png.height - 1 - inset) * png.width + x) * 4 + 3], 0, `${id} lost bottom safety gutter`)
    }
    for (let y = 0; y < png.height; y += 1) {
      assert.equal(png.data[(y * png.width + inset) * 4 + 3], 0, `${id} lost left safety gutter`)
      assert.equal(png.data[(y * png.width + png.width - 1 - inset) * 4 + 3], 0, `${id} lost right safety gutter`)
    }
  }
  assert.equal(register.outputs[id].downscalingApplied, false)
  assert.ok(register.outputs[id].contactRow >= 8 && register.outputs[id].contactRow < png.height - 8)
  assert.ok(opaqueComponents(png).slice(1).every(size => size <= 64), `${id} contains a detached crop artefact larger than an authored crumb`)
  assert.ok(bottomProfileVariation(png) >= 4, `${id} has a suspicious flat clipped contact edge`)
}
assert.equal(register.outputs['kettle-off'].sha256, register.outputs['kettle-on'].sha256)
assert.equal(register.outputs['kettle-on'].steamLayer, 'separate-not-drawn')
assert.equal(opaqueComponents(pngs['toaster-on']).length, 1, 'ON toaster toast/body must form one connected silhouette')
assert.ok(register.outputs['bowl-broken'].dimensions[0] > register.outputs['bowl-standard'].dimensions[0], 'broken bowl needs detached pieces')
assert.equal(register.outputs['chair-standard'].facing, 'rear')
assert.equal(register.outputs['table-standard'].physicalModelMm.height, 750)
assert.equal(register.outputs['chair-standard'].physicalModelMm.seatHeight, 460)
assert.deepEqual(register.globalStateMap.on, { toaster: 'on', kettle: 'on', bin: 'standard', bowl: 'standard' })

for (const required of [
  "const ROOT='/keeper-review/kitchen-room-layout-v5/assets/'",
  'WORKTOP_Y=RUN_TOP+84',
  'KEEPER_WORLD_SCALE=228/168',
  'width:347.428571px;height:434.285714px',
  "on:{toaster:'on',kettle:'on',bin:'standard',bowl:'standard'}",
  'Promise.all(assetUrls.map(decodeImage))',
  'V4’s loose family is rejected evidence',
]) assert.ok(page.includes(required), `V5 page missing ${required}`)
for (const forbidden of ['RUN_TOP+71', '84x74.png', 'mix-blend-mode', 'width:256px;height:320px']) assert.equal(page.includes(forbidden), false, `V5 page contains forbidden rendering ${forbidden}`)
assert.ok(route.includes('/keeper-review/kitchen-room-layout-v5/index.html'))
assert.ok(archiveRoute.includes("'kitchen-room-layout-v5'"))

const archive = json('review-archive/index.json')
const expected = [
  ['prime-keeper-neutral-native-256x320.png', register.keeperPresentation.neutral.sha256],
  ['prime-keeper-seated-back-native-256x320.png', register.keeperPresentation.seated.sha256],
  ...Object.values(register.outputs).map(output => [output.publicReviewFile.split('/').pop(), output.sha256]),
]
for (const [asset, expectedHash] of expected) {
  const pathname = `/keeper-review/kitchen-room-layout-v5/assets/${asset}`
  const entry = archive.legacyPaths[pathname]
  assert.ok(entry, `${pathname} is not content-addressed`)
  assert.equal(entry.sha256, expectedHash, `${pathname} archive hash changed`)
  assert.equal(fs.existsSync(`review-archive/${entry.object.replace(/^review-archive\//, '')}`), true)
  assert.equal(fs.existsSync(`public${pathname}`), false, `${pathname} should be removed after archiving`)
}

console.log('Kitchen room layout review V5 verified: locked fitted base, native loose redraw, forward worktop placement, connected states and shared world scale.')
