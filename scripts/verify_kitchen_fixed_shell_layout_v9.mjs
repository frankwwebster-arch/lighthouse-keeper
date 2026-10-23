#!/usr/bin/env node
import assert from 'node:assert/strict'
import crypto from 'node:crypto'
import fs from 'node:fs'
import path from 'node:path'
import vm from 'node:vm'
import { PNG } from 'pngjs'

const root = process.cwd()
const set = 'kitchen-fixed-shell-2026-10-23-v9'
const slug = 'kitchen-fixed-shell-layout-v9'
const route = `/keeper-review/${slug}`
const draft = path.join(root, 'art/drafts', set)
const publicRoot = path.join(root, 'public/keeper-review', slug)
const sha = file => crypto.createHash('sha256').update(fs.readFileSync(file)).digest('hex')
const manifest = JSON.parse(fs.readFileSync(path.join(draft, 'manifest.json'), 'utf8'))
const publicManifest = JSON.parse(fs.readFileSync(path.join(publicRoot, 'manifest.json'), 'utf8'))
const grid = JSON.parse(fs.readFileSync(path.join(root, 'data/kitchen_room_grid_contract_v2.json'), 'utf8'))

assert.deepEqual(publicManifest, manifest)
assert.equal(manifest.schema, 'lighthouse-keeper/kitchen-fixed-shell-layout@9')
assert.equal(manifest.status, 'unapproved-complete-front-and-perspective-review')
assert.deepEqual(manifest.roomGrid, grid)
assert.deepEqual(grid.fittedGrid.slotOriginsX, [84, 168, 252, 336, 420, 504])
assert.deepEqual(grid.fittedGrid.slotCentresX, [126, 210, 294, 378, 462, 546])
assert.deepEqual(grid.fittedGrid.bodySizePixels, [84, 74])
assert.equal(grid.fittedGrid.worktopSupportY, 141)
assert.equal(grid.fittedGrid.floorSupportY, 208)
assert.equal(grid.fittedGrid.keeperStopTurnY, 218)
assert.deepEqual(grid.countertopObjectOwnership.defaultOwners, { kettle: 'cupboard', toaster: 'drawers' })

for (const authority of Object.values(manifest.visualAuthorities)) {
  assert.equal(authority.changed, false)
  assert.equal(sha(path.join(root, authority.path)), authority.sha256)
}
assert.equal(manifest.architecture.healingOverlay, false)
assert.equal(manifest.architecture.standardCabinetTopFasciaUsed, false)
assert.equal(manifest.architecture.blueDividerFillUsed, false)
assert.equal(manifest.architecture.sinkSourceCountertopPixelsUsed, false)
assert.equal(manifest.architecture.outerEndPerspectivePlanes, true)
assert.equal(manifest.corrections.standardCabinetTopStripRemoved, true)
assert.equal(manifest.corrections.completeTopDrawerAndDoorOutlineVisible, true)
assert.equal(manifest.corrections.standardFrontSourceShiftMasterPixels, 10)
assert.equal(manifest.corrections.outerEndPerspectivePlaneMasterWidth, 34)
assert.equal(manifest.corrections.verticalGridChanged, false)
assert.equal(manifest.corrections.stateBehaviourChanged, false)
assert.deepEqual(manifest.fixedLayers['worktop-run'].logicalSize, [504, 10])
assert.deepEqual(manifest.states.dishwasher, { off: 'dishwasher-off', on: 'dishwasher-on', broken: 'dishwasher-broken' })

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

// Standard fronts begin on the very first master row after the 50 px worktop;
// the preceding row is empty. This rejects any reintroduced top fascia/gap.
for (const name of ['cupboard', 'drawers']) {
  const record = manifest.assets[name]
  const [ax, ay] = record.atlasRect
  const [bx, by, bw] = record.bodyRect
  const opaque = row => {
    let count = 0
    for (let x = bx; x < bx + bw; x += 1) {
      const i = ((ay + row) * atlas.width + ax + x) * 4
      if (atlas.data[i + 3]) count += 1
    }
    return count
  }
  assert.equal(opaque(by + 49), 0, `${name} leaks above fixed worktop boundary`)
  assert.ok(opaque(by + 50) > 400, `${name} top front is cropped or separated from worktop`)
}

// The outer perspective planes are materially wider than V8 and taper.
const [cx, cy, cw] = manifest.fixedLayers['carcass-run'].atlasRect
const alphaAt = (x, y) => atlas.data[((cy + y) * atlas.width + cx + x) * 4 + 3]
for (const [x, y] of [[5, 70], [25, 70], [5, 330], [cw - 6, 70], [cw - 26, 70], [cw - 6, 330]]) {
  assert.equal(alphaAt(x, y), 255, `missing outer perspective plane at ${x}/${y}`)
}
assert.equal(alphaAt(40, 100), 0, 'left perspective plane intrudes into the first front')
assert.equal(alphaAt(cw - 41, 100), 0, 'right perspective plane intrudes into the last front')

const page = fs.readFileSync(path.join(publicRoot, 'index.html'), 'utf8')
assert.ok(page.includes(`const ROUTE='${route}'`))
assert.ok(page.includes("const STORAGE='lighthouse-kitchen-fixed-shell-v9'"))
assert.ok(page.includes('drawRecord(ctx,w,84,134,504,10)'))
assert.ok(page.includes('No top fascia exists over standard cabinets'))
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

console.log('Kitchen Fixed Shell Layout V9 verification passed: no standard-cabinet top strip, complete top-front outlines, readable end perspective, unchanged grid/states.')
