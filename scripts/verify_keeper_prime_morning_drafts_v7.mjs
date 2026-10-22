import assert from 'node:assert/strict'
import crypto from 'node:crypto'
import fs from 'node:fs'
import path from 'node:path'
import { execFileSync } from 'node:child_process'
import { fileURLToPath } from 'node:url'
import { PNG } from 'pngjs'

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..')
const sha256 = (bytes) => crypto.createHash('sha256').update(bytes).digest('hex')
execFileSync(process.execPath, ['scripts/build_keeper_prime_morning_drafts_v7.mjs', '--check'], { cwd: root, stdio: 'inherit' })

const v6Bytes = fs.readFileSync(path.join(root, 'data/keeper_prime_animation_drafts_v6.json'))
const v6 = JSON.parse(v6Bytes)
const v6Archive = JSON.parse(fs.readFileSync(path.join(root, 'review-archive/sets/keeper-prime-morning-drafts-v6.json')))
const v7 = JSON.parse(fs.readFileSync(path.join(root, 'data/keeper_prime_animation_drafts_v7.json')))
const corrections = JSON.parse(fs.readFileSync(path.join(root, 'art/drafts/keeper-prime-morning-drafts-corrections-2026-10-22-v7/corrections.json')))
const register = JSON.parse(fs.readFileSync(path.join(root, 'art/drafts/keeper-prime-morning-drafts-corrections-2026-10-22-v7/batch-register.json')))
const setManifestFile = path.join(root, 'review-archive/sets/keeper-prime-morning-drafts-v7.json')
const authorityHash = 'e6520aab48100c44aabdb0825c9424dbe35bffb2587b5270898e5214db2038df'
const authority = PNG.sync.read(fs.readFileSync(path.join(root, 'review-archive/objects/e6', `${authorityHash}.png`)))
const BODY_LEFT = 84
const BODY_RIGHT = 171

assert.equal(v7.version, 7)
assert.equal(v7.status, 'feedback-corrected-review-only')
assert.equal(v7.sequences.length, 10)
assert.equal(v7.sequences.reduce((sum, sequence) => sum + sequence.frames.length, 0), 162)
assert.equal(corrections.sourceBatchSha256, sha256(v6Bytes))
assert.equal(corrections.version, 7)
assert.equal(corrections.rejectedAmendment.version, 6)
assert.match(corrections.rejectedAmendment.reason, /second ribbed band/i)
assert.match(corrections.rejectedAmendment.reason, /duplicated/i)
assert.equal(corrections.imageGeneration.usedInDelivery, false)
assert.equal(register.set, 'keeper-prime-morning-drafts-v7')
assert.equal(corrections.frames.length, 21)

const setManifest = fs.existsSync(setManifestFile) ? JSON.parse(fs.readFileSync(setManifestFile)) : null
function bytesFor(frame) {
  const publicFile = path.join(root, 'public', frame.src.slice(1))
  if (fs.existsSync(publicFile)) return fs.readFileSync(publicFile)
  assert.ok(setManifest, `No public asset or archive manifest for ${frame.src}`)
  return fs.readFileSync(path.join(root, setManifest.entries[frame.src].object))
}
function v6BytesFor(frame) {
  const entry = v6Archive.entries[frame.src]
  assert.ok(entry, `Missing V6 archive entry for ${frame.src}`)
  return fs.readFileSync(path.join(root, entry.object))
}
function isSkinPixel(image, y, x) {
  const offset = (y * 256 + x) * 4
  const [red, green, blue, alpha] = image.data.subarray(offset, offset + 4)
  return alpha > 0 && red > 120 && red > green * 1.15 && green > blue * 1.1
}
function saturatedJumperBlue(image, y, x) {
  const offset = (y * 256 + x) * 4
  const [red, green, blue, alpha] = image.data.subarray(offset, offset + 4)
  return alpha > 0 && blue > 120 && blue > red * 1.5 && blue > green * 1.25
}

const v6ById = new Map(v6.sequences.map((sequence) => [sequence.id, sequence]))
const v7ById = new Map(v7.sequences.map((sequence) => [sequence.id, sequence]))
let changed = 0
for (const sequence of v7.sequences) {
  const previous = v6ById.get(sequence.id)
  assert.equal(sequence.frames.length, previous.frames.length)
  sequence.frames.forEach((frame, index) => {
    assert.equal(frame.priorV6.position, index + 1)
    assert.equal(frame.priorV6.sha256, previous.frames[index].sha256)
    assert.ok(frame.src.startsWith('/keeper-review/keeper-prime-morning-drafts-v7/assets/'))
    if (frame.sha256 !== previous.frames[index].sha256) changed += 1
    else assert.equal(sha256(bytesFor(frame)), previous.frames[index].sha256, `${frame.id} did not preserve V6 bytes`)
  })
}
assert.equal(changed, 21, 'V7 must change only the 21 rejected rear-task composites')

const rear = v7ById.get('rear-work-turn-return-v1')
const repaired = rear.frames.slice(10, 31)
assert.equal(repaired.length, 21)
const actionHashes = new Set()
for (const frame of repaired) {
  assert.match(frame.correction, /one lower-jumper hem/)
  assert.equal(frame.amendmentComparison.label, 'Rejected V6 doubled lower jumper')
  const image = PNG.sync.read(bytesFor(frame))
  const previous = v6ById.get('rear-work-turn-return-v1').frames[frame.priorV6.position - 1]
  const previousImage = PNG.sync.read(v6BytesFor(previous))
  const record = corrections.frames.find((item) => item.position === frame.priorV6.position)
  assert.ok(record, `${frame.id} lacks a correction record`)
  assert.deepEqual(
    [record.actionRetainedThrough, record.authorityTorsoStart, record.authorityRootStart, record.bodyLeft, record.bodyRight],
    [179, 180, 231, BODY_LEFT, BODY_RIGHT],
  )
  assert.ok(image.data.subarray(0, 180 * 256 * 4).equals(previousImage.data.subarray(0, 180 * 256 * 4)), `${frame.id} changed head, beard, cap, stripe or upper action drawing`)
  actionHashes.add(sha256(image.data.subarray(0, 180 * 256 * 4)))

  // Rows 180–230 contain only the exact central authority body: no passive
  // sleeves or hand skin, no source hip fragments and no second ribbed band.
  let oldSecondBandBlue = 0
  let newSecondBandBlue = 0
  for (let y = 180; y <= 230; y += 1) {
    for (let x = 0; x < 256; x += 1) {
      const offset = (y * 256 + x) * 4
      const owned = x >= BODY_LEFT && x <= BODY_RIGHT
      const expected = owned ? authority.data.subarray(offset, offset + 4) : Buffer.from([0, 0, 0, 0])
      assert.ok(image.data.subarray(offset, offset + 4).equals(expected), `${frame.id} has an invalid clean-root pixel at y${y} x${x}`)
      if (y >= 214 && saturatedJumperBlue(previousImage, y, x)) oldSecondBandBlue += 1
      if (y >= 214 && saturatedJumperBlue(image, y, x)) newSecondBandBlue += 1
      assert.equal(isSkinPixel(image, y, x), false, `${frame.id} exposes a clipped passive hand at y${y} x${x}`)
    }
  }
  assert.ok(oldSecondBandBlue > 100, `${frame.id} no longer demonstrates the rejected V6 second band`)
  assert.equal(newSecondBandBlue, 0, `${frame.id} still contains a second blue ribbed band below the authority hem`)

  // Trousers and boots are the exact current corrected rear authority.
  for (let y = 231; y < 320; y += 1) for (let x = 0; x < 256; x += 1) {
    const offset = (y * 256 + x) * 4
    const expected = x >= 70 && x <= 186 ? authority.data.subarray(offset, offset + 4) : Buffer.from([0, 0, 0, 0])
    assert.ok(image.data.subarray(offset, offset + 4).equals(expected), `${frame.id} lower authority body differs at y${y} x${x}`)
  }

  let edgeAlpha = 0
  for (let x = 0; x < 256; x += 1) edgeAlpha += Number(Boolean(image.data[x * 4 + 3])) + Number(Boolean(image.data[((319 * 256) + x) * 4 + 3]))
  for (let y = 0; y < 320; y += 1) edgeAlpha += Number(Boolean(image.data[(y * 256) * 4 + 3])) + Number(Boolean(image.data[(y * 256 + 255) * 4 + 3]))
  assert.equal(edgeAlpha, 0, `${frame.id} lost its transparent safety gutter`)
}
assert.ok(actionHashes.size > 10, 'V7 unexpectedly froze the retained work choreography')

const allFrames = v7.sequences.flatMap((sequence) => sequence.frames)
assert.equal(new Set(allFrames.map((frame) => frame.id)).size, allFrames.length)
assert.equal(new Set(allFrames.map((frame) => frame.redraftSlot)).size, allFrames.length)
assert.equal(register.publishedAssets.length, new Set(allFrames.map((frame) => frame.src)).size)
for (const name of ['front', 'back']) assert.ok(allFrames.some((frame) => frame.sha256 === v7.reviewAuthorities[name].sha256), `${name} review authority is not displayed`)

const component = fs.readFileSync(path.join(root, 'src/prime-keeper-drafts/PrimeKeeperDraftReview.tsx'), 'utf8')
for (const phrase of ['image.decode', 'Ⅱ Pause', '← Frame', 'Frame →', '■ Stop', 'Draft sequence sandbox', 'reviewAuthorities', 'amendmentComparison']) assert.ok(component.includes(phrase), `review UI omits ${phrase}`)
assert.match(component, /batch\.version >= 7[^\n]+one lower-jumper hem/, 'V7 review header does not describe the delivered single-hem correction')
assert.match(fs.readFileSync(path.join(root, 'src/app/prime-keeper-animation-drafts/page.tsx'), 'utf8'), /keeper_prime_animation_drafts_v7/)
assert.match(fs.readFileSync(path.join(root, 'src/app/prime-keeper-animation-drafts-v7/page.tsx'), 'utf8'), /keeper_prime_animation_drafts_v7/)

if (setManifest) {
  assert.equal(Object.keys(setManifest.entries).length, register.publishedAssets.length)
  for (const asset of register.publishedAssets) {
    const url = `/${asset.publicAssemblyPath.replace(/^public\//, '')}`
    assert.equal(setManifest.entries[url].sha256, asset.sourceSha256)
  }
}

console.log(`Verified Prime morning draft V7: ${allFrames.length} frame occurrences, ${register.publishedAssets.length} unique assets, 21 single-hem repairs.`)
