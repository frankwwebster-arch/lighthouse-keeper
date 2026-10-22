import assert from 'node:assert/strict'
import crypto from 'node:crypto'
import fs from 'node:fs'
import path from 'node:path'
import { execFileSync } from 'node:child_process'
import { fileURLToPath } from 'node:url'
import { PNG } from 'pngjs'

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..')
const sha256 = (bytes) => crypto.createHash('sha256').update(bytes).digest('hex')
execFileSync(process.execPath, ['scripts/build_keeper_prime_morning_drafts_v5.mjs', '--check'], { cwd: root, stdio: 'inherit' })

const v4Bytes = fs.readFileSync(path.join(root, 'data/keeper_prime_animation_drafts_v4.json'))
const v4 = JSON.parse(v4Bytes)
const v4Archive = JSON.parse(fs.readFileSync(path.join(root, 'review-archive/sets/keeper-prime-morning-drafts-v4.json')))
const v5 = JSON.parse(fs.readFileSync(path.join(root, 'data/keeper_prime_animation_drafts_v5.json')))
const corrections = JSON.parse(fs.readFileSync(path.join(root, 'art/drafts/keeper-prime-morning-drafts-corrections-2026-10-22-v5/corrections.json')))
const register = JSON.parse(fs.readFileSync(path.join(root, 'art/drafts/keeper-prime-morning-drafts-corrections-2026-10-22-v5/batch-register.json')))
const setManifestFile = path.join(root, 'review-archive/sets/keeper-prime-morning-drafts-v5.json')
const authorityHash = '31dbac4efc00089fe6f831dc23f8397b4e3a8faf4d4aaa09a92b2ff407eebc35'
const authority = PNG.sync.read(fs.readFileSync(path.join(root, 'review-archive/objects/31', `${authorityHash}.png`)))

assert.equal(v5.version, 5)
assert.equal(v5.status, 'feedback-corrected-review-only')
assert.equal(v5.sequences.length, 10)
assert.equal(v5.sequences.reduce((sum, sequence) => sum + sequence.frames.length, 0), 162)
assert.equal(corrections.sourceBatchSha256, sha256(v4Bytes))
assert.match(corrections.rejectedAmendment.reason, /second fixed hem/i)
assert.match(corrections.rejectedAmendment.reason, /detached authority fragments/i)
assert.equal(corrections.imageGeneration.usedInDelivery, false)
assert.equal(register.set, 'keeper-prime-morning-drafts-v5')
assert.equal(corrections.frames.length, 21)

const setManifest = fs.existsSync(setManifestFile) ? JSON.parse(fs.readFileSync(setManifestFile)) : null
function bytesFor(frame) {
  const publicFile = path.join(root, 'public', frame.src.slice(1))
  if (fs.existsSync(publicFile)) return fs.readFileSync(publicFile)
  assert.ok(setManifest, `No public asset or archive manifest for ${frame.src}`)
  return fs.readFileSync(path.join(root, setManifest.entries[frame.src].object))
}
function v4BytesFor(frame) {
  const entry = v4Archive.entries[frame.src]
  assert.ok(entry, `Missing V4 archive entry for ${frame.src}`)
  return fs.readFileSync(path.join(root, entry.object))
}
function sourceV2Image(frame) {
  const hash = frame.priorV2.sha256
  return PNG.sync.read(fs.readFileSync(path.join(root, 'review-archive/objects', hash.slice(0, 2), `${hash}.png`)))
}

const v4ById = new Map(v4.sequences.map((sequence) => [sequence.id, sequence]))
const v5ById = new Map(v5.sequences.map((sequence) => [sequence.id, sequence]))
let changed = 0
for (const sequence of v5.sequences) {
  const previous = v4ById.get(sequence.id)
  assert.equal(sequence.frames.length, previous.frames.length)
  sequence.frames.forEach((frame, index) => {
    assert.equal(frame.priorV4.position, index + 1)
    assert.equal(frame.priorV4.sha256, previous.frames[index].sha256)
    assert.ok(frame.src.startsWith('/keeper-review/keeper-prime-morning-drafts-v5/assets/'))
    if (frame.sha256 !== previous.frames[index].sha256) changed += 1
    else assert.equal(sha256(bytesFor(frame)), previous.frames[index].sha256, `${frame.id} did not preserve V4 bytes`)
  })
}
assert.equal(changed, 21, 'V5 must change only the 21 rejected rear-task composites')

const rear = v5ById.get('rear-work-turn-return-v1')
const repaired = rear.frames.slice(10, 31)
assert.equal(repaired.length, 21)
const hemHashes = new Set()
for (const frame of repaired) {
  assert.match(frame.correction, /complete moving V2 jumper hem/)
  assert.equal(frame.amendmentComparison.label, 'Rejected V4 split-hem composite')
  const image = PNG.sync.read(bytesFor(frame))
  const previous = v4ById.get('rear-work-turn-return-v1').frames[frame.priorV4.position - 1]
  const previousImage = PNG.sync.read(v4BytesFor(previous))
  const record = corrections.frames.find((item) => item.position === frame.priorV4.position)
  const source = sourceV2Image(frame)
  assert.ok(record, `${frame.id} lacks a correction record`)
  assert.ok(image.data.subarray(0, 195 * 256 * 4).equals(previousImage.data.subarray(0, 195 * 256 * 4)), `${frame.id} changed head, beard, cap, stripe or upper action drawing`)

  // The visible moving hem is sourced only from the original action frame.
  // V4's fixed authority hem is never copied into rows 195–218.
  let movingHemPixels = 0
  for (let y = 195; y <= 218; y += 1) for (let x = 0; x < 256; x += 1) {
    const offset = (y * 256 + x) * 4
    const pixel = image.data.subarray(offset, offset + 4)
    if (!pixel[3]) continue
    movingHemPixels += 1
    const sourceX = x - record.recenterDx
    assert.ok(sourceX >= 0 && sourceX < 256, `${frame.id} moving hem escaped its source`)
    const sourceOffset = (y * 256 + sourceX) * 4
    assert.ok(pixel.equals(source.data.subarray(sourceOffset, sourceOffset + 4)), `${frame.id} moving hem pixel is neither exact nor source-owned at y${y} x${x}`)
    if (y >= 213) assert.ok(x >= 76 && x <= 180, `${frame.id} retains an outboard lower-seam fragment at y${y} x${x}`)
  }
  assert.ok(movingHemPixels > 1_000, `${frame.id} lost its moving hem`)
  hemHashes.add(sha256(image.data.subarray(195 * 256 * 4, 219 * 256 * 4)))

  // The approved trousers begin behind the moving hem, and the detached V4
  // authority fragments cannot survive outside the declared waist envelope.
  for (let y = 219; y <= 235; y += 1) for (let x = 0; x < 256; x += 1) {
    const offset = (y * 256 + x) * 4
    const pixel = image.data.subarray(offset, offset + 4)
    if (pixel[3]) assert.ok(pixel.equals(authority.data.subarray(offset, offset + 4)), `${frame.id} has non-authority trousers at y${y} x${x}`)
    if (x < 76 || x > 180) assert.equal(pixel[3], 0, `${frame.id} retains a detached waist fragment at y${y} x${x}`)
  }
  for (let y = 236; y < 320; y += 1) for (let x = 0; x < 256; x += 1) {
    const offset = (y * 256 + x) * 4
    const expected = x >= 70 && x <= 186 ? authority.data.subarray(offset, offset + 4) : Buffer.from([0, 0, 0, 0])
    assert.ok(image.data.subarray(offset, offset + 4).equals(expected), `${frame.id} lower authority body differs at y${y} x${x}`)
  }

  let edgeAlpha = 0
  for (let x = 0; x < 256; x += 1) edgeAlpha += Number(Boolean(image.data[x * 4 + 3])) + Number(Boolean(image.data[((319 * 256) + x) * 4 + 3]))
  for (let y = 0; y < 320; y += 1) edgeAlpha += Number(Boolean(image.data[(y * 256) * 4 + 3])) + Number(Boolean(image.data[(y * 256 + 255) * 4 + 3]))
  assert.equal(edgeAlpha, 0, `${frame.id} lost its transparent safety gutter`)
}
assert.ok(hemHashes.size > 10, 'V5 unexpectedly froze the moving jumper hem')

const allFrames = v5.sequences.flatMap((sequence) => sequence.frames)
assert.equal(new Set(allFrames.map((frame) => frame.id)).size, allFrames.length)
assert.equal(new Set(allFrames.map((frame) => frame.redraftSlot)).size, allFrames.length)
assert.equal(register.publishedAssets.length, new Set(allFrames.map((frame) => frame.src)).size)
for (const name of ['front', 'back']) assert.ok(allFrames.some((frame) => frame.sha256 === v5.reviewAuthorities[name].sha256), `${name} review authority is not displayed`)

const component = fs.readFileSync(path.join(root, 'src/prime-keeper-drafts/PrimeKeeperDraftReview.tsx'), 'utf8')
for (const phrase of ['image.decode', 'Ⅱ Pause', '← Frame', 'Frame →', '■ Stop', 'Draft sequence sandbox', 'reviewAuthorities', 'amendmentComparison']) assert.ok(component.includes(phrase), `review UI omits ${phrase}`)
assert.match(fs.readFileSync(path.join(root, 'src/app/prime-keeper-animation-drafts-v5/page.tsx'), 'utf8'), /keeper_prime_animation_drafts_v5/)

if (setManifest) {
  assert.equal(Object.keys(setManifest.entries).length, register.publishedAssets.length)
  for (const asset of register.publishedAssets) {
    const url = `/${asset.publicAssemblyPath.replace(/^public\//, '')}`
    assert.equal(setManifest.entries[url].sha256, asset.sourceSha256)
  }
}

console.log(`Verified Prime morning draft V5: ${allFrames.length} frame occurrences, ${register.publishedAssets.length} unique assets, 21 moving-hem ownership repairs.`)
