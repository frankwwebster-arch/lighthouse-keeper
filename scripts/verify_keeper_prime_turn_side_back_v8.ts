#!/usr/bin/env node
/** Verify V8's 16-pose cadence, ear occlusion, geometry, strips and review surface. */
import crypto from 'node:crypto'
import fs from 'node:fs'
import path from 'node:path'
import { PNG } from 'pngjs'

const ROOT = path.resolve(import.meta.dirname, '..')
const PACK = path.join(ROOT, 'art/drafts/keeper-prime-turn-side-back-2026-10-13-v8')
const REGISTER = path.join(PACK, 'batch-register.json')
const V7_REGISTER = path.join(ROOT, 'art/drafts/keeper-prime-turn-side-back-2026-10-13-v7/batch-register.json')
const PALETTE = path.join(ROOT, 'art/drafts/keeper-prime-turn-side-back-2026-10-13-v3/palette/keeper-standard-outfit-palette-v1-draft.json')
const PUBLIC = path.join(ROOT, 'public/keeper-review/keeper-prime-turn-side-back-v8')
const PUBLIC_ROUTE = '/keeper-review/keeper-prime-turn-side-back-v8'
const ANGLES = [90, 94, 98, 101.5, 105, 112.5, 120, 127.5, 135, 142.5, 150, 157.5, 165, 170, 175, 180]
const RETAINED = [1, 3, 5, 7, 9, 11, 13, 16]
const fail = (message: string): never => { throw new Error(`Keeper Prime side ↔ back Turn V8: ${message}`) }
const sha256 = (file: string) => crypto.createHash('sha256').update(fs.readFileSync(file)).digest('hex')

for (const file of [REGISTER, V7_REGISTER, PALETTE, path.join(PACK, 'HANDOFF.md'), path.join(PACK, 'PROMPT_LOG.md'), path.join(PUBLIC, 'index.html')]) {
  if (!fs.existsSync(file)) fail(`missing ${path.relative(ROOT, file)}`)
}
const register = JSON.parse(fs.readFileSync(REGISTER, 'utf8')) as Record<string, any>
const v7 = JSON.parse(fs.readFileSync(V7_REGISTER, 'utf8')) as Record<string, any>
const palette = JSON.parse(fs.readFileSync(PALETTE, 'utf8')) as Record<string, any>
if (register.batchId !== 'keeper-prime-turn-side-back-2026-10-13-v8' || register.status !== 'draft-v8-sixteen-pose-cadence-awaiting-visual-approval') fail('batch identity/status changed')
if (register.sourceCandidate?.registerSha256 !== sha256(V7_REGISTER) || register.palette?.sha256 !== sha256(PALETTE)) fail('V7/palette provenance changed')
if (JSON.stringify(register.anglesDegrees) !== JSON.stringify(ANGLES) || JSON.stringify(register.retainedV7Positions) !== JSON.stringify(RETAINED)) fail('angle/retention plan changed')
if (register.cadence?.v7?.authoredPoses !== 8 || register.cadence?.v7?.fps !== 8 || register.cadence?.v8?.authoredPoses !== 16 || register.cadence?.v8?.fps !== 16 || register.cadence?.v7?.durationSeconds !== 1 || register.cadence?.v8?.durationSeconds !== 1) fail('equal-duration cadence contract changed')

const frames = register.frames as Record<string, any>[]
if (frames.length !== 16 || register.generatedSources?.length !== 8) fail('expected sixteen frames and eight new intermediates')
const decoded = frames.map((record, index) => {
  const file = path.join(ROOT, record.file)
  if (!fs.existsSync(file) || sha256(file) !== record.sha256) fail(`frame ${index + 1} hash changed`)
  const png = PNG.sync.read(fs.readFileSync(file))
  if (png.width !== 256 || png.height !== 320) fail(`frame ${index + 1} cell geometry changed`)
  if (record.angleDegrees !== ANGLES[index] || record.floorY !== 316) fail(`frame ${index + 1} angle/floor changed`)
  for (let x = 0; x < 256; x += 1) if (png.data[x * 4 + 3] || png.data[((319 * 256 + x) * 4) + 3]) fail(`frame ${index + 1} touches a horizontal cell edge`)
  for (let y = 1; y < 319; y += 1) if (png.data[(y * 256) * 4 + 3] || png.data[(y * 256 + 255) * 4 + 3]) fail(`frame ${index + 1} touches a vertical cell edge`)
  if (record.edgeAlphaPixels !== 0) fail(`frame ${index + 1} recorded edge alpha`)
  return png
})

for (let oldIndex = 0; oldIndex < 8; oldIndex += 1) {
  const newIndex = RETAINED[oldIndex] - 1
  const currentFile = path.join(ROOT, frames[newIndex].file)
  const priorFile = path.join(ROOT, v7.frames[oldIndex].file)
  if (!fs.readFileSync(currentFile).equals(fs.readFileSync(priorFile))) fail(`retained V7 frame ${oldIndex + 1} is not byte-identical at V8 frame ${newIndex + 1}`)
  if (frames[newIndex].source?.kind !== 'retained-v7' || frames[newIndex].source?.v7Sha256 !== v7.frames[oldIndex].sha256) fail(`retained provenance missing at V8 frame ${newIndex + 1}`)
}

for (const generated of register.generatedSources as Record<string, any>[]) {
  const source = path.join(ROOT, generated.source)
  if (!fs.existsSync(source) || sha256(source) !== generated.sourceSha256) fail(`generated source changed for frame ${generated.frame}`)
  const sourcePng = PNG.sync.read(fs.readFileSync(source))
  if (sourcePng.width !== 1122 || sourcePng.height !== 1402) fail(`generated source dimensions changed for frame ${generated.frame}`)
  if (generated.registration?.axisX !== 128 || generated.registration?.floorY !== 316 || generated.registration?.filter !== 'Lanczos' || generated.registration?.creativePixelWarp !== false) fail(`registration changed for frame ${generated.frame}`)
  if (generated.trouserBootMaskOverlapPixels !== 0) fail(`trouser/boot masks overlap for frame ${generated.frame}`)
  for (const name of Object.keys(generated.componentChecks)) {
    const check = generated.componentChecks[name]
    for (const [fileKey, hashKey] of [['coverageMask', 'coverageMaskSha256'], ['changedMask', 'changedMaskSha256']] as const) {
      if (sha256(path.join(ROOT, check[fileKey])) !== check[hashKey]) fail(`${name} ${fileKey} changed for frame ${generated.frame}`)
    }
    const target = palette.components[name].target.medianHSV as number[]
    const measured = check.corrected.medianHSV as number[]
    for (let channel = 0; channel < 3; channel += 1) {
      if (Math.abs(target[channel] - measured[channel]) > [0.02, 0.08, 0.02][channel]) fail(`${name} palette target missed for frame ${generated.frame}`)
    }
  }
}

for (let index = 1; index < frames.length; index += 1) {
  if (Math.abs(frames[index].opaqueHeight - frames[index - 1].opaqueHeight) > 2) fail(`height jumps at F${index}→F${index + 1}`)
  if (Math.abs(frames[index].alphaCentroid[0] - frames[index - 1].alphaCentroid[0]) > 4) fail(`horizontal centroid jumps at F${index}→F${index + 1}`)
  if (Math.abs(frames[index].alphaCentroid[1] - frames[index - 1].alphaCentroid[1]) > 8) fail(`vertical centroid jumps at F${index}→F${index + 1}`)
}
const earCounts = [12, 13, 14, 15].map(index => frames[index].farLeftEarSkinPixels)
if (JSON.stringify(earCounts) !== '[0,13,25,181]' || !(earCounts[0] < earCounts[1] && earCounts[1] < earCounts[2] && earCounts[2] < earCounts[3])) fail(`far-ear reveal changed: ${JSON.stringify(earCounts)}`)
if (JSON.stringify(register.earOcclusion?.farLeftEarSkinPixels) !== JSON.stringify(earCounts)) fail('ear-occlusion record disagrees with frames')

for (const direction of ['forward', 'reverse'] as const) {
  const record = register.animation[direction]
  const stripPath = path.join(ROOT, record.file)
  const sidecarPath = path.join(ROOT, record.sidecar)
  if (sha256(stripPath) !== record.sha256 || sha256(sidecarPath) !== record.sidecarSha256) fail(`${direction} strip/sidecar changed`)
  const sidecar = JSON.parse(fs.readFileSync(sidecarPath, 'utf8')) as Record<string, any>
  if (sidecar.frames !== 16 || sidecar.fps !== 16 || sidecar.durationSeconds !== 1 || sidecar.w !== 32 || sidecar.h !== 40 || sidecar.density !== 8 || sidecar.sha256 !== record.sha256) fail(`${direction} sidecar contract changed`)
  const strip = PNG.sync.read(fs.readFileSync(stripPath))
  if (strip.width !== 4096 || strip.height !== 320) fail(`${direction} strip geometry changed`)
  for (let frame = 0; frame < 16; frame += 1) {
    const expected = decoded[direction === 'forward' ? frame : 15 - frame]
    for (let y = 0; y < 320; y += 1) {
      const start = ((y * strip.width) + frame * 256) * 4
      if (!strip.data.subarray(start, start + 1024).equals(expected.data.subarray(y * 1024, y * 1024 + 1024))) fail(`${direction} strip F${frame + 1} disagrees with frame file`)
    }
  }
}

for (const flag of ['allEightV7PosesByteIdentical', 'everyFrameFloorY316', 'everyFrameTransparentCellEdge', 'allNewTrouserBootMasksDisjoint', 'forwardReverseExact', 'stripSidecarAgreement']) if (register.validation?.[flag] !== true) fail(`${flag} validation changed`)
if (register.validation?.newIntermediateCount !== 8) fail('new-intermediate count changed')
for (const flag of ['productionSpritesChanged', 'runtimeManifestChanged', 'finalLaneChanged', 'priorDraftsChanged']) if (register.validation?.[flag] !== false) fail(`${flag} boundary changed`)
if (register.approvalBoundary?.v8Approved !== false || register.approvalBoundary?.v7Superseded !== false || register.approvalBoundary?.productionPromotionAllowed !== false || register.approvalBoundary?.finalLaneEntryAllowed !== false) fail('approval boundary changed')
for (const evidence of Object.values(register.evidence) as Record<string, any>[]) if (sha256(path.join(ROOT, evidence.file)) !== evidence.sha256) fail(`evidence changed: ${evidence.file}`)

const html = fs.readFileSync(path.join(PUBLIC, 'index.html'), 'utf8')
for (const phrase of ['Keeper Prime Turn V8', '16 authored poses', 'same one-second', 'id="previous"', 'id="next"', 'id="largePlayer"', 'id="gamePlayer"', 'id="oldPlayer"', 'id="comparePlayer"', 'width:128px;height:160px', 'far/left ear']) if (!html.includes(phrase)) fail(`review page omits ${phrase}`)
if (html.includes('src="assets/') || html.includes('"assets/')) fail('review page uses relative assets')
for (let index = 1; index <= 16; index += 1) {
  const asset = fs.readdirSync(path.join(PUBLIC, 'assets')).find(name => name.startsWith(`frame${index}-`))
  if (!asset || !html.includes(`${PUBLIC_ROUTE}/assets/${asset}`) || sha256(path.join(PUBLIC, 'assets', asset)) !== frames[index - 1].sha256) fail(`public frame ${index} changed or misrouted`)
}
const script = html.split('<script>')[1]?.split('</script>')[0]
if (!script) fail('review playback script missing')
new Function(script)

console.log('Keeper Prime side ↔ back Turn V8 verified: 16 poses/16 fps over one second; all V7 poses exact; progressive far-ear occlusion; stable geometry; palette masks, strips, sidecars and review assets agree; no promotion.')
