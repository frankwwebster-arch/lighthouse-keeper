#!/usr/bin/env node
import assert from 'node:assert/strict'
import crypto from 'node:crypto'
import fs from 'node:fs'
import path from 'node:path'
import vm from 'node:vm'
import { PNG } from 'pngjs'

const root = process.cwd()
const set = 'kitchen-countertop-interface-2026-10-22-v5'
const route = '/keeper-review/kitchen-complete-room-layout-v5'
const draft = path.join(root, 'art/drafts', set)
const v4Root = path.join(root, 'art/drafts/kitchen-complete-room-layout-2026-10-22-v4')
const publicRoot = path.join(root, 'public/keeper-review/kitchen-complete-room-layout-v5')
const archivePath = path.join(root, 'review-archive/sets/kitchen-complete-room-layout-v5.json')
const sha = file => crypto.createHash('sha256').update(fs.readFileSync(file)).digest('hex')

const manifest = JSON.parse(fs.readFileSync(path.join(draft, 'manifest.json'), 'utf8'))
const publicManifest = JSON.parse(fs.readFileSync(path.join(publicRoot, 'manifest.json'), 'utf8'))
const grid = JSON.parse(fs.readFileSync(path.join(root, 'data/kitchen_room_grid_contract_v2.json'), 'utf8'))
const v4 = JSON.parse(fs.readFileSync(path.join(v4Root, 'manifest.json'), 'utf8'))
assert.deepEqual(publicManifest, manifest)
assert.equal(manifest.schema, 'lighthouse-keeper/kitchen-complete-room-layout@5')
assert.equal(manifest.status, 'unapproved-countertop-interface-and-cabinet-owned-objects')
assert.equal(manifest.deliveryPredecessor.manifestSha256, '6340d9cddddabd430872af08dd2b6672b38f08cd2cedad4256016512f164c4f6')
assert.equal(sha(path.join(v4Root, 'manifest.json')), manifest.deliveryPredecessor.manifestSha256)
assert.equal(manifest.deliveryPredecessor.v4Changed, false)
assert.equal(manifest.approvedAuthoritiesPreserved.changed, false)
assert.equal(manifest.boundaries.productionChanged, false)
assert.equal(manifest.boundaries.runtimeChanged, false)
assert.equal(manifest.boundaries.approvedSourceOverwritten, false)
assert.deepEqual(manifest.roomGrid, grid)

for (const source of [
  manifest.candidateSources.foundation,
  manifest.candidateSources.states,
  ...manifest.candidateSources.rejectedHobColourAttempts,
  ...manifest.candidateSources.supersededBeforeStraightSinkDatum,
]) assert.equal(sha(path.join(root, source.path)), source.sha256, `${source.path} changed`)

assert.deepEqual(grid.fittedGrid.slotOriginsX, [84, 168, 252, 336, 420, 504])
assert.deepEqual(grid.fittedGrid.slotCentresX, [126, 210, 294, 378, 462, 546])
assert.equal(grid.fittedGrid.bayWidthPixels, 84)
assert.equal(grid.fittedGrid.bayWidthLogicalPixels, 21)
assert.deepEqual(grid.fittedGrid.bodySizePixels, [84, 74])
assert.equal(grid.fittedGrid.worktopSupportY, 141)
assert.equal(grid.fittedGrid.floorSupportY, 208)
assert.equal(grid.fittedGrid.keeperStopTurnY, 218)
assert.deepEqual(grid.countertopObjectOwnership.eligibleOwnerTypes, ['cupboard', 'drawers'])
assert.deepEqual(grid.countertopObjectOwnership.objects, ['kettle', 'toaster'])
assert.deepEqual(grid.countertopObjectOwnership.defaultOwners, { kettle: 'cupboard', toaster: 'drawers' })
assert.equal(grid.countertopObjectOwnership.oneObjectPerOwner, true)
assert.equal(grid.countertopObjectOwnership.ownerMovesObject, true)
assert.equal(grid.countertopObjectOwnership.rawCoordinatesPersisted, false)
assert.equal(grid.countertopObjectOwnership.dropOnOccupiedOwner, 'swap-object-owners')
assert.equal(new Set(Object.values(grid.countertopObjectOwnership.defaultOwners)).size, 2)
assert.deepEqual(grid.floorSlots.defaultAssignments, { bin: 'floor-west', chair: 'floor-dining-left', table: 'floor-dining-right' })
assert.equal(new Set(Object.values(grid.floorSlots.defaultAssignments)).size, 3)

assert.equal(manifest.countertopInterface.legacyV22V32HealingUsed, false)
assert.equal(manifest.countertopInterface.allBodyRectsExact, true)
assert.deepEqual(manifest.countertopInterface.bodyMasterPixels, [420, 370])
assert.deepEqual(Object.keys(manifest.assets).sort(), Object.keys(v4.assets).sort())
assert.deepEqual(Object.keys(manifest.canonicalAssets).sort(), Object.keys(v4.assets).sort())
for (const [name, record] of Object.entries(manifest.assets)) {
  assert.deepEqual(record.bodyRect.slice(2), [420, 370], `${name} does not map to an exact 84×74 body`)
  assert.deepEqual(record.logicalBody, [84, 74])
  assert.equal(record.file, manifest.atlas.file)
}

const atlasPath = path.join(draft, 'assets', manifest.atlas.file)
assert.equal(manifest.atlas.drawingCount, 36)
assert.equal(manifest.atlas.uniqueImageRequests, 1)
assert.equal(manifest.atlas.lossless, true)
assert.equal(sha(atlasPath), manifest.atlas.sha256)
const atlas = PNG.sync.read(fs.readFileSync(atlasPath))
assert.deepEqual([atlas.width, atlas.height], manifest.atlas.pixels)
for (const record of [
  ...Object.values(manifest.canonicalAssets),
  ...Object.values(manifest.assets),
  ...Object.values(manifest.looseAssets),
  ...Object.values(manifest.interfaceAssets),
]) {
  assert.equal(record.file, manifest.atlas.file)
  const [x, y, w, h] = record.atlasRect
  assert.ok(x >= 0 && y >= 0 && x + w <= atlas.width && y + h <= atlas.height)
}
assert.deepEqual(Object.keys(manifest.interfaceAssets).sort(), ['oven-standard', 'standard-oven', 'standard-standard'])
for (const record of Object.values(manifest.interfaceAssets)) assert.deepEqual(record.logicalSize, [6, 13])

const v4Atlas = PNG.sync.read(fs.readFileSync(path.join(v4Root, 'assets', v4.atlas.file)))
for (const [name, canonical] of Object.entries(manifest.canonicalAssets)) {
  const old = v4.assets[name].atlasRect
  const fresh = canonical.atlasRect
  assert.deepEqual(fresh.slice(2), old.slice(2), `${name} canonical dimensions changed`)
  for (let row = 0; row < old[3]; row += 1) {
    const oldStart = ((old[1] + row) * v4Atlas.width + old[0]) * 4
    const newStart = ((fresh[1] + row) * atlas.width + fresh[0]) * 4
    assert.deepEqual(
      atlas.data.subarray(newStart, newStart + old[2] * 4),
      v4Atlas.data.subarray(oldStart, oldStart + old[2] * 4),
      `${name} canonical pixel row ${row} changed`,
    )
  }
}

for (const name of ['sink', 'sink-on', 'sink-broken']) {
  const image = PNG.sync.read(fs.readFileSync(path.join(draft, 'candidates', `${name}.png`)))
  const [bodyX, bodyY, bodyW] = manifest.assets[name].bodyRect
  const xs = [10, 50, 90, bodyW - 90, bodyW - 50, bodyW - 10].map(offset => bodyX + offset)
  const firstOpaque = xs.map(x => {
    for (let y = 0; y < image.height; y += 1) if (image.data[(y * image.width + x) * 4 + 3] > 127) return y
    return -1
  })
  assert.ok(firstOpaque.every(y => Math.abs(y - bodyY) <= 1), `${name} rear edge is not on the body datum: ${firstOpaque}`)
  assert.ok(Math.max(...firstOpaque) - Math.min(...firstOpaque) <= 1, `${name} rear edge is not straight: ${firstOpaque}`)
}

for (const name of ['kettle', 'toaster']) {
  const owner = grid.countertopObjectOwnership.defaultOwners[name]
  const centre = grid.fittedGrid.slotCentresX[grid.fittedGrid.slotOriginsX.indexOf(grid.fittedGrid.slotOriginsX[['cupboard', 'drawers'].indexOf(owner)])]
  assert.ok([126, 210].includes(centre))
  const asset = manifest.looseAssets[name]
  const x = centre - (asset.opaqueDrawRect[0] + asset.logicalSize[0] / 2)
  assert.equal(x + asset.opaqueDrawRect[0] + asset.logicalSize[0] / 2, centre, `${name} centre drift`)
}

const page = fs.readFileSync(path.join(publicRoot, 'index.html'), 'utf8')
assert.ok(page.includes("const ROUTE='/keeper-review/kitchen-complete-room-layout-v5'"))
assert.ok(page.includes('Immutable V4 reference'))
assert.ok(page.includes('Corrected modules, no connector'))
assert.ok(page.includes('Occupancy-derived fitted interface'))
assert.ok(page.includes("const canvases=[document.getElementById('canonical'),document.getElementById('raw'),document.getElementById('fitted')]"))
assert.ok(page.includes("canonical?'canonicalAssets':'assets'"))
assert.ok(page.includes("drag?.kind==='cabinet'&&drag.name===owner?drag.x+42"), 'owned countertop object must visually travel during cabinet drag')
assert.ok(page.includes('It carried ${carried.join'))
assert.ok(page.includes('Only cabinet identities and floor slot IDs persist; raw pointer coordinates never do.'))
assert.equal(page.includes('counterSlot'), false)
assert.equal(page.includes('healingAssets'), false)
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
assert.equal(fs.existsSync(path.join(publicRoot, 'assets')), false)

const config = fs.readFileSync(path.join(root, 'next.config.mjs'), 'utf8')
assert.ok(config.includes("source: '/keeper-review/kitchen-complete-room-layout-v5'"))
assert.ok(config.includes("destination: '/keeper-review/kitchen-complete-room-layout-v5/index.html'"))
const archiveRoute = fs.readFileSync(path.join(root, 'src/app/keeper-review/[set]/assets/[asset]/route.ts'), 'utf8')
assert.ok(archiveRoute.includes("'kitchen-complete-room-layout-v5'"))

console.log('Kitchen Complete Room Layout V5 verification passed: immutable comparison, exact 84×74 bodies, straight sink datum, pair-aware fitted interface, and cabinet-owned kettle/toaster.')
