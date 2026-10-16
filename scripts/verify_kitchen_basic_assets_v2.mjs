import assert from 'node:assert/strict'
import crypto from 'node:crypto'
import fs from 'node:fs'
import path from 'node:path'
import { PNG } from 'pngjs'

const root = process.cwd()
const rawDir = path.join(root, 'art/raw/kitchen-basic-assets-2026-10-16-v2')
const sourceDir = path.join(root, 'art/source/kitchen-basic-assets-2026-10-16-v2')
const draftDir = path.join(root, 'art/drafts/kitchen-basic-assets-2026-10-16-v2')
const publicDir = path.join(root, 'public/keeper-review/kitchen-basic-assets-v2')
const pageFile = path.join(publicDir, 'index.html')
const setFile = path.join(root, 'review-archive/sets/kitchen-basic-assets-v2.json')

const readJson = (file) => JSON.parse(fs.readFileSync(file, 'utf8'))
const sha = (file) => crypto.createHash('sha256').update(fs.readFileSync(file)).digest('hex')
const png = (file) => PNG.sync.read(fs.readFileSync(file))

const catalogue = readJson(path.join(draftDir, 'asset-catalogue.json'))
const register = readJson(path.join(draftDir, 'batch-register.json'))
const archiveSet = readJson(setFile)
const page = fs.readFileSync(pageFile, 'utf8')

assert.equal(catalogue.version, 2)
assert.equal(catalogue.status, 'reversible-draft')
assert.equal(catalogue.density, 4)
assert.equal(Object.keys(catalogue.assets).length, 10)
assert.deepEqual(catalogue.room, {
  doorClearLp: 4,
  bayLp: 21,
  heightLp: 56,
  widthsLp: { 9: 193, 12: 256 },
})

assert.equal(register.status, 'reversible-draft')
assert.equal(register.supersedesForReviewOnly, 'kitchen-basic-assets-v1')
assert.deepEqual(register.geometryChanges, {
  chairSeatLp: 11,
  confirmedSeatContactLp: 10.61,
  tableSurfaceLp: 17,
  tableUndersideLp: 15,
  cupboardLeaf: '32 lp wide, floor-to-lintel, no foot gap',
})

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
for (let bays = 6; bays <= 12; bays += 1) {
  exactSizes.set(`room_kitchen_shell_${bays}bay.png`, [4 + bays * 21, 56])
}
for (const [name, [logicalW, logicalH]] of exactSizes) {
  const image = png(path.join(rawDir, name))
  assert.deepEqual([image.width, image.height], [logicalW * 4, logicalH * 4], `${name} density-4 geometry`)
}

for (const [stem, asset] of Object.entries(catalogue.assets)) {
  for (const [state, value] of Object.entries(asset.states)) {
    const image = png(path.join(root, value.png))
    const { w, h, frames, density } = value.meta
    assert.equal(density, 4, `${stem}/${state} density`)
    assert.deepEqual([image.width, image.height], [w * density * frames, h * density], `${stem}/${state} strip geometry`)
    for (let frame = 0; frame < frames; frame += 1) {
      const left = frame * w * density
      const right = left + w * density - 1
      for (let y = 0; y < image.height; y += 1) {
        assert.equal(image.data[(y * image.width + left) * 4 + 3], 0, `${stem}/${state} frame ${frame + 1} left gutter`)
        assert.equal(image.data[(y * image.width + right) * 4 + 3], 0, `${stem}/${state} frame ${frame + 1} right gutter`)
      }
    }
  }
}

const fridge = catalogue.assets.obj_fridge
assert.equal(fridge.bays, 1)
assert.ok(fridge.states.standard.bounds[0].widthLp >= 15, 'freestanding fridge must retain a readable appliance silhouette')
assert.equal(catalogue.assets.obj_table.bays, 2)
assert.equal(catalogue.assets.obj_table.interactionOffsetKu, -84)
assert.equal(catalogue.assets.obj_petbowl.bays, 0)

const closedCupboard = catalogue.assets.obj_cupboard.states.standard.bounds[0]
assert.equal(closedCupboard.widthLp, 34)
assert.equal(closedCupboard.heightLp, 52)
assert.equal(closedCupboard.yLp + closedCupboard.heightLp, 56, 'closed cupboard must reach the floor')
assert.equal(catalogue.assets.obj_cupboard.interactionOffsetKu, -84)

assert.match(page, /Reversible smooth-style redraft · V1 preserved/)
assert.match(page, /Promise\.all\(uniq\.map/)
assert.match(page, /i\.decode/)
assert.match(page, /room_kitchen_shell_12bay_frame1\.png/)
assert.match(page, /Under-counter fridge/)
assert.match(page, /10\.61 lp above floor/)
assert.match(page, /table surface is now <strong>17 lp<\/strong>/)
assert.match(page, /fully hidden—including boots and tool/i)
assert.match(page, /hiddenKeeper'\)\.src=DATA\.keeper\.keeper_sweep_broom/)
assert.match(page, /cupB'\)\.src=DATA\.cupboardClosed/)
assert.match(page, /19-lp door/)
assert.match(page, /keeper_cake_from_oven_back/)
assert.match(page, /keeper_meal_from_oven_back/)
assert.match(page, /both existing retrieval clips still read/)
assert.match(page, /document\.querySelectorAll\('button,select'\).*disabled=false/)

assert.equal(archiveSet.set, 'kitchen-basic-assets-v2')
assert.equal(archiveSet.page.path, 'public/keeper-review/kitchen-basic-assets-v2/index.html')
assert.equal(archiveSet.page.sha256, sha(pageFile))
assert.ok(Object.keys(archiveSet.entries).length >= 130)
assert.equal(fs.existsSync(path.join(publicDir, 'assets')), false, 'review media must be archived, not public')

for (const item of [...register.inputs, ...register.outputs]) {
  const absolute = path.join(root, item.path)
  if (fs.existsSync(absolute)) {
    assert.equal(sha(absolute), item.sha256, `registered hash changed: ${item.path}`)
    continue
  }
  const route = item.path.startsWith('public/') ? `/${item.path.slice('public/'.length)}` : null
  assert.ok(route && archiveSet.entries[route], `registered file missing: ${item.path}`)
  assert.equal(archiveSet.entries[route].sha256, item.sha256, `archive hash mismatch: ${item.path}`)
}

for (const file of [
  'generated/obj_fridge_standard_source.png',
  'rejected/obj_fridge_integrated_rejected_source.png',
  'reference/kitchen-furniture-concept-v1.png',
  'reference/kitchen-shell-concept-v1.png',
]) {
  assert.ok(fs.existsSync(path.join(sourceDir, file)), `${file} missing`)
}

console.log(JSON.stringify({
  set: archiveSet.set,
  assets: Object.keys(catalogue.assets).length,
  rawPngs: fs.readdirSync(rawDir).filter((name) => name.endsWith('.png')).length,
  archivedReviewMedia: Object.keys(archiveSet.entries).length,
  roomWidthsLp: [193, 256],
  seatContactLp: 10.61,
  tableSurfaceLp: 17,
  cupboardOcclusion: 'full-height closed leaf',
  fridge: 'freestanding',
  status: 'verified',
}, null, 2))
