#!/usr/bin/env node
/** Verify the boot-only F8 redraw and its strict V3 preservation boundary. */
import crypto from 'node:crypto'
import fs from 'node:fs'
import path from 'node:path'
import { PNG } from 'pngjs'

const ROOT = path.resolve(import.meta.dirname, '..')
const PACK = path.join(ROOT, 'art/drafts/keeper-prime-turn-side-back-2026-10-13-v4')
const PRIOR_REGISTER = path.join(ROOT, 'art/drafts/keeper-prime-turn-side-back-2026-10-13-v3/batch-register.json')
const REGISTER = path.join(PACK, 'batch-register.json')
const PUBLIC = path.join(ROOT, 'public/keeper-review/keeper-prime-turn-side-back-v4')
const PUBLIC_ROUTE = '/keeper-review/keeper-prime-turn-side-back-v4'
const CUT_Y = 250
const fail = (message: string): never => { throw new Error(`Keeper Prime side ↔ back Turn V4: ${message}`) }
const sha256 = (file: string) => crypto.createHash('sha256').update(fs.readFileSync(file)).digest('hex')

for (const file of [REGISTER, PRIOR_REGISTER, path.join(PACK, 'HANDOFF.md'), path.join(PACK, 'PROMPT_LOG.md'), path.join(PUBLIC, 'index.html')]) {
  if (!fs.existsSync(file)) fail(`missing ${path.relative(ROOT, file)}`)
}
const register = JSON.parse(fs.readFileSync(REGISTER, 'utf8')) as Record<string, any>
const prior = JSON.parse(fs.readFileSync(PRIOR_REGISTER, 'utf8')) as Record<string, any>
if (register.batchId !== 'keeper-prime-turn-side-back-2026-10-13-v4' || register.status !== 'draft-side-back-turn-v4-boot-geometry-awaiting-visual-approval') fail('batch identity/status changed')
if (register.priorDraft?.registerSha256 !== sha256(PRIOR_REGISTER)) fail('V3 provenance changed')
const palettePath = path.join(ROOT, register.palette.file)
if (register.palette.status !== 'draft-awaiting-visual-approval' || sha256(palettePath) !== register.palette.sha256) fail('V3 draft palette provenance changed')

const generation = register.generation
for (const [key, hashKey] of [['source', 'sourceSha256'], ['cleanSource', 'cleanSourceSha256']] as const) {
  const file = path.join(ROOT, generation[key])
  if (!fs.existsSync(file) || sha256(file) !== generation[hashKey]) fail(`${key} provenance changed`)
}
if (generation.creativePixelWarp !== false || generation.registration?.creativePixelWarp !== false) fail('creative pixel warping entered the registration')
if (generation.acceptedRegion?.minYInclusive !== CUT_Y || generation.acceptedRegion?.maxYExclusive !== 320 || generation.rejectedRegion?.maxYExclusive !== CUT_Y) fail('generated-region boundary changed')

const frames = register.frames as Record<string, any>[]
if (frames.length !== 8 || JSON.stringify(frames.map((item) => item.angleDegrees)) !== '[90,98,105,120,135,150,165,180]') fail('frame sequence changed')
const currentPngs = frames.map((item) => PNG.sync.read(fs.readFileSync(path.join(ROOT, item.file))))
const priorPngs = prior.frames.map((item: Record<string, any>) => PNG.sync.read(fs.readFileSync(path.join(ROOT, item.file))))
for (let index = 0; index < 7; index += 1) {
  const currentFile = path.join(ROOT, frames[index].file)
  const priorFile = path.join(ROOT, prior.frames[index].file)
  if (!fs.readFileSync(currentFile).equals(fs.readFileSync(priorFile))) fail(`frame ${index + 1} is not byte-identical to V3`)
  if (frames[index].sha256 !== sha256(currentFile) || frames[index].sourceV3Sha256 !== sha256(priorFile) || frames[index].change !== 'none-byte-identical') fail(`frame ${index + 1} provenance changed`)
}

const current = currentPngs[7]
const original = priorPngs[7]
const changedMaskPath = path.join(ROOT, register.bootRedraw.changedMask)
if (sha256(changedMaskPath) !== register.bootRedraw.changedMaskSha256) fail('changed-pixel mask changed')
const changedMask = PNG.sync.read(fs.readFileSync(changedMaskPath))
let changedPixels = 0
for (let y = 0; y < 320; y += 1) for (let x = 0; x < 256; x += 1) {
  const offset = (y * 256 + x) * 4
  const changed = !current.data.subarray(offset, offset + 4).equals(original.data.subarray(offset, offset + 4))
  const declared = changedMask.data[offset] > 0
  if (changed !== declared) fail(`changed-pixel mask disagrees at ${x},${y}`)
  if (changed && y < CUT_Y) fail(`F8 changed above the boot boundary at ${x},${y}`)
  if (changed) changedPixels += 1
}
if (changedPixels !== register.bootRedraw.changedPixels || changedPixels !== 5900) fail('F8 changed-pixel count changed')
if (frames[7].change !== 'boot-geometry-and-palette-only-below-y250' || frames[7].sha256 !== sha256(path.join(ROOT, frames[7].file))) fail('F8 change declaration changed')
if (frames[7].sourceV3Sha256 !== sha256(path.join(ROOT, prior.frames[7].file))) fail('F8 V3 provenance changed')

const alphaBounds = (png: PNG): [number, number, number, number] => {
  const xs: number[] = [], ys: number[] = []
  for (let y = 0; y < png.height; y += 1) for (let x = 0; x < png.width; x += 1) if (png.data[(y * png.width + x) * 4 + 3] >= 8) { xs.push(x); ys.push(y) }
  return [Math.min(...xs), Math.min(...ys), Math.max(...xs) + 1, Math.max(...ys) + 1]
}
const bounds = alphaBounds(current)
if (bounds[1] !== 18 || bounds[3] !== 316 || frames[7].opaqueHeight !== 298) fail('F8 cap top, height or floor anchor changed')
for (const [index, png] of currentPngs.entries()) {
  if (png.width !== 256 || png.height !== 320) fail(`frame ${index + 1} geometry changed`)
  for (let x = 0; x < png.width; x += 1) if (png.data[x * 4 + 3] || png.data[(((png.height - 1) * png.width + x) * 4) + 3]) fail(`frame ${index + 1} touches a horizontal cell edge`)
  for (let y = 1; y < png.height - 1; y += 1) if (png.data[(y * png.width) * 4 + 3] || png.data[(y * png.width + png.width - 1) * 4 + 3]) fail(`frame ${index + 1} touches a vertical cell edge`)
}

const expectedBootTarget = JSON.parse(fs.readFileSync(palettePath, 'utf8')).components.bootNavy.target.medianHSV as number[]
const measuredBootTarget = register.bootRedraw.paletteCheck.targetMedianHSV as number[]
if (JSON.stringify(measuredBootTarget) !== JSON.stringify(expectedBootTarget)) fail('boot target no longer comes from the registered V3 palette')
const corrected = register.bootRedraw.paletteCheck.corrected.medianHSV as number[]
const tolerances = [0.02, 0.08, 0.02]
for (let channel = 0; channel < 3; channel += 1) if (Math.abs(corrected[channel] - expectedBootTarget[channel]) > tolerances[channel]) fail('redrawn boots no longer match the registered palette')
const metrics = register.bootRedraw.metrics
if (metrics.f8V4.floorExclusiveY !== 316 || metrics.f8V4.left.height !== 66 || metrics.f8V4.right.height !== 66) fail('rear boot height or floor geometry changed')
if (metrics.f8V4.left.width >= metrics.f8V3.left.width || metrics.f8V4.right.width >= metrics.f8V3.right.width) fail('rear boots no longer correct the V3 width jump')

for (const direction of ['forward', 'reverse'] as const) {
  const record = register.animation[direction]
  if (sha256(path.join(ROOT, record.file)) !== record.sha256 || sha256(path.join(ROOT, record.sidecar)) !== record.sidecarSha256) fail(`${direction} strip/sidecar hash changed`)
  const sidecar = JSON.parse(fs.readFileSync(path.join(ROOT, record.sidecar), 'utf8')) as Record<string, any>
  if (sidecar.sha256 !== record.sha256 || sidecar.frames !== 8 || sidecar.w !== 32 || sidecar.h !== 40 || sidecar.density !== 8 || sidecar.palette !== 'keeper-standard-outfit-palette-2026-10-13-v1-draft') fail(`${direction} sidecar contract changed`)
  const strip = PNG.sync.read(fs.readFileSync(path.join(ROOT, record.file)))
  if (strip.width !== 2048 || strip.height !== 320) fail(`${direction} strip geometry changed`)
  for (let frame = 0; frame < 8; frame += 1) {
    const expected = currentPngs[direction === 'forward' ? frame : 7 - frame]
    for (let y = 0; y < 320; y += 1) {
      const start = ((y * strip.width) + frame * 256) * 4
      if (!strip.data.subarray(start, start + 1024).equals(expected.data.subarray(y * 1024, y * 1024 + 1024))) fail(`${direction} strip frame ${frame + 1} disagrees with source`)
    }
  }
}

for (const flag of ['frames1To7ByteIdenticalToV3', 'frame8RowsAbove250ByteIdenticalToV3', 'frame8ChangesConfinedToY250AndBelow', 'frame8CapTopAndFloorStable', 'everyFrameTransparentCellEdge']) if (register.validation?.[flag] !== true) fail(`${flag} validation changed`)
for (const flag of ['productionSpritesChanged', 'runtimeManifestChanged', 'approvedBackMasterChanged', 'priorDraftsChanged']) if (register.validation?.[flag] !== false) fail(`${flag} boundary changed`)
for (const flag of ['sideBackTurnV4Approved', 'rearBootEndpointApproved', 'standardOutfitPaletteApproved', 'finalLaneEntryAllowed', 'productionPromotionAllowed']) if (register.approvalBoundary?.[flag] !== false) fail(`${flag} approval boundary changed`)
for (const evidence of Object.values(register.evidence) as Record<string, any>[]) if (sha256(path.join(ROOT, evidence.file)) !== evidence.sha256) fail(`evidence changed: ${evidence.file}`)

const html = fs.readFileSync(path.join(PUBLIC, 'index.html'), 'utf8')
for (const phrase of ['Keeper Prime Turn V4', 'F8 boot geometry correction', 'F1–F7 are exact V3 bytes', 'exact V3 above y=250', 'Nothing has entered Final or production']) if (!html.includes(phrase)) fail(`review page omits ${phrase}`)
if (html.includes('src="assets/') || html.includes('"assets/')) fail('review page uses trailing-slash-dependent relative asset URLs')
for (let index = 1; index <= 8; index += 1) {
  const asset = fs.readdirSync(path.join(PUBLIC, 'assets')).find((name) => name.startsWith(`frame${index}-`))
  if (!asset || !html.includes(`${PUBLIC_ROUTE}/assets/${asset}`)) fail(`review page does not route frame ${index} correctly`)
}
const script = html.split('<script>')[1]?.split('</script>')[0]
if (!script) fail('public playback script missing')
new Function(script)

console.log(`Keeper Prime side ↔ back Turn V4 verified: F1–F7 exact V3; F8 exact above y=${CUT_Y}; ${changedPixels} boot-region pixels; palette/floor/gutters/strips locked; no promotion.`)
