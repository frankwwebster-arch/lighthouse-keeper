import assert from 'node:assert/strict'
import crypto from 'node:crypto'
import fs from 'node:fs'
import path from 'node:path'
import { PNG } from 'pngjs'

const root = process.cwd()
const rawDir = path.join(root, 'art/raw/kitchen-bin-effects-2026-10-18-v30')
const v29RawDir = path.join(root, 'art/raw/kitchen-bin-effects-2026-10-18-v29')
const draftDir = path.join(root, 'art/drafts/kitchen-bin-effects-2026-10-18-v30')
const pageFile = path.join(root, 'public/keeper-review/kitchen-bin-effects-v30/index.html')
const archiveFile = path.join(root, 'review-archive/sets/kitchen-bin-effects-v30.json')
const sha = file => crypto.createHash('sha256').update(fs.readFileSync(file)).digest('hex')
const png = file => PNG.sync.read(fs.readFileSync(file))
const alpha = (image, x, y) => image.data[(y * image.width + x) * 4 + 3]

const preservedHashes = {
  'bin-standard.png': '86b05224a7da5fc5c05918f2875018920ed54cf46fc00cb08952ffd29789f9c0',
  'bin-broken-overflowing.png': '77ad87fabfd3e5c10a4a14f294af343a5d93a2a2015e6d77f18a4140b1f5fb4f',
  'kitchen-bin-standard-in-situ.png': '027e5b1d722b65ed55eecc2f96640fb07f5e0b33283ce8fdce0e5d892450e674',
  'kitchen-bin-broken-in-situ.png': 'bf1c741f9ff7e985ddc44584c9c13c76c60e0df8104d34a2a11848f1be58a1c3',
  'fx-slow-flies-f40.png': '28f3b35fdfe91d655ebe47914d17c948203f2def6bfa6b8fd5e2bf0a2b86cc5c',
}
const v29MiasmaSha = '4eed9dfb501d965d761669bf7ccbe563b18c175e87ab39bffd7ee5c41a795d6c'

const catalogue = JSON.parse(fs.readFileSync(path.join(draftDir, 'candidate-catalogue.json'), 'utf8'))
const register = JSON.parse(fs.readFileSync(path.join(draftDir, 'batch-register.json'), 'utf8'))
assert.equal(catalogue.version, 30)
assert.equal(catalogue.objectSourceVersion, 28)
assert.equal(catalogue.effectSourceVersion, 29)
assert.equal(catalogue.objectPixelsChanged, false)
assert.equal(catalogue.flyPixelsChanged, false)
assert.equal(catalogue.miasmaColourPaletteChanged, false)
assert.deepEqual(catalogue.states, ['standard', 'broken_overflowing'])
assert.match(register.v29Disposition, /palette, flies and timing preserved/)

for (const [name, expected] of Object.entries(preservedHashes)) {
  const file = path.join(rawDir, name)
  assert.equal(sha(file), expected, `${name} no longer matches its approved source pixels`)
  assert.equal(sha(file), catalogue.outputs[name].sha256)
}

const effect = catalogue.effects.stench_miasma
assert.equal(effect.reusable, true)
assert.equal(effect.frames, 40)
assert.equal(effect.fps, 4)
assert.equal(effect.durationSeconds, 10)
assert.equal(effect.objectPixelsChanged, false)
assert.equal(effect.previousSha256, v29MiasmaSha)
assert.deepEqual(effect.cellPixels, [80, 80])

const v29File = path.join(v29RawDir, 'fx-stench-miasma-f40.png')
const v30File = path.join(rawDir, effect.file)
assert.equal(sha(v29File), v29MiasmaSha)
assert.notEqual(sha(v30File), v29MiasmaSha, 'V30 miasma must not silently reuse the too-subtle V29 strip')
assert.equal(sha(v30File), catalogue.outputs[effect.file].sha256)
const v29 = png(v29File)
const v30 = png(v30File)
assert.deepEqual([v30.width, v30.height], [80 * 40, 80])

const v29Palette = new Set()
for (let index = 0; index < v29.data.length; index += 4) {
  if (v29.data[index + 3] === 0) continue
  v29Palette.add([...v29.data.subarray(index, index + 4)].join(','))
}

const frameHashes = new Set()
let v29TotalPixels = 0
let v30TotalPixels = 0
for (let frame = 0; frame < 40; frame++) {
  const x0 = frame * 80
  const bytes = Buffer.alloc(80 * 80 * 4)
  let top = 80
  let sourcePixels = 0
  for (let y = 0; y < 80; y++) {
    for (let x = 0; x < 80; x++) {
      const a30 = alpha(v30, x0 + x, y)
      const a29 = alpha(v29, x0 + x, y)
      if (a29 > 0) v29TotalPixels++
      if (a30 > 0) {
        v30TotalPixels++
        top = Math.min(top, y)
        const pixelIndex = (y * v30.width + x0 + x) * 4
        const rgba = [...v30.data.subarray(pixelIndex, pixelIndex + 4)].join(',')
        assert.ok(v29Palette.has(rgba), `V30 introduced a colour outside V29 at frame ${frame}, ${x},${y}: ${rgba}`)
        if (x >= 36 && x <= 44 && y >= 63 && y <= 70) sourcePixels++
      }
    }
  }
  assert.ok(top <= 5, `V30 frame ${frame} does not rise high enough: top y=${top}`)
  assert.ok(sourcePixels >= 4, `V30 frame ${frame} is detached from the bin opening`)
  for (let x = 0; x < 80; x++) {
    assert.equal(alpha(v30, x0 + x, 0), 0, `V30 frame ${frame} touches top edge`)
    assert.equal(alpha(v30, x0 + x, 79), 0, `V30 frame ${frame} touches bottom edge`)
  }
  for (let y = 0; y < 80; y++) {
    assert.equal(alpha(v30, x0, y), 0, `V30 frame ${frame} touches left edge`)
    assert.equal(alpha(v30, x0 + 79, y), 0, `V30 frame ${frame} touches right edge`)
    v30.data.copy(bytes, y * 80 * 4, (y * v30.width + x0) * 4, (y * v30.width + x0 + 80) * 4)
  }
  frameHashes.add(crypto.createHash('sha256').update(bytes).digest('hex'))
}
assert.ok(frameHashes.size >= 28, 'V30 needs enough distinct poses for a ten-second loop')
assert.ok(v30TotalPixels >= v29TotalPixels * 3.5, 'V30 cloud is not substantially fuller than V29')

assert.deepEqual(catalogue.boundaries, {
  approved: false,
  promoted: false,
  v28ObjectPixelsPreserved: true,
  v29FlyPixelsPreserved: true,
  v29MiasmaPalettePreserved: true,
  objectAnimated: false,
  environmentalFxAnimated: true,
  runtimeChanged: false,
  canonicalChanged: false,
  v20ThroughV29Changed: false,
})

const page = fs.readFileSync(pageFile, 'utf8')
const nextConfig = fs.readFileSync(path.join(root, 'next.config.mjs'), 'utf8')
assert.match(page, /V29 green palette, subdued flies and ten-second timing are preserved exactly/)
assert.match(page, /rises substantially higher and broadens into a fuller, recognisable cloud/)
assert.match(page, /40 frames · 4 fps · 10 seconds/)
assert.match(page, /data-strip data-frames="40" data-fps="4"/)
assert.match(page, /Promise\.all\(media\.map/)
assert.match(page, /loaded and decoded\. Playback unlocked/)
assert.match(nextConfig, /source: '\/keeper-review\/kitchen-bin-effects-v30'/)

if (fs.existsSync(archiveFile)) {
  const archive = JSON.parse(fs.readFileSync(archiveFile, 'utf8'))
  assert.equal(Object.keys(archive.entries).length, 6)
  for (const record of Object.values(archive.entries)) assert.equal(sha(path.join(root, record.object)), record.sha256)
}

console.log('Kitchen V30 verified: exact V28 bin, exact V29 palette/flies/timing, and a taller fuller 40-frame miasma cloud')
