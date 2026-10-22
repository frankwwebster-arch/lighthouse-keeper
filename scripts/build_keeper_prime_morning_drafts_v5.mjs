import crypto from 'node:crypto'
import fs from 'node:fs'
import path from 'node:path'
import { fileURLToPath } from 'node:url'
import { PNG } from 'pngjs'

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..')
const set = 'keeper-prime-morning-drafts-v5'
const reviewRoot = path.join(root, 'public/keeper-review', set)
const assetRoot = path.join(reviewRoot, 'assets')
const draftRoot = path.join(root, 'art/drafts/keeper-prime-morning-drafts-corrections-2026-10-22-v5')
const check = process.argv.includes('--check')
const sha256 = (bytes) => crypto.createHash('sha256').update(bytes).digest('hex')
const v4File = path.join(root, 'data/keeper_prime_animation_drafts_v4.json')
const v4Bytes = fs.readFileSync(v4File)
const v4 = JSON.parse(v4Bytes)
const v4Archive = JSON.parse(fs.readFileSync(path.join(root, 'review-archive/sets/keeper-prime-morning-drafts-v4.json')))
const REAR_AUTHORITY_HASH = '31dbac4efc00089fe6f831dc23f8397b4e3a8faf4d4aaa09a92b2ff407eebc35'

function objectFile(hash, extension = '.png') {
  return path.join(root, 'review-archive/objects', hash.slice(0, 2), `${hash}${extension}`)
}

function archivedFrameBytes(frame) {
  const entry = v4Archive.entries[frame.src]
  if (!entry) throw new Error(`V4 archive entry missing: ${frame.src}`)
  const bytes = fs.readFileSync(path.join(root, entry.object))
  if (sha256(bytes) !== frame.sha256) throw new Error(`V4 frame changed: ${frame.sha256}`)
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

function repairRearWorkV5(bytes, authorityBytes) {
  const candidate = PNG.sync.read(bytes)
  const authority = PNG.sync.read(authorityBytes)
  if (candidate.width !== 256 || candidate.height !== 320) throw new Error('Rear work source is not a 256x320 isolated frame')
  const image = new PNG({ width: 256, height: 320 })
  const dx = recenterDx(candidate)

  // The approved rear trousers own the lower component. At the waist, select
  // only navy trouser material and its adjacent outline, then retain the
  // connected central component. This excludes the authority's passive hands
  // and the three detached fragments that escaped V4 at rows 223/228/229.
  const pantColour = new Uint8Array(256 * 320)
  for (let y = 219; y <= 235; y += 1) for (let x = 76; x <= 180; x += 1) {
    const offset = (y * 256 + x) * 4
    const [r, g, b, a] = authority.data.subarray(offset, offset + 4)
    if (a > 0 && r < 120 && b > r && b >= g && b < 160) pantColour[y * 256 + x] = 1
  }
  const pantMask = new Uint8Array(256 * 320)
  for (let y = 219; y <= 235; y += 1) for (let x = 76; x <= 180; x += 1) {
    const offset = (y * 256 + x) * 4
    const [r, g, b, a] = authority.data.subarray(offset, offset + 4)
    let keep = Boolean(pantColour[y * 256 + x])
    if (!keep && a > 0 && Math.max(r, g, b) < 100) {
      for (let ny = Math.max(219, y - 2); ny <= Math.min(235, y + 2) && !keep; ny += 1) {
        for (let nx = Math.max(76, x - 2); nx <= Math.min(180, x + 2); nx += 1) {
          if (pantColour[ny * 256 + nx]) { keep = true; break }
        }
      }
    }
    if (keep) pantMask[y * 256 + x] = 1
  }
  const owned = new Uint8Array(256 * 320)
  const stack = [219 * 256 + 128]
  owned[stack[0]] = 1
  while (stack.length) {
    const current = stack.pop()
    const y = Math.floor(current / 256)
    const x = current % 256
    const offset = current * 4
    authority.data.copy(image.data, offset, offset, offset + 4)
    for (const [nextX, nextY] of [[x - 1, y], [x + 1, y], [x, y - 1], [x, y + 1]]) {
      if (nextX < 76 || nextX > 180 || nextY < 219 || nextY > 235) continue
      const next = nextY * 256 + nextX
      if (!owned[next] && pantMask[next]) { owned[next] = 1; stack.push(next) }
    }
  }
  for (let y = 236; y < 320; y += 1) for (let x = 70; x <= 186; x += 1) {
    const offset = (y * 256 + x) * 4
    authority.data.copy(image.data, offset, offset, offset + 4)
  }

  // Keep the full moving action drawing through the sleeves, then retain the
  // source's complete ribbed hem as one central component. V4 cut this moving
  // hem at row 203 and exposed a second fixed hem below it. V5 copies the
  // moving hem through its sole lower edge (row 218) and begins the approved
  // trousers behind it at row 219.
  for (let y = 0; y < 195; y += 1) copyShiftedRow(candidate, image, y, 0, 255, dx)
  const centre = 128 - dx
  const cap = centralRun(candidate, 206, centre)
  for (let y = 195; y <= 218; y += 1) {
    const run = centralRun(candidate, y, centre)
    const lowerLeft = y >= 213 ? 76 - dx : 0
    const lowerRight = y >= 213 ? 180 - dx : 255
    copyShiftedRow(candidate, image, y, Math.max(run.left, cap.left, lowerLeft), Math.min(run.right, cap.right, lowerRight), dx)
  }
  return { bytes: PNG.sync.write(image), dx, hemCap: [cap.left + dx, cap.right + dx] }
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
    if (!existing || !existing.equals(bytes)) throw new Error(`Stale or missing V5 file: ${path.relative(root, file)}`)
    return
  }
  fs.mkdirSync(path.dirname(file), { recursive: true })
  fs.writeFileSync(file, bytes)
}

function storeObject(bytes) {
  const hash = sha256(bytes)
  const file = objectFile(hash)
  if (check) {
    if (!fs.existsSync(file) || sha256(fs.readFileSync(file)) !== hash) throw new Error(`Missing V5 archive object: ${hash}`)
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

for (const sequence of v4.sequences) {
  const records = []
  for (let index = 0; index < sequence.frames.length; index += 1) {
    const frame = sequence.frames[index]
    const position = index + 1
    const repaired = sequence.id === 'rear-work-turn-return-v1' && position >= 11 && position <= 31
    const result = repaired ? repairRearWorkV5(sourceV2Bytes(frame), authorityBytes) : { bytes: archivedFrameBytes(frame) }
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
      ? 'V4 rejected: complete moving V2 jumper hem now occludes the fixed join; exact authority trousers begin behind it and detached waist fragments are excluded by component ownership'
      : frame.correction
    if (repaired) correctionRecords.push({ sequence: sequence.id, position, sourceV2Sha256: frame.priorV2.sha256, rejectedV4Sha256: frame.sha256, draftV5Sha256: hash, recenterDx: result.dx, movingHemCap: result.hemCap, correction })
    records.push({ frame, bytes: result.bytes, hash, asset, correction, repaired })
  }
  const repairedSequence = sequence.id === 'rear-work-turn-return-v1'
  sequences.push({
    ...sequence,
    status: repairedSequence ? 'feedback-corrected-versioned-draft-v5' : sequence.status,
    source: repairedSequence ? { path: 'art/drafts/keeper-prime-morning-drafts-corrections-2026-10-22-v5/corrections.json', sha256: '' } : sequence.source,
    draftStrip: repairedSequence ? saveStrip(sequence, records) : sequence.draftStrip,
    frames: records.map(({ frame, hash, asset, correction, repaired }, index) => ({
      ...frame,
      id: `${sequence.id}-v5-f${String(index + 1).padStart(2, '0')}`,
      src: asset.url,
      sha256: hash,
      redraftSlot: `${sequence.id}/v5-frame-${String(index + 1).padStart(2, '0')}`,
      priorV4: { position: index + 1, sha256: frame.sha256 },
      ...(repaired ? { amendmentComparison: { label: 'Rejected V4 split-hem composite', src: frame.src, sha256: frame.sha256 } } : {}),
      correction,
    })),
  })
}

const corrections = {
  schema: 'lighthouse-keeper/prime-animation-feedback-corrections@1',
  version: 5,
  generatedOn: '2026-10-22',
  sourceBatch: 'data/keeper_prime_animation_drafts_v4.json',
  sourceBatchSha256: sha256(v4Bytes),
  authority: { rearBody: REAR_AUTHORITY_HASH },
  rejectedAmendment: { version: 4, scope: 'rear-work-turn-return-v1 positions 11–31 only', reason: 'V4 cut through the moving ribbed hem, exposed a second fixed hem beneath it, and copied three detached authority fragments at rows 223, 228 and 229.' },
  frames: correctionRecords,
  imageGeneration: { usedInDelivery: false, reason: 'This identity-critical correction is an exact deterministic ownership composite from hash-pinned Prime action and authority pixels.' },
}
const correctionBytes = Buffer.from(`${JSON.stringify(corrections, null, 2)}\n`)
const correctionHash = sha256(correctionBytes)
sequences.find((sequence) => sequence.id === 'rear-work-turn-return-v1').source.sha256 = correctionHash
writeOrCheck(path.join(draftRoot, 'corrections.json'), correctionBytes)

const reviewAuthorities = Object.fromEntries(Object.entries(v4.reviewAuthorities).map(([name, authority]) => [name, { ...authority, src: `/keeper-review/${set}/assets/frame-${authority.sha256.slice(0, 16)}.png` }]))
const frameCount = sequences.reduce((sum, sequence) => sum + sequence.frames.length, 0)
if (sequences.length !== 10 || frameCount !== 162) throw new Error(`Unexpected V5 inventory: ${sequences.length} sequences, ${frameCount} frames`)
const manifest = {
  ...v4,
  version: 5,
  generatedOn: '2026-10-22',
  status: 'feedback-corrected-review-only',
  note: 'V5 preserves V4 and replaces only rear-task positions 11–31. Their complete moving jumper hems now occlude the fixed join, approved rear trousers begin behind them, and detached authority fragments are excluded. No prior review, approved authority, runtime or production file is overwritten.',
  reviewAuthorities,
  sequences,
}
writeOrCheck(path.join(root, 'data/keeper_prime_animation_drafts_v5.json'), Buffer.from(`${JSON.stringify(manifest, null, 2)}\n`))

const shellBytes = Buffer.from('<!doctype html><meta charset="utf-8"><title>Prime Keeper review V5</title><meta http-equiv="refresh" content="0;url=/prime-keeper-animation-drafts-v5"><a href="/prime-keeper-animation-drafts-v5">Open Prime Keeper review V5</a>\n')
writeOrCheck(path.join(reviewRoot, 'index.html'), shellBytes)
const register = { schema: 'lighthouse-keeper/reversible-review-batch@1', set, status: 'feedback-corrected-review-only', candidate: { publicShell: { file: `public/keeper-review/${set}/index.html`, sha256: sha256(shellBytes) } }, publishedAssets: [...publishedByHash.values()].map(({ source, sourceSha256, publicAssemblyPath, url }) => ({ source, sourceSha256, publicAssemblyPath, url })) }
writeOrCheck(path.join(draftRoot, 'batch-register.json'), Buffer.from(`${JSON.stringify(register, null, 2)}\n`))

console.log(`${check ? 'Verified' : 'Wrote'} Prime morning draft V5: ${sequences.length} sequences, ${frameCount} occurrences, ${publishedByHash.size} unique images, ${correctionRecords.length} moving-hem ownership repairs.`)
