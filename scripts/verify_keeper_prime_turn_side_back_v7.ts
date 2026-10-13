#!/usr/bin/env node
/** Verify V7's isolated Frame 8 lower-leg correction and review surface. */
import crypto from 'node:crypto'
import fs from 'node:fs'
import path from 'node:path'
import { PNG } from 'pngjs'

const ROOT = path.resolve(import.meta.dirname, '..')
const PACK = path.join(ROOT, 'art/drafts/keeper-prime-turn-side-back-2026-10-13-v7')
const REGISTER = path.join(PACK, 'batch-register.json')
const V6_REGISTER = path.join(ROOT, 'art/drafts/keeper-prime-turn-side-back-2026-10-13-v6/batch-register.json')
const V5_APPROVAL = path.join(ROOT, 'art/drafts/keeper-prime-turn-side-back-2026-10-13-v5/batch-register.json')
const V4_REGISTER = path.join(ROOT, 'art/drafts/keeper-prime-turn-side-back-2026-10-13-v4/batch-register.json')
const PUBLIC = path.join(ROOT, 'public/keeper-review/keeper-prime-turn-side-back-v7')
const PUBLIC_ROUTE = '/keeper-review/keeper-prime-turn-side-back-v7'
const fail = (message: string): never => { throw new Error(`Keeper Prime side ↔ back Turn V7: ${message}`) }
const sha256 = (file: string) => crypto.createHash('sha256').update(fs.readFileSync(file)).digest('hex')

for (const file of [REGISTER, V6_REGISTER, V5_APPROVAL, V4_REGISTER, path.join(PACK, 'HANDOFF.md'), path.join(PACK, 'PROMPT_LOG.md'), path.join(PUBLIC, 'index.html')]) if (!fs.existsSync(file)) fail(`missing ${path.relative(ROOT, file)}`)
const register = JSON.parse(fs.readFileSync(REGISTER, 'utf8')) as Record<string, any>
const v6 = JSON.parse(fs.readFileSync(V6_REGISTER, 'utf8')) as Record<string, any>
const v4 = JSON.parse(fs.readFileSync(V4_REGISTER, 'utf8')) as Record<string, any>
if (register.batchId !== 'keeper-prime-turn-side-back-2026-10-13-v7' || register.status !== 'draft-v7-f8-lower-leg-correction-awaiting-visual-approval') fail('batch identity/status changed')
if (register.sourceCandidate?.registerSha256 !== sha256(V6_REGISTER) || register.approvalProvenance?.registerSha256 !== sha256(V5_APPROVAL) || register.geometryReference?.registerSha256 !== sha256(V4_REGISTER)) fail('source/approval provenance changed')
if (register.geometryReference?.f8Sha256 !== v4.frames[7].sha256 || JSON.stringify(register.geometryReference?.targetLowerBoundsFromY260) !== '[75,260,180,316]') fail('approved V4 lower-leg geometry reference changed')

const smooth = register.smoothMaster
const originalPath = path.join(ROOT, smooth.original.file)
const draftPath = path.join(ROOT, smooth.draft.file)
if (sha256(originalPath) !== smooth.original.sha256 || sha256(draftPath) !== smooth.draft.sha256 || JSON.stringify(smooth.original.dimensions) !== '[1122,1402]' || JSON.stringify(smooth.draft.dimensions) !== '[1122,1402]') fail('smooth source provenance changed')
if (smooth.lowerRegistration?.startSourceY !== 1068 || smooth.lowerRegistration?.fullSourceY !== 1120 || smooth.lowerRegistration?.maximumHorizontalScale !== 1.05 || smooth.lowerRegistration?.filter !== 'Lanczos' || smooth.lowerRegistration?.upperMasterRowsUnchanged !== true) fail('lower-master registration changed')
const originalMaster = PNG.sync.read(fs.readFileSync(originalPath))
const draftMaster = PNG.sync.read(fs.readFileSync(draftPath))
for (let y = 0; y < 1068; y += 1) {
  const start = y * originalMaster.width * 4
  const end = start + originalMaster.width * 4
  if (!originalMaster.data.subarray(start, end).equals(draftMaster.data.subarray(start, end))) fail(`smooth master changed above row 1068 at row ${y}`)
}

const frames = register.frames as Record<string, any>[]
if (frames.length !== 8 || JSON.stringify(frames.map((item) => item.angleDegrees)) !== '[90,98,105,120,135,150,165,180]') fail('frame sequence changed')
const current = frames.map((item) => PNG.sync.read(fs.readFileSync(path.join(ROOT, item.file))))
const prior = v6.frames.map((item: Record<string, any>) => PNG.sync.read(fs.readFileSync(path.join(ROOT, item.file))))
for (let index = 0; index < 7; index += 1) {
  if (!fs.readFileSync(path.join(ROOT, frames[index].file)).equals(fs.readFileSync(path.join(ROOT, v6.frames[index].file)))) fail(`frame ${index + 1} is not byte-identical to V6`)
  if (frames[index].change !== 'none-byte-identical-to-v6' || frames[index].changedPixels !== 0) fail(`frame ${index + 1} change boundary changed`)
}
if (frames[7].change !== 'f8-smooth-lower-leg-width-and-nonoverlap-palette' || frames[7].changedPixels !== 5259 || JSON.stringify(frames[7].opaqueBoundsExclusive) !== '[50,18,205,316]' || frames[7].opaqueHeight !== 298) fail('F8 declared correction changed')

let changed = 0
let earliestY = 320
for (let pixel = 0; pixel < 256 * 320; pixel += 1) {
  const offset = pixel * 4
  const different = !current[7].data.subarray(offset, offset + 4).equals(prior[7].data.subarray(offset, offset + 4))
  if (different) { changed += 1; earliestY = Math.min(earliestY, Math.floor(pixel / 256)) }
}
if (changed !== 5259 || earliestY !== 245 || register.changes.frame8.earliestChangedNormalizedRow !== 245) fail('F8 measured change scope changed')
for (let y = 0; y < 245; y += 1) {
  const start = y * 256 * 4
  if (!current[7].data.subarray(start, start + 1024).equals(prior[7].data.subarray(start, start + 1024))) fail(`F8 changed above lower-leg boundary at row ${y}`)
}

const lowerPoints: Array<[number, number]> = []
for (let y = 260; y < 320; y += 1) for (let x = 0; x < 256; x += 1) if (current[7].data[(y * 256 + x) * 4 + 3] >= 8) lowerPoints.push([x, y])
const lowerBounds = [Math.min(...lowerPoints.map(([x]) => x)), 260, Math.max(...lowerPoints.map(([x]) => x)) + 1, Math.max(...lowerPoints.map(([, y]) => y)) + 1]
if (JSON.stringify(lowerBounds) !== '[75,260,180,316]') fail(`F8 lower bounds do not match approved V4: ${JSON.stringify(lowerBounds)}`)

if (register.palette?.trouserBootMaskOverlapPixels !== 0 || register.validation?.trouserBootMasksDisjoint !== true) fail('trouser/boot masks overlap')
const coverages: Record<string, Set<number>> = {}
for (const name of ['capCrownBlue', 'capBandNavy', 'jumperBlue', 'jumperCream', 'trouserNavy', 'bootNavy']) {
  const check = register.palette.componentChecks[name]
  for (const [key, hashKey] of [['coverageMask', 'coverageMaskSha256'], ['changedMask', 'changedMaskSha256']] as const) if (sha256(path.join(ROOT, check[key])) !== check[hashKey]) fail(`${name} ${key} changed`)
  const png = PNG.sync.read(fs.readFileSync(path.join(ROOT, check.coverageMask)))
  coverages[name] = new Set<number>()
  for (let pixel = 0; pixel < 256 * 320; pixel += 1) if (png.data[pixel * 4] > 0) coverages[name].add(pixel)
  const target = check.targetMedianHSV as number[]
  const measured = check.corrected.medianHSV as number[]
  for (let channel = 0; channel < 3; channel += 1) if (Math.abs(target[channel] - measured[channel]) > [0.02, 0.08, 0.02][channel]) fail(`${name} palette target missed`)
}
for (const pixel of coverages.trouserNavy) if (coverages.bootNavy.has(pixel)) fail(`trouser/boot overlap at pixel ${pixel}`)
if (register.palette.v6PatchBrightness?.medianRgbMean !== 110.333333 || register.palette.v7PatchBrightness?.medianRgbMean !== 83.333333 || register.validation?.patchBrightnessReduced !== true) fail('pale-patch brightness correction changed')

for (const [index, png] of current.entries()) {
  if (png.width !== 256 || png.height !== 320 || frames[index].sha256 !== sha256(path.join(ROOT, frames[index].file))) fail(`frame ${index + 1} geometry/hash changed`)
  for (let x = 0; x < 256; x += 1) if (png.data[x * 4 + 3] || png.data[(((319 * 256) + x) * 4) + 3]) fail(`frame ${index + 1} touches horizontal edge`)
  for (let y = 1; y < 319; y += 1) if (png.data[(y * 256) * 4 + 3] || png.data[(y * 256 + 255) * 4 + 3]) fail(`frame ${index + 1} touches vertical edge`)
}
if (sha256(path.join(ROOT, frames[7].changedMask)) !== frames[7].changedMaskSha256) fail('F8 aggregate change mask changed')

for (const direction of ['forward', 'reverse'] as const) {
  const record = register.animation[direction]
  if (sha256(path.join(ROOT, record.file)) !== record.sha256 || sha256(path.join(ROOT, record.sidecar)) !== record.sidecarSha256) fail(`${direction} strip/sidecar changed`)
  const strip = PNG.sync.read(fs.readFileSync(path.join(ROOT, record.file)))
  if (strip.width !== 2048 || strip.height !== 320) fail(`${direction} strip geometry changed`)
  for (let frame = 0; frame < 8; frame += 1) {
    const expected = current[direction === 'forward' ? frame : 7 - frame]
    for (let y = 0; y < 320; y += 1) {
      const start = ((y * strip.width) + frame * 256) * 4
      if (!strip.data.subarray(start, start + 1024).equals(expected.data.subarray(y * 1024, y * 1024 + 1024))) fail(`${direction} strip frame ${frame + 1} disagrees with source`)
    }
  }
}

for (const flag of ['frames1To7ByteIdenticalToV6', 'frame8BoundsStable', 'frame8FloorStable', 'trouserBootMasksDisjoint', 'patchBrightnessReduced', 'lowerBoundsMatchApprovedV4', 'everyFrameTransparentCellEdge']) if (register.validation?.[flag] !== true) fail(`${flag} validation changed`)
for (const flag of ['productionSpritesChanged', 'runtimeManifestChanged', 'finalLaneChanged', 'priorDraftsChanged']) if (register.validation?.[flag] !== false) fail(`${flag} boundary changed`)
if (register.approvalBoundary?.v7Approved !== false || register.approvalBoundary?.v6Superseded !== false || register.approvalBoundary?.productionPromotionAllowed !== false || register.approvalBoundary?.finalLaneEntryAllowed !== false) fail('approval boundary changed')
for (const evidence of Object.values(register.evidence) as Record<string, any>[]) if (sha256(path.join(ROOT, evidence.file)) !== evidence.sha256) fail(`evidence changed: ${evidence.file}`)

const html = fs.readFileSync(path.join(PUBLIC, 'index.html'), 'utf8')
for (const phrase of ['Keeper Prime Turn V7', 'Frames 1–7 byte-identical to V6', 'pale bars above the boots', 'id="previous"', 'id="next"', 'id="largePlayer"', 'id="gamePlayer"', 'width:128px;height:160px', 'large.src=frames[index];game.src=frames[index]']) if (!html.includes(phrase)) fail(`review page omits ${phrase}`)
if (html.includes('src="assets/') || html.includes('"assets/')) fail('review page uses relative assets')
for (let index = 1; index <= 8; index += 1) {
  const asset = fs.readdirSync(path.join(PUBLIC, 'assets')).find((name) => name.startsWith(`frame${index}-`))
  if (!asset || !html.includes(`${PUBLIC_ROUTE}/assets/${asset}`) || sha256(path.join(PUBLIC, 'assets', asset)) !== frames[index - 1].sha256) fail(`public frame ${index} changed or misrouted`)
}
const script = html.split('<script>')[1]?.split('</script>')[0]
if (!script) fail('review playback script missing')
new Function(script)

console.log('Keeper Prime side ↔ back Turn V7 verified: F1–F7 exact V6; F8 pale mask overlap removed; smooth lower boots broadened to V4 bounds; synchronized review; no promotion.')
