import crypto from 'node:crypto'
import fs from 'node:fs'
import path from 'node:path'
import { fileURLToPath } from 'node:url'
import { PNG } from 'pngjs'

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..')
const reviewSet = 'keeper-prime-morning-drafts-v2'
const reviewRoot = path.join(root, 'public/keeper-review', reviewSet)
const assetRoot = path.join(reviewRoot, 'assets')
const check = process.argv.includes('--check')
const sha256 = (bytes) => crypto.createHash('sha256').update(bytes).digest('hex')
const readJson = (file) => JSON.parse(fs.readFileSync(path.join(root, file), 'utf8'))

const v1 = readJson('data/keeper_prime_animation_drafts_v1.json')
const catalogue = readJson('public/prime-keeper-animations/catalogue.json')
const clipMap = new Map(catalogue.clips.map((clip) => [clip.id, clip]))

function reviewUrlBytes(url) {
  const publicFile = path.join(root, 'public', url.replace(/^\//, ''))
  if (fs.existsSync(publicFile)) return fs.readFileSync(publicFile)
  const match = url.match(/^\/keeper-review\/([^/]+)\//)
  if (!match) throw new Error(`Cannot resolve non-review URL: ${url}`)
  const setManifestFile = path.join(root, 'review-archive/sets', `${match[1]}.json`)
  const setManifest = JSON.parse(fs.readFileSync(setManifestFile, 'utf8'))
  const entry = setManifest.entries?.[url]
  if (!entry) throw new Error(`Archive entry missing: ${url}`)
  return fs.readFileSync(path.join(root, entry.object))
}

function sourceBytes(source) {
  if (source.url) return reviewUrlBytes(source.url)
  if (source.path) return fs.readFileSync(path.join(root, source.path))
  throw new Error('Frame source needs path or URL')
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

function archivedCurrentBytes(file) {
  if (!file.startsWith(reviewRoot)) return null
  const setManifestFile = path.join(root, 'review-archive/sets', `${reviewSet}.json`)
  if (!fs.existsSync(setManifestFile)) return null
  const setManifest = JSON.parse(fs.readFileSync(setManifestFile, 'utf8'))
  const url = `/keeper-review/${reviewSet}/${path.relative(reviewRoot, file).split(path.sep).join('/')}`
  const entry = setManifest.entries?.[url]
  return entry ? fs.readFileSync(path.join(root, entry.object)) : null
}

function writeOrCheck(file, bytes) {
  if (check) {
    const existing = fs.existsSync(file) ? fs.readFileSync(file) : archivedCurrentBytes(file)
    if (!existing || !existing.equals(bytes)) throw new Error(`Stale or missing V2 file: ${path.relative(root, file)}`)
    return
  }
  fs.mkdirSync(path.dirname(file), { recursive: true })
  fs.writeFileSync(file, bytes)
}

function clipFrames(id) {
  const clip = clipMap.get(id)
  if (!clip) throw new Error(`Approved clip missing: ${id}`)
  return clip.frames.map((frame, index) => ({
    url: frame.src,
    durationMs: frame.durationMs,
    label: frame.label,
    phase: frame.phase ?? clip.title,
    sourceClip: id,
    sourceIndex: index,
  }))
}

function occurrence(frame, label, phase, durationMs = frame.durationMs) {
  return { ...frame, label, phase, durationMs }
}

const sideSit = clipFrames('sit-side-right-v6')
const frontSit = clipFrames('sit-front-v4')
const backSit = clipFrames('sit-back-v2')
const frontTurn = clipFrames('turn-front-side-v1')
const backTurn = clipFrames('turn-side-back-v10')
const rearAction = clipFrames('rear-action-v1').slice(-24)

const sweepRoot = 'art/drafts/keeper-prime-sweep-broom-2026-10-18-v2/drafts/frames'
const sweep = (name) => ({ path: `${sweepRoot}/keeper_prime_sweep-broom-${name}.png`, durationMs: 125, sourceClip: 'keeper-prime-sweep-broom-v2' })
const sweepNeutral = sweep('neutral-exact')
const sweepAcquire = sweep('acquire')
const sweep1 = sweep('phase1')
const sweep2 = sweep('phase2')
const sweep3 = sweep('phase3')
const sweep4 = sweep('phase4')

const definitions = [
  {
    id: 'sweep-broom-isolated-v2',
    title: 'Collect broom, sweep and recover',
    status: 'unapproved-isolated-action-candidate',
    draftRoot: 'art/drafts/keeper-prime-sweep-broom-choreography-2026-10-22-v3',
    sourceAuthority: 'art/drafts/keeper-prime-sweep-broom-2026-10-18-v2/keeper-prime-sweep-broom-v2.json',
    fps: 8,
    startPose: 'standing-side-right-with-staged-broom',
    endPose: 'standing-side-right-with-staged-broom',
    frames: [
      occurrence(sweepNeutral, 'Prime endpoint; broom staged', 'endpoint'),
      occurrence(sweepAcquire, 'take two-hand grip', 'acquire'),
      occurrence(sweep1, 'outward sweep 1', 'sweep'),
      occurrence(sweep2, 'outward sweep 2', 'sweep'),
      occurrence(sweep3, 'outward sweep 3', 'sweep'),
      occurrence(sweep4, 'furthest planted sweep', 'sweep'),
      occurrence(sweep3, 'return sweep 1', 'recover'),
      occurrence(sweep2, 'return sweep 2', 'recover'),
      occurrence(sweep1, 'return sweep 3', 'recover'),
      occurrence(sweepAcquire, 'release two-hand grip', 'release'),
      occurrence(sweepNeutral, 'Prime endpoint; broom staged', 'endpoint'),
    ],
  },
  {
    id: 'side-leisure-sit-hold-stand-v1',
    title: 'Side leisure: sit, hold and stand',
    status: 'approved-components-choreography-review',
    draftRoot: 'art/drafts/keeper-prime-side-leisure-choreography-2026-10-22-v1',
    sourceAuthority: 'public/prime-keeper-animations/catalogue.json',
    fps: 8,
    startPose: 'standing-side-right',
    endPose: 'standing-side-right',
    frames: [
      ...sideSit.slice(0, 6).map((frame, index) => occurrence(frame, `sit ${index + 1}`, 'sit')),
      ...Array.from({ length: 4 }, (_, index) => occurrence(sideSit[5], `seated hold ${index + 1}`, 'hold', 250)),
      ...sideSit.slice(6).map((frame, index) => occurrence(frame, `stand ${index + 1}`, 'stand')),
    ],
  },
  {
    id: 'diary-turn-sit-write-return-v1',
    title: 'Diary: turn, sit, write, stand and return',
    status: 'approved-components-choreography-review',
    draftRoot: 'art/drafts/keeper-prime-diary-choreography-2026-10-22-v1',
    sourceAuthority: 'public/prime-keeper-animations/catalogue.json',
    fps: 8,
    startPose: 'standing-side-right',
    endPose: 'standing-side-right',
    frames: [
      ...backTurn.map((frame, index) => occurrence(frame, `turn to desk ${index + 1}`, 'turn to back')),
      ...backSit.slice(1, 6).map((frame, index) => occurrence(frame, `sit back ${index + 1}`, 'sit')),
      ...Array.from({ length: 4 }, (_, index) => occurrence(backSit[5], `seated diary hold ${index + 1}`, 'hold', 250)),
      ...backSit.slice(6).map((frame, index) => occurrence(frame, `stand back ${index + 1}`, 'stand')),
      ...backTurn.slice(0, 8).reverse().map((frame, index) => occurrence(frame, `return to room ${index + 1}`, 'turn to side')),
    ],
  },
  {
    id: 'front-seat-complete-route-v1',
    title: 'Front seat consumer route',
    status: 'approved-components-choreography-review',
    draftRoot: 'art/drafts/keeper-prime-front-seat-choreography-2026-10-22-v1',
    sourceAuthority: 'public/prime-keeper-animations/catalogue.json',
    fps: 8,
    startPose: 'standing-side-right',
    endPose: 'standing-side-right',
    frames: [
      ...frontTurn.slice().reverse().map((frame, index) => occurrence(frame, `turn to front ${index + 1}`, 'turn to front')),
      ...frontSit.slice(1, 6).map((frame, index) => occurrence(frame, `sit front ${index + 1}`, 'sit')),
      ...Array.from({ length: 4 }, (_, index) => occurrence(frontSit[5], `front seated hold ${index + 1}`, 'hold', 250)),
      ...frontSit.slice(6).map((frame, index) => occurrence(frame, `stand front ${index + 1}`, 'stand')),
      ...frontTurn.slice(1).map((frame, index) => occurrence(frame, `turn to side ${index + 1}`, 'turn to side')),
    ],
  },
  {
    id: 'rear-work-turn-return-v1',
    title: 'Rear task: turn, work and return',
    status: 'approved-components-choreography-review',
    draftRoot: 'art/drafts/keeper-prime-rear-work-return-2026-10-22-v1',
    sourceAuthority: 'public/prime-keeper-animations/catalogue.json',
    fps: 8,
    startPose: 'standing-side-right',
    endPose: 'standing-side-right',
    frames: [
      ...backTurn.map((frame, index) => occurrence(frame, `turn to task ${index + 1}`, 'turn to back')),
      ...rearAction.map((frame, index) => occurrence(frame, `rear work ${index + 1}`, 'work')),
      ...backTurn.slice(0, 8).reverse().map((frame, index) => occurrence(frame, `return to side ${index + 1}`, 'turn to side')),
    ],
  },
]

if (!check && fs.existsSync(assetRoot)) {
  for (const file of fs.readdirSync(assetRoot)) if (file.endsWith('.png')) fs.unlinkSync(path.join(assetRoot, file))
}

const sequences = []
for (const sequence of v1.sequences) {
  const frames = sequence.frames.map((frame) => {
    const bytes = reviewUrlBytes(frame.src)
    if (sha256(bytes) !== frame.sha256) throw new Error(`V1 frame hash changed: ${frame.id}`)
    const fileName = path.basename(frame.src)
    writeOrCheck(path.join(assetRoot, fileName), bytes)
    return { ...frame, src: `/keeper-review/${reviewSet}/assets/${fileName}` }
  })
  sequences.push({ ...sequence, status: 'unapproved-versioned-draft-carried-from-v1', frames })
}

for (const definition of definitions) {
  const authorityBytes = fs.readFileSync(path.join(root, definition.sourceAuthority))
  const frameRecords = definition.frames.map((input, index) => {
    const bytes = sourceBytes(input)
    const image = PNG.sync.read(bytes)
    if (image.height !== 320) throw new Error(`${definition.id} frame ${index + 1}: expected 320px authoring height, got ${image.height}`)
    if (edgeAlpha(image)) throw new Error(`${definition.id} frame ${index + 1}: opaque cell edge`)
    const hash = sha256(bytes)
    const fileName = `${definition.id}-frame-${String(index + 1).padStart(2, '0')}-${hash.slice(0, 16)}.png`
    return { input, bytes, image, hash, fileName }
  })
  const sourceManifest = {
    schema: 'lighthouse-keeper/prime-choreography-composition@1',
    id: definition.id,
    status: definition.status,
    sourceAuthority: definition.sourceAuthority,
    sourceAuthoritySha256: sha256(authorityBytes),
    rule: 'Every occurrence copies a hash-pinned isolated source frame byte-for-byte. No approved source pixel is rewritten.',
    frames: frameRecords.map(({ input, hash }, index) => ({ occurrence: index + 1, label: input.label, phase: input.phase, source: input.url ?? input.path, sourceSha256: hash })),
  }
  const sourceManifestBytes = Buffer.from(`${JSON.stringify(sourceManifest, null, 2)}\n`)
  const sourceManifestPath = `${definition.draftRoot}/composition.json`
  writeOrCheck(path.join(root, sourceManifestPath), sourceManifestBytes)

  if (!check) {
    const framesRoot = path.join(root, definition.draftRoot, 'frames')
    if (fs.existsSync(framesRoot)) for (const file of fs.readdirSync(framesRoot)) if (file.endsWith('.png')) fs.unlinkSync(path.join(framesRoot, file))
    for (const file of fs.readdirSync(path.join(root, definition.draftRoot))) if (file.startsWith(`${definition.id}-`) && file.endsWith('.png')) fs.unlinkSync(path.join(root, definition.draftRoot, file))
  }

  const frames = []
  const stripWidth = frameRecords.reduce((sum, frame) => sum + frame.image.width, 0)
  const strip = new PNG({ width: stripWidth, height: 320 })
  let stripX = 0
  for (let index = 0; index < frameRecords.length; index += 1) {
    const record = frameRecords[index]
    writeOrCheck(path.join(root, definition.draftRoot, 'frames', record.fileName), record.bytes)
    writeOrCheck(path.join(assetRoot, record.fileName), record.bytes)
    PNG.bitblt(record.image, strip, 0, 0, record.image.width, 320, stripX, 0)
    stripX += record.image.width
    frames.push({
      id: `${definition.id}-f${String(index + 1).padStart(2, '0')}`,
      label: record.input.label,
      phase: record.input.phase,
      src: `/keeper-review/${reviewSet}/assets/${record.fileName}`,
      sha256: record.hash,
      durationMs: record.input.durationMs,
      cell: [record.image.width, 320],
      anchor: [128, 320],
      redraftSlot: `${definition.id}/frame-${String(index + 1).padStart(2, '0')}`,
      authorityOverride: null,
      sourceClip: record.input.sourceClip,
    })
  }
  const stripBytes = PNG.sync.write(strip)
  const stripHash = sha256(stripBytes)
  const stripPath = `${definition.draftRoot}/${definition.id}-${stripHash.slice(0, 16)}.png`
  writeOrCheck(path.join(root, stripPath), stripBytes)
  sequences.push({
    id: definition.id,
    title: definition.title,
    status: definition.status,
    source: { path: sourceManifestPath, sha256: sha256(sourceManifestBytes) },
    draftStrip: { path: stripPath, sha256: stripHash },
    fps: definition.fps,
    startPose: definition.startPose,
    endPose: definition.endPose,
    frames,
  })
}

const quarantinedSources = v1.quarantinedSources.map((item) => item.id === 'sweep-broom-v1'
  ? { ...item, reason: `${item.reason} It is retained as rejected history; the independently isolated Prime Sweep V2 candidate is now included in this page.` }
  : item)

const frameCount = sequences.reduce((sum, item) => sum + item.frames.length, 0)
const redraftSlots = sequences.flatMap((sequence) => sequence.frames.map((frame) => frame.redraftSlot))
if (sequences.length !== 10 || frameCount !== 163) {
  throw new Error(`Unexpected V2 inventory: ${sequences.length} sequences, ${frameCount} frame occurrences`)
}
if (new Set(redraftSlots).size !== redraftSlots.length) throw new Error('Duplicate V2 redraft slot')

const manifest = {
  ...v1,
  version: 2,
  generatedOn: '2026-10-22',
  status: 'mixed-review-unapproved-sequences-and-approved-source-compositions',
  note: 'V2 preserves every V1 frame, adds one isolated unapproved sweep candidate, and adds four choreography previews made only from byte-exact approved component frames. No canonical or approved source is modified. Every displayed occurrence has a stable feedback slot.',
  expandedCells: { sweepBroom: [384, 320], reason: 'The separately owned broom requires a prop-safe horizontal gutter outside the 256×320 Prime body cell.' },
  quarantinedSources,
  sequences,
}
const manifestBytes = Buffer.from(`${JSON.stringify(manifest, null, 2)}\n`)
writeOrCheck(path.join(reviewRoot, 'batch.json'), manifestBytes)
writeOrCheck(path.join(root, 'data/keeper_prime_animation_drafts_v2.json'), manifestBytes)

console.log(`${check ? 'Verified' : 'Wrote'} Prime morning draft V2: ${sequences.length} sequences, ${frameCount} frame occurrences.`)
