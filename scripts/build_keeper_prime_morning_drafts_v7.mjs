import crypto from 'node:crypto'
import fs from 'node:fs'
import path from 'node:path'
import { fileURLToPath } from 'node:url'
import { PNG } from 'pngjs'

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..')
const set = 'keeper-prime-morning-drafts-v7'
const reviewRoot = path.join(root, 'public/keeper-review', set)
const assetRoot = path.join(reviewRoot, 'assets')
const draftRoot = path.join(root, 'art/drafts/keeper-prime-morning-drafts-corrections-2026-10-22-v7')
const check = process.argv.includes('--check')
const sha256 = (bytes) => crypto.createHash('sha256').update(bytes).digest('hex')
const v6File = path.join(root, 'data/keeper_prime_animation_drafts_v6.json')
const v6Bytes = fs.readFileSync(v6File)
const v6 = JSON.parse(v6Bytes)
const v6Archive = JSON.parse(fs.readFileSync(path.join(root, 'review-archive/sets/keeper-prime-morning-drafts-v6.json')))
const REAR_AUTHORITY_HASH = 'e6520aab48100c44aabdb0825c9424dbe35bffb2587b5270898e5214db2038df'
const BODY_LEFT = 84
const BODY_RIGHT = 171

function objectFile(hash, extension = '.png') {
  return path.join(root, 'review-archive/objects', hash.slice(0, 2), `${hash}${extension}`)
}

function archivedFrameBytes(frame) {
  const entry = v6Archive.entries[frame.src]
  if (!entry) throw new Error(`V6 archive entry missing: ${frame.src}`)
  const bytes = fs.readFileSync(path.join(root, entry.object))
  if (sha256(bytes) !== frame.sha256) throw new Error(`V6 frame changed: ${frame.sha256}`)
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

function copyPixel(source, target, y, x) {
  const offset = (y * source.width + x) * 4
  source.data.copy(target.data, offset, offset, offset + 4)
}

function repairRearWorkV7(bytes, authorityBytes) {
  const candidate = PNG.sync.read(bytes)
  const authority = PNG.sync.read(authorityBytes)
  if (candidate.width !== 256 || candidate.height !== 320) throw new Error('Rear work source is not a 256x320 isolated frame')
  const image = PNG.sync.read(PNG.sync.write(candidate))

  // V6 retained the generated action source's duplicated lower ribbing. Keep
  // its head, beard, shoulders and working arms through row 179, then give the
  // complete lower torso and jumper to the current corrected rear authority.
  // The fixed 84–171 centre interval is bounded by the authority's own inner
  // torso outlines, excluding its passive sleeves and hands as well as every
  // generated hip fragment.
  for (let y = 180; y <= 230; y += 1) {
    image.data.fill(0, y * 256 * 4, (y + 1) * 256 * 4)
    for (let x = BODY_LEFT; x <= BODY_RIGHT; x += 1) copyPixel(authority, image, y, x)
  }

  // The complete corrected authority root supplies trousers and boots.
  for (let y = 231; y < 320; y += 1) {
    image.data.fill(0, y * 256 * 4, (y + 1) * 256 * 4)
    for (let x = 70; x <= 186; x += 1) copyPixel(authority, image, y, x)
  }
  return { bytes: PNG.sync.write(image), actionRetainedThrough: 179, authorityTorsoStart: 180, authorityRootStart: 231, bodyLeft: BODY_LEFT, bodyRight: BODY_RIGHT }
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
    if (!existing || !existing.equals(bytes)) throw new Error(`Stale or missing V7 file: ${path.relative(root, file)}`)
    return
  }
  fs.mkdirSync(path.dirname(file), { recursive: true })
  fs.writeFileSync(file, bytes)
}

function storeObject(bytes) {
  const hash = sha256(bytes)
  const file = objectFile(hash)
  if (check) {
    if (!fs.existsSync(file) || sha256(fs.readFileSync(file)) !== hash) throw new Error(`Missing V7 archive object: ${hash}`)
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

for (const sequence of v6.sequences) {
  const records = []
  for (let index = 0; index < sequence.frames.length; index += 1) {
    const frame = sequence.frames[index]
    const position = index + 1
    const repaired = sequence.id === 'rear-work-turn-return-v1' && position >= 11 && position <= 31
    const sourceBytes = archivedFrameBytes(frame)
    const result = repaired ? repairRearWorkV7(sourceBytes, authorityBytes) : { bytes: sourceBytes }
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
      ? 'V6 rejected: its generated lower jumper contains two ribbed bands; V7 keeps the action above the waist but uses the corrected rear Prime authority for one lower-jumper hem, trousers and boots'
      : frame.correction
    if (repaired) correctionRecords.push({ sequence: sequence.id, position, sourceV2Sha256: frame.priorV2.sha256, rejectedV6Sha256: frame.sha256, draftV7Sha256: hash, actionRetainedThrough: result.actionRetainedThrough, authorityTorsoStart: result.authorityTorsoStart, authorityRootStart: result.authorityRootStart, bodyLeft: result.bodyLeft, bodyRight: result.bodyRight, correction })
    records.push({ frame, bytes: result.bytes, hash, asset, correction, repaired })
  }
  const repairedSequence = sequence.id === 'rear-work-turn-return-v1'
  sequences.push({
    ...sequence,
    status: repairedSequence ? 'feedback-corrected-versioned-draft-v7' : sequence.status,
    source: repairedSequence ? { path: 'art/drafts/keeper-prime-morning-drafts-corrections-2026-10-22-v7/corrections.json', sha256: '' } : sequence.source,
    draftStrip: repairedSequence ? saveStrip(sequence, records) : sequence.draftStrip,
    frames: records.map(({ frame, hash, asset, correction, repaired }, index) => ({
      ...frame,
      id: `${sequence.id}-v7-f${String(index + 1).padStart(2, '0')}`,
      src: asset.url,
      sha256: hash,
      redraftSlot: `${sequence.id}/v7-frame-${String(index + 1).padStart(2, '0')}`,
      priorV6: { position: index + 1, sha256: frame.sha256 },
      ...(repaired ? { amendmentComparison: { label: 'Rejected V6 doubled lower jumper', src: frame.src, sha256: frame.sha256 } } : {}),
      correction,
    })),
  })
}

const corrections = {
  schema: 'lighthouse-keeper/prime-animation-feedback-corrections@1',
  version: 7,
  generatedOn: '2026-10-22',
  sourceBatch: 'data/keeper_prime_animation_drafts_v6.json',
  sourceBatchSha256: sha256(v6Bytes),
  authority: { rearBody: REAR_AUTHORITY_HASH },
  rejectedAmendment: { version: 6, scope: 'rear-work-turn-return-v1 positions 11–31 only', reason: 'V6 retained the generated source lower jumper, whose second ribbed band reads as a duplicated, independently moving bottom seam in every affected frame.' },
  frames: correctionRecords,
  imageGeneration: { usedInDelivery: false, reason: 'This identity-critical correction is an exact deterministic ownership composite from hash-pinned Prime action and authority pixels.' },
}
const correctionBytes = Buffer.from(`${JSON.stringify(corrections, null, 2)}\n`)
const correctionHash = sha256(correctionBytes)
sequences.find((sequence) => sequence.id === 'rear-work-turn-return-v1').source.sha256 = correctionHash
writeOrCheck(path.join(draftRoot, 'corrections.json'), correctionBytes)

const reviewAuthorities = Object.fromEntries(Object.entries(v6.reviewAuthorities).map(([name, authority]) => [name, { ...authority, src: `/keeper-review/${set}/assets/frame-${authority.sha256.slice(0, 16)}.png` }]))
const frameCount = sequences.reduce((sum, sequence) => sum + sequence.frames.length, 0)
if (sequences.length !== 10 || frameCount !== 162) throw new Error(`Unexpected V7 inventory: ${sequences.length} sequences, ${frameCount} frames`)
const manifest = {
  ...v6,
  version: 7,
  generatedOn: '2026-10-22',
  status: 'feedback-corrected-review-only',
  note: 'V7 preserves rejected V6 and replaces only rear-task positions 11–31. It removes the generated duplicated lower-jumper band, retains the action above the waist, and uses the current corrected rear Prime authority for one hem, trousers and boots. No prior review, approved authority, runtime or production file is overwritten.',
  reviewAuthorities,
  sequences,
}
writeOrCheck(path.join(root, 'data/keeper_prime_animation_drafts_v7.json'), Buffer.from(`${JSON.stringify(manifest, null, 2)}\n`))

const shellBytes = Buffer.from('<!doctype html><meta charset="utf-8"><title>Prime Keeper review V7</title><meta http-equiv="refresh" content="0;url=/prime-keeper-animation-drafts-v7"><a href="/prime-keeper-animation-drafts-v7">Open Prime Keeper review V7</a>\n')
writeOrCheck(path.join(reviewRoot, 'index.html'), shellBytes)
const register = { schema: 'lighthouse-keeper/reversible-review-batch@1', set, status: 'feedback-corrected-review-only', candidate: { publicShell: { file: `public/keeper-review/${set}/index.html`, sha256: sha256(shellBytes) } }, publishedAssets: [...publishedByHash.values()].map(({ source, sourceSha256, publicAssemblyPath, url }) => ({ source, sourceSha256, publicAssemblyPath, url })) }
writeOrCheck(path.join(draftRoot, 'batch-register.json'), Buffer.from(`${JSON.stringify(register, null, 2)}\n`))

console.log(`${check ? 'Verified' : 'Wrote'} Prime morning draft V7: ${sequences.length} sequences, ${frameCount} occurrences, ${publishedByHash.size} unique images, ${correctionRecords.length} single-hem repairs.`)
