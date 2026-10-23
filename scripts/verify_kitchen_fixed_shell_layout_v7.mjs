#!/usr/bin/env node
import assert from 'node:assert/strict'
import crypto from 'node:crypto'
import fs from 'node:fs'
import path from 'node:path'
import vm from 'node:vm'
import { PNG } from 'pngjs'

const root = process.cwd()
const set = 'kitchen-fixed-shell-2026-10-23-v7'
const slug = 'kitchen-fixed-shell-layout-v7'
const route = `/keeper-review/${slug}`
const draft = path.join(root, 'art/drafts', set)
const publicRoot = path.join(root, 'public/keeper-review', slug)
const sha = file => crypto.createHash('sha256').update(fs.readFileSync(file)).digest('hex')
const manifest = JSON.parse(fs.readFileSync(path.join(draft, 'manifest.json'), 'utf8'))
const publicManifest = JSON.parse(fs.readFileSync(path.join(publicRoot, 'manifest.json'), 'utf8'))
const grid = JSON.parse(fs.readFileSync(path.join(root, 'data/kitchen_room_grid_contract_v2.json'), 'utf8'))

assert.deepEqual(publicManifest, manifest)
assert.equal(manifest.schema, 'lighthouse-keeper/kitchen-fixed-shell-layout@7')
assert.equal(manifest.status, 'unapproved-fixed-shell-correction-review')
assert.deepEqual(manifest.roomGrid, grid)
assert.deepEqual(grid.fittedGrid.slotOriginsX, [84, 168, 252, 336, 420, 504])
assert.deepEqual(grid.fittedGrid.slotCentresX, [126, 210, 294, 378, 462, 546])
assert.deepEqual(grid.fittedGrid.bodySizePixels, [84, 74])
assert.equal(grid.fittedGrid.worktopSupportY, 141)
assert.equal(grid.fittedGrid.floorSupportY, 208)
assert.equal(grid.fittedGrid.keeperStopTurnY, 218)
assert.equal(grid.countertopObjectOwnership.oneObjectPerOwner, true)
assert.equal(grid.countertopObjectOwnership.ownerMovesObject, true)
assert.deepEqual(grid.countertopObjectOwnership.defaultOwners, { kettle: 'cupboard', toaster: 'drawers' })

for (const authority of Object.values(manifest.visualAuthorities)) {
  assert.equal(authority.changed, false)
  assert.equal(sha(path.join(root, authority.path)), authority.sha256)
}
assert.equal(manifest.architecture.internalEndBevels, false)
assert.equal(manifest.architecture.healingOverlay, false)
assert.equal(manifest.architecture.flatMonotoneCarcass, true)
assert.equal(manifest.architecture.sampledRailPixelsUsed, false)
assert.equal(manifest.architecture.opaqueBelfastSink, true)
assert.equal(manifest.architecture.sourceWorktopUndersideUsed, false)
assert.equal(manifest.corrections.gridOrStateBehaviourChanged, false)
assert.equal(manifest.corrections.applianceTopMaskingStripRemoved, true)
assert.equal(manifest.corrections.outerRunArtifactsRemoved, true)
assert.deepEqual(manifest.fixedLayers['worktop-run'].logicalSize, [504, 10])
assert.equal(manifest.fixedLayers['worktop-run'].atlasRect[3], 50)
assert.deepEqual(manifest.fixedLayers['carcass-run'].logicalSize, [504, 74])
assert.deepEqual(manifest.states.dishwasher, { off: 'dishwasher-off', on: 'dishwasher-on', broken: 'dishwasher-broken' })
for (const state of ['sink', 'sink-on', 'sink-broken']) {
  assert.equal(manifest.overlays[state].role, 'opaque Belfast sink cut-in above fixed worktop')
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

// The carcass layer may contain only the declared flat ink/blue palette.
const [cx, cy, cw, ch] = manifest.fixedLayers['carcass-run'].atlasRect
const allowed = new Set(['0,0,0,0', '3,22,37,255', '7,87,161,255', '5,70,135,255'])
for (let y = cy; y < cy + ch; y += 1) for (let x = cx; x < cx + cw; x += 1) {
  const i = (y * atlas.width + x) * 4
  const key = `${atlas.data[i]},${atlas.data[i + 1]},${atlas.data[i + 2]},${atlas.data[i + 3]}`
  assert.ok(allowed.has(key), `undeclared carcass pixel ${key}`)
}

const page = fs.readFileSync(path.join(publicRoot, 'index.html'), 'utf8')
assert.ok(page.includes(`const ROUTE='${route}'`))
assert.ok(page.includes("const STORAGE='lighthouse-kitchen-fixed-shell-v7'"))
assert.ok(page.includes('drawRecord(ctx,w,84,134,504,10)'))
assert.ok(page.includes('Belfast sink overpaints its real cutout'))
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

console.log('Kitchen Fixed Shell Layout V7 verification passed: opaque Belfast cut-in, shallow worktop, flat monotone skeleton, clean ends, unchanged grid and states.')
