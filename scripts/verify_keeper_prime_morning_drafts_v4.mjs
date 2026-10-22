import assert from 'node:assert/strict'
import crypto from 'node:crypto'
import fs from 'node:fs'
import path from 'node:path'
import { execFileSync } from 'node:child_process'
import { fileURLToPath } from 'node:url'
import { PNG } from 'pngjs'

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..')
const sha256 = (bytes) => crypto.createHash('sha256').update(bytes).digest('hex')
execFileSync(process.execPath, ['scripts/build_keeper_prime_morning_drafts_v4.mjs', '--check'], { cwd: root, stdio: 'inherit' })

const v3Bytes = fs.readFileSync(path.join(root, 'data/keeper_prime_animation_drafts_v3.json'))
const v3 = JSON.parse(v3Bytes)
const v3Archive = JSON.parse(fs.readFileSync(path.join(root, 'review-archive/sets/keeper-prime-morning-drafts-v3.json')))
const v4 = JSON.parse(fs.readFileSync(path.join(root, 'data/keeper_prime_animation_drafts_v4.json')))
const corrections = JSON.parse(fs.readFileSync(path.join(root, 'art/drafts/keeper-prime-morning-drafts-corrections-2026-10-22-v4/corrections.json')))
const register = JSON.parse(fs.readFileSync(path.join(root, 'art/drafts/keeper-prime-morning-drafts-corrections-2026-10-22-v4/batch-register.json')))
const setManifestFile = path.join(root, 'review-archive/sets/keeper-prime-morning-drafts-v4.json')
const authorityHash = '31dbac4efc00089fe6f831dc23f8397b4e3a8faf4d4aaa09a92b2ff407eebc35'
const authority = PNG.sync.read(fs.readFileSync(path.join(root, 'review-archive/objects/31', `${authorityHash}.png`)))

assert.equal(v4.version, 4)
assert.equal(v4.status, 'feedback-corrected-review-only')
assert.equal(v4.sequences.length, 10)
assert.equal(v4.sequences.reduce((sum, sequence) => sum + sequence.frames.length, 0), 162)
assert.equal(corrections.sourceBatchSha256, sha256(v3Bytes))
assert.match(corrections.rejectedAmendment.reason, /two vertical cut seams/i)
assert.equal(corrections.imageGeneration.usedInDelivery, false)
assert.equal(register.set, 'keeper-prime-morning-drafts-v4')
assert.equal(corrections.frames.length, 21)

const setManifest = fs.existsSync(setManifestFile) ? JSON.parse(fs.readFileSync(setManifestFile)) : null
function bytesFor(frame) {
  const publicFile = path.join(root, 'public', frame.src.slice(1))
  if (fs.existsSync(publicFile)) return fs.readFileSync(publicFile)
  assert.ok(setManifest, `No public asset or archive manifest for ${frame.src}`)
  return fs.readFileSync(path.join(root, setManifest.entries[frame.src].object))
}
function v3BytesFor(frame) {
  const entry = v3Archive.entries[frame.src]
  assert.ok(entry, `Missing V3 archive entry for ${frame.src}`)
  return fs.readFileSync(path.join(root, entry.object))
}

const v3ById = new Map(v3.sequences.map((sequence) => [sequence.id, sequence]))
const v4ById = new Map(v4.sequences.map((sequence) => [sequence.id, sequence]))
let changed = 0
for (const sequence of v4.sequences) {
  const previous = v3ById.get(sequence.id)
  assert.equal(sequence.frames.length, previous.frames.length)
  sequence.frames.forEach((frame, index) => {
    assert.equal(frame.priorV3.position, index + 1)
    assert.equal(frame.priorV3.sha256, previous.frames[index].sha256)
    assert.ok(frame.src.startsWith('/keeper-review/keeper-prime-morning-drafts-v4/assets/'))
    if (frame.sha256 !== previous.frames[index].sha256) changed += 1
    else assert.equal(sha256(bytesFor(frame)), previous.frames[index].sha256, `${frame.id} did not preserve V3 bytes`)
  })
}
assert.equal(changed, 21, 'V4 must change only the 21 rejected rear-task repairs')

const rear = v4ById.get('rear-work-turn-return-v1')
const repaired = rear.frames.slice(10, 31)
assert.equal(repaired.length, 21)
const lowerReference = PNG.sync.read(bytesFor(repaired[0])).data.subarray(204 * 256 * 4)
for (const frame of repaired) {
  assert.match(frame.correction, /continuous authority hem/)
  const image = PNG.sync.read(bytesFor(frame))
  const previous = v3ById.get('rear-work-turn-return-v1').frames[frame.priorV3.position - 1]
  const previousImage = PNG.sync.read(v3BytesFor(previous))
  assert.ok(image.data.subarray(0, 204 * 256 * 4).equals(previousImage.data.subarray(0, 204 * 256 * 4)), `${frame.id} changed head, beard, cap, stripe or upper action drawing`)
  assert.ok(image.data.subarray(204 * 256 * 4).equals(lowerReference), `${frame.id} lower body differs`)

  for (let y = 204; y <= 227; y += 1) for (let x = 0; x < 256; x += 1) {
    const offset = (y * 256 + x) * 4
    const pixel = image.data.subarray(offset, offset + 4)
    if (pixel[3] > 0) assert.ok(pixel.equals(authority.data.subarray(offset, offset + 4)), `${frame.id} y${y} x${x} is not exact authority hem data`)
    if (x < 76 || x > 179) assert.equal(pixel[3], 0, `${frame.id} retains a hip/hand fragment at y${y} x${x}`)
  }
  for (let y = 228; y < 320; y += 1) for (let x = 0; x < 256; x += 1) {
    const offset = (y * 256 + x) * 4
    const expected = x >= 70 && x <= 186 ? authority.data.subarray(offset, offset + 4) : Buffer.from([0, 0, 0, 0])
    assert.ok(image.data.subarray(offset, offset + 4).equals(expected), `${frame.id} lower body differs from authority at y${y} x${x}`)
  }

  let edgeAlpha = 0
  for (let x = 0; x < 256; x += 1) edgeAlpha += Number(Boolean(image.data[x * 4 + 3])) + Number(Boolean(image.data[((319 * 256) + x) * 4 + 3]))
  for (let y = 0; y < 320; y += 1) edgeAlpha += Number(Boolean(image.data[(y * 256) * 4 + 3])) + Number(Boolean(image.data[(y * 256 + 255) * 4 + 3]))
  assert.equal(edgeAlpha, 0, `${frame.id} lost its transparent safety gutter`)
}

const allFrames = v4.sequences.flatMap((sequence) => sequence.frames)
assert.equal(new Set(allFrames.map((frame) => frame.id)).size, allFrames.length)
assert.equal(new Set(allFrames.map((frame) => frame.redraftSlot)).size, allFrames.length)
assert.equal(register.publishedAssets.length, new Set(allFrames.map((frame) => frame.src)).size)
for (const name of ['front', 'back']) assert.ok(allFrames.some((frame) => frame.sha256 === v4.reviewAuthorities[name].sha256), `${name} review authority is not displayed`)

const component = fs.readFileSync(path.join(root, 'src/prime-keeper-drafts/PrimeKeeperDraftReview.tsx'), 'utf8')
for (const phrase of ['image.decode', 'Ⅱ Pause', '← Frame', 'Frame →', '■ Stop', 'Draft sequence sandbox', 'reviewAuthorities', 'amendmentComparison']) assert.ok(component.includes(phrase), `review UI omits ${phrase}`)
assert.match(fs.readFileSync(path.join(root, 'src/app/prime-keeper-animation-drafts/page.tsx'), 'utf8'), /keeper_prime_animation_drafts_v4/)
assert.match(fs.readFileSync(path.join(root, 'src/app/prime-keeper-animation-drafts-v4/page.tsx'), 'utf8'), /keeper_prime_animation_drafts_v4/)

if (setManifest) {
  assert.equal(Object.keys(setManifest.entries).length, register.publishedAssets.length)
  for (const asset of register.publishedAssets) {
    const url = `/${asset.publicAssemblyPath.replace(/^public\//, '')}`
    assert.equal(setManifest.entries[url].sha256, asset.sourceSha256)
  }
}

console.log(`Verified Prime morning draft V4: ${allFrames.length} frame occurrences, ${register.publishedAssets.length} unique assets, 21 authority-locked rear seam repairs.`)
