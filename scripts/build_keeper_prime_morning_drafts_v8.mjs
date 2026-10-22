import crypto from 'node:crypto'
import fs from 'node:fs'
import path from 'node:path'
import { fileURLToPath } from 'node:url'
import { PNG } from 'pngjs'

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..')
const set = 'keeper-prime-morning-drafts-v8'
const reviewRoot = path.join(root, 'public/keeper-review', set)
const assetRoot = path.join(reviewRoot, 'assets')
const draftRoot = path.join(root, 'art/drafts/keeper-prime-morning-drafts-corrections-2026-10-23-v8')
const check = process.argv.includes('--check')
const sha256 = (bytes) => crypto.createHash('sha256').update(bytes).digest('hex')
const v7File = path.join(root, 'data/keeper_prime_animation_drafts_v7.json')
const v7Bytes = fs.readFileSync(v7File)
const v7 = JSON.parse(v7Bytes)
const v6 = JSON.parse(fs.readFileSync(path.join(root, 'data/keeper_prime_animation_drafts_v6.json')))
const v7Archive = JSON.parse(fs.readFileSync(path.join(root, 'review-archive/sets/keeper-prime-morning-drafts-v7.json')))
const v6Archive = JSON.parse(fs.readFileSync(path.join(root, 'review-archive/sets/keeper-prime-morning-drafts-v6.json')))
const ROOT_AUTHORITY_HASH = '31dbac4efc00089fe6f831dc23f8397b4e3a8faf4d4aaa09a92b2ff407eebc35'

function objectFile(hash) {
  return path.join(root, 'review-archive/objects', hash.slice(0, 2), `${hash}.png`)
}

function archivedBytes(frame, archive, label) {
  const entry = archive.entries[frame.src]
  if (!entry) throw new Error(`${label} archive entry missing: ${frame.src}`)
  const bytes = fs.readFileSync(path.join(root, entry.object))
  if (sha256(bytes) !== frame.sha256) throw new Error(`${label} frame changed: ${frame.sha256}`)
  return bytes
}

function edgeAlpha(image) {
  let count = 0
  for (let x = 0; x < image.width; x += 1) {
    count += Number(Boolean(image.data[x * 4 + 3]))
    count += Number(Boolean(image.data[((image.height - 1) * image.width + x) * 4 + 3]))
  }
  for (let y = 0; y < image.height; y += 1) {
    count += Number(Boolean(image.data[(y * image.width) * 4 + 3]))
    count += Number(Boolean(image.data[(y * image.width + image.width - 1) * 4 + 3]))
  }
  return count
}

function copyPixel(source, target, y, x) {
  const offset = (y * source.width + x) * 4
  source.data.copy(target.data, offset, offset, offset + 4)
}

function alphaBounds(image, y) {
  const xs = []
  for (let x = 0; x < image.width; x += 1) if (image.data[(y * image.width + x) * 4 + 3]) xs.push(x)
  return xs.length ? [xs[0], xs.at(-1)] : null
}

function copyPixelTranslated(source, target, y, sourceX, targetX) {
  const sourceOffset = (y * source.width + sourceX) * 4
  const targetOffset = (y * target.width + targetX) * 4
  source.data.copy(target.data, targetOffset, sourceOffset, sourceOffset + 4)
}

function repairRearWorkV8(sourceBytes, authority) {
  const source = PNG.sync.read(sourceBytes)
  const image = PNG.sync.read(PNG.sync.write(source))
  if (image.width !== 256 || image.height !== 320) throw new Error('Rear work source is not a 256x320 isolated frame')
  const [joinLeft, joinRight] = alphaBounds(source, 213)
  if (joinRight - joinLeft !== 90) throw new Error(`Unexpected moving hem bounds: ${joinLeft}–${joinRight}`)
  const dx = joinLeft - 82

  // Keep the complete moving torso and its one natural ribbed hem. The
  // approved rear-turn authority begins only after that hem, where its outer
  // trouser edges are exactly x=82 and x=172 as well. This removes V7's early
  // torso cut and therefore removes the visible step on both sides.
  for (let y = 214; y <= 230; y += 1) {
    image.data.fill(0, y * 256 * 4, (y + 1) * 256 * 4)
    for (let x = 82; x <= 172; x += 1) copyPixelTranslated(authority, image, y, x, x + dx)
  }
  for (let y = 231; y < 320; y += 1) {
    image.data.fill(0, y * 256 * 4, (y + 1) * 256 * 4)
    for (let x = 70; x <= 186; x += 1) copyPixelTranslated(authority, image, y, x, x + dx)
  }
  return { bytes: PNG.sync.write(image), actionRetainedThrough: 213, authorityRootStart: 214, joinLeft, joinRight, rootDx: dx }
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
    if (!existing || !existing.equals(bytes)) throw new Error(`Stale or missing V8 file: ${path.relative(root, file)}`)
    return
  }
  fs.mkdirSync(path.dirname(file), { recursive: true })
  fs.writeFileSync(file, bytes)
}

function storeObject(bytes) {
  const hash = sha256(bytes)
  const file = objectFile(hash)
  if (check) {
    if (!fs.existsSync(file) || sha256(fs.readFileSync(file)) !== hash) throw new Error(`Missing V8 archive object: ${hash}`)
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

const authorityBytes = fs.readFileSync(objectFile(ROOT_AUTHORITY_HASH))
if (sha256(authorityBytes) !== ROOT_AUTHORITY_HASH) throw new Error('Rear root authority hash mismatch')
const authority = PNG.sync.read(authorityBytes)
const v6ById = new Map(v6.sequences.map((sequence) => [sequence.id, sequence]))
const publishedByHash = new Map()
const correctionRecords = []
const sequences = []

for (const sequence of v7.sequences) {
  const records = []
  for (let index = 0; index < sequence.frames.length; index += 1) {
    const frame = sequence.frames[index]
    const position = index + 1
    const repaired = sequence.id === 'rear-work-turn-return-v1' && position >= 11 && position <= 31
    const v7FrameBytes = archivedBytes(frame, v7Archive, 'V7')
    const v6Frame = repaired ? v6ById.get(sequence.id).frames[index] : null
    const sourceBytes = repaired ? archivedBytes(v6Frame, v6Archive, 'V6') : v7FrameBytes
    const result = repaired ? repairRearWorkV8(sourceBytes, authority) : { bytes: sourceBytes }
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
    const correction = repaired
      ? 'V7 rejected: its authority body started before the moving torso ended, creating a stepped side outline; V8 retains the complete moving torso and its single hem through row 213, then registers approved rear-authority legs to the exact per-frame left and right outline'
      : frame.correction
    if (repaired) correctionRecords.push({ sequence: sequence.id, position, sourceV6Sha256: v6Frame.sha256, rejectedV7Sha256: frame.sha256, draftV8Sha256: hash, actionRetainedThrough: result.actionRetainedThrough, authorityRootStart: result.authorityRootStart, joinLeft: result.joinLeft, joinRight: result.joinRight, rootDx: result.rootDx, correction })
    records.push({ frame, bytes: result.bytes, hash, asset, correction, repaired })
  }
  const repairedSequence = sequence.id === 'rear-work-turn-return-v1'
  sequences.push({
    ...sequence,
    status: repairedSequence ? 'feedback-corrected-versioned-draft-v8' : sequence.status,
    source: repairedSequence ? { path: 'art/drafts/keeper-prime-morning-drafts-corrections-2026-10-23-v8/corrections.json', sha256: '' } : sequence.source,
    draftStrip: repairedSequence ? saveStrip(sequence, records) : sequence.draftStrip,
    frames: records.map(({ frame, hash, asset, correction, repaired }, index) => ({
      ...frame,
      id: `${sequence.id}-v8-f${String(index + 1).padStart(2, '0')}`,
      src: asset.url,
      sha256: hash,
      redraftSlot: `${sequence.id}/v8-frame-${String(index + 1).padStart(2, '0')}`,
      priorV7: { position: index + 1, sha256: frame.sha256 },
      ...(repaired ? { amendmentComparison: { label: 'Rejected V7 premature torso cut', src: frame.src, sha256: frame.sha256 } } : {}),
      correction,
    })),
  })
}

const corrections = {
  schema: 'lighthouse-keeper/prime-animation-feedback-corrections@1',
  version: 8,
  generatedOn: '2026-10-23',
  sourceBatch: 'data/keeper_prime_animation_drafts_v7.json',
  sourceBatchSha256: sha256(v7Bytes),
  authority: { lowerBody: ROOT_AUTHORITY_HASH },
  rejectedAmendment: { version: 7, scope: 'rear-work-turn-return-v1 positions 11–31 only', reason: 'V7 began the fixed lower-body ownership at row 180, before the moving torso silhouette ended, producing a visible inward step on both sides.' },
  frames: correctionRecords,
  imageGeneration: { usedInDelivery: false, reason: 'V8 is exact deterministic compositing from hash-pinned Prime action and approved rear-authority pixels.' },
}
const correctionBytes = Buffer.from(`${JSON.stringify(corrections, null, 2)}\n`)
const correctionHash = sha256(correctionBytes)
sequences.find((sequence) => sequence.id === 'rear-work-turn-return-v1').source.sha256 = correctionHash
writeOrCheck(path.join(draftRoot, 'corrections.json'), correctionBytes)

const reviewAuthorities = Object.fromEntries(Object.entries(v7.reviewAuthorities).map(([name, item]) => [name, { ...item, src: `/keeper-review/${set}/assets/frame-${item.sha256.slice(0, 16)}.png` }]))
const frameCount = sequences.reduce((sum, sequence) => sum + sequence.frames.length, 0)
const manifest = { ...v7, version: 8, generatedOn: '2026-10-23', status: 'feedback-corrected-review-only', note: 'V8 preserves V1–V7 and replaces only rear-task positions 11–31. The complete moving torso and its one natural hem remain intact through row 213; approved rear-authority trousers are registered per frame so both side outlines meet exactly below it. No canonical, runtime or production file is overwritten.', reviewAuthorities, sequences }
writeOrCheck(path.join(root, 'data/keeper_prime_animation_drafts_v8.json'), Buffer.from(`${JSON.stringify(manifest, null, 2)}\n`))

const shellBytes = Buffer.from('<!doctype html><meta charset="utf-8"><title>Prime Keeper review V8</title><meta http-equiv="refresh" content="0;url=/prime-keeper-animation-drafts-v8"><a href="/prime-keeper-animation-drafts-v8">Open Prime Keeper review V8</a>\n')
writeOrCheck(path.join(reviewRoot, 'index.html'), shellBytes)
const register = { schema: 'lighthouse-keeper/reversible-review-batch@1', set, status: 'feedback-corrected-review-only', candidate: { publicShell: { file: `public/keeper-review/${set}/index.html`, sha256: sha256(shellBytes) } }, publishedAssets: [...publishedByHash.values()].map(({ source, sourceSha256, publicAssemblyPath, url }) => ({ source, sourceSha256, publicAssemblyPath, url })) }
writeOrCheck(path.join(draftRoot, 'batch-register.json'), Buffer.from(`${JSON.stringify(register, null, 2)}\n`))

console.log(`${check ? 'Verified' : 'Wrote'} Prime morning draft V8: ${sequences.length} sequences, ${frameCount} occurrences, ${publishedByHash.size} unique images, ${correctionRecords.length} exact-outline repairs.`)
