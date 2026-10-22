import crypto from 'node:crypto'
import fs from 'node:fs'
import path from 'node:path'
import { fileURLToPath } from 'node:url'
import { PNG } from 'pngjs'

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..')
const set = 'keeper-prime-morning-drafts-v6'
const reviewRoot = path.join(root, 'public/keeper-review', set)
const assetRoot = path.join(reviewRoot, 'assets')
const draftRoot = path.join(root, 'art/drafts/keeper-prime-morning-drafts-corrections-2026-10-22-v6')
const check = process.argv.includes('--check')
const sha256 = (bytes) => crypto.createHash('sha256').update(bytes).digest('hex')
const v5File = path.join(root, 'data/keeper_prime_animation_drafts_v5.json')
const v5Bytes = fs.readFileSync(v5File)
const v5 = JSON.parse(v5Bytes)
const v5Archive = JSON.parse(fs.readFileSync(path.join(root, 'review-archive/sets/keeper-prime-morning-drafts-v5.json')))
const REAR_AUTHORITY_HASH = '31dbac4efc00089fe6f831dc23f8397b4e3a8faf4d4aaa09a92b2ff407eebc35'

function objectFile(hash, extension = '.png') {
  return path.join(root, 'review-archive/objects', hash.slice(0, 2), `${hash}${extension}`)
}

function archivedFrameBytes(frame) {
  const entry = v5Archive.entries[frame.src]
  if (!entry) throw new Error(`V5 archive entry missing: ${frame.src}`)
  const bytes = fs.readFileSync(path.join(root, entry.object))
  if (sha256(bytes) !== frame.sha256) throw new Error(`V5 frame changed: ${frame.sha256}`)
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

function recenterDx(candidate) {
  const centres = []
  for (let y = 188; y < 203; y += 1) {
    const xs = []
    for (let x = 74; x <= 182; x += 1) if (candidate.data[(y * candidate.width + x) * 4 + 3] > 32) xs.push(x)
    if (xs.length) centres.push((xs[0] + xs[xs.length - 1]) / 2)
  }
  centres.sort((a, b) => a - b)
  return Math.round(128 - (centres[Math.floor(centres.length / 2)] ?? 128))
}

function copyShiftedRow(source, target, y, left, right, dx) {
  for (let x = left; x <= right; x += 1) {
    const targetX = x + dx
    if (targetX < 0 || targetX >= target.width) continue
    const sourceOffset = (y * source.width + x) * 4
    const targetOffset = (y * target.width + targetX) * 4
    source.data.copy(target.data, targetOffset, sourceOffset, sourceOffset + 4)
  }
}

function centralRun(image, y, centre) {
  let cursor = Math.max(0, Math.min(image.width - 1, centre))
  while (cursor > 0 && image.data[(y * image.width + cursor) * 4 + 3] === 0) cursor -= 1
  let left = cursor
  let right = cursor
  while (left > 0 && image.data[(y * image.width + left - 1) * 4 + 3] > 0) left -= 1
  while (right < image.width - 1 && image.data[(y * image.width + right + 1) * 4 + 3] > 0) right += 1
  return { left, right }
}

function repairRearWorkV6(bytes, authorityBytes) {
  const candidate = PNG.sync.read(bytes)
  const authority = PNG.sync.read(authorityBytes)
  if (candidate.width !== 256 || candidate.height !== 320) throw new Error('Rear work source is not a 256x320 isolated frame')
  const image = new PNG({ width: 256, height: 320 })
  const dx = recenterDx(candidate)

  // V5 introduced a hard ownership cut at row 219. Keep the original action
  // body and its one complete ribbed hem instead, then ease its horizontal
  // registration back to the fixed root over rows 195–230. The transition is
  // zero at row 230, so the authority trousers begin on the next row without
  // a lateral step, second hem or new black waist line.
  for (let y = 0; y <= 230; y += 1) {
    const rowDx = y <= 194 ? dx : Math.round(dx * (230 - y) / 36)
    if (y >= 214) {
      const run = centralRun(candidate, y, 128)
      // At rows 220–221 the generated hip strokes touch the true body run.
      // Bound those two bridge rows by the clean runs immediately above and
      // below; all other affected rows can use their own central run directly.
      const upper = centralRun(candidate, 219, 128)
      const lower = centralRun(candidate, 222, 128)
      const left = y === 220 || y === 221 ? Math.max(run.left, Math.min(upper.left, lower.left)) : run.left
      const right = y === 220 || y === 221 ? Math.min(run.right, Math.max(upper.right, lower.right)) : run.right
      copyShiftedRow(candidate, image, y, left, right, rowDx)
    } else {
      copyShiftedRow(candidate, image, y, 0, 255, rowDx)
    }
  }

  // At row 231 the original action and the approved rear authority share the
  // same leg split and outer geometry. Switching here removes generated trouser
  // speckles while leaving the natural source hem/trouser join untouched.
  for (let y = 231; y < 320; y += 1) for (let x = 70; x <= 186; x += 1) {
    const offset = (y * 256 + x) * 4
    authority.data.copy(image.data, offset, offset, offset + 4)
  }
  return { bytes: PNG.sync.write(image), dx, taperStart: 195, taperEnd: 230, authorityStart: 231 }
}

function writeOrCheck(file, bytes) {
  if (check) {
    let existing = fs.existsSync(file) ? fs.readFileSync(file) : null
    if (!existing && file.startsWith(assetRoot)) {
      const manifestFile = path.join(root, 'review-archive/sets', `${set}.json`)
      if (fs.existsSync(manifestFile)) {
        const manifest = JSON.parse(fs.readFileSync(manifestFile, 'utf8'))
        const entry = manifest.entries?.[`/keeper-review/${set}/assets/${path.basename(file)}`]
        if (entry) existing = fs.readFileSync(path.join(root, entry.object))
      }
    }
    if (!existing || !existing.equals(bytes)) throw new Error(`Stale or missing V6 file: ${path.relative(root, file)}`)
    return
  }
  fs.mkdirSync(path.dirname(file), { recursive: true })
  fs.writeFileSync(file, bytes)
}

function storeObject(bytes) {
  const hash = sha256(bytes)
  const file = objectFile(hash)
  if (check) {
    if (!fs.existsSync(file) || sha256(fs.readFileSync(file)) !== hash) throw new Error(`Missing V6 archive object: ${hash}`)
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

for (const sequence of v5.sequences) {
  const records = []
  for (let index = 0; index < sequence.frames.length; index += 1) {
    const frame = sequence.frames[index]
    const position = index + 1
    const repaired = sequence.id === 'rear-work-turn-return-v1' && position >= 11 && position <= 31
    const result = repaired ? repairRearWorkV6(sourceV2Bytes(frame), authorityBytes) : { bytes: archivedFrameBytes(frame) }
    const image = PNG.sync.read(result.bytes)
    if (image.width !== frame.cell[0] || image.height !== frame.cell[1]) throw new Error(`${sequence.id} frame ${position}: geometry changed`)
    if (edgeAlpha(image)) throw new Error(`${sequence.id} frame ${position}: opaque cell edge`)
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
      ? 'V5 rejected: the complete V2 action hem is tapered onto the fixed root; only its central waist run survives, and exact authority trousers begin below the geometry-matched crotch split'
      : frame.correction
    if (repaired) correctionRecords.push({ sequence: sequence.id, position, sourceV2Sha256: frame.priorV2.sha256, rejectedV5Sha256: frame.sha256, draftV6Sha256: hash, recenterDx: result.dx, taperStart: result.taperStart, taperEnd: result.taperEnd, authorityStart: result.authorityStart, correction })
    records.push({ frame, bytes: result.bytes, hash, asset, correction, repaired })
  }
  const repairedSequence = sequence.id === 'rear-work-turn-return-v1'
  sequences.push({
    ...sequence,
    status: repairedSequence ? 'feedback-corrected-versioned-draft-v6' : sequence.status,
    source: repairedSequence ? { path: 'art/drafts/keeper-prime-morning-drafts-corrections-2026-10-22-v6/corrections.json', sha256: '' } : sequence.source,
    draftStrip: repairedSequence ? saveStrip(sequence, records) : sequence.draftStrip,
    frames: records.map(({ frame, hash, asset, correction, repaired }, index) => ({
      ...frame,
      id: `${sequence.id}-v6-f${String(index + 1).padStart(2, '0')}`,
      src: asset.url,
      sha256: hash,
      redraftSlot: `${sequence.id}/v6-frame-${String(index + 1).padStart(2, '0')}`,
      priorV5: { position: index + 1, sha256: frame.sha256 },
      ...(repaired ? { amendmentComparison: { label: 'Rejected V5 hard waist cut', src: frame.src, sha256: frame.sha256 } } : {}),
      correction,
    })),
  })
}

const corrections = {
  schema: 'lighthouse-keeper/prime-animation-feedback-corrections@1',
  version: 6,
  generatedOn: '2026-10-22',
  sourceBatch: 'data/keeper_prime_animation_drafts_v5.json',
  sourceBatchSha256: sha256(v5Bytes),
  authority: { rearBody: REAR_AUTHORITY_HASH },
  rejectedAmendment: { version: 5, scope: 'rear-work-turn-return-v1 positions 11–31 only', reason: 'V5 made the repair worse by introducing a harsh horizontal waist cut and an unstable moving-hem/fixed-trouser handoff.' },
  frames: correctionRecords,
  imageGeneration: { usedInDelivery: false, reason: 'This identity-critical correction is an exact deterministic ownership composite from hash-pinned Prime action and authority pixels.' },
}
const correctionBytes = Buffer.from(`${JSON.stringify(corrections, null, 2)}\n`)
const correctionHash = sha256(correctionBytes)
sequences.find((sequence) => sequence.id === 'rear-work-turn-return-v1').source.sha256 = correctionHash
writeOrCheck(path.join(draftRoot, 'corrections.json'), correctionBytes)

const reviewAuthorities = Object.fromEntries(Object.entries(v5.reviewAuthorities).map(([name, authority]) => [name, { ...authority, src: `/keeper-review/${set}/assets/frame-${authority.sha256.slice(0, 16)}.png` }]))
const frameCount = sequences.reduce((sum, sequence) => sum + sequence.frames.length, 0)
if (sequences.length !== 10 || frameCount !== 162) throw new Error(`Unexpected V6 inventory: ${sequences.length} sequences, ${frameCount} frames`)
const manifest = {
  ...v5,
  version: 6,
  generatedOn: '2026-10-22',
  status: 'feedback-corrected-review-only',
  note: 'V6 preserves rejected V5 and replaces only rear-task positions 11–31. The complete source hem now tapers onto the fixed root, outboard artefact runs are removed, and exact authority trousers begin below the geometry-matched crotch split. No prior review, approved authority, runtime or production file is overwritten.',
  reviewAuthorities,
  sequences,
}
writeOrCheck(path.join(root, 'data/keeper_prime_animation_drafts_v6.json'), Buffer.from(`${JSON.stringify(manifest, null, 2)}\n`))

const shellBytes = Buffer.from('<!doctype html><meta charset="utf-8"><title>Prime Keeper review V6</title><meta http-equiv="refresh" content="0;url=/prime-keeper-animation-drafts-v6"><a href="/prime-keeper-animation-drafts-v6">Open Prime Keeper review V6</a>\n')
writeOrCheck(path.join(reviewRoot, 'index.html'), shellBytes)
const register = { schema: 'lighthouse-keeper/reversible-review-batch@1', set, status: 'feedback-corrected-review-only', candidate: { publicShell: { file: `public/keeper-review/${set}/index.html`, sha256: sha256(shellBytes) } }, publishedAssets: [...publishedByHash.values()].map(({ source, sourceSha256, publicAssemblyPath, url }) => ({ source, sourceSha256, publicAssemblyPath, url })) }
writeOrCheck(path.join(draftRoot, 'batch-register.json'), Buffer.from(`${JSON.stringify(register, null, 2)}\n`))

console.log(`${check ? 'Verified' : 'Wrote'} Prime morning draft V6: ${sequences.length} sequences, ${frameCount} occurrences, ${publishedByHash.size} unique images, ${correctionRecords.length} tapered-root repairs.`)
