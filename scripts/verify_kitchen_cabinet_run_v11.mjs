import assert from 'node:assert/strict'
import crypto from 'node:crypto'
import fs from 'node:fs'
import path from 'node:path'
import { PNG } from 'pngjs'

const root = process.cwd()
const set = 'kitchen-cabinet-run-2026-10-19-v11'
const sourceDir = path.join(root, 'art/source', set)
const rawDir = path.join(root, 'art/raw', set)
const draftDir = path.join(root, 'art/drafts', set)
const reviewDir = path.join(root, 'public/keeper-review/kitchen-cabinet-run-v11')
const backgroundPath = path.join(root, 'art/raw/kitchen-rebuild-foundation-2026-10-18-v1/kitchen-standard-background.png')

const sha = file => crypto.createHash('sha256').update(fs.readFileSync(file)).digest('hex')
const png = file => PNG.sync.read(fs.readFileSync(file))
const at = (image, x, y) => (y * image.width + x) * 4
const pixel = (image, x, y) => [...image.data.subarray(at(image, x, y), at(image, x, y) + 4)]
const same = (a, b) => a.every((value, index) => value === b[index])
const bbox = image => {
  let minX = image.width; let minY = image.height; let maxX = -1; let maxY = -1
  for (let y = 0; y < image.height; y++) for (let x = 0; x < image.width; x++) {
    if (pixel(image, x, y)[3]) {
      minX = Math.min(minX, x); minY = Math.min(minY, y)
      maxX = Math.max(maxX, x); maxY = Math.max(maxY, y)
    }
  }
  return maxX < 0 ? null : [minX, minY, maxX + 1, maxY + 1]
}
const over = (under, top) => {
  const ta = top[3] / 255; const ua = under[3] / 255; const oa = ta + ua * (1 - ta)
  if (!oa) return [0, 0, 0, 0]
  return [0, 1, 2].map(index => Math.round((top[index] * ta + under[index] * ua * (1 - ta)) / oa)).concat(Math.round(oa * 255))
}

const catalogue = JSON.parse(fs.readFileSync(path.join(draftDir, 'candidate-catalogue.json'), 'utf8'))
const register = JSON.parse(fs.readFileSync(path.join(draftDir, 'batch-register.json'), 'utf8'))
assert.equal(catalogue.set, set)
assert.equal(catalogue.status, 'approved-cabinet-review-authority')
assert.equal(catalogue.source.generatedFromScratch, true)
assert.equal(catalogue.source.historicalCabinetPixelsUsed, false)
assert.equal(catalogue.source.sha256, sha(path.join(sourceDir, 'cabinet-run-generated-source.png')))
assert.equal(catalogue.asset.name, 'cabinet-run-two-bay')
assert.deepEqual(catalogue.asset.logicalBodyPixels, [168, 74])
assert.deepEqual(catalogue.asset.cellPixels, [176, 82])
assert.deepEqual(catalogue.asset.cellGutterPixels, [4, 4])
assert.deepEqual(catalogue.asset.bayPixels, [84, 74])
assert.equal(catalogue.asset.projection, 'straight-on-flat-cutaway-parallel')
assert.equal(catalogue.asset.containsSink, false)
assert.equal(catalogue.asset.containsAppliances, false)
assert.deepEqual(catalogue.nativeRoom.pixels, [772, 224])
assert.deepEqual(catalogue.nativeRoom.bodyPlacements, [[168, 134], [420, 134]])
assert.deepEqual(catalogue.nativeRoom.standaloneOvenGapPixels, [336, 134, 84, 74])
assert.equal(register.status, 'approved-review-authority-unpromoted')
assert.equal(register.approvedOn, '2026-10-19')

for (const [relative, expected] of Object.entries(register.files)) {
  const file = path.join(root, relative)
  assert.ok(fs.existsSync(file), `registered file missing: ${relative}`)
  assert.equal(sha(file), expected, `registered file hash drifted: ${relative}`)
}

const master = png(path.join(rawDir, 'cabinet-run-master.png'))
const cell = png(path.join(rawDir, 'cabinet-run-native-cell.png'))
const room = png(path.join(rawDir, 'cabinet-run-duplicated-native-room.png'))
const background = png(backgroundPath)
assert.deepEqual([cell.width, cell.height], [176, 82])
assert.deepEqual(bbox(cell), [4, 4, 172, 78], 'native cabinet body or transparent gutter drifted')
assert.deepEqual([room.width, room.height], [772, 224])
assert.deepEqual([background.width, background.height], [772, 224])
assert.ok(master.width > 1100 && master.height > 500, 'master is not a high-resolution construction')
assert.deepEqual(bbox(master), [32, 32, master.width - 32, master.height - 32], 'master gutter drifted')

// Both room appearances must be literal composites of the same native cell.
const placements = [[164, 130], [416, 130]]
for (const [originX, originY] of placements) {
  for (let y = 0; y < cell.height; y++) for (let x = 0; x < cell.width; x++) {
    const expected = over(pixel(background, originX + x, originY + y), pixel(cell, x, y))
    assert.ok(same(expected, pixel(room, originX + x, originY + y)), `duplicate composite drift at ${originX + x},${originY + y}`)
  }
}

// No cabinet operation may alter the room outside the two transparent cells.
for (let y = 0; y < room.height; y++) for (let x = 0; x < room.width; x++) {
  const inside = placements.some(([px, py]) => x >= px && x < px + 176 && y >= py && y < py + 82)
  if (!inside) assert.ok(same(pixel(room, x, y), pixel(background, x, y)), `room changed outside cabinet cells at ${x},${y}`)
}

// The oven slot remains entirely background; this pass does not draw sink or appliances.
for (let y = 134; y < 208; y++) for (let x = 336; x < 420; x++) {
  assert.ok(same(pixel(room, x, y), pixel(background, x, y)), `standalone oven gap contaminated at ${x},${y}`)
}

const html = fs.readFileSync(path.join(reviewDir, 'index.html'), 'utf8')
for (const pattern of [
  /Cabinet-only V11 approved authority/,
  /One two-cabinet run/,
  /No sink or appliances/,
  /Installed body:<\/strong> 168 × 74 px/,
  /Two byte-identical runs · exact 772 × 224 game view/,
  /Promise\.all\(images\.map/,
  /img\.decode\(\)/,
]) assert.match(html, pattern)
assert.doesNotMatch(html, /Play|40-frame|4 fps|Broken state/, 'cabinet-only page accidentally claims state or animation work')

const archivePath = path.join(root, 'review-archive/sets/kitchen-cabinet-run-v11.json')
assert.ok(fs.existsSync(archivePath), 'cabinet V11 archive manifest missing; run npm run archive:keeper-review')
const archive = JSON.parse(fs.readFileSync(archivePath, 'utf8'))
assert.equal(archive.set, 'kitchen-cabinet-run-v11')
const archivedNames = new Set(Object.keys(archive.entries).map(entry => path.basename(entry)))
for (const name of ['cabinet-run-master.png', 'cabinet-run-native-cell.png', 'cabinet-run-duplicated-native-room.png']) {
  assert.ok(archivedNames.has(name), `review media was not archived: ${name}`)
}

console.log('Kitchen Cabinet Run V11 verified: one from-scratch high-resolution two-bay run, exact 168×74 native body, 4px gutters, and two literal duplicate composites')
