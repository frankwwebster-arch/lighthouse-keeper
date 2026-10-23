import assert from 'node:assert/strict'
import crypto from 'node:crypto'
import fs from 'node:fs'
import path from 'node:path'
import { execFileSync } from 'node:child_process'
import { fileURLToPath } from 'node:url'
import { PNG } from 'pngjs'

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..')
const sha256 = bytes => crypto.createHash('sha256').update(bytes).digest('hex')
execFileSync(process.execPath, ['scripts/build_keeper_prime_morning_drafts_v12.mjs', '--check'], { cwd: root, stdio: 'inherit' })

const v11Bytes = fs.readFileSync(path.join(root, 'data/keeper_prime_animation_drafts_v11.json'))
const v11 = JSON.parse(v11Bytes)
const v12 = JSON.parse(fs.readFileSync(path.join(root, 'data/keeper_prime_animation_drafts_v12.json')))
const v11Archive = JSON.parse(fs.readFileSync(path.join(root, 'review-archive/sets/keeper-prime-morning-drafts-v11.json')))
const corrections = JSON.parse(fs.readFileSync(path.join(root, 'art/drafts/keeper-prime-morning-drafts-corrections-2026-10-23-v12/corrections.json')))
const register = JSON.parse(fs.readFileSync(path.join(root, 'art/drafts/keeper-prime-morning-drafts-corrections-2026-10-23-v12/batch-register.json')))
const setManifestFile = path.join(root, 'review-archive/sets/keeper-prime-morning-drafts-v12.json')
const setManifest = fs.existsSync(setManifestFile) ? JSON.parse(fs.readFileSync(setManifestFile)) : null
const donorPositions = [2, 3, 4, 5, 6, 7, 8]

const archivedV11 = frame => fs.readFileSync(path.join(root, v11Archive.entries[frame.src].object))
function bytesFor(frame) {
  const publicFile = path.join(root, 'public', frame.src.slice(1))
  if (fs.existsSync(publicFile)) return fs.readFileSync(publicFile)
  assert.ok(setManifest, `No V12 archive manifest for ${frame.src}`)
  return fs.readFileSync(path.join(root, setManifest.entries[frame.src].object))
}
const edgeAlpha = image => {
  let count = 0
  for (let x = 0; x < image.width; x += 1) count += Number(Boolean(image.data[x * 4 + 3])) + Number(Boolean(image.data[((image.height - 1) * image.width + x) * 4 + 3]))
  for (let y = 0; y < image.height; y += 1) count += Number(Boolean(image.data[(y * image.width) * 4 + 3])) + Number(Boolean(image.data[(y * image.width + image.width - 1) * 4 + 3]))
  return count
}

assert.equal(v12.version, 12)
assert.equal(v12.status, 'intact-cooking-whole-frame-choreography-review')
assert.equal(v12.sequences.length, 10)
assert.equal(v12.sequences.reduce((sum, sequence) => sum + sequence.frames.length, 0), 162)
assert.equal(corrections.sourceBatchSha256, sha256(v11Bytes))
assert.deepEqual(corrections.wholeFrameAuthority.positions, donorPositions)
assert.equal(corrections.rejectedAmendment.version, 11)
assert.match(corrections.rejectedAmendment.reason, /inner sleeve.*jumper boundaries/i)
assert.equal(corrections.frames.length, 21)
assert.equal(register.set, 'keeper-prime-morning-drafts-v12')

const v11ById = new Map(v11.sequences.map(sequence => [sequence.id, sequence]))
const v12ById = new Map(v12.sequences.map(sequence => [sequence.id, sequence]))
const cooking = v11ById.get('cook-counter-v1')
const rearV11 = v11ById.get('rear-work-turn-return-v1')
const rearV12 = v12ById.get('rear-work-turn-return-v1')
let changed = 0

for (const sequence of v12.sequences) {
  const previous = v11ById.get(sequence.id)
  assert.equal(sequence.frames.length, previous.frames.length)
  sequence.frames.forEach((frame, index) => {
    assert.deepEqual(frame.priorV11, { position: index + 1, sha256: previous.frames[index].sha256 })
    assert.ok(frame.src.startsWith('/keeper-review/keeper-prime-morning-drafts-v12/assets/'))
    const shouldChange = sequence.id === 'rear-work-turn-return-v1' && index + 1 >= 11 && index + 1 <= 31
    assert.equal(frame.sha256 !== previous.frames[index].sha256, shouldChange, `${frame.id}: unexpected V11/V12 change scope`)
    if (shouldChange) changed += 1
  })
}
assert.equal(changed, 21)

const donorHashes = new Set()
for (let position = 11; position <= 31; position += 1) {
  const donorPosition = donorPositions[(position - 11) % donorPositions.length]
  const donor = cooking.frames[donorPosition - 1]
  const candidate = rearV12.frames[position - 1]
  const rejected = rearV11.frames[position - 1]
  const record = corrections.frames.find(item => item.position === position)
  assert.deepEqual(candidate.cookingDonor, { position: donorPosition, sha256: donor.sha256 })
  assert.equal(candidate.sha256, donor.sha256, `${candidate.id}: not the exact cooking donor`)
  assert.ok(bytesFor(candidate).equals(archivedV11(donor)), `${candidate.id}: cooking donor bytes changed`)
  assert.equal(candidate.amendmentComparison.label, 'Rejected V11 layered jumper')
  assert.equal(candidate.amendmentComparison.sha256, rejected.sha256)
  assert.equal(record.rejectedV11Sha256, rejected.sha256)
  assert.equal(record.cookingDonorPosition, donorPosition)
  assert.equal(record.cookingDonorSha256, donor.sha256)
  assert.equal(record.draftV12Sha256, donor.sha256)
  const image = PNG.sync.read(bytesFor(candidate))
  assert.equal(image.width, 256)
  assert.equal(image.height, 320)
  assert.equal(edgeAlpha(image), 0, `${candidate.id}: frame touches a shared cell edge`)
  donorHashes.add(candidate.sha256)
}
assert.equal(donorHashes.size, 7, 'V12 must retain all seven intact cooking poses')

const strip = PNG.sync.read(fs.readFileSync(path.join(root, rearV12.draftStrip.path)))
assert.equal(strip.width, 41 * 256)
assert.equal(strip.height, 320)
for (let index = 0; index < rearV12.frames.length; index += 1) {
  const frame = PNG.sync.read(bytesFor(rearV12.frames[index]))
  for (let y = 0; y < 320; y += 1) {
    const stripOffset = (y * strip.width + index * 256) * 4
    const frameOffset = y * 256 * 4
    assert.ok(strip.data.subarray(stripOffset, stripOffset + 256 * 4).equals(frame.data.subarray(frameOffset, frameOffset + 256 * 4)), `V12 strip cell ${index + 1} mismatch`)
  }
}

const allFrames = v12.sequences.flatMap(sequence => sequence.frames)
assert.equal(new Set(allFrames.map(frame => frame.id)).size, allFrames.length)
assert.equal(new Set(allFrames.map(frame => frame.redraftSlot)).size, allFrames.length)
assert.equal(register.publishedAssets.length, new Set(allFrames.map(frame => frame.src)).size)
const component = fs.readFileSync(path.join(root, 'src/prime-keeper-drafts/PrimeKeeperDraftReview.tsx'), 'utf8')
assert.match(component, /useState\(batch\.version === 10\)/, 'V12 alignment ghost is not off by default')
assert.match(component, /V12 borrows the complete cooking poses/)
for (const phrase of ['Show Prime ghost', 'Hide Prime ghost', 'Prime ghost opacity']) assert.ok(component.includes(phrase))
assert.match(fs.readFileSync(path.join(root, 'src/app/prime-keeper-animation-drafts/page.tsx'), 'utf8'), /keeper_prime_animation_drafts_v12/)
assert.match(fs.readFileSync(path.join(root, 'src/app/prime-keeper-animation-drafts-v12/page.tsx'), 'utf8'), /keeper_prime_animation_drafts_v12/)
assert.match(fs.readFileSync(path.join(root, 'src/app/prime-keeper-animation-drafts-v11/page.tsx'), 'utf8'), /keeper_prime_animation_drafts_v11/)
if (setManifest) for (const asset of register.publishedAssets) {
  const url = `/${asset.publicAssemblyPath.replace(/^public\//, '')}`
  assert.equal(setManifest.entries[url].sha256, asset.sourceSha256)
}
console.log(`Verified Prime morning draft V12: ${allFrames.length} frame occurrences, ${register.publishedAssets.length} unique assets, 21 exact whole-frame cooking transfers.`)
