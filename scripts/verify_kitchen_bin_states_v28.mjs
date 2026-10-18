import assert from 'node:assert/strict'
import crypto from 'node:crypto'
import fs from 'node:fs'
import path from 'node:path'
import { PNG } from 'pngjs'

const root = process.cwd()
const rawDir = path.join(root, 'art/raw/kitchen-bin-states-2026-10-18-v28')
const sourceDir = path.join(root, 'art/source/kitchen-bin-states-2026-10-18-v28/generated')
const draftDir = path.join(root, 'art/drafts/kitchen-bin-states-2026-10-18-v28')
const pageFile = path.join(root, 'public/keeper-review/kitchen-bin-states-v28/index.html')
const archiveFile = path.join(root, 'review-archive/sets/kitchen-bin-states-v28.json')
const sha = file => crypto.createHash('sha256').update(fs.readFileSync(file)).digest('hex')
const png = file => PNG.sync.read(fs.readFileSync(file))
const alpha = (image, x, y) => image.data[(y * image.width + x) * 4 + 3]

const sourceV1Sha = 'd917330d83d2e9527e02dc7d8dbdaae0a9e27aa024879775839645a89f99d5ba'
const sourceV2Sha = 'f07c82b186dab52aff66fbde0ccabe23ef0f3428f64656dbe4f9716b6c74d1ec'
assert.equal(sha(path.join(sourceDir, 'bin-two-state-source-v1.png')), sourceV1Sha)
assert.equal(sha(path.join(sourceDir, 'bin-two-state-spill-source-v2.png')), sourceV2Sha)

const catalogue = JSON.parse(fs.readFileSync(path.join(draftDir, 'candidate-catalogue.json'), 'utf8'))
const register = JSON.parse(fs.readFileSync(path.join(draftDir, 'batch-register.json'), 'utf8'))
assert.equal(catalogue.version, 28)
assert.equal(catalogue.status, 'static-bin-state-family-awaiting-visual-confirmation')
assert.deepEqual(catalogue.states, ['standard', 'broken_overflowing'])
assert.deepEqual(catalogue.cellPixels, [72, 72])
assert.equal(catalogue.baselineYExclusive, 68)
assert.equal(catalogue.source.initialSha256, sourceV1Sha)
assert.equal(catalogue.source.spillRevisionSha256, sourceV2Sha)
assert.deepEqual(catalogue.boundaries, { approved: false, promoted: false, objectAnimated: false, environmentalFxAnimated: true, runtimeChanged: false, canonicalChanged: false, v20ThroughV27Changed: false })
assert.equal(register.v27Disposition, 'rejected-provenance-retained')

for (const name of ['bin-standard.png', 'bin-broken-overflowing.png']) {
  const file = path.join(rawDir, name)
  const image = png(file)
  assert.deepEqual([image.width, image.height], [72, 72], `${name} cell geometry changed`)
  assert.equal(sha(file), catalogue.outputs[name].sha256, `${name} hash drifted`)
  for (let x = 0; x < image.width; x++) {
    assert.equal(alpha(image, x, 0), 0, `${name} touches top edge`)
    assert.equal(alpha(image, x, image.height - 1), 0, `${name} touches bottom edge`)
  }
  for (let y = 0; y < image.height; y++) {
    assert.equal(alpha(image, 0, y), 0, `${name} touches left edge`)
    assert.equal(alpha(image, image.width - 1, y), 0, `${name} touches right edge`)
  }
  for (let i = 3; i < image.data.length; i += 4) assert.ok(image.data[i] === 0 || image.data[i] === 255, `${name} contains partial alpha`)
}

const standardBounds = catalogue.opaqueBounds.standard
const brokenBounds = catalogue.opaqueBounds.broken_overflowing
assert.equal(standardBounds[3], brokenBounds[3], 'states do not share the same floor contact')
assert.ok(brokenBounds[0] < standardBounds[0] && brokenBounds[2] > standardBounds[2], 'broken spill must extend beyond both sides of the standard footprint')
assert.ok(brokenBounds[1] < standardBounds[1], 'broken lid/contents must extend above the standard bin')

for (const name of ['kitchen-bin-standard-in-situ.png', 'kitchen-bin-broken-in-situ.png']) {
  const file = path.join(rawDir, name)
  const image = png(file)
  assert.deepEqual([image.width, image.height], [772, 224], `${name} room geometry changed`)
  assert.equal(sha(file), catalogue.outputs[name].sha256, `${name} hash drifted`)
}

assert.deepEqual(Object.keys(catalogue.effects), ['stench_miasma', 'slow_flies'])
for (const effect of Object.values(catalogue.effects)) {
  assert.equal(effect.reusable, true)
  assert.equal(effect.frames, 24)
  assert.equal(effect.fps, 4)
  assert.equal(effect.durationSeconds, 6)
  assert.equal(effect.objectPixelsChanged, false)
  assert.deepEqual(effect.cellPixels, [80, 80])
  const file = path.join(rawDir, effect.file)
  const image = png(file)
  assert.deepEqual([image.width, image.height], [80 * 24, 80], `${effect.file} strip geometry changed`)
  assert.equal(sha(file), catalogue.outputs[effect.file].sha256, `${effect.file} hash drifted`)
  const hashes = new Set()
  for (let frame = 0; frame < 24; frame++) {
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
  assert.ok(hashes.size >= 18, `${effect.file} needs enough distinct poses for a slow six-second loop`)
}
const stench = png(path.join(rawDir, catalogue.effects.stench_miasma.file))
for (let frame = 0; frame < 24; frame++) {
  let sourcePixels = 0
  for (let y = 63; y <= 70; y++) for (let x = 36; x <= 44; x++) if (alpha(stench, frame * 80 + x, y) > 0) sourcePixels++
  assert.ok(sourcePixels >= 4, `stench frame ${frame} is detached from the bin opening`)
}

const page = fs.readFileSync(pageFile, 'utf8')
const nextConfig = fs.readFileSync(path.join(root, 'next.config.mjs'), 'utf8')
assert.match(page, /coordinated two-state family/)
assert.match(page, /bin itself is static in both states/)
assert.match(page, /24 frames · 4 fps · 6 seconds/)
assert.match(page, /data-strip data-frames="24" data-fps="4"/)
assert.match(page, /AudioContext/)
assert.match(page, /actual game size/)
assert.match(page, /Promise\.all\(media\.map/)
assert.match(nextConfig, /source: '\/keeper-review\/kitchen-bin-states-v28'/)

if (fs.existsSync(archiveFile)) {
  const archive = JSON.parse(fs.readFileSync(archiveFile, 'utf8'))
  assert.equal(Object.keys(archive.entries).length, 6)
  for (const record of Object.values(archive.entries)) assert.equal(sha(path.join(root, record.object)), record.sha256)
}

console.log('Kitchen V28 bin states verified: static object, 2 reusable 24-frame/4-fps environmental loops, and 2 native-scale room proofs')
