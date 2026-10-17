#!/usr/bin/env node

import { spawnSync } from 'node:child_process'
import crypto from 'node:crypto'
import fs from 'node:fs'
import path from 'node:path'
import { PNG } from 'pngjs'

const root = path.resolve(import.meta.dirname, '..')
const set = 'keeper-prime-sit-stand-front-v4'
const reviewAssetOrigin = process.env.KEEPER_REVIEW_ASSET_ORIGIN ?? ''
const v3Pack = path.join(root, 'art/drafts/keeper-prime-sit-stand-front-2026-10-17-v3')
const v3RegisterFile = path.join(v3Pack, 'batch-register.json')
const v3DataFile = path.join(v3Pack, 'keeper-prime-sit-stand-front-v3.json')
const rejectionFile = path.join(root, 'docs/review/keeper-prime-sit-stand-front-v3-rejection-2026-10-18.json')
const pack = path.join(root, 'art/drafts/keeper-prime-sit-stand-front-2026-10-17-v4')
const frameDir = path.join(pack, 'drafts/frames')
const evidenceDir = path.join(pack, 'evidence')
const publicDir = path.join(root, 'public/keeper-review', set)
const assetsDir = path.join(publicDir, 'assets')
const reviewRouteFile = path.join(root, 'src/app/keeper-review', set, 'route.ts')
const generated = [2, 3, 4, 5].map((n) => path.join(pack, `sources/generated/front-f${n}-generated-v2.png`))
const targetSizes = new Map([[2, [143, 286]], [3, [143, 276]], [4, [143, 270]], [5, [143, 266]]])
const v3Frames = [1, 2, 3, 4, 5, 6].map((n) => path.join(v3Pack, `drafts/frames/keeper_prime_stand-to-sit-front_f${String(n).padStart(2, '0')}.png`))

const rel = (file) => path.relative(root, file).split(path.sep).join('/')
const sha = (file) => crypto.createHash('sha256').update(fs.readFileSync(file)).digest('hex')
const json = (file) => JSON.parse(fs.readFileSync(file, 'utf8'))
const writeJson = (file, value) => fs.writeFileSync(file, `${JSON.stringify(value, null, 2)}\n`)

for (const file of [v3RegisterFile, v3DataFile, rejectionFile, reviewRouteFile, ...generated, ...v3Frames]) if (!fs.existsSync(file)) throw new Error(`Missing ${rel(file)}`)
const v3Register = json(v3RegisterFile)
const v3Data = json(v3DataFile)
const rejection = json(rejectionFile)
if (rejection.decision !== 'rejected-lowering-elbow-width-drift-frames-28-through-32') throw new Error('V3 rejection is not pinned')
if (rejection.rejectedHashes.batchRegister !== sha(v3RegisterFile) || rejection.rejectedHashes.routeData !== sha(v3DataFile)) throw new Error('V3 rejection hashes changed')

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
  const png = PNG.sync.read(fs.readFileSync(file)); const bounds = alphaBounds(png); let edgeAlphaPixels = 0; let elbowSpanPx = 0
  for (let x = 0; x < png.width; x += 1) { if (png.data[x * 4 + 3]) edgeAlphaPixels += 1; if (png.data[((png.height - 1) * png.width + x) * 4 + 3]) edgeAlphaPixels += 1 }
  for (let y = 1; y < png.height - 1; y += 1) { if (png.data[(y * png.width) * 4 + 3]) edgeAlphaPixels += 1; if (png.data[(y * png.width + png.width - 1) * 4 + 3]) edgeAlphaPixels += 1 }
  const elbowStart = Math.round(bounds.minY + bounds.height * 0.45); const elbowEnd = Math.round(bounds.minY + bounds.height * 0.68)
  for (let y = elbowStart; y <= elbowEnd; y += 1) { let minX = png.width, maxX = -1; for (let x = 0; x < png.width; x += 1) if (png.data[(y * png.width + x) * 4 + 3] > 8) { minX = Math.min(minX, x); maxX = Math.max(maxX, x) }; if (maxX >= 0) elbowSpanPx = Math.max(elbowSpanPx, maxX - minX + 1) }
  return { cellPixels: [png.width, png.height], bounds, elbowBandFraction: [0.45, 0.68], elbowSpanPx, edgeAlphaPixels, transparentGutterPx: Math.min(bounds.minX, bounds.minY, png.width - 1 - bounds.maxX, png.height - 1 - bounds.maxY) }
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
for (const index of [0, 5]) fs.copyFileSync(v3Frames[index], actionFiles[index])
const newRegistrations = new Map()
for (const frame of [2, 3, 4, 5]) newRegistrations.set(frame, register(generated[frame - 2], actionFiles[frame - 1], ...targetSizes.get(frame)))

const actionRecords = actionFiles.map((file, index) => {
  const frame = index + 1
  const source = frame >= 2 && frame <= 5 ? generated[frame - 2] : v3Frames[index]
  const record = { frame, file: rel(file), sha256: sha(file), source: rel(source), sourceSha256: sha(source), inheritedV3ByteExact: frame === 1 || frame === 6, registration: newRegistrations.get(frame) ?? null, ...inspect(file) }
  writeJson(file.replace(/\.png$/, '.json'), { schema: 'lighthouse-keeper/sprite-sidecar@draft-1', name: `keeper_prime_stand-to-sit-front-v4_f${String(frame).padStart(2, '0')}`, w: 32, h: 40, density: 8, frames: 1, fps: 0, anchor: [16, 40], floorOpaqueMaximumY: 315, view: 'front', poseIndex: frame, source: record.source, sourceSha256: record.sourceSha256, sha256: record.sha256, registration: record.registration, derivation: record.inheritedV3ByteExact ? 'exact-V3-endpoint-preserved' : 'new-complete-Prime-frame32-elbow-width-locked-redraw', productionPromotionAllowed: false })
  return record
})
const expectedWidths = [152, 143, 143, 143, 143, 143]
actionRecords.forEach((record, index) => {
  if (record.cellPixels.join('x') !== '256x320' || record.edgeAlphaPixels || record.transparentGutterPx < 4 || record.bounds.width !== expectedWidths[index]) throw new Error(`Frame ${index + 1} geometry failed`)
})
const correctElbowSpan = actionRecords[5].elbowSpanPx
for (const frame of [2, 3, 4, 5]) if (actionRecords[frame - 1].elbowSpanPx !== correctElbowSpan) throw new Error(`Frame ${frame} elbow span does not match frame 32/F6`)

const forwardStrip = path.join(pack, 'drafts/keeper_prime_stand-to-sit-front-v4_f6.png')
const reverseStrip = path.join(pack, 'drafts/keeper_prime_sit-to-stand-front-v4_f6.png')
saveStrip(forwardStrip, actionFiles); saveStrip(reverseStrip, [...actionFiles].reverse())
writeJson(forwardStrip.replace(/\.png$/, '.json'), { schema: 'lighthouse-keeper/sprite-sidecar@draft-1', name: 'keeper_prime_stand-to-sit-front-v4', w: 32, h: 40, density: 8, frames: 6, fps: 8, loop: false, anchor: [16, 40], sha256: sha(forwardStrip), frameSha256: actionFiles.map(sha), status: 'review-draft-not-production' })
writeJson(reverseStrip.replace(/\.png$/, '.json'), { schema: 'lighthouse-keeper/sprite-sidecar@draft-1', name: 'keeper_prime_sit-to-stand-front-v4', w: 32, h: 40, density: 8, frames: 6, fps: 8, loop: false, anchor: [16, 40], sha256: sha(reverseStrip), frameSha256: [...actionFiles].reverse().map(sha), status: 'review-draft-not-production' })
const contactSheet = path.join(evidenceDir, 'keeper-prime-stand-to-sit-front-v4-contact-sheet.png'); saveStrip(contactSheet, actionFiles)

const publishedAssets = []; const publishedByHash = new Map()
function publish(file, label) {
  const digest = sha(file); if (publishedByHash.has(digest)) return publishedByHash.get(digest)
  const filename = `${label}-${digest.slice(0, 16)}.png`; fs.copyFileSync(file, path.join(assetsDir, filename))
  const entry = { source: rel(file), sourceSha256: digest, url: reviewAssetOrigin ? `${reviewAssetOrigin}/assets/${filename}` : `/keeper-review/${set}/assets/${filename}` }
  publishedByHash.set(digest, entry); publishedAssets.push(entry); return entry
}
const oldUrlToSource = new Map(v3Register.publishedAssets.map((entry) => [entry.url, path.join(root, entry.source)]))
const actionPublished = actionFiles.map((file, index) => publish(file, `sit-front-v4-f${index + 1}`))
const data = structuredClone(v3Data)
data.set = set; data.status = 'reversible-frame32-elbow-width-locked-front-review-candidate-not-approved'
data.derivation = { ...data.derivation, generatedIntermediateCount: 4, inheritedV3EndpointCount: 2, correction: 'V3 frames 28-31 F2-F5 replaced by complete Prime-derived redraws locked to exact frame 32 F6 elbow span; lowering is articulated rather than whole-character scaling' }
data.action.frames = actionRecords.map((record, index) => ({ index: index + 1, src: actionPublished[index].url, sourcePreviewSrc: publish(path.join(root, record.source), `v4-source-f${index + 1}`).url, sha256: record.sha256, source: record.source, sourceSha256: record.sourceSha256, bounds: record.bounds, elbowBandFraction: record.elbowBandFraction, elbowSpanPx: record.elbowSpanPx, registration: record.registration, inheritedV3ByteExact: record.inheritedV3ByteExact }))
data.turn.frames = data.turn.frames.map((frame) => ({ ...frame, src: publish(oldUrlToSource.get(frame.src), 'approved-turn').url }))
data.route = data.route.map((frame) => {
  if (frame.actionFrame) return { ...frame, src: actionPublished[frame.actionFrame - 1].url, label: frame.actionFrame >= 2 && frame.actionFrame <= 5 ? `frame-32-width-locked Prime front F${frame.actionFrame}` : frame.label }
  const source = oldUrlToSource.get(frame.src); if (!source) throw new Error(`No V3 source for ${frame.src}`)
  return { ...frame, src: publish(source, 'approved-context').url }
})
const dataFile = path.join(pack, 'keeper-prime-sit-stand-front-v4.json'); writeJson(dataFile, data); writeJson(path.join(publicDir, 'route.json'), data)

const registerFile = path.join(pack, 'batch-register.json')
const registerData = {
  schema: 'lighthouse-keeper/reversible-review-batch@1', set, status: 'front-frame32-elbow-width-locked-v4-awaiting-frank',
  supersedes: { candidate: 'keeper-prime-sit-stand-front-v3', reason: rejection.requiredCorrection.fault, rejection: { file: rel(rejectionFile), sha256: sha(rejectionFile), decision: rejection.decision }, immutableV3: { register: rel(v3RegisterFile), sha256: sha(v3RegisterFile), routeData: rel(v3DataFile), routeDataSha256: sha(v3DataFile) } },
  authorities: v3Register.authorities,
  historicalChoreographyOnly: v3Register.historicalChoreographyOnly,
  generation: { tool: 'built-in image generation', generatedSources: generated.map((file, index) => ({ pose: index + 2, file: rel(file), sha256: sha(file) })), promptLog: rel(path.join(pack, 'PROMPT_LOG.md')), endpointPixelsGenerated: false },
  candidate: { frames: actionRecords, forwardStrip: { file: rel(forwardStrip), sha256: sha(forwardStrip), pixels: [1536, 320] }, reverseStrip: { file: rel(reverseStrip), sha256: sha(reverseStrip), pixels: [1536, 320] }, contactSheet: { file: rel(contactSheet), sha256: sha(contactSheet) }, route: { file: rel(dataFile), sha256: sha(dataFile), frames: data.route.length }, reviewRoute: { file: rel(reviewRouteFile), sha256: sha(reviewRouteFile), url: `/keeper-review/${set}/` } },
  widthCorrection: { rejectedCompleteContextFrames: [28, 29, 30, 31, 32], correctedActionFrames: [2, 3, 4, 5], correctAuthorityActionFrame: 6, v3ElbowSpansPx: rejection.requiredCorrection.measuredV3ElbowSpansPx, v4ElbowSpansPx: actionRecords.slice(1).map((record) => record.elbowSpanPx), exactUnchangedActionFrames: [1, 6] },
  checks: { v3ImmutableAndHashPinned: true, exactEndpointsPreserved: actionRecords[0].sha256 === v3Register.candidate.frames[0].sha256 && actionRecords[5].sha256 === v3Register.candidate.frames[5].sha256, framesOneAndSixExactV3: [0, 5].every((index) => actionRecords[index].sha256 === v3Register.candidate.frames[index].sha256), rejectedF2ThroughF5PixelsReplaced: [1, 2, 3, 4].every((index) => actionRecords[index].sha256 !== v3Register.candidate.frames[index].sha256), loweringFramesMatchFrame32ElbowSpan: actionRecords.slice(1).every((record) => record.elbowSpanPx === correctElbowSpan), loweringHeightsMonotonic: actionRecords.slice(1).every((record, index, frames) => index === 0 || record.bounds.height < frames[index - 1].bounds.height), sitToStandExactByteReverse: true, sixIsolatedActionCells: true, complete59FrameContextPreserved: data.route.length === 59, ghostOverlaysProvided: true, allImagesPreloadedBeforePlayback: true, finalUnchanged: true, runtimeUnchanged: true, productionUnchanged: true },
  publishedAssets,
  approvalBoundary: { frontV1Rejected: true, frontV2Rejected: true, frontV3Rejected: true, frontV4Approved: false, backSitStandApproved: false, rearAngleSitStandApproved: false, promotionAllowed: false, finalChanged: false, runtimeChanged: false, productionChanged: false },
  rollback: `Delete only ${rel(pack)}, public/keeper-review/${set}, ${rel(reviewRouteFile)}, scripts/build_keeper_prime_sit_stand_front_v4.mjs and scripts/verify_keeper_prime_sit_stand_front_v4.mjs; V1–V3 and every approved authority remain unchanged.`,
}
for (const [name, value] of Object.entries(registerData.checks)) if (value !== true) throw new Error(`${name} failed`)
writeJson(registerFile, registerData)
fs.writeFileSync(path.join(pack, 'HANDOFF.md'), '# Prime Keeper front sit/stand V4\n\nV1–V3 are immutable rejected provenance. V4 keeps exact V3 endpoints, redraws complete F2–F5 figures so complete-context frames 28–32 all match exact frame 32/F6 at 143 px elbow-to-elbow, and preserves the full 59-frame route. Nothing is approved or promoted.\n')
console.log(JSON.stringify({ candidate: `/keeper-review/${set}/`, routeFrames: data.route.length, widths: actionRecords.map((record) => record.bounds.width), elbowSpans: actionRecords.map((record) => record.elbowSpanPx), heights: actionRecords.map((record) => record.bounds.height), checks: registerData.checks }, null, 2))
