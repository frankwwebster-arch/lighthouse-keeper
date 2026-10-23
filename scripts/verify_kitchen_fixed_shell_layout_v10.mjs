#!/usr/bin/env node
import assert from 'node:assert/strict'
import crypto from 'node:crypto'
import fs from 'node:fs'
import path from 'node:path'
import vm from 'node:vm'
import { PNG } from 'pngjs'

const root = process.cwd()
const set = 'kitchen-fixed-shell-2026-10-23-v10'
const slug = 'kitchen-fixed-shell-layout-v10'
const route = `/keeper-review/${slug}`
const draft = path.join(root, 'art/drafts', set)
const publicRoot = path.join(root, 'public/keeper-review', slug)
const sha = file => crypto.createHash('sha256').update(fs.readFileSync(file)).digest('hex')
const manifest = JSON.parse(fs.readFileSync(path.join(draft, 'manifest.json'), 'utf8'))
const publicManifest = JSON.parse(fs.readFileSync(path.join(publicRoot, 'manifest.json'), 'utf8'))
const grid = JSON.parse(fs.readFileSync(path.join(root, 'data/kitchen_room_grid_contract_v2.json'), 'utf8'))

assert.deepEqual(publicManifest, manifest)
assert.equal(manifest.schema, 'lighthouse-keeper/kitchen-fixed-shell-layout@10')
assert.equal(manifest.status, 'unapproved-full-end-perspective-and-broken-loose-states-review')
assert.deepEqual(manifest.roomGrid, grid)
assert.deepEqual(grid.fittedGrid.slotOriginsX, [84, 168, 252, 336, 420, 504])
assert.deepEqual(grid.fittedGrid.slotCentresX, [126, 210, 294, 378, 462, 546])
assert.deepEqual(grid.fittedGrid.bodySizePixels, [84, 74])
assert.equal(grid.fittedGrid.worktopSupportY, 141)
assert.equal(grid.fittedGrid.floorSupportY, 208)
assert.equal(grid.fittedGrid.keeperStopTurnY, 218)
assert.deepEqual(grid.countertopObjectOwnership.defaultOwners, { kettle: 'cupboard', toaster: 'drawers' })

assert.equal(manifest.architecture.healingOverlay, false)
assert.equal(manifest.architecture.standardCabinetTopFasciaUsed, false)
assert.equal(manifest.architecture.fullOuterEndPerspectiveReturns, true)
assert.equal(manifest.architecture.outerReturnsOutsideFrontGrid, true)
assert.equal(manifest.corrections.v9FrontsAndGridRetained, true)
assert.equal(manifest.corrections.outerEndReturnLogicalDepth, 16)
assert.equal(manifest.corrections.verticalGridChanged, false)
assert.equal(manifest.corrections.interactionCoordinatesChanged, false)
assert.deepEqual(manifest.fixedLayers['worktop-run'].logicalSize, [504, 10])
assert.deepEqual(manifest.states.dishwasher, { off: 'dishwasher-off', on: 'dishwasher-on', broken: 'dishwasher-broken' })
assert.deepEqual(manifest.states.kettle, { off: 'kettle', on: 'kettle', broken: 'kettle-broken' })
assert.deepEqual(manifest.states.toaster, { standard: 'toaster', on: 'toaster', broken: 'toaster-broken' })
assert.deepEqual(manifest.states.bowl, { standard: 'bowl', broken: 'bowl-broken' })
assert.equal(manifest.looseGeometry.bowlOwnership, 'table-child')
assert.equal(manifest.looseGeometry.bowlMovesWithTable, true)
assert.equal(manifest.looseAssets['bowl-broken'].whiskBesideBowl, true)
assert.equal(manifest.looseAssets['bowl-broken'].spillRetained, true)
assert.equal(manifest.looseAssets['toaster-broken'].casingChanged, false)

for (const [file, digest] of [
  ['art/source/kitchen-high-resolution-foundation-2026-10-22-v1/kitchen-fitted-run-first-render-authority.png', 'bb37dc2e3e47c7c26649e627bae32eed04801c2e20571cbee7996d13e6e06bf2'],
  ['art/source/kitchen-fixed-shell-2026-10-23-v10/warm-bowl-state-reference.png', '9e124727bd4e9225b80d715798324a5d2407146d87b837f92b46cce8750f6b8e'],
  ['art/drafts/kitchen-fixed-shell-2026-10-23-v9/assets/kitchen-fixed-shell-atlas-v9.png', '2eeaef85609eed228a0ecfa7eed30ef722d2ed070957969d3b86792c517b480f'],
]) assert.equal(sha(path.join(root, file)), digest)

const atlasPath = path.join(draft, 'assets', manifest.atlas.file)
assert.equal(manifest.atlas.uniqueImageRequests, 1)
assert.equal(manifest.atlas.lossless, true)
assert.equal(sha(atlasPath), manifest.atlas.sha256)
const atlas = PNG.sync.read(fs.readFileSync(atlasPath))
assert.deepEqual([atlas.width, atlas.height], manifest.atlas.pixels)
for (const section of ['fixedLayers', 'overlays', 'assets', 'looseAssets']) {
  for (const record of Object.values(manifest[section])) {
    assert.equal(record.file, manifest.atlas.file)
    const [x, y, w, h] = record.atlasRect
    assert.ok(x >= 0 && y >= 0 && x + w <= atlas.width && y + h <= atlas.height)
  }
}

const pixel = (record, x, y) => {
  const [ax, ay] = record.atlasRect
  const i = ((ay + y) * atlas.width + ax + x) * 4
  return Array.from(atlas.data.subarray(i, i + 4))
}

// V9's no-fascia front boundary remains exact.
for (const name of ['cupboard', 'drawers']) {
  const record = manifest.assets[name]
  const [bx, by, bw] = record.bodyRect
  const opaque = row => {
    let count = 0
    for (let x = bx; x < bx + bw; x += 1) if (pixel(record, x, row)[3]) count += 1
    return count
  }
  assert.equal(opaque(by + 49), 0)
  assert.ok(opaque(by + 50) > 400)
}

// The complete returns live outside the 2520-master-pixel front run.
const ends = manifest.fixedLayers['end-perspective-returns']
assert.deepEqual(ends.logicalSize, [536, 74])
assert.deepEqual(ends.bodyOrigin, [68, 134])
for (const [x, y] of [[6, 25], [12, 100], [70, 300], [2609, 300], [2673, 100], [2673, 25]]) {
  assert.equal(pixel(ends, x, y)[3], 255, `missing end-return pixel ${x}/${y}`)
}
assert.equal(pixel(ends, 81, 100)[3], 0, 'left return entered the exact front grid')
assert.equal(pixel(ends, 2599, 100)[3], 0, 'right return entered the exact front grid')

// The new door is a foreground, bottom-hinged trapezoid above the floor,
// while the V9 controls/interior above the replacement boundary are exact.
const door = manifest.overlays['dishwasher-broken-door']
const doorAlpha = []
for (let y = 0; y < door.atlasRect[3]; y += 1) {
  for (let x = 0; x < door.atlasRect[2]; x += 1) if (pixel(door, x, y)[3]) doorAlpha.push([x, y])
}
assert.ok(doorAlpha.length > 20000)
assert.ok(Math.min(...doorAlpha.map(([, y]) => y)) < 250)
assert.ok(Math.max(...doorAlpha.map(([, y]) => y)) < 350)
assert.ok(door.role.includes('bottom-hinged'))

const v9Manifest = JSON.parse(fs.readFileSync(path.join(root, 'art/drafts/kitchen-fixed-shell-2026-10-23-v9/manifest.json'), 'utf8'))
const v9Atlas = PNG.sync.read(fs.readFileSync(path.join(root, 'art/drafts/kitchen-fixed-shell-2026-10-23-v9/assets', v9Manifest.atlas.file)))
const v9Record = v9Manifest.assets['dishwasher-broken']
const currentRecord = manifest.assets['dishwasher-broken']
for (let y = 0; y < 276; y += 1) {
  for (let x = 0; x < currentRecord.atlasRect[2]; x += 1) {
    const [vax, vay] = v9Record.atlasRect
    const vi = ((vay + y) * v9Atlas.width + vax + x) * 4
    assert.deepEqual(pixel(currentRecord, x, y), Array.from(v9Atlas.data.subarray(vi, vi + 4)))
  }
}

// Every fully opaque accepted toaster-casing pixel is byte-exact in Broken.
const toaster = manifest.looseAssets.toaster
const toasterBroken = manifest.looseAssets['toaster-broken']
for (let y = 0; y < toaster.atlasRect[3]; y += 1) {
  for (let x = 0; x < toaster.atlasRect[2]; x += 1) {
    const standard = pixel(toaster, x, y)
    if (standard[3] === 255) assert.deepEqual(pixel(toasterBroken, x, y), standard)
  }
}

// Loose-state canvases remain genuinely transparent and isolated.
for (const name of ['kettle-broken', 'bowl', 'bowl-broken']) {
  const record = manifest.looseAssets[name]
  assert.equal(pixel(record, 0, 0)[3], 0)
  let opaque = 0
  const total = record.atlasRect[2] * record.atlasRect[3]
  for (let y = 0; y < record.atlasRect[3]; y += 1) {
    for (let x = 0; x < record.atlasRect[2]; x += 1) if (pixel(record, x, y)[3]) opaque += 1
  }
  assert.ok(opaque / total < 0.55, `${name} retained an opaque review-card background`)
}

const page = fs.readFileSync(path.join(publicRoot, 'index.html'), 'utf8')
assert.ok(page.includes(`const ROUTE='${route}'`))
assert.ok(page.includes("const STORAGE='lighthouse-kitchen-fixed-shell-v10'"))
assert.ok(page.includes("drawRecord(ctx,manifest.fixedLayers['end-perspective-returns'],68,134,536,74)"))
assert.ok(page.includes("drawDishwasherDoor(ctx)"))
assert.ok(page.includes("kettle:'broken',toaster:'broken',bowl:'broken'"))
assert.ok(page.includes("The bowl is centred on and moves with the table."))
const inlineScript = page.match(/<script>([\s\S]+)<\/script>/)?.[1]
assert(inlineScript)
new vm.Script(inlineScript, { filename: `${route}/inline.js` })

const archivePath = path.join(root, 'review-archive/sets', `${slug}.json`)
assert.ok(fs.existsSync(archivePath), 'run npm run maintain:keeper-review before verification')
const archive = JSON.parse(fs.readFileSync(archivePath, 'utf8'))
const entry = archive.entries[`${route}/assets/${manifest.atlas.file}`]
assert.ok(entry)
assert.equal(entry.sha256, manifest.atlas.sha256)
assert.equal(sha(path.join(root, entry.object)), manifest.atlas.sha256)
assert.equal(fs.existsSync(path.join(publicRoot, 'assets')), false)

const config = fs.readFileSync(path.join(root, 'next.config.mjs'), 'utf8')
assert.ok(config.includes(`source: '${route}'`))
assert.ok(config.includes(`destination: '${route}/index.html'`))
const archiveRoute = fs.readFileSync(path.join(root, 'src/app/keeper-review/[set]/assets/[asset]/route.ts'), 'utf8')
assert.ok(archiveRoute.includes(`'${slug}'`))

console.log('Kitchen Fixed Shell Layout V10 verification passed: exact V9 front grid, full external end returns, partly-open dishwasher and complete Broken loose states.')
