import assert from 'node:assert/strict'
import crypto from 'node:crypto'
import fs from 'node:fs'
import path from 'node:path'
import { PNG } from 'pngjs'

const root = process.cwd()
const raw = path.join(root, 'art/raw/kitchen-sink-cabinet-2026-10-19-v13')
const draft = path.join(root, 'art/drafts/kitchen-sink-cabinet-2026-10-19-v13')
const review = path.join(root, 'public/keeper-review/kitchen-sink-cabinet-v13')
const cabinetPath = path.join(root, 'art/raw/kitchen-cabinet-run-2026-10-19-v11/cabinet-run-native-cell.png')
const backgroundPath = path.join(root, 'art/raw/kitchen-rebuild-foundation-2026-10-18-v1/kitchen-standard-background.png')
const sha = file => crypto.createHash('sha256').update(fs.readFileSync(file)).digest('hex')
const png = file => PNG.sync.read(fs.readFileSync(file))
const pixel = (image, x, y) => [...image.data.subarray((y * image.width + x) * 4, (y * image.width + x) * 4 + 4)]
const same = (a, b) => a.every((value, index) => value === b[index])
const bbox = image => {
  let minX = image.width; let minY = image.height; let maxX = -1; let maxY = -1
  for (let y = 0; y < image.height; y++) for (let x = 0; x < image.width; x++) if (pixel(image, x, y)[3]) {
    minX = Math.min(minX, x); minY = Math.min(minY, y); maxX = Math.max(maxX, x); maxY = Math.max(maxY, y)
  }
  return [minX, minY, maxX + 1, maxY + 1]
}
const over = (under, top) => {
  const ta = top[3] / 255; const ua = under[3] / 255; const oa = ta + ua * (1 - ta)
  if (!oa) return [0, 0, 0, 0]
  return [0, 1, 2].map(index => Math.round((top[index] * ta + under[index] * ua * (1 - ta)) / oa)).concat(Math.round(oa * 255))
}

const catalogue = JSON.parse(fs.readFileSync(path.join(draft, 'candidate-catalogue.json'), 'utf8'))
const register = JSON.parse(fs.readFileSync(path.join(draft, 'batch-register.json'), 'utf8'))
assert.equal(catalogue.set, 'kitchen-sink-cabinet-2026-10-19-v13')
assert.equal(catalogue.status, 'standalone-sink-fit-awaiting-visual-review')
assert.equal(catalogue.construction.completeStandaloneOneBayUnit, true)
assert.equal(catalogue.construction.overlaysApprovedCabinet, false)
assert.equal(catalogue.construction.containsOwnCabinetWorktopBasinTap, true)
assert.deepEqual(catalogue.construction.bodyPixels, [84, 74])
assert.deepEqual(catalogue.construction.cellPixels, [92, 108])
assert.deepEqual(catalogue.construction.bodyOriginInCell, [4, 30])
assert.equal(catalogue.construction.tapAndBasinChangeWhenBroken, false)
assert.equal(catalogue.states.allStaticBasesByteIdentical, true)
assert.equal(catalogue.states.waterEffectsIncluded, false)
assert.deepEqual(catalogue.fitProof.approvedTwoBayRunBodyBoundsExclusive, [168, 134, 336, 208])
assert.deepEqual(catalogue.fitProof.standaloneSinkBodyBoundsExclusive, [336, 134, 420, 208])
assert.equal(catalogue.fitProof.sharedPixels, false)
for (const [relative, expected] of Object.entries(register.files)) assert.equal(sha(path.join(root, relative)), expected, `registered file drifted: ${relative}`)

const stateNames = ['sink-cabinet-standard.png', 'sink-cabinet-on-base.png', 'sink-cabinet-broken-base.png']
for (const name of stateNames) {
  const image = png(path.join(raw, name))
  assert.deepEqual([image.width, image.height], [92, 108])
  assert.deepEqual(bbox(image), [4, 4, 88, 104], `${name} lost its four-pixel safety gutter`)
  assert.equal(sha(path.join(raw, name)), catalogue.outputs[name])
}
assert.equal(new Set(stateNames.map(name => sha(path.join(raw, name)))).size, 1, 'static state bases are not byte-identical')

const room = png(path.join(raw, 'cabinet-run-plus-sink-native-room.png'))
const background = png(backgroundPath)
const cabinet = png(cabinetPath)
const sink = png(path.join(raw, stateNames[0]))
assert.deepEqual([room.width, room.height], [772, 224])
for (let y = 0; y < room.height; y++) for (let x = 0; x < room.width; x++) {
  let expected = pixel(background, x, y)
  if (x >= 164 && x < 340 && y >= 130 && y < 212) expected = over(expected, pixel(cabinet, x - 164, y - 130))
  if (x >= 332 && x < 424 && y >= 104 && y < 212) expected = over(expected, pixel(sink, x - 332, y - 104))
  assert.ok(same(expected, pixel(room, x, y)), `fit proof changed outside exact source composites at ${x},${y}`)
}
for (let y = 0; y < 108; y++) for (let x = 0; x < 92; x++) {
  if (!pixel(sink, x, y)[3]) continue
  const roomX = 332 + x
  assert.ok(roomX >= 336 && roomX < 420, `sink opaque pixel escaped its one-bay x bounds at ${roomX}`)
}

const html = fs.readFileSync(path.join(review, 'index.html'), 'utf8')
for (const pattern of [/Standalone sink cabinet/, /No cabinet beneath/, /byte-identical/, /Approved two-cabinet run \+ standalone sink/, /does not overlay or redraw any approved cabinet/, /img\.decode\(\)/]) assert.match(html, pattern)
const archive = JSON.parse(fs.readFileSync(path.join(root, 'review-archive/sets/kitchen-sink-cabinet-v13.json'), 'utf8'))
assert.equal(Object.keys(archive.entries).length, 5)
for (const name of Object.keys(catalogue.outputs)) assert.equal(archive.entries[`/keeper-review/kitchen-sink-cabinet-v13/assets/${name}`].sha256, catalogue.outputs[name])
console.log('Kitchen Sink Cabinet V13 verified: complete independent 84×74 one-bay unit, byte-identical static state bases, exact no-overlap fit beside approved V11 run')
