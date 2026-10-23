import crypto from 'node:crypto'
import fs from 'node:fs'
import path from 'node:path'
import { fileURLToPath } from 'node:url'
import { PNG } from 'pngjs'

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..')
const set = 'keeper-prime-morning-drafts-v11'
const reviewRoot = path.join(root, 'public/keeper-review', set)
const assetRoot = path.join(reviewRoot, 'assets')
const draftRoot = path.join(root, 'art/drafts/keeper-prime-morning-drafts-corrections-2026-10-23-v11')
const check = process.argv.includes('--check')
const sha256 = bytes => crypto.createHash('sha256').update(bytes).digest('hex')
const v10File = path.join(root, 'data/keeper_prime_animation_drafts_v10.json')
const v10Bytes = fs.readFileSync(v10File)
const v10 = JSON.parse(v10Bytes)
const v6 = JSON.parse(fs.readFileSync(path.join(root, 'data/keeper_prime_animation_drafts_v6.json')))
const v10Archive = JSON.parse(fs.readFileSync(path.join(root, 'review-archive/sets/keeper-prime-morning-drafts-v10.json')))
const v6Archive = JSON.parse(fs.readFileSync(path.join(root, 'review-archive/sets/keeper-prime-morning-drafts-v6.json')))
const BODY_AUTHORITY_HASH = '31dbac4efc00089fe6f831dc23f8397b4e3a8faf4d4aaa09a92b2ff407eebc35'
const RESTING_ARM_CLEAR = { y0: 115, y1: 242, leftMaxX: 81, rightMinX: 174 }
const ACTION_ARM_COPY = { y0: 70, y1: 242, shoulderY: 115, leftMaxX: 95, rightMinX: 160, alphaThreshold: 16, neutralExclusionRadius: 2, neutralFramePosition: 10 }

const objectFile = hash => path.join(root, 'review-archive/objects', hash.slice(0, 2), `${hash}.png`)
const archivedBytes = (frame, archive, label) => {
  const entry = archive.entries[frame.src]
  if (!entry) throw new Error(`${label} archive entry missing: ${frame.src}`)
  const bytes = fs.readFileSync(path.join(root, entry.object))
  if (sha256(bytes) !== frame.sha256) throw new Error(`${label} frame changed: ${frame.sha256}`)
  return bytes
}
const edgeAlpha = image => {
  let count = 0
  for (let x = 0; x < image.width; x += 1) count += Number(Boolean(image.data[x * 4 + 3])) + Number(Boolean(image.data[((image.height - 1) * image.width + x) * 4 + 3]))
  for (let y = 0; y < image.height; y += 1) count += Number(Boolean(image.data[(y * image.width) * 4 + 3])) + Number(Boolean(image.data[(y * image.width + image.width - 1) * 4 + 3]))
  return count
}
const outerArmColumn = x => x <= ACTION_ARM_COPY.leftMaxX || x >= ACTION_ARM_COPY.rightMinX
const neutralNearby = (neutral, x, y) => {
  const radius = ACTION_ARM_COPY.neutralExclusionRadius
  for (let yy = Math.max(0, y - radius); yy <= Math.min(neutral.height - 1, y + radius); yy += 1) {
    for (let xx = Math.max(0, x - radius); xx <= Math.min(neutral.width - 1, x + radius); xx += 1) {
      if (neutral.data[(yy * neutral.width + xx) * 4 + 3] >= ACTION_ARM_COPY.alphaThreshold) return true
    }
  }
  return false
}
const actionArmPixel = (source, authority, neutral, x, y) => {
  if (y < ACTION_ARM_COPY.y0 || y > ACTION_ARM_COPY.y1 || !outerArmColumn(x)) return false
  const offset = (y * source.width + x) * 4
  if (source.data[offset + 3] < ACTION_ARM_COPY.alphaThreshold) return false
  if (y >= ACTION_ARM_COPY.shoulderY) return true
  return authority.data[offset + 3] < ACTION_ARM_COPY.alphaThreshold && !neutralNearby(neutral, x, y)
}

function composeApprovedBodyWithCompleteActionArms(sourceBytes, authorityBytes, neutralBytes) {
  const source = PNG.sync.read(sourceBytes)
  const authority = PNG.sync.read(authorityBytes)
  const neutral = PNG.sync.read(neutralBytes)
  if ([source, authority, neutral].some(image => image.width !== 256 || image.height !== 320)) throw new Error('Rear work source, neutral or authority is not a 256x320 isolated frame')
  const image = PNG.sync.read(PNG.sync.write(authority))
  let clearedPixels = 0
  let copiedActionPixels = 0
  let copiedPixelsAboveV10Cutoff = 0
  let raisedExtensionPixels = 0
  for (let y = RESTING_ARM_CLEAR.y0; y <= RESTING_ARM_CLEAR.y1; y += 1) for (let x = 0; x < 256; x += 1) {
    if (x > RESTING_ARM_CLEAR.leftMaxX && x < RESTING_ARM_CLEAR.rightMinX) continue
    const offset = (y * 256 + x) * 4
    if (image.data[offset + 3]) clearedPixels += 1
    image.data.fill(0, offset, offset + 4)
  }
  for (let y = ACTION_ARM_COPY.y0; y <= ACTION_ARM_COPY.y1; y += 1) for (let x = 0; x < 256; x += 1) {
    if (!actionArmPixel(source, authority, neutral, x, y)) continue
    const offset = (y * 256 + x) * 4
    source.data.copy(image.data, offset, offset, offset + 4)
    copiedActionPixels += 1
    if (y < 125) copiedPixelsAboveV10Cutoff += 1
    if (y < ACTION_ARM_COPY.shoulderY) raisedExtensionPixels += 1
  }
  let changedPixels = 0
  for (let offset = 0; offset < image.data.length; offset += 4) if (!image.data.subarray(offset, offset + 4).equals(authority.data.subarray(offset, offset + 4))) changedPixels += 1
  return { bytes: PNG.sync.write(image), clearedPixels, copiedActionPixels, copiedPixelsAboveV10Cutoff, raisedExtensionPixels, changedPixels }
}

function writeOrCheck(file, bytes) {
  if (check) {
    let existing = fs.existsSync(file) ? fs.readFileSync(file) : null
    if (!existing && file.startsWith(assetRoot)) {
      const manifestFile = path.join(root, 'review-archive/sets', `${set}.json`)
      if (fs.existsSync(manifestFile)) {
        const manifest = JSON.parse(fs.readFileSync(manifestFile))
        const entry = manifest.entries?.[`/keeper-review/${set}/assets/${path.basename(file)}`]
        if (entry) existing = fs.readFileSync(path.join(root, entry.object))
      }
    }
    if (!existing || !existing.equals(bytes)) throw new Error(`Stale or missing V11 file: ${path.relative(root, file)}`)
    return
  }
  fs.mkdirSync(path.dirname(file), { recursive: true })
  fs.writeFileSync(file, bytes)
}
function storeObject(bytes) {
  const hash = sha256(bytes)
  const file = objectFile(hash)
  if (check) {
    if (!fs.existsSync(file) || sha256(fs.readFileSync(file)) !== hash) throw new Error(`Missing V11 archive object: ${hash}`)
  } else {
    fs.mkdirSync(path.dirname(file), { recursive: true })
    if (!fs.existsSync(file)) fs.writeFileSync(file, bytes)
  }
  return { hash, file }
}
function saveStrip(sequence, records) {
  const strip = new PNG({ width: records.length * 256, height: 320 })
  records.forEach((record, index) => PNG.bitblt(PNG.sync.read(record.bytes), strip, 0, 0, 256, 320, index * 256, 0))
  const bytes = PNG.sync.write(strip)
  const hash = sha256(bytes)
  const file = path.join(draftRoot, 'strips', `${sequence.id}-${hash.slice(0, 16)}.png`)
  writeOrCheck(file, bytes)
  return { path: path.relative(root, file).split(path.sep).join('/'), sha256: hash }
}

if (!check) for (const directory of [assetRoot, path.join(draftRoot, 'frames'), path.join(draftRoot, 'strips')]) fs.rmSync(directory, { recursive: true, force: true })
const authorityBytes = fs.readFileSync(objectFile(BODY_AUTHORITY_HASH))
if (sha256(authorityBytes) !== BODY_AUTHORITY_HASH) throw new Error('Rear body authority hash mismatch')
const authority = PNG.sync.read(authorityBytes)
const v6ById = new Map(v6.sequences.map(sequence => [sequence.id, sequence]))
const v6Rear = v6ById.get('rear-work-turn-return-v1')
const neutralFrame = v6Rear.frames[ACTION_ARM_COPY.neutralFramePosition - 1]
const neutralBytes = archivedBytes(neutralFrame, v6Archive, 'V6 neutral rear')
const publishedByHash = new Map()
const correctionRecords = []
const sequences = []

for (const sequence of v10.sequences) {
  const records = []
  for (let index = 0; index < sequence.frames.length; index += 1) {
    const frame = sequence.frames[index]
    const position = index + 1
    const repaired = sequence.id === 'rear-work-turn-return-v1' && position >= 11 && position <= 31
    const v10FrameBytes = archivedBytes(frame, v10Archive, 'V10')
    const v6Frame = repaired ? v6Rear.frames[index] : null
    const sourceBytes = repaired ? archivedBytes(v6Frame, v6Archive, 'V6') : v10FrameBytes
    const result = repaired ? composeApprovedBodyWithCompleteActionArms(sourceBytes, authorityBytes, neutralBytes) : { bytes: sourceBytes }
    const image = PNG.sync.read(result.bytes)
    if (image.width !== frame.cell[0] || image.height !== frame.cell[1] || edgeAlpha(image)) throw new Error(`${sequence.id} frame ${position}: invalid isolated geometry`)
    const hash = sha256(result.bytes)
    let asset = publishedByHash.get(hash)
    if (!asset) {
      const fileName = `frame-${hash.slice(0, 16)}.png`
      const publicFile = path.join(assetRoot, fileName)
      writeOrCheck(publicFile, result.bytes)
      const stored = storeObject(result.bytes)
      const sourceFile = repaired ? path.join(draftRoot, 'frames', fileName) : stored.file
      if (repaired) writeOrCheck(sourceFile, result.bytes)
      asset = { source: path.relative(root, sourceFile).split(path.sep).join('/'), sourceSha256: hash, publicAssemblyPath: path.relative(root, publicFile).split(path.sep).join('/'), url: `/keeper-review/${set}/assets/${fileName}` }
      publishedByHash.set(hash, asset)
    }
    const correction = repaired ? 'V10 rejected: its row-125 arm-transfer boundary visibly cropped sleeve and raised-hand silhouettes; V11 retains the approved body while extending the arm mask above the shoulder only through transparent authority pixels outside the neutral rear-body envelope' : frame.correction
    if (repaired) correctionRecords.push({ sequence: sequence.id, position, sourceV6Sha256: v6Frame.sha256, rejectedV10Sha256: frame.sha256, draftV11Sha256: hash, bodyAuthoritySha256: BODY_AUTHORITY_HASH, neutralRearSha256: neutralFrame.sha256, restingArmClear: RESTING_ARM_CLEAR, actionArmCopy: ACTION_ARM_COPY, clearedPixels: result.clearedPixels, copiedActionPixels: result.copiedActionPixels, copiedPixelsAboveV10Cutoff: result.copiedPixelsAboveV10Cutoff, raisedExtensionPixels: result.raisedExtensionPixels, changedPixels: result.changedPixels, correction })
    records.push({ frame, bytes: result.bytes, hash, asset, correction, repaired })
  }
  const repairedSequence = sequence.id === 'rear-work-turn-return-v1'
  sequences.push({
    ...sequence,
    status: repairedSequence ? 'approved-body-complete-arm-choreography-review-v11' : sequence.status,
    source: repairedSequence ? { path: 'art/drafts/keeper-prime-morning-drafts-corrections-2026-10-23-v11/corrections.json', sha256: '' } : sequence.source,
    draftStrip: repairedSequence ? saveStrip(sequence, records) : sequence.draftStrip,
    frames: records.map(({ frame, hash, asset, correction, repaired }, index) => ({ ...frame, id: `${sequence.id}-v11-f${String(index + 1).padStart(2, '0')}`, src: asset.url, sha256: hash, redraftSlot: `${sequence.id}/v11-frame-${String(index + 1).padStart(2, '0')}`, priorV10: { position: index + 1, sha256: frame.sha256 }, ...(repaired ? { amendmentComparison: { label: 'Rejected V10 cropped arm mask', src: frame.src, sha256: frame.sha256 } } : {}), correction })),
  })
}

const corrections = { schema: 'lighthouse-keeper/prime-animation-feedback-corrections@1', version: 11, generatedOn: '2026-10-23', sourceBatch: 'data/keeper_prime_animation_drafts_v10.json', sourceBatchSha256: sha256(v10Bytes), authority: { completeRearBody: BODY_AUTHORITY_HASH, neutralRear: neutralFrame.sha256 }, rejectedAmendment: { version: 10, scope: 'rear-work-turn-return-v1 positions 11–31 only', reason: 'The fixed row-125 transfer boundary visibly cropped the tops of sleeves and raised hands. The exact-Prime alignment overlay was also mistakenly enabled by default.' }, frames: correctionRecords, imageGeneration: { usedInDelivery: false, reason: 'V11 is deterministic exact-pixel compositing from the hash-pinned approved rear body and V6 arm choreography.' } }
const correctionBytes = Buffer.from(`${JSON.stringify(corrections, null, 2)}\n`)
const correctionHash = sha256(correctionBytes)
sequences.find(sequence => sequence.id === 'rear-work-turn-return-v1').source.sha256 = correctionHash
writeOrCheck(path.join(draftRoot, 'corrections.json'), correctionBytes)
const reviewAuthorities = Object.fromEntries(Object.entries(v10.reviewAuthorities).map(([name, item]) => [name, { ...item, src: `/keeper-review/${set}/assets/frame-${item.sha256.slice(0, 16)}.png` }]))
const frameCount = sequences.reduce((sum, sequence) => sum + sequence.frames.length, 0)
const manifest = { ...v10, version: 11, generatedOn: '2026-10-23', status: 'approved-body-complete-arm-choreography-review', note: 'V11 preserves V1–V10 and replaces only rear-task positions 11–31. It removes V10’s row-125 arm crop while retaining the complete approved rear body. Raised arm pixels may enter above the shoulder only outside the approved body and outside a two-pixel dilation of the neutral rear source. The optional alignment ghost is off by default. No canonical, runtime or production file is overwritten.', reviewAuthorities, sequences }
writeOrCheck(path.join(root, 'data/keeper_prime_animation_drafts_v11.json'), Buffer.from(`${JSON.stringify(manifest, null, 2)}\n`))
const shellBytes = Buffer.from('<!doctype html><meta charset="utf-8"><title>Prime Keeper review V11</title><meta http-equiv="refresh" content="0;url=/prime-keeper-animation-drafts-v11"><a href="/prime-keeper-animation-drafts-v11">Open Prime Keeper review V11</a>\n')
writeOrCheck(path.join(reviewRoot, 'index.html'), shellBytes)
const register = { schema: 'lighthouse-keeper/reversible-review-batch@1', set, status: 'approved-body-complete-arm-choreography-review', candidate: { publicShell: { file: `public/keeper-review/${set}/index.html`, sha256: sha256(shellBytes) } }, publishedAssets: [...publishedByHash.values()].map(({ source, sourceSha256, publicAssemblyPath, url }) => ({ source, sourceSha256, publicAssemblyPath, url })) }
writeOrCheck(path.join(draftRoot, 'batch-register.json'), Buffer.from(`${JSON.stringify(register, null, 2)}\n`))
console.log(`${check ? 'Verified' : 'Wrote'} Prime morning draft V11: ${sequences.length} sequences, ${frameCount} occurrences, ${publishedByHash.size} unique images, ${correctionRecords.length} complete-arm repairs.`)
