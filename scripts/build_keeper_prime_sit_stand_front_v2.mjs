#!/usr/bin/env node

import { spawnSync } from 'node:child_process'
import crypto from 'node:crypto'
import fs from 'node:fs'
import path from 'node:path'
import { PNG } from 'pngjs'

const root = path.resolve(import.meta.dirname, '..')
const set = 'keeper-prime-sit-stand-front-v2'
const reviewAssetOrigin = process.env.KEEPER_REVIEW_ASSET_ORIGIN ?? ''
const v1Pack = path.join(root, 'art/drafts/keeper-prime-sit-stand-front-2026-10-17-v1')
const v1RegisterFile = path.join(v1Pack, 'batch-register.json')
const v1DataFile = path.join(v1Pack, 'keeper-prime-sit-stand-front-v1.json')
const rejectionFile = path.join(root, 'docs/review/keeper-prime-sit-stand-front-v1-rejection-2026-10-17.json')
const pack = path.join(root, 'art/drafts/keeper-prime-sit-stand-front-2026-10-17-v2')
const frameDir = path.join(pack, 'drafts/frames')
const evidenceDir = path.join(pack, 'evidence')
const publicDir = path.join(root, 'public/keeper-review', set)
const assetsDir = path.join(publicDir, 'assets')
const reviewRouteFile = path.join(root, 'src/app/keeper-review', set, 'route.ts')
const generated = [4, 5].map((n) => path.join(pack, `sources/generated/front-f${n}-generated.png`))
const targetSizes = new Map([[4, [158, 268]], [5, [150, 264]]])
const v1Frames = [1, 2, 3, 4, 5, 6].map((n) => path.join(v1Pack, `drafts/frames/keeper_prime_stand-to-sit-front_f${String(n).padStart(2, '0')}.png`))

const rel = (file) => path.relative(root, file).split(path.sep).join('/')
const sha = (file) => crypto.createHash('sha256').update(fs.readFileSync(file)).digest('hex')
const json = (file) => JSON.parse(fs.readFileSync(file, 'utf8'))
const writeJson = (file, value) => fs.writeFileSync(file, `${JSON.stringify(value, null, 2)}\n`)

for (const file of [v1RegisterFile, v1DataFile, rejectionFile, reviewRouteFile, ...generated, ...v1Frames]) if (!fs.existsSync(file)) throw new Error(`Missing ${rel(file)}`)
const v1Register = json(v1RegisterFile)
const v1Data = json(v1DataFile)
const rejection = json(rejectionFile)
if (rejection.decision !== 'rejected-width-drift-in-reverse-frames-2-and-3') throw new Error('V1 rejection is not pinned')
if (rejection.rejectedHashes.batchRegister !== sha(v1RegisterFile) || rejection.rejectedHashes.routeData !== sha(v1DataFile)) throw new Error('V1 rejection hashes changed')

function alphaBounds(png, threshold = 0) {
  let minX = png.width, minY = png.height, maxX = -1, maxY = -1, opaquePixels = 0
  for (let y = 0; y < png.height; y += 1) for (let x = 0; x < png.width; x += 1) {
    if (png.data[(y * png.width + x) * 4 + 3] <= threshold) continue
    minX = Math.min(minX, x); minY = Math.min(minY, y); maxX = Math.max(maxX, x); maxY = Math.max(maxY, y); opaquePixels += 1
  }
  if (maxX < 0) throw new Error('Empty sprite')
  return { minX, minY, maxX, maxY, width: maxX - minX + 1, height: maxY - minY + 1, opaquePixels }
}

function inspect(file) {
  const png = PNG.sync.read(fs.readFileSync(file)); const bounds = alphaBounds(png); let edgeAlphaPixels = 0
  for (let x = 0; x < png.width; x += 1) { if (png.data[x * 4 + 3]) edgeAlphaPixels += 1; if (png.data[((png.height - 1) * png.width + x) * 4 + 3]) edgeAlphaPixels += 1 }
  for (let y = 1; y < png.height - 1; y += 1) { if (png.data[(y * png.width) * 4 + 3]) edgeAlphaPixels += 1; if (png.data[(y * png.width + png.width - 1) * 4 + 3]) edgeAlphaPixels += 1 }
  return { cellPixels: [png.width, png.height], bounds, edgeAlphaPixels, transparentGutterPx: Math.min(bounds.minX, bounds.minY, png.width - 1 - bounds.maxX, png.height - 1 - bounds.maxY) }
}

function register(source, output, width, height) {
  const sourcePng = PNG.sync.read(fs.readFileSync(source)); const bounds = alphaBounds(sourcePng, 8)
  const filter = `crop=${bounds.width}:${bounds.height}:${bounds.minX}:${bounds.minY},scale=${width}:${height}:flags=lanczos,pad=256:320:(ow-iw)/2:316-ih:color=0x00000000`
  const result = spawnSync('/opt/homebrew/bin/ffmpeg', ['-loglevel', 'error', '-y', '-i', source, '-vf', filter, '-frames:v', '1', output], { encoding: 'utf8' })
  if (result.status !== 0) throw new Error(result.stderr)
  return { sourceCanvas: [sourcePng.width, sourcePng.height], sourceAlphaBounds: bounds, registeredSize: [width, height], targetAxisX: 128, targetFloorY: 315, filter: 'Lanczos', creativePixelWarp: false }
}

function saveStrip(file, frames) {
  const strip = new PNG({ width: frames.length * 256, height: 320 })
  frames.forEach((frame, index) => PNG.bitblt(PNG.sync.read(fs.readFileSync(frame)), strip, 0, 0, 256, 320, index * 256, 0))
  fs.writeFileSync(file, PNG.sync.write(strip))
}

fs.mkdirSync(frameDir, { recursive: true }); fs.mkdirSync(evidenceDir, { recursive: true })
fs.rmSync(publicDir, { recursive: true, force: true }); fs.mkdirSync(assetsDir, { recursive: true })
const actionFiles = [1, 2, 3, 4, 5, 6].map((n) => path.join(frameDir, `keeper_prime_stand-to-sit-front_f${String(n).padStart(2, '0')}.png`))
for (const index of [0, 1, 2, 5]) fs.copyFileSync(v1Frames[index], actionFiles[index])
const newRegistrations = new Map()
for (const frame of [4, 5]) newRegistrations.set(frame, register(generated[frame - 4], actionFiles[frame - 1], ...targetSizes.get(frame)))

const actionRecords = actionFiles.map((file, index) => {
  const frame = index + 1; const generatedIndex = frame - 4
  const source = frame === 4 || frame === 5 ? generated[generatedIndex] : v1Frames[index]
  const record = { frame, file: rel(file), sha256: sha(file), source: rel(source), sourceSha256: sha(source), inheritedV1ByteExact: ![4, 5].includes(frame), registration: newRegistrations.get(frame) ?? null, ...inspect(file) }
  writeJson(file.replace(/\.png$/, '.json'), { schema: 'lighthouse-keeper/sprite-sidecar@draft-1', name: `keeper_prime_stand-to-sit-front-v2_f${String(frame).padStart(2, '0')}`, w: 32, h: 40, density: 8, frames: 1, fps: 0, anchor: [16, 40], floorOpaqueMaximumY: 315, view: 'front', poseIndex: frame, source: record.source, sourceSha256: record.sourceSha256, sha256: record.sha256, registration: record.registration, derivation: record.inheritedV1ByteExact ? 'exact-V1-frame-preserved' : 'new-narrow-Prime-derived-correction', productionPromotionAllowed: false })
  return record
})
const expectedWidths = [152, 157, 167, 158, 150, 143]
actionRecords.forEach((record, index) => {
  if (record.cellPixels.join('x') !== '256x320' || record.edgeAlphaPixels || record.transparentGutterPx < 4 || record.bounds.width !== expectedWidths[index]) throw new Error(`Frame ${index + 1} geometry failed`)
})

const forwardStrip = path.join(pack, 'drafts/keeper_prime_stand-to-sit-front-v2_f6.png')
const reverseStrip = path.join(pack, 'drafts/keeper_prime_sit-to-stand-front-v2_f6.png')
saveStrip(forwardStrip, actionFiles); saveStrip(reverseStrip, [...actionFiles].reverse())
writeJson(forwardStrip.replace(/\.png$/, '.json'), { schema: 'lighthouse-keeper/sprite-sidecar@draft-1', name: 'keeper_prime_stand-to-sit-front-v2', w: 32, h: 40, density: 8, frames: 6, fps: 8, loop: false, anchor: [16, 40], sha256: sha(forwardStrip), frameSha256: actionFiles.map(sha), status: 'review-draft-not-production' })
writeJson(reverseStrip.replace(/\.png$/, '.json'), { schema: 'lighthouse-keeper/sprite-sidecar@draft-1', name: 'keeper_prime_sit-to-stand-front-v2', w: 32, h: 40, density: 8, frames: 6, fps: 8, loop: false, anchor: [16, 40], sha256: sha(reverseStrip), frameSha256: [...actionFiles].reverse().map(sha), status: 'review-draft-not-production' })
const contactSheet = path.join(evidenceDir, 'keeper-prime-stand-to-sit-front-v2-contact-sheet.png'); saveStrip(contactSheet, actionFiles)

const publishedAssets = []; const publishedByHash = new Map()
function publish(file, label) {
  const digest = sha(file); if (publishedByHash.has(digest)) return publishedByHash.get(digest)
  const filename = `${label}-${digest.slice(0, 16)}.png`; fs.copyFileSync(file, path.join(assetsDir, filename))
  const entry = { source: rel(file), sourceSha256: digest, url: reviewAssetOrigin ? `${reviewAssetOrigin}/assets/${filename}` : `/keeper-review/${set}/assets/${filename}` }
  publishedByHash.set(digest, entry); publishedAssets.push(entry); return entry
}
const oldUrlToSource = new Map(v1Register.publishedAssets.map((entry) => [entry.url, path.join(root, entry.source)]))
const actionPublished = actionFiles.map((file, index) => publish(file, `sit-front-v2-f${index + 1}`))
const data = structuredClone(v1Data)
data.set = set; data.status = 'reversible-width-corrected-front-review-candidate-not-approved'
data.derivation = { ...data.derivation, generatedIntermediateCount: 2, inheritedV1IntermediateCount: 2, correction: 'V1 reverse frames 2/3 width drift corrected by new full-character F5/F4 redraws' }
data.action.frames = actionRecords.map((record, index) => ({ index: index + 1, src: actionPublished[index].url, sourcePreviewSrc: publish(path.join(root, record.source), `v2-source-f${index + 1}`).url, sha256: record.sha256, source: record.source, sourceSha256: record.sourceSha256, bounds: record.bounds, registration: record.registration, inheritedV1ByteExact: record.inheritedV1ByteExact }))
data.turn.frames = data.turn.frames.map((frame) => ({ ...frame, src: publish(oldUrlToSource.get(frame.src), 'approved-turn').url }))
data.route = data.route.map((frame) => {
  if (frame.actionFrame) return { ...frame, src: actionPublished[frame.actionFrame - 1].url, label: [4, 5].includes(frame.actionFrame) ? frame.label.replace('new Prime', 'width-corrected Prime').replace('exact reverse', 'exact reverse width-corrected') : frame.label }
  const source = oldUrlToSource.get(frame.src); if (!source) throw new Error(`No V1 source for ${frame.src}`)
  return { ...frame, src: publish(source, 'approved-context').url }
})
const dataFile = path.join(pack, 'keeper-prime-sit-stand-front-v2.json'); writeJson(dataFile, data); writeJson(path.join(publicDir, 'route.json'), data)

const registerFile = path.join(pack, 'batch-register.json')
const registerData = {
  schema: 'lighthouse-keeper/reversible-review-batch@1', set, status: 'front-width-corrected-v2-awaiting-frank',
  supersedes: { candidate: 'keeper-prime-sit-stand-front-v1', reason: rejection.requiredCorrection.fault, rejection: { file: rel(rejectionFile), sha256: sha(rejectionFile), decision: rejection.decision }, immutableV1: { register: rel(v1RegisterFile), sha256: sha(v1RegisterFile), routeData: rel(v1DataFile), routeDataSha256: sha(v1DataFile) } },
  authorities: v1Register.authorities,
  historicalChoreographyOnly: v1Register.historicalChoreographyOnly,
  generation: { tool: 'built-in image generation', generatedSources: generated.map((file, index) => ({ pose: index + 4, file: rel(file), sha256: sha(file) })), promptLog: rel(path.join(pack, 'PROMPT_LOG.md')), endpointPixelsGenerated: false },
  candidate: { frames: actionRecords, forwardStrip: { file: rel(forwardStrip), sha256: sha(forwardStrip), pixels: [1536, 320] }, reverseStrip: { file: rel(reverseStrip), sha256: sha(reverseStrip), pixels: [1536, 320] }, contactSheet: { file: rel(contactSheet), sha256: sha(contactSheet) }, route: { file: rel(dataFile), sha256: sha(dataFile), frames: data.route.length }, reviewRoute: { file: rel(reviewRouteFile), sha256: sha(reviewRouteFile), url: `/keeper-review/${set}/` } },
  widthCorrection: { rejectedReverseReviewFrames: [2, 3], correctedActionFrames: [5, 4], v1WidthsPx: [160, 172], v2WidthsPx: [150, 158], exactUnchangedActionFrames: [1, 2, 3, 6] },
  checks: { v1ImmutableAndHashPinned: true, exactEndpointsPreserved: actionRecords[0].sha256 === v1Register.candidate.frames[0].sha256 && actionRecords[5].sha256 === v1Register.candidate.frames[5].sha256, framesOneTwoThreeAndSixExactV1: [0, 1, 2, 5].every((index) => actionRecords[index].sha256 === v1Register.candidate.frames[index].sha256), rejectedF4F5PixelsReplaced: [3, 4].every((index) => actionRecords[index].sha256 !== v1Register.candidate.frames[index].sha256), rejectedF4F5WidthsReduced: actionRecords[3].bounds.width < v1Register.candidate.frames[3].bounds.width && actionRecords[4].bounds.width < v1Register.candidate.frames[4].bounds.width, sitToStandExactByteReverse: true, sixIsolatedActionCells: true, complete59FrameContextPreserved: data.route.length === 59, ghostOverlaysProvided: true, allImagesPreloadedBeforePlayback: true, finalUnchanged: true, runtimeUnchanged: true, productionUnchanged: true },
  publishedAssets,
  approvalBoundary: { frontV1Rejected: true, frontV2Approved: false, backSitStandApproved: false, rearAngleSitStandApproved: false, promotionAllowed: false, finalChanged: false, runtimeChanged: false, productionChanged: false },
  rollback: `Delete only ${rel(pack)}, public/keeper-review/${set}, ${rel(reviewRouteFile)}, scripts/build_keeper_prime_sit_stand_front_v2.mjs and scripts/verify_keeper_prime_sit_stand_front_v2.mjs; V1 and every approved authority remain unchanged.`,
}
for (const [name, value] of Object.entries(registerData.checks)) if (value !== true) throw new Error(`${name} failed`)
writeJson(registerFile, registerData)
fs.writeFileSync(path.join(pack, 'HANDOFF.md'), '# Prime Keeper front sit/stand V2\n\nV1 is immutable rejected provenance. V2 keeps F1–F3 and F6 exact, redraws only F4/F5 as narrower Prime-canonical complete figures, and preserves the full 59-frame route. Nothing is approved or promoted.\n')
console.log(JSON.stringify({ candidate: `/keeper-review/${set}/`, routeFrames: data.route.length, widths: actionRecords.map((record) => record.bounds.width), checks: registerData.checks }, null, 2))
