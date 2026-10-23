import assert from 'node:assert/strict'
import crypto from 'node:crypto'
import fs from 'node:fs'
import path from 'node:path'
import { execFileSync } from 'node:child_process'
import { fileURLToPath } from 'node:url'
import { PNG } from 'pngjs'

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..')
const sha256 = bytes => crypto.createHash('sha256').update(bytes).digest('hex')
execFileSync(process.execPath, ['scripts/build_keeper_prime_morning_drafts_v11.mjs', '--check'], { cwd: root, stdio: 'inherit' })

const v10Bytes = fs.readFileSync(path.join(root, 'data/keeper_prime_animation_drafts_v10.json'))
const v10 = JSON.parse(v10Bytes)
const v6 = JSON.parse(fs.readFileSync(path.join(root, 'data/keeper_prime_animation_drafts_v6.json')))
const v11 = JSON.parse(fs.readFileSync(path.join(root, 'data/keeper_prime_animation_drafts_v11.json')))
const v6Archive = JSON.parse(fs.readFileSync(path.join(root, 'review-archive/sets/keeper-prime-morning-drafts-v6.json')))
const corrections = JSON.parse(fs.readFileSync(path.join(root, 'art/drafts/keeper-prime-morning-drafts-corrections-2026-10-23-v11/corrections.json')))
const register = JSON.parse(fs.readFileSync(path.join(root, 'art/drafts/keeper-prime-morning-drafts-corrections-2026-10-23-v11/batch-register.json')))
const setManifestFile = path.join(root, 'review-archive/sets/keeper-prime-morning-drafts-v11.json')
const setManifest = fs.existsSync(setManifestFile) ? JSON.parse(fs.readFileSync(setManifestFile)) : null
const authorityHash = '31dbac4efc00089fe6f831dc23f8397b4e3a8faf4d4aaa09a92b2ff407eebc35'
const authority = PNG.sync.read(fs.readFileSync(path.join(root, 'review-archive/objects/31', `${authorityHash}.png`)))

const archived = (frame, archive) => fs.readFileSync(path.join(root, archive.entries[frame.src].object))
function bytesFor(frame) {
  const publicFile = path.join(root, 'public', frame.src.slice(1))
  if (fs.existsSync(publicFile)) return fs.readFileSync(publicFile)
  assert.ok(setManifest, `No V11 archive manifest for ${frame.src}`)
  return fs.readFileSync(path.join(root, setManifest.entries[frame.src].object))
}
const opaqueBounds = image => {
  let x0 = 256; let y0 = 320; let x1 = -1; let y1 = -1
  for (let y = 0; y < 320; y += 1) for (let x = 0; x < 256; x += 1) if (image.data[(y * 256 + x) * 4 + 3] >= 128) {
    x0 = Math.min(x0, x); y0 = Math.min(y0, y); x1 = Math.max(x1, x); y1 = Math.max(y1, y)
  }
  return { x0, y0, x1, y1, height: y1 - y0 + 1 }
}

assert.equal(v11.version, 11)
assert.equal(v11.status, 'approved-body-complete-arm-choreography-review')
assert.equal(v11.sequences.length, 10)
assert.equal(v11.sequences.reduce((sum, sequence) => sum + sequence.frames.length, 0), 162)
assert.equal(corrections.sourceBatchSha256, sha256(v10Bytes))
assert.equal(corrections.rejectedAmendment.version, 10)
assert.match(corrections.rejectedAmendment.reason, /row-125.*cropped/i)
assert.equal(corrections.authority.completeRearBody, authorityHash)
assert.equal(corrections.frames.length, 21)
assert.equal(register.set, 'keeper-prime-morning-drafts-v11')

const v10ById = new Map(v10.sequences.map(sequence => [sequence.id, sequence]))
const v11ById = new Map(v11.sequences.map(sequence => [sequence.id, sequence]))
let changed = 0
for (const sequence of v11.sequences) {
  const previous = v10ById.get(sequence.id)
  assert.equal(sequence.frames.length, previous.frames.length)
  sequence.frames.forEach((frame, index) => {
    assert.deepEqual(frame.priorV10, { position: index + 1, sha256: previous.frames[index].sha256 })
    assert.ok(frame.src.startsWith('/keeper-review/keeper-prime-morning-drafts-v11/assets/'))
    if (frame.sha256 !== previous.frames[index].sha256) changed += 1
  })
}
assert.equal(changed, 21, 'V11 must change only the 21 cropped V10 rear-task composites')

const v6Rear = v6.sequences.find(sequence => sequence.id === 'rear-work-turn-return-v1')
const neutral = PNG.sync.read(archived(v6Rear.frames[9], v6Archive))
const repaired = v11ById.get('rear-work-turn-return-v1').frames.slice(10, 31)
const authorityBounds = opaqueBounds(authority)
let raisedExtensionTotal = 0
const actionHashes = new Set()
for (const frame of repaired) {
  const position = frame.priorV10.position
  const image = PNG.sync.read(bytesFor(frame))
  const source = PNG.sync.read(archived(v6Rear.frames[position - 1], v6Archive))
  const record = corrections.frames.find(item => item.position === position)
  assert.deepEqual(record.restingArmClear, { y0: 115, y1: 242, leftMaxX: 81, rightMinX: 174 })
  assert.deepEqual(record.actionArmCopy, { y0: 70, y1: 242, shoulderY: 115, leftMaxX: 95, rightMinX: 160, alphaThreshold: 16, neutralExclusionRadius: 2, neutralFramePosition: 10 })
  assert.equal(frame.amendmentComparison.label, 'Rejected V10 cropped arm mask')
  let copiedActionPixels = 0
  let copiedPixelsAboveV10Cutoff = 0
  let raisedExtensionPixels = 0
  let changedPixels = 0
  const neutralNearby = (x, y) => {
    for (let yy = Math.max(0, y - 2); yy <= Math.min(319, y + 2); yy += 1) for (let xx = Math.max(0, x - 2); xx <= Math.min(255, x + 2); xx += 1) {
      if (neutral.data[(yy * 256 + xx) * 4 + 3] >= 16) return true
    }
    return false
  }
  for (let y = 0; y < 320; y += 1) for (let x = 0; x < 256; x += 1) {
    const offset = (y * 256 + x) * 4
    const outerCopy = x <= 95 || x >= 160
    const sourceOpaque = source.data[offset + 3] >= 16
    const upperExtension = y >= 70 && y < 115 && outerCopy && sourceOpaque && authority.data[offset + 3] < 16 && !neutralNearby(x, y)
    const normalArm = y >= 115 && y <= 242 && outerCopy && sourceOpaque
    const cleared = y >= 115 && y <= 242 && (x <= 81 || x >= 174)
    const expected = upperExtension || normalArm ? source.data.subarray(offset, offset + 4) : cleared ? Buffer.from([0, 0, 0, 0]) : authority.data.subarray(offset, offset + 4)
    assert.ok(image.data.subarray(offset, offset + 4).equals(expected), `${frame.id} violates complete-arm ownership at y${y} x${x}`)
    if (upperExtension || normalArm) {
      copiedActionPixels += 1
      if (y < 125) copiedPixelsAboveV10Cutoff += 1
      if (y < 115) raisedExtensionPixels += 1
    }
    if (!image.data.subarray(offset, offset + 4).equals(authority.data.subarray(offset, offset + 4))) changedPixels += 1
    if (y < 115 && authority.data[offset + 3] >= 16) assert.ok(image.data.subarray(offset, offset + 4).equals(authority.data.subarray(offset, offset + 4)), `${frame.id} changed approved head pixels`)
  }
  assert.equal(record.copiedActionPixels, copiedActionPixels)
  assert.equal(record.copiedPixelsAboveV10Cutoff, copiedPixelsAboveV10Cutoff)
  assert.equal(record.raisedExtensionPixels, raisedExtensionPixels)
  assert.equal(record.changedPixels, changedPixels)
  assert.ok(copiedPixelsAboveV10Cutoff > 0, `${frame.id} still uses the cropped V10 upper boundary`)
  raisedExtensionTotal += raisedExtensionPixels
  const bounds = opaqueBounds(image)
  assert.equal(bounds.y0, authorityBounds.y0)
  assert.equal(bounds.y1, authorityBounds.y1)
  assert.equal(bounds.height, authorityBounds.height)
  for (let y = 0; y < 320; y += 1) for (let x = 96; x <= 159; x += 1) {
    const offset = (y * 256 + x) * 4
    assert.ok(image.data.subarray(offset, offset + 4).equals(authority.data.subarray(offset, offset + 4)), `${frame.id} changed the protected central Prime body`)
  }
  let edgeAlpha = 0
  for (let x = 0; x < 256; x += 1) edgeAlpha += Number(Boolean(image.data[x * 4 + 3])) + Number(Boolean(image.data[(319 * 256 + x) * 4 + 3]))
  for (let y = 0; y < 320; y += 1) edgeAlpha += Number(Boolean(image.data[(y * 256) * 4 + 3])) + Number(Boolean(image.data[(y * 256 + 255) * 4 + 3]))
  assert.equal(edgeAlpha, 0)
  actionHashes.add(sha256(image.data))
}
assert.ok(raisedExtensionTotal > 100, 'V11 failed to restore raised arm and hand pixels above the shoulders')
assert.ok(actionHashes.size > 10, 'V11 froze the arm choreography')

const allFrames = v11.sequences.flatMap(sequence => sequence.frames)
assert.equal(new Set(allFrames.map(frame => frame.id)).size, allFrames.length)
assert.equal(new Set(allFrames.map(frame => frame.redraftSlot)).size, allFrames.length)
assert.equal(register.publishedAssets.length, new Set(allFrames.map(frame => frame.src)).size)
const component = fs.readFileSync(path.join(root, 'src/prime-keeper-drafts/PrimeKeeperDraftReview.tsx'), 'utf8')
assert.match(component, /useState\(batch\.version === 10\)/, 'V11 alignment ghost is not off by default')
for (const phrase of ['Show Prime ghost', 'Hide Prime ghost', 'Prime ghost opacity']) assert.ok(component.includes(phrase))
assert.match(fs.readFileSync(path.join(root, 'src/app/prime-keeper-animation-drafts/page.tsx'), 'utf8'), /keeper_prime_animation_drafts_v11/)
assert.match(fs.readFileSync(path.join(root, 'src/app/prime-keeper-animation-drafts-v11/page.tsx'), 'utf8'), /keeper_prime_animation_drafts_v11/)
assert.match(fs.readFileSync(path.join(root, 'src/app/prime-keeper-animation-drafts-v10/page.tsx'), 'utf8'), /keeper_prime_animation_drafts_v10/)
if (setManifest) for (const asset of register.publishedAssets) {
  const url = `/${asset.publicAssemblyPath.replace(/^public\//, '')}`
  assert.equal(setManifest.entries[url].sha256, asset.sourceSha256)
}
console.log(`Verified Prime morning draft V11: ${allFrames.length} frame occurrences, ${register.publishedAssets.length} unique assets, 21 complete-arm repairs, ${raisedExtensionTotal} raised-extension pixels.`)
