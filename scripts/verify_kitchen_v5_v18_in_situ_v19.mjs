import assert from 'node:assert/strict'
import crypto from 'node:crypto'
import fs from 'node:fs'
import path from 'node:path'
import { PNG } from 'pngjs'

const root = process.cwd()
const raw = path.join(root, 'art/raw/kitchen-v5-v18-in-situ-2026-10-17-v19')
const draft = path.join(root, 'art/drafts/kitchen-v5-v18-in-situ-2026-10-17-v19')
const v5 = path.join(root, 'art/raw/kitchen-basic-assets-2026-10-16-v5')
const v18 = path.join(root, 'art/raw/kitchen-countertop-gate-2026-10-17-v18')
const pageFile = path.join(root, 'public/keeper-review/kitchen-v5-v18-in-situ-comparison-v19/index.html')
const archiveFile = path.join(root, 'review-archive/sets/kitchen-v5-v18-in-situ-comparison-v19.json')
const readJson = file => JSON.parse(fs.readFileSync(file, 'utf8'))
const sha = file => crypto.createHash('sha256').update(fs.readFileSync(file)).digest('hex')
const png = file => PNG.sync.read(fs.readFileSync(file))
const pixel = (image, x, y) => image.data.subarray((y * image.width + x) * 4, (y * image.width + x) * 4 + 4)
const samePixel = (a, b, x, y) => pixel(a, x, y).every((value, i) => value === pixel(b, x, y)[i])

const sourcePins = {
  obj_kettle: {
    v5: ['obj_kettle_standard_f1.png', 'bc296bff87334d769aadccd75e749f4edd0221853f1d52eae90ab04270552b3c'],
    v18: ['obj_kettle_candidate.png', 'add806a1f9f84e0865a473082972d05421c6a04e6c4482a0da46f58065a67e3c'],
  },
  obj_cooker: {
    v5: ['obj_cooker_standard_f1.png', 'a6183f51f506957fb77c79ef5dfddc82c287dfa781838fe099944f76cf303034'],
    v18: ['obj_cooker_candidate.png', '67942103f64aa4ed8fb42c4fc3db2223ee0af0986d653305aeb5ddbe48bff437'],
  },
  obj_sink: {
    v5: ['obj_sink_standard_f1.png', '31ca919a515f05ac51c2850092df8501c9574c05013ea5a88ea5aca5e3d40f2a'],
    v18: ['obj_sink_candidate.png', '8f1c1f6fd9d8fb6ecd566c873affc7c34853eaabbdc78261c57b4763cc48522a'],
  },
}
const compositePins = {
  'empty_room.png': 'ec3e4e328883818ed86459651eb04b482a5953adc150192ad9c085de248a4f82',
  'v5_room.png': 'eec532fbab3324e49ef5548b02bdfe396f6478b766a31a20380e5a467f92ecab',
  'v5_room_guides.png': '9a8bf1be4a50396fba8c68136e02510b538fa1aa2e7e7d4ea62e6d1dd40dc12b',
  'v18_room.png': 'ca412b57db919c19b8ff2dc319f6beeba938668e1bd07beb97bb146f0ba7d39d',
  'v18_room_guides.png': 'd2379caa34e7d277c2e3b976ce0c64ff9bd239666dc48b656f4efe08964de343',
}

const data = readJson(path.join(draft, 'comparison-data.json'))
const register = readJson(path.join(draft, 'batch-register.json'))
const page = fs.readFileSync(pageFile, 'utf8')

assert.equal(data.version, 19)
assert.equal(data.status, 'review-only-comparison')
assert.deepEqual(data.order, ['obj_kettle', 'obj_cooker', 'obj_sink'])
assert.deepEqual(data.roomGeometry, { logical: [63, 56], pixels: [252, 224], bayPx: 84, wallFloorLp: 51, footLineLp: 52, foregroundLp: 4 })
assert.equal(register.decision, 'V18 rejected; exact V5 preferred for this comparison')
assert.equal(register.sameRoomFunction, 'scripts/build_kitchen_countertop_gate_v18.py::neutral_room_context')
for (const key of ['sourcePixelsAltered', 'sourcePixelsScaled', 'roomRebuilt', 'fullFamilyRebuilt', 'runtimeChanged', 'finalChanged', 'keeperChanged']) {
  assert.equal(register[key], false, `${key} must stay false`)
}

for (const [stem, pins] of Object.entries(sourcePins)) {
  const [v5File, v5Sha] = pins.v5
  const [v18File, v18Sha] = pins.v18
  assert.equal(sha(path.join(v5, v5File)), v5Sha, `${stem} exact V5 source changed`)
  assert.equal(sha(path.join(v18, v18File)), v18Sha, `${stem} rejected V18 source changed`)
  assert.equal(data.sources[stem].v5Sha256, v5Sha)
  assert.equal(data.sources[stem].v18Sha256, v18Sha)
}
for (const [file, expected] of Object.entries(compositePins)) {
  assert.equal(sha(path.join(raw, file)), expected, `${file} no longer matches the pinned deterministic composite`)
}

const empty = png(path.join(raw, 'empty_room.png'))
const v5Room = png(path.join(raw, 'v5_room.png'))
const v18Room = png(path.join(raw, 'v18_room.png'))
for (const image of [empty, v5Room, v18Room]) assert.deepEqual([image.width, image.height], [252, 224])

// The two variants must use the identical room. Wherever neither exact source
// raster contributes alpha, both output rooms must equal the shared empty room.
const v5Sources = data.order.map(stem => png(path.join(v5, sourcePins[stem].v5[0])))
const v18Sources = data.order.map(stem => png(path.join(v18, sourcePins[stem].v18[0])))
let sharedBackgroundPixels = 0
for (let y = 0; y < 224; y++) {
  for (let x = 0; x < 252; x++) {
    const bay = Math.floor(x / 84)
    const localX = x - bay * 84
    const v5LocalY = y - (208 - v5Sources[bay].height)
    const v18LocalY = y - (208 - v18Sources[bay].height)
    const v5Alpha = v5LocalY >= 0 && v5LocalY < v5Sources[bay].height ? pixel(v5Sources[bay], localX, v5LocalY)[3] : 0
    const v18Alpha = v18LocalY >= 0 && v18LocalY < v18Sources[bay].height ? pixel(v18Sources[bay], localX, v18LocalY)[3] : 0
    if (v5Alpha === 0 && v18Alpha === 0) {
      assert.ok(samePixel(v5Room, empty, x, y), `V5 room changed shared background at ${x},${y}`)
      assert.ok(samePixel(v18Room, empty, x, y), `V18 room changed shared background at ${x},${y}`)
      sharedBackgroundPixels++
    }
  }
}
assert.ok(sharedBackgroundPixels > 35000, 'expected most pixels to be the identical shared room')
for (let y = 208; y < 224; y++) {
  for (let x = 0; x < 252; x++) {
    assert.ok(samePixel(v5Room, empty, x, y), `V5 intrudes into the 4-lp foreground at ${x},${y}`)
    assert.ok(samePixel(v18Room, empty, x, y), `V18 intrudes into the 4-lp foreground at ${x},${y}`)
  }
}

assert.match(page, /Native V5 kettle, cooker and sink in the measured V18 room/)
assert.match(page, /Three 21-lp bays/)
assert.ok(page.includes(data.rooms.v5Clean))
assert.ok(page.includes(data.rooms.v5Guides))
assert.ok(!page.includes(data.rooms.v18Clean), 'rejected V18 must not displace the requested V5 review')

if (fs.existsSync(archiveFile)) {
  const archive = readJson(archiveFile)
  assert.equal(Object.keys(archive.entries).length, 4)
  for (const [sourceUrl, record] of Object.entries(archive.entries)) {
    if (sourceUrl.includes('/v5_room')) assert.ok(page.includes(sourceUrl))
    assert.equal(sha(path.join(root, record.object)), record.sha256)
  }
}

console.log('Kitchen V19 exact V5/V18 in-situ comparison verified')
