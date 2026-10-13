#!/usr/bin/env node
/** Verify the reversible finished-art Keeper Prime right-facing Walk V1 draft. */
import crypto from 'node:crypto'
import fs from 'node:fs'
import path from 'node:path'
import { PNG } from 'pngjs'

const ROOT = path.resolve(import.meta.dirname, '..')
const PACK = path.join(ROOT, 'art/drafts/keeper-prime-walk-2026-10-13-v1')
const REGISTER = path.join(PACK, 'batch-register.json')
const PUBLIC = path.join(ROOT, 'public/keeper-review/keeper-prime-walk-v1')
const SIDE = path.join(ROOT, 'art/drafts/keeper-prime-side-right-rigged-2026-10-13-v1/drafts/keeper_prime_master-neutral-standing-side-right_f1.png')
const SIDE_APPROVAL = path.join(ROOT, 'art/drafts/keeper-prime-side-right-rigged-2026-10-13-v2/batch-register.json')
const MOTION = path.join(ROOT, 'art/drafts/keeper-prime-construction-rig-2026-10-13-v3/motion/keeper-prime-rig-motion-v3.json')
const MOTION_APPROVAL = path.join(ROOT, 'art/drafts/keeper-prime-construction-rig-2026-10-13-v4/batch-register.json')
const SOURCE = path.join(PACK, 'sources/keeper-prime-walk-8pose-generated.png')
const ORIGINAL_RAW = path.join(ROOT, 'art/raw/keeper-first-batch/keeper_walk_f8.png')
const ORIGINAL_SIDECAR = path.join(ROOT, 'art/raw/keeper-first-batch/keeper_walk_f8.json')
const ORIGINAL_RUNTIME = path.join(ROOT, 'public/sprites/keeper_walk.png')
const SOURCE_HASH = '3df7c4bac24b8e9f066f0dc58a485e330f407fd2b779a120cc50c2a5ffb05e47'
const fail = (message: string): never => { throw new Error(`Keeper Prime Walk V1: ${message}`) }
const sha256 = (file: string) => crypto.createHash('sha256').update(fs.readFileSync(file)).digest('hex')

for (const file of [REGISTER, SIDE, SIDE_APPROVAL, MOTION, MOTION_APPROVAL, SOURCE, ORIGINAL_RAW, ORIGINAL_SIDECAR, ORIGINAL_RUNTIME, path.join(PACK, 'HANDOFF.md'), path.join(PACK, 'PROMPT_LOG.md'), path.join(PUBLIC, 'index.html')]) {
  if (!fs.existsSync(file)) fail(`missing ${path.relative(ROOT, file)}`)
}
if (sha256(SOURCE) !== SOURCE_HASH) fail('selected generated source changed')

const sideApproval = JSON.parse(fs.readFileSync(SIDE_APPROVAL, 'utf8')) as Record<string, any>
if (sideApproval.status !== 'approved-side-right-artwork-authority' || sideApproval.approval?.wording !== 'Approve side-right V1 and build Turn V1.') fail('side-right artwork approval gate changed')
const motionApproval = JSON.parse(fs.readFileSync(MOTION_APPROVAL, 'utf8')) as Record<string, any>
if (motionApproval.status !== 'approved-motion-authority' || motionApproval.approval?.wording !== 'Approved, very good indeed') fail('Rig Motion V3 approval gate changed')

const register = JSON.parse(fs.readFileSync(REGISTER, 'utf8')) as Record<string, any>
if (register.batchId !== 'keeper-prime-walk-2026-10-13-v1' || register.status !== 'draft-finished-art-walk-v1-awaiting-visual-approval') fail('batch identity/status changed')
for (const [name, file, approval] of [['sideRight', SIDE, SIDE_APPROVAL], ['motion', MOTION, MOTION_APPROVAL]] as const) {
  const authority = register.authorities?.[name]
  if (!authority || authority.sha256 !== sha256(file) || authority.approvalSha256 !== sha256(approval)) fail(`${name} authority provenance changed`)
}
if (register.generation?.selectedSource?.sha256 !== SOURCE_HASH || sha256(path.join(ROOT, register.generation.selectedSource.file)) !== SOURCE_HASH) fail('selected source provenance changed')
for (const [name, file] of [['rawStrip', ORIGINAL_RAW], ['rawSidecar', ORIGINAL_SIDECAR], ['runtimeStrip', ORIGINAL_RUNTIME]] as const) {
  const original = register.canonicalComparison?.[name]
  if (!original || original.sha256 !== sha256(file) || sha256(path.join(ROOT, original.file)) !== original.sha256) fail(`${name} canonical comparison changed`)
}
if (register.canonicalComparison?.allRemainUnchanged !== true) fail('canonical comparison mutation boundary changed')
if (register.generation?.cleanSource?.lowAlphaCleanupThreshold !== 8 || sha256(path.join(ROOT, register.generation.cleanSource.file)) !== register.generation.cleanSource.sha256) fail('clean source changed')
if (register.generation?.sourceGrid?.columns !== 4 || register.generation?.sourceGrid?.rows !== 2 || JSON.stringify(register.generation?.sourceGrid?.cell) !== '[384,512]') fail('source grid changed')
if (register.generation?.sourceCells?.length !== 8 || register.generation.sourceCells.some((cell: Record<string, any>) => cell.edgeAlphaPixels !== 0)) fail('source-cell ownership gutter changed')

const frames = register.frames as Record<string, any>[]
if (frames.length !== 8 || register.animation?.frames !== 8 || register.animation?.fps !== 8 || register.animation?.durationSeconds !== 1 || register.animation?.loop !== true) fail('walk timing changed')
const expectedPoses = ['contact', 'down', 'passing', 'up', 'opposite contact', 'opposite down', 'opposite passing', 'opposite up']
if (JSON.stringify(frames.map((frame) => frame.pose)) !== JSON.stringify(expectedPoses)) fail('gait pose order changed')
const framePngs = frames.map((frame) => PNG.sync.read(fs.readFileSync(path.join(ROOT, frame.file))))
const scales = new Set<number>()
for (const [index, frame] of frames.entries()) {
  const local = path.join(ROOT, frame.file)
  if (sha256(local) !== frame.sha256) fail(`frame ${index + 1} hash changed`)
  const png = framePngs[index]
  if (png.width !== 256 || png.height !== 320) fail(`frame ${index + 1} geometry changed`)
  if (frame.edgeAlphaPixels !== 0 || frame.opaqueBoundsExclusive[3] !== 316) fail(`frame ${index + 1} floor/gutter changed`)
  scales.add(frame.registration?.sharedScale)
  if (frame.registration?.perFrameScaleChange !== false || frame.registration?.creativePixelWarp !== false || frame.registration?.filter !== 'Lanczos') fail(`frame ${index + 1} registration method changed`)
  for (let x = 0; x < png.width; x += 1) if (png.data[(x * 4) + 3] || png.data[(((png.height - 1) * png.width + x) * 4) + 3]) fail(`frame ${index + 1} has horizontal edge alpha`)
  for (let y = 1; y < png.height - 1; y += 1) if (png.data[((y * png.width) * 4) + 3] || png.data[((y * png.width + png.width - 1) * 4) + 3]) fail(`frame ${index + 1} has vertical edge alpha`)
}
if (scales.size !== 1) fail('walk frames no longer use one shared scale')
const heights = frames.map((frame) => frame.opaqueHeight)
if (Math.max(...heights) - Math.min(...heights) > 6) fail('gait height variation exceeds six high-resolution pixels')

const stripPath = path.join(ROOT, register.animation.strip.file)
if (sha256(stripPath) !== register.animation.strip.sha256) fail('strip hash changed')
const strip = PNG.sync.read(fs.readFileSync(stripPath))
if (strip.width !== 2048 || strip.height !== 320) fail('strip geometry changed')
for (let frame = 0; frame < 8; frame += 1) {
  const expected = framePngs[frame]
  for (let y = 0; y < 320; y += 1) {
    const actualStart = ((y * strip.width) + frame * 256) * 4
    const expectedStart = y * 256 * 4
    if (!strip.data.subarray(actualStart, actualStart + 1024).equals(expected.data.subarray(expectedStart, expectedStart + 1024))) fail(`strip frame ${frame + 1} disagrees with source frame`)
  }
}
const sidecarPath = path.join(ROOT, register.animation.strip.sidecar)
if (sha256(sidecarPath) !== register.animation.strip.sidecarSha256) fail('sidecar hash changed')
const sidecar = JSON.parse(fs.readFileSync(sidecarPath, 'utf8')) as Record<string, any>
for (const [key, value] of Object.entries({ w: 32, h: 40, density: 8, frames: 8, fps: 8 })) if (sidecar[key] !== value) fail(`sidecar ${key} changed`)
if (sidecar.sha256 !== sha256(stripPath) || sidecar.rootMotion?.speedLogicalPixelsPerSecond !== 21) fail('strip/sidecar root-motion agreement changed')

const palette = register.palette as Record<string, any>
for (const key of ['capBlue', 'jumperBlue', 'trouserNavy', 'bootNavy']) {
  const samples = palette.frames.map((frame: Record<string, number[]>) => frame[key])
  for (let channel = 0; channel < 3; channel += 1) {
    const values = samples.map((sample: number[]) => sample[channel])
    if (Math.max(...values) - Math.min(...values) > 12) fail(`${key} palette flashes across the walk`)
    const reference = palette.approvedSideReference[key][channel]
    if (values.some((value: number) => Math.abs(value - reference) > 15)) fail(`${key} diverges from approved side palette`)
  }
}
const loopSeam = (register.continuity as Record<string, any>[]).find((item) => item.fromFrame === 8 && item.toFrame === 1)
if (!loopSeam || Math.abs(loopSeam.opaqueHeightDelta) > 5 || Math.abs(loopSeam.opaqueWidthDelta) > 10 || Math.abs(loopSeam.alphaCentroidDelta[0]) > 5 || Math.abs(loopSeam.alphaCentroidDelta[1]) > 5 || loopSeam.opaqueAreaRatio < 0.95 || loopSeam.opaqueAreaRatio > 1.05) fail('F8→F1 loop continuity bound failed')
if (register.animation?.rootMotion?.bakedIntoStrip !== false || register.animation?.rootMotion?.speedHighResolutionPixelsPerSecond !== 168 || register.animation?.rootMotion?.beginsAndEndsFullyHidden !== true) fail('root-motion contract changed')
for (const flag of ['sharedScaleOnly', 'everySourceCellHasTransparentEdge', 'everyOutputCellHasTransparentEdge', 'stripMatchesFrames', 'sidecarMatchesStrip', 'leftWalkDeferredToDeterministicMirror']) if (register.validation?.[flag] !== true) fail(`${flag} validation changed`)
for (const flag of ['productionSpritesChanged', 'runtimeManifestChanged', 'workbenchFinalChanged']) if (register.validation?.[flag] !== false) fail(`${flag} boundary changed`)
if (register.approvalBoundary?.walkV1Approved !== false || register.approvalBoundary?.walkStopApproved !== false || register.approvalBoundary?.finalLaneEntryAllowed !== false || register.approvalBoundary?.productionPromotionAllowed !== false) fail('approval boundary changed')

for (const evidence of Object.values(register.evidence) as Record<string, any>[]) if (!fs.existsSync(path.join(ROOT, evidence.file)) || sha256(path.join(ROOT, evidence.file)) !== evidence.sha256) fail(`evidence missing or changed: ${evidence.file}`)
for (const item of [...frames, register.animation.strip, ...Object.values(register.evidence) as Record<string, any>[]]) {
  const publicAsset = fs.readdirSync(path.join(PUBLIC, 'assets')).find((name) => name.includes(item.sha256.slice(0, 16)))
  if (!publicAsset || sha256(path.join(PUBLIC, 'assets', publicAsset)) !== item.sha256) fail(`public asset missing for ${item.file}`)
}
const html = fs.readFileSync(path.join(PUBLIC, 'index.html'), 'utf8')
for (const phrase of ['Keeper Prime Walk V1 · right-facing', 'Finished-art walk draft · awaiting visual approval', 'Previous frame', 'Next frame', 'Exact proposed game display size', 'Moving route', 'begins and ends fully hidden', 'Current production versus Walk V1', 'Current production · unchanged', 'Nothing has entered Final or production', 'proposes only the right-facing walk loop']) if (!html.includes(phrase)) fail(`public review omits ${phrase}`)
const script = html.split('<script>')[1]?.split('</script>')[0]
if (!script) fail('public playback script missing')
new Function(script)

console.log('Keeper Prime Walk V1 verified: 8 isolated smooth poses, one shared scale, stable standard palette, exact strip/sidecar agreement, bounded loop seam, synchronized large/game views and no promotion.')
