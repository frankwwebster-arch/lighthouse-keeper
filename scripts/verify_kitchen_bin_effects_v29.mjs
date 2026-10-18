import assert from 'node:assert/strict'
import crypto from 'node:crypto'
import fs from 'node:fs'
import path from 'node:path'
import { PNG } from 'pngjs'

const root = process.cwd()
const rawDir = path.join(root, 'art/raw/kitchen-bin-effects-2026-10-18-v29')
const draftDir = path.join(root, 'art/drafts/kitchen-bin-effects-2026-10-18-v29')
const pageFile = path.join(root, 'public/keeper-review/kitchen-bin-effects-v29/index.html')
const archiveFile = path.join(root, 'review-archive/sets/kitchen-bin-effects-v29.json')
const sha = file => crypto.createHash('sha256').update(fs.readFileSync(file)).digest('hex')
const png = file => PNG.sync.read(fs.readFileSync(file))
const alpha = (image, x, y) => image.data[(y * image.width + x) * 4 + 3]

const staticHashes = {
  'bin-standard.png': '86b05224a7da5fc5c05918f2875018920ed54cf46fc00cb08952ffd29789f9c0',
  'bin-broken-overflowing.png': '77ad87fabfd3e5c10a4a14f294af343a5d93a2a2015e6d77f18a4140b1f5fb4f',
  'kitchen-bin-standard-in-situ.png': '027e5b1d722b65ed55eecc2f96640fb07f5e0b33283ce8fdce0e5d892450e674',
  'kitchen-bin-broken-in-situ.png': 'bf1c741f9ff7e985ddc44584c9c13c76c60e0df8104d34a2a11848f1be58a1c3',
}

const catalogue = JSON.parse(fs.readFileSync(path.join(draftDir, 'candidate-catalogue.json'), 'utf8'))
const register = JSON.parse(fs.readFileSync(path.join(draftDir, 'batch-register.json'), 'utf8'))
assert.equal(catalogue.version, 29)
assert.equal(catalogue.objectSourceVersion, 28)
assert.equal(catalogue.objectPixelsChanged, false)
assert.deepEqual(catalogue.states, ['standard', 'broken_overflowing'])
assert.deepEqual(catalogue.boundaries, {
  approved: false,
  promoted: false,
  v28ObjectPixelsPreserved: true,
  objectAnimated: false,
  environmentalFxAnimated: true,
  runtimeChanged: false,
  canonicalChanged: false,
  v20ThroughV28Changed: false,
})
assert.match(register.v28Disposition, /retained-byte-for-byte/)

for (const [name, expected] of Object.entries(staticHashes)) {
  const file = path.join(rawDir, name)
  assert.equal(sha(file), expected, `${name} no longer matches the approved V28 pixels`)
  assert.equal(sha(file), catalogue.outputs[name].sha256)
}

assert.deepEqual(Object.keys(catalogue.effects), ['stench_miasma', 'slow_flies'])
for (const effect of Object.values(catalogue.effects)) {
  assert.equal(effect.reusable, true)
  assert.equal(effect.frames, 40)
  assert.equal(effect.fps, 4)
  assert.equal(effect.durationSeconds, 10)
  assert.equal(effect.objectPixelsChanged, false)
  assert.deepEqual(effect.cellPixels, [80, 80])
  const file = path.join(rawDir, effect.file)
  const image = png(file)
  assert.deepEqual([image.width, image.height], [80 * 40, 80], `${effect.file} strip geometry changed`)
  assert.equal(sha(file), catalogue.outputs[effect.file].sha256, `${effect.file} hash drifted`)
  const hashes = new Set()
  for (let frame = 0; frame < 40; frame++) {
    const x0 = frame * 80
    const bytes = Buffer.alloc(80 * 80 * 4)
    for (let x = 0; x < 80; x++) {
      assert.equal(alpha(image, x0 + x, 0), 0, `${effect.file} frame ${frame} touches top edge`)
      assert.equal(alpha(image, x0 + x, 79), 0, `${effect.file} frame ${frame} touches bottom edge`)
    }
    for (let y = 0; y < 80; y++) {
      assert.equal(alpha(image, x0, y), 0, `${effect.file} frame ${frame} touches left edge`)
      assert.equal(alpha(image, x0 + 79, y), 0, `${effect.file} frame ${frame} touches right edge`)
      image.data.copy(bytes, y * 80 * 4, (y * image.width + x0) * 4, (y * image.width + x0 + 80) * 4)
    }
    hashes.add(crypto.createHash('sha256').update(bytes).digest('hex'))
  }
  assert.ok(hashes.size >= 28, `${effect.file} needs enough distinct poses for a ten-second loop`)
}

const stench = png(path.join(rawDir, catalogue.effects.stench_miasma.file))
for (let frame = 0; frame < 40; frame++) {
  let sourcePixels = 0
  for (let y = 63; y <= 70; y++) {
    for (let x = 36; x <= 44; x++) if (alpha(stench, frame * 80 + x, y) > 0) sourcePixels++
  }
  assert.ok(sourcePixels >= 4, `stench frame ${frame} is detached from the bin opening`)
}

const page = fs.readFileSync(pageFile, 'utf8')
const nextConfig = fs.readFileSync(path.join(root, 'next.config.mjs'), 'utf8')
assert.match(page, /V28 standard and overflowing bin pixels are preserved exactly/)
assert.match(page, /40 frames · 4 fps · 10 seconds/)
assert.match(page, /data-strip data-frames="40" data-fps="4"/)
assert.match(page, /kitchen_bin_flies_slow_loop/)
assert.match(page, /Promise\.all\(media\.map/)
assert.match(page, /loaded and decoded\. Playback unlocked/)
assert.match(nextConfig, /source: '\/keeper-review\/kitchen-bin-effects-v29'/)

if (fs.existsSync(archiveFile)) {
  const archive = JSON.parse(fs.readFileSync(archiveFile, 'utf8'))
  assert.equal(Object.keys(archive.entries).length, 6)
  for (const record of Object.values(archive.entries)) assert.equal(sha(path.join(root, record.object)), record.sha256)
}

console.log('Kitchen V29 bin effects verified: exact V28 bin pixels plus 2 reusable 40-frame/4-fps ten-second loops')
