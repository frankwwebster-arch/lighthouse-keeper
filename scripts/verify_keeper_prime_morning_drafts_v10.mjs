import assert from 'node:assert/strict'
import crypto from 'node:crypto'
import fs from 'node:fs'
import path from 'node:path'
import { execFileSync } from 'node:child_process'
import { fileURLToPath } from 'node:url'
import { PNG } from 'pngjs'

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..')
const sha256 = (bytes) => crypto.createHash('sha256').update(bytes).digest('hex')
execFileSync(process.execPath, ['scripts/build_keeper_prime_morning_drafts_v10.mjs', '--check'], { cwd: root, stdio: 'inherit' })

const v9Bytes = fs.readFileSync(path.join(root, 'data/keeper_prime_animation_drafts_v9.json'))
const v9 = JSON.parse(v9Bytes)
const v6 = JSON.parse(fs.readFileSync(path.join(root, 'data/keeper_prime_animation_drafts_v6.json')))
const v10 = JSON.parse(fs.readFileSync(path.join(root, 'data/keeper_prime_animation_drafts_v10.json')))
const v9Archive = JSON.parse(fs.readFileSync(path.join(root, 'review-archive/sets/keeper-prime-morning-drafts-v9.json')))
const v6Archive = JSON.parse(fs.readFileSync(path.join(root, 'review-archive/sets/keeper-prime-morning-drafts-v6.json')))
const corrections = JSON.parse(fs.readFileSync(path.join(root, 'art/drafts/keeper-prime-morning-drafts-corrections-2026-10-23-v10/corrections.json')))
const register = JSON.parse(fs.readFileSync(path.join(root, 'art/drafts/keeper-prime-morning-drafts-corrections-2026-10-23-v10/batch-register.json')))
const setManifestFile = path.join(root, 'review-archive/sets/keeper-prime-morning-drafts-v10.json')
const setManifest = fs.existsSync(setManifestFile) ? JSON.parse(fs.readFileSync(setManifestFile)) : null
const authorityHash = '31dbac4efc00089fe6f831dc23f8397b4e3a8faf4d4aaa09a92b2ff407eebc35'
const authority = PNG.sync.read(fs.readFileSync(path.join(root, 'review-archive/objects/31', `${authorityHash}.png`)))

function archived(frame, archive) {
  const entry = archive.entries[frame.src]
  assert.ok(entry, `Missing archive entry for ${frame.src}`)
  return fs.readFileSync(path.join(root, entry.object))
}

function bytesFor(frame) {
  const publicFile = path.join(root, 'public', frame.src.slice(1))
  if (fs.existsSync(publicFile)) return fs.readFileSync(publicFile)
  assert.ok(setManifest, `No V10 archive manifest for ${frame.src}`)
  return fs.readFileSync(path.join(root, setManifest.entries[frame.src].object))
}

function inRegion(x, y, region) {
  return y >= region.y0 && y <= region.y1 && (x <= region.leftMaxX || x >= region.rightMinX)
}

function opaqueBounds(image) {
  let x0 = 256; let y0 = 320; let x1 = -1; let y1 = -1
  for (let y = 0; y < 320; y += 1) for (let x = 0; x < 256; x += 1) {
    if (image.data[(y * 256 + x) * 4 + 3] < 128) continue
    x0 = Math.min(x0, x); y0 = Math.min(y0, y); x1 = Math.max(x1, x); y1 = Math.max(y1, y)
  }
  return { x0, y0, x1, y1, width: x1 - x0 + 1, height: y1 - y0 + 1 }
}

assert.equal(v10.version, 10)
assert.equal(v10.status, 'approved-body-arm-choreography-review')
assert.equal(v10.sequences.length, 10)
assert.equal(v10.sequences.reduce((sum, sequence) => sum + sequence.frames.length, 0), 162)
assert.equal(corrections.sourceBatchSha256, sha256(v9Bytes))
assert.equal(corrections.rejectedAmendment.version, 9)
assert.match(corrections.rejectedAmendment.reason, /visibly assembled/i)
assert.equal(corrections.imageGeneration.usedInDelivery, false)
assert.match(corrections.imageGeneration.reason, /generated redraw.*rejected/i)
assert.equal(corrections.authority.completeRearBody, authorityHash)
assert.equal(corrections.frames.length, 21)
assert.equal(register.set, 'keeper-prime-morning-drafts-v10')

const v6ById = new Map(v6.sequences.map((sequence) => [sequence.id, sequence]))
const v9ById = new Map(v9.sequences.map((sequence) => [sequence.id, sequence]))
const v10ById = new Map(v10.sequences.map((sequence) => [sequence.id, sequence]))
let changed = 0
for (const sequence of v10.sequences) {
  const previous = v9ById.get(sequence.id)
  assert.equal(sequence.frames.length, previous.frames.length)
  sequence.frames.forEach((frame, index) => {
    assert.deepEqual(frame.priorV9, { position: index + 1, sha256: previous.frames[index].sha256 })
    assert.ok(frame.src.startsWith('/keeper-review/keeper-prime-morning-drafts-v10/assets/'))
    if (frame.sha256 !== previous.frames[index].sha256) changed += 1
    else assert.equal(sha256(bytesFor(frame)), previous.frames[index].sha256)
  })
}
assert.equal(changed, 21, 'V10 must change only the 21 rejected V9 rear-task composites')

const repaired = v10ById.get('rear-work-turn-return-v1').frames.slice(10, 31)
const v6Rear = v6ById.get('rear-work-turn-return-v1')
const authorityBounds = opaqueBounds(authority)
const actionHashes = new Set()
for (const frame of repaired) {
  const position = frame.priorV9.position
  const image = PNG.sync.read(bytesFor(frame))
  const source = PNG.sync.read(archived(v6Rear.frames[position - 1], v6Archive))
  const record = corrections.frames.find((item) => item.position === position)
  assert.equal(record.bodyAuthoritySha256, authorityHash)
  assert.deepEqual(record.restingArmClear, { y0: 132, y1: 242, leftMaxX: 81, rightMinX: 174 })
  assert.deepEqual(record.actionArmCopy, { y0: 125, y1: 226, leftMaxX: 95, rightMinX: 160, alphaThreshold: 16 })
  assert.equal(frame.amendmentComparison.label, 'Rejected V9 torso/lower-body splice')

  let changedPixels = 0
  let copiedActionPixels = 0
  for (let y = 0; y < 320; y += 1) for (let x = 0; x < 256; x += 1) {
    const offset = (y * 256 + x) * 4
    const sourceOpaqueInCopy = inRegion(x, y, record.actionArmCopy) && source.data[offset + 3] >= record.actionArmCopy.alphaThreshold
    const cleared = inRegion(x, y, record.restingArmClear)
    const expected = sourceOpaqueInCopy
      ? source.data.subarray(offset, offset + 4)
      : cleared
        ? Buffer.from([0, 0, 0, 0])
        : authority.data.subarray(offset, offset + 4)
    assert.ok(image.data.subarray(offset, offset + 4).equals(expected), `${frame.id} violates arm-only ownership at y${y} x${x}`)
    if (sourceOpaqueInCopy) copiedActionPixels += 1
    if (!image.data.subarray(offset, offset + 4).equals(authority.data.subarray(offset, offset + 4))) changedPixels += 1
  }
  assert.equal(record.copiedActionPixels, copiedActionPixels)
  assert.equal(record.changedPixels, changedPixels)
  assert.ok(record.changedPixels > 0 && record.changedPixels < 9000, `${frame.id} changed an implausible area`)
  const bounds = opaqueBounds(image)
  assert.equal(bounds.y0, authorityBounds.y0, `${frame.id} changed Prime cap-top registration`)
  assert.equal(bounds.y1, authorityBounds.y1, `${frame.id} changed Prime floor registration`)
  assert.equal(bounds.height, authorityBounds.height, `${frame.id} changed Prime standing height`)
  for (let y = 0; y < 320; y += 1) for (let x = 96; x <= 159; x += 1) {
    const offset = (y * 256 + x) * 4
    assert.ok(image.data.subarray(offset, offset + 4).equals(authority.data.subarray(offset, offset + 4)), `${frame.id} changed the protected central Prime body`)
  }
  actionHashes.add(sha256(image.data))

  let edgeAlpha = 0
  for (let x = 0; x < 256; x += 1) edgeAlpha += Number(Boolean(image.data[x * 4 + 3])) + Number(Boolean(image.data[(319 * 256 + x) * 4 + 3]))
  for (let y = 0; y < 320; y += 1) edgeAlpha += Number(Boolean(image.data[(y * 256) * 4 + 3])) + Number(Boolean(image.data[(y * 256 + 255) * 4 + 3]))
  assert.equal(edgeAlpha, 0, `${frame.id} lost its transparent safety gutter`)
}
assert.ok(actionHashes.size > 10, 'V10 froze the arm choreography')

const allFrames = v10.sequences.flatMap((sequence) => sequence.frames)
assert.equal(new Set(allFrames.map((frame) => frame.id)).size, allFrames.length)
assert.equal(new Set(allFrames.map((frame) => frame.redraftSlot)).size, allFrames.length)
assert.equal(register.publishedAssets.length, new Set(allFrames.map((frame) => frame.src)).size)
const component = fs.readFileSync(path.join(root, 'src/prime-keeper-drafts/PrimeKeeperDraftReview.tsx'), 'utf8')
for (const phrase of ['image.decode', 'Ⅱ Pause', '← Frame', 'Frame →', '■ Stop', 'Draft sequence sandbox', 'reviewAuthorities', 'amendmentComparison', 'Show Prime ghost', 'Hide Prime ghost', 'Prime ghost opacity']) assert.ok(component.includes(phrase), `V10 review UI omits ${phrase}`)
assert.match(component, /batch\.version >= 10[^\n]+complete approved rear Prime/, 'V10 review header omits the approved-body arm-only contract')
assert.match(fs.readFileSync(path.join(root, 'src/app/prime-keeper-animation-drafts/page.tsx'), 'utf8'), /keeper_prime_animation_drafts_v10/)
assert.match(fs.readFileSync(path.join(root, 'src/app/prime-keeper-animation-drafts-v10/page.tsx'), 'utf8'), /keeper_prime_animation_drafts_v10/)
assert.match(fs.readFileSync(path.join(root, 'src/app/prime-keeper-animation-drafts-v9/page.tsx'), 'utf8'), /keeper_prime_animation_drafts_v9/)

if (setManifest) for (const asset of register.publishedAssets) {
  const url = `/${asset.publicAssemblyPath.replace(/^public\//, '')}`
  assert.equal(setManifest.entries[url].sha256, asset.sourceSha256)
}

console.log(`Verified Prime morning draft V10: ${allFrames.length} frame occurrences, ${register.publishedAssets.length} unique assets, 21 exact-approved-body arm-only choreography frames.`)
