import assert from 'node:assert/strict'
import crypto from 'node:crypto'
import fs from 'node:fs'
import path from 'node:path'
import { PNG } from 'pngjs'

const root = process.cwd()
const source = path.join(root, 'art/source/kitchen-fitted-galley-2026-10-17-v20')
const raw = path.join(root, 'art/raw/kitchen-fitted-galley-2026-10-17-v20')
const draft = path.join(root, 'art/drafts/kitchen-fitted-galley-2026-10-17-v20')
const pageFile = path.join(root, 'public/keeper-review/kitchen-fitted-galley-v20/index.html')
const archiveFile = path.join(root, 'review-archive/sets/kitchen-fitted-galley-v20.json')
const sha = file => crypto.createHash('sha256').update(fs.readFileSync(file)).digest('hex')
const png = file => PNG.sync.read(fs.readFileSync(file))
const pixel = (image, x, y) => Array.from(image.data.subarray((y * image.width + x) * 4, (y * image.width + x) * 4 + 4))
const data = JSON.parse(fs.readFileSync(path.join(draft, 'review-data.json'), 'utf8'))
const register = JSON.parse(fs.readFileSync(path.join(draft, 'batch-register.json'), 'utf8'))
const page = fs.readFileSync(pageFile, 'utf8')

const pins = {
  'isolated-six-appearance-source.png': '971cb7d0047c380fbdf1561a06e8d64dcef1e6b20327ec0c0263ebaa49c9db81',
  'three-bay-fitted-run-source.png': 'b1af0ccf926adb6b24b0596eeeac056ff1b32ab14e7ab87560ee7ba44fad3b9a',
  'isolated-six-appearance-grid.png': '2348325e75d82f09116914b774de084e19d2f52728d19db3edb4e1aaacb9a88d',
  'three-bay-fitted-room.png': '5730e51c07c3c0baa38fbc537fc542179ea427bf0870eff0576e6fad5d8a7a57',
}
for (const [file, expected] of Object.entries(pins)) {
  const folder = file.includes('-source') ? source : raw
  assert.equal(sha(path.join(folder, file)), expected, `${file} changed outside the reviewed V20 build`)
}
assert.equal(data.version, 20)
assert.equal(data.status, 'review-only-fitted-galley-gate')
assert.deepEqual(data.grid, {
  pixelsPerLp: 4,
  bayLp: 21,
  bayPx: 84,
  roomLp: [63, 56],
  roomPx: [252, 224],
  footLineLp: 52,
  foregroundLp: 4,
})
assert.equal(data.physicalScale.cabinetCm, 60)
assert.equal(data.physicalScale.kettle.cm, 18)
assert.ok(Math.abs(data.physicalScale.kettle.calculatedLp - 6.3) < 1e-10)
assert.equal(data.physicalScale.kettle.targetLp, 7)
assert.equal(data.physicalScale.toaster.cm, 28)
assert.ok(Math.abs(data.physicalScale.toaster.calculatedLp - 9.8) < 1e-10)
assert.equal(data.physicalScale.toaster.targetLp, 10)
assert.deepEqual(data.construction.sharedAcrossWholeRun, ['worktop', 'highlight', 'fascia', 'plinth'])
assert.equal(data.construction.outerCapsOnly, true)
for (const key of ['approved', 'promoted', 'runtimeChanged', 'finalChanged', 'keeperChanged', 'fullStateFamilyBuilt']) {
  assert.equal(register[key], false, `${key} must remain false`)
}

const sheet = png(path.join(raw, 'isolated-six-appearance-grid.png'))
const room = png(path.join(raw, 'three-bay-fitted-room.png'))
assert.deepEqual([sheet.width, sheet.height], [324, 240])
assert.deepEqual([room.width, room.height], [252, 224])

// Each appearance has a fully transparent cell boundary and an exact 84-pixel
// visible width.  This catches source bleed and any loss of the 21-lp bay lock.
for (let index = 0; index < 6; index++) {
  const cellX = (index % 3) * 108
  const cellY = Math.floor(index / 3) * 120
  const xs = []
  const ys = []
  for (let y = 0; y < 120; y++) {
    for (let x = 0; x < 108; x++) {
      const alpha = pixel(sheet, cellX + x, cellY + y)[3]
      if (x === 0 || x === 107 || y === 0 || y === 119) assert.equal(alpha, 0, `cell ${index + 1} touches a shared boundary`)
      if (alpha >= 8) { xs.push(x); ys.push(y) }
    }
  }
  assert.equal(Math.max(...xs) - Math.min(...xs) + 1, 84, `cell ${index + 1} lost its exact 21-lp appearance width`)
  assert.ok(Math.min(...xs) >= 12 && 107 - Math.max(...xs) >= 12, `cell ${index + 1} lost its horizontal safety gutter`)
}

function coralWidth(cellX, cellY) {
  const xs = []
  for (let y = 0; y < 120; y++) for (let x = 0; x < 108; x++) {
    const [r, g, b, a] = pixel(sheet, cellX + x, cellY + y)
    if (a > 80 && r > 140 && r > g * 1.25 && r > b * 1.35) xs.push(x)
  }
  return Math.max(...xs) - Math.min(...xs) + 1
}
assert.ok(coralWidth(216, 0) >= 26 && coralWidth(216, 0) <= 30, 'kettle must remain approximately 7 lp wide')
assert.ok(coralWidth(0, 120) >= 36 && coralWidth(0, 120) <= 40, 'toaster must remain approximately 10 lp wide')

// The joined proof uses a real three-bay room and leaves the final 4 lp as
// clear foreground floor.  No storm-blue cabinet pixel may intrude there.
for (let y = 208; y < 224; y++) for (let x = 0; x < 252; x++) {
  const [r, g, b] = pixel(room, x, y)
  assert.ok(!(b > r * 1.3 && b > g * 1.05), `cabinet intrudes into foreground at ${x},${y}`)
}

// Both internal bay seams remain inside one cyan worktop.  This permanent test
// specifically rejects the old split/dollhouse construction at x=84/168.
for (const x of [83, 84, 167, 168]) for (const y of [137, 138, 139, 140]) {
  const [r, g, b] = pixel(room, x, y)
  assert.ok(g > 120 && b > 120 && g > r * 1.05, `continuous worktop breaks at ${x},${y}`)
}

assert.match(page, /one continuous worktop, highlight, fascia and recessed plinth/i)
assert.match(page, /60 cm = 21 lp = 84 source px/)
assert.match(page, /Kettle.*18 cm = 6.3 lp/s)
assert.match(page, /Toaster.*28 cm = 9.8 lp/s)
assert.match(page, /does not approve, promote or wire kitchen art/i)
assert.ok(page.includes(data.images.appearanceSheet))
assert.ok(page.includes(data.images.roomProof))

if (fs.existsSync(archiveFile)) {
  const archive = JSON.parse(fs.readFileSync(archiveFile, 'utf8'))
  assert.equal(Object.keys(archive.entries).length, 2)
  for (const record of Object.values(archive.entries)) {
    assert.equal(sha(path.join(root, record.object)), record.sha256)
  }
}

console.log('Kitchen V20 fitted-galley appearance and construction gate verified')
