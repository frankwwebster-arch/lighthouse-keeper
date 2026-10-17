import assert from 'node:assert/strict'
import crypto from 'node:crypto'
import fs from 'node:fs'
import path from 'node:path'
import { PNG } from 'pngjs'

const root = process.cwd()
const raw = path.join(root, 'art/raw/kitchen-countertop-gate-2026-10-17-v18')
const draft = path.join(root, 'art/drafts/kitchen-countertop-gate-2026-10-17-v18')
const v5 = path.join(root, 'art/raw/kitchen-basic-assets-2026-10-16-v5')
const oldGate = path.join(root, 'art/raw/kitchen-basic-assets-2026-10-16-v6-calibration')
const pageFile = path.join(root, 'public/keeper-review/kitchen-countertop-gate-v18/index.html')
const archiveFile = path.join(root, 'review-archive/sets/kitchen-countertop-gate-v18.json')
const readJson = file => JSON.parse(fs.readFileSync(file, 'utf8'))
const png = file => PNG.sync.read(fs.readFileSync(file))
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
const pixel = (image, x, y) => {
  const index = (y * image.width + x) * 4
  return image.data.subarray(index, index + 4)
}
const samePixel = (a, b, x, y) => pixel(a, x, y).every((value, index) => value === pixel(b, x, y)[index])

const data = readJson(path.join(draft, 'gate-data.json'))
const register = readJson(path.join(draft, 'batch-register.json'))
const page = fs.readFileSync(pageFile, 'utf8')

assert.equal(data.version, 18)
assert.equal(data.status, 'review-only-gate')
assert.deepEqual(data.unitOrder, ['obj_kettle', 'obj_cooker', 'obj_sink'])
assert.equal(register.soleVisualBaseline, 'Kitchen Basic Assets V5')
assert.equal(register.historicalCalibrationPixelsReused, false)
assert.deepEqual(register.selectedAbstractConstruction, { option: 'B', topRevealLp: 1.5, fasciaLp: 2, shearLp: 0 })
assert.equal(register.fullFamilyRebuilt, false)
assert.equal(register.roomRebuilt, false)
assert.equal(register.runtimeChanged, false)
assert.equal(register.finalChanged, false)
assert.equal(register.keeperChanged, false)

const specs = {
  obj_kettle: { file: 'obj_kettle_standard_f1.png', size: [84, 124], contactY: 48, structureBottom: 55 },
  obj_cooker: { file: 'obj_cooker_standard_f1.png', size: [84, 112], contactY: 36, structureBottom: 35 },
  obj_sink: { file: 'obj_sink_standard_f1.png', size: [84, 116], contactY: 40, structureBottom: 47 },
}

const structuralErrors = (candidate, structure, appliance, spec) => {
  const errors = []
  const rearY = spec.contactY - 6
  for (let y = 0; y < candidate.height; y++) {
    if (pixel(candidate, 0, y)[3] !== 0 || pixel(candidate, 83, y)[3] !== 0) errors.push(`shared-edge-alpha@${y}`)
  }
  for (let y = rearY; y <= spec.structureBottom; y++) {
    for (let x = 2; x <= 81; x++) {
      if (pixel(structure, x, y)[3] === 0) errors.push(`structure-gap@${x},${y}`)
      if (pixel(appliance, x, y)[3] === 0 && !samePixel(candidate, structure, x, y)) errors.push(`nonsemantic-overwrite@${x},${y}`)
    }
  }
  return errors
}

for (const [stem, spec] of Object.entries(specs)) {
  const record = data.units[stem]
  const originalFile = path.join(v5, spec.file)
  const candidateFile = path.join(raw, `${stem}_candidate.png`)
  const candidate = png(candidateFile)
  const structure = png(path.join(raw, `${stem}_structure.png`))
  const appliance = png(path.join(raw, `${stem}_applianceMask.png`))
  assert.deepEqual([candidate.width, candidate.height], spec.size)
  assert.deepEqual([structure.width, structure.height], spec.size)
  assert.deepEqual([appliance.width, appliance.height], spec.size)
  assert.equal(record.contactY, candidate.height - 19 * 4, `${stem} must derive contact from its own foot anchor`)
  assert.equal(record.contactY, spec.contactY)
  assert.equal(record.topRevealPx, 6)
  assert.equal(record.fasciaPx, 8)
  assert.equal(record.v5Sha256, sha(originalFile))
  assert.equal(record.candidateSha256, sha(candidateFile))
  assert.deepEqual(structuralErrors(candidate, structure, appliance, spec), [], `${stem} has a chipped, overwritten or discontinuous surface`)

  const old = png(path.join(oldGate, `${stem}_option_b_candidate.png`))
  assert.ok(structuralErrors(old, structure, appliance, spec).length > 0, `${stem} historical B negative control unexpectedly passed`)
}

const room = png(path.join(raw, 'three_unit_neutral_room.png'))
const roomGuides = png(path.join(raw, 'three_unit_neutral_room_guides.png'))
assert.deepEqual([room.width, room.height], [252, 224])
assert.deepEqual([roomGuides.width, roomGuides.height], [252, 224])
// The room-floor junction is 51 lp and the object foot line 52 lp, leaving the
// last 4 lp as an unobstructed foreground channel.
for (let y = 208; y < 224; y++) {
  for (let x = 0; x < room.width; x++) assert.equal(pixel(room, x, y)[3], 255, `foreground floor hole at ${x},${y}`)
}
assert.ok(page.includes('In situ · three adjacent rear-wall bays'))
assert.ok(page.includes('neutral painted/stone surround'))
assert.ok(page.includes('exactly 4 lp of unobstructed foreground floor'))
assert.ok(page.includes('Historical gate B'))
assert.ok(page.includes('Promise.all'))
assert.ok(page.includes('.decode'))

assert.equal(register.protectedSnapshots.kitchenV5, treeSha(v5), 'V5 baseline changed')
assert.equal(register.protectedSnapshots.kitchenV17, treeSha(path.join(root, 'art/raw/kitchen-v5-exact-rollback-2026-10-17-v17')), 'V17 rollback changed')
assert.equal(register.protectedSnapshots.runtimeSpriteManifest, sha(path.join(root, 'public/sprites/manifest.json')), 'runtime manifest changed')
assert.equal(register.protectedSnapshots.animationWorkbenchFinalState, sha(path.join(root, 'data/keeper_animation_workbench.json')), 'Final/workbench state changed')
assert.equal(register.protectedSnapshots.approvedKeeperSourceFamily, treeSha(path.join(root, 'art/raw/keeper-first-batch')), 'approved Keeper source changed')

assert.ok(fs.existsSync(archiveFile), 'content-addressed review archive set is missing')
const archive = readJson(archiveFile)
const urls = []
const collect = value => {
  if (typeof value === 'string' && value.startsWith('/keeper-review/')) urls.push(value)
  else if (Array.isArray(value)) value.forEach(collect)
  else if (value && typeof value === 'object') Object.values(value).forEach(collect)
}
collect(data)
for (const url of new Set(urls)) assert.ok(archive.entries[url], `archive missing ${url}`)
assert.ok(!fs.existsSync(path.join(root, 'public/keeper-review/kitchen-countertop-gate-v18/assets')), 'public review binaries must be archived')

console.log('Kitchen V18 countertop gate verified: corrected B-only structure, historical gate fails, 19-lp contact and rear-wall room context pinned; runtime unchanged.')
