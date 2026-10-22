import crypto from 'node:crypto'
import fs from 'node:fs'
import path from 'node:path'
import { fileURLToPath } from 'node:url'
import { PNG } from 'pngjs'

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..')
const set = 'keeper-prime-morning-drafts-v4'
const reviewRoot = path.join(root, 'public/keeper-review', set)
const assetRoot = path.join(reviewRoot, 'assets')
const draftRoot = path.join(root, 'art/drafts/keeper-prime-morning-drafts-corrections-2026-10-22-v4')
const check = process.argv.includes('--check')
const sha256 = (bytes) => crypto.createHash('sha256').update(bytes).digest('hex')
const v3File = path.join(root, 'data/keeper_prime_animation_drafts_v3.json')
const v3Bytes = fs.readFileSync(v3File)
const v3 = JSON.parse(v3Bytes)
const v3Archive = JSON.parse(fs.readFileSync(path.join(root, 'review-archive/sets/keeper-prime-morning-drafts-v3.json')))
const REAR_AUTHORITY_HASH = '31dbac4efc00089fe6f831dc23f8397b4e3a8faf4d4aaa09a92b2ff407eebc35'

function objectFile(hash, extension = '.png') {
  return path.join(root, 'review-archive/objects', hash.slice(0, 2), `${hash}${extension}`)
}

function archivedFrameBytes(frame) {
  const entry = v3Archive.entries[frame.src]
  if (!entry) throw new Error(`V3 archive entry missing: ${frame.src}`)
  const bytes = fs.readFileSync(path.join(root, entry.object))
  if (sha256(bytes) !== frame.sha256) throw new Error(`V3 frame changed: ${frame.sha256}`)
  return bytes
}

function sourceV2Bytes(frame) {
  const hash = frame.priorV2?.sha256
  if (!hash) throw new Error(`V2 provenance missing: ${frame.id}`)
  const bytes = fs.readFileSync(objectFile(hash))
  if (sha256(bytes) !== hash) throw new Error(`V2 source changed: ${hash}`)
  return bytes
}

function edgeAlpha(image) {
  let count = 0
  for (let x = 0; x < image.width; x += 1) {
    if (image.data[x * 4 + 3]) count += 1
    if (image.data[((image.height - 1) * image.width + x) * 4 + 3]) count += 1
  }
  for (let y = 0; y < image.height; y += 1) {
    if (image.data[(y * image.width) * 4 + 3]) count += 1
    if (image.data[(y * image.width + image.width - 1) * 4 + 3]) count += 1
  }
  return count
}

function copyAuthorityRow(authority, target, y, left, right) {
  for (let x = left; x <= right; x += 1) {
    const offset = (y * target.width + x) * 4
    authority.data.copy(target.data, offset, offset, offset + 4)
  }
}

function repairRearWorkV4(bytes, authorityBytes) {
  const candidate = PNG.sync.read(bytes)
  const authority = PNG.sync.read(authorityBytes)
  if (candidate.width !== 256 || candidate.height !== 320) throw new Error('Rear work source is not a 256x320 isolated frame')

  const centres = []
  for (let y = 188; y < 203; y += 1) {
    const xs = []
    for (let x = 74; x <= 182; x += 1) if (candidate.data[(y * candidate.width + x) * 4 + 3] > 32) xs.push(x)
    if (xs.length) centres.push((xs[0] + xs[xs.length - 1]) / 2)
  }
  centres.sort((a, b) => a - b)
  const dx = Math.round(128 - (centres[Math.floor(centres.length / 2)] ?? 128))
  const image = new PNG({ width: 256, height: 320 })

  // Retain the complete action drawing through the torso and sleeves. At the
  // start of the ribbed hem, switch to one exact approved rear-body component.
  // This removes both generated hip fragments and V3's two rectangular join
  // seams without inventing, smoothing or regenerating a single pixel.
  for (let y = 0; y < 204; y += 1) for (let x = 0; x < candidate.width; x += 1) {
    const targetX = x + dx
    if (targetX < 0 || targetX >= image.width) continue
    const sourceOffset = (y * candidate.width + x) * 4
    const targetOffset = (y * image.width + targetX) * 4
    candidate.data.copy(image.data, targetOffset, sourceOffset, sourceOffset + 4)
  }

  // Rows 204–227 also contain the authority's passive hands. Select only the
  // central blue body run and its contiguous dark outline so those hands do
  // not leak into the action pose. From row 228 the authority is body-only.
  for (let y = 204; y <= 227; y += 1) {
    const blues = []
    for (let x = 76; x <= 179; x += 1) {
      const offset = (y * authority.width + x) * 4
      const r = authority.data[offset]
      const g = authority.data[offset + 1]
      const b = authority.data[offset + 2]
      const a = authority.data[offset + 3]
      if (a > 32 && b > r * 1.15 && b > g * 1.05) blues.push(x)
    }
    if (!blues.length) throw new Error(`Authority body run missing at y=${y}`)
    let left = Math.min(...blues)
    let right = Math.max(...blues)
    for (let step = 0; step < 3 && left > 0; step += 1) {
      const offset = (y * authority.width + left - 1) * 4
      const dark = authority.data[offset + 3] > 0 && Math.max(authority.data[offset], authority.data[offset + 1], authority.data[offset + 2]) < 100
      if (!dark) break
      left -= 1
    }
    for (let step = 0; step < 3 && right < authority.width - 1; step += 1) {
      const offset = (y * authority.width + right + 1) * 4
      const dark = authority.data[offset + 3] > 0 && Math.max(authority.data[offset], authority.data[offset + 1], authority.data[offset + 2]) < 100
      if (!dark) break
      right += 1
    }
    copyAuthorityRow(authority, image, y, left, right)
  }
  for (let y = 228; y < image.height; y += 1) copyAuthorityRow(authority, image, y, 70, 186)
  return PNG.sync.write(image)
}

function writeOrCheck(file, bytes) {
  if (check) {
    let existing = fs.existsSync(file) ? fs.readFileSync(file) : null
    if (!existing && file.startsWith(assetRoot)) {
      const manifestFile = path.join(root, 'review-archive/sets', `${set}.json`)
      if (fs.existsSync(manifestFile)) {
        const manifest = JSON.parse(fs.readFileSync(manifestFile, 'utf8'))
        const url = `/keeper-review/${set}/assets/${path.basename(file)}`
        const entry = manifest.entries?.[url]
        if (entry) existing = fs.readFileSync(path.join(root, entry.object))
      }
    }
    if (!existing || !existing.equals(bytes)) throw new Error(`Stale or missing V4 file: ${path.relative(root, file)}`)
    return
  }
  fs.mkdirSync(path.dirname(file), { recursive: true })
  fs.writeFileSync(file, bytes)
}

function storeObject(bytes) {
  const hash = sha256(bytes)
  const file = objectFile(hash)
  if (check) {
    if (!fs.existsSync(file) || sha256(fs.readFileSync(file)) !== hash) throw new Error(`Missing V4 archive object: ${hash}`)
  } else {
    fs.mkdirSync(path.dirname(file), { recursive: true })
    if (fs.existsSync(file) && sha256(fs.readFileSync(file)) !== hash) throw new Error(`Archive collision: ${hash}`)
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

const authorityBytes = fs.readFileSync(objectFile(REAR_AUTHORITY_HASH))
const publishedByHash = new Map()
const correctionRecords = []
const sequences = []

for (const sequence of v3.sequences) {
  const records = []
  for (let index = 0; index < sequence.frames.length; index += 1) {
    const frame = sequence.frames[index]
    const position = index + 1
    const repaired = sequence.id === 'rear-work-turn-return-v1' && position >= 11 && position <= 31
    const bytes = repaired ? repairRearWorkV4(sourceV2Bytes(frame), authorityBytes) : archivedFrameBytes(frame)
    const image = PNG.sync.read(bytes)
    if (image.width !== frame.cell[0] || image.height !== frame.cell[1]) throw new Error(`${sequence.id} frame ${position}: geometry changed`)
    if (edgeAlpha(image)) throw new Error(`${sequence.id} frame ${position}: opaque cell edge`)
    const hash = sha256(bytes)
    let asset = publishedByHash.get(hash)
    if (!asset) {
      const fileName = `frame-${hash.slice(0, 16)}.png`
      const publicFile = path.join(assetRoot, fileName)
      writeOrCheck(publicFile, bytes)
      const stored = storeObject(bytes)
      const sourceFile = repaired ? path.join(draftRoot, 'frames', fileName) : stored.file
      if (repaired) writeOrCheck(sourceFile, bytes)
      asset = {
        source: path.relative(root, sourceFile).split(path.sep).join('/'),
        sourceSha256: hash,
        publicAssemblyPath: path.relative(root, publicFile).split(path.sep).join('/'),
        url: `/keeper-review/${set}/assets/${fileName}`,
      }
      publishedByHash.set(hash, asset)
    }
    const correction = repaired
      ? 'V3 seam rejected: continuous authority hem and lower body replace the entire generated cut region; action upper body remains unchanged and recentered'
      : frame.correction
    if (repaired) correctionRecords.push({
      sequence: sequence.id,
      position,
      sourceV2Sha256: frame.priorV2.sha256,
      rejectedV3Sha256: frame.sha256,
      draftV4Sha256: hash,
      correction,
    })
    records.push({ frame, bytes, hash, asset, correction, repaired })
  }
  const repairedSequence = sequence.id === 'rear-work-turn-return-v1'
  sequences.push({
    ...sequence,
    status: repairedSequence ? 'feedback-corrected-versioned-draft-v4' : sequence.status,
    source: repairedSequence ? { path: 'art/drafts/keeper-prime-morning-drafts-corrections-2026-10-22-v4/corrections.json', sha256: '' } : sequence.source,
    draftStrip: repairedSequence ? saveStrip(sequence, records) : sequence.draftStrip,
    frames: records.map(({ frame, hash, asset, correction, repaired }, index) => ({
      ...frame,
      id: `${sequence.id}-v4-f${String(index + 1).padStart(2, '0')}`,
      src: asset.url,
      sha256: hash,
      redraftSlot: `${sequence.id}/v4-frame-${String(index + 1).padStart(2, '0')}`,
      priorV3: { position: index + 1, sha256: frame.sha256 },
      ...(repaired ? { amendmentComparison: { label: 'Rejected V3 seam repair', src: frame.src, sha256: frame.sha256 } } : {}),
      correction,
    })),
  })
}

const corrections = {
  schema: 'lighthouse-keeper/prime-animation-feedback-corrections@1',
  version: 4,
  generatedOn: '2026-10-22',
  sourceBatch: 'data/keeper_prime_animation_drafts_v3.json',
  sourceBatchSha256: sha256(v3Bytes),
  authority: { rearBody: REAR_AUTHORITY_HASH },
  rejectedAmendment: {
    version: 3,
    scope: 'rear-work-turn-return-v1 positions 11–31 only',
    reason: 'Two vertical cut seams remained at the bottom of the jumper because V3 replaced only a central rectangle of the hem.',
  },
  frames: correctionRecords,
  imageGeneration: { usedInDelivery: false, reason: 'This identity-critical correction is an exact deterministic composite from hash-pinned Prime source and authority pixels.' },
}
const correctionBytes = Buffer.from(`${JSON.stringify(corrections, null, 2)}\n`)
const correctionHash = sha256(correctionBytes)
sequences.find((sequence) => sequence.id === 'rear-work-turn-return-v1').source.sha256 = correctionHash
writeOrCheck(path.join(draftRoot, 'corrections.json'), correctionBytes)

const reviewAuthorities = Object.fromEntries(Object.entries(v3.reviewAuthorities).map(([name, authority]) => [name, {
  ...authority,
  src: `/keeper-review/${set}/assets/frame-${authority.sha256.slice(0, 16)}.png`,
}]))
const frameCount = sequences.reduce((sum, sequence) => sum + sequence.frames.length, 0)
if (sequences.length !== 10 || frameCount !== 162) throw new Error(`Unexpected V4 inventory: ${sequences.length} sequences, ${frameCount} frames`)
const manifest = {
  ...v3,
  version: 4,
  generatedOn: '2026-10-22',
  status: 'feedback-corrected-review-only',
  note: 'V4 preserves V3 and replaces only rear-task positions 11–31. Their upper-body choreography is retained, while one continuous exact-authority hem and lower body remove V3’s two bottom-jumper seams and all generated hip fragments. No prior review, approved authority, runtime or production file is overwritten.',
  reviewAuthorities,
  sequences,
}
writeOrCheck(path.join(root, 'data/keeper_prime_animation_drafts_v4.json'), Buffer.from(`${JSON.stringify(manifest, null, 2)}\n`))

const shellBytes = Buffer.from('<!doctype html><meta charset="utf-8"><title>Prime Keeper review V4</title><meta http-equiv="refresh" content="0;url=/prime-keeper-animation-drafts-v4"><a href="/prime-keeper-animation-drafts-v4">Open Prime Keeper review V4</a>\n')
writeOrCheck(path.join(reviewRoot, 'index.html'), shellBytes)
const register = {
  schema: 'lighthouse-keeper/reversible-review-batch@1',
  set,
  status: 'feedback-corrected-review-only',
  candidate: { publicShell: { file: `public/keeper-review/${set}/index.html`, sha256: sha256(shellBytes) } },
  publishedAssets: [...publishedByHash.values()].map(({ source, sourceSha256, publicAssemblyPath, url }) => ({ source, sourceSha256, publicAssemblyPath, url })),
}
writeOrCheck(path.join(draftRoot, 'batch-register.json'), Buffer.from(`${JSON.stringify(register, null, 2)}\n`))

console.log(`${check ? 'Verified' : 'Wrote'} Prime morning draft V4: ${sequences.length} sequences, ${frameCount} occurrences, ${publishedByHash.size} unique images, ${correctionRecords.length} rear seam repairs.`)
