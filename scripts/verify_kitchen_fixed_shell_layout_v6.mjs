#!/usr/bin/env node
import assert from 'node:assert/strict'
import crypto from 'node:crypto'
import fs from 'node:fs'
import path from 'node:path'
import vm from 'node:vm'
import { PNG } from 'pngjs'

const root = process.cwd()
const set = 'kitchen-fixed-shell-2026-10-23-v6'
const route = '/keeper-review/kitchen-fixed-shell-layout-v6'
const draft = path.join(root, 'art/drafts', set)
const publicRoot = path.join(root, 'public/keeper-review/kitchen-fixed-shell-layout-v6')
const sha = file => crypto.createHash('sha256').update(fs.readFileSync(file)).digest('hex')
const manifest = JSON.parse(fs.readFileSync(path.join(draft, 'manifest.json'), 'utf8'))
const publicManifest = JSON.parse(fs.readFileSync(path.join(publicRoot, 'manifest.json'), 'utf8'))
const grid = JSON.parse(fs.readFileSync(path.join(root, 'data/kitchen_room_grid_contract_v2.json'), 'utf8'))

assert.deepEqual(publicManifest, manifest)
assert.equal(manifest.schema, 'lighthouse-keeper/kitchen-fixed-shell-layout@6')
assert.equal(manifest.status, 'unapproved-fixed-shell-review')
assert.deepEqual(manifest.roomGrid, grid)
assert.equal(manifest.architecture.internalEndBevels, false)
assert.equal(manifest.architecture.healingOverlay, false)
assert.equal(manifest.architecture.sourceUnitShellPixelsExcluded, true)
assert.deepEqual(manifest.architecture.fixed, [
  'one continuous worktop',
  'one six-bay carcass run',
  'one continuous plinth',
  'six exact grid apertures',
])
assert.deepEqual(grid.fittedGrid.slotOriginsX, [84, 168, 252, 336, 420, 504])
assert.deepEqual(grid.fittedGrid.slotCentresX, [126, 210, 294, 378, 462, 546])
assert.equal(grid.fittedGrid.bayWidthPixels, 84)
assert.deepEqual(grid.fittedGrid.bodySizePixels, [84, 74])
assert.equal(grid.fittedGrid.worktopSupportY, 141)
assert.equal(grid.fittedGrid.floorSupportY, 208)
assert.equal(grid.fittedGrid.keeperStopTurnY, 218)
assert.equal(grid.countertopObjectOwnership.oneObjectPerOwner, true)
assert.equal(grid.countertopObjectOwnership.ownerMovesObject, true)
assert.deepEqual(grid.countertopObjectOwnership.defaultOwners, { kettle: 'cupboard', toaster: 'drawers' })
assert.equal(new Set(Object.values(grid.countertopObjectOwnership.defaultOwners)).size, 2)

for (const authority of Object.values(manifest.visualAuthorities)) {
  assert.equal(authority.changed, false)
  assert.equal(sha(path.join(root, authority.path)), authority.sha256, `${authority.path} changed`)
}

for (const [name, record] of Object.entries(manifest.assets)) {
  assert.deepEqual(record.bodyRect.slice(2), [420, 370], `${name} body does not map to 84×74`)
  assert.deepEqual(record.logicalBody, [84, 74])
  assert.equal(record.file, manifest.atlas.file)
}
assert.ok(manifest.assets['dishwasher-off'])
assert.deepEqual(manifest.states.dishwasher, {
  off: 'dishwasher-off',
  on: 'dishwasher-on',
  broken: 'dishwasher-broken',
})
assert.deepEqual(manifest.fixedLayers['carcass-backing'].logicalSize, [504, 74])
assert.deepEqual(manifest.fixedLayers['carcass-run'].logicalSize, [504, 74])
assert.deepEqual(manifest.fixedLayers['worktop-run'].logicalSize, [504, 14])
assert.deepEqual(manifest.fixedLayers['worktop-run'].bodyOrigin, [84, 134])
assert.deepEqual(manifest.overlays.hob.logicalSize, [84, 14])
for (const state of ['sink', 'sink-on', 'sink-broken']) assert.equal(manifest.overlays[state].role, 'sink cut-in above fixed worktop')

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
    assert.ok(x >= 0 && y >= 0 && x + w <= atlas.width && y + h <= atlas.height, `${section} atlas bounds`)
  }
}

const page = fs.readFileSync(path.join(publicRoot, 'index.html'), 'utf8')
assert.ok(page.includes("const ROUTE='/keeper-review/kitchen-fixed-shell-layout-v6'"))
assert.ok(page.includes('drawBacking(ctx)'))
assert.ok(page.includes('drawFixed(ctx)'))
assert.ok(page.includes('drawSinkOverlay(ctx)'))
assert.ok(page.includes('drawHob(ctx)'))
assert.ok(page.includes('no healing layer'))
assert.ok(page.includes("const STORAGE='lighthouse-kitchen-fixed-shell-v6'"))
assert.ok(page.includes("ownerCentre=owner=>ORIGINS[order.indexOf(owner)]+42"))
const inlineScript = page.match(/<script>([\s\S]+)<\/script>/)?.[1]
assert(inlineScript)
new vm.Script(inlineScript, { filename: `${route}/inline.js` })

const archivePath = path.join(root, 'review-archive/sets/kitchen-fixed-shell-layout-v6.json')
assert.ok(fs.existsSync(archivePath), 'run npm run maintain:keeper-review before verification')
const archive = JSON.parse(fs.readFileSync(archivePath, 'utf8'))
const entry = archive.entries[`${route}/assets/${manifest.atlas.file}`]
assert.ok(entry)
assert.equal(entry.sha256, manifest.atlas.sha256)
assert.equal(sha(path.join(root, entry.object)), manifest.atlas.sha256)
assert.equal(fs.existsSync(path.join(publicRoot, 'assets')), false)

const config = fs.readFileSync(path.join(root, 'next.config.mjs'), 'utf8')
assert.ok(config.includes("source: '/keeper-review/kitchen-fixed-shell-layout-v6'"))
assert.ok(config.includes("destination: '/keeper-review/kitchen-fixed-shell-layout-v6/index.html'"))
const archiveRoute = fs.readFileSync(path.join(root, 'src/app/keeper-review/[set]/assets/[asset]/route.ts'), 'utf8')
assert.ok(archiveRoute.includes("'kitchen-fixed-shell-layout-v6'"))

console.log('Kitchen Fixed Shell Layout V6 verification passed: one immutable worktop/carcass/plinth, exact 84 px bays, registered sink/hob overlays, complete appliance states, and cabinet-owned countertop objects.')
