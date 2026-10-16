import assert from 'node:assert/strict'
import crypto from 'node:crypto'
import fs from 'node:fs'
import path from 'node:path'
import { PNG } from 'pngjs'

const root = process.cwd()
const raw = path.join(root, 'art/raw/kitchen-basic-assets-2026-10-16-v6-calibration')
const draft = path.join(root, 'art/drafts/kitchen-basic-assets-2026-10-16-v6-calibration')
const v5 = path.join(root, 'art/raw/kitchen-basic-assets-2026-10-16-v5')
const pageFile = path.join(root, 'public/keeper-review/kitchen-countertop-calibration-v6/index.html')
const archiveFile = path.join(root, 'review-archive/sets/kitchen-countertop-calibration-v6.json')
const readJson = file => JSON.parse(fs.readFileSync(file, 'utf8'))
const sha = file => crypto.createHash('sha256').update(fs.readFileSync(file)).digest('hex')
const treeSha = directory => {
  const files = []
  const visit = current => {
    for (const entry of fs.readdirSync(current, { withFileTypes: true })) {
      const absolute = path.join(current, entry.name)
      if (entry.isDirectory()) visit(absolute)
      else if (entry.isFile()) files.push(absolute)
    }
  }
  visit(directory)
  const digest = crypto.createHash('sha256')
  for (const file of files.sort()) {
    digest.update(path.relative(directory, file).split(path.sep).join('/'))
    digest.update('\0')
    digest.update(fs.readFileSync(file))
    digest.update('\0')
  }
  return digest.digest('hex')
}
const png = file => PNG.sync.read(fs.readFileSync(file))
const data = readJson(path.join(draft, 'calibration-data.json'))
const register = readJson(path.join(draft, 'batch-register.json'))
const page = fs.readFileSync(pageFile, 'utf8')

assert.equal(data.version, 6)
assert.equal(data.status, 'review-only-calibration-gate')
assert.deepEqual(data.unitOrder, ['obj_kettle', 'obj_cooker', 'obj_sink'])
assert.deepEqual(Object.keys(data.options), ['a', 'b', 'c'])
assert.equal(register.soleVisualBaseline, 'Kitchen Basic Assets V5')
assert.equal(register.readsFormerV6, false)
assert.equal(register.fullFamilyRebuilt, false)
assert.equal(register.runtimeChanged, false)
assert.equal(register.finalChanged, false)
assert.equal(register.keeperChanged, false)

const specs = {
  obj_kettle: { file: 'obj_kettle_standard_f1.png', size: [84, 124], mask: [0, 40, 84, 56], logical: [21, 31], frontY: 48 },
  obj_cooker: { file: 'obj_cooker_standard_f1.png', size: [84, 112], mask: [0, 20, 84, 36], logical: [21, 28], frontY: 32 },
  obj_sink: { file: 'obj_sink_standard_f1.png', size: [84, 116], mask: [0, 40, 84, 56], logical: [21, 29], frontY: 48 },
}
const depth = { a: 4, b: 6, c: 8 }

const pixel = (image, x, y) => {
  const i = (y * image.width + x) * 4
  return image.data.subarray(i, i + 4)
}
const samePixel = (a, b, x, y) => pixel(a, x, y).every((v, i) => v === pixel(b, x, y)[i])

for (const [key, option] of Object.entries(data.options)) {
  assert.equal(option.construction.edgeLengthLp, 20)
  assert.equal(option.construction.shearLp, 0)
  assert.equal(option.construction.fasciaLp, 2)
  assert.equal(option.construction.rearEdgeScale, 1)
  assert.equal(option.topRevealLp, depth[key] / 4)
  for (const stem of data.unitOrder) {
    const spec = specs[stem]
    const record = option.units[stem]
    const originalFile = path.join(v5, spec.file)
    const candidateFile = path.join(raw, `${stem}_option_${key}_candidate.png`)
    assert.equal(record.v5Sha256, sha(originalFile))
    assert.equal(record.candidateSha256, sha(candidateFile))
    assert.deepEqual(record.logical, spec.logical)
    assert.deepEqual(record.declaredChangeMaskPx, spec.mask)
    const original = png(originalFile)
    const candidate = png(candidateFile)
    assert.deepEqual([candidate.width, candidate.height], spec.size)

    const [x0, y0, x1, y1] = spec.mask
    let changed = 0
    for (let y = 0; y < candidate.height; y++) {
      for (let x = 0; x < candidate.width; x++) {
        const same = samePixel(original, candidate, x, y)
        if (!same) changed++
        if (x < x0 || x >= x1 || y < y0 || y >= y1) assert.ok(same, `${stem}/${key} changed outside countertop mask at ${x},${y}`)
      }
      assert.equal(pixel(candidate, 0, y)[3], 0, `${stem}/${key} left safety edge is opaque`)
      assert.equal(pixel(candidate, candidate.width - 1, y)[3], 0, `${stem}/${key} right safety edge is opaque`)
    }
    assert.ok(changed > 0)

    const rearY = spec.frontY - depth[key]
    for (let x = 2; x <= 81; x++) {
      assert.ok(pixel(candidate, x, rearY)[3] > 0, `${stem}/${key} rear edge is not a full 20-lp run`)
      assert.ok(pixel(candidate, x, spec.frontY - 1)[3] > 0, `${stem}/${key} front edge is not a full 20-lp run`)
    }
  }
  const seam = png(path.join(raw, `ordinary_counter_seam_option_${key}.png`))
  assert.deepEqual([seam.width, seam.height], [168, 124])
}

assert.ok(page.includes('native 4× authoring scale'))
assert.ok(page.includes('Exact logical game scale'))
assert.ok(page.includes('V5 sole baseline'))
assert.ok(page.includes('0.5-lp transparent gutter'))
assert.ok(page.includes('SHA-256 and protected surfaces'))
assert.ok(page.includes('Promise.all'))
assert.ok(page.includes('.decode'))
assert.ok(page.includes('Animated states are deliberately not rebuilt'))

for (const [name, expected] of Object.entries(register.protectedSnapshots)) {
  assert.match(expected, /^[a-f0-9]{64}$/, `invalid protected snapshot ${name}`)
}
assert.equal(register.protectedSnapshots.kitchenV5, treeSha(v5), 'Kitchen V5 changed after calibration build')
assert.equal(register.protectedSnapshots.runtimeSpriteManifest, sha(path.join(root, 'public/sprites/manifest.json')), 'runtime sprite manifest changed')
assert.equal(register.protectedSnapshots.animationWorkbenchFinalState, sha(path.join(root, 'data/keeper_animation_workbench.json')), 'animation workbench/Final state changed')
assert.equal(register.protectedSnapshots.approvedKeeperSourceFamily, treeSha(path.join(root, 'art/raw/keeper-first-batch')), 'approved Keeper source family changed')

assert.ok(fs.existsSync(archiveFile), 'content-addressed review archive set is missing')
const archive = readJson(archiveFile)
for (const option of Object.values(data.options)) {
  for (const unit of Object.values(option.units)) {
    for (const key of ['v5', 'candidate', 'ghost', 'edges']) assert.ok(archive.entries[unit[key]], `archive missing ${unit[key]}`)
  }
  assert.ok(archive.entries[option.seam], `archive missing ${option.seam}`)
}

assert.ok(!fs.existsSync(path.join(root, 'public/keeper-review/kitchen-countertop-calibration-v6/assets')), 'public review binaries must be archived')
console.log('Kitchen V6 countertop calibration verified: 3 options × 3 exact V5-derived units; room-grid gutters retained; runtime unchanged.')
