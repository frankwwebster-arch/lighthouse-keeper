import crypto from 'node:crypto'
import fs from 'node:fs'
import path from 'node:path'
import { fileURLToPath } from 'node:url'
import { PNG } from 'pngjs'

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..')
const set = 'keeper-prime-morning-drafts-v3'
const reviewRoot = path.join(root, 'public/keeper-review', set)
const assetRoot = path.join(reviewRoot, 'assets')
const draftRoot = path.join(root, 'art/drafts/keeper-prime-morning-drafts-corrections-2026-10-22-v3')
const check = process.argv.includes('--check')
const sha256 = (bytes) => crypto.createHash('sha256').update(bytes).digest('hex')
const v2 = JSON.parse(fs.readFileSync(path.join(root, 'data/keeper_prime_animation_drafts_v2.json'), 'utf8'))
const FRONT_HASHES = new Set([
  'a9a5c37fe72221992ec499fa3096fdd0581977b4ac03ff7788da2af411107a2e',
  'a61f822bead5dcabda07feea87e17754e85bdd85682bb4b479fcfee9ed54766c',
])
const BACK_HASH = 'd3e7c44b241030c02023f5f5aa8dbf7953162489f7c8b6c1f0b5ad72b321e1bd'
const REAR_AUTHORITY_HASH = '31dbac4efc00089fe6f831dc23f8397b4e3a8faf4d4aaa09a92b2ff407eebc35'

function objectFile(hash, extension = '.png') {
  return path.join(root, 'review-archive/objects', hash.slice(0, 2), `${hash}${extension}`)
}

function frameBytes(frame) {
  const file = objectFile(frame.sha256)
  if (!fs.existsSync(file)) throw new Error(`Archived V2 frame missing: ${frame.sha256}`)
  const bytes = fs.readFileSync(file)
  if (sha256(bytes) !== frame.sha256) throw new Error(`Archived V2 frame changed: ${frame.sha256}`)
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

function jumperPixels(image) {
  const result = []
  for (let y = 112; y < 226; y += 1) {
    for (let x = 28; x < image.width - 28; x += 1) {
      const offset = (y * image.width + x) * 4
      const r = image.data[offset]
      const g = image.data[offset + 1]
      const b = image.data[offset + 2]
      const a = image.data[offset + 3]
      if (a > 0 && b > g * 1.18 && g > r + 18 && b > r + 42) result.push(offset)
    }
  }
  return result
}

const luma = (image, offset) => 0.2126 * image.data[offset] + 0.7152 * image.data[offset + 1] + 0.0722 * image.data[offset + 2]

function registerJumperPalette(bytes, authorityBytes) {
  const image = PNG.sync.read(bytes)
  const authority = PNG.sync.read(authorityBytes)
  const target = jumperPixels(image).sort((a, b) => luma(image, a) - luma(image, b))
  const samples = jumperPixels(authority).sort((a, b) => luma(authority, a) - luma(authority, b))
  if (target.length < 4000 || samples.length < 4000) throw new Error('Jumper palette mask is unexpectedly small')
  for (let rank = 0; rank < target.length; rank += 1) {
    const sourceOffset = samples[Math.round(rank * (samples.length - 1) / Math.max(1, target.length - 1))]
    const targetOffset = target[rank]
    image.data[targetOffset] = authority.data[sourceOffset]
    image.data[targetOffset + 1] = authority.data[sourceOffset + 1]
    image.data[targetOffset + 2] = authority.data[sourceOffset + 2]
  }
  return PNG.sync.write(image)
}

function repairRearWork(bytes, authorityBytes) {
  const candidate = PNG.sync.read(bytes)
  const authority = PNG.sync.read(authorityBytes)
  if (candidate.width !== 256 || candidate.height !== 320) throw new Error('Rear work source is not a 256x320 isolated frame')
  // The V1 builder locked only pixels it classified as trousers/boots. It left
  // a generated cut outline around the hips, while the upper body leaned about
  // a different centre from the fixed legs. Centre the complete, continuous
  // upper-body drawing over x=128, then join it to a full exact-authority
  // waistband/lower body. The continuous cream band is retained.
  const centres = []
  for (let y = 188; y < 203; y += 1) {
    const xs = []
    for (let x = 74; x <= 182; x += 1) if (candidate.data[(y * candidate.width + x) * 4 + 3] > 32) xs.push(x)
    if (xs.length) centres.push((xs[0] + xs[xs.length - 1]) / 2)
  }
  centres.sort((a, b) => a - b)
  const centre = centres[Math.floor(centres.length / 2)] ?? 128
  const dx = Math.round(128 - centre)
  const image = new PNG({ width: 256, height: 320 })
  for (let y = 0; y < 205; y += 1) {
    for (let x = 0; x < candidate.width; x += 1) {
      const targetX = x + dx
      if (targetX < 0 || targetX >= image.width) continue
      const sourceOffset = (y * candidate.width + x) * 4
      const targetOffset = (y * image.width + targetX) * 4
      candidate.data.copy(image.data, targetOffset, sourceOffset, sourceOffset + 4)
    }
  }
  for (let y = 205; y < 235; y += 1) {
    for (let x = 82; x <= 174; x += 1) {
      const offset = (y * image.width + x) * 4
      authority.data.copy(image.data, offset, offset, offset + 4)
    }
  }
  for (let y = 235; y < image.height; y += 1) for (let x = 0; x < image.width; x += 1) {
    if (x < 70 || x > 186) continue
    const offset = (y * image.width + x) * 4
    authority.data.copy(image.data, offset, offset, offset + 4)
  }
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
    if (!existing || !existing.equals(bytes)) throw new Error(`Stale or missing V3 file: ${path.relative(root, file)}`)
    return
  }
  fs.mkdirSync(path.dirname(file), { recursive: true })
  fs.writeFileSync(file, bytes)
}

function storeObject(bytes) {
  const hash = sha256(bytes)
  const file = objectFile(hash)
  if (check) {
    if (!fs.existsSync(file) || sha256(fs.readFileSync(file)) !== hash) throw new Error(`Missing V3 archive object: ${hash}`)
  } else {
    fs.mkdirSync(path.dirname(file), { recursive: true })
    if (fs.existsSync(file) && sha256(fs.readFileSync(file)) !== hash) throw new Error(`Archive collision: ${hash}`)
    if (!fs.existsSync(file)) fs.writeFileSync(file, bytes)
  }
  return { hash, file }
}

function saveStrip(sequence, records) {
  const images = records.map((record) => PNG.sync.read(record.bytes))
  const width = images.reduce((sum, image) => sum + image.width, 0)
  const strip = new PNG({ width, height: 320 })
  let x = 0
  for (const image of images) {
    PNG.bitblt(image, strip, 0, 0, image.width, image.height, x, 0)
    x += image.width
  }
  const bytes = PNG.sync.write(strip)
  const hash = sha256(bytes)
  const file = path.join(draftRoot, 'strips', `${sequence.id}-${hash.slice(0, 16)}.png`)
  writeOrCheck(file, bytes)
  return { path: path.relative(root, file).split(path.sep).join('/'), sha256: hash }
}

const rearAuthorityBytes = fs.readFileSync(objectFile(REAR_AUTHORITY_HASH))
const frontAuthorityFrame = v2.sequences.flatMap((sequence) => sequence.frames).find((frame) => frame.sha256 === [...FRONT_HASHES][0])
const backAuthorityFrame = v2.sequences.flatMap((sequence) => sequence.frames).find((frame) => frame.sha256 === BACK_HASH)
if (!frontAuthorityFrame || !backAuthorityFrame) throw new Error('V2 passive endpoints missing')
const correctedFrontBytes = registerJumperPalette(frameBytes(frontAuthorityFrame), rearAuthorityBytes)
const correctedBackBytes = registerJumperPalette(frameBytes(backAuthorityFrame), rearAuthorityBytes)
const correctedFrontHash = sha256(correctedFrontBytes)
const correctedBackHash = sha256(correctedBackBytes)

if (!check) {
  for (const directory of [assetRoot, path.join(draftRoot, 'frames'), path.join(draftRoot, 'strips')]) {
    fs.rmSync(directory, { recursive: true, force: true })
  }
}

const publishedByHash = new Map()
const modifiedSequences = new Set(['lift-enter-exit-v1', 'cook-counter-v1', 'brush-teeth-v1', 'wave-front-v1', 'front-seat-complete-route-v1', 'rear-work-turn-return-v1'])
const sequences = []
const correctionRecords = []

for (const sequence of v2.sequences) {
  const inputs = sequence.id === 'lift-enter-exit-v1'
    ? sequence.frames.filter((_, index) => index !== 1)
    : sequence.frames
  const records = []
  for (let index = 0; index < inputs.length; index += 1) {
    const frame = inputs[index]
    const oldPosition = sequence.frames.indexOf(frame) + 1
    let bytes = frameBytes(frame)
    let correction = null
    if (FRONT_HASHES.has(frame.sha256)) {
      bytes = correctedFrontBytes
      correction = 'jumper palette registered to exact bright rear turn colour authority; geometry and alpha preserved'
    } else if (frame.sha256 === BACK_HASH) {
      bytes = correctedBackBytes
      correction = 'jumper palette registered to exact bright rear turn colour authority; geometry and alpha preserved'
    } else if (sequence.id === 'rear-work-turn-return-v1' && oldPosition >= 11 && oldPosition <= 31) {
      bytes = repairRearWork(bytes, rearAuthorityBytes)
      correction = 'complete upper body recentered over the fixed root; exact-authority waist and legs replace the generated seam'
    }
    const image = PNG.sync.read(bytes)
    if (image.width !== frame.cell[0] || image.height !== frame.cell[1]) throw new Error(`${sequence.id} frame ${oldPosition}: geometry changed`)
    if (edgeAlpha(image)) throw new Error(`${sequence.id} frame ${oldPosition}: opaque cell edge`)
    const hash = sha256(bytes)
    let asset = publishedByHash.get(hash)
    if (!asset) {
      const fileName = `frame-${hash.slice(0, 16)}.png`
      const publicFile = path.join(assetRoot, fileName)
      writeOrCheck(publicFile, bytes)
      const stored = storeObject(bytes)
      const sourceFile = correction
        ? path.join(draftRoot, 'frames', fileName)
        : stored.file
      if (correction) writeOrCheck(sourceFile, bytes)
      asset = {
        source: path.relative(root, sourceFile).split(path.sep).join('/'),
        sourceSha256: hash,
        publicAssemblyPath: path.relative(root, publicFile).split(path.sep).join('/'),
        url: `/keeper-review/${set}/assets/${fileName}`,
      }
      publishedByHash.set(hash, asset)
    }
    if (correction) correctionRecords.push({ sequence: sequence.id, oldPosition, newPosition: index + 1, sourceSha256: frame.sha256, draftSha256: hash, correction })
    records.push({ frame, bytes, hash, asset, oldPosition, correction })
  }
  const changed = modifiedSequences.has(sequence.id)
  sequences.push({
    ...sequence,
    title: sequence.id === 'diary-turn-sit-write-return-v1' ? 'Turn, sit, hold, stand and return' : sequence.title,
    status: changed ? 'feedback-corrected-versioned-draft-v3' : sequence.status,
    source: changed ? { path: 'art/drafts/keeper-prime-morning-drafts-corrections-2026-10-22-v3/corrections.json', sha256: '' } : sequence.source,
    draftStrip: changed ? saveStrip(sequence, records) : sequence.draftStrip,
    frames: records.map(({ frame, hash, asset, oldPosition, correction }, index) => ({
      ...frame,
      id: `${sequence.id}-v3-f${String(index + 1).padStart(2, '0')}`,
      src: asset.url,
      sha256: hash,
      redraftSlot: `${sequence.id}/v3-frame-${String(index + 1).padStart(2, '0')}`,
      priorV2: { position: oldPosition, sha256: frame.sha256 },
      correction,
    })),
  })
}

const corrections = {
  schema: 'lighthouse-keeper/prime-animation-feedback-corrections@1',
  version: 3,
  generatedOn: '2026-10-22',
  sourceBatch: 'data/keeper_prime_animation_drafts_v2.json',
  sourceBatchSha256: sha256(fs.readFileSync(path.join(root, 'data/keeper_prime_animation_drafts_v2.json'))),
  authority: { rearColourAndBody: REAR_AUTHORITY_HASH },
  excluded: [{ sequence: 'lift-enter-exit-v1', v2Position: 2, sha256: v2.sequences.find((item) => item.id === 'lift-enter-exit-v1').frames[1].sha256, reason: 'Frank: frame is pointless' }],
  renamed: [{ sequence: 'diary-turn-sit-write-return-v1', from: 'Diary: turn, sit, write, stand and return', to: 'Turn, sit, hold, stand and return', reason: 'No writing motion is depicted.' }],
  frames: correctionRecords,
  imageGenerationStudy: { usedInDelivery: false, reason: 'Representative edit changed the Prime scale and rendering; deterministic authority-locked repair preserves exact identity.' },
}
let correctionBytes = Buffer.from(`${JSON.stringify(corrections, null, 2)}\n`)
const correctionHash = sha256(correctionBytes)
for (const sequence of sequences) if (modifiedSequences.has(sequence.id)) sequence.source.sha256 = correctionHash
writeOrCheck(path.join(draftRoot, 'corrections.json'), correctionBytes)

const reviewAuthorities = {
  front: { src: `/keeper-review/${set}/assets/frame-${correctedFrontHash.slice(0, 16)}.png`, sha256: correctedFrontHash, status: 'feedback-corrected-review-reference' },
  back: { src: `/keeper-review/${set}/assets/frame-${correctedBackHash.slice(0, 16)}.png`, sha256: correctedBackHash, status: 'feedback-corrected-review-reference' },
  sideRight: { src: '/sprites/keeper_prime_neutral_standing-side-right.png', sha256: v2.canonicalAuthorities.sideRight.sha256, status: 'approved-authority-unchanged' },
}
const frameCount = sequences.reduce((sum, sequence) => sum + sequence.frames.length, 0)
if (sequences.length !== 10 || frameCount !== 162) throw new Error(`Unexpected V3 inventory: ${sequences.length} sequences, ${frameCount} frames`)
const manifest = {
  ...v2,
  version: 3,
  generatedOn: '2026-10-22',
  status: 'feedback-corrected-review-only',
  note: 'V3 preserves V2, removes only the redundant lift frame, corrects every reused passive front/back jumper occurrence, renames the non-writing seated route, and repairs the rear-work waist seam in versioned draft copies. No V1/V2, approved authority, runtime or production file is overwritten.',
  reviewAuthorities,
  sequences,
}
const manifestBytes = Buffer.from(`${JSON.stringify(manifest, null, 2)}\n`)
writeOrCheck(path.join(root, 'data/keeper_prime_animation_drafts_v3.json'), manifestBytes)

const shellBytes = Buffer.from('<!doctype html><meta charset="utf-8"><title>Prime Keeper review V3</title><meta http-equiv="refresh" content="0;url=/prime-keeper-animation-drafts-v3"><a href="/prime-keeper-animation-drafts-v3">Open Prime Keeper review V3</a>\n')
writeOrCheck(path.join(reviewRoot, 'index.html'), shellBytes)
const register = {
  schema: 'lighthouse-keeper/reversible-review-batch@1',
  set,
  status: 'feedback-corrected-review-only',
  candidate: { publicShell: { file: `public/keeper-review/${set}/index.html`, sha256: sha256(shellBytes) } },
  publishedAssets: [...publishedByHash.values()].map(({ source, sourceSha256, publicAssemblyPath, url }) => ({ source, sourceSha256, publicAssemblyPath, url })),
}
writeOrCheck(path.join(draftRoot, 'batch-register.json'), Buffer.from(`${JSON.stringify(register, null, 2)}\n`))

console.log(`${check ? 'Verified' : 'Wrote'} Prime morning draft V3: ${sequences.length} sequences, ${frameCount} occurrences, ${publishedByHash.size} unique images, ${correctionRecords.length} corrected occurrences.`)
