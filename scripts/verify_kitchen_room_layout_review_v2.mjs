#!/usr/bin/env node
import assert from 'node:assert/strict'
import crypto from 'node:crypto'
import fs from 'node:fs'
import { PNG } from 'pngjs'

const json = file => JSON.parse(fs.readFileSync(file, 'utf8'))
const hashBytes = bytes => crypto.createHash('sha256').update(bytes).digest('hex')
const hash = file => hashBytes(fs.readFileSync(file))
const record = json('data/kitchen_room_layout_review_v2.json')
const rejected = json('data/kitchen_room_layout_review_v1.json')
const contract = json('data/kitchen_asset_contract_v1.json')
const register = json(record.nativeCutouts.register)
const page = fs.readFileSync('public/keeper-review/kitchen-room-layout-v2/index.html', 'utf8')
const archiveRoute = fs.readFileSync('src/app/keeper-review/[set]/assets/[asset]/route.ts', 'utf8')
const reviewRoute = fs.readFileSync('src/app/keeper-review/kitchen-room-layout-v2/route.ts', 'utf8')

assert.equal(hash(record.authority.master), record.authority.masterSha256)
assert.deepEqual(register.sourceDimensions, [1536, 1024])
assert.equal(register.sourceSha256, record.authority.masterSha256)
assert.equal(register.scaleApplied, false)
assert.equal(register.resamplingApplied, false)
assert.equal(register.colourTransformApplied, false)
assert.equal(register.keeperScaleReference.sourceSha256, hash(register.keeperScaleReference.source))
assert.deepEqual(register.keeperScaleReference.sourceDimensions, [256, 320])
assert.equal(contract.visualAuthority.downscalingPermitted, false)
assert.equal(contract.visualAuthority.resamplingPermitted, false)
assert.equal(contract.locomotionPresentation.paceLogicalPixels, 10.5)
assert.equal(contract.locomotionPresentation.paceKeeperUnits, 84)
assert.equal(record.locomotion.sourcePixelsPerPace, 114)
assert.equal(record.nativePresentation.sourceBayWidthPixels / record.locomotion.sourcePixelsPerPace, 2)
assert.equal(record.locomotion.reviewStageLogicalSize[0], 193)
assert.equal(record.locomotion.reviewStageLogicalSize[1], 56)
for (const x of [...record.locomotion.counterInteractionCentresSourceX, ...record.locomotion.floorInteractionCentresSourceX]) {
  assert.equal(x % record.locomotion.sourcePixelsPerPace, 0, `interaction centre ${x} is off the Keeper pace lattice`)
}
assert.match(rejected.status, /^rejected-/)
assert.equal(rejected.rejection.replacement, record.reviewRoute)
assert.equal(record.boundary.runtimeChanged, false)
assert.equal(record.boundary.approvedArtChanged, false)
assert.equal(record.boundary.legacyRuntime84x74UsedByReview, false)

const source = PNG.sync.read(fs.readFileSync(record.authority.master))
for (const [id, output] of Object.entries(register.outputs)) {
  const bytes = fs.readFileSync(output.file)
  assert.equal(hashBytes(bytes), output.sha256, `${id} hash changed`)
  const png = PNG.sync.read(bytes)
  assert.deepEqual([png.width, png.height], output.dimensions, `${id} dimensions changed`)
  const [x, y, width, height] = output.crop
  assert.deepEqual(output.sourceCropDimensions, [width, height])
  assert.deepEqual(output.dimensions, [width + 8, height + 8])
  for (let py = 0; py < png.height; py += 1) {
    for (let px = 0; px < png.width; px += 1) {
      const i = (py * png.width + px) * 4
      if (px < 4 || py < 4 || px >= png.width - 4 || py >= png.height - 4) {
        assert.equal(png.data[i + 3], 0, `${id} lost its four-pixel transparent safety gutter`)
        continue
      }
      const sourceI = ((y + py - 4) * source.width + x + px - 4) * 4
      assert.deepEqual(
        [...png.data.slice(i, i + 3)],
        [...source.data.slice(sourceI, sourceI + 3)],
        `${id} retained RGB differs from its exact source coordinate`,
      )
    }
  }
}

for (const required of [
  'width="1536" height="1024"',
  'WORLD_SCALE=228/21',
  'ROOM_LOGICAL_W=193,ROOM_LOGICAL_H=56',
  'PACE_LOGICAL=10.5',
  'const PACE=PACE_LOGICAL*WORLD_SCALE',
  'const COUNTER_CENTRES=[342,570,798,1026,1254,1482]',
  'const FLOOR_CENTRES=[114,1710,1938]',
  'Promise.all(assetUrls.map(decodeImage))',
  'prime-keeper-neutral-native-256x320.png',
  'No downscaling or resampling',
]) assert.ok(page.includes(required), `native review page missing ${required}`)
for (const forbidden of ['/sprites/kitchen-v4/', '84x74.png', 'object-fit', 'mix-blend-mode']) {
  assert.equal(page.includes(forbidden), false, `native review page contains forbidden reduced/manipulated rendering: ${forbidden}`)
}
assert.ok(archiveRoute.includes("'kitchen-room-layout-v2'"), 'V2 assets must use the integrity-checking same-origin archive proxy')
assert.ok(reviewRoute.includes('/keeper-review/kitchen-room-layout-v2/index.html'), 'stable V2 route must resolve its immutable public shell')

const archive = json('review-archive/index.json')
const expectedArchiveAssets = ['kitchen-v4-master.png', 'prime-keeper-neutral-native-256x320.png', ...Object.values(register.outputs).map(output => output.publicReviewFile.split('/').pop())]
for (const asset of expectedArchiveAssets) {
  const pathname = `/keeper-review/kitchen-room-layout-v2/assets/${asset}`
  const entry = archive.legacyPaths[pathname]
  assert.ok(entry, `${pathname} is not content-addressed`)
  const expectedHash = asset === 'kitchen-v4-master.png'
    ? record.authority.masterSha256
    : asset === 'prime-keeper-neutral-native-256x320.png'
      ? register.keeperScaleReference.sourceSha256
      : Object.values(register.outputs).find(output => output.publicReviewFile.endsWith(`/${asset}`)).sha256
  assert.equal(entry.sha256, expectedHash, `${pathname} archive hash changed`)
  assert.equal(fs.existsSync(`review-archive/${entry.object.replace(/^review-archive\//, '')}`), true)
  assert.equal(fs.existsSync(`public${pathname}`), false, `${pathname} should have been removed after archiving`)
}

console.log('Kitchen room layout review V2 verified: native source pixels, approved Prime Keeper scale, exact pace anchors, no reduced runtime art, reversible boundary.')
