import assert from 'node:assert/strict'
import crypto from 'node:crypto'
import fs from 'node:fs'
import path from 'node:path'
import { execFileSync } from 'node:child_process'
import { fileURLToPath } from 'node:url'
import { PNG } from 'pngjs'

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..')
const sha256 = (bytes) => crypto.createHash('sha256').update(bytes).digest('hex')
execFileSync(process.execPath, ['scripts/build_keeper_prime_morning_drafts_v3.mjs', '--check'], { cwd: root, stdio: 'inherit' })

const v2Bytes = fs.readFileSync(path.join(root, 'data/keeper_prime_animation_drafts_v2.json'))
const v2 = JSON.parse(v2Bytes)
const v3 = JSON.parse(fs.readFileSync(path.join(root, 'data/keeper_prime_animation_drafts_v3.json')))
const corrections = JSON.parse(fs.readFileSync(path.join(root, 'art/drafts/keeper-prime-morning-drafts-corrections-2026-10-22-v3/corrections.json')))
const register = JSON.parse(fs.readFileSync(path.join(root, 'art/drafts/keeper-prime-morning-drafts-corrections-2026-10-22-v3/batch-register.json')))
const setManifestFile = path.join(root, 'review-archive/sets/keeper-prime-morning-drafts-v3.json')

assert.equal(v3.version, 3)
assert.equal(v3.status, 'feedback-corrected-review-only')
assert.equal(v3.sequences.length, 10)
assert.equal(v3.sequences.reduce((sum, sequence) => sum + sequence.frames.length, 0), 162)
assert.equal(corrections.sourceBatchSha256, sha256(v2Bytes))
assert.equal(corrections.imageGenerationStudy.usedInDelivery, false)
assert.equal(register.set, 'keeper-prime-morning-drafts-v3')

const byId = new Map(v3.sequences.map((sequence) => [sequence.id, sequence]))
const lift = byId.get('lift-enter-exit-v1')
assert.equal(lift.frames.length, 7)
assert.ok(!lift.frames.some((frame) => frame.priorV2.sha256 === '55305750610604207ffd8d293d41f3418a7296c61d7a613d3ba9c728f52f8fd7'))
assert.equal(byId.get('diary-turn-sit-write-return-v1').title, 'Turn, sit, hold, stand and return')

const allFrames = v3.sequences.flatMap((sequence) => sequence.frames)
assert.equal(new Set(allFrames.map((frame) => frame.id)).size, allFrames.length)
assert.equal(new Set(allFrames.map((frame) => frame.redraftSlot)).size, allFrames.length)
assert.ok(allFrames.every((frame) => frame.src.startsWith('/keeper-review/keeper-prime-morning-drafts-v3/assets/')))
assert.equal(register.publishedAssets.length, new Set(allFrames.map((frame) => frame.src)).size)

function bytesFor(frame) {
  const publicFile = path.join(root, 'public', frame.src.slice(1))
  if (fs.existsSync(publicFile)) return fs.readFileSync(publicFile)
  const setManifest = JSON.parse(fs.readFileSync(setManifestFile))
  return fs.readFileSync(path.join(root, setManifest.entries[frame.src].object))
}
function mask(image) {
  const result = []
  for (let y = 112; y < 226; y += 1) for (let x = 28; x < image.width - 28; x += 1) {
    const offset = (y * image.width + x) * 4
    const r = image.data[offset], g = image.data[offset + 1], b = image.data[offset + 2], a = image.data[offset + 3]
    if (a > 0 && b > g * 1.18 && g > r + 18 && b > r + 42) result.push([r, g, b])
  }
  return result
}
function median(values) { const sorted = [...values].sort((a, b) => a - b); return sorted[Math.floor(sorted.length / 2)] }

for (const name of ['front', 'back']) {
  const authority = v3.reviewAuthorities[name]
  const frame = allFrames.find((item) => item.sha256 === authority.sha256)
  assert.ok(frame, `${name} corrected review authority is not displayed`)
  const bytes = bytesFor(frame)
  assert.equal(sha256(bytes), authority.sha256)
  const image = PNG.sync.read(bytes)
  const colours = mask(image)
  assert.ok(colours.length > 4000)
  assert.ok(median(colours.map((rgb) => rgb[1])) >= 100, `${name} jumper green channel is still too dark`)
  assert.ok(median(colours.map((rgb) => rgb[2])) >= 215, `${name} jumper blue channel is still too dark`)
  const originalHash = name === 'front' ? 'a9a5c37fe72221992ec499fa3096fdd0581977b4ac03ff7788da2af411107a2e' : 'd3e7c44b241030c02023f5f5aa8dbf7953162489f7c8b6c1f0b5ad72b321e1bd'
  const original = PNG.sync.read(fs.readFileSync(path.join(root, 'review-archive/objects', originalHash.slice(0, 2), `${originalHash}.png`)))
  for (let offset = 3; offset < image.data.length; offset += 4) assert.equal(image.data[offset], original.data[offset], `${name} alpha geometry changed`)
}

const rear = byId.get('rear-work-turn-return-v1')
const repaired = rear.frames.slice(10, 31)
assert.equal(repaired.length, 21)
const lowerReference = PNG.sync.read(bytesFor(repaired[0])).data.subarray(205 * 256 * 4)
for (const frame of repaired) {
  assert.match(frame.correction, /recentered/)
  const image = PNG.sync.read(bytesFor(frame))
  assert.ok(image.data.subarray(205 * 256 * 4).equals(lowerReference), `${frame.id} lower body differs`)
  let edgeAlpha = 0
  for (let x = 0; x < 256; x += 1) edgeAlpha += Number(Boolean(image.data[x * 4 + 3])) + Number(Boolean(image.data[((319 * 256) + x) * 4 + 3]))
  for (let y = 0; y < 320; y += 1) edgeAlpha += Number(Boolean(image.data[(y * 256) * 4 + 3])) + Number(Boolean(image.data[(y * 256 + 255) * 4 + 3]))
  assert.equal(edgeAlpha, 0, `${frame.id} lost its transparent safety gutter`)
}

const component = fs.readFileSync(path.join(root, 'src/prime-keeper-drafts/PrimeKeeperDraftReview.tsx'), 'utf8')
for (const phrase of ['image.decode', 'Ⅱ Pause', '← Frame', 'Frame →', '■ Stop', 'Draft sequence sandbox', 'reviewAuthorities']) assert.ok(component.includes(phrase), `review UI omits ${phrase}`)
assert.match(fs.readFileSync(path.join(root, 'src/app/prime-keeper-animation-drafts/page.tsx'), 'utf8'), /keeper_prime_animation_drafts_v3/)
assert.match(fs.readFileSync(path.join(root, 'src/app/prime-keeper-animation-drafts-v3/page.tsx'), 'utf8'), /keeper_prime_animation_drafts_v3/)

if (fs.existsSync(setManifestFile)) {
  const archived = JSON.parse(fs.readFileSync(setManifestFile))
  assert.equal(Object.keys(archived.entries).length, register.publishedAssets.length)
  for (const asset of register.publishedAssets) {
    const url = `/${asset.publicAssemblyPath.replace(/^public\//, '')}`
    assert.equal(archived.entries[url].sha256, asset.sourceSha256)
  }
}

console.log(`Verified Prime morning draft V3: ${allFrames.length} frame occurrences, ${register.publishedAssets.length} unique assets, 31 feedback corrections.`)
