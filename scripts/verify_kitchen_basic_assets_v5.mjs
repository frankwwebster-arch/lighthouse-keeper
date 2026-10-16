import assert from 'node:assert/strict'
import crypto from 'node:crypto'
import fs from 'node:fs'
import path from 'node:path'
import { PNG } from 'pngjs'

const root = process.cwd()
const rawDir = path.join(root, 'art/raw/kitchen-basic-assets-2026-10-16-v5')
const sourceDir = path.join(root, 'art/source/kitchen-basic-assets-2026-10-16-v5')
const draftDir = path.join(root, 'art/drafts/kitchen-basic-assets-2026-10-16-v5')
const publicDir = path.join(root, 'public/keeper-review/kitchen-basic-assets-v5')
const pageFile = path.join(publicDir, 'index.html')
const setFile = path.join(root, 'review-archive/sets/kitchen-basic-assets-v5.json')

const readJson = (file) => JSON.parse(fs.readFileSync(file, 'utf8'))
const sha = (file) => crypto.createHash('sha256').update(fs.readFileSync(file)).digest('hex')
const png = (file) => PNG.sync.read(fs.readFileSync(file))
const catalogue = readJson(path.join(draftDir, 'asset-catalogue.json'))
const register = readJson(path.join(draftDir, 'batch-register.json'))
const archiveSet = readJson(setFile)
const page = fs.readFileSync(pageFile, 'utf8')

assert.equal(catalogue.version, 5)
assert.equal(catalogue.status, 'reversible-draft')
assert.equal(catalogue.density, 4)
assert.deepEqual(catalogue.projection, {
  id: 'flat-cutaway-v1', runtimeDepthScaling: false, camera: 'straight-on', vanishingPoint: false,
})
assert.deepEqual(catalogue.room, {
  doorDatumLp: 4, bayLp: 21, heightLp: 56, floorBandLp: 5, footLineLp: 56,
  widthsLp: { 9: 193, 12: 256 },
})
assert.equal(Object.keys(catalogue.assets).length, 10)

assert.equal(register.supersedesForReviewOnly, 'kitchen-basic-assets-v4')
assert.equal(register.status, 'reversible-draft')
assert.equal(register.projection.id, 'flat-cutaway-v1')
assert.equal(register.projection.runtimeDepthScaling, false)
assert.equal(register.projection.frontFace, 'true-rectangle')
assert.equal(register.projection.floorBandLp, 5)
assert.equal(register.projection.rearEdgeScale, 1)
assert.equal(register.geometryChanges.oneBayArtWidthLp, 20)
assert.equal(register.geometryChanges.safetyGutterLpEachSide, 0.5)
assert.equal(register.geometryChanges.worktopHobTableLp, 19)
assert.equal(register.geometryChanges.chairSeatLp, 11)
assert.equal(register.geometryChanges.confirmedRearSeatContactLp, 10.67)
assert.equal(register.geometryChanges.cupboardView, 'right-side wall; closed leaf edge-on')
assert.deepEqual(register.geometryChanges.cupboardProjectedWidthsLp, [1, 8, 22, 34])
assert.equal(register.geometryChanges.doorRemainsOpenDuringActivity, true)
assert.equal(register.geometryChanges.doorClosesAfterStandardWalkExitClear, true)
assert.equal(register.geometryChanges.broomTurnClipRequired, false)
assert.equal(register.geometryChanges.genericSeatedBackArmClipAvailable, false)

const exactSizes = new Map([
  ['room_kitchen_repeat_a.png', [21, 56]],
  ['room_kitchen_repeat_b.png', [21, 56]],
  ['room_kitchen_repeat_c.png', [21, 56]],
  ['room_kitchen_stair_cap.png', [46, 56]],
  ['room_kitchen_far_cap_closed.png', [38, 56]],
  ['room_kitchen_far_cap_open.png', [38, 56]],
  ['obj_table_chair_back_f1.png', [42, 28]],
  ['obj_table_foreground_f1.png', [42, 28]],
  ['room_kitchen_9bay_composite.png', [193, 56]],
  ['room_kitchen_12bay_outline.png', [256, 56]],
])
for (let bays = 6; bays <= 12; bays += 1) exactSizes.set(`room_kitchen_shell_${bays}bay.png`, [4 + bays * 21, 56])
for (const [name, [logicalW, logicalH]] of exactSizes) {
  const image = png(path.join(rawDir, name))
  assert.deepEqual([image.width, image.height], [logicalW * 4, logicalH * 4], `${name} density-4 geometry`)
}

for (const [stem, asset] of Object.entries(catalogue.assets)) {
  assert.equal(asset.projection.id, 'flat-cutaway-v1', `${stem} projection`)
  assert.equal(asset.projection.frontFace, 'true-rectangle', `${stem} front face`)
  assert.equal(asset.projection.rearEdgeScale, 1, `${stem} no rear narrowing`)
  assert.equal(asset.projection.runtimeDepthScaling, false, `${stem} no runtime depth scaling`)
  assert.ok(asset.topRevealLp <= (stem === 'obj_table' ? 3 : 2), `${stem} top-reveal limit`)
  for (const [state, value] of Object.entries(asset.states)) {
    const image = png(path.join(root, value.png))
    const { w, h, frames, density } = value.meta
    assert.equal(density, 4, `${stem}/${state} density`)
    assert.deepEqual([image.width, image.height], [w * density * frames, h * density], `${stem}/${state} strip geometry`)
    for (let frame = 0; frame < frames; frame += 1) {
      const left = frame * w * density
      const right = left + w * density - 1
      for (let y = 0; y < image.height; y += 1) {
        assert.equal(image.data[(y * image.width + left) * 4 + 3], 0, `${stem}/${state} f${frame + 1} left gutter`)
        assert.equal(image.data[(y * image.width + right) * 4 + 3], 0, `${stem}/${state} f${frame + 1} right gutter`)
      }
    }
  }
}

for (const stem of ['obj_bin', 'obj_fridge', 'obj_kettle', 'obj_toaster', 'obj_cooker', 'obj_mixer', 'obj_sink']) {
  assert.equal(catalogue.assets[stem].largestBound.widthLp, 20, `${stem} fills usable bay width`)
}
assert.equal(catalogue.assets.obj_fridge.label, 'Freestanding under-counter fridge')
assert.equal(catalogue.assets.obj_fridge.largestBound.heightLp, 19)
assert.equal(catalogue.assets.obj_cooker.frontRectLp.height, 19)
assert.equal(catalogue.assets.obj_cooker.frontRectLp.width, 20)
assert.equal(catalogue.assets.obj_table.bays, 2)
assert.deepEqual(catalogue.assets.obj_table.frontRectLp, { width: 40, height: 19 })
assert.equal(catalogue.assets.obj_table.states.standard.meta.contactDatumsLp.table, undefined)
assert.equal(catalogue.assets.obj_table.states.standard.meta.contactDatumsLp.worktopOrTable, 19)
assert.equal(catalogue.assets.obj_table.states.standard.meta.contactDatumsLp.seat, 11)
assert.equal(catalogue.assets.obj_petbowl.largestBound.widthLp, 12)
assert.equal(catalogue.assets.obj_petbowl.largestBound.heightLp, 3)

// The generated room source's angled floor is excluded: all three repeat
// variants end in one identical, exactly 20-source-pixel (5-lp) flat band.
const repeats = ['a', 'b', 'c'].map((v) => png(path.join(rawDir, `room_kitchen_repeat_${v}.png`)))
const floorBytes = (image) => {
  const start = (image.height - 20) * image.width * 4
  return image.data.subarray(start)
}
assert.deepEqual(Buffer.from(floorBytes(repeats[0])), Buffer.from(floorBytes(repeats[1])))
assert.deepEqual(Buffer.from(floorBytes(repeats[0])), Buffer.from(floorBytes(repeats[2])))
assert.notDeepEqual(Buffer.from(repeats[0].data.subarray((repeats[0].height - 21) * repeats[0].width * 4, (repeats[0].height - 20) * repeats[0].width * 4)), Buffer.from(repeats[0].data.subarray((repeats[0].height - 20) * repeats[0].width * 4, (repeats[0].height - 19) * repeats[0].width * 4)))

const door = catalogue.assets.obj_cupboard
assert.deepEqual(door.states.on.meta.projectedWidthLp, [1, 8, 22, 34])
assert.deepEqual(door.states.on.meta.realLeafSizeLp, [34, 52])
assert.equal(door.states.on.meta.hingeXLp, 37)
assert.equal(door.states.on.meta.hingeSide, 'right')
assert.equal(door.states.on.meta.opens, 'left')
for (const bound of door.states.on.bounds) assert.equal(bound.heightLp, 52, 'door height is invariant during rotation')
assert.deepEqual(door.states.on.bounds.map((b) => b.widthLp), [1, 8, 22, 34])
const openLeaf = png(path.join(rawDir, 'obj_cupboard_open_f1.png'))
for (let y = 16; y < 224; y += 1) {
  let left = openLeaf.width; let right = -1
  for (let x = 0; x < openLeaf.width; x += 1) {
    if (openLeaf.data[(y * openLeaf.width + x) * 4 + 3] > 0) { left = Math.min(left, x); right = Math.max(right, x) }
  }
  assert.deepEqual([left, right], [12, 147], `open rectangular leaf row ${y}`)
}

assert.match(page, /Kitchen basic assets V5/)
assert.match(page, /flat-cutaway-v1/)
assert.match(page, /Preloading and decoding every unique review image/)
assert.match(page, /Promise\.all\(uniq\.map/)
assert.match(page, /i\.decode/)
assert.match(page, /4× authoring scale/)
assert.match(page, /Same raster in three bays/)
assert.match(page, /show 1-lp shallow top cue/)
assert.match(page, /Keeper scale beside every major asset/)
assert.match(page, /table 19 lp/)
assert.match(page, /seat 11 lp/)
assert.match(page, /chair is nearest the player\/camera in floor placement[\s\S]*table apron is foreground/)
assert.match(page, /right side wall/i)
assert.match(page, /hinged on the right and extending left/i)
assert.match(page, /34×52-lp fully open rectangle hides/)
assert.match(page, /closes only after he is clear/)
assert.match(page, /19-lp oven door/)
assert.match(page, /both existing rear retrieval clips still read/)
assert.match(page, /generic seated arm overlay/)

assert.equal(archiveSet.set, 'kitchen-basic-assets-v5')
assert.equal(archiveSet.page.path, 'public/keeper-review/kitchen-basic-assets-v5/index.html')
assert.equal(archiveSet.page.sha256, sha(pageFile))
assert.ok(Object.keys(archiveSet.entries).length >= 100)
assert.equal(fs.existsSync(path.join(publicDir, 'assets')), false, 'review media must be archived, not public')

for (const item of [...register.inputs, ...register.outputs]) {
  const absolute = path.join(root, item.path)
  if (fs.existsSync(absolute)) {
    assert.equal(sha(absolute), item.sha256, `registered hash changed: ${item.path}`)
  } else {
    const route = item.path.startsWith('public/') ? `/${item.path.slice('public/'.length)}` : null
    assert.ok(route && archiveSet.entries[route], `registered output missing: ${item.path}`)
    assert.equal(archiveSet.entries[route].sha256, item.sha256, `archive hash mismatch: ${item.path}`)
  }
}

for (const file of [
  'generated/flat_kitchen_run_sheet.png',
  'generated/flat_mixer_unit_source.png',
  'generated/flat_room_shell_source.png',
  'generated/flat_table_chair_bin_bowl_sheet.png',
  'generated/flat_cupboard_leaf_source.png',
  'reference/approved_flat_room_mockup.png',
]) assert.ok(fs.existsSync(path.join(sourceDir, file)), `${file} missing`)

for (const item of register.outputs) {
  assert.doesNotMatch(item.path, /^public\/sprites\//, 'V5 must not write runtime sprites')
  assert.doesNotMatch(item.path, /manifest|register/i, 'V5 must not write runtime manifests/registers')
}

console.log(JSON.stringify({
  set: archiveSet.set,
  assets: Object.keys(catalogue.assets).length,
  archivedReviewMedia: Object.keys(archiveSet.entries).length,
  projection: 'flat-cutaway-v1',
  floorBandLp: 5,
  roomWidthsLp: [193, 256],
  worktopTableLp: 19,
  chairSeatLp: 11,
  cupboard: 'right-side wall; edge-on closed; rectangular foreground leaf open',
  runtimeChanged: false,
  status: 'verified',
}, null, 2))
