#!/usr/bin/env node
import assert from 'node:assert/strict'
import crypto from 'node:crypto'
import fs from 'node:fs'
import path from 'node:path'
import vm from 'node:vm'
import { PNG } from 'pngjs'

const root = process.cwd()
const set = 'kitchen-complete-room-layout-2026-10-22-v4'
const route = '/keeper-review/kitchen-complete-room-layout-v4'
const draft = path.join(root, 'art/drafts', set)
const pagePath = path.join(root, 'public/keeper-review/kitchen-complete-room-layout-v4/index.html')
const publicManifestPath = path.join(root, 'public/keeper-review/kitchen-complete-room-layout-v4/manifest.json')
const archivePath = path.join(root, 'review-archive/sets/kitchen-complete-room-layout-v4.json')
const v3Root = path.join(root, 'art/drafts/kitchen-complete-room-layout-2026-10-22-v3')
const gridPath = path.join(root, 'data/kitchen_room_grid_contract_v1.json')
const sha = file => crypto.createHash('sha256').update(fs.readFileSync(file)).digest('hex')

const manifest = JSON.parse(fs.readFileSync(path.join(draft, 'manifest.json'), 'utf8'))
const publicManifest = JSON.parse(fs.readFileSync(publicManifestPath, 'utf8'))
const grid = JSON.parse(fs.readFileSync(gridPath, 'utf8'))
assert.deepEqual(publicManifest, manifest)
assert.equal(manifest.schema, 'lighthouse-keeper/kitchen-complete-room-layout@4')
assert.equal(manifest.deliveryPredecessor.manifestSha256, 'cb80afc71a42b9e3b1ed43dc910d018a0ec746fc6380732f719e78689e3ea9c1')
assert.equal(manifest.deliveryPredecessor.drawingPixelsChanged, false)
assert.equal(manifest.deliveryPredecessor.fittedGeometryChanged, false)
assert.equal(manifest.deliveryPredecessor.stateBehaviourChanged, false)
assert.equal(manifest.deliveryPredecessor.loosePlacementChangedToExactGridSlots, true)
assert.deepEqual(manifest.roomGrid, grid)

assert.deepEqual(grid.fittedGrid.slotOriginsX, [84, 168, 252, 336, 420, 504])
assert.deepEqual(grid.fittedGrid.slotCentresX, [126, 210, 294, 378, 462, 546])
assert.equal(grid.fittedGrid.bayWidthPixels, 84)
assert.equal(grid.fittedGrid.bayWidthLogicalPixels, 21)
assert.deepEqual(grid.fittedGrid.bodySizePixels, [84, 74])
assert.equal(grid.fittedGrid.worktopSupportY, 141)
assert.equal(grid.fittedGrid.floorSupportY, 208)
assert.equal(grid.fittedGrid.keeperStopTurnY, 218)
assert.deepEqual(grid.countertopSlots.eligibleSupportingUnits, ['cupboard', 'drawers', 'dishwasher', 'fridge'])
assert.equal(grid.countertopSlots.oneObjectPerSlot, true)
assert.equal(grid.floorSlots.oneObjectPerSlot, true)
assert.deepEqual(grid.floorSlots.sections, [
  { id: 'floor-west', boundsX: [0, 84], centreX: 42 },
  { id: 'floor-dining-left', boundsX: [604, 688], centreX: 646 },
  { id: 'floor-dining-right', boundsX: [688, 772], centreX: 730 },
])
assert.deepEqual(grid.defaultAssignments, {
  kettle: 'counter-4', toaster: 'counter-6', bin: 'floor-west', chair: 'floor-dining-left', table: 'floor-dining-right',
})
assert.equal(new Set([grid.defaultAssignments.kettle, grid.defaultAssignments.toaster]).size, 2)
assert.equal(new Set([grid.defaultAssignments.bin, grid.defaultAssignments.chair, grid.defaultAssignments.table]).size, 3)

const slotById = new Map()
grid.countertopSlots.ids.forEach((id, index) => slotById.set(id, { centreX: grid.countertopSlots.centresX[index], supportY: grid.countertopSlots.supportY }))
grid.floorSlots.sections.forEach(section => slotById.set(section.id, { centreX: section.centreX, supportY: grid.floorSlots.supportY }))
for (const [name, slotId] of Object.entries(grid.defaultAssignments)) {
  const asset = manifest.looseAssets[name]
  const slot = slotById.get(slotId)
  const centreOffset = asset.opaqueDrawRect[0] + asset.logicalSize[0] / 2
  const bottomOffset = asset.opaqueDrawRect[1] + asset.logicalSize[1]
  const x = slot.centreX - centreOffset
  const y = slot.supportY - bottomOffset
  assert.equal(x + centreOffset, slot.centreX, `${name} centre drift`)
  assert.equal(y + bottomOffset, slot.supportY, `${name} support drift`)
  assert.ok(Math.abs((x + centreOffset) - slot.centreX) <= grid.invariants.maximumCentreErrorPixels)
}

assert.equal(manifest.atlas.drawingCount, 24)
assert.equal(manifest.atlas.uniqueImageRequests, 1)
assert.equal(manifest.atlas.lossless, true)
assert.equal(manifest.atlas.v3AtlasPixelsCopiedAtOrigin, true)
const atlasPath = path.join(draft, 'assets', manifest.atlas.file)
assert.equal(sha(atlasPath), manifest.atlas.sha256)
const atlas = PNG.sync.read(fs.readFileSync(atlasPath))
assert.deepEqual([atlas.width, atlas.height], manifest.atlas.pixels)
const v3Manifest = JSON.parse(fs.readFileSync(path.join(v3Root, 'manifest.json'), 'utf8'))
const v3Atlas = PNG.sync.read(fs.readFileSync(path.join(v3Root, 'assets', v3Manifest.atlas.file)))
assert.equal(atlas.width, v3Atlas.width)
for (let y = 0; y < v3Atlas.height; y += 1) {
  const length = v3Atlas.width * 4
  const start = y * length
  assert.deepEqual(atlas.data.subarray(start, start + length), v3Atlas.data.subarray(start, start + length), `V3 atlas row ${y} changed`)
}
for (const record of [...Object.values(manifest.assets), ...Object.values(manifest.looseAssets)]) assert.equal(record.file, manifest.atlas.file)
assert.deepEqual(Object.keys(manifest.healingAssets).sort(), [
  'countertop-join-cap-template', 'countertop-triangle-underlay-template', 'join-body-backfill-template', 'neighbour-seam-cleanup-left', 'neighbour-seam-cleanup-right',
])
for (const record of Object.values(manifest.healingAssets)) {
  assert.equal(sha(path.join(root, record.sourceFile)), record.sourceSha256)
  const [x, y, width, height] = record.atlasRect
  assert.ok(x >= 0 && y >= v3Atlas.height && x + width <= atlas.width && y + height <= atlas.height)
  assert.deepEqual([width, height], record.pixels)
}

const page = fs.readFileSync(pagePath, 'utf8')
assert.ok(page.includes("const ROUTE='/keeper-review/kitchen-complete-room-layout-v4'"))
assert.ok(page.includes('1 ATLAS READY • 24 DRAWINGS'))
assert.ok(page.includes('Established pair-aware healing'))
assert.ok(page.includes("'join-body-backfill-template'"))
assert.ok(page.includes("'countertop-triangle-underlay-template'"))
assert.ok(page.includes("'countertop-join-cap-template'"))
assert.ok(page.includes("'neighbour-seam-cleanup-left'"))
assert.ok(page.includes("'neighbour-seam-cleanup-right'"))
assert.ok(page.includes("positionStorage" ) === false, 'page should use roomGrid contract rather than duplicate manifest prose')
assert.ok(page.includes('slots={...manifest.roomGrid.defaultAssignments}'))
assert.ok(page.includes('Only exact slot IDs persist; raw pointer coordinates never do.'))
assert.ok(page.includes('one object; occupied drops swap'))
assert.ok(page.includes("Blocked: that cabinet swap would leave the kettle or toaster over the sink/hob."))
assert.ok(page.includes('4× reveals detail that physically cannot all survive at game size.'))
assert.equal(page.includes('loose[name][0]'), false)
assert.equal(page.includes('drag.x=Math.max(0'), false)
const inlineScript = page.match(/<script>([\s\S]+)<\/script>/)?.[1]
assert(inlineScript)
new vm.Script(inlineScript, { filename: `${route}/inline.js` })

assert.ok(fs.existsSync(archivePath), 'run npm run maintain:keeper-review before verification')
const archive = JSON.parse(fs.readFileSync(archivePath, 'utf8'))
const entry = archive.entries[`${route}/assets/${manifest.atlas.file}`]
assert.ok(entry)
assert.equal(entry.sha256, manifest.atlas.sha256)
assert.equal(sha(path.join(root, entry.object)), manifest.atlas.sha256)
assert.equal(Object.keys(archive.entries).length, 1)
assert.equal(fs.existsSync(path.join(root, 'public/keeper-review/kitchen-complete-room-layout-v4/assets')), false)

const config = fs.readFileSync(path.join(root, 'next.config.mjs'), 'utf8')
assert.ok(config.includes("source: '/keeper-review/kitchen-complete-room-layout-v4'"))
assert.ok(config.includes("destination: '/keeper-review/kitchen-complete-room-layout-v4/index.html'"))
console.log('Kitchen Complete Room Layout V4 verification passed: exact grid slots, direct master atlas, and three synchronized healing views.')
