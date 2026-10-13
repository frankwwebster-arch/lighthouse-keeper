#!/usr/bin/env node
/** Verify the reversible Keeper Prime Walk V3 opposing-arm draft. */
import crypto from 'node:crypto'
import fs from 'node:fs'
import path from 'node:path'
import { PNG } from 'pngjs'

const ROOT = path.resolve(import.meta.dirname, '..')
const PACK = path.join(ROOT, 'art/drafts/keeper-prime-walk-2026-10-13-v3')
const PUBLIC = path.join(ROOT, 'public/keeper-review/keeper-prime-walk-v3')
const REGISTER = path.join(PACK, 'batch-register.json')
const PREFIX = '/keeper-review/keeper-prime-walk-v3/assets/'
const SOURCE_HASH = 'a1fe0f983f83e8f66154fc0522617e84c76699759ad3bb10a979089770070209'
const FEEDBACK = "the arm swing isn't quite right, his left arm remains far more static than the right"
const fail = (message: string): never => { throw new Error(`Keeper Prime Walk V3: ${message}`) }
const sha256 = (file: string) => crypto.createHash('sha256').update(fs.readFileSync(file)).digest('hex')

for (const file of [REGISTER, path.join(PACK, 'HANDOFF.md'), path.join(PACK, 'PROMPT_LOG.md'), path.join(PUBLIC, 'index.html')]) if (!fs.existsSync(file)) fail(`missing ${path.relative(ROOT, file)}`)
const register = JSON.parse(fs.readFileSync(REGISTER, 'utf8')) as Record<string, any>
if (register.batchId !== 'keeper-prime-walk-2026-10-13-v3' || register.status !== 'draft-opposing-arm-walk-v3-awaiting-visual-approval' || register.userFeedback !== FEEDBACK) fail('batch identity, status or feedback changed')
const source = path.join(ROOT, register.generation?.selectedSource?.file)
if (sha256(source) !== SOURCE_HASH || register.generation.selectedSource.sha256 !== SOURCE_HASH) fail('selected source changed')
if (register.generation?.poseGuide?.nearArmColour !== 'cyan' || register.generation?.poseGuide?.farArmColour !== 'magenta' || register.generation?.poseGuide?.retainedInFinalPixels !== false) fail('rig arm-guide contract changed')
for (const key of ['walkV1', 'walkV2RoutingWrapper']) {
  const prior = register.priorCandidates?.[key]
  if (!prior || sha256(path.join(ROOT, prior.register)) !== prior.sha256 || prior.artworkChanged !== false) fail(`${key} provenance changed`)
}
const previousFrames = register.previousWalkV1FrameComparison as Record<string, any>[]
if (!Array.isArray(previousFrames) || previousFrames.length !== 8) fail('Walk V1 frame comparison inventory changed')
for (const item of previousFrames) {
  const source = path.join(ROOT, item.source)
  const published = path.join(ROOT, item.public)
  if (sha256(source) !== item.sourceSha256 || sha256(published) !== item.publicSha256 || item.sourceSha256 !== item.publicSha256 || item.byteIdentical !== true) fail(`Walk V1 comparison frame ${item.frame} changed`)
}
const rejected = register.generation?.rejectedSources as Record<string, any>[]
if (!Array.isArray(rejected) || rejected.length !== 8) fail('rejected-source inventory changed')
for (const item of rejected) if (!fs.existsSync(path.join(ROOT, item.file)) || sha256(path.join(ROOT, item.file)) !== item.sha256) fail(`rejected source changed: ${item.file}`)

const frames = register.frames as Record<string, any>[]
if (frames.length !== 8 || register.animation?.frames !== 8 || register.animation?.fps !== 8 || register.animation?.loop !== true) fail('animation contract changed')
const scales = new Set<number>()
const pngs = frames.map((frame, index) => {
  const file = path.join(ROOT, frame.file)
  if (sha256(file) !== frame.sha256 || frame.edgeAlphaPixels !== 0 || frame.opaqueBoundsExclusive[3] !== 316) fail(`frame ${index + 1} hash/floor/gutter changed`)
  scales.add(frame.registration?.sharedScale)
  const png = PNG.sync.read(fs.readFileSync(file))
  if (png.width !== 256 || png.height !== 320) fail(`frame ${index + 1} geometry changed`)
  for (let x = 0; x < png.width; x += 1) if (png.data[x * 4 + 3] || png.data[(((png.height - 1) * png.width + x) * 4) + 3]) fail(`frame ${index + 1} horizontal edge alpha`)
  for (let y = 1; y < png.height - 1; y += 1) if (png.data[(y * png.width) * 4 + 3] || png.data[(y * png.width + png.width - 1) * 4 + 3]) fail(`frame ${index + 1} vertical edge alpha`)
  return png
})
if (scales.size !== 1) fail('frames no longer use one shared scale')

const stripPath = path.join(ROOT, register.animation.strip.file)
if (sha256(stripPath) !== register.animation.strip.sha256) fail('strip changed')
const strip = PNG.sync.read(fs.readFileSync(stripPath))
if (strip.width !== 2048 || strip.height !== 320) fail('strip geometry changed')
for (let frame = 0; frame < 8; frame += 1) for (let y = 0; y < 320; y += 1) {
  const actual = strip.data.subarray(((y * strip.width) + frame * 256) * 4, ((y * strip.width) + frame * 256) * 4 + 1024)
  const expected = pngs[frame].data.subarray(y * 1024, y * 1024 + 1024)
  if (!actual.equals(expected)) fail(`strip frame ${frame + 1} disagrees with source frame`)
}
const sidecarPath = path.join(ROOT, register.animation.strip.sidecar)
if (sha256(sidecarPath) !== register.animation.strip.sidecarSha256) fail('sidecar changed')
const sidecar = JSON.parse(fs.readFileSync(sidecarPath, 'utf8')) as Record<string, any>
if (sidecar.sha256 !== sha256(stripPath) || sidecar.frames !== 8 || sidecar.fps !== 8 || sidecar.w !== 32 || sidecar.h !== 40 || sidecar.density !== 8) fail('strip/sidecar agreement changed')

for (const flag of ['approvedRigOpposingArmGuideUsed', 'sharedScaleOnly', 'everySourceCellHasTransparentEdge', 'everyOutputCellHasTransparentEdge', 'stripMatchesFrames', 'sidecarMatchesStrip']) if (register.validation?.[flag] !== true) fail(`${flag} changed`)
for (const flag of ['walkV1FilesChanged', 'productionSpritesChanged', 'runtimeManifestChanged', 'workbenchFinalChanged']) if (register.validation?.[flag] !== false) fail(`${flag} boundary changed`)
for (const flag of ['walkV3Approved', 'walkStopApproved', 'finalLaneEntryAllowed', 'productionPromotionAllowed']) if (register.approvalBoundary?.[flag] !== false) fail(`${flag} approval boundary changed`)

for (const item of [...frames, register.animation.strip, ...Object.values(register.evidence) as Record<string, any>[]]) {
  const publicAsset = fs.readdirSync(path.join(PUBLIC, 'assets')).find((name) => name.includes(item.sha256.slice(0, 16)))
  if (!publicAsset || sha256(path.join(PUBLIC, 'assets', publicAsset)) !== item.sha256) fail(`public asset missing for ${item.file}`)
}
const htmlPath = path.join(PUBLIC, 'index.html')
if (register.reviewPage?.sha256 !== sha256(htmlPath) || register.reviewPage?.assetPrefix !== PREFIX || register.reviewPage?.relativeAssetUrls !== false) fail('review page record changed')
const html = fs.readFileSync(htmlPath, 'utf8')
for (const forbidden of ['src="assets/', 'const frames=["assets/']) if (html.includes(forbidden)) fail(`relative URL remains: ${forbidden}`)
for (const phrase of ['Keeper Prime Walk V3 · right-facing', 'Opposing-arm walk correction · awaiting visual approval', 'both arms must now swing visibly and naturally in opposition', 'Walk V1 versus Walk V3 · same frame', 'exact 128 × 160 proposed game size', 'nothing has entered Final or production']) if (!html.includes(phrase)) fail(`review page omits ${phrase}`)
const script = html.split('<script>')[1]?.split('</script>')[0]
if (!script) fail('playback script missing')
new Function(script)

console.log('Keeper Prime Walk V3 verified: rig-guided eight-pose opposing-arm candidate, shared scale/floor, transparent gutters, exact strip/sidecar/public agreement and no promotion.')
