#!/usr/bin/env node
import assert from 'node:assert/strict'
import crypto from 'node:crypto'
import fs from 'node:fs'
import { PNG } from 'pngjs'

const json = file => JSON.parse(fs.readFileSync(file, 'utf8'))
const hashBytes = bytes => crypto.createHash('sha256').update(bytes).digest('hex')
const hash = file => hashBytes(fs.readFileSync(file))
const record = json('data/kitchen_room_layout_review_v3.json')
const register = json(record.nativeAssets.register)
const page = fs.readFileSync('public/keeper-review/kitchen-room-layout-v3/index.html', 'utf8')
const route = fs.readFileSync('src/app/keeper-review/kitchen-room-layout-v3/route.ts', 'utf8')
const archiveRoute = fs.readFileSync('src/app/keeper-review/[set]/assets/[asset]/route.ts', 'utf8')
const dimensions = json('data/keeper_object_dimensions.json').furniture.kitchenTableForOneV21
const rearSeat = json('art/drafts/keeper-prime-sit-stand-back-2026-10-18-v2/keeper-prime-sit-stand-back-v2.json').room.chair

assert.equal(hash(record.authority.master), record.authority.masterSha256)
assert.equal(hash('public/sprites/room_kitchen.png'), 'c1cb3c90b911ea09ae13d8fd09297787b990b0997dc589fb9e6a62c658099eff', 'runtime room changed')
assert.equal(hash('public/keeper-review/kitchen-room-layout-v2/index.html'), 'e9d9d5031961365dfb28ab89ca80ded68f30c34b1a389409d637353da69fddc2', 'immutable V2 shell changed')
assert.equal(hash('art/drafts/kitchen-room-layout-review-2026-10-24-v2/native-cutouts/extraction-register.json'), 'eea5815b87b365640589f525d3123b8bc1c152c8f64b5bc4814d6d8ca21cd75d', 'immutable V2 register changed')
assert.equal(register.sourceSha256, record.authority.masterSha256)
assert.deepEqual(register.sourceDimensions, [1536, 1024])
assert.equal(register.scaleApplied, false)
assert.equal(register.resamplingApplied, false)
assert.equal(register.colourTransformApplied, false)
for (const source of Object.values(register.correctionSources)) assert.equal(hash(source.file), source.sha256, `${source.file} correction source changed`)
assert.equal(hash(register.keeperScaleReference.source), register.keeperScaleReference.sha256)
assert.equal(hash(register.seatedFitReference.source), register.seatedFitReference.sha256)

assert.equal(record.locomotion.sourcePixelsPerPace, 114)
assert.equal(record.nativePresentation.sourceBayWidthPixels / record.locomotion.sourcePixelsPerPace, 2)
for (const x of [...record.locomotion.counterInteractionCentresSourceX, ...record.locomotion.floorInteractionCentresSourceX]) assert.equal(x % 114, 0, `${x} is off the exact pace lattice`)
assert.equal(register.fittedRunCrop.includesTapCrown, true)
assert.deepEqual(register.fittedRunCrop.sourceYByState, { off: 0, on: 282, broken: 570 })
assert.equal(register.fittedRunCrop.height, 284)

const pngs = {}
for (const [id, output] of Object.entries(register.outputs)) {
  const bytes = fs.readFileSync(output.file)
  assert.equal(hashBytes(bytes), output.sha256, `${id} hash changed`)
  const png = PNG.sync.read(bytes)
  pngs[id] = png
  assert.deepEqual([png.width, png.height], output.dimensions, `${id} dimensions changed`)
  for (let x = 0; x < png.width; x += 1) for (const y of [0, 1, 2, 3, png.height - 4, png.height - 3, png.height - 2, png.height - 1]) assert.equal(png.data[(y * png.width + x) * 4 + 3], 0, `${id} lost vertical safety gutter`)
  for (let y = 0; y < png.height; y += 1) for (const x of [0, 1, 2, 3, png.width - 4, png.width - 3, png.width - 2, png.width - 1]) assert.equal(png.data[(y * png.width + x) * 4 + 3], 0, `${id} lost horizontal safety gutter`)
  assert.ok(output.contactRow > 0 && output.contactRow < png.height, `${id} needs a physical support row`)
}

function assertEmbedded(baseId, compositeId, dx, dy) {
  const base = pngs[baseId], composite = pngs[compositeId]
  for (let y = 0; y < base.height; y += 1) for (let x = 0; x < base.width; x += 1) {
    const bi = (y * base.width + x) * 4, ci = ((y + dy) * composite.width + x + dx) * 4
    if (base.data[bi + 3] === 0) continue
    assert.deepEqual([...composite.data.slice(ci, ci + 4)], [...base.data.slice(bi, bi + 4)], `${compositeId} altered ${baseId} body at ${x},${y}`)
  }
}
assertEmbedded('toaster-off', 'toaster-on', 0, 48)
assertEmbedded('kettle-off', 'kettle-on', 0, 180)
assert.equal(register.outputs['toaster-on'].method.includes('neighbouring broken sprite pixels'), true)
assert.equal(register.outputs['kettle-broken'].replacesV2State, 'on')
assert.deepEqual(register.outputs['kettle-broken'].excludedV2Crop, [620, 872, 120, 137])
assert.equal(register.outputs['kettle-broken'].sha256, json('art/drafts/kitchen-room-layout-review-2026-10-24-v2/native-cutouts/extraction-register.json').outputs['kettle-on'].sha256, 'former kettle ON was not preserved exactly as BROKEN')
assert.equal(Object.keys(register.outputs).some(id => id === 'kettle-loose-lid' || id === 'kettle-broken-old'), false)

assert.deepEqual(register.outputs['table-standard'].logicalDimensions, [dimensions.width, dimensions.surfaceHeight])
assert.equal(register.outputs['table-standard'].physicalDimensions[0], 217)
assert.equal(register.outputs['table-standard'].physicalDimensions[1], 157)
assert.deepEqual(register.outputs['chair-standard'].logicalDimensions, [rearSeat.widthLp, rearSeat.backrestTopWorldYLp ? 21 : -1])
assert.equal(register.outputs['chair-standard'].seatTopLogicalPixels, rearSeat.seatHeightAboveFloorLp)
assert.equal(register.outputs['chair-standard'].backrestWidthLogicalPixels, rearSeat.backrestWidthLp)
assert.equal(register.outputs['chair-standard'].facing, 'rear')
assert.deepEqual(register.outputs['chair-standard'].physicalDimensions, [261, 228])

for (const required of [
  'Review-only V3 correction', 'No downscaling or resampling', 'const RUN_TOPS={off:0,on:-282,broken:-570}',
  'contacts:{off:80,on:128,broken:123}', 'Rear-seat fit proof', 'Promise.all(assetUrls.map(decodeImage))',
  'prime-keeper-seated-back-native.png', '114 source px = one Prime Keeper pace',
]) assert.ok(page.includes(required), `V3 page missing ${required}`)
for (const forbidden of ['/sprites/kitchen-v4/', '84x74.png', 'mix-blend-mode', 'kettle-broken-native.png?v=2']) assert.equal(page.includes(forbidden), false, `V3 page contains forbidden rendering ${forbidden}`)
assert.ok(route.includes('/keeper-review/kitchen-room-layout-v3/index.html'))
assert.ok(archiveRoute.includes("'kitchen-room-layout-v3'"))
assert.equal(record.boundary.runtimeChanged, false)
assert.equal(record.boundary.approvedArtChanged, false)
assert.equal(record.boundary.legacyRuntime84x74UsedByReview, false)

const archive = json('review-archive/index.json')
const expected = [
  ['kitchen-v4-master.png', record.authority.masterSha256],
  ['prime-keeper-neutral-native-256x320.png', register.keeperScaleReference.sha256],
  ['prime-keeper-seated-back-native.png', register.seatedFitReference.sha256],
  ...Object.values(register.outputs).map(output => [output.publicReviewFile.split('/').pop(), output.sha256]),
]
for (const [asset, expectedHash] of expected) {
  const pathname = `/keeper-review/kitchen-room-layout-v3/assets/${asset}`
  const entry = archive.legacyPaths[pathname]
  assert.ok(entry, `${pathname} is not content-addressed`)
  assert.equal(entry.sha256, expectedHash, `${pathname} archive hash changed`)
  assert.equal(fs.existsSync(`review-archive/${entry.object.replace(/^review-archive\//, '')}`), true)
  assert.equal(fs.existsSync(`public${pathname}`), false, `${pathname} should be removed after archiving`)
}

console.log('Kitchen room layout review V3 verified: corrected native states, tap crop, support contacts, rear-seat furniture fit, exact pace anchors and reversible boundary.')
