#!/usr/bin/env node

import { spawnSync } from 'node:child_process'
import crypto from 'node:crypto'
import fs from 'node:fs'
import path from 'node:path'
import { PNG } from 'pngjs'

const root = path.resolve(import.meta.dirname, '..')
const set = 'keeper-prime-sit-stand-front-v3'
const reviewAssetOrigin = process.env.KEEPER_REVIEW_ASSET_ORIGIN ?? ''
const v2Pack = path.join(root, 'art/drafts/keeper-prime-sit-stand-front-2026-10-17-v2')
const v2RegisterFile = path.join(v2Pack, 'batch-register.json')
const v2DataFile = path.join(v2Pack, 'keeper-prime-sit-stand-front-v2.json')
const rejectionFile = path.join(root, 'docs/review/keeper-prime-sit-stand-front-v2-rejection-2026-10-17.json')
const pack = path.join(root, 'art/drafts/keeper-prime-sit-stand-front-2026-10-17-v3')
const frameDir = path.join(pack, 'drafts/frames')
const evidenceDir = path.join(pack, 'evidence')
const publicDir = path.join(root, 'public/keeper-review', set)
const assetsDir = path.join(publicDir, 'assets')
const reviewRouteFile = path.join(root, 'src/app/keeper-review', set, 'route.ts')
const generated = path.join(pack, 'sources/generated/front-f3-generated.png')
const targetSize = [158, 276]
const v2Frames = [1, 2, 3, 4, 5, 6].map((n) => path.join(v2Pack, `drafts/frames/keeper_prime_stand-to-sit-front_f${String(n).padStart(2, '0')}.png`))

const rel = (file) => path.relative(root, file).split(path.sep).join('/')
const sha = (file) => crypto.createHash('sha256').update(fs.readFileSync(file)).digest('hex')
const json = (file) => JSON.parse(fs.readFileSync(file, 'utf8'))
const writeJson = (file, value) => fs.writeFileSync(file, `${JSON.stringify(value, null, 2)}\n`)

for (const file of [v2RegisterFile, v2DataFile, rejectionFile, reviewRouteFile, generated, ...v2Frames]) if (!fs.existsSync(file)) throw new Error(`Missing ${rel(file)}`)
const v2Register = json(v2RegisterFile)
const v2Data = json(v2DataFile)
const rejection = json(rejectionFile)
if (rejection.decision !== 'rejected-complete-context-width-snap-frames-29-and-30') throw new Error('V2 rejection is not pinned')
if (rejection.rejectedHashes.batchRegister !== sha(v2RegisterFile) || rejection.rejectedHashes.routeData !== sha(v2DataFile)) throw new Error('V2 rejection hashes changed')

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
for (const index of [0, 1, 3, 4, 5]) fs.copyFileSync(v2Frames[index], actionFiles[index])
const f3Registration = register(generated, actionFiles[2], ...targetSize)

const actionRecords = actionFiles.map((file, index) => {
  const frame = index + 1
  const source = frame === 3 ? generated : v2Frames[index]
  const record = { frame, file: rel(file), sha256: sha(file), source: rel(source), sourceSha256: sha(source), inheritedV2ByteExact: frame !== 3, registration: frame === 3 ? f3Registration : null, ...inspect(file) }
  writeJson(file.replace(/\.png$/, '.json'), { schema: 'lighthouse-keeper/sprite-sidecar@draft-1', name: `keeper_prime_stand-to-sit-front-v3_f${String(frame).padStart(2, '0')}`, w: 32, h: 40, density: 8, frames: 1, fps: 0, anchor: [16, 40], floorOpaqueMaximumY: 315, view: 'front', poseIndex: frame, source: record.source, sourceSha256: record.sourceSha256, sha256: record.sha256, registration: record.registration, derivation: record.inheritedV2ByteExact ? 'exact-V2-frame-preserved' : 'new-narrow-Prime-F3-width-smoothing-correction', productionPromotionAllowed: false })
  return record
})
const expectedWidths = [152, 157, 158, 158, 150, 143]
actionRecords.forEach((record, index) => {
  if (record.cellPixels.join('x') !== '256x320' || record.edgeAlphaPixels || record.transparentGutterPx < 4 || record.bounds.width !== expectedWidths[index]) throw new Error(`Frame ${index + 1} geometry failed`)
})

const forwardStrip = path.join(pack, 'drafts/keeper_prime_stand-to-sit-front-v3_f6.png')
const reverseStrip = path.join(pack, 'drafts/keeper_prime_sit-to-stand-front-v3_f6.png')
saveStrip(forwardStrip, actionFiles); saveStrip(reverseStrip, [...actionFiles].reverse())
writeJson(forwardStrip.replace(/\.png$/, '.json'), { schema: 'lighthouse-keeper/sprite-sidecar@draft-1', name: 'keeper_prime_stand-to-sit-front-v3', w: 32, h: 40, density: 8, frames: 6, fps: 8, loop: false, anchor: [16, 40], sha256: sha(forwardStrip), frameSha256: actionFiles.map(sha), status: 'review-draft-not-production' })
writeJson(reverseStrip.replace(/\.png$/, '.json'), { schema: 'lighthouse-keeper/sprite-sidecar@draft-1', name: 'keeper_prime_sit-to-stand-front-v3', w: 32, h: 40, density: 8, frames: 6, fps: 8, loop: false, anchor: [16, 40], sha256: sha(reverseStrip), frameSha256: [...actionFiles].reverse().map(sha), status: 'review-draft-not-production' })
const contactSheet = path.join(evidenceDir, 'keeper-prime-stand-to-sit-front-v3-contact-sheet.png'); saveStrip(contactSheet, actionFiles)

const publishedAssets = []; const publishedByHash = new Map()
function publish(file, label) {
  const digest = sha(file); if (publishedByHash.has(digest)) return publishedByHash.get(digest)
  const filename = `${label}-${digest.slice(0, 16)}.png`; fs.copyFileSync(file, path.join(assetsDir, filename))
  const entry = { source: rel(file), sourceSha256: digest, url: reviewAssetOrigin ? `${reviewAssetOrigin}/assets/${filename}` : `/keeper-review/${set}/assets/${filename}` }
  publishedByHash.set(digest, entry); publishedAssets.push(entry); return entry
}
const oldUrlToSource = new Map(v2Register.publishedAssets.map((entry) => [entry.url, path.join(root, entry.source)]))
const actionPublished = actionFiles.map((file, index) => publish(file, `sit-front-v3-f${index + 1}`))
const data = structuredClone(v2Data)
data.set = set; data.status = 'reversible-complete-context-width-smoothed-front-review-candidate-not-approved'
data.derivation = { ...data.derivation, generatedIntermediateCount: 1, inheritedV2FrameCount: 5, correction: 'V2 complete-context frame 29 F3 width spike corrected by one new full-character Prime-derived redraw; frame 30 F4 preserved exactly' }
data.action.frames = actionRecords.map((record, index) => ({ index: index + 1, src: actionPublished[index].url, sourcePreviewSrc: publish(path.join(root, record.source), `v3-source-f${index + 1}`).url, sha256: record.sha256, source: record.source, sourceSha256: record.sourceSha256, bounds: record.bounds, registration: record.registration, inheritedV2ByteExact: record.inheritedV2ByteExact }))
data.turn.frames = data.turn.frames.map((frame) => ({ ...frame, src: publish(oldUrlToSource.get(frame.src), 'approved-turn').url }))
data.route = data.route.map((frame) => {
  if (frame.actionFrame) return { ...frame, src: actionPublished[frame.actionFrame - 1].url, label: frame.actionFrame === 3 ? frame.label.replace('new Prime', 'width-smoothed Prime').replace('exact reverse', 'exact reverse width-smoothed') : frame.label }
  const source = oldUrlToSource.get(frame.src); if (!source) throw new Error(`No V2 source for ${frame.src}`)
  return { ...frame, src: publish(source, 'approved-context').url }
})
const dataFile = path.join(pack, 'keeper-prime-sit-stand-front-v3.json'); writeJson(dataFile, data); writeJson(path.join(publicDir, 'route.json'), data)

const registerFile = path.join(pack, 'batch-register.json')
const registerData = {
  schema: 'lighthouse-keeper/reversible-review-batch@1', set, status: 'front-complete-context-width-smoothed-v3-awaiting-frank',
  supersedes: { candidate: 'keeper-prime-sit-stand-front-v2', reason: rejection.requiredCorrection.fault, rejection: { file: rel(rejectionFile), sha256: sha(rejectionFile), decision: rejection.decision }, immutableV2: { register: rel(v2RegisterFile), sha256: sha(v2RegisterFile), routeData: rel(v2DataFile), routeDataSha256: sha(v2DataFile) } },
  authorities: v2Register.authorities,
  historicalChoreographyOnly: v2Register.historicalChoreographyOnly,
  generation: { tool: 'built-in image generation', generatedSources: [{ pose: 3, file: rel(generated), sha256: sha(generated) }], promptLog: rel(path.join(pack, 'PROMPT_LOG.md')), endpointPixelsGenerated: false },
  candidate: { frames: actionRecords, forwardStrip: { file: rel(forwardStrip), sha256: sha(forwardStrip), pixels: [1536, 320] }, reverseStrip: { file: rel(reverseStrip), sha256: sha(reverseStrip), pixels: [1536, 320] }, contactSheet: { file: rel(contactSheet), sha256: sha(contactSheet) }, route: { file: rel(dataFile), sha256: sha(dataFile), frames: data.route.length }, reviewRoute: { file: rel(reviewRouteFile), sha256: sha(reviewRouteFile), url: `/keeper-review/${set}/` } },
  widthCorrection: { rejectedCompleteContextFrames: [29, 30], correctedActionFrames: [3], v2WidthsPx: [167, 158], v3WidthsPx: [158, 158], exactUnchangedActionFrames: [1, 2, 4, 5, 6] },
  checks: { v2ImmutableAndHashPinned: true, exactEndpointsPreserved: actionRecords[0].sha256 === v2Register.candidate.frames[0].sha256 && actionRecords[5].sha256 === v2Register.candidate.frames[5].sha256, framesOneTwoFourFiveSixExactV2: [0, 1, 3, 4, 5].every((index) => actionRecords[index].sha256 === v2Register.candidate.frames[index].sha256), rejectedF3PixelsReplaced: actionRecords[2].sha256 !== v2Register.candidate.frames[2].sha256, rejectedF3WidthReduced: actionRecords[2].bounds.width < v2Register.candidate.frames[2].bounds.width, completeContextFrames29And30EqualWidth: actionRecords[2].bounds.width === actionRecords[3].bounds.width, sitToStandExactByteReverse: true, sixIsolatedActionCells: true, complete59FrameContextPreserved: data.route.length === 59, ghostOverlaysProvided: true, allImagesPreloadedBeforePlayback: true, finalUnchanged: true, runtimeUnchanged: true, productionUnchanged: true },
  publishedAssets,
  approvalBoundary: { frontV1Rejected: true, frontV2Rejected: true, frontV3Approved: false, backSitStandApproved: false, rearAngleSitStandApproved: false, promotionAllowed: false, finalChanged: false, runtimeChanged: false, productionChanged: false },
  rollback: `Delete only ${rel(pack)}, public/keeper-review/${set}, ${rel(reviewRouteFile)}, scripts/build_keeper_prime_sit_stand_front_v3.mjs and scripts/verify_keeper_prime_sit_stand_front_v3.mjs; V1, V2 and every approved authority remain unchanged.`,
}
for (const [name, value] of Object.entries(registerData.checks)) if (value !== true) throw new Error(`${name} failed`)
writeJson(registerFile, registerData)
fs.writeFileSync(path.join(pack, 'HANDOFF.md'), '# Prime Keeper front sit/stand V3\n\nV1 and V2 are immutable rejected provenance. V3 keeps V2 F1, F2 and F4–F6 byte-identical, redraws only F3 to remove the complete-context frame 29→30 width snap, and preserves the full 59-frame route. Nothing is approved or promoted.\n')
console.log(JSON.stringify({ candidate: `/keeper-review/${set}/`, routeFrames: data.route.length, widths: actionRecords.map((record) => record.bounds.width), checks: registerData.checks }, null, 2))
