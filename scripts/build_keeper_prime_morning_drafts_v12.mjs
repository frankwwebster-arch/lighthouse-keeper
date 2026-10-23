import crypto from 'node:crypto'
import fs from 'node:fs'
import path from 'node:path'
import { fileURLToPath } from 'node:url'
import { PNG } from 'pngjs'

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..')
const set = 'keeper-prime-morning-drafts-v12'
const reviewRoot = path.join(root, 'public/keeper-review', set)
const assetRoot = path.join(reviewRoot, 'assets')
const draftRoot = path.join(root, 'art/drafts/keeper-prime-morning-drafts-corrections-2026-10-23-v12')
const check = process.argv.includes('--check')
const sha256 = bytes => crypto.createHash('sha256').update(bytes).digest('hex')
const v11File = path.join(root, 'data/keeper_prime_animation_drafts_v11.json')
const v11Bytes = fs.readFileSync(v11File)
const v11 = JSON.parse(v11Bytes)
const v11Archive = JSON.parse(fs.readFileSync(path.join(root, 'review-archive/sets/keeper-prime-morning-drafts-v11.json')))
const COOK_DONOR_POSITIONS = [2, 3, 4, 5, 6, 7, 8]

const objectFile = hash => path.join(root, 'review-archive/objects', hash.slice(0, 2), `${hash}.png`)
const archivedBytes = (frame, label) => {
  const entry = v11Archive.entries[frame.src]
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
    if (!existing || !existing.equals(bytes)) throw new Error(`Stale or missing V12 file: ${path.relative(root, file)}`)
    return
  }
  fs.mkdirSync(path.dirname(file), { recursive: true })
  fs.writeFileSync(file, bytes)
}

function storeObject(bytes) {
  const hash = sha256(bytes)
  const file = objectFile(hash)
  if (check) {
    if (!fs.existsSync(file) || sha256(fs.readFileSync(file)) !== hash) throw new Error(`Missing V12 archive object: ${hash}`)
  } else {
    fs.mkdirSync(path.dirname(file), { recursive: true })
    if (!fs.existsSync(file)) fs.writeFileSync(file, bytes)
  }
  return file
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

const byId = new Map(v11.sequences.map(sequence => [sequence.id, sequence]))
const cooking = byId.get('cook-counter-v1')
if (!cooking || cooking.frames.length !== 8) throw new Error('Expected the eight-frame cooking authority sequence')
const donorFrames = COOK_DONOR_POSITIONS.map(position => cooking.frames[position - 1])
const donorBytes = donorFrames.map((frame, index) => archivedBytes(frame, `Cooking donor ${COOK_DONOR_POSITIONS[index]}`))
const publishedByHash = new Map()
const correctionRecords = []
const sequences = []

for (const sequence of v11.sequences) {
  const records = []
  for (let index = 0; index < sequence.frames.length; index += 1) {
    const frame = sequence.frames[index]
    const position = index + 1
    const replaced = sequence.id === 'rear-work-turn-return-v1' && position >= 11 && position <= 31
    const donorIndex = replaced ? (position - 11) % donorFrames.length : -1
    const donorFrame = replaced ? donorFrames[donorIndex] : null
    const bytes = replaced ? donorBytes[donorIndex] : archivedBytes(frame, 'V11')
    const image = PNG.sync.read(bytes)
    if (image.width !== frame.cell[0] || image.height !== frame.cell[1] || edgeAlpha(image)) throw new Error(`${sequence.id} frame ${position}: invalid isolated geometry`)
    const hash = sha256(bytes)
    if (replaced) writeOrCheck(path.join(draftRoot, 'frames', `frame-${hash.slice(0, 16)}.png`), bytes)
    let asset = publishedByHash.get(hash)
    if (!asset) {
      const fileName = `frame-${hash.slice(0, 16)}.png`
      const publicFile = path.join(assetRoot, fileName)
      writeOrCheck(publicFile, bytes)
      const stored = storeObject(bytes)
      asset = {
        source: path.relative(root, stored).split(path.sep).join('/'),
        sourceSha256: hash,
        publicAssemblyPath: path.relative(root, publicFile).split(path.sep).join('/'),
        url: `/keeper-review/${set}/assets/${fileName}`,
      }
      publishedByHash.set(hash, asset)
    }
    const correction = replaced
      ? 'V11 rejected: layered action arms carried their old inner sleeve and jumper edges into the approved torso. V12 borrows the complete, intact rear cooking pose byte-for-byte, so torso, stripe, sleeves, ribbed hem, trousers and boots remain one coherent drawing.'
      : frame.correction
    if (replaced) correctionRecords.push({
      sequence: sequence.id,
      position,
      rejectedV11Sha256: frame.sha256,
      cookingDonorPosition: COOK_DONOR_POSITIONS[donorIndex],
      cookingDonorSha256: donorFrame.sha256,
      draftV12Sha256: hash,
      correction,
    })
    records.push({ frame, bytes, hash, asset, correction, replaced, donorFrame })
  }
  const repairedSequence = sequence.id === 'rear-work-turn-return-v1'
  sequences.push({
    ...sequence,
    status: repairedSequence ? 'intact-cooking-whole-frame-choreography-review-v12' : sequence.status,
    source: repairedSequence ? { path: 'art/drafts/keeper-prime-morning-drafts-corrections-2026-10-23-v12/corrections.json', sha256: '' } : sequence.source,
    draftStrip: repairedSequence ? saveStrip(sequence, records) : sequence.draftStrip,
    frames: records.map(({ frame, hash, asset, correction, replaced, donorFrame }, index) => ({
      ...frame,
      id: `${sequence.id}-v12-f${String(index + 1).padStart(2, '0')}`,
      src: asset.url,
      sha256: hash,
      redraftSlot: `${sequence.id}/v12-frame-${String(index + 1).padStart(2, '0')}`,
      priorV11: { position: index + 1, sha256: frame.sha256 },
      ...(replaced ? {
        cookingDonor: { position: COOK_DONOR_POSITIONS[(index + 1 - 11) % donorFrames.length], sha256: donorFrame.sha256 },
        amendmentComparison: { label: 'Rejected V11 layered jumper', src: frame.src, sha256: frame.sha256 },
      } : {}),
      correction,
    })),
  })
}

const corrections = {
  schema: 'lighthouse-keeper/prime-animation-feedback-corrections@1',
  version: 12,
  generatedOn: '2026-10-23',
  sourceBatch: 'data/keeper_prime_animation_drafts_v11.json',
  sourceBatchSha256: sha256(v11Bytes),
  wholeFrameAuthority: {
    sequence: 'cook-counter-v1',
    positions: COOK_DONOR_POSITIONS,
    source: cooking.source,
  },
  rejectedAmendment: {
    version: 11,
    scope: 'rear-work-turn-return-v1 positions 11–31 only',
    reason: 'The transferred arm layers retained inner sleeve and jumper boundaries that visibly broke the torso and cream stripe at both sides.',
  },
  frames: correctionRecords,
  imageGeneration: { usedInDelivery: false, reason: 'V12 reuses the seven complete, intact cooking frames byte-for-byte and changes only their order inside the rear-task work section.' },
}
const correctionBytes = Buffer.from(`${JSON.stringify(corrections, null, 2)}\n`)
const correctionHash = sha256(correctionBytes)
sequences.find(sequence => sequence.id === 'rear-work-turn-return-v1').source.sha256 = correctionHash
writeOrCheck(path.join(draftRoot, 'corrections.json'), correctionBytes)

const reviewAuthorities = Object.fromEntries(Object.entries(v11.reviewAuthorities).map(([name, item]) => [name, { ...item, src: `/keeper-review/${set}/assets/frame-${item.sha256.slice(0, 16)}.png` }]))
const frameCount = sequences.reduce((sum, sequence) => sum + sequence.frames.length, 0)
const manifest = {
  ...v11,
  version: 12,
  generatedOn: '2026-10-23',
  status: 'intact-cooking-whole-frame-choreography-review',
  note: 'V12 preserves V1–V11 and replaces only rear-task positions 11–31. Instead of layering arms onto a separate torso, it reuses complete, intact frames 2–8 from the existing cooking sequence for three seven-frame work cycles. This removes the broken inner sleeve, cream-stripe and jumper edges by keeping every work pose as one coherent drawing. The optional alignment ghost is off by default. No canonical, runtime or production file is overwritten.',
  reviewAuthorities,
  sequences,
}
writeOrCheck(path.join(root, 'data/keeper_prime_animation_drafts_v12.json'), Buffer.from(`${JSON.stringify(manifest, null, 2)}\n`))
const shellBytes = Buffer.from('<!doctype html><meta charset="utf-8"><title>Prime Keeper review V12</title><meta http-equiv="refresh" content="0;url=/prime-keeper-animation-drafts-v12"><a href="/prime-keeper-animation-drafts-v12">Open Prime Keeper review V12</a>\n')
writeOrCheck(path.join(reviewRoot, 'index.html'), shellBytes)
const register = {
  schema: 'lighthouse-keeper/reversible-review-batch@1',
  set,
  status: 'intact-cooking-whole-frame-choreography-review',
  candidate: { publicShell: { file: `public/keeper-review/${set}/index.html`, sha256: sha256(shellBytes) } },
  publishedAssets: [...publishedByHash.values()].map(({ source, sourceSha256, publicAssemblyPath, url }) => ({ source, sourceSha256, publicAssemblyPath, url })),
}
writeOrCheck(path.join(draftRoot, 'batch-register.json'), Buffer.from(`${JSON.stringify(register, null, 2)}\n`))
console.log(`${check ? 'Verified' : 'Wrote'} Prime morning draft V12: ${sequences.length} sequences, ${frameCount} occurrences, ${publishedByHash.size} unique images, ${correctionRecords.length} whole-frame cooking transfers.`)
