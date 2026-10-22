#!/usr/bin/env node
import assert from 'node:assert/strict'
import crypto from 'node:crypto'
import fs from 'node:fs'
import path from 'node:path'
import vm from 'node:vm'
import { fileURLToPath } from 'node:url'
import { PNG } from 'pngjs'

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..')
const sha256 = bytes => crypto.createHash('sha256').update(bytes).digest('hex')
const route = 'kitchen-complete-room-layout-v2'
const set = 'kitchen-complete-room-layout-2026-10-22-v2'
const draftRoot = `art/drafts/${set}`
const sourcePath = 'art/source/kitchen-loose-object-foundation-2026-10-22-v1/loose-object-construction-sheet.png'
const sourceHash = '3f7be0874d6a3320d89f5c15e5c467d1f71af58d5ed594530e5aef82a4b2df33'
const v1Root = 'art/drafts/kitchen-cabinetry-room-layout-2026-10-22-v1'
const v1ManifestHash = '18cfad03b5d466e447e8bf7f66f4c5c0d9628c29e37398eecfa8bd74f13d6ffb'
const outputPins = {
  toaster: '75de96915b5038ea1c756f62cd0d7814412a2a517e1ef5e6eac94e6b755c287b',
  kettle: '73e881f6eeb34df257b55e324daf02b40f6c99f00f613a1fbb2fdbe995fad00a',
  bin: '0246dd50519cd897a034705cd758f23b60d9db61840107a75b8353ac95508aa6',
  table: '1e5410475c6117b89650b34d84eb6781a46aaaf9ffc0fcbec5c5e4763d926da4',
  chair: '395aaf0ec88674444afbc757cd184f8e11470e35a0b085ad1b540937ad037d56',
}

assert.equal(sha256(fs.readFileSync(path.join(root, sourcePath))), sourceHash, 'loose-object source changed')
assert.equal(sha256(fs.readFileSync(path.join(root, v1Root, 'manifest.json'))), v1ManifestHash, 'V1 room manifest changed')
const manifestBytes = fs.readFileSync(path.join(root, draftRoot, 'manifest.json'))
assert.deepEqual(manifestBytes, fs.readFileSync(path.join(root, `public/keeper-review/${route}/manifest.json`)), 'public and draft manifests differ')
const manifest = JSON.parse(manifestBytes)
const v1 = JSON.parse(fs.readFileSync(path.join(root, v1Root, 'manifest.json'), 'utf8'))
assert.equal(manifest.status, 'unapproved-complete-room-layout-review')
assert.equal(manifest.cabinetryPredecessor.assetsByteExact, true)
assert.deepEqual(manifest.room, v1.room)
assert.deepEqual(manifest.states, v1.states)
assert.deepEqual(manifest.looseGeometry, {
  worktopSupportY: 141,
  floorSupportY: 208,
  chairSeatTopHeightLp: 7.75,
  chairSeatTopHeightRoomPixels: 31,
  tableTopHeightLp: 14.5,
  defaultPositions: { toaster: [374, 109], kettle: [334, 103], bin: [728, 152], table: [630, 146], chair: [650, 125] },
})
assert.equal(manifest.boundaries.looseObjectArtApproved, false)
assert.equal(manifest.boundaries.looseObjectStatesAuthored, false)
assert.equal(manifest.boundaries.runtimeChanged, false)
assert.equal(manifest.boundaries.productionChanged, false)

for (const [name, record] of Object.entries(v1.assets)) {
  const inherited = manifest.assets[name]
  assert.deepEqual(inherited, record, `${name} V1 metadata changed`)
  assert.deepEqual(
    fs.readFileSync(path.join(root, draftRoot, 'assets', inherited.file)),
    fs.readFileSync(path.join(root, v1Root, 'assets', record.file)),
    `${name} V1 crop changed`,
  )
}

const archive = JSON.parse(fs.readFileSync(path.join(root, `review-archive/sets/${route}.json`), 'utf8'))
for (const [name, record] of Object.entries(manifest.looseAssets)) {
  const draft = fs.readFileSync(path.join(root, draftRoot, 'assets', record.file))
  assert.equal(sha256(draft), outputPins[name], `${name} output pin changed`)
  assert.equal(record.sha256, outputPins[name], `${name} manifest pin changed`)
  const archived = archive.entries[`/keeper-review/${route}/assets/${record.file}`]
  assert(archived, `${name} missing from archive set`)
  assert.equal(archived.sha256, outputPins[name])
  assert.deepEqual(draft, fs.readFileSync(path.join(root, archived.object)), `${name} archive object differs`)
  const png = PNG.sync.read(draft)
  assert.deepEqual([png.width, png.height], record.pixels)
  assert.deepEqual(record.logicalCanvas, [record.logicalSize[0] + 8, record.logicalSize[1] + 8])
  for (let x = 0; x < png.width; x++) assert.equal(png.data[x * 4 + 3], 0, `${name} top gutter occupied`)
  for (let x = 0; x < png.width; x++) assert.equal(png.data[((png.height - 1) * png.width + x) * 4 + 3], 0, `${name} bottom gutter occupied`)
  for (let y = 0; y < png.height; y++) {
    assert.equal(png.data[(y * png.width) * 4 + 3], 0, `${name} left gutter occupied`)
    assert.equal(png.data[(y * png.width + png.width - 1) * 4 + 3], 0, `${name} right gutter occupied`)
  }
}
assert.deepEqual(manifest.looseAssets.table.logicalSize, [80, 58])
assert.deepEqual(manifest.looseAssets.chair.logicalSize, [35, 79])

const page = fs.readFileSync(path.join(root, `public/keeper-review/${route}/index.html`), 'utf8')
assert.match(page, /UNAPPROVED COMPLETE-ROOM REVIEW V2/)
assert.match(page, /exact high-resolution style/)
assert.match(page, /chair seat <code>7\.75 lp<\/code>/)
assert.match(page, /Loose-object states follow after this foundation is approved/)
assert.match(page, /Promise\.all\(requests\)/, 'all 19 assets must decode before controls unlock')
assert.match(page, /localStorage/)
const inlineScript = page.match(/<script>([\s\S]+)<\/script>/)?.[1]
assert(inlineScript, 'room workbench script missing')
new vm.Script(inlineScript, { filename: `${route}/inline.js` })
const config = fs.readFileSync(path.join(root, 'next.config.mjs'), 'utf8')
assert.match(config, /source: '\/keeper-review\/kitchen-complete-room-layout-v2',[\s\S]*?destination: '\/keeper-review\/kitchen-complete-room-layout-v2\/index\.html'/)

console.log('Kitchen Complete Room Layout V2 verified: exact V1 cabinetry, five coordinated high-resolution movable loose objects, fixed support/seat/table geometry, synchronized join comparison and closed runtime gate.')
