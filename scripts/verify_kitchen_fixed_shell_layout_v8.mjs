#!/usr/bin/env node
import assert from 'node:assert/strict'
import crypto from 'node:crypto'
import fs from 'node:fs'
import path from 'node:path'
import vm from 'node:vm'
import { PNG } from 'pngjs'

const root = process.cwd()
const set = 'kitchen-fixed-shell-2026-10-23-v8'
const slug = 'kitchen-fixed-shell-layout-v8'
const route = `/keeper-review/${slug}`
const draft = path.join(root, 'art/drafts', set)
const publicRoot = path.join(root, 'public/keeper-review', slug)
const sha = file => crypto.createHash('sha256').update(fs.readFileSync(file)).digest('hex')
const manifest = JSON.parse(fs.readFileSync(path.join(draft, 'manifest.json'), 'utf8'))
const publicManifest = JSON.parse(fs.readFileSync(path.join(publicRoot, 'manifest.json'), 'utf8'))
const grid = JSON.parse(fs.readFileSync(path.join(root, 'data/kitchen_room_grid_contract_v2.json'), 'utf8'))

assert.deepEqual(publicManifest, manifest)
assert.equal(manifest.schema, 'lighthouse-keeper/kitchen-fixed-shell-layout@8')
assert.equal(manifest.status, 'unapproved-material-and-sink-mask-review')
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
assert.equal(manifest.architecture.continuousShadedCarcassMaterial, true)
assert.equal(manifest.architecture.flatMonotoneCarcass, false)
assert.equal(manifest.architecture.sampledRailPixelsUsed, false)
assert.equal(manifest.architecture.blueDividerFillUsed, false)
assert.equal(manifest.architecture.sinkSourceCountertopPixelsUsed, false)
assert.equal(manifest.architecture.outerEndPerspectivePlanes, true)
assert.equal(manifest.corrections.verticalGridChanged, false)
assert.equal(manifest.corrections.stateBehaviourChanged, false)
assert.deepEqual(manifest.fixedLayers['worktop-run'].logicalSize, [504, 10])
assert.equal(manifest.fixedLayers['worktop-run'].atlasRect[3], 50)
assert.deepEqual(manifest.states.dishwasher, { off: 'dishwasher-off', on: 'dishwasher-on', broken: 'dishwasher-broken' })
for (const state of ['sink', 'sink-on', 'sink-broken']) {
  assert.equal(manifest.overlays[state].role, 'geometry-masked Belfast porcelain/hardware/state-water; zero source countertop pixels')
}

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

// Internal dividers contain exactly the narrow ink seam: no opaque blue band.
const carcass = manifest.fixedLayers['carcass-run'].atlasRect
for (const edge of [420, 840, 1260, 1680, 2100]) {
  for (let y = 70; y < 330; y += 13) {
    for (let dx = -10; dx <= 10; dx += 1) {
      const x = carcass[0] + edge + dx
      const row = carcass[1] + y
      const i = (row * atlas.width + x) * 4
      const alpha = atlas.data[i + 3]
      if (dx >= -2 && dx <= 1) assert.equal(alpha, 255, `missing ink seam at ${edge}/${y}`)
      else assert.equal(alpha, 0, `blue divider surface at ${edge + dx}/${y}`)
    }
  }
}

// Standard/On blue is confined to the central stream. Broken may retain pale
// approved overflow, but no low-red turquoise countertop pixel may spread.
for (const state of ['sink', 'sink-on', 'sink-broken']) {
  const record = manifest.overlays[state]
  const [x0, y0, w, h] = record.atlasRect
  const centre = record.bodyRect[0] + record.bodyRect[2] / 2
  for (let y = 0; y < h; y += 1) for (let x = 0; x < w; x += 1) {
    const i = ((y0 + y) * atlas.width + x0 + x) * 4
    const [r, g, b, a] = atlas.data.subarray(i, i + 4)
    if (a && b > 145 && b > r * 1.2 && b > g * 1.02 && Math.abs(x - centre) > 30) {
      assert.ok(state === 'sink-broken' && r > 145, `${state} retained source countertop blue`)
    }
  }
}

const page = fs.readFileSync(path.join(publicRoot, 'index.html'), 'utf8')
assert.ok(page.includes(`const ROUTE='${route}'`))
assert.ok(page.includes("const STORAGE='lighthouse-kitchen-fixed-shell-v8'"))
assert.ok(page.includes('drawRecord(ctx,w,84,134,504,10)'))
assert.ok(page.includes('one shared worktop supplies its exact colour and alignment'))
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

console.log('Kitchen Fixed Shell Layout V8 verification passed: no sink countertop pixels, no blue divider bands, continuous shaded material, end perspective, unchanged grid/states.')
