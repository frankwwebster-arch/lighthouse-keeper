import assert from 'node:assert/strict'
import crypto from 'node:crypto'
import fs from 'node:fs'
import path from 'node:path'
import { PNG } from 'pngjs'

const root = process.cwd()
const set = 'kitchen-rebuild-foundation-2026-10-18-v1'
const source = path.join(root, 'art/source', set, 'generated/full-standard-kitchen-transparent-v2.png')
const master = path.join(root, 'art/source', set, 'generated/full-standard-kitchen-master-v1.png')
const raw = path.join(root, 'art/raw', set)
const draft = path.join(root, 'art/drafts', set)
const page = path.join(root, 'public/keeper-review/kitchen-rebuild-foundation-v1/index.html')
const archive = path.join(root, 'review-archive/sets/kitchen-rebuild-foundation-v1.json')
const binStandardAuthority = path.join(root, 'art/raw/kitchen-bin-states-2026-10-18-v28/bin-standard.png')
const binBrokenAuthority = path.join(root, 'art/raw/kitchen-bin-states-2026-10-18-v28/bin-broken-overflowing.png')

const sha = file => crypto.createHash('sha256').update(fs.readFileSync(file)).digest('hex')
const readPng = file => PNG.sync.read(fs.readFileSync(file))
const at = (image, x, y) => (y * image.width + x) * 4
const pixel = (image, x, y) => image.data.subarray(at(image, x, y), at(image, x, y) + 4)
const samePixel = (a, b) => a[0] === b[0] && a[1] === b[1] && a[2] === b[2] && a[3] === b[3]
const bbox = image => {
  let minX = image.width; let minY = image.height; let maxX = -1; let maxY = -1
  for (let y = 0; y < image.height; y++) for (let x = 0; x < image.width; x++) {
    if (pixel(image, x, y)[3]) { minX = Math.min(minX, x); minY = Math.min(minY, y); maxX = Math.max(maxX, x); maxY = Math.max(maxY, y) }
  }
  return maxX < 0 ? null : [minX, minY, maxX + 1, maxY + 1]
}
const dimensions = (image, expected, label) => assert.deepEqual([image.width, image.height], expected, `${label} dimensions drifted`)

assert.equal(sha(source), '3a4430a0d07be4a945e00ba717d2f23e55e8730ba63b420efa41aaa3c283a9f1', 'transparent unified source changed')
assert.equal(sha(master), 'a6f0b8d3d8181096e0455effc2753630ad893c34760c68a20fb40baedb60b48d', 'opaque unified source changed')
assert.equal(sha(binStandardAuthority), '86b05224a7da5fc5c05918f2875018920ed54cf46fc00cb08952ffd29789f9c0', 'accepted standard bin changed')
assert.equal(sha(binBrokenAuthority), '77ad87fabfd3e5c10a4a14f294af343a5d93a2a2015e6d77f18a4140b1f5fb4f', 'accepted broken bin changed')

const catalogue = JSON.parse(fs.readFileSync(path.join(draft, 'candidate-catalogue.json'), 'utf8'))
const register = JSON.parse(fs.readFileSync(path.join(draft, 'batch-register.json'), 'utf8'))
assert.equal(catalogue.set, set)
assert.equal(catalogue.status, 'clean-slate-standard-foundation-awaiting-review')
assert.equal(catalogue.scope, 'standard-state foundation only; no alternate states or animation')
assert.deepEqual(catalogue.roomPixels, [772, 224])
assert.deepEqual(catalogue.logicalRoomPixels, [193, 56])
assert.equal(catalogue.renderScale, 4)
assert.deepEqual(catalogue.geometry, {
  fittedRunXExclusive: [84, 588],
  bayCount: 6,
  bayWidthPixels: 84,
  bayOrder: ['fridge', 'kettle', 'toaster', 'oven-hob', 'mixing-bowl', 'basin'],
  worktopTopY: 134,
  fasciaTopY: 151,
  rearWallFootLineY: 208,
  runVisibleBottomYExclusive: 218,
  tableChairBoundsExclusive: [680, 148, 764, 222],
  approvedBinCellTopLeft: [8, 149],
})
assert.equal(catalogue.construction.oneUnifiedGeneratedMaster, true)
assert.equal(catalogue.construction.allNewAssetsDerivedFromSameMaster, true)
assert.deepEqual(catalogue.construction.priorAssetPixelsUsed, ['accepted-bin-standard', 'accepted-bin-broken-authority-card'])
assert.equal(catalogue.acceptedBinAuthority.modified, false)
assert.equal(register.status, 'awaiting-standard-foundation-visual-review')
assert.equal(register.promotion, 'none')
assert.equal(register.runtimeWiring, 'unchanged')

for (const [filename, metadata] of Object.entries(catalogue.outputs)) {
  const file = path.join(raw, filename)
  assert.ok(fs.existsSync(file), `missing output ${filename}`)
  assert.equal(sha(file), metadata.sha256, `${filename} hash drifted`)
  dimensions(readPng(file), metadata.pixels, filename)
}
assert.equal(sha(path.join(raw, 'bin-standard-approved.png')), sha(binStandardAuthority), 'standard bin is not byte-identical')
assert.equal(sha(path.join(raw, 'bin-broken-approved.png')), sha(binBrokenAuthority), 'broken bin is not byte-identical')

const background = readPng(path.join(raw, 'kitchen-standard-background.png'))
const furniture = readPng(path.join(raw, 'kitchen-standard-furniture-layer.png'))
const roomWithoutBin = readPng(path.join(raw, 'kitchen-standard-without-bin.png'))
const room = readPng(path.join(raw, 'kitchen-standard-foundation.png'))
const run = readPng(path.join(raw, 'standard-fitted-run.png'))
const table = readPng(path.join(raw, 'standard-table-chair.png'))
for (const [image, label] of [[background, 'background'], [furniture, 'furniture'], [roomWithoutBin, 'room without bin'], [room, 'room']]) dimensions(image, [772, 224], label)
dimensions(run, [504, 113], 'fitted run')
dimensions(table, [84, 74], 'table and chair')
assert.deepEqual(bbox(run), [0, 0, 504, 113], 'run has left its declared measured box')
assert.deepEqual(bbox(table), [0, 0, 84, 74], 'table/chair has left its declared measured box')

// The transparent furniture layer may contain pixels only inside the measured
// fitted run or the complete table/chair cell.
for (let y = 0; y < 224; y++) for (let x = 0; x < 772; x++) {
  const allowed = (x >= 84 && x < 588 && y >= 105 && y < 218) || (x >= 680 && x < 764 && y >= 148 && y < 222)
  if (!allowed) assert.equal(pixel(furniture, x, y)[3], 0, `furniture escaped measured boxes at ${x},${y}`)
  assert.equal(pixel(background, x, y)[3], 255, `background is not opaque at ${x},${y}`)
}

const over = (under, top) => {
  const ta = top[3] / 255; const ua = under[3] / 255; const oa = ta + ua * (1 - ta)
  if (!oa) return [0, 0, 0, 0]
  return [0, 1, 2].map(i => Math.round((top[i] * ta + under[i] * ua * (1 - ta)) / oa)).concat(Math.round(oa * 255))
}
for (let y = 0; y < 224; y++) for (let x = 0; x < 772; x++) {
  const expected = over(pixel(background, x, y), pixel(furniture, x, y))
  assert.ok(samePixel(expected, pixel(roomWithoutBin, x, y)), `room-without-bin compositing drift at ${x},${y}`)
}

const bin = readPng(binStandardAuthority)
for (let y = 0; y < 224; y++) for (let x = 0; x < 772; x++) {
  let expected = pixel(roomWithoutBin, x, y)
  if (x >= 8 && x < 80 && y >= 149 && y < 221) expected = over(expected, pixel(bin, x - 8, y - 149))
  assert.ok(samePixel(expected, pixel(room, x, y)), `approved bin composite drift at ${x},${y}`)
}

for (let bay = 0; bay < 6; bay++) {
  const name = catalogue.geometry.bayOrder[bay]
  const image = readPng(path.join(raw, `bay-${name}.png`))
  dimensions(image, [84, 120], `${name} isolated bay`)
  for (let y = 0; y < 120; y++) for (let x = 0; x < 84; x++) {
    assert.ok(samePixel(pixel(image, x, y), pixel(furniture, 84 + bay * 84 + x, 98 + y)), `${name} is not a literal master crop at ${x},${y}`)
  }
  for (let x = 0; x < 84; x++) assert.equal(pixel(image, x, 0)[3], 0, `${name} has no transparent inspection gutter above it`)
}

const html = fs.readFileSync(page, 'utf8')
assert.match(html, /exact native game size/i)
assert.match(html, /Promise\.all\(media\.map/)
assert.match(html, /img\.decode\(\)/)
assert.match(html, /V41 and the earlier asset-by-asset kitchen drafts are rejected provenance/)
assert.doesNotMatch(html, /40-frame|4 fps|Play effects/, 'foundation page accidentally claims animation')
const refs = [...html.matchAll(/(?:src=|\?')"?(?:assets\/)([^"'?]+)/g)].map(match => match[1])
assert.ok(refs.length >= 11, 'review page does not expose the complete standard foundation')

assert.ok(fs.existsSync(archive), 'content-addressed review manifest missing; run npm run archive:keeper-review')
const archived = JSON.parse(fs.readFileSync(archive, 'utf8'))
assert.equal(archived.set, 'kitchen-rebuild-foundation-v1')
const archivedNames = new Set(Object.keys(archived.entries).map(entry => path.basename(entry)))
for (const filename of refs) assert.ok(archivedNames.has(filename), `review media was not archived: ${filename}`)

console.log('Kitchen Rebuild V1 verified: one coherent 772x224 standard room, six exact 84px bays, literal isolated crops, complete table/chair, and byte-identical accepted bin')
