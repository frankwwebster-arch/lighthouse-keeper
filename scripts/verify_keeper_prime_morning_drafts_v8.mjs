import assert from 'node:assert/strict'
import crypto from 'node:crypto'
import fs from 'node:fs'
import path from 'node:path'
import { execFileSync } from 'node:child_process'
import { fileURLToPath } from 'node:url'
import { PNG } from 'pngjs'

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..')
const sha256 = (bytes) => crypto.createHash('sha256').update(bytes).digest('hex')
execFileSync(process.execPath, ['scripts/build_keeper_prime_morning_drafts_v8.mjs', '--check'], { cwd: root, stdio: 'inherit' })

const v7Bytes = fs.readFileSync(path.join(root, 'data/keeper_prime_animation_drafts_v7.json'))
const v7 = JSON.parse(v7Bytes)
const v6 = JSON.parse(fs.readFileSync(path.join(root, 'data/keeper_prime_animation_drafts_v6.json')))
const v8 = JSON.parse(fs.readFileSync(path.join(root, 'data/keeper_prime_animation_drafts_v8.json')))
const v7Archive = JSON.parse(fs.readFileSync(path.join(root, 'review-archive/sets/keeper-prime-morning-drafts-v7.json')))
const v6Archive = JSON.parse(fs.readFileSync(path.join(root, 'review-archive/sets/keeper-prime-morning-drafts-v6.json')))
const corrections = JSON.parse(fs.readFileSync(path.join(root, 'art/drafts/keeper-prime-morning-drafts-corrections-2026-10-23-v8/corrections.json')))
const register = JSON.parse(fs.readFileSync(path.join(root, 'art/drafts/keeper-prime-morning-drafts-corrections-2026-10-23-v8/batch-register.json')))
const setManifestFile = path.join(root, 'review-archive/sets/keeper-prime-morning-drafts-v8.json')
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
  assert.ok(setManifest, `No V8 archive manifest for ${frame.src}`)
  return fs.readFileSync(path.join(root, setManifest.entries[frame.src].object))
}
function alphaBounds(image, y) {
  const xs = []
  for (let x = 0; x < 256; x += 1) if (image.data[(y * 256 + x) * 4 + 3]) xs.push(x)
  return xs.length ? [xs[0], xs.at(-1)] : null
}
assert.equal(v8.version, 8)
assert.equal(v8.status, 'feedback-corrected-review-only')
assert.equal(v8.sequences.length, 10)
assert.equal(v8.sequences.reduce((sum, sequence) => sum + sequence.frames.length, 0), 162)
assert.equal(corrections.sourceBatchSha256, sha256(v7Bytes))
assert.equal(corrections.rejectedAmendment.version, 7)
assert.match(corrections.rejectedAmendment.reason, /visible inward step/i)
assert.equal(corrections.imageGeneration.usedInDelivery, false)
assert.equal(corrections.frames.length, 21)
assert.equal(register.set, 'keeper-prime-morning-drafts-v8')

const v6ById = new Map(v6.sequences.map((sequence) => [sequence.id, sequence]))
const v7ById = new Map(v7.sequences.map((sequence) => [sequence.id, sequence]))
const v8ById = new Map(v8.sequences.map((sequence) => [sequence.id, sequence]))
let changed = 0
for (const sequence of v8.sequences) {
  const previous = v7ById.get(sequence.id)
  assert.equal(sequence.frames.length, previous.frames.length)
  sequence.frames.forEach((frame, index) => {
    assert.deepEqual(frame.priorV7, { position: index + 1, sha256: previous.frames[index].sha256 })
    assert.ok(frame.src.startsWith('/keeper-review/keeper-prime-morning-drafts-v8/assets/'))
    if (frame.sha256 !== previous.frames[index].sha256) changed += 1
    else assert.equal(sha256(bytesFor(frame)), previous.frames[index].sha256)
  })
}
assert.equal(changed, 21, 'V8 must change only the 21 rejected V7 rear-task composites')

const repaired = v8ById.get('rear-work-turn-return-v1').frames.slice(10, 31)
const v6Rear = v6ById.get('rear-work-turn-return-v1')
const actionHashes = new Set()
for (const frame of repaired) {
  const position = frame.priorV7.position
  const image = PNG.sync.read(bytesFor(frame))
  const source = PNG.sync.read(archived(v6Rear.frames[position - 1], v6Archive))
  const rejected = PNG.sync.read(archived(v7ById.get('rear-work-turn-return-v1').frames[position - 1], v7Archive))
  const record = corrections.frames.find((item) => item.position === position)
  assert.equal(record.actionRetainedThrough, 213)
  assert.equal(record.authorityRootStart, 214)
  assert.equal(record.joinRight - record.joinLeft, 90)
  assert.equal(record.rootDx, record.joinLeft - 82)
  assert.ok(record.rootDx >= -2 && record.rootDx <= 2, `${frame.id} lower-body registration is unexpectedly large`)
  assert.equal(frame.amendmentComparison.label, 'Rejected V7 premature torso cut')
  assert.ok(image.data.subarray(0, 214 * 256 * 4).equals(source.data.subarray(0, 214 * 256 * 4)), `${frame.id} changed the moving torso or its natural hem`)
  actionHashes.add(sha256(image.data.subarray(0, 214 * 256 * 4)))

  // The retained hem ends and approved trousers begin on the same exact
  // same per-frame outline. V7's row-179 x=84/x=171 step cannot recur.
  const retainedBounds = alphaBounds(image, 213)
  assert.deepEqual(retainedBounds, [record.joinLeft, record.joinRight], `${frame.id} retained hem boundary moved`)
  assert.deepEqual(alphaBounds(image, 214), retainedBounds, `${frame.id} authority legs do not meet the hem exactly`)
  assert.notDeepEqual(alphaBounds(rejected, 179), alphaBounds(rejected, 180), `${frame.id} no longer demonstrates the rejected V7 step`)

  for (let y = 214; y < 320; y += 1) for (let x = 0; x < 256; x += 1) {
    const i = (y * 256 + x) * 4
    const sourceX = x - record.rootDx
    const owned = y <= 230 ? sourceX >= 82 && sourceX <= 172 : sourceX >= 70 && sourceX <= 186
    const authorityOffset = (y * 256 + sourceX) * 4
    const expected = owned ? authority.data.subarray(authorityOffset, authorityOffset + 4) : Buffer.from([0, 0, 0, 0])
    assert.ok(image.data.subarray(i, i + 4).equals(expected), `${frame.id} lower authority differs at y${y} x${x}`)
  }

  let edgeAlpha = 0
  for (let x = 0; x < 256; x += 1) edgeAlpha += Number(Boolean(image.data[x * 4 + 3])) + Number(Boolean(image.data[(319 * 256 + x) * 4 + 3]))
  for (let y = 0; y < 320; y += 1) edgeAlpha += Number(Boolean(image.data[(y * 256) * 4 + 3])) + Number(Boolean(image.data[(y * 256 + 255) * 4 + 3]))
  assert.equal(edgeAlpha, 0, `${frame.id} lost its transparent safety gutter`)
}
assert.ok(actionHashes.size > 10, 'V8 froze the retained work choreography')

const allFrames = v8.sequences.flatMap((sequence) => sequence.frames)
assert.equal(new Set(allFrames.map((frame) => frame.id)).size, allFrames.length)
assert.equal(new Set(allFrames.map((frame) => frame.redraftSlot)).size, allFrames.length)
assert.equal(register.publishedAssets.length, new Set(allFrames.map((frame) => frame.src)).size)
const component = fs.readFileSync(path.join(root, 'src/prime-keeper-drafts/PrimeKeeperDraftReview.tsx'), 'utf8')
for (const phrase of ['image.decode', 'Ⅱ Pause', '← Frame', 'Frame →', '■ Stop', 'Draft sequence sandbox', 'reviewAuthorities', 'amendmentComparison']) assert.ok(component.includes(phrase), `review UI omits ${phrase}`)
assert.match(component, /batch\.version >= 8[^\n]+outlines meet exactly/, 'V8 review header omits the exact-outline correction')
assert.match(fs.readFileSync(path.join(root, 'src/app/prime-keeper-animation-drafts/page.tsx'), 'utf8'), /keeper_prime_animation_drafts_v8/)
assert.match(fs.readFileSync(path.join(root, 'src/app/prime-keeper-animation-drafts-v8/page.tsx'), 'utf8'), /keeper_prime_animation_drafts_v8/)

if (setManifest) for (const asset of register.publishedAssets) {
  const url = `/${asset.publicAssemblyPath.replace(/^public\//, '')}`
  assert.equal(setManifest.entries[url].sha256, asset.sourceSha256)
}

console.log(`Verified Prime morning draft V8: ${allFrames.length} frame occurrences, ${register.publishedAssets.length} unique assets, 21 exact-outline repairs.`)
