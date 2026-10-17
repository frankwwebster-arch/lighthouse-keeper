import assert from 'node:assert/strict'
import crypto from 'node:crypto'
import fs from 'node:fs'
import path from 'node:path'
import { PNG } from 'pngjs'

const root = process.cwd()
const rawDir = path.join(root, 'art/raw/kitchen-broken-loops-2026-10-18-v27')
const sourceDir = path.join(root, 'art/source/kitchen-broken-loops-2026-10-18-v27/generated')
const draftDir = path.join(root, 'art/drafts/kitchen-broken-loops-2026-10-18-v27')
const pageFile = path.join(root, 'public/keeper-review/kitchen-broken-loops-v27/index.html')
const archiveFile = path.join(root, 'review-archive/sets/kitchen-broken-loops-v27.json')
const roomSha = '175d77c063297c435eab468f297c369f79e5491b89bbdd2b03400d31cd334f4a'
const primeSha = '28a879bcee43c6d06330d05fb3cd74b4098b2ccce38ce41d15117f5fb0be5167'
const sha = file => crypto.createHash('sha256').update(fs.readFileSync(file)).digest('hex')
const png = file => PNG.sync.read(fs.readFileSync(file))
const alpha = (image, x, y) => image.data[(y * image.width + x) * 4 + 3]
const pixel = (image, x, y) => Array.from(image.data.subarray((y * image.width + x) * 4, (y * image.width + x) * 4 + 4))

assert.equal(sha(path.join(root, 'art/raw/kitchen-narrower-bin-2026-10-17-v25/full-kitchen-narrower-bin.png')), roomSha, 'V25 room changed')
assert.equal(sha(path.join(root, 'art/drafts/keeper-prime-seated-six-view-2026-10-16-v1/drafts/frames/keeper_prime_neutral_sitting-back_f01.png')), primeSha, 'Prime seated-back source changed')

const catalogue = JSON.parse(fs.readFileSync(path.join(draftDir, 'candidate-catalogue.json'), 'utf8'))
const register = JSON.parse(fs.readFileSync(path.join(draftDir, 'batch-register.json'), 'utf8'))
assert.equal(catalogue.version, 27)
assert.equal(catalogue.status, 'broken-state-loop-draft-awaiting-visual-confirmation')
assert.equal(catalogue.densityPxPerLp, 4)
assert.equal(catalogue.frames, 8)
assert.equal(catalogue.fps, 8)
assert.deepEqual(catalogue.boundaries, { approved: false, promoted: false, runtimeChanged: false, canonicalChanged: false, v20ThroughV26Changed: false })
assert.deepEqual(register.preserves, [20, 21, 22, 23, 24, 25, 26])
assert.equal(register.rejectedSourceRetained, 'table-broken-snapped-rejected-source.png')

const expected = ['bin', 'fridge', 'kettle', 'toaster', 'oven', 'bowl', 'sink', 'table']
assert.deepEqual(Object.keys(catalogue.clips), expected)
for (const name of expected) {
  const record = catalogue.clips[name]
  assert.equal(record.frames, 8)
  assert.equal(record.fps, 8)
  assert.equal(record.density, 4)
  assert.equal(record.loop, true)
  assert.ok(record.sfxCues.length >= 1, `${name} needs an SFX placeholder cue`)
  for (const cue of record.sfxCues) {
    assert.ok(Number.isInteger(cue.frame) && cue.frame >= 0 && cue.frame < 8)
    assert.match(cue.cue, /^kitchen_[a-z0-9_]+$/)
  }
  const image = png(path.join(rawDir, record.file))
  assert.equal(sha(path.join(rawDir, record.file)), record.sha256, `${name} output hash drifted`)
  const cellW = record.w * record.density
  const cellH = record.h * record.density
  assert.deepEqual([image.width, image.height], [cellW * 8, cellH], `${name} strip geometry differs from metadata`)
  const hashes = new Set()
  for (let frame = 0; frame < 8; frame++) {
    const x0 = frame * cellW
    for (let x = 0; x < cellW; x++) {
      assert.equal(alpha(image, x0 + x, 0), 0, `${name} frame ${frame} touches top shared edge`)
      assert.equal(alpha(image, x0 + x, cellH - 1), 0, `${name} frame ${frame} touches bottom shared edge`)
    }
    for (let y = 0; y < cellH; y++) {
      assert.equal(alpha(image, x0, y), 0, `${name} frame ${frame} touches left shared edge`)
      assert.equal(alpha(image, x0 + cellW - 1, y), 0, `${name} frame ${frame} touches right shared edge`)
    }
    const bytes = Buffer.alloc(cellW * cellH * 4)
    for (let y = 0; y < cellH; y++) image.data.copy(bytes, y * cellW * 4, (y * image.width + x0) * 4, (y * image.width + x0 + cellW) * 4)
    hashes.add(crypto.createHash('sha256').update(bytes).digest('hex'))
  }
  assert.ok(hashes.size > 1, `${name} loop has no animated frame change`)
}

assert.deepEqual(Object.keys(catalogue.effects), ['smell', 'smoke_black', 'smoke_light', 'steam', 'flame', 'water', 'sparks'])
for (const [name, record] of Object.entries(catalogue.effects)) {
  assert.equal(record.reusable, true)
  assert.equal(record.loop, true)
  const image = png(path.join(rawDir, record.file))
  assert.equal(sha(path.join(rawDir, record.file)), record.sha256, `${name} effect output hash drifted`)
  const cellW = record.w * 4, cellH = record.h * 4
  assert.deepEqual([image.width, image.height], [cellW * 8, cellH], `${name} effect geometry differs from metadata`)
  for (let frame = 0; frame < 8; frame++) {
    const x0 = frame * cellW
    for (let x = 0; x < cellW; x++) {
      assert.equal(alpha(image, x0 + x, 0), 0, `${name} effect frame ${frame} touches top edge`)
      assert.equal(alpha(image, x0 + x, cellH - 1), 0, `${name} effect frame ${frame} touches bottom edge`)
    }
    for (let y = 0; y < cellH; y++) {
      assert.equal(alpha(image, x0, y), 0, `${name} effect frame ${frame} touches left edge`)
      assert.equal(alpha(image, x0 + cellW - 1, y), 0, `${name} effect frame ${frame} touches right edge`)
    }
  }
}

assert.deepEqual(catalogue.effectPlacements.oven, ['smoke_black', 'flame:left_hob', 'flame:right_hob'])
assert.equal(catalogue.reusedEffectSources.smoke.file, 'art/raw/floor-asset-catalogue/fx_broken_smoke_f8.png')
assert.equal(catalogue.reusedEffectSources.sparks.file, 'art/raw/floor-asset-catalogue/fx_broken_sparks_f6.png')
assert.equal(sha(path.join(root, catalogue.reusedEffectSources.smoke.file)), catalogue.reusedEffectSources.smoke.sha256)
assert.equal(sha(path.join(root, catalogue.reusedEffectSources.sparks.file)), catalogue.reusedEffectSources.sparks.sha256)

for (const [name, expectedSha] of Object.entries(catalogue.sources)) {
  assert.equal(sha(path.join(sourceDir, name)), expectedSha, `${name} generated-source hash drifted`)
}
assert.ok(fs.existsSync(path.join(sourceDir, 'table-broken-snapped-rejected-source.png')), 'rejected snapped-leg draft must remain reversible')

const room = png(path.join(rawDir, 'kitchen-broken-full-room-cycle-f8.png'))
assert.deepEqual([room.width, room.height], [772 * 8, 224])
assert.equal(sha(path.join(rawDir, 'kitchen-broken-full-room-cycle-f8.png')), catalogue.roomLoop.sha256)
const chair = png(path.join(rawDir, 'kitchen-prime-seated-chair-corrected.png'))
assert.deepEqual([chair.width, chair.height], [772, 224])
let restoredChairPixels = 0
const plainRoom = png(path.join(rawDir, 'kitchen-game-scale-room-v25.png'))
for (let y = 114; y < 186; y++) for (let x = 700; x < 740; x++) {
  if (pixel(chair, x, y).every((value, index) => value === pixel(plainRoom, x, y)[index])) restoredChairPixels++
}
assert.ok(restoredChairPixels > 150, 'chair-back foreground was not restored over the seated Keeper')

const page = fs.readFileSync(pageFile, 'utf8')
const nextConfig = fs.readFileSync(path.join(root, 'next.config.mjs'), 'utf8')
assert.match(page, /All broken items in situ/)
assert.match(page, /Mixing bowl/)
assert.match(page, /Basin/)
assert.match(page, /animated flames on both hob burners/)
assert.match(page, /Corrected chair \/ Keeper registration/)
assert.match(page, /Promise\.all\(media\.map/)
assert.match(page, /AudioContext/)
assert.match(nextConfig, /source: '\/keeper-review\/kitchen-broken-loops-v27'/)

if (fs.existsSync(archiveFile)) {
  const archive = JSON.parse(fs.readFileSync(archiveFile, 'utf8'))
  assert.equal(Object.keys(archive.entries).length, 18)
  for (const record of Object.values(archive.entries)) assert.equal(sha(path.join(root, record.object)), record.sha256)
}

console.log('Kitchen V27 broken loops verified: 8 isolated repair clips, 7 reusable FX loops, chair occlusion corrected')
