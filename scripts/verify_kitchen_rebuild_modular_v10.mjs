import assert from 'node:assert/strict'
import crypto from 'node:crypto'
import fs from 'node:fs'
import path from 'node:path'
import { PNG } from 'pngjs'

const root = process.cwd()
const set = 'kitchen-rebuild-modular-2026-10-19-v10'
const raw = path.join(root, 'art/raw', set)
const draft = path.join(root, 'art/drafts', set)
const v1 = path.join(root, 'art/raw/kitchen-rebuild-foundation-2026-10-18-v1')
const v9 = path.join(root, 'art/raw/kitchen-rebuild-states-2026-10-19-v9')
const catalogue = JSON.parse(fs.readFileSync(path.join(draft, 'candidate-catalogue.json')))
const sha = file => crypto.createHash('sha256').update(fs.readFileSync(file)).digest('hex')
const png = file => PNG.sync.read(fs.readFileSync(file))

assert.equal(catalogue.set, set)
assert.equal(catalogue.version, 10)
assert.equal(catalogue.status, 'modular-structural-separation-awaiting-visual-review')
assert.equal(catalogue.promotion, 'none')
assert.equal(catalogue.runtimeWiring, 'unchanged')
for (const key of ['structuralCabinetLayer', 'objectOnlyTransparentStates', 'standaloneFridge', 'standaloneOvenAndHob', 'fixedInteractionAnchors', 'environmentalEffectsSeparate']) {
  assert.equal(catalogue.method[key], true, `${key} contract missing`)
}
assert.deepEqual(catalogue.layout.sequence, ['fridge', 'cabinet-run-left', 'oven', 'cabinet-run-right', 'table'])
assert.deepEqual(catalogue.layout.slotOrder, ['fridge', 'kettle', 'toaster', 'oven', 'bowl', 'basin'])
assert.deepEqual(catalogue.layout.cabinetRuns.left, { origin: [168, 98], pixels: [168, 120] })
assert.deepEqual(catalogue.layout.cabinetRuns.right, { origin: [420, 98], pixels: [168, 120], includesSinkCabinet: true })

const expectedAnchors = { fridge: [126, 218], kettle: [210, 218], toaster: [294, 218], oven: [378, 218], bowl: [462, 218], basin: [546, 218] }
assert.deepEqual(catalogue.interactionAnchors, expectedAnchors)
for (const [asset, x] of Object.entries({ fridge: 84, kettle: 168, toaster: 252, oven: 336, bowl: 420, basin: 504 })) {
  assert.deepEqual(catalogue.states[asset], ['off', 'on', 'broken'])
  assert.deepEqual(catalogue.installedSlots[asset], [x, 98, 84, 120])
  const origins = ['off', 'on', 'broken'].map(state => catalogue.objectOrigins[`${asset}-${state}`])
  assert.deepEqual(origins[0], origins[1], `${asset} On origin moved`)
  assert.deepEqual(origins[0], origins[2], `${asset} Broken origin moved`)
  assert.equal(expectedAnchors[asset][0], x + 42, `${asset} anchor is no longer the bay centre`)
}

assert.equal(sha(path.join(raw, 'kitchen-background.png')), sha(path.join(v1, 'kitchen-standard-background.png')), 'accepted V1 room background changed')
assert.equal(sha(path.join(raw, 'table-chair.png')), sha(path.join(v9, 'table-chair.png')), 'accepted V9 table/chair changed')
assert.equal(sha(path.join(raw, 'bin-standard.png')), sha(path.join(v9, 'bin-standard.png')), 'approved bin changed')
assert.equal(sha(path.join(raw, 'bin-broken.png')), sha(path.join(v9, 'bin-broken.png')), 'approved broken bin changed')

const left = png(path.join(raw, 'cabinet-run-left.png'))
const right = png(path.join(raw, 'cabinet-run-right.png'))
assert.deepEqual([left.width, left.height], [168, 120])
assert.deepEqual([right.width, right.height], [168, 120])
for (const [label, image] of [['left', left], ['right', right]]) {
  for (let y = 0; y < 35; y++) for (let x = 0; x < image.width; x++) assert.equal(image.data[(y * image.width + x) * 4 + 3], 0, `${label} run contains an object above the worktop at ${x},${y}`)
  for (let y = 35; y < 53; y++) for (let x = 80; x < 88; x++) assert.ok(image.data[(y * image.width + x) * 4 + 3] > 0, `${label} run countertop breaks at its internal join ${x},${y}`)
}

function assertTransparentGutter(image, label, gutter = 2) {
  for (let y = 0; y < image.height; y++) for (let x = 0; x < image.width; x++) {
    if (x < gutter || x >= image.width - gutter || y < gutter || y >= image.height - gutter) {
      assert.equal(image.data[(y * image.width + x) * 4 + 3], 0, `${label} violates ${gutter}px transparent gutter at ${x},${y}`)
    }
  }
}

for (const asset of Object.keys(expectedAnchors)) for (const state of ['off', 'on', 'broken']) {
  const name = `${asset}-${state}.png`
  const image = png(path.join(raw, name))
  assert.deepEqual([image.width, image.height], asset === 'fridge' ? [128, 130] : [88, 124], `${name} cell geometry`)
  assertTransparentGutter(image, name)
  if (!['fridge', 'oven'].includes(asset)) {
    // Countertop props may overlap the counter surface, but can never contain
    // cabinet-front or floor pixels.
    for (let y = 55; y < image.height; y++) for (let x = 0; x < image.width; x++) assert.equal(image.data[(y * image.width + x) * 4 + 3], 0, `${name} contains structural pixels below its prop envelope`)
  }
  assert.equal(sha(path.join(raw, name)), catalogue.outputs[name].sha256, `${name} catalogue hash`)
}
assert.equal(sha(path.join(raw, 'bowl-off.png')), sha(path.join(raw, 'bowl-on.png')), 'non-powered bowl On state must remain the exact Off object')

const structure = png(path.join(raw, 'kitchen-structure-only.png'))
const background = png(path.join(raw, 'kitchen-background.png'))
assert.deepEqual([structure.width, structure.height], [772, 224])
for (const [start, end, label] of [[84, 168, 'fridge'], [336, 420, 'oven']]) {
  for (let y = 98; y < 218; y++) for (let x = start; x < end; x++) {
    const i = (y * 772 + x) * 4
    assert.deepEqual([...structure.data.subarray(i, i + 4)], [...background.data.subarray(i, i + 4)], `${label} slot is not structurally empty at ${x},${y}`)
  }
}

for (const [name, meta] of Object.entries(catalogue.outputs)) {
  const file = path.join(raw, name)
  assert.ok(fs.existsSync(file), `${name} missing`)
  assert.equal(sha(file), meta.sha256, `${name} output hash`)
  const image = png(file)
  assert.deepEqual([image.width, image.height], meta.pixels, `${name} output geometry`)
}

for (const family of Object.values(catalogue.effectFamilies)) for (const name of family.models) {
  const effect = catalogue.effects[name]
  assert.equal(effect.frames, 40, `${name} frames`)
  assert.equal(effect.fps, 4, `${name} fps`)
  assert.equal(effect.canonicalDurationSeconds, 10, `${name} duration`)
  const image = png(path.join(raw, effect.file))
  const [cw, ch] = effect.cellPixels
  assert.deepEqual([image.width, image.height], [cw * 40, ch], `${name} strip geometry`)
  for (let frame = 0; frame < 40; frame++) for (let y = 0; y < ch; y++) for (let x = 0; x < cw; x++) {
    if (x < 2 || x >= cw - 2 || y < 2 || y >= ch - 2) assert.equal(image.data[(y * image.width + frame * cw + x) * 4 + 3], 0, `${name} frame ${frame} shared-edge alpha`)
  }
}

const html = fs.readFileSync(path.join(root, 'public/keeper-review/kitchen-rebuild-modular-v10/index.html'), 'utf8')
for (const pattern of [
  /Rebuild V10 reversible modular draft/,
  /Structure only · two cabinet runs/,
  /All Off · native game size/,
  /cabinet-run-left\.png/,
  /cabinet-run-right\.png/,
  /kitchen-rebuild-v10-asset-layer-config/,
  /Promise\.all\(DATA\.media\.map\(load\)/,
  /drawStructure/,
  /objectOrigins/,
]) assert.match(html, pattern)
assert.doesNotMatch(html, /fridge-standard\.png|kettle-standard\.png|oven-standard\.png/)

const archiveFile = path.join(root, 'review-archive/sets/kitchen-rebuild-modular-v10.json')
assert.ok(fs.existsSync(archiveFile), 'V10 archive manifest missing')
const archive = JSON.parse(fs.readFileSync(archiveFile))
assert.equal(archive.set, 'kitchen-rebuild-modular-v10')
const archived = new Set(Object.keys(archive.entries).map(entry => path.basename(entry)))
for (const name of Object.keys(catalogue.outputs)) assert.ok(archived.has(name), `${name} not archived`)

console.log('Kitchen Rebuild Modular V10 verified: two continuous cabinet runs, empty standalone fridge/oven slots, 18 alpha-isolated states, fixed six bay-centre Keeper anchors, and isolated 40-frame effect cells')
