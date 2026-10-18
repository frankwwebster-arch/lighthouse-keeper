import assert from 'node:assert/strict'
import crypto from 'node:crypto'
import fs from 'node:fs'
import path from 'node:path'
import { PNG } from 'pngjs'

const root = process.cwd()
const set = 'kitchen-rebuild-states-2026-10-18-v2'
const sourceDir = path.join(root, 'art/source', set, 'generated')
const raw = path.join(root, 'art/raw', set)
const draft = path.join(root, 'art/drafts', set)
const page = path.join(root, 'public/keeper-review/kitchen-rebuild-states-v2/index.html')
const archive = path.join(root, 'review-archive/sets/kitchen-rebuild-states-v2.json')
const v1 = path.join(root, 'art/raw/kitchen-rebuild-foundation-2026-10-18-v1')
const binV28 = path.join(root, 'art/raw/kitchen-bin-states-2026-10-18-v28')
const binV31 = path.join(root, 'art/raw/kitchen-bin-effects-2026-10-18-v31')

const sha = file => crypto.createHash('sha256').update(fs.readFileSync(file)).digest('hex')
const png = file => PNG.sync.read(fs.readFileSync(file))
const offset = (image, x, y) => (y * image.width + x) * 4
const pixel = (image, x, y) => image.data.subarray(offset(image, x, y), offset(image, x, y) + 4)
const alpha = (image, x, y) => pixel(image, x, y)[3]
const same = (a, b) => a.every((value, index) => value === b[index])
const assertSize = (image, size, label) => assert.deepEqual([image.width, image.height], size, `${label} dimensions drifted`)

const sources = {
  'on-object-amendments-v1.png': 'f7e459c8c39db0fc77b995cbdcdc31b569eaf9f54c1267991e32e077ff445086',
  'broken-object-amendments-v1.png': '8a3f278218711a4684e9fdc7bdf318d19af29d8d768342ed5c7def4a53a141d8',
  'on-effects-reference-v1.png': 'fb76d72ac18bbbdc1dbd5235c30e4f3824e3ebf2f6f107eed1b29fa5aecc6e5f',
  'broken-effects-reference-v2.png': 'a0b422980d159cffaba8fb8b782a4a8a2f21670b53cbf9c5136cbfe3caf68248',
}
for (const [name, hash] of Object.entries(sources)) assert.equal(sha(path.join(sourceDir, name)), hash, `${name} source changed`)

const catalogue = JSON.parse(fs.readFileSync(path.join(draft, 'candidate-catalogue.json'), 'utf8'))
const register = JSON.parse(fs.readFileSync(path.join(draft, 'batch-register.json'), 'utf8'))
assert.equal(catalogue.set, set)
assert.equal(catalogue.version, 2)
assert.equal(catalogue.status, 'amended-state-family-awaiting-review')
assert.equal(catalogue.foundation.immutable, true)
assert.deepEqual(catalogue.foundation.roomPixels, [772, 224])
assert.equal(catalogue.foundation.bayWidthPixels, 84)
assert.equal(catalogue.foundation.bayCount, 6)
assert.equal(catalogue.method.amendmentsNotRerenders, true)
assert.equal(catalogue.method.sharedCabinetAuthority, 'V1')
assert.equal(catalogue.method.environmentalEffectsSeparate, true)
assert.equal(catalogue.method.fridgeDoorColour, 'warm-white-ivory-enamel')
assert.deepEqual(catalogue.states, {
  fridge: ['standard', 'broken'], kettle: ['standard', 'on', 'broken'], toaster: ['standard', 'on', 'broken'],
  oven: ['standard', 'on', 'broken'], bowl: ['standard', 'broken'], basin: ['standard', 'on', 'broken'],
})
assert.equal(catalogue.promotion, 'none')
assert.equal(catalogue.runtimeWiring, 'unchanged')
assert.equal(register.status, 'awaiting-complete-state-family-visual-review')

for (const [name, meta] of Object.entries(catalogue.outputs)) {
  const file = path.join(raw, name)
  assert.ok(fs.existsSync(file), `missing output ${name}`)
  assert.equal(sha(file), meta.sha256, `${name} hash drifted`)
  assertSize(png(file), meta.pixels, name)
}

assert.equal(sha(path.join(raw, 'kitchen-background.png')), sha(path.join(v1, 'kitchen-standard-background.png')), 'V1 background changed')
assert.equal(sha(path.join(raw, 'table-chair.png')), sha(path.join(v1, 'standard-table-chair.png')), 'V1 table/chair changed')
assert.equal(sha(path.join(raw, 'bin-standard.png')), sha(path.join(binV28, 'bin-standard.png')), 'accepted standard bin changed')
assert.equal(sha(path.join(raw, 'bin-broken.png')), sha(path.join(binV28, 'bin-broken-overflowing.png')), 'accepted broken bin changed')
assert.equal(sha(path.join(raw, 'fx-bin-stench-f40.png')), sha(path.join(binV31, 'fx-stench-miasma-f40.png')), 'approved stench effect changed')
assert.equal(sha(path.join(raw, 'fx-bin-flies-f40.png')), sha(path.join(binV31, 'fx-slow-flies-f40.png')), 'approved flies effect changed')

const assets = ['fridge', 'kettle', 'toaster', 'oven', 'bowl', 'basin']
const standardV1 = Object.fromEntries(assets.map(asset => [asset, png(path.join(v1, `bay-${asset === 'oven' ? 'oven-hob' : asset === 'bowl' ? 'mixing-bowl' : asset}.png`))]))
for (const asset of assets) {
  const standard = png(path.join(raw, `${asset}-standard.png`))
  assertSize(standard, [84, 120], `${asset} standard`)
  if (asset !== 'fridge') assert.equal(sha(path.join(raw, `${asset}-standard.png`)), sha(path.join(v1, `bay-${asset === 'oven' ? 'oven-hob' : asset === 'bowl' ? 'mixing-bowl' : asset}.png`)), `${asset} standard is not exact V1`)
  for (let x = 0; x < 84; x++) assert.equal(alpha(standard, x, 0), 0, `${asset} standard lacks top inspection gutter`)
}

const fridgeStandard = png(path.join(raw, 'fridge-standard.png'))
let paleDoor = 0; let blueDoor = 0
for (let y = 52; y < 113; y++) for (let x = 9; x < 76; x++) {
  const [r, g, b, a] = pixel(fridgeStandard, x, y)
  if (!a) continue
  if (r > 165 && g > 150 && b > 120) paleDoor++
  if (b > r * 1.25 && b > g * 1.15) blueDoor++
}
assert.ok(paleDoor > 2600, 'standard fridge door is not unmistakably white/ivory')
assert.ok(paleDoor > blueDoor * 8, 'blue still dominates the fridge door')

assert.equal(sha(path.join(raw, 'kettle-on.png')), sha(path.join(raw, 'kettle-standard.png')), 'kettle On object should stay static; steam must be separate')
assert.equal(sha(path.join(raw, 'basin-on.png')), sha(path.join(raw, 'basin-standard.png')), 'basin On object should stay static; water must be separate')
for (const asset of ['toaster', 'oven']) assert.notEqual(sha(path.join(raw, `${asset}-on.png`)), sha(path.join(raw, `${asset}-standard.png`)), `${asset} On amendment is missing`)
for (const asset of assets) assert.notEqual(sha(path.join(raw, `${asset}-broken.png`)), sha(path.join(raw, `${asset}-standard.png`)), `${asset} Broken amendment is missing`)
assertSize(png(path.join(raw, 'fridge-broken.png')), [124, 119], 'extended broken fridge')

const brokenFridge = png(path.join(raw, 'fridge-broken.png'))
let puddlePixels = 0
for (let y = 109; y < 119; y++) for (let x = 0; x < 124; x++) {
  const [r, g, b, a] = pixel(brokenFridge, x, y)
  if (a > 70 && b > r * 1.3 && b > g * 1.05) puddlePixels++
}
assert.ok(puddlePixels > 260, 'broken fridge puddle is not a clear flat floor footprint')

const countWarm = image => {
  let total = 0
  for (let y = 65; y < 112; y++) for (let x = 22; x < 72; x++) {
    const [r, g, b, a] = pixel(image, x, y)
    if (a && r > 120 && r > b * 1.45 && g > b * 1.2) total++
  }
  return total
}
assert.ok(countWarm(png(path.join(raw, 'oven-on.png'))) > countWarm(png(path.join(raw, 'oven-standard.png'))) * 3, 'oven On lacks strong warm cavity/dish light')

const effectNames = Object.keys(catalogue.effects)
assert.equal(effectNames.length, 9)
for (const name of effectNames) {
  const meta = catalogue.effects[name]
  assert.equal(meta.frames, 40); assert.equal(meta.fps, 4); assert.equal(meta.durationSeconds, 10)
  assert.equal(meta.reusable, true); assert.equal(meta.effectOnly, true)
  assert.deepEqual(meta.cellPixels, [120, 144])
  assert.match(meta.sfx, /^kitchen_/)
  const strip = png(path.join(raw, meta.file))
  assertSize(strip, [4800, 144], name)
  const hashes = new Set()
  const visibility = []
  for (let frame = 0; frame < 40; frame++) {
    const bytes = Buffer.alloc(120 * 144 * 4)
    let visible = 0
    for (let y = 0; y < 144; y++) for (let x = 0; x < 120; x++) {
      const source = offset(strip, frame * 120 + x, y)
      strip.data.copy(bytes, (y * 120 + x) * 4, source, source + 4)
      if (strip.data[source + 3]) visible++
      if (x === 0 || x === 119 || y === 0 || y === 143) assert.equal(strip.data[source + 3], 0, `${name} frame ${frame} touches a shared edge`)
    }
    visibility.push(visible)
    if (name !== 'oven-broken-flicker') assert.ok(visible > 8, `${name} frame ${frame} is unreadably empty`)
    hashes.add(crypto.createHash('sha256').update(bytes).digest('hex'))
  }
  if (name === 'oven-broken-flicker') {
    assert.ok(visibility.filter(value => value === 0).length >= 8, 'oven warning light never clearly switches off')
    assert.ok(visibility.filter(value => value > 20).length >= 16, 'oven warning light lacks enough angry flashes')
    assert.ok(hashes.size >= 4, 'oven warning/cavity flicker lacks distinct phases')
  } else {
    assert.ok(hashes.size >= 12, `${name} lacks a sedate ten-second pose range`)
  }
}

for (const roomName of ['kitchen-standard-v2.png', 'kitchen-all-on-static.png', 'kitchen-all-broken-static.png', 'kitchen-mixed-static.png', 'kitchen-all-on-preview.png', 'kitchen-all-broken-preview.png', 'kitchen-mixed-preview.png']) {
  assertSize(png(path.join(raw, roomName)), [772, 224], roomName)
}

const html = fs.readFileSync(page, 'utf8')
assert.match(html, /All On · complete kitchen at native game size/)
assert.match(html, /All Broken · complete kitchen at native game size/)
assert.match(html, /Intermingled state mixer/)
assert.match(html, /Promise\.all\(DATA\.media\.map\(load\)/)
assert.match(html, /i\.decode\(\)/)
assert.match(html, /state-bearing pixels inside each existing bay/)
assert.match(html, /there is no intact appliance hidden underneath/)
assert.match(html, /kitchen_kettle_boiling_steam_loop/)
assert.match(html, /kitchen_basin_broken_upward_spray_loop/)

assert.ok(fs.existsSync(archive), 'archive manifest missing; run npm run archive:keeper-review')
const manifest = JSON.parse(fs.readFileSync(archive, 'utf8'))
assert.equal(manifest.set, 'kitchen-rebuild-states-v2')
const archived = new Set(Object.keys(manifest.entries).map(entry => path.basename(entry)))
for (const name of Object.keys(catalogue.outputs)) assert.ok(archived.has(name), `output was not content-addressed: ${name}`)

console.log('Kitchen Rebuild V2 verified: white fridge, bay-confined amendments, exact V1 background/cabinet authorities, 9 isolated 40-frame effects, all-On/all-Broken rooms and mixed-state compositor')
