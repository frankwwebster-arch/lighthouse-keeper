#!/usr/bin/env node
import assert from 'node:assert/strict'
import crypto from 'node:crypto'
import fs from 'node:fs'

const json = file => JSON.parse(fs.readFileSync(file, 'utf8'))
const hash = file => crypto.createHash('sha256').update(fs.readFileSync(file)).digest('hex')
const record = json('data/kitchen_room_layout_review_v1.json')
const grid = json('data/kitchen_room_grid_contract_v2.json')
const authority = json('data/kitchen_asset_contract_v1.json')
const page = fs.readFileSync('public/keeper-review/kitchen-room-layout-v1/index.html', 'utf8')
const archiveRoute = fs.readFileSync('src/app/keeper-review/[set]/assets/[asset]/route.ts', 'utf8')
const reviewRoute = fs.readFileSync('src/app/keeper-review/kitchen-room-layout-v1/route.ts', 'utf8')

assert.deepEqual(record.room.logicalSize, [772, 224])
assert.deepEqual(record.room.fittedBodySize, [84, 74])
assert.deepEqual(record.room.fittedBayOriginsX, grid.fittedGrid.slotOriginsX)
assert.deepEqual(record.room.fittedBayCentresX, grid.fittedGrid.slotCentresX)
assert.equal(record.room.worktopSupportY, grid.fittedGrid.worktopSupportY)
assert.equal(record.room.floorSupportY, grid.floorSlots.supportY)
assert.deepEqual(record.defaultLayout.counterOwners, grid.countertopObjectOwnership.defaultOwners)
assert.deepEqual(record.defaultLayout.floorAssignments, grid.floorSlots.defaultAssignments)
assert.deepEqual(Object.keys(record.sourceSheetCrops).sort(), Object.keys(authority.looseObjects).sort())
assert.equal(hash(record.authority.master), record.authority.masterSha256)
assert.equal(record.boundary.runtimeChanged, false)
assert.equal(record.boundary.approvedArtChanged, false)
assert.match(record.status, /^rejected-/)
assert.equal(record.rejection.replacement, '/keeper-review/kitchen-room-layout-v2/')
assert.ok(archiveRoute.includes("'kitchen-room-layout-v1'"), 'review master must use the integrity-checking same-origin archive proxy')
assert.ok(reviewRoute.includes("/keeper-review/kitchen-room-layout-v1/index.html"), 'stable review route must resolve the immutable public shell')

for (const required of [
  'width:772px', 'height:224px', 'BODY_Y=134', 'BODY_W=84', 'BODY_H=74',
  'const BAY_ORIGINS=[84,168,252,336,420,504]',
  'const BAY_CENTRES=[126,210,294,378,462,546]',
  'const FLOOR_CENTRES=[42,646,730]',
  'Promise.all(uniqueUrls.map(decodeImage))',
  "document.querySelectorAll('button,select,input').forEach(control=>control.disabled=false)",
  'Broken appliances are movement-locked',
  '/keeper-review/kitchen-room-layout-v1/assets/kitchen-v4-master.png',
  '/sprites/kitchen-v4/',
]) assert.ok(page.includes(required), `review page missing ${required}`)

const archive = json('review-archive/index.json')
const legacyPath = '/keeper-review/kitchen-room-layout-v1/assets/kitchen-v4-master.png'
const entry = archive.legacyPaths[legacyPath]
assert.ok(entry, 'approved master review copy is not content-addressed')
assert.equal(entry.sha256, record.authority.masterSha256)
assert.equal(fs.existsSync(`review-archive/${entry.object.replace(/^review-archive\//, '')}`), true)
assert.equal(fs.existsSync(`public${legacyPath}`), false)

const legacy = 'public/sprites/room_kitchen.png'
assert.equal(hash(legacy), 'c1cb3c90b911ea09ae13d8fd09297787b990b0997dc589fb9e6a62c658099eff')
console.log('Kitchen room layout review V1 historical mechanics verified; rejection status and V2 replacement are pinned.')
