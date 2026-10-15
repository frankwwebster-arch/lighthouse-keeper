import assert from 'node:assert/strict'
import crypto from 'node:crypto'
import fs from 'node:fs'
import path from 'node:path'
import { PNG } from 'pngjs'

const root = process.cwd()
const rawDir = path.join(root, 'art/raw/kitchen-basic-assets-2026-10-16-v1')
const sourceDir = path.join(root, 'art/source/kitchen-basic-assets-2026-10-16-v1')
const draftDir = path.join(root, 'art/drafts/kitchen-basic-assets-2026-10-16-v1')
const publicDir = path.join(root, 'public/keeper-review/kitchen-basic-assets-v1')
const pageFile = path.join(publicDir, 'index.html')
const setFile = path.join(root, 'review-archive/sets/kitchen-basic-assets-v1.json')

const readJson = (file) => JSON.parse(fs.readFileSync(file, 'utf8'))
const sha = (file) => crypto.createHash('sha256').update(fs.readFileSync(file)).digest('hex')
const png = (file) => PNG.sync.read(fs.readFileSync(file))

const catalogue = readJson(path.join(draftDir, 'asset-catalogue.json'))
const register = readJson(path.join(draftDir, 'batch-register.json'))
const archiveSet = readJson(setFile)
const page = fs.readFileSync(pageFile, 'utf8')

assert.equal(catalogue.status, 'reversible-tier-1-draft-awaiting-frank-review')
assert.deepEqual(catalogue.room, {
  heightLp: 56,
  doorDirectionProposal: 'outward-into-stairwell',
  doorClearLp: 4,
  doorClearKu: 32,
  startBays: 9,
  startWidthLp: 193,
  startWidthKu: 1544,
  maxBays: 12,
  maxWidthLp: 256,
  maxWidthKu: 2048,
  repeatSectionLp: [21, 56],
  repeatSectionKu: [168, 448],
})
assert.equal(catalogue.layout9.obj_petbowl.interactionXKu, 1376)
assert.equal(catalogue.layout9.obj_petbowl.bays.length, 0)
assert.match(catalogue.layout9.obj_petbowl.choice, /foreground.*moves with table.*no bay/i)
assert.equal(catalogue.layout9.obj_cupboard.interactionXKu, 1460)
assert.equal(catalogue.layout12.obj_cupboardInteractionXKu, 1964)

const exactSizes = new Map([
  ['room_kitchen_repeat_a.png', [21, 56]],
  ['room_kitchen_repeat_b.png', [21, 56]],
  ['room_kitchen_repeat_c.png', [21, 56]],
  ['room_kitchen_stair_cap_outward_closed.png', [46, 56]],
  ['room_kitchen_stair_cap_outward_open.png', [46, 56]],
  ['room_kitchen_far_cap_closed.png', [38, 56]],
  ['room_kitchen_far_cap_open.png', [38, 56]],
  ['room_kitchen_9bay_composite.png', [193, 56]],
  ['room_kitchen_12bay_outline.png', [256, 56]],
])
for (let bays = 6; bays <= 12; bays += 1) exactSizes.set(`room_kitchen_shell_${bays}bay.png`, [4 + bays * 21, 56])
for (const [name, expected] of exactSizes) {
  const image = png(path.join(rawDir, name))
  assert.deepEqual([image.width, image.height], expected, `${name} geometry`)
}

const specs = {
  obj_fridge: { cell: 21, max: [21, 19] },
  obj_kettle: { cell: 21, max: [21, 30] },
  obj_toaster: { cell: 21, max: [21, 30] },
  obj_cooker: { cell: 21, max: [21, 26] },
  obj_mixer: { cell: 21, max: [21, 30] },
  obj_sink: { cell: 21, max: [21, 27] },
  obj_table: { cell: 42, max: [42, 26] },
  obj_bin: { cell: 21, max: [21, 14] },
  obj_petbowl: { cell: 16, max: [12, 3] },
}

function bounds(image, x0, x1) {
  let minX = x1; let minY = image.height; let maxX = -1; let maxY = -1
  for (let y = 0; y < image.height; y += 1) {
    for (let x = x0; x < x1; x += 1) {
      if (image.data[(y * image.width + x) * 4 + 3] > 0) {
        minX = Math.min(minX, x); minY = Math.min(minY, y)
        maxX = Math.max(maxX, x); maxY = Math.max(maxY, y)
      }
    }
  }
  return maxX < 0 ? null : { width: maxX - minX + 1, height: maxY - minY + 1 }
}

for (const file of fs.readdirSync(rawDir).filter((name) => /^obj_.*\.png$/.test(name) && !name.includes('dishes'))) {
  const stem = Object.keys(specs).find((candidate) => file.startsWith(`${candidate}_`))
  if (!stem) continue
  const spec = specs[stem]
  const image = png(path.join(rawDir, file))
  const frames = file.endsWith('_f4.png') ? 4 : 1
  assert.equal(image.width, spec.cell * frames, `${file} strip width`)
  for (let frame = 0; frame < frames; frame += 1) {
    const left = frame * spec.cell
    const right = left + spec.cell - 1
    for (let y = 0; y < image.height; y += 1) {
      assert.equal(image.data[(y * image.width + left) * 4 + 3], 0, `${file} frame ${frame + 1} left gutter`)
      assert.equal(image.data[(y * image.width + right) * 4 + 3], 0, `${file} frame ${frame + 1} right gutter`)
    }
    const box = bounds(image, left, left + spec.cell)
    assert.ok(box.width <= spec.max[0] && box.height <= spec.max[1], `${file} frame ${frame + 1} exceeds max: ${JSON.stringify(box)}`)
  }
}

assert.equal(catalogue.objects.obj_cooker.measuredStandardBoundsLp.width, 19)
assert.match(catalogue.objects.obj_cooker.note, /oven door exactly 19 lp/)
assert.equal(catalogue.objects.obj_table.interactionOffsetKu, -84)
assert.equal(catalogue.objects.obj_petbowl.bays, 0)

assert.match(page, /Reversible tier-1 draft · nothing approved, promoted or wired/)
assert.match(page, /Promise\.all\(ALL_URLS\.map/)
assert.match(page, /img\.decode\(\)/)
assert.match(page, /room_kitchen_shell_.*bay\.png/)
assert.match(page, /\['Pet bowl',172\]/)
assert.match(page, /petbowl-overlay/)
assert.match(page, /z-index:10/)
assert.match(page, /oven-guide/)
assert.match(page, /fully hidden root/i)

assert.equal(archiveSet.set, 'kitchen-basic-assets-v1')
assert.equal(archiveSet.page.path, 'public/keeper-review/kitchen-basic-assets-v1/index.html')
assert.equal(archiveSet.page.sha256, sha(pageFile))
assert.ok(Object.keys(archiveSet.entries).length >= 130)
assert.equal(fs.existsSync(path.join(publicDir, 'assets')), false, 'review media must be archived, not public')

for (const file of register.files) {
  const absolute = path.join(root, file.path)
  if (fs.existsSync(absolute)) {
    assert.equal(sha(absolute), file.sha256, `registered hash changed: ${file.path}`)
    continue
  }
  const route = file.path.startsWith('public/') ? `/${file.path.slice('public/'.length)}` : null
  assert.ok(route && archiveSet.entries[route], `registered file missing: ${file.path}`)
  assert.equal(archiveSet.entries[route].sha256, file.sha256, `archive hash mismatch: ${file.path}`)
}

for (const concept of ['kitchen-furniture-concept-v1.png', 'kitchen-shell-concept-v1.png']) {
  assert.ok(fs.existsSync(path.join(sourceDir, 'reference', concept)), `${concept} source reference missing`)
}

console.log(JSON.stringify({
  set: archiveSet.set,
  rawPngs: fs.readdirSync(rawDir).filter((name) => name.endsWith('.png')).length,
  archivedReviewMedia: Object.keys(archiveSet.entries).length,
  roomWidthsLp: [catalogue.room.startWidthLp, catalogue.room.maxWidthLp],
  petBowlForeground: true,
  status: 'verified',
}, null, 2))
